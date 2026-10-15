from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from bom_tools import list_sheets, preview_sheet, search_item

load_dotenv(Path(__file__).parent.parent / "source" / ".env"   )
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[
        list_sheets,
        preview_sheet,
        search_item,
    ],
    checkpointer=InMemorySaver(),
    system_prompt="You are a BOM assistant. Use the tools; never guess item data.",
)

def ask(text: str, thread: str)-> str:
    config = {"configurable": {"thread_id": thread}}
    result = agent.invoke({"messages": [{"role": "user", "content": text}]}, config)
    return result["messages"][-1].content

print(ask("what sheet is called 'BOM (2)'? Preview its first 5 rows.", "alice"))
print("-"*50)
print(ask("what was the sheet i just asked about?", "alice"))
print("-"*50)
print (ask("what was the sheet i just asked about?", "bob"))

