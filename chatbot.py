from dotenv import load_dotenv
import os
import streamlit as st
from groq import Groq

# Load environment variables
load_dotenv()

# Streamlit page config
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Sneh's Chatbot(Aiden)")

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display existing chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_prompt = st.chat_input("💬 Ask something...")

if user_prompt:
    # Display and store user message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Build messages list for Groq (with system prompt)
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for msg in st.session_state.chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Call Groq API
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # Free model on Groq
        messages=messages,
        temperature=0.7,
    )

    assistant_response = response.choices[0].message.content

    # Store and display assistant response
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
