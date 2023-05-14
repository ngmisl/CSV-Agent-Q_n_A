import os
import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from streamlit_chat import message

st.sidebar.title("OpenAI API Key")
api_key = st.sidebar.text_input("Enter your API key:", type="password")

uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

st.sidebar.title("Follow Us")
st.sidebar.markdown(
    """
    * [Web](https://ngmi.ai/)
    * [Mastodon](https://mastodon.online/@ngmi)
    * [GitHub](https://github.com/ngmisl)
    """
)

st.sidebar.title("Our Product")
st.sidebar.markdown(
    "[The Ultimate 5 ChatGPT Prompts: Simplify Your AI Experience](https://ngmi.gumroad.com/l/nobsprompts)"
)

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    st.title("CSV Agent Interaction")

    if uploaded_file:
        st.write("CSV file uploaded successfully!")

        agent = create_csv_agent(
            OpenAI(temperature=0, client=any), uploaded_file, verbose=True
        )

        # Initialize the chat history in the session_state if it doesn't exist
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_input = st.text_input("Enter your question:", key="input_field")

        if user_input:
            answer = agent.run(user_input)
            # Add the question and answer to the chat_history
            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("agent", answer))

        # Display the chat_history in a chat-like format using streamlit-chat
        for i, (sender, message_text) in enumerate(st.session_state.chat_history):
            if sender == "user":
                message(message_text, is_user=True, key=f"{i}_user")
            else:
                message(message_text, key=f"{i}")

    else:
        st.write("Please upload a CSV file.")
else:
    st.sidebar.error("Please enter your OpenAI API key.")
