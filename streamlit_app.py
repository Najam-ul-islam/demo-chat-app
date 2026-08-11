# src/streamlit_app.py

import requests
import streamlit as st


# ============================================================
# Configuration
# ============================================================

FASTAPI_URL = "http://127.0.0.1:8000"


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Azure Foundry RAG Assistant",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# Custom CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #777;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    .answer-box {
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Header
# ============================================================

st.markdown(
    '<div class="main-title">🤖 Azure Foundry RAG Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Ask questions from your Azure AI Foundry RAG agent."
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.header("Configuration")

    st.write("Backend API")

    st.code(
        FASTAPI_URL,
        language="text",
    )

    st.divider()

    st.header("Agent")

    st.success("Azure AI Foundry Agent")

    st.caption(
        "RAG retrieval and answer generation "
        "are handled by the FastAPI backend."
    )

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# Chat State
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# Display Chat History
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================
# Chat Input
# ============================================================

question = st.chat_input(
    "Ask a question about your knowledge base..."
)


# ============================================================
# Send Question
# ============================================================

if question:

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # --------------------------------------------------------
    # Call FastAPI
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Searching knowledge base..."):

            try:

                response = requests.post(
                    f"{FASTAPI_URL}/ask",
                    json={
                        "question": question
                    },
                    timeout=120,
                )

                # ------------------------------------------------
                # HTTP error
                # ------------------------------------------------

                response.raise_for_status()

                data = response.json()

                answer = data.get(
                    "answer",
                    "No answer was returned."
                )

                # ------------------------------------------------
                # Display answer
                # ------------------------------------------------

                st.markdown(answer)

                # ------------------------------------------------
                # Save assistant response
                # ------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except requests.exceptions.ConnectionError:

                error_message = (
                    "❌ Could not connect to the FastAPI backend. "
                    "Make sure the FastAPI server is running on "
                    f"{FASTAPI_URL}."
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )

            except requests.exceptions.Timeout:

                error_message = (
                    "⏱️ The request timed out while waiting "
                    "for the Azure Foundry agent."
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )

            except requests.exceptions.HTTPError:

                try:
                    error_detail = response.json()
                except Exception:
                    error_detail = response.text

                error_message = (
                    f"❌ FastAPI returned an error:\n\n"
                    f"{error_detail}"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )

            except Exception as e:

                error_message = (
                    f"❌ Unexpected error: {str(e)}"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )