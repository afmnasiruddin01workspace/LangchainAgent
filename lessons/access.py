from dataclasses import dataclass
from langchain.agents.middleware import  before_agent, wrap_tool_call
from langchain_core.messages import ToolMessage


ACCESS = {
    "admin":  None,
    "viewer": ["HIL vatable", "Raw material"],
    "packing": ["Master carton BOM", "roofing screw"],
}


def allowed_for(role: str):
    return ACCESS.get(role, [])


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

def decide(ctx, name, args, call_id):
    """Return a ToolMessage to answer/deny the call, or None to let it run."""
    allowed = allowed_for(ctx.role)
    print(f"[audit] {ctx.user}({ctx.role}) -> {name}({args})")

    if allowed is None:  # admin
        return None
    if name == "list_sheets":
        return ToolMessage(content="\n".join(allowed), tool_call_id=call_id)

    sheet = args.get("sheet", "").strip()
    if not sheet:
        msg = f"name one of your sheets: {allowed}"
    elif sheet not in allowed:
        msg = f"sheet '{sheet}' is not allowed for role {ctx.role}"
    else:
        return None
    print(f"[deny] {msg}")
    return ToolMessage(content=f"Access denied: {msg}", tool_call_id=call_id)


@wrap_tool_call
async def guard_tools(request, handler):
    call = request.tool_call
    denied = decide(request.runtime.context, call['name'], call['args'], call['id'])
    return denied if denied is not None else await handler(request)


