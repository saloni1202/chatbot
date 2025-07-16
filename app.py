import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Model
model = genai.GenerativeModel("models/gemini-2.5-pro")

# Page setup
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Chatbot")

# Custom CSS for clean interface
st.markdown("""
    <style>
        .block-container { padding: 2rem 2rem; }
        .stChatMessage.user .stMarkdown { background: #dcf8c6; border-radius: 10px; padding: 8px 16px; }
        .stChatMessage.model .stMarkdown { background: #f1f0f0; border-radius: 10px; padding: 8px 16px; }
    </style>
""", unsafe_allow_html=True)

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.experimental_rerun()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display past messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["parts"])

# Chat input
user_input = st.chat_input("Ask Anything")

if user_input:
    # Show user input
    st.session_state.chat_history.append({"role": "user", "parts": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate reply from Gemini
    with st.chat_message("model"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(st.session_state.chat_history)
                reply = response.text
            except Exception as e:
                reply = f"❌ Error: {str(e)}"
        st.markdown(reply)

    st.session_state.chat_history.append({"role": "model", "parts": reply})

