# SQL Mind — AI SQL Assistant

SQL Mind is an AI-powered SQL Assistant that allows users to query a database using plain English.

Built with:

* Streamlit
* LangChain
* Ollama
* SQLite
* Docker

The application converts natural language questions into SQL queries using a local Large Language Model (LLM) and returns readable database results through an interactive UI.

---

## Features

* Natural Language → SQL conversion
* Local LLM inference using Ollama
* Interactive Streamlit interface
* SQLite database integration
* Dockerized deployment
* Privacy-focused (no external API calls)
* Clean futuristic UI
* Automatic SQL query execution

---

## Tech Stack

| Technology | Purpose              |
| ---------- | -------------------- |
| Python     | Core backend         |
| Streamlit  | Frontend UI          |
| LangChain  | LLM orchestration    |
| Ollama     | Local LLM runtime    |
| CodeLlama  | SQL generation model |
| SQLite     | Database             |
| Docker     | Containerization     |

---

## Project Structure

```bash
AI-SQL-Assistant/
│
├── app.py
├── sql_assistant.py
├── setup_database.py
├── sales.db
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

---

## How It Works

1. User enters a question in plain English
2. LangChain reads database schema
3. Ollama generates SQL query
4. Query executes on SQLite database
5. Results are displayed in the UI

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/aakashbachhav/ai-sql-assistant.git

cd ai-sql-assistant
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

#### macOS / Linux

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install Ollama

Download and install Ollama:

https://ollama.com

Pull the model:

```bash
ollama pull codellama
```

Verify:

```bash
ollama list
```

---

## Run Application Locally

Start Ollama:

```bash
ollama serve
```

Run Streamlit app:

```bash
streamlit run app.py
```

Open browser:

```bash
http://localhost:8501
```

---

## Docker Setup

### Build Docker Image

```bash
docker build -t ai-sql-assistant .
```

### Run Docker Container

```bash
docker run \
-p 8501:8501 \
--add-host=host.docker.internal:host-gateway \
ai-sql-assistant
```

---

## Example Questions

* Which product generated the highest revenue?
* Show total sales by region
* Which customer placed the most orders?
* What are the monthly sales trends?
* Show top-selling products

---

## Security Note

This project is intended for development and educational purposes.

For production:

* Use read-only database permissions
* Validate generated SQL queries
* Add authentication
* Limit dangerous SQL operations

---

## Future Improvements

* CSV upload support
* PostgreSQL/MySQL support
* Query history
* Authentication
* SQL query visualization
* Chat-based interface
* Multi-database support

---

## Screenshots

*Add screenshots here*

---

## Author

Aakash Bachhav

GitHub:
https://github.com/aakashbachhav

---

## License

This project is open-source and available under the MIT License.
