import os
import chromadb
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI

# Initialize embeddings
embeddings = OpenAIEmbeddings()


OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
CHROMA_PATH = os.environ['CHROMA_PATH']
MAX_BATCH_SIZE = int(os.environ['MAX_BATCH_SIZE'])

# Initialize the LLM
model_id=os.environ['MODEL_ID']
local_llm = ChatOpenAI(model_name=model_id)


def get_qa_chain():
    vector_store = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    # Set up the QA chain
    qa = RetrievalQA.from_chain_type(
        llm=local_llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        return_source_documents=True,
    )
    return qa