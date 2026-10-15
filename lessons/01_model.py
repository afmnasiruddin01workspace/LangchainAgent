from pathlib import Path
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv(Path(__file__).parent.parent / "source" / ".env")

model = init_chat_model("openai:gpt-4o-mini", temperature=0)

for chunk in model.stream("In one sentence, what is a Bill of Materials (BOM)?"):
    print(chunk.content, end="", flush=True)
print(type(chunk).__name__)