"""
Master Orchestration (GraphFlow)

This module defines the master orchestrator using GraphFlow to route queries to the appropriate team
(Financial Education, Portfolio Optimization, Market Research) based on intent.
"""

from fintech_autogen.teams.financial_education_team import create_financial_education_team
from fintech_autogen.teams.portfolio_optimization_team import create_portfolio_optimization_flow
from fintech_autogen.teams.market_research_team import create_market_research_team
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console
import logging

class MasterOrchestrator:
    """GraphFlow-based orchestrator for routing queries to the correct team(s) based on use case intent."""
    def __init__(self, termination_str="TERMINATE", model_name="gpt-4o-mini"):
        self.financial_education_team = create_financial_education_team(termination_str=termination_str)
        self.portfolio_optimization_team = create_portfolio_optimization_flow(termination_str=termination_str)
        self.market_research_team = create_market_research_team(termination_str=termination_str, model_name=model_name)
        self.termination_str = termination_str
        # Dedicated model client for infra agents (router, aggregator)
        self.model_client = OpenAIChatCompletionClient(
            model=model_name
        )
        self.logger = logging.getLogger("MasterOrchestrator")

    def _intent_router(self, query: str):
        print(f"[Orchestrator] Routing intent for query: {query}")
        q = query.lower()
        # Only severe market events trigger research+optimization
        crisis_words = ["crisis", "volatility", "real-time", "web"]
        portfolio_words = ["optimize", "rebalance", "portfolio", "allocation", "returns", "risk"]
        education_words = ["educate", "learn", "explain", "teach", "education", "beginner"]
        # Complex: market crisis response (must check first)
        if any(word in q for word in crisis_words) and any(word in q for word in portfolio_words):
            print("[Orchestrator] Intent detected: research+optimization")
            return "research+optimization"
        # Complex: investment decision with education
        if (any(word in q for word in education_words) and any(word in q for word in portfolio_words)) or \
           ("should i invest" in q or ("invest" in q and "know" in q)):
            print("[Orchestrator] Intent detected: education+optimization")
            return "education+optimization"
        # Education/learning
        if any(word in q for word in education_words):
            print("[Orchestrator] Intent detected: education")
            return "education"
        # Portfolio optimization
        if any(word in q for word in portfolio_words):
            print("[Orchestrator] Intent detected: optimization")
            return "optimization"
        # Market research/news
        if any(word in q for word in crisis_words) or "research" in q:
            print("[Orchestrator] Intent detected: research")
            return "research"
        # Default
        print("[Orchestrator] Intent detected: optimization (default)")
        return "optimization"

    async def run_stream(self, task: str):
        print(f"[Orchestrator] Received task: {task}")
        intent = self._intent_router(task)
        flow = self._get_flow(intent)
        print(f"[Orchestrator] Running flow for intent: {intent}")
        # Use Console to stream output for the flow
        result = await  Console(flow.run_stream(task=task))
        print(f"[Orchestrator] Flow for intent '{intent}' completed.")
        return result


    # --- Team function wrappers for GraphFlow ---
    async def run_education(self, task: str):
        """
        Provides educational explanations and learning resources for financial topics and user questions.
        """
        print("[Orchestrator] Invoking Financial Education Team...")
        stream = self.financial_education_team.run_stream(task=task)
        task_result = await Console(stream)
        # Return the last message from the TaskResult object's messages list
        return task_result.messages[-1] if task_result and hasattr(task_result, 'messages') and task_result.messages else None

    async def run_optimization(self, task: str):
        """
        Analyzes and optimizes user portfolios, suggesting allocations and improvements for better returns and risk management.
        """
        print("[Orchestrator] Invoking Portfolio Optimization Team...")
        stream = self.portfolio_optimization_team.run_stream(task=task)
        task_result = await Console(stream)
        return task_result.messages[-1] if task_result and hasattr(task_result, 'messages') and task_result.messages else None

    async def run_research(self, task: str):
        """
        Performs market research, analyzes news and trends, and provides crisis or volatility insights for user queries.
        """
        print("[Orchestrator] Invoking Market Research Team...")
        stream = self.market_research_team.run_stream(task=task)
        task_result = await Console(stream)
        return task_result.messages[-1] if task_result and hasattr(task_result, 'messages') and task_result.messages else None

    def _build_agents(self):
        """Create AssistantAgents for each team function."""
        from autogen_agentchat.agents import AssistantAgent
        client = self.model_client
        education_agent = AssistantAgent(
            "education_agent",
            model_client=client,
            system_message="""
Provide financial education and explanations for user queries. When you have completed your task, include 'EDUCATION_DONE' in your final response.
""",
            tools=[self.run_education],
            reflect_on_tool_use=True
        )
        optimization_agent = AssistantAgent(
            "optimization_agent",
            model_client=client,
            system_message="""
Optimize user portfolios and provide allocation advice. When you have completed your task, include 'OPTIMIZATION_DONE' in your final response.
""",
            tools=[self.run_optimization],
            reflect_on_tool_use=True
        )
        research_agent = AssistantAgent(
            "research_agent",
            model_client=client,
            system_message="""
Provide market research, news, and crisis analysis. When you have completed your task, include 'RESEARCH_DONE' in your final response.
""",
            tools=[self.run_research],
            reflect_on_tool_use=True
        )
        return education_agent, optimization_agent, research_agent

    def _build_flows(self):
        """Build GraphFlow objects for each use case."""
        from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
        education_agent, optimization_agent, research_agent = self._build_agents()
        flows = {}
        # Single team flows
        builder = DiGraphBuilder()
        builder.add_node(education_agent)
        flows["education"] = GraphFlow(
            participants=builder.get_participants(),
            graph=builder.build(),
            termination_condition=TextMentionTermination("EDUCATION_DONE")
        )
        builder = DiGraphBuilder()
        builder.add_node(optimization_agent)
        flows["optimization"] = GraphFlow(
            participants=builder.get_participants(),
            graph=builder.build(),
            termination_condition=TextMentionTermination("OPTIMIZATION_DONE")
        )
        builder = DiGraphBuilder()
        builder.add_node(research_agent)
        flows["research"] = GraphFlow(
            participants=builder.get_participants(),
            graph=builder.build(),
            termination_condition=TextMentionTermination("RESEARCH_DONE")
        )
        # Sequential: education → optimization
        builder = DiGraphBuilder()
        builder.add_node(education_agent).add_node(optimization_agent)
        builder.add_edge(education_agent, optimization_agent)
        # Terminate only when optimization_agent signals done
        flows["education+optimization"] = GraphFlow(
            participants=builder.get_participants(),
            graph=builder.build(),
            termination_condition=TextMentionTermination("OPTIMIZATION_DONE")
        )
        # Parallel: research & optimization, then aggregate (fan-out from start node)
        builder = DiGraphBuilder()
        # Start node that simply passes the user input to both agents
        start_agent = AssistantAgent(
            "start_agent",
            model_client=self.model_client,
            system_message="Receive the user query and forward it to both research and optimization agents."
        )
        aggregator_termination = "AGGREGATOR_DONE"
        aggregator = AssistantAgent(
            "aggregator",
            model_client=self.model_client,
            system_message=(
                "Aggregate and synthesize the outputs from research and optimization agents into a comprehensive response. "
                f"When you have completed aggregation, include '{aggregator_termination}' in your final response."
            )
        )
        builder.add_node(start_agent).add_node(research_agent).add_node(optimization_agent).add_node(aggregator)
        builder.add_edge(start_agent, research_agent)
        builder.add_edge(start_agent, optimization_agent)
        builder.add_edge(research_agent, aggregator)
        builder.add_edge(optimization_agent, aggregator)
        builder.set_entry_point(start_agent)
        flows["research+optimization"] = GraphFlow(
            participants=builder.get_participants(),
            graph=builder.build(),
            termination_condition=TextMentionTermination(aggregator_termination)
        )
        self._flows = flows

    def _get_flow(self, intent):
        if not hasattr(self, '_flows'):
            self._build_flows()
        return self._flows.get(intent, self._flows["optimization"])

