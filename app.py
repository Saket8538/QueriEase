import streamlit as st
import google.generativeai as genai
import sqlite3
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os
import time  # Import time for the typing effect

def configure():
    load_dotenv()
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Use the fastest model available
    model = genai.GenerativeModel("gemini-2.0-flash")  
    return model

# Database path (modify as needed)
database_path = 'Music.db'

# Prompt for Text-to-Chart AI
prompt = [
    """
    Imagine you're an SQL expert and data visualization advisor adept at translating English questions into precise SQL queries and recommending visualization types for a database named Chinook, which comprises several tables including Employees, Customers, Invoices, Invoice_Items, Artists, Albums, Media_Types, Genres, Tracks, Playlists, and Playlist_Track. Your expertise enables you to select the most appropriate chart type based on the expected query result set to effectively communicate the insights.

    Here are examples to guide your query generation and visualization recommendation:

    - Example Question 1: "How many unique artists are there?"
      SQL Query: SELECT COUNT(DISTINCT name) FROM Artists;
      Recommended Chart: None (The result is a single numeric value.)

    - Example Question 2: "What are the total number of albums by each artist?"
      SQL Query: SELECT Artists.name, COUNT(Albums.AlbumId) AS total_albums FROM Artists JOIN Albums ON Artists.ArtistId = Albums.ArtistId GROUP BY Artists.name;
      Recommended Chart: Bar chart (Artists on the X-axis and total albums on the Y-axis.)

    - Example Question 3: "List all employees who report to a specific manager."
      SQL Query: SELECT first_name, last_name FROM Employees WHERE ReportsTo = (SELECT EmployeeId FROM Employees WHERE first_name = 'Nancy' AND last_name = 'Edwards');
      Recommended Chart: None (The result is a list of employee names.)

    - Example Question 4: "What percentage of tracks belong to each genre?"
      SQL Query: SELECT Genres.Name, (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Tracks)) AS percentage FROM Tracks JOIN Genres ON Tracks.GenreId = Genres.GenreId GROUP BY Genres.Name;
      Recommended Chart: Pie chart (Show each genre's percentage of the total tracks.)

    - Example Question 5: "Which customers have the highest total invoice amounts?"
      SQL Query: SELECT Customers.FirstName, Customers.LastName, SUM(Invoices.Total) AS total_spent FROM Customers JOIN Invoices ON Customers.CustomerId = Invoices.CustomerId GROUP BY Customers.FirstName, Customers.LastName ORDER BY total_spent DESC LIMIT 10;
      Recommended Chart: Bar chart (Customer names on the X-axis and total invoice amounts on the Y-axis.)

    Your task is to craft the correct SQL query in response to the given English questions and suggest an appropriate chart type for visualizing the query results, if applicable. Please ensure that the SQL code generated does not include triple backticks (\`\`\`) at the beginning or end and avoids including the word "sql" within the output. Also, provide clear and concise chart recommendations when the query results lend themselves to visualization.
    """
]


def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([prompt[0], question])
    return response.text

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df


def get_sql_query_from_response(response):
    try:
        query_start = response.index('SELECT')
        query_end = response.index(';') + 1
        sql_query = response[query_start:query_end]
        return sql_query
    except ValueError:
        st.error("Could not extract SQL query from the response.")
        return None


def determine_chart_type(df):
    if len(df.columns) == 2:
        if df.dtypes[1] in ['int64', 'float64'] and len(df) > 1:
            return 'bar'
        elif df.dtypes[1] in ['int64', 'float64'] and len(df) <= 10:
            return 'pie'
    elif len(df.columns) >= 3 and df.dtypes[1] in ['int64', 'float64']:
        return 'line'
    return None


def generate_chart(df, chart_type):
    if chart_type == 'bar':
        fig = px.bar(df, x=df.columns[0], y=df.columns[1],
                     title=f"{df.columns[0]} vs. {df.columns[1]}",
                     template="plotly_white", color=df.columns[0])
    elif chart_type == 'pie':
        fig = px.pie(df, names=df.columns[0], values=df.columns[1],
                     title=f"Distribution of {df.columns[0]}",
                     template="plotly_white")
    elif chart_type == 'line':
        fig = px.line(df, x=df.columns[0], y=df.columns[1],
                     title=f"{df.columns[1]} Over {df.columns[0]}",
                     template="plotly_white", markers=True)
    else:
        st.write("No suitable chart type determined for this data.")
        return
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

def generate_sql_query(model, input_prompt):
    template = """
        Create a SQL query snippet using the below text:

        ```
        {text_input}
        ```  
        i just want a Sql query         
    """
    formatted_template = template.format(text_input=input_prompt)
    response = model.generate_content(formatted_template)
    sql_query = response.text.strip().lstrip("```sql").rstrip("```")
    return sql_query

