"""
Research Agent (MagenticOne)

This module defines the Research Agent using MagenticOne for web research, real-time market data, and news analysis.
"""

import os
from typing import Optional
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.teams.magentic_one import MagenticOne
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat

def _build_agent(
    name: str = "ResearchAgent",
    model_name: str = "gpt-4o-mini",
    api_key: Optional[str] = None
):
    model_client = OpenAIChatCompletionClient(
        model=model_name,
        api_key=api_key or os.environ.get("OPENAI_API_KEY")
    )
    agent = MagenticOne(client=model_client)
    return agent

def create_research_agent(
    name: str = "ResearchAgent",
    model_name: str = "gpt-4o-mini",
    api_key: Optional[str] = None
) -> RoundRobinGroupChat:
    """
    Create a Research Agent team (RoundRobinGroupChat with a single AssistantAgent).
    Returns a team instance ready for streaming.
    """
    return _build_agent(name=name, model_name=model_name, api_key=api_key)

def get_research_agent(
    name: str = "ResearchAgent",
    model_name: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    system_message: Optional[str] = None
) -> AssistantAgent:
    """
    Returns a single AssistantAgent for research (not a team).
    """
    return _build_agent(name=name, model_name=model_name, api_key=api_key)

def _get_demo_tasks():
    return [
        "Find the latest news about the electric vehicle market.",
        "Summarize real-time market data for S&P 500.",
        "What are the top trends in AI research this month?",
        "Provide a brief on recent financial regulations.",
        "Analyze the impact of global events on stock markets."
    ]

async def run_research_agent_demo():
    """Run a demonstration of the Research Agent"""
    from dotenv import load_dotenv
    from autogen_agentchat.ui import Console
    load_dotenv()
    print("\n" + "="*50)
    print("Research Agent Demo")
    print("="*50)
    agent = create_research_agent()
    tasks = _get_demo_tasks()
    for i, task in enumerate(tasks, 1):
        print(f"\nTask {i}: {task}")
        print("-" * 50)
        stream =  agent.run_stream(task=task)
        await Console(stream)
        if i < len(tasks):
            input("\nPress Enter to continue to the next task...")
    print("\nDemo completed!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_research_agent_demo())
