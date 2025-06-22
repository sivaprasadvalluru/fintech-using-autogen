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

## UI Components

### 1. User Authentication
- Radio button selection for Admin/User role
- Email input for user authentication
- Session management

### 2. Admin Interface
- Document upload interface for knowledge base
- ChromaDB ingestion management
- User management dashboard
- System monitoring

### 3. User Interface
- Chat interface with conversation history
- Portfolio dashboard with visualizations
- Educational content display

## Implementation Plan

### Phase 1: Project Setup (COMPLETED)
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

### Phase 2: Tool Development (COMPLETED)
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

### Phase 5: UI and Integration
1. Streamlit UI development
2. End-to-end integration (UI wired to agents/teams via orchestrator)
3. Documentation and example generation

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