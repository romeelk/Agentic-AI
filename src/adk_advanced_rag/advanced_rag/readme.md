# Introduction

This agent example demonstrates the ability to use agent as a tool
to decide on what RAG source to use in response to the user query.

It is based on the google tutorial:
https://codelabs.developers.google.com/codelabs/production-ready-ai-with-gc/7-advanced-agent-capabilities/building-agents-with-retrieval-augmented-generation#0

It has two sources of grounding:
- Microsoft q2 report via web url:https://www.microsoft.com/en-us/investor/earnings/fy-2026-q2/press-release-webcast
- Structured csv file of the last two weeks of stock prices starting and closing prices

