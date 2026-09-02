from typing import List
from travelops.llm.factory import LLMFactory
from travelops.models import (
    Itinerary, ItineraryDay, ItineraryItem, 
    AgentResult, FlightOption, HotelOption, ActivityOption
)
from travelops.tools.geography import estimate_travel_time

class ItineraryAgent:
    def __init__(self):
        self.llm = LLMFactory.get_llm()

    def run(self, 
             flight: FlightOption, 
             hotel: HotelOption, 
             activities: List[ActivityOption], 
             duration_days: int) -> Itinerary:
        
        # In Phase 1, we implement a deterministic logic for itinerary synthesis
        # to ensure the mock mode works perfectly.
        
        days = []
        for d in range(1, duration_days + 1):
            items = []
            # Simple distribution of activities across days
            act_idx = (d - 1) % len(activities) if activities else 0
            activity = activities[act_idx] if activities else None
            
            if activity:
                items.append(ItineraryItem(
                    date=f"Day {d}",
                    time_period="Morning",
                    activity=activity.name,
                    location=activity.neighborhood,
                    estimated_duration=f"{activity.duration_hours}h",
                    estimated_cost=activity.estimated_cost,
                    transportation_estimate=10.0,
                    reason="Matches user preferences"
                ))
                
                items.append(ItineraryItem(
                    date=f"Day {d}",
                    time_period="Afternoon",
                    activity="Local Exploration",
                    location=hotel.neighborhood if hotel else "City Center",
                    estimated_duration="3h",
                    estimated_cost=20.0,
                    transportation_estimate=5.0,
                    reason="Proximity to hotel" if hotel else "General exploration"
                ))
            
            days.append(ItineraryDay(
                day_number=d,
                date=f"Day {d}",
                items=items
            ))
            
        return Itinerary(days=days)
