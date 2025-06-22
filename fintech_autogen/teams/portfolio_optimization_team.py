"""
Portfolio Optimization Flow

This module provides a function to create a portfolio optimization GraphFlow team.
It creates and runs Portfolio Manager, Market Analyst, Risk Assessment, and optionally Financial Educator agents in parallel,
then aggregates and synthesizes their outputs.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from autogen_agentchat.conditions import TextMentionTermination
from fintech_autogen.agents import (
    get_portfolio_manager_agent,
    get_market_analyst_agent,
    get_risk_assessment_agent,
    get_financial_educator_agent,
    get_global_model_client
)

def create_portfolio_optimization_flow(include_educator: bool = True, termination_str: str = "TERMINATE") -> GraphFlow:
    """
    Create a GraphFlow for portfolio optimization with parallel agents and aggregation.
    Returns a GraphFlow instance ready for streaming.
    """
    # Use unique termination texts for each agent
    pm_termination = "PORTFOLIO_MANAGER_DONE"
    analyst_termination = "ANALYST_DONE"
    risk_termination = "RISK_DONE"
    educator_termination = "EDUCATOR_DONE"
    # Pass custom system messages to instruct agents to use their unique termination text
    portfolio_manager = get_portfolio_manager_agent(
        system_message=(
            "You are a Portfolio Manager Agent responsible for managing financial portfolios.\n\n"
            "Your capabilities include:\n"
            "1. Analyzing portfolio composition and performance\n"
            "2. Managing holdings and transactions\n"
            "3. Providing investment recommendations\n"
            "4. Calculating risk metrics\n"
            "5. Generating portfolio reports\n"
            "6. Implementing investment strategies\n"
            "7. Balancing portfolios based on risk-reward profiles\n\n"
            "Use your database tools to retrieve portfolio information and perform operations.\n"
            "Use your knowledge tools to provide context about investment strategies and risk management.\n"
            "Always be precise and data-driven in your analysis.\n"
            f"When you have completed the task, include '{pm_termination}' in your final response."
        )
    )
    market_analyst = get_market_analyst_agent(
        system_message=(
            "You are a Market Analyst Agent responsible for analyzing market trends, providing sector insights, and identifying investment opportunities.\n\n"
            "Your capabilities include:\n"
            "1. Analyzing sector and market trends\n"
            "2. Retrieving real-time and historical market data\n"
            "3. Identifying key market drivers\n"
            "4. Providing investment opportunity analysis\n"
            "5. Using knowledge base and external data sources\n\n"
            "Always provide data-driven, up-to-date, and actionable insights.\n"
            f"When you have completed the task, include '{analyst_termination}' in your final response."
        )
    )
    risk_assessment = get_risk_assessment_agent(
        system_message=(
            "You are a Risk Assessment Agent responsible for evaluating investment risks, suggesting risk mitigation strategies, and balancing risk-reward profiles.\n\n"
            "Your capabilities include:\n"
            "1. Assessing portfolio and transaction risks\n"
            "2. Retrieving and summarizing risk management guidelines\n"
            "3. Suggesting risk mitigation and diversification strategies\n"
            "4. Calculating risk metrics using available data\n"
            "5. Providing actionable, data-driven advice\n\n"
            "Always be thorough, analytical, and user-focused in your responses.\n"
            f"When you have completed the risk assessment, include '{risk_termination}' in your final response."
        )
    )
    financial_educator = get_financial_educator_agent(
        system_message=(
            "You are a Financial Educator Agent responsible for providing financial education, retrieving knowledge from ChromaDB, and creating personalized learning paths.\n\n"
            "Your capabilities include:\n"
            "1. Explaining financial concepts in simple terms\n"
            "2. Retrieving and summarizing knowledge from the knowledge base\n"
            "3. Creating step-by-step learning paths for users\n"
            "4. Providing investment and risk management guidelines\n"
            "5. Answering user questions with clear, educational context\n\n"
            "Always be clear, concise, and supportive in your explanations.\n"
            f"When you have completed the educational task, include '{educator_termination}' in your final response."
        )
    ) if include_educator else None
    agents = [
        portfolio_manager,
        market_analyst,
        risk_assessment
    ]
    if financial_educator is not None:
        agents.append(financial_educator)
    # Build the parallel graph
    builder = DiGraphBuilder()
    for agent in agents:
        builder.add_node(agent)
    # Entry node as a router (does not answer, just forwards)
    entry_model_client = get_global_model_client()
    entry = AssistantAgent(
        "entry",
        model_client=entry_model_client,
        system_message="You are a router. Do not answer the user's question. Just forward the task to all downstream agents."
    )
    builder.add_node(entry)
    for agent in agents:
        builder.add_edge(entry, agent)
    # Join node to aggregate results

    aggregator_termination = "AGGREGATOR_DONE"
    join = AssistantAgent(
        "aggregator",
        model_client=entry_model_client,
        system_message=f"""Aggregate and synthesize all agent outputs into a comprehensive 
        portfolio recommendation. Always include educational context if available.
        When you have completed aggregation, include '{aggregator_termination}' 
        in your final response."""
    )
    builder.add_node(join)
    for agent in agents:
        builder.add_edge(agent, join)
    builder.set_entry_point(entry)
    graph = builder.build()

    return GraphFlow(
        participants=builder.get_participants(),
        graph=graph,
        termination_condition=TextMentionTermination(aggregator_termination)
    )

def _get_demo_tasks():
    return [
        "Given the current tech sector trends, how should I rebalance my portfolio to maximize returns while maintaining moderate risk for user admin@example.com?",
        "Evaluate the risk and suggest optimization for a portfolio with 60% tech, 30% healthcare, and 10% bonds for user user@example.com.",
        "What are the latest market opportunities and risk mitigation strategies for financial services for user analyst@example.com?"
    ]

async def run_portfolio_optimization_team_demo():
    from dotenv import load_dotenv
    from autogen_agentchat.ui import Console
    load_dotenv()
    print("\n" + "="*50)
    print("Portfolio Optimization Team Demo")
    print("="*50)
    team = create_portfolio_optimization_flow()
    tasks = _get_demo_tasks()
    for i, task in enumerate(tasks, 1):
        print(f"\nTask {i}: {task}")
        print("-" * 50)
        stream =  team.run_stream(task=task)
        await Console(stream)
        if i < len(tasks):
            input("\nPress Enter to continue to the next task...")
    print("\nDemo completed!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_portfolio_optimization_team_demo())
