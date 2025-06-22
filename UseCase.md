# Fintech-AutoGen Application

## Overview
This document outlines the various use cases, agent interactions, and team structures for our fintech application. The application combines portfolio management, market analysis, and financial education using a multi-agent system powered by AutoGen, with GraphFlow orchestrating agent interactions.

## System Components

### 1. Database Structure
- Users (with admin/regular user roles)
- Portfolios
- Stocks
- Portfolio Holdings
- Transactions
- Market News

### 2. Knowledge Base (ChromaDB)
- General Financial Knowledge
- Sector-Specific Knowledge:
  - Technology Sector
  - Financial Services Sector
  - Healthcare Sector
- Investment Strategies
- Market Analysis Patterns
- Risk Management Guidelines

### 3. Agents and Teams

#### Individual Agents
1. **Portfolio Manager Agent**
   - Handles portfolio operations
   - Manages holdings and transactions
   - Provides portfolio analytics

2. **Market Analyst Agent**
   - Analyzes market trends
   - Provides sector insights
   - Identifies investment opportunities

3. **Financial Educator Agent**
   - Retrieves knowledge from ChromaDB
   - Explains financial concepts
   - Creates personalized learning paths

4. **Risk Assessment Agent**
   - Evaluates investment risks
   - Suggests risk mitigation strategies
   - Balances risk-reward profiles

5. **Research Agent (MagenticOne)**
   - Conducts web research
   - Gathers real-time market data
   - Provides news analysis

#### Team Structures
1. **Financial Education Team (RoundRobinGroupChat)**
   - Combines Financial Educator and Market Analyst agents
   - Sequential processing for educational content and context
   - Termination condition: complete learning objectives

2. **Portfolio Optimization Team (Parallel Execution via GraphFlow)**
   - Executes Portfolio Manager, Market Analyst, and Risk Assessment agents in parallel using GraphFlow's parallel edges.
   - Aggregates and synthesizes outputs for comprehensive recommendations.
   - Termination condition: complete portfolio recommendations.

3. **Market Research Team (MagenticOne)**
   - Web research capabilities
   - Real-time data analysis
   - Crisis response strategies

4. **Master Orchestration (GraphFlow)**
   - Manages workflow between teams
   - Routes queries based on intent
   - Handles state transitions

### 4. Tools (LangChainToolAdapter)
- ChromaDB Knowledge Retrieval
- Database Operations
- Financial Data API Access
- Portfolio Analytics
- Market Data Analysis
- Visualization Generation

## System Architecture Overview

The Fintech-AutoGen system consists of the following layers:

1. **User Input Layer:** Users interact with the system by running scripts or command-line commands (e.g., via `main.py`).
2. **Orchestration Layer (GraphFlow):** The `master_orchestrator.py` receives user queries, detects intent, and routes requests to the appropriate team or agent.
3. **Teams & Agents:** Teams (e.g., Portfolio Optimization Team) coordinate multiple agents (e.g., Portfolio Manager, Market Analyst) to process complex tasks.
4. **Tools Layer:** Agents use tools (in `tools/`) to access the database, knowledge base, and external APIs.
5. **Data & Knowledge Layer:** The SQLite database and ChromaDB knowledge base provide structured and unstructured data.

---

## Example User Journey

**Scenario:** A user wants to rebalance their portfolio based on current tech sector trends.

1. **User submits query** by running a script or calling a function in `main.py`:
   "Given the current tech sector trends, how should I rebalance my portfolio to maximize returns while maintaining moderate risk?"

2. **Orchestration:**  
   - `master_orchestrator.py` (GraphFlow) analyzes the query, detects the need for portfolio optimization, and routes the request to the Portfolio Optimization Team.

3. **Team Processing:**  
   - The Portfolio Optimization Team runs the Portfolio Manager, Market Analyst, and Risk Assessment agents in parallel.
   - Each agent uses relevant tools (e.g., database queries, knowledge base retrieval) to generate insights.

4. **Aggregation:**  
   - The team aggregates results, synthesizes recommendations, and passes them back to the orchestrator.

