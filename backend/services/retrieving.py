from langchain_community.vectorstores import Chroma
from services.chunking_and_loading import chunking_docs
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.runnables import RunnableParallel , RunnableLambda
from langchain_community.retrievers import BM25Retriever
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

PERSIST_DIR=str(BASE_DIR/"chroma_db")
ASSSETS_DIR=BASE_DIR/"assets"

def retrieving():
    embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store=Chroma(persist_directory=PERSIST_DIR,
                        embedding_function=embeddings)

    all_chunks=chunking_docs(ASSSETS_DIR)
    if not all_chunks:
        raise ValueError(f"Please check your Dir{ASSSETS_DIR} if it has files")

    existing_docs=vector_store.get()
    indexed_sources=set()
    if existing_docs and "metadatas" in existing_docs and existing_docs["metadatas"]:
        for meta in existing_docs["metadatas"]:
            indexed_sources.add(os.path.normpath(meta["source"]))
    new_chunks=[]
    for chunk in all_chunks:
        source=chunk.metadata.get("source")
        if source not in indexed_sources:
            new_chunks.append(chunk)
    if new_chunks:
        print(f"Embedding {len(new_chunks)} new chunks into the DB...")
        vector_store.add_documents(new_chunks)
    else:
        print("The ChromaDB is up to date!")

    dense_retriever=vector_store.as_retriever(search_kwargs={"k":2})
    bm25_retriever=BM25Retriever.from_documents(all_chunks)
    bm25_retriever.k=3
    parallel_retriever=RunnableParallel(dense=dense_retriever,bm25=bm25_retriever)

    def merge_and_duplicate(retrieved_docs):
        all_docs=retrieved_docs["dense"]+retrieved_docs["bm25"]
        unique_docs={doc.page_content: doc for doc in all_docs}
        return list(unique_docs.values())

    return parallel_retriever | RunnableLambda(merge_and_duplicate)                    


    
if __name__ == "__main__":
    query = "Enterprise Escalations"
    print(f"Testing retrieval for query: '{query}'\n")
    
    hybrid_retriever = retrieving()
    
    results = hybrid_retriever.invoke(query)
    
    print(f"\nFound {len(results)} relevant document(s):\n" + "-"*40)
    for i, doc in enumerate(results, start=1):
        source = doc.metadata.get("source", "Unknown")
        print(f"[{i}] Source: {source}")
        print(f"Content: {doc.page_content.strip()}")
        print("-" * 40)