def _get_demo_tasks():
    return [
        # Triggers: optimization (portfolio-specific, needs email)
       # "Given the current tech sector trends, how should I rebalance my portfolio to maximize returns while maintaining moderate risk for user admin@example.com?",
        # Triggers: education+optimization (investment decision with education)
        "Should I invest in healthcare AI companies, and what should I know before investing?",
        # Triggers: research+optimization (market crisis + portfolio)
      #  "The tech sector is experiencing high volatility. How should I protect my portfolio and identify opportunities for user user@example.com?",
        # Triggers: education (pure education)
       # "Explain the basics of portfolio diversification for a beginner.",
        # Triggers: research (market research/news)
       # "What are the latest news and trends in the financial services sector?"
    ]

async def run_master_orchestrator_demo():
    from dotenv import load_dotenv
    from autogen_agentchat.ui import Console
    load_dotenv()
    print("\n" + "="*50)
    print("Master Orchestrator Demo (GraphFlow)")
    print("="*50)
    orchestrator = MasterOrchestrator()
    tasks = _get_demo_tasks()
    for i, task in enumerate(tasks, 1):
        print(f"\nTask {i}: {task}")
        print("-" * 50)
        await orchestrator.run_stream(task=task)
       # await Console(stream)
        if i < len(tasks):
            input("\nPress Enter to continue to the next task...")
    print("\nDemo completed!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_master_orchestrator_demo())
