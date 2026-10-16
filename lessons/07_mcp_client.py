import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv("source/.env")
SERVER = str(Path(__file__).parent/"07_bom_server.py")

async def main():
    client = MultiServerMCPClient(
        {"bom":{
            "command":sys.executable,
            "args": [SERVER],
            "transport":"stdio",
        }}
    )
    tools = await client.get_tools()
    print("tools from mcp: ", [t.name for t in tools])

    agent = create_agent(
        model = "openai:gpt-4o-mini",
        tools=tools,
        system_prompt= "You are a BOM assistant. Use the tools; never guess item data",
    )

    out =  await agent.ainvoke({
        "messages":[
            {"role": "user", "content":"which sheets are in the workbook?"},
            {"role": "user", "content":"Search 'screw' in the roofing screw sheet"}
            
        ]
    })

    print(out["messages"][-1].content)

asyncio.run(main())