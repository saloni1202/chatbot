import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("models/gemini-2.5-pro")

# Page setup
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stChatMessage .user {
            background-color: #DCF8C6;
            color: black;
            padding: 0.5rem;
            border-radius: 1rem;
            margin: 0.5rem 0;
            max-width: 85%;
        }
        .stChatMessage .ai {
            background-color: #F1F0F0;
            color: black;
            padding: 0.5rem;
            border-radius: 1rem;
            margin: 0.5rem 0;
            max-width: 85%;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Gemini ChatBot")

# Initialize history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display messages with proper role + styling
for role, content in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(content)

# Input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # User message
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gemini response
    with st.chat_message("ai"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(user_input)
                reply = response.text
            except Exception as e:
                reply = f"❌ Error: {str(e)}"
        st.markdown(reply)

    st.session_state.chat_history.append(("ai", reply))
