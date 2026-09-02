from __future__ import annotations
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --- Enums ---

class AgentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"
    NEEDS_REWORK = "needs_rework"

class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ActivityCategory(str, Enum):
    CULTURE = "culture"
    FOOD = "food"
    HIKING = "hiking"
    NATURE = "nature"
    MUSEUM = "museum"
    SHOPPING = "shopping"
    TOUR = "tour"
    NIGHTLIFE = "nightlife"
    FAMILY = "family"

# --- Request & Constraints ---

class TripRequest(BaseModel):
    raw_text: str
    destination: Optional[str] = None
    origin: Optional[str] = None
    duration_days: Optional[int] = None
    budget: Optional[float] = None
    travelers: Optional[int] = 1
    preferences: List[str] = Field(default_factory=list)
    start_date: Optional[str] = None

class TripConstraints(BaseModel):
    hard_constraints: List[str] = Field(default_factory=list)
    soft_preferences: List[str] = Field(default_factory=list)
    budget_limit: float
    time_frame: str

# --- Domain Options ---

class FlightOption(BaseModel):
    flight_id: str
    airline: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    return_departure_time: Optional[str] = None
    return_arrival_time: Optional[str] = None
    price: float
    currency: str = "USD"
    stops: int
    duration_hours: float
    tradeoffs: List[str] = Field(default_factory=list)

class HotelOption(BaseModel):
    hotel_id: str
    name: str
    city: str
    neighborhood: str
    price_per_night: float
    rating: float
    amenities: List[str] = Field(default_factory=list)
    check_in_time: str
    check_out_time: str

class ActivityOption(BaseModel):
    activity_id: str
    name: str
    city: str
    neighborhood: str
    category: ActivityCategory
    estimated_cost: float
    duration_hours: float
    opening_days: List[str] = Field(default_factory=list)
    opening_hours: str
    rating: float

# --- Itinerary ---

class ItineraryItem(BaseModel):
    date: str
    time_period: str  # e.g., "Morning", "Afternoon", "Evening"
    activity: str
    location: str
    estimated_duration: str
    estimated_cost: float
    transportation_estimate: float
    reason: str

class ItineraryDay(BaseModel):
    day_number: int
    date: str
    items: List[ItineraryItem]

class Itinerary(BaseModel):
    days: List[ItineraryDay]

# --- Analysis & Quality ---

class BudgetAnalysis(BaseModel):
    flights_cost: float
    hotels_cost: float
    activities_cost: float
    food_estimate: float
    transportation_estimate: float
    total_cost: float
    budget_limit: float
    remaining: float
    is_over_budget: bool
    primary_causes: List[str] = Field(default_factory=list)
    recommended_rework_agents: List[str] = Field(default_factory=list)

class CritiqueIssue(BaseModel):
    issue_id: str
    severity: Severity
    description: str
    affected_component: str
    recommended_agent: str
    recommended_action: str

class Critique(BaseModel):
    approved: bool
    issues: List[CritiqueIssue] = Field(default_factory=list)
    summary: str

# --- Agent Communication ---

class AgentFinding(BaseModel):
    id: str
    type: str # e.g., "recommendation", "constraint"
    summary: str
    details: Dict[str, Any]

class AgentRecommendation(BaseModel):
    option_id: str
    reasoning: str
    score: float

class AgentResult(BaseModel):
    agent: str
    status: AgentStatus
    summary: str
    findings: List[AgentFinding] = Field(default_factory=list)
    recommendations: List[AgentRecommendation] = Field(default_factory=list)
    constraints_discovered: List[str] = Field(default_factory=list)
    estimated_cost: float = 0.0

class ReworkRequest(BaseModel):
    agent: str
    reason: str
    required_changes: List[str]

class ExecutionEvent(BaseModel):
    timestamp: str
    agent: str
    node: str
    event_type: str
    summary: str
    iteration: int

# --- Final Plan ---

class TravelPlan(BaseModel):
    summary: str
    destination: str
    duration_days: int
    travelers: int
    budget_limit: float
    estimated_total: float
    selected_flight: Optional[FlightOption] = None
    selected_hotel: Optional[HotelOption] = None
    itinerary: Optional[Itinerary] = None
    budget_analysis: Optional[BudgetAnalysis] = None
    assumptions: List[str] = Field(default_factory=list)
    quality_check: Optional[Critique] = None
