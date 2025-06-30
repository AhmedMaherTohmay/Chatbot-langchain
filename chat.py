#Python Packages
from tools import App_Details, search_transactions
from utils import create_tool_node_with_fallback
from prompt import Assistant, bot_prompt
from config.config import Config

######################################### LLM #########################################
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
# Retrieve the API key
gemini_api_key = Config.GEMINI_API_KEY
# Pass it to the configure method
genai.configure(api_key=gemini_api_key)

# using gemnini api
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=gemini_api_key)
part_1_tools = [search_transactions, App_Details]
part_1_assistant_runnable = bot_prompt() | llm.bind_tools(part_1_tools)

######################################### Graph #########################################
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Define nodes: these do the work
builder = StateGraph(State)
builder.add_node("assistant", Assistant(part_1_assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(part_1_tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

# The checkpointer lets the graph persist its state
# this is a complete memory for the entire graph.
memory = MemorySaver()
part_1_graph = builder.compile(checkpointer=memory)

######################################### Output #########################################
import uuid
from langchain_core.messages.ai import AIMessage

# Update with the backup file so we can restart from the original place in each section
thread_id = str(uuid.uuid4())

config = {
    "configurable": {
        # Checkpoints are accessed by thread_id
        "thread_id": thread_id,
    }
}

from langchain_core.messages.ai import AIMessage
def llm_response(message: str):
    full_response = ""
    tool_calls = []

    for chunk, metadata in part_1_graph.stream({"messages": message}, config, stream_mode="messages"):
        if isinstance(chunk, AIMessage):
            full_response += chunk.content or ""

        if hasattr(chunk, "tool_calls") and chunk.tool_calls:
            tool_calls.extend(
                tool_call.get("args")
                for tool_call in chunk.tool_calls
                if tool_call.get("name") == "search_transactions"
            )

    return {
        "response": full_response,
        "tool_calls": tool_calls[0] if tool_calls else None
    }

if __name__ == "__main__":
    while True:
        print("User: ", end='')
        user_question = input()

        if user_question.lower() in ["quit", "exit", "end", 'q', 'ex']:
            print("Assistant: Goodbye! Have a great day!")
            break

        print("Assistant:")

        # Call llm_response and print the complete result
        responses = llm_response(user_question)
        for response in responses:
            # Print tool calls if any
            if "tool_calls" in response:
                print("Tool Call Arguments:", response["tool_calls"][0])
            # Print the assistant's message
            if "response" in response:
                print(response["response"])