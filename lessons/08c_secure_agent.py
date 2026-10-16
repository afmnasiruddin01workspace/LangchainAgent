import asyncio
import sys
from getpass import getpass
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver

from access import UserContext, check_login, guard_tools
from users import verify_login

load_dotenv(Path(__file__).parent.parent / "source" / ".env")
SERVER  = str(Path(__file__).parent / "07_bom_server.py")

def login() -> UserContext:
    for _ in range(3):
        name = input("username: ").strip()
        role = verify_login(name, getpass("password: "))
        if role:
            return UserContext(user=name, role=role)
        print("Wrong username or password.")
    sys.exit("Too many failed attemts.")

async def main():
    ctx = login()
    client = MultiServerMCPClient(
        {"bom": {"command": sys.executable, "args": [SERVER], "transport": "stdio"}}
    )
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools = await client.get_tools(),
        system_prompt="You are a BOM assistant. Use the tools; never guess item data",
        middleware=[check_login, guard_tools],
        checkpointer=InMemorySaver(),
        context_schema=UserContext,
    )

    config = {"configurable": {"thread_id": ctx.user}}
    print(f"Welcome {ctx.user} ({ctx.role}). Type 'exit' to quite.")
    while True:
        q = input("you> ").strip()
        if q.lower() in {"exit","quit"}:
            break
        out = await agent.ainvoke(
            {"messages":[
                {"role":"user","content": q}
            ]},
            config,
            context=ctx
        )
        print("bot> ", out["messages"][-1].content)

asyncio.run(main())
    
          