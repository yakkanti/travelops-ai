from typing import List
from travelops.llm.factory import LLMFactory
from travelops.models import Critique, CritiqueIssue, Severity, Itinerary, BudgetAnalysis

class CriticAgent:
    def __init__(self):
        self.llm = LLMFactory.get_llm()

    def run(self, itinerary: Itinerary, budget: BudgetAnalysis) -> Critique:
        issues = []
        
        # 1. Budget check
        if budget.is_over_budget:
            issues.append(CritiqueIssue(
                issue_id="CRIT-001",
                severity=Severity.CRITICAL,
                description=f"Trip is over budget by {abs(budget.remaining)}",
                affected_component="Budget",
                recommended_agent="budget_agent",
                recommended_action="Reduce costs in flights or hotels"
            ))
            
        # 2. Schedule density check
        for day in itinerary.days:
            if len(day.items) > 5:
                issues.append(CritiqueIssue(
                    issue_id="CRIT-002",
                    severity=Severity.MEDIUM,
                    description=f"Day {day.day_number} is too crowded",
                    affected_component="Itinerary",
                    recommended_agent="itinerary_agent",
                    recommended_action="Remove some activities"
                ))
        
        approved = len(issues) == 0
        summary = "Plan looks good" if approved else f"Found {len(issues)} issues"
        
        return Critique(
            approved=approved,
            issues=issues,
            summary=summary
        )
