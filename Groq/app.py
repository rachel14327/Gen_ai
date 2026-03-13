import streamlit as st
import os
import time
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader, ConfluenceLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if "vector" not in st.session_state:
    st.session_state.embeddings = OllamaEmbeddings(model="nomic-embed-text")
    confluence_user = os.getenv("CONFLUENCE_USERNAME")
    confluence_token = os.getenv("CONFLUENCE_API_KEY")
    if confluence_user and confluence_token:
        loader = ConfluenceLoader(
            url="https://mafretail.atlassian.net/wiki",
            username=confluence_user,
            api_key=confluence_token,
            space_key="ECOF",
            limit=50,
        )
        st.session_state.docs = loader.load()
    else:
        st.session_state.docs = WebBaseLoader(web_paths=["https://mafretail.atlassian.net/wiki/spaces/ECOF/overview?homepageId=1632698802"]).load()
    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
    st.session_state.vectorstore = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

st.title("ChatGroq Demo")
if not (os.getenv("CONFLUENCE_USERNAME") and os.getenv("CONFLUENCE_API_KEY")):
    st.sidebar.info("Add CONFLUENCE_USERNAME and CONFLUENCE_API_KEY to .env to load real Confluence wiki content.")
llm = ChatGroq(groq_api_key=groq_api_key,
               model="llama-3.1-8b-instant",
               temperature=0) ## temperature is the randomness of the model

prompt = ChatPromptTemplate.from_template(
    "Answer the question based on the context provided.\n"
    "Think step by step before providing the detailed answer.\n"
    "I will tip you 100$ if you answer correctly.\n\n"
    "<context>\n{context}\n</context>\n\n"
    "Question: {input}"
)

chain = prompt | llm | StrOutputParser()
retriever = st.session_state.vectorstore.as_retriever()
retriever_chain = create_retrieval_chain(retriever, chain)

prompt = st.text_input("Enter your question")

if prompt:
    start = time.process_time()
    response = retriever_chain.invoke({"input": prompt})
    print("Rsponse Time :", time.process_time() - start)
    st.write(response["answer"])

    # With streamlit expander
    with st.expander("Document similarity search"):
        # Skip chunks that are Atlassian login/JS placeholder (Confluence needs API auth for real content)
        junk_markers = ("Log in with Atlassian", "JavaScript is disabled", "enable JavaScript", "atl-paas.net")
        relevant = [doc for doc in response["context"] if not any(m in doc.page_content for m in junk_markers)]
        if not relevant:
            st.info("No useful chunks found. Confluence URLs need the Confluence API + credentials to load real content (see ConfluenceLoader in langchain_community).")
        for i, doc in enumerate(relevant):
            st.write(f"Relevant chunk {i+1}")
            st.write(doc.page_content)
            st.write("--------------------------------")