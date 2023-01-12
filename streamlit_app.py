import openai
import streamlit as st
import re
import os

# Clase para representar una referencia
class Reference:
    def __init__(self, type, authors, year, title, source):
        self.type = type
        self.authors = authors
        self.year = year
        self.title = title
        self.source = source

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
            if line.startswith("TY"):
                match = re.search(r"TY\s+(.*)\n", reference)
                reference_type = match.group(1) if match else ""
            elif line.startswith("AU"):
                match = re.search(r"AU\s+(.*)\n", reference)
                authors = match.group(1) if match else ""
            elif line.startswith("PY"):
                match = re.search(r"PY\s+(\d{4})\n", reference)
                year = match.group(1) if match else ""
            elif line.startswith("TI"):
                match = re.search(r"TI\s+(.*)\n", reference)
                title = match.group(1) if match else ""
            elif line.startswith("T2"):
                match = re.search(r"T2\s+(.*)\n", reference)
                source = match.group(1) if match else ""
            elif line.startswith("ER"):
                # Parse reference
                references.append(Reference(type=reference_type, authors=authors, year=year, title=title, source=source))
                reference = ""
            else:
                reference += line
    return references

def format_reference(reference):
    """Use GPT-3 to format a reference in APA style.

    Parameters:
        reference (Reference): A named tuple representing a reference.

    Returns:
        str: The reference in APA style.
    """
    openai_prompt = (f"Format the following reference in APA style: "
                     f"{reference.authors} ({reference.year}). {reference.title}. {reference.source}")
    completions = openai.Completion.create(engine="text-davinci-002", prompt=openai_prompt, max_tokens=1024, n=1,stop=None,temperature=0.5)
    message = completions.choices[ 
    return completions.choices[0].text

def run_app():
    """Run the Streamlit app.
    """
    st.set_page_config(page_title="Reference Formatter", page_icon=":guardsman:", layout="wide")
    st.title("Reference Formatter using GPT-3")
    st.subheader("Upload your RIS file")
    file = st.file_uploader("", type=["ris"])
    if file:
        references = read_ris_file(file)
        for reference in references:
            st.subheader(reference.authors)
            st.write(format_reference(reference))

if __name__ == "__main__":
    run_app()

