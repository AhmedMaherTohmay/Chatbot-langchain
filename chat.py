#Python files
from policy import lookup_policy
from search import search_transactions
from utils import create_tool_node_with_fallback
from prompt import Assistant, bot_prompt

######################################### LLM #########################################
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

# Configure the API key
# groq_api_key='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'
gemini='AIzaSyBiJbXUIdGeupUaIZx1y1DxRZSiHdZFDtY'
genai.configure(api_key=gemini)

# using gemnini api
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=gemini)
part_1_tools = [search_transactions, lookup_policy]
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

# Let's create an example conversation a user might have with the assistant
tutorial_questions = [
    "Hi there, can you tell me about yourself?",
    "Hi there, I cannot find the video transaction page can you provide me with it's link?",
    "Can you tell me about the app",
]

# Update with the backup file so we can restart from the original place in each section
thread_id = str(uuid.uuid4())

config = {
    "configurable": {
        # Checkpoints are accessed by thread_id
        "thread_id": thread_id,
    }
}

def llm_response(message: str) -> str:
    response = part_1_graph.invoke(
        {"messages": [("user", message)]},
        config=config,
    )

    # Extract and print the assistant's response
    assistant_response = response["messages"][-1].content
    return assistant_response


# for i in range(2):
#     # Initialize the graph with the first question
#     print("User: ", end='')
#     user_question = input()
#     response = part_1_graph.invoke(
#         {"messages": [("user", user_question)]},
#         config=config,
#     )

#     # Extract and print the assistant's response
#     assistant_response = response["messages"][-1].content
#     print(f"Assistant: {assistant_response}\n")


# # Simulate the conversation
# for question in tutorial_questions:
#     print(f"User: {question}")

#     # Invoke the graph with the user's question
#     response = part_1_graph.invoke(
#         {"messages": [("user", question)]},
#         config=config,
#     )

#     # Extract and print the assistant's response
#     assistant_response = response["messages"][-1].content
#     print(f"Assistant: {assistant_response}\n")