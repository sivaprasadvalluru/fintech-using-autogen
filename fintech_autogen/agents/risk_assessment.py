"""
Risk Assessment Agent

This module defines the Risk Assessment Agent which evaluates investment risks,
suggests risk mitigation strategies, and balances risk-reward profiles.
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
    get_risk_management_guidelines,
    format_results_as_text
)
from fintech_autogen.tools.external_tools import setup_sql_database_toolkit

def _get_tools_and_message():
    tools = [
        get_risk_management_guidelines,
        format_results_as_text
    ]
    sql_tools = setup_sql_database_toolkit()
    if sql_tools:
        tools.extend(sql_tools)
    default_system_message = (
        "You are a Risk Assessment Agent responsible for evaluating investment risks, "
        "suggesting risk mitigation strategies, and balancing risk-reward profiles.\n\n"
        "Your capabilities include:\n"
        "1. Assessing portfolio and transaction risks\n"
        "2. Retrieving and summarizing risk management guidelines\n"
        "3. Suggesting risk mitigation and diversification strategies\n"
        "4. Calculating risk metrics using available data\n"
        "5. Providing actionable, data-driven advice\n\n"
        "Always be thorough, analytical, and user-focused in your responses.\n"
        "When you have completed the risk assessment, include 'TERMINATE' in your final response."
    )
    return tools, default_system_message

def _build_agent(
    name: str = "RiskAssessmentAgent",
    model_name: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    tools: Optional[list] = None,
    system_message: Optional[str] = None,
    default_system_message: Optional[str] = None
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

def create_risk_assessment_team(
    name: str = "RiskAssessmentAgent",
    model_name: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    system_message: Optional[str] = None
) -> RoundRobinGroupChat:
    """
    Create a risk assessment team for evaluating investment risks and mitigation.
    Returns a RoundRobinGroupChat team instance ready for streaming.
    """
    tools, default_system_message = _get_tools_and_message()
    agent = _build_agent(
        name=name,
        model_name=model_name,
        api_key=api_key,
        tools=tools,
        system_message=system_message,
        default_system_message=default_system_message
    )
    text_termination = TextMentionTermination("TERMINATE")
    team = RoundRobinGroupChat([
        agent
    ], termination_condition=text_termination)
    return team

def get_risk_assessment_agent(
    name: str = "RiskAssessmentAgent",
    model_name: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    system_message: Optional[str] = None
) -> AssistantAgent:
    """
    Returns a single AssistantAgent for risk assessment (not a team).
    """
    tools, default_system_message = _get_tools_and_message()
    return _build_agent(
        name=name,
        model_name=model_name,
        api_key=api_key,
        tools=tools,
        system_message=system_message,
        default_system_message=default_system_message
    )

def _get_demo_tasks():
    return [
        "Assess the risk profile of the portfolio for admin@example.com.",
        "Suggest risk mitigation strategies for a tech-heavy portfolio for user@example.com.",
        "Summarize risk management guidelines for new investors.",
        "Calculate risk metrics for the portfolio of analyst@example.com.",
        "What are the main risk factors in emerging markets?"
    ]

async def run_risk_assessment_demo():
    """Run a demonstration of the Risk Assessment Agent"""
    from dotenv import load_dotenv
    from autogen_agentchat.ui import Console
    load_dotenv()
    print("\n" + "="*50)
    print("Risk Assessment Agent Demo")
    print("="*50)
    agent = create_risk_assessment_team()
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
    asyncio.run(run_risk_assessment_demo())