def generate_expected_output(model, sql_query):
    expected_output = """
        What would be the expected response of this SQL query snippet:

        ```
        {sql_query}
        ```  
        Provide sample table response with no explanation        
    """
    expected_output_formatted = expected_output.format(sql_query=sql_query)
    response = model.generate_content(expected_output_formatted)
    return response.text

def generate_explanation(model, sql_query):
    explanation = """
        Explain this SQL query:

        ```
        {sql_query}
        ```  
        Please provide the simplest explanation:       
    """
    explanation_formatted = explanation.format(sql_query=sql_query)
    response = model.generate_content(explanation_formatted)
    return response.text

def sql_formatter(model, sql_code):
    template = """
        Format this SQL code block:

        ```
        {sql_code}
        ```  
        Format this SQL code        
    """
    formatted_template = template.format(sql_code=sql_code)
    response = model.generate_content(formatted_template)
    formatted_sql = response.text.strip().lstrip("```sql").rstrip("```")
    return formatted_sql

def query_explainer(model, sql_syntax):
    explanation = """
        Explain each part of this SQL query:

        ```
        {sql_syntax}
        ```  
        Please break down the query and explain each important concept or word:      
    """
    explanation_formatted = explanation.format(sql_syntax=sql_syntax)
    response = model.generate_content(explanation_formatted)
    return response.text

