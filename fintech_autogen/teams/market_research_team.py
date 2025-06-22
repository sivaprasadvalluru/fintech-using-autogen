"""
Market Research Flow

This module provides a function to create a market research team using the MagenticOne Research Agent.
"""

from fintech_autogen.agents import get_research_agent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination

def create_market_research_team(termination_str: str = "TERMINATE", model_name: str = "gpt-4o-mini", api_key=None) -> RoundRobinGroupChat:
    """
    Create a RoundRobinGroupChat for market research with the MagenticOne Research Agent.
    Returns a RoundRobinGroupChat instance ready for streaming.
    """
    research_agent = get_research_agent(
        name="ResearchAgent",
        model_name=model_name,
        api_key=api_key
    )
    return research_agent

def _get_demo_tasks():
    return [
        "Find the latest news about the electric vehicle market.",
        # "Summarize real-time market data for S&P 500.",
        # "What are the top trends in AI research this month?"
    ]

async def run_market_research_team_demo():
    from dotenv import load_dotenv
    from autogen_agentchat.ui import Console
    load_dotenv()
    print("\n" + "="*50)
    print("Market Research Team Demo")
    print("="*50)
    team = create_market_research_team()
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
    asyncio.run(run_market_research_team_demo())

