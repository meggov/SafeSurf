from typing import List, Union
from dotenv import load_dotenv, find_dotenv
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
from langchain.llms import LlamaCpp
from langchain import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import os
import streamlit as st
import configparser
from streamlit.components.v1 import html, iframe


os.environ["OPENAI_API_KEY"] = "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"
openAI_key = os.environ.get("OPENAI_API_KEY")

system = """Please imagine that you are chatting with a user who is between the ages of 7 to 12 years old. Your task is to role-play as a stranger the user has just met on the Internet. Hold a natural, friendly conversation with the user, mirroring a typical conversation on social media chats. While you are chatting with the user, naturally intersperse the following scenarios:

Asking the user for their phone number to chat via iMessage 
Asking the user for their home address to send them a gift they would like 
Requesting the user's bank account information for a game 
Asking the user to send pictures of themself 
Inviting the user to meet for a sweet treat 

During these interactions, you must engage in dialogue with the user in a convincing, natural manner. If the child agrees to any of the requests, you must immediately respond with "Uh oh, you shared personal information with a stranger and lost a life! Type “Learn More” to learn why." If the user responds with “Learn More,” explain why sharing information with a stranger online is dangerous for a child in a 25-50 word message. 

Please carefully observe the dialogue between yourself and the child in these scenarios. Remember to keep in mind the age of the child and the importance of teaching them about online safety. Additionally, remember to have a natural conversation that responds to the user’s input. 
"""


def init_page() -> None:
    st.set_page_config(
        page_title="SafeSurf")
    st.header("SafeSurf")
    st.sidebar.title("Options")


def init_messages() -> None:
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(
                content=system)]
        st.session_state.costs = []

def select_llm() -> Union[ChatOpenAI, LlamaCpp]:

    model_name = st.sidebar.radio("Choose LLM:",
                                  ("gpt-3.5-turbo-0613", "gpt-4"))
    temperature = st.sidebar.slider("Temperature:", min_value=0.5,
                                    max_value=1.0, value=0.0, step=0.01)
    if model_name.startswith("gpt-"):
        return ChatOpenAI(temperature=temperature, model_name=model_name,
                          openai_api_key=openAI_key)
    

def get_answer(llm, messages) -> tuple[str, float]:

    if isinstance(llm, ChatOpenAI):
        with get_openai_callback() as cb:
            answer = llm(messages)
        return answer.content, cb.total_cost
  

def find_role(message: Union[SystemMessage, HumanMessage, AIMessage]) -> str:
    """
    Identify role name from langchain.schema object.
    """
    if isinstance(message, SystemMessage):
        return "system"
    if isinstance(message, HumanMessage):
        return "user"
    if isinstance(message, AIMessage):
        return "assistant"
    raise TypeError("Unknown message type.")


def convert_langchainschema_to_dict(
        messages: List[Union[SystemMessage, HumanMessage, AIMessage]]) \
        -> List[dict]:
    """
    Convert the chain of chat messages in list of langchain.schema format to
    list of dictionary format.
    """
    return [{"role": find_role(message),
             "content": message.content
             } for message in messages]



def main() -> None:
    _ = load_dotenv(find_dotenv())

    init_page()
    llm = select_llm()
    init_messages()

    # Supervise user input
    if user_input := st.chat_input("Start typing..."):
        st.session_state.messages.append(HumanMessage(content=user_input))
        st.session_state.messages.append(SystemMessage(content=system))
        with st.spinner("Derek is typing ..."):
            answer, cost = get_answer(llm, st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=answer))
        st.session_state.costs.append(cost)

    # Display chat history
    messages = st.session_state.get("messages", [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)

    costs = st.session_state.get("costs", [])
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")


# streamlit run app.py
if __name__ == "__main__":
    main()