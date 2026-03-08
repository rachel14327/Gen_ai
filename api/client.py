import requests
import streamlit as st

def get_groq_response(input_text):
    url = "http://localhost:8001/essay/invoke"
    response = requests.post(url, json={'input' : {'topic': input_text}})
    return response.json()['output']['content']

def get_ollama_response(input_text):
    url = "http://localhost:8001/poem/invoke"
    response = requests.post(url, json={'input' : {'topic': input_text}})
    return response.json()["response"]

st.title("LangChain API Client")

##Streamlit UI

st.title("Langchain demo")
input_text = st.text_input("Write an essay on")
input_text1 = st.text_input("Write a poem on")

if input_text:
    st.write(get_groq_response(input_text))
if input_text1: 
    st.write(get_ollama_response(input_text1))


            