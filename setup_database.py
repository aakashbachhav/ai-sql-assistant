from langchain_commmunnit.utilities import SQLDatabase
from langchain_ollama import OllamaLLM
from langchain_experimental.sql import SQLDatabaseChain

#Connect SQLite database
db = SQLDatabase.from_uri("sqlite:///sales.db")

#Loading the Ollama LLM
# We use the temperature = 0 as we want deterministic, precise sql, not creative writing
llm - OllamaLLM(
    model = "codellama",
    temperature = 0
)

#Create the SQLDatabaseChain
db_chain = SQLDatabaseChain.from_llm(
    llm=llm,
    db=db,
    verbose=True,
    return_direct=True
)

#User query
question = "Which product generated the highest revenue?"

# Generate and execute the SQL query
response = db_chain.invoke({
    "query": question
})

#Print final response
print("\nFinal Response:")
print(response)