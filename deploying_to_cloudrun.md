# Deploy to Cloud run

To deploy the adk agent to Cloud Run use the following instructions.
This is based on the official doc:https://docs.cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-adk-service

## Prerequesites

Make sure you have the following permissions:

- gcloud services enable run.googleapis.com aiplatform.googleapis.com cloudbuild.googleapis.com
- Cloud Run Source Developer (roles/run.sourceDeveloper) on the project
- Vertex AI User (roles/aiplatform.user) on the project
- Service Account User (roles/iam.serviceAccountUser) on the service identity
- Logs Viewer (roles/logging.viewer) on the project

## Deploying from source

Run the following command from the parent folder of your agents:

```
adk_agents
├── adk_agent
│   ├── __init__.py
│   └── agent.py
├── currency_agent
│   ├── __init__.py
│   └── agent.py
├── deploying.md
└── requirements.txt

```
gcloud run deploy --source .    

```

You will be prompted to select an agent to deploy. type one of the sub agents. For example adkagent
```
Service name (adkagents):  adkagent

Once deployed gcloud cli should print

```
Service [currencyagent] revision [currencyagent-00001-wbm] has been deployed and is serving 100 percent of traffic.
Service URL: https://currencyagent-823900990542.europe-west1.run.app
```

## Testing the deployment

To test the deployment first query the adk endpoint:

```
export serviceurl=https://currencyagent-823900990542.europe-west1.run.app
curl -X GET https://{$serviceurl/}list-apps
["adk_agent","currency_agent"]%                              
```

Then create an agent session

```
curl -X POST $serviceurl/apps/currency_agent/users/u_123/sessions/s_123 -H "Content-Type: application/json" -d '{"key1": "value1", "key2": 42}'
```

Query the currency agent to convert $1 USD to GBP

```
 curl -X POST https://currencyagent-823900990542.europe-west1.run.app/run -H "Content-Type: application/json" -d "{\"appName\": \"currency_agent\",\"userId\": \"u_123\",\"sessionId\": \"s_123\",\"newMessage\": { \"role\": \"user\", \"parts\": [{ \"text\": \"What is 1 USD worth as GBP today\" }]}}"
```