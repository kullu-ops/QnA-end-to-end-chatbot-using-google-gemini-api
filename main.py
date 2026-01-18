import os
import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")  

if not LANGCHAIN_API_KEY:
    raise ValueError("LANGCHAIN_API_KEY is missing! Set it in .env or environment variables")

os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "chatbot"

##chatpromt template
prompt=ChatPromptTemplate.from_messages([
    ("system","you are a brilliant agent very helpful in answering the querires"),
    ("user","question:{question}")
    
])


def generate_res(question, api_key, llm, temperature, max_tokens):
    model = ChatGoogleGenerativeAI(
        model=llm,
        google_api_key=api_key,
        temperature=temperature,
        max_output_tokens=max_tokens,
    )

    output_parser = StrOutputParser()
    chain = prompt | model | output_parser

    answer = chain.invoke({"question": question})
    return answer
##creating streamlit app
st.title("chatbot using Google Gemini")

st.sidebar.title("settings")
api_key = st.sidebar.text_input("enter your google api key",type="password")



llm = st.sidebar.selectbox(
    "Select the model",
    ["gemini-3-flash-preview", "gemini-1.5-turbo", "gemini-2", "gemini-2-100b"]
)

temperture=st.sidebar.slider("select the temp",min_value=0.0,max_value=1.0,value=0.7)
token = st.sidebar.slider("select the number of tokens", min_value=256, max_value=4096, value=1024, step=256)



st.write("ask any question")
user_input=st.text_input("enter your question here")

if user_input:
    response=generate_res(user_input,api_key,llm,temperture,token)
    st.write(response)
else:
    st.write("please enter a question ")