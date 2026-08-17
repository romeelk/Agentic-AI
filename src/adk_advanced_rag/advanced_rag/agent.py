from google.adk.agents.llm_agent import Agent, LlmAgent
from google.genai.types import GenerateContentConfig 
from google.adk.tools import FunctionTool
from google.adk.tools import VertexAiSearchTool
from google.adk.tools import AgentTool
import pandas as pd
from datetime import datetime
import os


# 1. Create the Vertex AI Search tool
full_datastore_id = f"projects/{os.environ['GOOGLE_CLOUD_PROJECT']}/locations/global/collections/default_collection/dataStores/{os.environ['DATA_STORE_ID']}"
vertex_ai_search_tool = VertexAiSearchTool(
    data_store_id=full_datastore_id
)

doc_qa_agent = LlmAgent(
    name="search_and_qna_agent",
    model="gemini-2.5-flash",
    tools=[vertex_ai_search_tool],
    instruction="""You are a helpful assistant that answers questions based on information found in the document store.
    Use the search tool to find relevant information before answering.
    If the answer isn't in the documents, say that you couldn't find the information.
    """,
    description="Answers questions using a specific Vertex AI Search datastore.",
)


def convert_dataframe_to_json(data:pd.DataFrame):
    return  {
        "date":data['Date'],
        "opening_price":data['Open'],
        "closing_price":data['Close']
    }
    
[FunctionTool]
def load_msft_ticker_data(query_date:str):
    """ Loads Microsoft sample stock market data
        for the last two weeks
    """
    try:
        stock_data_df = pd.read_csv(os.path.abspath('advanced_rag/MSFT_last_two_weeks_with_ticker.csv'))

        match_stock = stock_data_df.loc[stock_data_df["Date"]==query_date].iloc[0]

        if match_stock.empty:
            return {"status":"error","error_msg":f"Could not find stock price for date:{query_date}"}
        else:
            # find row by date
            return convert_dataframe_to_json(stock_data_df.loc[stock_data_df["Date"]==query_date].iloc[0])
    except FileNotFoundError:
        return {"status": "error", "message": "Stock data file (MSFT_last_two_weeks_with_ticke.csv) not found."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
    
root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='root_agent',
    generate_content_config=GenerateContentConfig(temperature=0.,),
    description='A helpful assistant for answering user questions about Microsoft Q2 earnings and two weeks worht of Stock prices',
    tools=[AgentTool(doc_qa_agent),load_msft_ticker_data],
    instruction="""Answer user questions about Microsofts stock prices. You have been provided a file via the tool load_msft_ticker_data that lists the last two weeks of July stock listsings.' \
    If you cannot find the stock listings given a particular date, then respond That you have only data  29th June 2026 upto including 15th July 2026. You can also use doc_qa_agent tool to lookup microsoft earnings report info "
    """
)

# print(load_msft_ticker_data('2026-07-15'))