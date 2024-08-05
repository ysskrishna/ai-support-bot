
import os

import chromadb
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import SentenceTransformerEmbeddings
from src.utils.chat import preprocess_documents

# Initialize embeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize the LLM
model_id="gpt-3.5-turbo"
local_llm = ChatOpenAI(model_name=model_id)


# Initialize Chroma client
chroma_client = chromadb.HttpClient(host="localhost", port=8000)
collection_name = "knowledgebase_collection"

# Initialize the vector store
vector_store = Chroma(client=chroma_client, collection_name=collection_name, embedding_function=embeddings)

# Preprocess the knowlegebase documents
csv_file_path = os.path.abspath(os.path.join("dataset_knowledgebase.csv"))
preprocess_documents(
    csv_file_path=csv_file_path, 
    chroma_client=chroma_client, 
    collection_name=collection_name, 
    embeddings=embeddings
)


# Set up the QA chain
qa = RetrievalQA.from_chain_type(
    llm=local_llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(),
    return_source_documents=True,
)