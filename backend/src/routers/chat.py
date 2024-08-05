
import os
import math
import asyncio
import chromadb
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain.chains import RetrievalQA
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from sse_starlette.sse import EventSourceResponse
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings

router = APIRouter()

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


def split_docs(documents,chunk_size=1000,chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs


# Function to split documents into batches
def batchify(docs, batch_size):
    for i in range(0, len(docs), batch_size):
        yield docs[i:i + batch_size]

# Load the tokenizer and model
model_id="gpt-3.5-turbo"
local_llm = ChatOpenAI(model_name=model_id)

# Load the CSV data
csv_file_path = os.path.abspath(os.path.join("dataset_knowledgebase.csv"))
loader = CSVLoader(file_path=csv_file_path, encoding="utf-8")
documents  = loader.load()


# Initialize Chroma client
chroma_client = chromadb.HttpClient(host="localhost", port=8000)
collection_name = "knowledgebase_collection"


def preprocess():
    # Create or retrieve an existing Chroma collection
    collection = chroma_client.get_or_create_collection(name=collection_name)
    docs = split_docs(documents)
    print(f"# of docs : {len(docs)}")

    # Check if the collection is empty before adding documents
    if collection.count() == 0:
        print("Processing started.")
        # Process documents in batches
        batch_size = 100  # Define your batch size
        batch_counter = 0
        total_batches = math.ceil(docs / batch_size)
        for batch in batchify(docs, batch_size):
            Chroma.from_documents(batch, embeddings, client=chroma_client, collection_name=collection_name)

            batch_counter += 1
            print(f"Processed batch {batch_counter}/{total_batches} of size: {len(batch)}")

        print("All documents processed.")
    else:
        print("Documents already present, so preprocessing step skipped")

preprocess()
vector_store = Chroma(client=chroma_client, collection_name=collection_name, embedding_function=embeddings)

# Set up the QA chain
qa = RetrievalQA.from_chain_type(
    llm=local_llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(),
    return_source_documents=True,
)

async def generate_response(query: str):
    try:
        result = qa({"query": query})
        # print(result)
        answer = result['result']
        for word in answer.split():
            yield f"data: {word}\n\n"
            await asyncio.sleep(0.1)
        yield "data: [END]\n\n"
    except Exception as e:
        print("exception", str(e))
        yield f"data: [ERROR] {str(e)}\n\n"

@router.get("/query")
async def ask_question(question: str):
    return StreamingResponse(generate_response(question), media_type='text/event-stream')