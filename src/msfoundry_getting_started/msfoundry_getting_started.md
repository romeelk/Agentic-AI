# Microsodt Foundry

The Microsoft Foundry portal is Microsoft's enterprise AI platform that provides users the ability to 
- Deploy numerous LLM models 
- Provide access to tools for agents
- Develop and host your AI applications using various Agent SDKs
- Observability of your agents
- Run Agent evaluations

## Setting up Microsoft Foundry resources

Follow this Microsoft article to setup your first MS Foundry project resources.

https://learn.microsoft.com/en-us/azure/foundry/tutorials/quickstart-create-foundry-resources?tabs=azurecli

You will need this so that you can deploy LLM models to test with the MS Foundry agent examples in this repository.


Microsoft Foundry organizes your access to models, agents and other related resources using Foundry projects.

When you deploy a Microsoft Foundry resource you essentially get a single unified Azure  resource acting as a shared management and billing boundary for security, access control, and endpoints.

You then create multiple projects under the single Foundry resource.  This allows you to orgnanize by project for  different use cases, teams, or applications.

Visually this structure looks like:

```
├── foundry_resource
│   ├── foundry_project_1
│   └── foundry_project_2
```

## Types of agents

There are essentially three types of Agent that can be created in Microsoft Foundry new portal experience.

- Prompt Agents via MS foundry Portal. These agents are developed using Foundry SDK. This is an API that exposes clients 
to interact with Foundry Service using primitives that allow you to interact with AI foundry project, and wraps OpenAI APIs to interact with chats, responeses, maintain conversations across sessions.
- Hosted Agents (Preview) - Agents developed locally using Micrsofts new Agent Framework SDK
- Workflow Agents - via MS Foundry Portal - Workflows are UI-based tools in Microsoft Foundry. Use them to create declarative, predefined sequences of actions that orchestrate agents and business logic in a visual builder.

Workflows Agents are ideal for scenarios where you need to:

- Orchestrate multiple agents in a repeatable process.
- Add branching logic (for example, if/else) and variable handling without writing code.
- Create human-in-the-loop steps (for example, approvals or clarifying questions).





