from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Chroma
from src.core.config import embeddings, CHROMA_PATH, MAX_BATCH_SIZE, OPENAI_API_KEY
import openai 
import os
import shutil


openai.api_key = OPENAI_API_KEY


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    csv_file_path = os.path.abspath(os.path.join("dataset_knowledgebase.csv"))
    loader = CSVLoader(file_path=csv_file_path, encoding="utf-8")
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    return chunks


def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    for i in range(0, len(chunks), MAX_BATCH_SIZE):
        batch = chunks[i:i + MAX_BATCH_SIZE]
        db = Chroma.from_documents(
            batch, embeddings, persist_directory=CHROMA_PATH
        )
        db.persist()
        print(f"Saved batch {i // MAX_BATCH_SIZE + 1} with {len(batch)} chunks to {CHROMA_PATH}.")

    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    generate_data_store()