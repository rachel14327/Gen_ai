from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that answers questions."),
    ("user", "Question: {question}")
])


st.title("LangChain + Ollama")
input_text = st.text_input("Enter your question")
submit = st.button("Submit")

## Ollama – use a model you have (e.g. ollama pull llama3.1)
llm = ChatOllama(model="llama3.1")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if submit and input_text:
    with st.spinner("Thinking..."):
        try:
            answer = chain.invoke({"question": input_text})
            st.write(answer)
        except Exception as e:
            st.error(f"Error: {e}")

elif submit and not input_text:
    st.warning("Please enter a question.")