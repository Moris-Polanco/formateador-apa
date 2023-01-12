import openai
import streamlit as st
import re
import os
import io

# Autenticación de OpenAI (oculta la clave en una variable de entorno)
openai.api_key = os.environ.get("OPENAI_API_KEY")

import streamlit as st
import openai
import re
from collections import namedtuple
from typing import List

openai.api_key = "YOUR_API_KEY"

Reference = namedtuple("Reference", ["type", "authors", "year", "title", "source"])

def format_reference(reference):
    """Use GPT-3 to format a reference in APA style.

    Parameters:
        reference (Reference): A named tuple representing a reference.

    Returns:
        str: The formatted reference in APA style.
    """
    prompt = f"Format the following reference in APA style: {reference.authors}.({reference.year}).{reference.title}.{reference.source}."
    formatted_reference = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5
    ).choices[0].text
    return formatted_reference

def format_references(references: List[Reference]):
    """Use GPT-3 to format a list of references in APA style.

    Parameters:
        references (List[Reference]): A list of named tuples representing references.

    Returns:
        str: The formatted references in APA style, joined by new lines.
    """
    formatted_references = []
    for reference in references:
        formatted_references.append(format_reference(reference))
    return "\n".join(formatted_references)

import io

def read_ris_file(file):
    """Read a RIS file and return a list of references.

    Parameters:
        file (UploadedFile): The UploadedFile object returned by st.file_uploader.

    Returns:
        List[Reference]: A list of named tuples representing references.
    """
    references = []
    file_data = io.StringIO(file.getvalue().decode("utf-8"))
    with file_data as f:
        lines = f.readlines()
        reference = ""
        for line in lines:
            if line.startswith("ER"):
                # Parse reference
                match = re.search(r"AU\s+(.*)\n", reference)
                authors = match.group(1) if match else ""
                match = re.search(r"PY\s+(\d{4})\n", reference)
                year = match.group(1) if match else ""
                match = re.search(r"TI\s+(.*)\n", reference)
                title = match.group(1) if match else ""
                match = re.search(r"JO\s+(.*)\n", reference)
                source = match.group(1) if match else ""
                references.append(Reference(type=reference_type, authors=authors, year=year, title=title, source=source))

def run_app():
    st.set_page_config(page_title="APA Reference Formatter", page_icon=":guardsman:", layout="wide")
    st.title("APA Reference Formatter")
    st.markdown("This app formats references in APA style.")
    file = st.file_uploader("Upload a RIS file", type=["ris"])
    if file is not None:
        references = read_ris_file(file)
        if not references:
            st.error("Invalid or empty RIS file. Please upload a valid RIS file.")
        else:
            formatted_references = format_references(references)
            st.text(formatted_references, formatting=False)
            st.success("References formatted in APA style!")
            # Add option to save the formatted references to a file
            if st.button("Save formatted references"):
                with open("formatted_references.txt", "w") as f:
                    f.write(formatted_references)
                st.success("References saved to 'formatted_references.txt'.")
    else:
        st.warning("Please upload a RIS file.")

if __name__ == "__main__":
    run_app()
