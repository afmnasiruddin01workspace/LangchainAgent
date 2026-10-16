# LangchainAgent

A learning project for building LangChain / LangGraph agents, step by step, on top of an Excel BOM workbook.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Put your `OPENAI_API_KEY` in `source/.env` and the BOM workbook at `source/BOM.xlsx` (both git-ignored where sensitive).

## Lessons (`lessons/`)

| File | Topic |
|------|-------|
| `01_model.py` | Calling a chat model |
| `02_messages.py` | Message types |
| `03_tools.py`, `03b_test_tools.py` | Defining and testing tools |
| `04_agent.py` | `create_agent` |
| `05_memory.py` | Conversation memory (checkpointer) |
| `06_hooks.py` | Middleware hooks |
| `07_bom_server.py`, `07_mcp_client.py` | BOM tools exposed over MCP, consumed by an agent |
| `08b_test_access.py` | Testing role-based access rules |
| `08c_secure_agent.py` | CLI agent with login + role-based tool guard |
| `08d_app.py` | Streamlit chat UI with login |
| `bom_tools.py`, `access.py`, `users.py` | Shared helpers (BOM tools, access rules, password auth) |

## Running

```bash
python lessons/users.py                 # create demo users (writes users.json)
python lessons/08c_secure_agent.py      # CLI chat
streamlit run lessons/08d_app.py        # web chat
```

## License

Practice / learning project.
