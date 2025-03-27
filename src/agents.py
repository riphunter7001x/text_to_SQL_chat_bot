from typing import TypedDict
from src.model import llm_model
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, PromptTemplate
from src.prompts import query_prompt
from typing_extensions import Annotated
from src.db_connection import db

class QueryOutput(TypedDict):
    """Defines the expected output structure for the generated SQL query."""
    query: Annotated[str, ..., "Syntactically valid SQL query."]

def write_query(state: dict):
    """
    Generates an SQL query to fetch relevant information from the database.
    
    Parameters:
        state (dict): The state dictionary containing the user's question.

    Returns:
        dict: A dictionary with the generated SQL query.
    """
    
    # Define a prompt template using ChatPromptTemplate to structure the LLM request
    query_prompt_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=['dialect', 'input', 'table_info', 'top_k'],
                template=query_prompt
            )
        )
    ])
    
    # Invoke the prompt template with relevant database and user information
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,  # Database dialect (e.g., PostgreSQL, MySQL)
            "top_k": 10,  # Limit the number of results
            "table_info": db.get_table_info(),  # Retrieve table schema information
            "input": state["question"],  # User's natural language query
        }
    )

    # Use the LLM model to generate a structured SQL query based on the provided input
    structured_llm = llm_model.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)

    return {"query": result["query"]}

from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool

def execute_query(state: dict):
    """
    Executes the generated SQL query on the connected database.

    Parameters:
        state (dict): The state dictionary containing the SQL query.

    Returns:
        dict: A dictionary with the query execution result.
    """
    
    # Initialize the SQL execution tool with the database connection
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    
    # Execute the SQL query and return the result
    return {"result": execute_query_tool.invoke(state["query"])}

def generate_answer(state: dict):
    """
    Uses the retrieved query results as context to generate an answer.

    Parameters:
        state (dict): The state dictionary containing the query results.

    Returns:
        dict: A dictionary containing the AI-generated answer.
    """
    
    prompt = (
        "You are a professional data analyst providing a detailed, insightful response. "
        "Analyze the following information with precision and clarity:\n\n"
        "Context:\n"
        f"- Original Question: {state['question']}\n"
        f"- SQL Query Used: {state['query']}\n\n"
        "Data Results:\n"
        f"{state['result']}\n\n"
        "Response Guidelines:\n"
        "1. If no relevant data is found in Data Results, clearly state: 'Information not found in our database.'\n"
        "2. Otherwise, provide a clear, concise answer based on the available data.\n"
        "3. Maintain a formal, data-driven tone.\n"
        "4. Do not mention questions in the response.\n"
        "5. Do not mention SQL queries in the response.\n"
    )
        
    # Invoke the LLM model to generate a response using the retrieved data
    response = llm_model.invoke(prompt)
    
    return {"answer": response.content}
