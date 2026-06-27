from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages

# 1. Initialize the free-tier Gemini model
# os.environ["GOOGLE_API_KEY"] = "your-gemini-api-key"
# Using gemini-2.5-flash for maximum free-tier quota limits
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# 2. Define your Graph State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Define the LLM Node
def chatbot_node(state: State):
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
    user_message = "It is a rainy day today."
    response = app.invoke({"messages": [{"role": "user", "content": user_message}]})
    print(response["messages"][-1].content)  # Print final AI response
