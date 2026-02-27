// Copyright (c) Microsoft. All rights reserved.

using Azure.AI.Agents.Persistent;
using Azure.AI.AgentServer.AgentFramework;
using Azure.AI.AgentServer.AgentFramework.Extensions;
using Azure.Core;
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Workflows;
using Microsoft.Agents.AI.Workflows.Reflection;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;


namespace hostedrevieweragent;

internal static class WorkflowCore
{
    public static async ValueTask RunAsync(bool containerMode = false)
    {
        // Build configuration
        var configuration = new ConfigurationBuilder()
            .SetBasePath(Directory.GetCurrentDirectory())
            .AddJsonFile("appsettings.Development.json", optional: true)
            .AddEnvironmentVariables()
            .Build();

        var endpoint = 
            configuration["Azure:ProjectEndpoint"]
            ?? throw new InvalidOperationException(
                "Azure:ProjectEndpoint is required. Set it in appsettings.Development.json for local development or as Azure__ProjectEndpoint environment variable for production");
        var deployment =
            configuration["Azure:ModelDeploymentName"]
            ?? throw new InvalidOperationException(
            "Azure:ModelDeploymentName is required. Set it in appsettings.Development.json for local development or as Azure__ModelDeploymentName environment variable for containers");

        Console.WriteLine($"Using Azure AI endpoint: {endpoint}");
        Console.WriteLine($"Using model deployment: {deployment}");

        // Create credential - use ManagedIdentityCredential if MSI_ENDPOINT exists, otherwise DefaultAzureCredential
        TokenCredential credential = string.IsNullOrEmpty(Environment.GetEnvironmentVariable("MSI_ENDPOINT"))
            ? new DefaultAzureCredential()
            : new ManagedIdentityCredential();

        // Create separate PersistentAgentsClient for each agent
        var writerClient = new PersistentAgentsClient(endpoint, credential);
        var reviewerClient = new PersistentAgentsClient(endpoint, credential);

        (ChatClientAgent agent, string id)? writer = null;
        (ChatClientAgent agent, string id)? reviewer = null;

        try
        {
            // Create Foundry agents with separate clients
            writer = await CreateAgentAsync(
                writerClient,
                deployment,
                "Writer",
                "You are an excellent content writer. You create new content and edit contents based on the feedback."
            );
            reviewer = await CreateAgentAsync(
                reviewerClient,
                deployment,
                "Reviewer",
                "You are an excellent content reviewer. Provide actionable feedback to the writer about the provided content. Provide the feedback in the most concise manner possible."
            );
            Console.WriteLine();

            var workflow = new WorkflowBuilder(writer.Value.agent)
                .AddEdge(writer.Value.agent, reviewer.Value.agent)
                .WithOutputFrom(reviewer.Value.agent)
                .Build();

            if (containerMode)
            {
                await workflow.AsAgent().RunAIAgentAsync();
            }
            else
            {
                await RunInteractiveAsync(workflow);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error running workflow: {ex.Message}");
            throw;
        }
        finally
        {
            // Clean up all resources
            await CleanupAsync(writerClient, writer?.id);
            await CleanupAsync(reviewerClient, reviewer?.id);

            if (credential is IDisposable disposable)
            {
                disposable.Dispose();
            }
        }
    }

    private static async Task RunInteractiveAsync(Workflow workflow)
    {
        await using var run = await InProcessExecution
            .StreamAsync(workflow, new ChatMessage(ChatRole.User, "Create a slogan for a new electric SUV that is affordable and fun to drive."))
            .ConfigureAwait(false);

        await run.TrySendMessageAsync(new TurnToken(emitEvents: true)).ConfigureAwait(false);

        await foreach (var evt in run.WatchStreamAsync().ConfigureAwait(false))
        {
            if (evt is AgentRunUpdateEvent agentUpdate)
            {
                Console.Write(agentUpdate.Update.Text);
            }
        }
    }

    private static async Task<(ChatClientAgent agent, string id)> CreateAgentAsync(
        PersistentAgentsClient client,
        string model,
        string name,
        string instructions
    )
    {
        var agentMetadata = await client.Administration.CreateAgentAsync(
            model: model,
            name: name,
            instructions: instructions
        );

        var chatClient = client.AsIChatClient(agentMetadata.Value.Id);
        return (new ChatClientAgent(chatClient), agentMetadata.Value.Id);
    }

    private static async Task CleanupAsync(PersistentAgentsClient client, string? agentId)
    {
        if (string.IsNullOrEmpty(agentId))
        {
            return;
        }

        try
        {
            await client.Administration.DeleteAgentAsync(agentId);
        }
        catch (Exception e)
        {
            Console.WriteLine($"Cleanup failed for agent {agentId}: {e.Message}");
        }
    }
}
