from langchain_core.runnables import Runnable, RunnableConfig
import google.generativeai as genai
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime

gemini='AIzaSyBiJbXUIdGeupUaIZx1y1DxRZSiHdZFDtY'
genai.configure(api_key=gemini)

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            passenger_id = configuration.get("passenger_id", None)
            state = {**state, "user_info": passenger_id}
            result = self.runnable.invoke(state)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}


def bot_prompt():
    primary_assistant_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a highly knowledgeable and professional customer support assistant for PayNow, a payment gateway service. "
                "Your primary role is to assist users with transaction-related queries, provide links to transaction pages, and explain company policies. "
                "You have access to tools that allow you to search for transaction links and retrieve policy information. "
                "Always follow these guidelines:\n"
                "1. **Understand the Query**: Carefully analyze the user's question to determine if it requires a transaction link or policy information.\n"
                "2. **Use Tools Appropriately**: Use the `search_transactions` tool to find transaction links and the `lookup_policy` tool to retrieve policy details.\n"
                "3. **Be Clear and Concise**: Provide responses in a structured format. Use bullet points for lists and ensure the information is easy to understand.\n"
                "4. **Handle Errors Gracefully**: If a tool fails to retrieve information, inform the user and suggest alternative solutions.\n"
                "5. **Be Persistent**: If the initial search returns no results, rephrase the query or expand the search scope before giving up.\n"
                "6. **Personalize Responses**: Use the user's information (if available) to tailor your responses.\n"
                "\n"
                "**Example Queries and Responses**:\n"
                "- User: 'Where can I find the video transaction page?'\n"
                "  Assistant: 'Here is the link to the video transaction page: [link]. Let me know if you need further assistance!'\n"
                "- User: 'What is the baggage policy?'\n"
                "  Assistant: 'According to our policy, each passenger is allowed to check in up to two bags, each not exceeding 23 kg. Additional fees may apply for extra or overweight luggage.'\n"
                "\n"
                "**Current User**:\n<User>\n{user_info}\n</User>\n"
                "**Current Time**: {time}.",
            ),
            ("placeholder", "{messages}"),
        ]
    ).partial(time=datetime.now)
    
    return primary_assistant_prompt