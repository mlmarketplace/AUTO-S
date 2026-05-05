import streamlit as st
import time

from core.agent import route_llm_with_rag
from core.intent_router import classify_intent

st.set_page_config(page_title="AUTO-S Agent", layout="centered")

st.title("AUTO-S: Terraform AI Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask a Terraform question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Processing..."):
        start = time.time()

        try:
            intent = classify_intent(user_input)
            parsed, _ = route_llm_with_rag(intent, user_input)
            latency = round(time.time() - start, 2)
        except Exception as e:
            parsed = {"status": "error", "message": str(e)}
            latency = 0

    response = f"""
Status: {parsed.get("status")}

Message: {parsed.get("message", parsed.get("reason", ""))}

Latency: {latency}s
"""

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})