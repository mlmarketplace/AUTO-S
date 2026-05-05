import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(ROOT_DIR)

import streamlit as st
import time
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

# Import YOUR system (not LangChain wrapper)
from _phase9.agent import route_llm_with_rag
from _phase9.intent_router import classify_intent
from _phase9.feedback.feedback_store import FeedbackStore

# -----------------------------------------
# CONFIG
# -----------------------------------------
st.set_page_config(
    page_title="AUTO-S Terraform Agent",
    layout="centered"
)

st.title("AUTO-S: Terraform AI Agent")
st.caption("Evaluation + Safety + Adaptive Behaviour")

# -----------------------------------------
# SESSION STATE
# -----------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_query" not in st.session_state:
    st.session_state.last_query = None

feedback_store = FeedbackStore()

# -----------------------------------------
# SIDEBAR (EVALUATION + DEBUG)
# -----------------------------------------
st.sidebar.header("Evaluation Panel")

show_debug = st.sidebar.checkbox("Show Debug Info")

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.last_query = None

# -----------------------------------------
# DISPLAY CHAT HISTORY
# -----------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------------------
# USER INPUT
# -----------------------------------------
user_input = st.chat_input("Ask a Terraform question...")

if user_input:
    st.session_state.last_query = user_input

    # Display user
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # -----------------------------------------
    # AGENT EXECUTION (WITH TIMING)
    # -----------------------------------------
    with st.spinner("Processing..."):
        start = time.time()

        try:
            intent = classify_intent(user_input)
            parsed, raw = route_llm_with_rag(intent, user_input)

            latency = round(time.time() - start, 2)

        except Exception as e:
            parsed = {
                "status": "error",
                "message": "Agent execution failed",
                "details": str(e)
            }
            raw = None
            latency = 0

    # -----------------------------------------
    # FORMAT RESPONSE
    # -----------------------------------------
    if isinstance(parsed, dict):
        status = parsed.get("status", "unknown")
        message = parsed.get("message") or parsed.get("reason", "")
        details = parsed.get("data", "")

        response_text = f"""
**Status:** {status}

**Message:** {message}
"""

        if details:
            response_text += f"\n**Details:** `{details}`"

    else:
        response_text = str(parsed)

    response_text += f"\n\nLatency: {latency}s"

    # -----------------------------------------
    # DISPLAY RESPONSE
    # -----------------------------------------
    with st.chat_message("assistant"):
        st.markdown(response_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })

    # -----------------------------------------
    # DEBUG PANEL
    # -----------------------------------------
    if show_debug:
        st.sidebar.write("Intent:", intent)
        st.sidebar.write("Raw:", raw)

# -----------------------------------------
# FEEDBACK (PHASE 7)
# -----------------------------------------
if st.session_state.last_query:
    st.markdown("### Feedback")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Good"):
            feedback_store.add_feedback(st.session_state.last_query, "good")
            st.success("Feedback saved")

    with col2:
        if st.button("Bad"):
            feedback_store.add_feedback(st.session_state.last_query, "bad")
            st.warning("Feedback saved")

# -----------------------------------------
# PHASE 9 EVALUATION (OPTIONAL BUTTON)
# -----------------------------------------
st.sidebar.header("Run Evaluation")

if st.sidebar.button("Run Test Harness"):
    from _phase9.eval.test_harness import run_tests

    results = run_tests()

    st.sidebar.write("Results:")
    for r in results:
        st.sidebar.write(r)