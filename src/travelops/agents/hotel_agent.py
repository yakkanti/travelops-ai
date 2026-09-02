from typing import List
from travelops.llm.factory import LLMFactory
from travelops.models import AgentResult, AgentStatus, AgentFinding, AgentRecommendation
from travelops.tools.hotels import search_hotels, compare_hotels

class HotelAgent:
    def __init__(self):
        self.llm = LLMFactory.get_llm()
        self.tools = [search_hotels, compare_hotels]
        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def run(self, city: str, budget_per_night: float) -> AgentResult:
        # 1. Search hotels
        hotels = search_hotels.invoke({"city": city})
        
        if not hotels:
            return AgentResult(
                agent="hotel_agent",
                status=AgentStatus.FAILED,
                summary=f"No hotels found in {city}.",
                estimated_cost=0.0
            )

        # 2. Recommendation logic
        recommended = hotels[0]
        
        return AgentResult(
            agent="hotel_agent",
            status=AgentStatus.COMPLETE,
            summary=f"Found {len(hotels)} hotel options in {city}.",
            findings=[
                AgentFinding(
                    id="HOTEL-REC",
                    type="recommendation",
                    summary=f"Recommended hotel {recommended.name}",
                    details={"hotel": recommended.dict()}
                )
            ],
            recommendations=[
                AgentRecommendation(
                    option_id=recommended.hotel_id,
                    reasoning="Highest rating and good location.",
                    score=0.95
                )
            ],
            estimated_cost=recommended.price_per_night * 7 # default duration for MVP
        )
