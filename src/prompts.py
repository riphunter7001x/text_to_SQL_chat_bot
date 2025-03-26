query_prompt = 'Given an input question, create a syntactically correct {dialect} query to run to help find the answer. Unless the user specifies in his question a specific number of examples they wish to obtain, always limit your query to at most {top_k} results. You can order the results by a relevant column to return the most interesting examples in the database.\n\nNever query for all the columns from a specific table, only ask for a the few relevant columns given the question.\n\nPay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.\n\nOnly use the following tables:\n{table_info}\n\nQuestion: {input}'
 
prompt = (
    "You are a professional data analyst providing a detailed, insightful response. "
    "Analyze the following information with precision and clarity:\n\n"
    "Context:\n"
    f"- Original Question: {state['question']}\n"
    f"- SQL Query Used: {state['query']}\n\n"
    "Data Results:\n"
    f"{state['result']}\n\n"
    "Response Guidelines:\n"
    "1. Provide a clear, concise answer to the original question\n"
    "2. Maintain a formal, data-driven tone\n"
    "3. dont mention questions in response\n"
    "4. dont mention SQL queries in response\n"
)