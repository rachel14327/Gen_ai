import os
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "langchain"


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that answers questions."),
    ("user", "Question: {question}")
])


st.title("LangChain + Groq Demo")

input_text = st.text_input("Enter your question")
submit = st.button("Submit")


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

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