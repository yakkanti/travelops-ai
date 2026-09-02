from typing import List
from travelops.llm.factory import LLMFactory
from travelops.models import AgentResult, AgentStatus, AgentFinding, AgentRecommendation
from travelops.tools.activities import search_activities, filter_activities

class ActivitiesAgent:
    def __init__(self):
        self.llm = LLMFactory.get_llm()
        self.tools = [search_activities, filter_activities]
        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def run(self, city: str, preferences: List[str]) -> AgentResult:
        # 1. Search activities
        # Map preferences to categories (simple mapping for MVP)
        categories = []
        if "food" in preferences: categories.append("food")
        if "hiking" in preferences: categories.append("hiking")
        if "culture" in preferences: categories.append("culture")
        
        activities = search_activities.invoke({"city": city, "categories": categories})
        
        if not activities:
            # Fallback search without category filters
            activities = search_activities.invoke({"city": city})

        if not activities:
            return AgentResult(
                agent="activities_agent",
                status=AgentStatus.FAILED,
                summary=f"No activities found in {city}.",
                estimated_cost=0.0
            )

        # 2. Selection
        recommended_ids = [a.activity_id for a in activities[:5]]
        
        total_cost = sum(a.estimated_cost for a in activities[:5])
        
        return AgentResult(
            agent="activities_agent",
            status=AgentStatus.COMPLETE,
            summary=f"Found {len(activities)} activities. Recommended top 5.",
            findings=[
                AgentFinding(
                    id="ACT-REC",
                    type="recommendation",
                    summary=f"Selected {len(recommended_ids)} activities based on preferences.",
                    details={"activities": [a.dict() for a in activities[:5]]}
                )
            ],
            recommendations=[
                AgentRecommendation(
                    option_id="MULTI-ACT",
                    reasoning="Top rated activities matching user interests.",
                    score=0.85
                )
            ],
            estimated_cost=total_cost
        )
