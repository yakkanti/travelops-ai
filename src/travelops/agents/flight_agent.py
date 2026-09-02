from typing import List
from travelops.llm.factory import LLMFactory
from travelops.models import AgentResult, AgentStatus, AgentFinding, AgentRecommendation
from travelops.tools.flights import search_flights, compare_flights

class FlightAgent:
    def __init__(self):
        self.llm = LLMFactory.get_llm()
        self.tools = [search_flights, compare_flights]
        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def run(self, origin: str, destination: str, budget: float) -> AgentResult:
        # Simplified logic for Phase 1 specialist agents
        # In a full implementation, this would be a LangGraph sub-graph or a chain
        
        # 1. Search flights
        flights = search_flights.invoke({"origin": origin, "destination": destination})
        
        if not flights:
            return AgentResult(
                agent="flight_agent",
                status=AgentStatus.FAILED,
                summary="No flights found for the given route.",
                estimated_cost=0.0
            )

        # 2. Determine recommendation (simple logic for MVP)
        # Usually, we'd use LLM to pick based on tradeoffs
        recommended = flights[0]
        
        return AgentResult(
            agent="flight_agent",
            status=AgentStatus.COMPLETE,
            summary=f"Found {len(flights)} flight options. Recommended {recommended.airline}.",
            findings=[
                AgentFinding(
                    id="FLIGHT-REC",
                    type="recommendation",
                    summary=f"Recommended flight {recommended.flight_id} via {recommended.airline}",
                    details={"flight": recommended.dict()}
                )
            ],
            recommendations=[
                AgentRecommendation(
                    option_id=recommended.flight_id,
                    reasoning="Best balance of price and duration.",
                    score=0.9
                )
            ],
            estimated_cost=recommended.price
        )
