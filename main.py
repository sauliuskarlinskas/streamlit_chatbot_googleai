import os
from google import genai
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

st.title("Google AI chatbot")

# Load environment variables from .env file
load_dotenv(override=True)

# Access the secret
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    st.error("API Key not found. Make sure you have set GEMINI_API_KEY in the .env file.")
    st.stop()

#Configure google genai
genai.configure(api_key=gemini_api_key)

# Create a chat model instance
model = genai.GenerativeModel("gemini-2.0-flash",)
chat_session = model.start_chat()  # Start a chat session

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
with st.container():
    st.subheader("Chat History")
    if not st.session_state.messages:
        st.write("No messages yet. Start chatting!")
    else:
        for message in st.session_state.messages:
            with st.expander(f"{message['role'].capitalize()} says:"):
                st.markdown(message["content"])

# User input
if prompt := st.text_input("You say:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Send message to the model and get the response
        response = chat_session.send_message(prompt)
        st.markdown(response.text)

    # Save assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.text})