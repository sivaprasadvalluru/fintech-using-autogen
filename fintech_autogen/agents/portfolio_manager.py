"""
Portfolio Manager Agent

This module defines the Portfolio Manager Agent which handles portfolio operations,
manages holdings and transactions, and provides portfolio analytics.
"""

import os
from typing import Any, List, Optional
import logging

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import TextMentionTermination

# Import tools
from fintech_autogen.tools.external_tools import setup_sql_database_toolkit
from fintech_autogen.tools.kb_tools import (
    get_investment_strategies,
    get_risk_management_guidelines,
    format_results_as_text
)


def _build_agent(
    name: str,
    model_name: str,
    api_key: Optional[str],
    tools: list,
    default_system_message: str,
    system_message: Optional[str] = None
):
    from fintech_autogen.agents import get_global_model_client
    model_client = get_global_model_client(model_name, api_key)
    if system_message is None:
        system_message = default_system_message
    return AssistantAgent(
        name=name,
        model_client=model_client,
        tools=tools,
        system_message=system_message,
        reflect_on_tool_use=True,
    )


def _get_tools_and_message():
    tools = []
    sql_tools = setup_sql_database_toolkit()
    if sql_tools:
        tools.extend(sql_tools)
    tools.append(get_investment_strategies)
    tools.append(get_risk_management_guidelines)
    default_system_message = (
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
        "Ensure all recommendations consider the user's risk tolerance and investment goals.\n\n"
        "When you have completed the task, include 'TERMINATE' in your final response."
    )
    return tools, default_system_message


def create_portfolio_manager_team(
    name: str = "PortfolioManager",
    model_name: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    system_message: Optional[str] = None
) -> RoundRobinGroupChat:
    """
    Factory function to create a Portfolio Manager team (RoundRobinGroupChat with a single AssistantAgent).
    Handles portfolio operations, analytics, and recommendations.
    Returns a team instance ready for streaming.
    """
    tools, default_system_message = _get_tools_and_message()
    agent = _build_agent(
        name=name,
        model_name=model_name,
        api_key=api_key,
        tools=tools,
        default_system_message=default_system_message,
        system_message=system_message
    )
    text_termination = TextMentionTermination("TERMINATE")
    team = RoundRobinGroupChat(
        [agent],
        termination_condition=text_termination
    )
    return team


def get_portfolio_manager_agent(
    name: str = "PortfolioManager",
    model_name: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    system_message: Optional[str] = None
) -> AssistantAgent:
    """
    Returns a single AssistantAgent for portfolio management (not a team).
    """
    tools, default_system_message = _get_tools_and_message()
    return _build_agent(
        name=name,
        model_name=model_name,
        api_key=api_key,
        tools=tools,
        default_system_message=default_system_message,
        system_message=system_message
    )


def _get_demo_tasks():
    return [
        "Show the current portfolio composition and performance for admin@example.com.",
        "Suggest a rebalancing strategy for a conservative investor with user@example.com.",
        "Add a new stock to the portfolio for analyst@example.com and update the holdings.",
        "Generate a portfolio report for the last quarter for admin@example.com.",
        "What are the risk metrics for the portfolio of user@example.com?"
    ]


async def run_portfolio_manager_demo():
    """Run a demonstration of the Portfolio Manager Agent"""
    from dotenv import load_dotenv
    from autogen_agentchat.ui import Console
    load_dotenv()
    print("\n" + "="*50)
    print("Portfolio Manager Agent Demo")
    print("="*50)
    manager = create_portfolio_manager_team()
    tasks = _get_demo_tasks()
    for i, task in enumerate(tasks, 1):
        print(f"\nTask {i}: {task}")
        print("-" * 50)
        stream =  manager.run_stream(task=task)
        await Console(stream)
        if i < len(tasks):
            input("\nPress Enter to continue to the next task...")
    print("\nDemo completed!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_portfolio_manager_demo())