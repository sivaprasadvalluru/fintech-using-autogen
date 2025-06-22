"""
Market Analyst Agent

This module defines the Market Analyst Agent which analyzes market trends,
provides sector insights, and identifies investment opportunities.
"""

import os
from typing import Any, List, Optional
import logging

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import TextMentionTermination

# Import tools
from fintech_autogen.tools.external_tools import setup_yahoo_finance
from fintech_autogen.tools.kb_tools import (
    get_sector_knowledge,
    get_market_analysis_patterns,
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
    yf_tools = setup_yahoo_finance()
    if yf_tools:
        tools.extend(list(yf_tools.values()))
    def sector_knowledge_tool(query: str, sector: str = "tech", n_results: int = 3):
        return get_sector_knowledge({"query": query, "sector": sector, "n_results": n_results})
    tools.append(sector_knowledge_tool)
    tools.append(get_market_analysis_patterns)
    default_system_message = (
        "You are a Market Analyst Agent responsible for analyzing market trends, providing sector insights, and identifying investment opportunities.\n\n"
        "Your capabilities include:\n"
        "1. Analyzing sector and market trends\n"
        "2. Retrieving real-time and historical market data\n"
        "3. Identifying key market drivers\n"
        "4. Providing investment opportunity analysis\n"
        "5. Using knowledge base and external data sources\n\n"
        "Always provide data-driven, up-to-date, and actionable insights.\n"
        "When you have completed the task, include 'TERMINATE' in your final response."
    )
    return tools, default_system_message

def create_market_analyst_team(
    name: str = "MarketAnalyst",
    model_name: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    system_message: Optional[str] = None
) -> RoundRobinGroupChat:
    """
    Create a Market Analyst team (RoundRobinGroupChat with a single AssistantAgent).
    Analyzes market trends, provides sector insights, and identifies investment opportunities.
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

def get_market_analyst_agent(
    name: str = "MarketAnalyst",
    model_name: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    system_message: Optional[str] = None
) -> AssistantAgent:
    """
    Returns a single AssistantAgent for market analysis (not a team).
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
        "Analyze the current trends in the technology sector.",
        "Provide sector insights for the healthcare industry.",
        "Identify investment opportunities in renewable energy.",
        "Summarize key market drivers for the financial sector.",
        "What are the latest patterns in global markets?"
    ]

async def run_market_analyst_demo():
    """Run a demonstration of the Market Analyst Agent"""
    from dotenv import load_dotenv
    from autogen_agentchat.ui import Console
    load_dotenv()
    print("\n" + "="*50)
    print("Market Analyst Agent Demo")
    print("="*50)
    analyst = create_market_analyst_team()
    tasks = _get_demo_tasks()
    for i, task in enumerate(tasks, 1):
        print(f"\nTask {i}: {task}")
        print("-" * 50)
        stream =  analyst.run_stream(task=task)
        await Console(stream)
        if i < len(tasks):
            input("\nPress Enter to continue to the next task...")
    print("\nDemo completed!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_market_analyst_demo())
