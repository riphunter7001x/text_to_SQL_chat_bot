import streamlit as st
from src.workflow import app
import traceback
from datetime import datetime
import time

def get_response(user_input, chat_history):
    """
    Invoke the AI assistant with conversation context.
    """
    try:
        messages = [("system", "You are a helpful AI assistant for analyzing banking transaction data.")]
        for msg in chat_history:
            messages.append(("user", msg[0]))
            messages.append(("assistant", msg[1]))
        
        messages.append(("user", user_input))
        ai_response = app.invoke({"question": user_input})
        time.sleep(3)
        return {
            "answer": ai_response["answer"],
            "query": ai_response.get("query", "No query generated"),
            "result": ai_response.get("result", "No results available")
        }
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error(traceback.format_exc())
        return {
            "answer": "Sorry, I encountered an error processing your request. Please try again.",
            "query": "",
            "result": ""
        }

def main():
    """
    Main Streamlit chatbot application
    """
    st.set_page_config(page_title="Banking SQL Chatbot", layout="wide")
    
    # Sidebar with dataset information
    st.sidebar.title("\U0001F3E6 Dataset Overview")
    st.sidebar.markdown("""
    ### Banking Transaction Dataset
    
    This dataset contains transactions of 100 Indian customers across two tables:
    - **customers.csv**: Stores account holder details like name, account number, and balance.
    - **transactions.csv**: Records deposits and withdrawals with date and amount.
    
    It helps analyze spending habits, account balances, and transaction trends.
    
    #### What I Can Help You With
    - Analyze transaction patterns
    - Explore customer spending habits
    - Provide insights on account activities
    
    **Tip:** Ask specific questions about banking data!
    
    #### Example Questions
    - Which customers have withdrawn more than 10,000 along with the date?
    - Who has the highest account balance along with their last deposit date?
    - Who are the top 5 customers who have deposited the most money?
    - Who was the last person to make a withdrawal along with the withdrawal amount?
    """)
    
    # Main chat interface
    st.title("\U0001F4AC Banking Transaction Chatbot")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append((
            "assistant", 
            "Hello! I'm your Banking Data Assistant. I can help you analyze customer transactions, account balances, and more. What would you like to know?"
        ))
    
    for msg in st.session_state.messages:
        with st.chat_message("assistant" if msg[0] == "assistant" else "user"):
            if isinstance(msg[1], dict):
                st.markdown(msg[1]["answer"])
            else:
                st.markdown(msg[1])
    
    if prompt := st.chat_input("Ask a question about banking data"):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_response(prompt, st.session_state.messages[:-1])
                st.markdown(response["answer"])
                with st.expander("🔍 View Query and Results"):
                    st.subheader("Generated SQL Query")
                    st.code(response["query"], language="sql")
                    st.subheader("Query Results")
                    st.code(response["result"], language="sql")
        
        st.session_state.messages.append(("user", prompt))
        st.session_state.messages.append(("assistant", response))
    
    if st.sidebar.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()
