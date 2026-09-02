from typing import TypedDict, List, Optional, Annotated
from operator import add
from travelops.models import (
    TripRequest, FlightOption, HotelOption, ActivityOption, 
    Itinerary, BudgetAnalysis, Critique, AgentResult, 
    ReworkRequest, ExecutionEvent, TravelPlan
)

class TravelState(TypedDict):
    trip_request: TripRequest
    assumptions: List[str]
    
    flight_results: List[AgentResult]
    hotel_results: List[AgentResult]
    activity_results: List[AgentResult]
    
    selected_flight: Optional[FlightOption]
    selected_hotel: Optional[HotelOption]
    selected_activities: List[ActivityOption]
    
    itinerary: Optional[Itinerary]
    budget_analysis: Optional[BudgetAnalysis]
    critique: Optional[Critique]
    
    agent_results: Annotated[List[AgentResult], add]
    rework_requests: Annotated[List[ReworkRequest], add]
    execution_trace: Annotated[List[ExecutionEvent], add]
    
    iteration_count: int
    max_iterations: int
    
    final_plan: Optional[TravelPlan]

