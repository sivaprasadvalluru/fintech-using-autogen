"""
Financial Education Flow

This module provides a function to create a financial education team as a RoundRobinGroupChat.
It combines Financial Educator and Market Analyst agents for sequential educational content and context.
"""

from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from fintech_autogen.agents import get_financial_educator_agent, get_market_analyst_agent

def create_financial_education_team(termination_str=None) -> SelectorGroupChat:
    """
    Create a SelectorGroupChat for financial education with educator and analyst agents.
    Optionally override the analyst's termination string.
    Returns a SelectorGroupChat instance ready for streaming.
    """
    educator_termination = "EDUCATOR_DONE"
    analyst_termination = termination_str if termination_str is not None else "ANALYST_DONE"
    educator = get_financial_educator_agent(
        system_message=(
            "You are a Financial Educator Agent responsible for providing financial education, "
            "retrieving knowledge from ChromaDB, and creating personalized learning paths.\n\n"
            "Your capabilities include:\n"
            "1. Explaining financial concepts in simple terms\n"
            "2. Retrieving and summarizing knowledge from the knowledge base\n"
            "3. Creating step-by-step learning paths for users\n"
            "4. Providing investment and risk management guidelines\n"
            "5. Answering user questions with clear, educational context\n\n"
            "Always be clear, concise, and supportive in your explanations.\n"
            f"When you have completed the educational task, include '{educator_termination}' in your final response."
        )
    )
    analyst = get_market_analyst_agent(
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
    # --- You can switch between SelectorGroupChat and RoundRobinGroupChat as needed ---
    # To use RoundRobinGroupChat, uncomment the following lines and comment out the SelectorGroupChat block below:
    # from autogen_agentchat.teams import RoundRobinGroupChat
    # return RoundRobinGroupChat(
    #     [educator, analyst],
    #     termination_condition=TextMentionTermination(analyst_termination)
    # )

    # Custom selector prompt: Let the educator speak until they signal completion, then let the analyst speak until they finish.
    selector_prompt = (
        "If the educator has not yet included 'EDUCATOR_DONE' in their response, select the educator. "
        "Once the educator is done, select the analyst until 'ANALYST_DONE' is included in their response."
    )
    return SelectorGroupChat(
        [educator, analyst],
        selector_prompt=selector_prompt
    )

def _get_demo_tasks():
    return [
        # General finance + market context
        "Explain what a stock and a bond are, then analyze how recent market trends have affected both asset classes.",
        # Investment strategies + sector analysis
        "Describe the concept of diversification and demonstrate how it applies to building a portfolio in the technology sector today.",
        # Risk management + sector context
        "Teach the basics of risk management in investing, and provide a current risk assessment for the healthcare sector.",
        # ESG and thematic investing
        "What is ESG investing? Summarize the latest trends and market sentiment around ESG-focused funds.",
        # Market analysis patterns + practical example
        "Explain what technical and fundamental analysis are, then apply them to a recent example from the financial services sector."
    ]

async def run_financial_education_team_demo():
    from dotenv import load_dotenv
    from autogen_agentchat.ui import Console
    load_dotenv()
    print("\n" + "="*50)
    print("Financial Education Team Demo")
    print("="*50)
    team = create_financial_education_team()
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
    asyncio.run(run_financial_education_team_demo())
