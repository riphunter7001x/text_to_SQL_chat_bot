# Banking Transaction Chatbot With SQL Agent

## Overview
This is a Streamlit-based chatbot application designed to analyze banking transactions using SQL queries. The chatbot helps users extract insights from banking transaction data, such as customer deposits, withdrawals, and balances.

## Features
- **Conversational AI**: Interact with the chatbot using natural language queries.
- **SQL Query Generation**: The AI converts user questions into SQL queries for data retrieval.
- **Transaction Insights**: Get details on customer deposits, withdrawals, and balances.
- **Example Queries**:
  - Which customers have withdrawn more than 10,000 along with the date?
  - Who has the highest account balance along with their last deposit date?
  - Who are the top 5 customers who have deposited the most money?
  - Who was the last person to make a withdrawal along with the withdrawal amount?

## Dataset
This chatbot uses a dataset of 100 Indian banking customers, consisting of two tables:
- **customers.csv**: Contains account holder details (name, account number, balance).
- **transactions.csv**: Stores deposit and withdrawal records (date, amount).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/riphunter7001x/text_to_SQL_chat_bot .git
   cd text_to_SQL_chat_bot 
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage
- Open the Streamlit app in your browser.
- Type a banking-related question in the chat interface.
- View the AI-generated SQL query and query results.
- Use the sidebar to clear the conversation history.