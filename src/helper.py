import fitz
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from apify_client import ApifyClient

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")


def extract_text(pdf_path):

    doc = fitz.open(stream=pdf_path.read(), filetype="pdf")
    text=""
    for page in doc:
        text += str(page.get_text())
    return text

def ask_qroq(prompt,max_tokens=500):

    reponse = llm.invoke(prompt, max_tokens=max_tokens,temperature=0.5)
    return reponse.content

