import openai
import streamlit as st
import re
import os

# Autenticación de OpenAI (oculta la clave en una variable de entorno)
openai.api_key = os.environ.get("OPENAI_API_KEY")

def format_reference(reference):
    formatted_reference = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Format the following reference in APA style: {reference}",
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5
    ).choices[0].text
    return formatted_reference

def format_references(references):
    formatted_references = []
    for reference in references:
        formatted_references.append(format_reference(reference))
    return "\n".join(formatted_references)

def read_ris_file(file):
    references = []
    with open(file, "r") as f:
        lines = f.readlines()
        reference = ""
        for line in lines:
            if line.startswith("ER"):
                references.append(reference.strip())
                reference = ""
            else:
                reference += line
    return references

def run_app():
    st.set_page_config(page_title="APA Reference Formatter", page_icon=":guardsman:", layout="wide")
    st.title("APA Reference Formatter")
    st.markdown("This app formats references in APA style.")
    file = st.file_uploader("Upload a RIS file", type=["ris"])
    if file is not None:
        references = read_ris_file(file)
        formatted_references = format_references(references)
        st.text(formatted_references, formatting=False)
        st.success("References formatted in APA style!")
    else:
        st.warning("Please upload a RIS file.")

if name == "main":
    run_app()
