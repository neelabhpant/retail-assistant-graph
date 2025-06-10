# crew/tasks.py
from crewai import Task

class RetailTasks:
    def route_query_task(self, agent, query: str) -> Task:
        return Task(
            description=f"Analyze the user's query: '{query}'.\n"
                        "Identify all distinct intents and required information, like customer IDs or product names.",
            expected_output="A clear summary of the user's intents. For example: "
                            "'The user C001 wants to see their order history and also wants to know the return policy.'",
            agent=agent,
        )

    def retail_inquiry_task(self, agent) -> Task:
        return Task(
            description="Based on the routed query, use your available tools to find the necessary information from the graph database.",
            expected_output="The specific, raw information retrieved from your tools. This could be order details, a return confirmation, "
                            "a list of products, or an answer from the FAQs.",
            agent=agent,
        )

    def summarize_response_task(self, agent) -> Task:
            return Task(
                # This is the original description
                description="Review the user's query and the factual results from the Retail Assistant Agent. "
                            "Synthesize this information into a single, cohesive, and friendly response. "
                            "Your final answer MUST be only the customer-facing response, without any of your own internal thoughts, "
                            "notes, or prefixes like 'Final Answer:'. Just provide the clean text ready to be shown to the customer.",
                
                expected_output="A final, well-formatted, and conversational response to the user that addresses all parts of their original query.",
                agent=agent,
            )