def add_custom_css():
    custom_css = """
    <style>
    /* Add smooth transitions for buttons and hover effects */
    button {
        transition: all 0.3s ease-in-out;
    }
    button:hover {
        transform: scale(1.1);
        background-color: #4CAF50 !important;
        color: white !important;
    }

    /* Add fade-in effect for chatbot responses */
    .fade-in {
        animation: fadeIn 1s ease-in-out;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    /* Style for chatbot response box */
    .response-box {
        background-color: #00FFFF;
        padding: 10px;
        border-radius: 5px;
        color: #333;
        margin-top: 10px;
        animation: fadeIn 1s ease-in-out;
    }

    /* Add hover effect for sidebar navigation */
    .css-1v3fvcr a {
        transition: all 1s ease-in-out;
    }
    .css-1v3fvcr a:hover {
        color: #4CAF50 !important;
        font-weight: bold !important;
    }

    /* Add smooth transitions for page content */
    .stApp {
        animation: slideIn 0.7s ease-in-out;
    }

    @keyframes slideIn {
        from {
            transform: translateY(20px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def gemini_chat_icon(model):
    with st.sidebar:
        if "show_chat" not in st.session_state:
            st.session_state.show_chat = False

        if st.button("💬 Gemini4U"):
            st.session_state.show_chat = not st.session_state.show_chat

    if st.session_state.show_chat:
        st.subheader("AI Chatbot 🤖")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []  # Initialize chat history

        with st.form(key='chat_form', clear_on_submit=True):
            user_input = st.text_area("Ask anything:", key="chat_input")
            submit_button = st.form_submit_button(label="Send")

        if submit_button and user_input:
            with st.spinner("Thinking..."):
                try:
                    # Generate AI response
                    response = model.generate_content(f"User: {user_input}\nAI:")
                    # Clear previous chat history and store only the latest question and response
                    st.session_state.chat_history = [{"user": user_input, "ai": response.text}]
                except Exception as e:
                    st.error(f"Error: {e}")

        # Display only the latest question and response
        if st.session_state.chat_history:
            latest_chat = st.session_state.chat_history[0]
            st.markdown(f"**You:** {latest_chat['user']}")
            
            # Typing effect for the AI response
            st.markdown("**Gemini4U:**")
            response_placeholder = st.empty()
            ai_response = latest_chat['ai']
            typed_response = ""
            for char in ai_response:
                typed_response += char
                response_placeholder.markdown(
                    f"<div class='response-box'>{typed_response}</div>",
                    unsafe_allow_html=True
                )
                time.sleep(0.02)  # Adjust typing speed here

def main():
    model = configure()
    st.set_page_config(page_title="QueriEase", page_icon="robot:")

    # Add custom CSS for animations and transitions
    add_custom_css()

    st.sidebar.title('Navigation')
    pages = st.sidebar.radio("Go to", ['About', 'SQL Query Generator', 'SQL Formatter', 'Query Explainer', 'Data Analysis & Visualization'])

    if pages == 'About':
        st.markdown(
            """
            <div style="text-align:center;">
                <h1>QueriEase 🤖</h1>
                <h3>Personal SQL Query Assistant</h3>
                <p> Welcome to QueriEase! Our project is your personal SQL query assistant powered by Google's Generative AI tools. 
                With QueriEase, you can effortlessly generate SQL queries and receive detailed explanations, and also format your for readability and consistency. Let's simplifying your data retrieval process!</p>           
            </div>
            """,
            unsafe_allow_html=True,
            
        )

        # New content added using Streamlit functions
        st.subheader("SQL Query Generator")
        st.write(
            """
            🔍 Quickly generate SQL queries by typing your data requests in simple language.
            🛠️ Simplifies the process of creating complex queries with ease.
            """
        )

        st.subheader("SQL Formatter")
        st.write(
            """
            ✨ Clean up and organize your SQL code for better readability and consistency.
            📜 Ensures your SQL queries are well-structured and easy to maintain.
            """
        )

        st.subheader("Query Explainer")
        st.write(
            """
            🧩 Break down SQL queries into understandable parts with detailed explanations.
            📖 Helps you grasp how each component of the query functions and why.
            """
        )

        st.subheader("Data Analysis & Visualization")
        st.write(
            """
            🔢 Convert natural language questions into SQL queries and visualize data with interactive charts.
            📊 Makes data analysis accessible and insightful without needing technical expertise.
            """
        )
        gemini_chat_icon(model)

    elif pages == 'SQL Query Generator':
        st.markdown(
            """
            <div style="text-align:center;">
            <h1>SQL Query Generator 📝</h1>
            <p>Use the SQL Query Generator to create SQL queries from natural language prompts.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        text_input = st.text_area("Type your desired query below to unlock the power of SQL Query Genie! 💬")
        submit = st.button("Generate SQL Query")

        if submit:
            with st.spinner("Generating SQL Query.."):
                sql_query = generate_sql_query(model, text_input)
                eoutput = generate_expected_output(model, sql_query)
                explanation = generate_explanation(model, sql_query)
                with st.container():
                    st.success("Your SQL query has been successfully generated. Feel free to copy and paste it into your database management system to retrieve the requested records.")
                    st.code(sql_query, language="sql")

                    st.markdown(
                        """
                        <div style="background-color: #d4edda; padding: 10px; border-radius: 5px;">
                            Expected output of this SQL Query.<br>
                            If the structure of the query isn't displayed, please click again on the 'Generate SQL Query' button.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(eoutput)

                    st.success("Explanation of SQL Query")
                    st.markdown(explanation)
        gemini_chat_icon(model)

    elif pages == 'SQL Formatter':
        st.markdown(
            """
            <div style="text-align:center;">
            <h1>SQL Formatter 📋</h1>
            <p>Use the SQL formatter to format your SQL queries for readability and consistency.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        sql_input = st.text_area("Paste your SQL code here:")
        format_button = st.button("Format SQL")

        if format_button:
            if sql_input:
                formatted_sql = sql_formatter(model, sql_input)
                st.code(formatted_sql, language='sql')
        gemini_chat_icon(model)

    elif pages == 'Query Explainer':
        st.markdown(
            """
            <div style="text-align:center;">
            <h1>Query Explainer 📢</h1>
            <p>Understand each part of your SQL query with explanations.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        sql_syntax = st.text_area("Paste your SQL syntax here:")
        explain_button = st.button("Explain Query")

        if explain_button:
            if sql_syntax:
                explanation = query_explainer(model, sql_syntax)
                st.markdown(explanation)
        gemini_chat_icon(model)

    elif pages == 'Data Analysis & Visualization':
        st.markdown(
            """
            <div style="text-align:center;">
                <h1>Data Analysis & Visualization 📊</h1>
                <p>Analyze your data and visualize insights effortlessly.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Add instructions with download link
        # st.header("Instructions")
        st.write("Download the database, [link](https://storage.googleapis.com/tidb_hack/Music.sql) or view ER-diagram, [link](https://storage.googleapis.com/tidb_hack/ER-diagram.jpg)")
        
        # Display sample questions
        st.write("Sample Questions,")
        st.write("""
        1. Which top 5 artists have the most albums?
        2. How many total artists are there in the database?
        3. Which genres have the most tracks? Show with a bar chart.
        """)
        
        question = st.text_area("Enter your data analysis question:")
        submit = st.button("Retrieve & Visualize Data")

        if submit and question:
            response = get_gemini_response(question, prompt)
            sql_query = get_sql_query_from_response(response)

            if sql_query:
                st.code(sql_query, language='sql')
                df = read_sql_query(sql_query, database_path)

                if not df.empty:
                    col_data, col_chart = st.columns(2)
                    with col_data:
                        st.subheader("Query Results:")
                        st.dataframe(df)
                    chart_type = determine_chart_type(df)

                    if chart_type:
                        with col_chart:
                            st.subheader("Visualization:")
                            generate_chart(df, chart_type)
                else:
                    st.write("No results found for the given query.")
            else:
                st.write("No valid SQL query could be extracted from the response.")
        gemini_chat_icon(model)

if __name__ == "__main__":
    main()