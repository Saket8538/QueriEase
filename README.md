# QueriEase 🤖

QueriEase is a powerful and interactive SQL query assistant powered by Google's Generative AI tools. It allows users to generate SQL queries from natural language, format SQL code, explain SQL queries, and visualize data insights. QueriEase is designed for both technical and non-technical users, making data analysis accessible and efficient.

---

## Features

1. **SQL Query Generator**: 
   - Generate SQL queries from natural language prompts.
   - Provides detailed explanations for complex queries.

2. **SQL Formatter**:
   - Beautify and format raw SQL code for better readability.

3. **Query Explainer**:
   - Break down SQL queries into simple, understandable components.

4. **Data Analysis & Visualization**:
   - Convert natural language questions into SQL queries.
   - Visualize data insights using interactive charts (e.g., bar charts, pie charts, line charts).

5. **AI Chatbot (Gemini4U)**:
   - Chat with an AI assistant for answering questions and generating responses.
   - Includes typing effects and an animated design for better user experience.

6. **Custom Animations**:
   - Smooth transitions, hover effects, and fade-in animations for a dynamic UI experience.

---

## Demo

![QueriEase Screenshot](https://via.placeholder.com/800x400.png?text=QueriEase+Screenshot+Demo)

---

## Installation and Local Setup

Follow these steps to set up the project on your local machine:

### 1. **Clone the Repository**
   ```bash
   git clone https://github.com/Saket8538/QueriEase.git
   cd QueriEase
   ```

### 2. **Set Up a Python Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

### 3. **Install Dependencies**
   Install all required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

### 4. **Configure Environment Variables**
   Create a `.env` file in the project root and add your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key
   ```

### 5. **Set Up the Database**
   Ensure the SQLite database file (`Music.db`) is placed in the project root directory. You can download the database [here](https://storage.googleapis.com/tidb_hack/Music.sql).

### 6. **Run the Application**
   Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

   The application will be accessible at `http://localhost:8501`.

---

## Project Structure

```
c:\Projects\QueriEase
├── app.py               # Main application file
├── requirements.txt     # Python dependencies
├── Music.db             # SQLite database
├── README.md            # Project documentation
├── .env                 # Environment variables
└── ...
```

---

## Usage

### **SQL Query Generator**
1. Navigate to the "SQL Query Generator" page.
2. Enter your query in plain English (e.g., "Show the top 5 artists with the most albums").
3. Click "Generate SQL Query" to see the SQL code, expected output, and explanation.

### **SQL Formatter**
1. Go to the "SQL Formatter" page.
2. Paste your SQL query in the text area.
3. Click "Format SQL" to beautify the code.

### **Query Explainer**
1. Open the "Query Explainer" page.
2. Paste your SQL query in the text area.
3. Click "Explain Query" to get a detailed breakdown of the query.

### **Data Analysis & Visualization**
1. Navigate to the "Data Analysis & Visualization" page.
2. Enter a natural language question (e.g., "Which genres have the most tracks?").
3. Click "Retrieve & Visualize Data" to see the query, results, and an interactive chart.

### **AI Chatbot (Gemini4U)**
1. Click the "💬 Gemini4U" button in the sidebar to open the chatbot.
2. Ask questions or interact with the AI assistant.
3. Enjoy typing effects and fade-in animations for responses.

---

## Technologies Used

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: Python, SQLite
- **Visualization**: Plotly
- **AI**: Google's Generative AI (Gemini)

---

## Contributing

We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Open a pull request.

---

## License

This project is licensed under the Apache License, Version 2.0. You may obtain a copy of the License at:

```
http://www.apache.org/licenses/LICENSE-2.0
```

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

---

## Contact

For any inquiries or support, please reach out to:
- **Email**: support@queriease.com
- **GitHub**: [GitHub Repository](https://github.com/Saket8538/QueriEase)