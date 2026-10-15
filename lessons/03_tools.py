from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / "source" /".env")
BOM_File = ROOT / "source" / "BOM.xlsx"


@tool
def list_sheets() -> list[str]:
    
    return pd.ExcelFile(BOM_File).sheet_names

model = init_chat_model("openai:gpt-4o-mini", temperature=0)
model_with_tools = model.bind_tools([list_sheets])

reply = model_with_tools.invoke("What is a BOM?")
print("content:   ", repr(reply.content))
print("tool_calls:", reply.tool_calls)
print(list_sheets.name, list_sheets.description, list_sheets.args)

for call in reply.tool_calls:
    result = list_sheets.invoke(call["args"])
    print("result:    ", result)
