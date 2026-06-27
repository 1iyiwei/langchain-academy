from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_xai import ChatXAI
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages
import random

# 1. Initialize the free-tier Gemini model
# os.environ["GOOGLE_API_KEY"] = "your-gemini-api-key"
# Using gemini-2.5-flash for maximum free-tier quota limits
google_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
grok_llm = ChatXAI(model="grok-4")

# 2. Define your Graph State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Define the LLM Node
def chatbot_node(state: State):
    llm = google_llm if "Google" in state["messages"][-1].content else grok_llm
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 4. Build the Graph Workflow
workflow = StateGraph(State)
workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

# Compile into an executable app
app = workflow.compile()


# 5. Run the Graph
if __name__ == "__main__":
    # Example input
    llm_to_use = "Google" if random.random() < 0.5 else "Grok"  # Randomly choose LLM for demo purposes

    user_message = "Hi " + llm_to_use + " how is the weather today?"
    print(user_message)
    response = app.invoke({"messages": [{"role": "user", "content": user_message}]})
    print(response["messages"][-1].content)  # Print final AI response
