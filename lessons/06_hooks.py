from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import  before_agent, wrap_tool_call
from bom_tools import list_sheets, preview_sheet, search_item

load_dotenv(Path(__file__).parent.parent / "source" / ".env")

@dataclass
class UserContext:
    user: str
    role: str

@before_agent
def check_login(state, runtime):
    ctx = runtime.context
    if ctx is None or not ctx.user:
        raise PermissionError("Not logged in")
    print(f"[hook] logged in as {ctx.user}({ctx.role})")

@wrap_tool_call
def audit_tools(request, handler):
    ctx = request.runtime.context
    print(f"[audit] {ctx.user} -> {request.tool_call['name']}({request.tool_call['args']})")
    return handler(request)

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[list_sheets, preview_sheet, search_item],
    system_prompt="You are a BOM assistant. Use the tools; never guess item data.",
    middleware=[check_login, audit_tools],
    context_schema=UserContext,
)

question = {
    "messages": [
        {"role": "user", "content": "How many sheets are in the workbook?"},
    ],
}

result = agent.invoke(question, context=UserContext(user="alice", role="viewer"))
print(result["messages"][-1].content)

print("=" * 40)
agent.invoke(question)  # no context: should be refused