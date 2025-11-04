import streamlit as st
from llm_backend import run_agent
from dotenv import load_dotenv
import uuid

load_dotenv()

st.set_page_config(page_title="AI Tool Chatbot", page_icon="🤖", layout="wide")

st.title("🤖 ChatGPT Lite")

# --- SESSION STATE INITIALIZATION ---
if "chat_sessions" not in st.session_state:
    st.session_state["chat_sessions"] = {}  # {uuid: {"title": str, "messages": list}}
if "current_chat" not in st.session_state:
    st.session_state["current_chat"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# --- FUNCTION TO START A NEW CHAT ---
def start_new_chat():
    chat_id = str(uuid.uuid4())[:8]  # short unique ID
    st.session_state["current_chat"] = chat_id
    st.session_state["chat_sessions"][chat_id] = {
        "title": f"New Chat {len(st.session_state['chat_sessions']) + 1}",
        "messages": []
    }
    st.session_state["messages"] = []
    st.rerun()


# --- SIDEBAR ---
with st.sidebar:
    st.title("💬 Chat History")

    if st.session_state["chat_sessions"]:
        # Show chat sessions (title + UUID)
        chat_titles = [
            f"{info['title']} ({cid})"
            for cid, info in st.session_state["chat_sessions"].items()
        ]
        selected_chat = st.selectbox(
            "Select a chat to resume:",
            options=["🆕 Start New Chat"] + chat_titles,
            index=0
        )

        if selected_chat == "🆕 Start New Chat":
            if st.button("➕ Create New Chat"):
                start_new_chat()
        else:
            chat_id = selected_chat.split("(")[-1].replace(")", "")
            if chat_id != st.session_state["current_chat"]:
                st.session_state["current_chat"] = chat_id
                st.session_state["messages"] = st.session_state["chat_sessions"][chat_id]["messages"]
                st.rerun()
    else:
        st.info("No chat history found.")
        if st.button("➕ Start Chat"):
            start_new_chat()

    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    model = st.selectbox("Choose Model:", ["GPT-3.5", "GPT-4", "Custom Model"])
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info("This chatbot demonstrates a simple conversational AI interface using Streamlit.")
    st.markdown("👨‍💻 **Developer:** Jawed Ali")
    st.markdown("📅 **Version:** 1.0.0")
    st.markdown("---")
    if st.button("🗑️ Clear Current Chat"):
        if st.session_state["current_chat"]:
            st.session_state["chat_sessions"][st.session_state["current_chat"]]["messages"] = []
        st.session_state["messages"] = []
        st.rerun()


# --- DISPLAY MESSAGES ---
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --- USER INPUT ---
if prompt := st.chat_input("Ask me anything..."):
    # Ensure there's a current chat
    if not st.session_state["current_chat"]:
        start_new_chat()

    # Append user message
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text = run_agent(st.session_state["messages"])
            st.write_stream(iter(response_text))

    # Save AI response
    st.session_state["messages"].append({"role": "assistant", "content": response_text})

    # Update chat session
    current_id = st.session_state["current_chat"]
    st.session_state["chat_sessions"][current_id]["messages"] = st.session_state["messages"]

    # Update title to first user message
    if st.session_state["chat_sessions"][current_id]["title"].startswith("New Chat"):
        st.session_state["chat_sessions"][current_id]["title"] = prompt[:25] + "..."

    st.rerun()

