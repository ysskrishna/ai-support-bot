import math
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_docs(documents,chunk_size=1000,chunk_overlap=20):
    """Splits documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)
    return docs


def batchify(docs, batch_size):
    """Splits documents into batches."""
    for i in range(0, len(docs), batch_size):
        yield docs[i:i + batch_size]


def preprocess_documents(csv_file_path, chroma_client, collection_name, embeddings):
    """Preprocess documents and store embeddings in Chroma collection."""
    loader = CSVLoader(file_path=csv_file_path, encoding="utf-8")
    documents = loader.load()

    collection = chroma_client.get_or_create_collection(name=collection_name)
    docs = split_docs(documents)
    print(f"# of docs : {len(docs)}")

    # Check if the collection is empty before adding documents
    if collection.count() == 0:
        print("Processing started.")
        # Process documents in batches
        batch_size = 100  # Define your batch size
        batch_counter = 0
        total_batches = math.ceil(len(docs) / batch_size)
        for batch in batchify(docs, batch_size):
            Chroma.from_documents(batch, embeddings, client=chroma_client, collection_name=collection_name)

            batch_counter += 1
            print(f"Processed batch {batch_counter}/{total_batches} of size: {len(batch)}")

        print("All documents processed.")
    else:
        print("Documents already present, so preprocessing step skipped")