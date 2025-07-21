from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

def read_resume(resume):
        loader = PyPDFLoader(resume)
        docs = loader.load()
        resume_text = "\n".join([doc.page_content for doc in docs])
        return resume_text

def get_resume_data(resume):
    resume_text = read_resume(resume)

    system_prompt = """"
                "You are an expert resume parser that extracts key fields from resume text and formats them into valid JSON."
    """

    human_prompt = """
        Here is the text of a resume:

    {resume_text}

    Please extract the following fields and return them in valid JSON:
    - name
    - email
    - contact_number
    - location
    - skills (as a list of strings)

    Only output valid JSON. Do not include any explanations or markdown.
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", human_prompt)
        ]
    )

    llm = ChatGroq(model="llama3-8b-8192")
    parser = JsonOutputParser()

    chain = prompt | llm | parser

    response = chain.invoke({"resume_text": resume_text})
    return response

