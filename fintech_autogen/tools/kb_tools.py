"""
Knowledge Base retrieval tools

This module provides tools for retrieving information from the ChromaDB knowledge base
using LangChain's Chroma integration
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import logging

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Define knowledge base directory path
KB_DIR = Path(__file__).parent.parent / "knowledge_base" / "chroma_db"
COLLECTION_NAME = "fintech_knowledge"

def get_embedding_function():
    """Get the default embedding function for text embeddings using OpenAIEmbeddings from langchain_openai"""
    return OpenAIEmbeddings()

def get_vectorstore():
    logger = logging.getLogger("kb_tools")
    logger.info("Creating Chroma vectorstore for knowledge base retrieval.")
    """Get a Chroma vectorstore for the single collection"""
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embedding_function(),
        persist_directory=str(KB_DIR)
    )

def query_knowledge_base(
    query_text: str, 
    n_results: int = 3,
    metadata_filter: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    logger = logging.getLogger("kb_tools")
    logger.info(f"Querying knowledge base: '{query_text}' (n_results={n_results})")
    """
    Query the single collection in the knowledge base
    
    Args:
        query_text: Query text to search for
        n_results: Number of results to return
        metadata_filter: Optional filter for metadata fields
        
    Returns:
        List of dictionaries with the query results
    """
    try:
        vectorstore = get_vectorstore()
        search_kwargs = {"k": n_results}
        if metadata_filter:
            search_kwargs["filter"] = metadata_filter
        retriever = vectorstore.as_retriever(search_type="similarity", **search_kwargs)
        results = retriever.invoke(query_text)
        processed_results = []
        for doc in results:
            score = getattr(doc, "score", None)
            if score is None:
                score = doc.metadata.get("score", 0.0)
            result = {
                'document': doc.page_content,
                'id': doc.metadata.get('id', ''),
                'distance': score,
                'metadata': doc.metadata
            }
            processed_results.append(result)
        return processed_results
    except Exception as e:
        print(f"Error querying collection {COLLECTION_NAME}: {e}")
        return []

def get_financial_knowledge(tool_input: str, n_results: int = 3) -> str:
    """
    Retrieve general financial knowledge
    
    Args:
        tool_input: Query text to search for
        n_results: Number of results to return
        
    Returns:
        Formatted text with the query results
    """
    results = query_knowledge_base(tool_input, n_results, metadata_filter={"domain": "general_finance"})
    return format_results_as_text(results)

def get_sector_knowledge(tool_input: Dict[str, Any]) -> str:
    """
    Retrieve sector-specific knowledge
    
    Args:
        tool_input: Dictionary with query and sector
            query: Query text to search for
            sector: Specific sector to search in (tech, finance, healthcare)
            n_results: Number of results to return (optional)
        
    Returns:
        Formatted text with the query results
    """
    query = tool_input.get("query", "")
    sector = tool_input.get("sector", None)
    n_results = tool_input.get("n_results", 3)
    if sector:
        sector_map = {
            "tech": "tech_sector",
            "technology": "tech_sector",
            "finance": "finance_sector",
            "financial": "finance_sector",
            "healthcare": "healthcare_sector",
            "health": "healthcare_sector"
        }
        domain = sector_map.get(sector.lower(), None)
        if domain:
            results = query_knowledge_base(query, n_results, metadata_filter={"domain": domain})
            return format_results_as_text(results)
        else:
            return f"Unknown sector: {sector}"
    else:
        # Query all sector domains
        domains = ["tech_sector", "finance_sector", "healthcare_sector"]
        flat_results = []
        for domain in domains:
            collection_results = query_knowledge_base(query, n_results, metadata_filter={"domain": domain})
            for result in collection_results:
                result['collection'] = domain
                flat_results.append(result)
        if flat_results and flat_results[0].get('distance') is not None:
            flat_results.sort(key=lambda x: x.get('distance', float('inf')))
        return format_results_as_text(flat_results[:n_results])

def get_investment_strategies(tool_input: str) -> str:
    """
    Retrieve investment strategy knowledge
    
    Args:
        tool_input: Query text to search for
        
    Returns:
        Formatted text with the query results
    """
    results = query_knowledge_base(tool_input, n_results=3, metadata_filter={"domain": "investment_strategies"})
    return format_results_as_text(results)

def get_market_analysis_patterns(tool_input: str, n_results: int = 3) -> str:
    """
    Retrieve market analysis pattern knowledge
    
    Args:
        tool_input: Query text to search for
        n_results: Number of results to return
        
    Returns:
        Formatted text with the query results
    """
    results = query_knowledge_base(tool_input, n_results, metadata_filter={"domain": "market_analysis"})
    return format_results_as_text(results)

def get_risk_management_guidelines(tool_input: str) -> str:
    """
    Retrieve risk management guidelines
    
    Args:
        tool_input: Query text to search for
        
    Returns:
        Formatted text with the query results
    """
    results = query_knowledge_base(tool_input, n_results=3, metadata_filter={"domain": "risk_management"})
    return format_results_as_text(results)

def format_results_as_text(results: List[Dict[str, Any]]) -> str:
    """
    Format knowledge base results as readable text
    
    Args:
        results: List of result dictionaries
        
    Returns:
        Formatted text string
    """
    if not results:
        return "No relevant information found."
    
    formatted_text = ""
    
    for i, result in enumerate(results):
        formatted_text += f"{i+1}. {result['document']}\n\n"
    
    return formatted_text

# For testing
if __name__ == "__main__":
    # Test some of the functions
    print("Testing financial knowledge query:")
    results = get_financial_knowledge("What is a stock?")
    print(results)
    
    print("\nTesting sector knowledge query:")
    results = get_sector_knowledge({"query": "cloud computing", "sector": "tech"})
    print(results)
    
    print("\nTesting investment strategies query:")
    results = get_investment_strategies("value investing")
    print(results)
    
    print("\nTesting market analysis patterns query:")
    results = get_market_analysis_patterns("technical analysis")
    print(results)
    
    print("\nTesting risk management guidelines query:")
    results = get_risk_management_guidelines("diversification")
    print(results)