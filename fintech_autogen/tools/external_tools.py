import os
from pathlib import Path
from typing import Dict, Any, List
import logging

def setup_sql_database_toolkit():
    logger = logging.getLogger("external_tools")
    logger.info("Setting up Autogen SQL tools.")
    try:
        # Import required packages
        from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
        from langchain_community.utilities import SQLDatabase
        from langchain_openai import ChatOpenAI
        from autogen_ext.tools.langchain import LangChainToolAdapter
        
        # Setup SQLDatabase
        DB_DIR = Path(__file__).parent.parent / "database"
        DB_FILE = DB_DIR / "fintech.db"
        db_uri = f"sqlite:///{DB_FILE}"
        
        # Create SQLDatabase instance
        db = SQLDatabase.from_uri(db_uri)
        
        # Create a simple LLM for the toolkit
        llm = ChatOpenAI(temperature=0,model="gpt-4o-mini")
        
        # Create toolkit
        sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        
        # Extract tools from the toolkit
        langchain_tools = sql_toolkit.get_tools()
        
        # Convert each Langchain tool to an Autogen tool
        autogen_tools = []
        for tool in langchain_tools:
            autogen_tool = LangChainToolAdapter(tool)
            autogen_tools.append(autogen_tool)
            
        logger.info("Autogen SQL tools setup complete.")
        return autogen_tools
    
    except ImportError as e:
        logger.error(f"Please install required packages: pip install langchain langchain-openai autogen-ext openai. Error: {e}")
        return []

def setup_yahoo_finance():
    logger = logging.getLogger("external_tools")
    logger.info("Setting up Yahoo Finance tools.")
    try:
        import yfinance as yf
        
        # Example functions using Yahoo Finance
        def get_stock_info(ticker: str) -> Dict[str, Any]:
            """Get stock information using Yahoo Finance"""
            stock = yf.Ticker(ticker)
            return stock.info
        
        def get_historical_data(ticker: str, period: str = "1y") -> Any:
            """Get historical stock data using Yahoo Finance"""
            stock = yf.Ticker(ticker)
            return stock.history(period=period)
        
        def get_market_news() -> List[Dict[str, Any]]:
            """Get market news from Yahoo Finance"""
            import requests
            import datetime
            # Yahoo Finance does not have a public news API, but we can scrape their RSS feed for headlines
            rss_url = "https://finance.yahoo.com/news/rssindex"
            try:
                import feedparser
            except ImportError:
                raise ImportError("Please install feedparser: pip install feedparser")
            feed = feedparser.parse(rss_url)
            news = []
            for entry in feed.entries:
                news.append({
                    "title": entry.get("title"),
                    "link": entry.get("link"),
                    "published": entry.get("published"),
                    "summary": entry.get("summary", "")
                })
            return news
            
        logger.info("Yahoo Finance tools setup complete.")
        return {
            "get_stock_info": get_stock_info,
            "get_historical_data": get_historical_data,
            "get_market_news": get_market_news
        }
    
    except ImportError as e:
        logger.error(f"Please install yfinance: pip install yfinance. Error: {e}")
        return {}


# For testing
if __name__ == "__main__":
    # Test Autogen SQL tools
    autogen_sql_tools = setup_sql_database_toolkit()
    if autogen_sql_tools:
        print("SQL database tools setup successful")
        print(f"Number of Autogen-compatible SQL tools: {len(autogen_sql_tools)}")
    
    # Test Yahoo Finance setup
    yf_functions = setup_yahoo_finance()
    if yf_functions:
        print("\nYahoo Finance setup successful")
        print("Getting Apple stock info...")
        info = yf_functions["get_stock_info"]("AAPL")
        print(f"Current price: ${info.get('currentPrice', 'N/A')}")