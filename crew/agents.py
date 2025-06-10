# crew/agents.py
from crewai import Agent
from utils.llm_loader import llm
from tools.order_history_tool import OrderHistoryTool
from tools.return_item_tool import ReturnItemTool
from tools.faq_tool import FAQTool
from tools.product_search_tool import ProductSearchTool
from tools.recommendation_tool import RecommendationTool

class RetailAgents:
    def query_router_agent(self) -> Agent:
        return Agent(
            role="Query Router Agent",
            goal="Examine the user query, decompose it into distinct intents, and route them appropriately.",
            backstory="You are an expert at understanding user intent and structuring complex queries into clear, actionable steps.",
            llm=llm,
            verbose=True,
            allow_delegation=True
        )

    def retail_assistant_agent(self) -> Agent:
        return Agent(
            role="Retail Assistant Agent",
            goal="Your primary goal is to use the provided tools to find factual answers to user inquiries. "
                 "Analyze the user's request and select the single best tool to answer it. "
                 "You must provide only the direct, raw output from the tool.",
            backstory="You are a diligent and fact-based customer service representative. "
                      "You do not provide information from your own knowledge. "
                      "You follow a strict process: analyze the query, select the most direct tool, use it, and return the output.",
            llm=llm,
            verbose=True,
            tools=[
                OrderHistoryTool(),
                ReturnItemTool(),
                FAQTool(),
                ProductSearchTool(),
                RecommendationTool(),
            ],
        )

    def summarizer_agent(self) -> Agent:
        return Agent(
            role="Summarizer Agent",
            goal="Synthesize information from other agents into a single, cohesive, and friendly response.",
            backstory="You are a communications expert who crafts final, polished responses for the customer.",
            llm=llm,
            verbose=True,
        )