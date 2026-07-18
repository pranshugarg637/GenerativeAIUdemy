# from typing_extensions import TypedDict
# from typing import Annotated
# from langgraph.graph.message import add_messages
# from langgraph.graph import StateGraph , START, END

# class State(TypedDict):
#     messages : Annotated[list, add_messages]  #whatever langgraph adds will keep adding in this message list

# def chatbot(state : State):
#     print(f" \n\n\n\n\nInside chatbot node ",state)
#     return {"messages": ["Hi, This is a message from chatbot"]}

# def samplenode(state: State):
#     print(f" \n\n\n\n\n\nInside SampleNode node ",state)
#     return {"messages": ["Sample message appended"]}

# graph_builder = StateGraph(State)
# graph_builder.add_node("xyz",chatbot) #xyz is name of the node
# graph_builder.add_node("xy",samplenode)
# graph_builder.add_edge(START,"xyz") # START -> xyz
# graph_builder.add_edge("xyz","xy") # xyz -> xy
# graph_builder.add_edge("xy",END) # xy -> END

# graph = graph_builder.compile()
# updated_state = graph.invoke(State({"messages" : ["Hi , My name is Pranshu Garg"]}))
# print("\n\n\n\n\nupdated state : ",updated_state)






from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph , START, END
from langchain.chat_models import init_chat_model
#load dotenv file after adding openai api key

llm=init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai"
)

class State(TypedDict):
    messages : Annotated[list, add_messages]  #whatever langgraph adds will keep adding in this message list

def chatbot(state : State): 
    print(f" \n\n\n\n\nInside chatbot node ",state)
    response= llm.invoke(state.get("messages"))
    return {"messages": [response]}

def samplenode(state: State):
    print(f" \n\n\n\n\n\nInside SampleNode node ",state)
    return {"messages": ["Sample message appended"]}

graph_builder = StateGraph(State)
graph_builder.add_node("xyz",chatbot) #xyz is name of the node
graph_builder.add_node("xy",samplenode)
graph_builder.add_edge(START,"xyz") # START -> xyz
graph_builder.add_edge("xyz","xy") # xyz -> xy
graph_builder.add_edge("xy",END) # xy -> END

graph = graph_builder.compile()
updated_state = graph.invoke(State({"messages" : ["Hi , My name is Pranshu Garg"]}))
print("\n\n\n\n\nupdated state : ",updated_state)