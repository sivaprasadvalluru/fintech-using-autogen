"""
Financial Educator Agent

This module defines the Financial Educator Agent which retrieves knowledge from ChromaDB,
explains financial concepts, and creates personalized learning paths.
"""

import os
from typing import Any, List, Optional
import logging

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import TextMentionTermination

# Import tools
from fintech_autogen.tools.kb_tools import (
    get_investment_strategies,
    get_risk_management_guidelines,
    format_results_as_text
)

def _build_agent(
    name: str = "FinancialEducator",
    model_name: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    system_message: Optional[str] = None
):
    from fintech_autogen.agents import get_global_model_client
    model_client = get_global_model_client(model_name, api_key)
    tools = [
        get_investment_strategies,
        get_risk_management_guidelines,
        format_results_as_text
    ]
    if system_message is None:
        system_message = (
            "You are a Financial Educator Agent responsible for providing financial education, "
            "retrieving knowledge from ChromaDB, and creating personalized learning paths.\n\n"
            "Your capabilities include:\n"
            "1. Explaining financial concepts in simple terms\n"
            "2. Retrieving and summarizing knowledge from the knowledge base\n"
            "3. Creating step-by-step learning paths for users\n"
            "4. Providing investment and risk management guidelines\n"
            "5. Answering user questions with clear, educational context\n\n"
            "Always be clear, concise, and supportive in your explanations.\n"
            "When you have completed the educational task, include 'TERMINATE' in your final response."
        )
    agent = AssistantAgent(
        name=name,
        model_client=model_client,
        tools=tools,
        system_message=system_message,
        reflect_on_tool_use=True,
    )
    return agent

def create_financial_educator_team(
    name: str = "FinancialEducator",
    model_name: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    system_message: Optional[str] = None
) -> RoundRobinGroupChat:
    """
    Create a Financial Educator team (RoundRobinGroupChat with a single AssistantAgent).
    Provides financial education, knowledge retrieval, and learning path creation.
    Returns a team instance ready for streaming.
    """
    agent = _build_agent(
        name=name,
        model_name=model_name,
        api_key=api_key,
        system_message=system_message
    )
    text_termination = TextMentionTermination("TERMINATE")
    team = RoundRobinGroupChat(
        [agent],
        termination_condition=text_termination
    )
    return team

def get_financial_educator_agent(
    name: str = "FinancialEducator",
    model_name: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    system_message: Optional[str] = None
) -> AssistantAgent:
    """
    Returns a single AssistantAgent for financial education (not a team).
    """
    return _build_agent(
        name=name,
        model_name=model_name,
        api_key=api_key,
        system_message=system_message
    )

# Demo logic for running as a script
def _get_demo_tasks():
    return [
        "Explain the concept of compound interest.",
        "What are some good investment strategies for beginners?",
        "Create a personalized learning path for understanding ETFs.",
        "Summarize risk management guidelines for new investors.",
        "What should I know before investing in the healthcare sector?"
    ]

async def run_financial_educator_demo():
    """Run a demonstration of the Financial Educator Agent"""
    import asyncio
    from dotenv import load_dotenv
    from autogen_agentchat.ui import Console
    load_dotenv()
    print("\n" + "="*50)
    print("Financial Educator Agent Demo")
    print("="*50)
    educator = create_financial_educator_team()
    tasks = _get_demo_tasks()
    for i, task in enumerate(tasks, 1):
        print(f"\nTask {i}: {task}")
        print("-" * 50)
        stream =  educator.run_stream(task=task)
        await Console(stream)
        if i < len(tasks):
            input("\nPress Enter to continue to the next task...")
    print("\nDemo completed!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_financial_educator_demo())
