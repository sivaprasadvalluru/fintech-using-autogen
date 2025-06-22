"""
Agent module for Fintech-AutoGen Application
"""

from fintech_autogen.agents.portfolio_manager import create_portfolio_manager_team, get_portfolio_manager_agent
from fintech_autogen.agents.market_analyst import create_market_analyst_team, get_market_analyst_agent
from fintech_autogen.agents.financial_educator import create_financial_educator_team, get_financial_educator_agent
from fintech_autogen.agents.risk_assessment import create_risk_assessment_team, get_risk_assessment_agent
from fintech_autogen.agents.research_agent import create_research_agent, get_research_agent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os

def get_global_model_client(model_name: str = "gpt-4o-mini", api_key: str = None):
    """Singleton for global model client."""
    if not hasattr(get_global_model_client, "_client"):
        get_global_model_client._client = OpenAIChatCompletionClient(
            model=model_name,
            api_key=api_key or os.environ.get("OPENAI_API_KEY")
        )
    return get_global_model_client._client

__all__ = [
    "create_portfolio_manager_team",
    "get_portfolio_manager_agent",
    "create_market_analyst_team",
    "get_market_analyst_agent",
    "create_financial_educator_team",
    "get_financial_educator_agent",
    "create_risk_assessment_team",
    "get_risk_assessment_agent",
    "create_research_agent",
    "get_research_agent",
    "get_global_model_client"
]