5. **Response:**  
   - The orchestrator returns the final, comprehensive response to the user (printed to console or returned by the script).

---

## Orchestration Logic

- The `master_orchestrator.py` uses intent detection to determine which team or agent should handle a user query.
- For example, investment education queries are routed to the Financial Education Team, while portfolio optimization queries go to the Portfolio Optimization Team.
- The orchestration logic is implemented using GraphFlow, which supports both sequential and parallel agent execution.

---

## Tools and Integration

| Tool Name                | File                        | Purpose                                      |
|--------------------------|-----------------------------|----------------------------------------------|
| ChromaDB Retrieval       | `tools/kb_tools.py`         | Retrieve knowledge base content              |
| SQLDatabaseToolkit       | `tools/external_tools.py`   | Query the SQLite database                    |
| Yahoo Finance API        | `tools/external_tools.py`   | Fetch real-time market data                  |
| LangChainToolAdapter     | `tools/kb_tools.py`         | Integrate LangChain with ChromaDB            |

## Complex Use Cases

### 1. Portfolio Optimization with Market Context

#### Scenario: User wants to optimize portfolio based on market conditions
**Flow:**
1. User submits complex query
2. GraphFlow:
   - Analyzes query intent
   - Determines required agents
   - Sets interaction sequence

**Questions and Answers:**
```
Q: "Given the current tech sector trends, how should I rebalance my portfolio to maximize returns while maintaining moderate risk?"

Flow:
1. GraphFlow:
   - Identifies need for portfolio optimization
   - Routes to Portfolio Optimization Team (parallel execution)

2. Portfolio Optimization Team:
   a. Parallel execution (via GraphFlow):
      - Market Analyst Agent:
         * Analyzes tech sector trends
         * Identifies key market drivers
         * Provides market outlook
      - Portfolio Manager Agent:
         * Analyzes current portfolio composition
         * Calculates risk metrics
         * Generates rebalancing suggestions
      - Risk Assessment Agent:
         * Evaluates risk levels
         * Suggests risk-balanced allocations
         * Provides mitigation strategies
      - Financial Educator Agent:
         * Retrieves relevant investment strategies
         * Gathers risk management guidelines
         * Provides educational context

   b. Results Aggregation:
      - The Portfolio Optimization Team (via GraphFlow) aggregates and synthesizes insights from all agents
      - Generates comprehensive recommendations
      - Provides educational context

3. GraphFlow:
   - Delivers comprehensive response to user
```

### 2. Investment Decision with Education

#### Scenario: User wants to make an informed investment decision
**Flow:**
1. User asks about specific investment
2. GraphFlow coordinates multiple teams

**Questions and Answers:**
```
Q: "Should I invest in healthcare AI companies, and what should I know before investing?"

Flow:
1. GraphFlow:
   - Recognizes need for education and market analysis
   - Routes to Financial Education Team (RoundRobinGroupChat)

2. Financial Education Team:
   a. Financial Educator Agent:
      - Queries ChromaDB for healthcare AI sector knowledge
      - Retrieves relevant investment guidelines
      - Gathers risk management information

   b. Market Analyst Agent:
      - Analyzes healthcare AI market trends
      - Identifies key players
      - Provides market outlook

3. Portfolio Optimization Team:
   - Portfolio Manager Agent:
      * Assesses portfolio fit
      * Suggests allocation strategy
   - Risk Assessment Agent:
      * Provides risk assessment
      * Suggests diversification strategies

4. GraphFlow:
   - Combines educational content with market analysis
   - Ensures balanced perspective
   - Delivers comprehensive response
```

### 3. Market Crisis Response

#### Scenario: User needs guidance during market volatility
**Flow:**
1. User asks about market situation
2. GraphFlow manages multiple team inputs

