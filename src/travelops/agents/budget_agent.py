from typing import List
from travelops.llm.factory import LLMFactory
from travelops.models import BudgetAnalysis, AgentResult, AgentStatus

class BudgetAgent:
    def __init__(self):
        self.llm = LLMFactory.get_llm()

    def run(self, 
             flight_cost: float, 
             hotel_cost: float, 
             activities_cost: float, 
             budget_limit: float) -> BudgetAnalysis:
        
        food_estimate = 50.0 * 7 * 2 # $50/day * 7 days * 2 people
        transport_estimate = 20.0 * 7 * 2
        
        total = flight_cost + hotel_cost + activities_cost + food_estimate + transport_estimate
        remaining = budget_limit - total
        is_over = total > budget_limit
        
        causes = []
        rework = []
        if is_over:
            if flight_cost > budget_limit * 0.4:
                causes.append("Flights are too expensive")
                rework.append("flight_agent")
            if hotel_cost > budget_limit * 0.3:
                causes.append("Hotel is too expensive")
                rework.append("hotel_agent")
            if activities_cost > budget_limit * 0.2:
                causes.append("Activities are too expensive")
                rework.append("activities_agent")
                
        return BudgetAnalysis(
            flights_cost=flight_cost,
            hotels_cost=hotel_cost,
            activities_cost=activities_cost,
            food_estimate=food_estimate,
            transportation_estimate=transport_estimate,
            total_cost=total,
            budget_limit=budget_limit,
            remaining=remaining,
            is_over_budget=is_over,
            primary_causes=causes,
            recommended_rework_agents=rework
        )
