from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langserve import add_routes
import uvicorn
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

app=FastAPI(
    title="LangChain API",
    version="0.1.0",
    description="API for LangChain",
)

model = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
add_routes(app, model, path="/groq")
llm = ChatOllama(model="llama3.1")

prompt1 = ChatPromptTemplate.from_template("Write me an essay about {topic} with {word_count} words")
prompt2 = ChatPromptTemplate.from_template("Write me a poem about {topic} with {word_count} words")

add_routes(
    app, 
    prompt1|model,
#This below api is for the essay prompt integrated with groq
    path="/essay" 
)

add_routes(
    app, 
    prompt2|llm,
#This below api is for the poem prompt integrated with ollama
    path="/poem" 
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port) 