**Questions and Answers:**
```
Q: "The tech sector is experiencing high volatility. How should I protect my portfolio and identify opportunities?"

Flow:
1. GraphFlow:
   - Recognizes urgency of situation
   - Prioritizes market analysis
   - Routes to Market Research Team (MagenticOne)

2. Market Research Team:
   - MagenticOne Agent:
      * Conducts web research on current situation
      * Gathers expert opinions and news
      * Provides real-time market insights

3. Portfolio Optimization Team:
   a. Parallel execution (via GraphFlow):
      - Market Analyst Agent:
         * Analyzes current market conditions
         * Identifies volatility drivers
         * Provides short-term outlook
      - Portfolio Manager Agent:
         * Assesses portfolio vulnerability
         * Suggests protective measures
         * Identifies potential opportunities
      - Risk Assessment Agent:
         * Retrieves crisis management strategies
         * Suggests hedging techniques
         * Provides risk mitigation advice

4. GraphFlow:
   - Ensures balanced perspective
   - Prioritizes critical information
   - Delivers actionable response
```


## Implementation Plan

### Phase 1: Project Setup 
1. Project structure created with directories for:
   - Database (SQLite)
   - Knowledge base (ChromaDB)
   - Agents
   - Teams
   - Tools
   - UI
2. SQLite database schema designed with tables for:
   - Users (with admin/regular user roles)
   - Portfolios
   - Stocks
   - Portfolio Holdings
   - Transactions
   - Market News
3. ChromaDB knowledge base configured with collections for:
   - General Financial Knowledge
   - Sector-Specific Knowledge (Tech, Finance, Healthcare)
   - Investment Strategies
   - Market Analysis Patterns
   - Risk Management Guidelines
4. Basic configuration files created (requirements.txt, README.md, main.py)

### Phase 2: Tool Development 
1. Knowledge retrieval tools (kb_tools.py)
   - LangChain's Chroma integration for vector search
   - Topic-specific knowledge retrieval functions
   - Context-aware querying capabilities
2. External tools integration (external_tools.py)
   - SQLDatabaseToolkit setup with Langchain for database operations
   - Yahoo Finance integration for market data retrieval
   - Stock information and historical data functions
   - Market news retrieval

### Phase 3: Agent Development
1. Portfolio Manager Agent
2. Market Analyst Agent
3. Financial Educator Agent
4. Risk Assessment Agent
5. Research Agent (MagenticOne)

### Phase 4: Team Configuration
1. Financial Education Team (RoundRobinGroupChat)
2. Portfolio Optimization Team (Parallel Execution via GraphFlow)
3. Market Research Team (MagenticOne)
4. GraphFlow orchestration



## Agent Interaction Patterns

### 1. Sequential Processing (RoundRobinGroupChat)
```
User -> GraphFlow -> Agent1 -> Agent2 -> Agent3 -> GraphFlow -> User
```

### 2. Dynamic Selection (SelectorGroupChat)
```
User -> GraphFlow -> SelectorGroupChat
                          -> Agent selection based on context
                          -> Selected agent responds
                          -> Next agent selection
                     -> GraphFlow -> User
```

### 3. Research Processing (MagenticOne)
```
User -> GraphFlow -> MagenticOne
                         -> Web research
                         -> Data analysis
                         -> Insight generation
                    -> GraphFlow -> User
```

### 4. Knowledge Base Integration
```
User Query -> GraphFlow
            -> Knowledge Base (ChromaDB)
               -> Content Retrieval via LangChainToolAdapter
               -> Context Synthesis
            -> Agent/Team Processing
            -> GraphFlow (synthesis) -> User
```

## Extensibility

- New agents, teams, or tools can be added by creating new Python modules in the respective directories and registering them in the orchestrator.
- The system is modular, allowing for easy integration of additional data sources or knowledge bases.

## Error Handling

- Agents and tools include basic error handling to manage issues such as missing data, API failures, or invalid queries.
- Errors are logged and user-friendly messages are returned to the user via the script or command line.

## Glossary

- **GraphFlow:** The orchestration engine that manages agent and team workflows.
- **SelectorGroupChat:** A pattern for dynamically selecting agents based on context.
- **RoundRobinGroupChat:** A pattern for sequentially processing tasks through multiple agents.
- **MagenticOne:** The research agent/team responsible for web research and real-time data gathering.