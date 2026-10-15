from pathlib import Path
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv(Path(__file__).parent.parent / "source" / ".env")
model = init_chat_model("openai:gpt-4o-mini", temperature=0)
messages = [
    SystemMessage(content="You are a BOM assistant for a manufacturing company. Answer in one short sentence."),
    HumanMessage(content="What is a raw material?")
]
reply = model.invoke(messages)
print(reply.content)

# messages.append(reply)
messages.append(HumanMessage(content="Give me an example from roofing screws."))

reply2 = model.invoke(messages)
print(reply2.content)
print(len(messages))
