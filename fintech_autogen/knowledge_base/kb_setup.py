"""
Knowledge Base setup module
Handles creation and population of ChromaDB vector database
"""

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import os
from pathlib import Path
import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader

# Define knowledge base directory path
KB_DIR = Path(__file__).parent / "chroma_db"
KB_TEXTS_DIR = Path(__file__).parent / "kb_texts"

def initialize_knowledge_base():
    """Initialize ChromaDB knowledge base with initial data using LangChain document loaders"""
    print(f"Setting up ChromaDB knowledge base at {KB_DIR}...")
    os.makedirs(KB_DIR, exist_ok=True)
    os.makedirs(KB_TEXTS_DIR, exist_ok=True)
 
    docs = []
    for txt_file in KB_TEXTS_DIR.glob("*.txt"):
        domain = txt_file.stem  # e.g., 'tech_sector' from 'tech_sector.txt'
        loader = TextLoader(str(txt_file))
        loaded_docs = loader.load()
        # Add domain metadata to each document
        for doc in loaded_docs:
            if not hasattr(doc, 'metadata') or doc.metadata is None:
                doc.metadata = {}
            doc.metadata['domain'] = domain
        docs.extend(loaded_docs)
    # Create vectorstore using LangChain Chroma
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        docs,
        embedding=embeddings,
        persist_directory=str(KB_DIR),
        collection_name="fintech_knowledge"
    )
    #vectorstore.persist()
    print("Knowledge base setup complete!")


# For testing
if __name__ == "__main__":
    initialize_knowledge_base()