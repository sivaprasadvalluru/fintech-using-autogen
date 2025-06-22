"""
Teams module for Fintech-AutoGen Application
"""

from fintech_autogen.teams.financial_education_team import create_financial_education_team
from fintech_autogen.teams.portfolio_optimization_team import create_portfolio_optimization_flow
from fintech_autogen.teams.market_research_team import create_market_research_team
from fintech_autogen.teams.master_orchestrator import MasterOrchestrator

__all__ = [
    "create_financial_education_team",
    "create_portfolio_optimization_flow",
    "create_market_research_team",
    "MasterOrchestrator"
]