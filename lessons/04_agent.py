from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from bom_tools import list_sheets, preview_sheet, search_item

load_dotenv(Path(__file__).parent.parent / "source" / ".env")

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[list_sheets, preview_sheet, search_item],
    system_prompt=(
        "You are a BOM assistant. Use the tools to answer from BOM.xlsx. "
        "Never guess item data. If the tools return nothing, say so."
    ),
)

question = "Which sheets mention 10B21, and what is one example row?"

result = agent.invoke({"messages": [{"role": "user", "content": question}]})

for m in result["messages"]:
    print(f"--- {type(m).__name__}")
    print(m.content if m.content else getattr(m, "tool_calls", ""))