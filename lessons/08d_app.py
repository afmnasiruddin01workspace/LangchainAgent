import asyncio
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver

from access import UserContext, check_login, guard_tools
from users import verify_login

load_dotenv(Path(__file__).parent.parent / "source" / ".env")
SERVER = str(Path(__file__).parent / "07_bom_server.py")

st.set_page_config(page_title="BOM Chat")

def build_agent():
    client = MultiServerMCPClient(
        {"bom": {"command": sys.executable, "args": [SERVER], "transport": "stdio"}}
    )
    return create_agent(
        model="openai:gpt-4o-mini",
        tools=asyncio.run(client.get_tools()),
        system_prompt="You are a BOM assistant. Use the tools; never guess item data.",
        middleware=[check_login, guard_tools],
        context_schema=UserContext,
        checkpointer=InMemorySaver(),
    )

# ---- login screen ----
if "ctx" not in st.session_state:
    st.title("BOM Chat - Login")
    with st.form("login"):
        name = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in")
    if submitted:
        role = verify_login(name.strip(), password)
        if role:
            st.session_state.ctx = UserContext(user=name.strip(), role=role)
            st.session_state.agent = build_agent()
            st.session_state.history = []
            st.rerun()
        st.error("Wrong username or password.")
    st.stop()

# ---- chat screen ----
ctx = st.session_state.ctx
st.title("BOM Chat")
st.sidebar.write(f"Logged in: **{ctx.user}** ({ctx.role})")
if st.sidebar.button("Log out"):
    st.session_state.clear()
    st.rerun()

for who, text in st.session_state.history:
    st.chat_message(who).write(text)

if q := st.chat_input("Ask about the BOM"):
    st.chat_message("user").write(q)
    out = asyncio.run(
        st.session_state.agent.ainvoke(
            {"messages": [{"role": "user", "content": q}]},
            {"configurable": {"thread_id": ctx.user}},
            context=ctx,
        )
    )
    answer = out["messages"][-1].content
    st.chat_message("assistant").write(answer)
    st.session_state.history += [("user", q), ("assistant", answer)]

    