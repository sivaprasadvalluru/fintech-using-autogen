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
│   │   ├── portfolio_manager.py
│   │   ├── market_analyst.py
│   │   ├── financial_educator.py
│   │   ├── risk_assessment.py
│   │   └── research_agent.py
│   ├── database/                   # SQLite database implementation
│   │   ├── __init__.py
│   │   ├── db_setup.py
│   │   ├── fintech.db
│   │   └── queries.py
│   ├── knowledge_base/             # ChromaDB knowledge base setup
│   │   ├── __init__.py
│   │   ├── kb_setup.py
│   │   ├── chroma_db/
│   │   │   └── chroma.sqlite3
│   │   └── kb_texts/
│   │       ├── etf_knowledge.txt
│   │       ├── finance_sector.txt
│   │       ├── general_finance.txt
│   │       ├── healthcare_sector.txt
│   │       ├── investment_strategies.txt
│   │       ├── market_analysis.txt
│   │       ├── risk_management.txt
│   │       └── tech_sector.txt
│   ├── teams/                      # Team structure configurations
│   │   ├── __init__.py
│   │   ├── financial_education_team.py
│   │   ├── market_research_team.py
│   │   ├── master_orchestrator.py
│   │   └── portfolio_optimization_team.py
│   └── tools/                      # Tool adapters for various functionalities
│       ├── __init__.py
│       ├── kb_tools.py
│       ├── external_tools.py
│       └── cache/
│
├── main.py                         # Main entry point for orchestration
├── pyproject.toml                  # Project configuration and dependencies
├── README.md                       # Project documentation
├── UseCase.md                      # Use case and architecture documentation
└── uv.lock                         # Dependency lock file
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

## Project Execution Guide

All interactions are performed via command-line scripts. No UI is provided in this implementation. You can run the main orchestration or individual agent/team demos as described below.

### Running Example Scenarios

#### 1. Portfolio Optimization with Market Context
- **Scenario:** Optimize your portfolio based on current market conditions.
- **How to Run:**
  - Execute the main orchestrator script:
    ```sh
    python main.py
    # or using uv
    uv pip run python main.py
    ```
  - Follow the prompts or edit `main.py` to set your query, e.g.:
    "Given the current tech sector trends, how should I rebalance my portfolio to maximize returns while maintaining moderate risk?"

#### 2. Investment Decision with Education
- **Scenario:** Get educational context and market analysis for a specific investment.
- **How to Run:**
  - Edit `main.py` or create a new script to send a query such as:
    "Should I invest in healthcare AI companies, and what should I know before investing?"
  - Run:
    ```sh
    python main.py
    # or
    uv pip run python main.py
    ```

#### 3. Market Crisis Response
- **Scenario:** Get guidance during market volatility.
- **How to Run:**
  - Use `main.py` or a custom script to submit a query like:
    "The tech sector is experiencing high volatility. How should I protect my portfolio and identify opportunities?"
  - Run as above.

#### 4. Agent/Team Demos
- **Portfolio Manager Demo:**
  ```sh
  python -m examples.portfolio_manager_demo
  # or
  uv pip run python -m examples.portfolio_manager_demo
  ```
- **Other agents/teams:**
  - You can create similar demo scripts in the `examples/` directory for other agents or teams, following the pattern in `portfolio_manager_demo.py`.

---

## Scenario-to-Script Mapping

| Scenario                                 | Script/File                | How to Run (python/uv)                  |
|------------------------------------------|----------------------------|-----------------------------------------|
| Portfolio Optimization                   | main.py                    | python main.py / uv pip run python main.py |
| Investment Decision with Education       | main.py (customize query)  | python main.py / uv pip run python main.py |
| Market Crisis Response                   | main.py (customize query)  | python main.py / uv pip run python main.py |
| Portfolio Manager Agent Demo             | examples/portfolio_manager_demo.py | python -m examples.portfolio_manager_demo / uv pip run python -m examples.portfolio_manager_demo |

---

## Implementation Plan
- Phase 1: Project Setup ✓
- Phase 2: Tool Development ✓ (using external tools)
- Phase 3: Agent Development ✓
  - Portfolio Manager Agent ✓
  - Market Analyst Agent ✓
  - Financial Educator Agent ✓
  - Risk Assessment Agent ✓
  - Research Agent (MagenticOne) ✓
- Phase 4: Team Configuration ✓
- Phase 5: Integration (No UI in this implementation)