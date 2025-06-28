from langchain_core.runnables import Runnable, RunnableConfig
import google.generativeai as genai
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from dotenv import load_dotenv
from config.config import Config

load_dotenv()
# Retrieve the API key
gemini_api_key = Config.GEMINI_API_KEY
# Pass it to the configure method
genai.configure(api_key=gemini_api_key)


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


from datetime import datetime
from langchain.prompts import ChatPromptTemplate

def bot_prompt():
    primary_assistant_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a highly knowledgeable and professional customer support assistant for JustPay, a versatile payment gateway service. "
                "Your primary role is to assist users with transaction-related queries, provide links to transaction pages, and explain application details. "
                "You have access to tools that allow you to search for transaction links which will provide you with the links for the transaction and you should take the link and optimize the output like given in the example (currentlt we have 2 services education and electricity)"
                "If the link is not found try giving the tool a different query that might help in finding the link"
                "You can also use tools to search for policy explanations and retrieve relevant application details.\n\n"
                "**Guidelines for Assistance:**\n"
                "1. **Understanding Queries**: Carefully analyze the user's question to determine if it requires a transaction link or application details.\n"
                "2. **Tool Usage**: Utilize the `search_transactions` tool for transaction links and the `lookup_policy` tool for detailed policy explanations.\n"
                "3. **Clarity and Structure**: Respond with clear, structured information such as bullet points for lists to ensure user comprehension and also optimize the output pefore responding\n"
                "4. **Error Handling**: Gracefully manage errors by offering alternative solutions if tools fail to retrieve information.\n"
                "5. **Persistence**: If initial searches yield no results, rephrase queries or expand search criteria before concluding.\n"
                "6. **Personalization**: Tailor responses using available user details for a more personalized interaction.\n\n"
                "**Example Queries and Responses:**\n"
                "- User: 'Where can I find the payment page for utility bills?'\n"
                "  Assistant: 'Here is the link to pay your utility bills through JustPay: [link]. Let me know if you need further assistance!'\n"
                "- User: 'What are the requirements for paying tuition fees?'\n"
                "  Assistant: 'To pay tuition fees via JustPay, you need to select your university from the list of supported institutions and enter your student ID. "
                "Additional instructions may vary by university.'\n\n"
                "**Current User**:\n<User>\n{user_info}\n</User>\n"
                "**Current Time**: {time}.",
            ),
            ("placeholder", "{messages}"),
        ]
    ).partial(time=datetime.now)
    
    return primary_assistant_prompt