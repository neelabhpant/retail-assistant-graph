# crew/crew_setup.py
from crewai import Crew, Process
from crew.agents import RetailAgents
from crew.tasks import RetailTasks

# Instantiate the agents and tasks
agents = RetailAgents()
tasks = RetailTasks()

# Instantiate the specific agents
query_router = agents.query_router_agent()
retail_assistant = agents.retail_assistant_agent()
summarizer = agents.summarizer_agent()

class RetailCrew:
    def __init__(self, query: str):
        self.query = query

    def run(self):
        # Define the tasks with the specific agents
        route_query = tasks.route_query_task(query_router, self.query)
        inquiry = tasks.retail_inquiry_task(retail_assistant)
        summary = tasks.summarize_response_task(summarizer)

        # Define the crew
        crew = Crew(
            agents=[query_router, retail_assistant, summarizer],
            tasks=[route_query, inquiry, summary],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result