from typing_extensions import TypedDict
from langgraph.graph import START, StateGraph
from src.agents import write_query, execute_query, generate_answer

class State(TypedDict):
    """
    Represents the state of the process at different stages.

    Attributes:
        question (str): The user's natural language question.
        query (str): The generated SQL query.
        result (str): The result obtained from executing the query.
        answer (str): The final AI-generated response based on the query results.
    """
    question: str
    query: str
    result: str
    answer: str

# Initialize a StateGraph with the defined State structure
graph_builder = StateGraph(State).add_sequence(
    [write_query, execute_query, generate_answer]
)

# Define the starting point of the process, where it begins with writing the query
graph_builder.add_edge(START, "write_query")

# Compile the graph to create an executable application flow
app = graph_builder.compile()
