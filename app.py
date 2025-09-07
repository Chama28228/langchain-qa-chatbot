# Q&A Chat bot
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

## Function to load Groq model and get responses
def get_llm():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        st.error("GROQ_API_KEY not found. Please set it in the Hugging Face Space secrets.")
        st.stop()
    
    return ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.1-8b-instant",
        temperature=0.5,
        max_retries=5
    )

# Prompt + Chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise, factual assistant. If a country has multiple capitals, label them."),
    ("human", "{question}")
])

# UI/ Frontend
st.set_page_config(page_title="Q&A Demo")
st.header("My First Langchain Application")

# Initialize LLM
try:
    llm = get_llm()
    chain = prompt | llm | StrOutputParser()
except Exception as e:
    st.error(f"Error initializing the model: {e}")
    st.stop()

question = st.text_input("Ask a question:")
if st.button("Ask") and question.strip():
    with st.spinner("Thinking..."):
        try:
            answer = chain.invoke({"question": question})
            st.subheader("Answer")
            st.write(answer)
        except Exception as e:
            st.error(f"Error getting response: {e}")