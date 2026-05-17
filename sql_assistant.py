from langchain_community.utilities import SQLDatabase
from langchain_ollama import OllamaLLM
from langchain_experimental.sql import SQLDatabaseChain

db = SQLDatabase.from_uri("sqlite:///sales.db")

llm - OllamaLLM(
    model = "codellama",
    temperature = 0
)

db_chain = SQLDatabaseChain.from_llm(
    llm=llm,
    db=db,
    verbose=True,
    return_direct=True
)

question = "Which product generated the highest revenue?"

response = db_chain.invoke(question)
print(response)
