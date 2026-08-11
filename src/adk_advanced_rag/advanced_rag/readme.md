# Introduction

This agent example demonstrates the ability to use agent as a tool
to decide on what RAG source to use in response to the user query.

It is based on the google tutorial:
https://codelabs.developers.google.com/codelabs/production-ready-ai-with-gc/7-advanced-agent-capabilities/building-agents-with-retrieval-augmented-generation#0

It has two sources of grounding:
- Microsoft q2 report via web url:https://www.microsoft.com/en-us/investor/earnings/fy-2026-q2/press-release-webcast
- Structured csv file of the last two weeks of stock prices starting and closing prices

## Tool usage

Two tools are defined:
- a Function that loads a csv as a panda dataframe representing MSFT stock prices for two weeks
- a search tool that uses Vertex AI data source - grounded with MSFT Q2 results pdf doc

## Performing Evals

Evaluations allow developers to test the non-dertiministic nature of LLMs in agents.

The key focus of Evals includes:

- Accuracy of responses 
- Tool trajectory - Does the agent workflow follow the expected logical sequence of Tool calls to perform a task
- This is important wherre business logic must follow a strict order 

## Creating a Golden dataset

In adk, the first step is to record your human interactions with your Agent to gather a history of conversation for a particular task.

