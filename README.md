# Fintech-AutoGen Application

## Overview
A multi-agent system for portfolio management, market analysis, and financial education powered by AutoGen and orchestrated by GraphFlow.

## Features
- Portfolio management and optimization
- Market analysis and trend identification
- Financial education with personalized learning paths
- Risk assessment and mitigation strategies
- Real-time market data research

## Project Structure
```
fintech-using-autogen/
│
├── fintech_autogen/                # Main package
│   ├── __init__.py                 # Package initialization
│   ├── agents/                     # Individual agent implementations
│   │   ├── __init__.py
│   │   └── portfolio_manager.py    # Portfolio Manager Agent
│   ├── database/                   # SQLite database implementation
│   │   ├── __init__.py
│   │   └── db_setup.py             # Database setup and initialization
│   ├── knowledge_base/             # ChromaDB knowledge base setup
│   │   ├── __init__.py
│   │   └── kb_setup.py             # Knowledge base setup
│   ├── tools/                      # Tool adapters for various functionalities
│   │   ├── __init__.py
│   │   ├── kb_tools.py             # Knowledge base retrieval tools
│   │   └── external_tools.py       # Integration with external tool libraries
│   ├── teams/                      # Team structure configurations
│   │   └── __init__.py
│   └── ui/                         # Streamlit UI components
│       └── __init__.py
│
├── examples/                       # Example scripts demonstrating functionality
│   └── portfolio_manager_demo.py   # Portfolio Manager Agent demo
│
├── tests/                          # Test modules
│   └── __init__.py
│
├── plots/                          # Generated visualization plots
├── pyproject.toml                  # Project configuration and dependencies
└── README.md                       # Project documentation
```

## Installation
1. Clone the repository
2. Install dependencies:
   ```
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

## Usage
1. Run the Portfolio Manager demonstration:
   ```
   python -m examples.portfolio_manager_demo
   ```

## Tool Overview

Instead of custom implementations for everything, we leverage existing tools and libraries:

### Database Access
- Using **Langchain's SQLDatabaseToolkit** for direct SQL database operations
- Provides dynamic SQL query generation and execution based on user needs
- Eliminates need for maintaining custom database access code

### Financial Data API
- Using **Yahoo Finance API** (yfinance) for market data retrieval
- Stock price data, company information, historical data
- Well-maintained and regularly updated with latest market information

### Portfolio Analytics & Visualization
- Using **Python REPL Tool** for on-demand code generation and execution
- Leverages pandas, matplotlib, and other data science libraries
- More flexible than fixed function implementation
- Allows LLM to generate custom analysis code based on specific user needs

### Knowledge Base Tools (Custom)
- Financial knowledge retrieval (ChromaDB specific implementation)
- Sector-specific knowledge
- Investment strategies
- Market analysis patterns
- Risk management guidelines

## Benefits of External Tools
- Reduced code maintenance burden
- Leveraging battle-tested implementations
- More flexible code generation for specific analysis needs
- Faster development of higher-level agent functionalities

## Implementation Plan
- Phase 1: Project Setup ✓
- Phase 2: Tool Development ✓ (using external tools)
- Phase 3: Agent Development (In Progress)
  - Portfolio Manager Agent ✓
  - Market Analyst Agent
  - Financial Educator Agent
  - Risk Assessment Agent
  - Research Agent (MagenticOne)
- Phase 4: Team Configuration
- Phase 5: UI and Integration 