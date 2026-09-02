from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, END
from datetime import datetime

from travelops.state import TravelState
from travelops.models import (
    ExecutionEvent, AgentStatus, TravelPlan
)
from travelops.agents.supervisor import TravelSupervisor
from travelops.agents.flight_agent import FlightAgent
from travelops.agents.hotel_agent import HotelAgent
from travelops.agents.activities_agent import ActivitiesAgent
from travelops.agents.itinerary_agent import ItineraryAgent
from travelops.agents.budget_agent import BudgetAgent
from travelops.agents.critic_agent import CriticAgent

class TravelGraph:
    def __init__(self):
        self.supervisor = TravelSupervisor()
        self.flight_agent = FlightAgent()
        self.hotel_agent = HotelAgent()
        self.activities_agent = ActivitiesAgent()
        self.itinerary_agent = ItineraryAgent()
        self.budget_agent = BudgetAgent()
        self.critic_agent = CriticAgent()
        
        self.workflow = self._build_graph()

    def _log_event(self, state: TravelState, agent: str, node: str, event_type: str, summary: str):
        event = ExecutionEvent(
            timestamp=datetime.now().isoformat(),
            agent=agent,
            node=node,
            event_type=event_type,
            summary=summary,
            iteration=state.get("iteration_count", 0)
        )
        return {"execution_trace": [event]}

    # --- Nodes ---

    def node_parse_request(self, state: TravelState):
        request = self.supervisor.parse_request(state["trip_request"].raw_text)
        return {
            "trip_request": request,
            "iteration_count": 0,
            "max_iterations": 3,
            "execution_trace": [ExecutionEvent(
                timestamp=datetime.now().isoformat(),
                agent="supervisor",
                node="parse_request",
                event_type="parsing",
                summary="Parsed trip request",
                iteration=0
            )]
        }

    def node_flight_agent(self, state: TravelState):
        req = state["trip_request"]
        res = self.flight_agent.run(req.origin or "SFO", req.destination or "Japan", req.budget or 6000.0)
        
        # Extract selected flight
        selected = None
        if res.recommendations:
            # In Phase 1, we'll just use the first rec
            # A real implementation would use the repo to get the actual FlightOption
            # For now, we'll mock it as the first flight from the repo
            from travelops.repositories.flights import FlightRepository
            selected = FlightRepository().get_by_id(res.recommendations[0].option_id)
            
        return {
            "flight_results": [res],
            "selected_flight": selected,
            "agent_results": [res],
            **self._log_event(state, "flight_agent", "node_flight_agent", "execution", "Searched and selected flight")
        }

    def node_hotel_agent(self, state: TravelState):
        req = state["trip_request"]
        res = self.hotel_agent.run(req.destination or "Tokyo", (req.budget or 6000.0) / 10)
        
        selected = None
        if res.recommendations:
            from travelops.repositories.hotels import HotelRepository
            selected = HotelRepository().get_by_id(res.recommendations[0].option_id)
            
        return {
            "hotel_results": [res],
            "selected_hotel": selected,
            "agent_results": [res],
            **self._log_event(state, "hotel_agent", "node_hotel_agent", "execution", "Searched and selected hotel")
        }

    def node_activities_agent(self, state: TravelState):
        req = state["trip_request"]
        res = self.activities_agent.run(req.destination or "Tokyo", req.preferences)
        
        selected = []
        if res.findings:
            # Extract activities from finding details
            details = res.findings[0].details.get("activities", [])
            # Convert dicts back to ActivityOption
            from travelops.models import ActivityOption
            selected = [ActivityOption(**a) for a in details]
            
        return {
            "activity_results": [res],
            "selected_activities": selected,
            "agent_results": [res],
            **self._log_event(state, "activities_agent", "node_activities_agent", "execution", "Searched and selected activities")
        }

    def node_itinerary_agent(self, state: TravelState):
        itinerary = self.itinerary_agent.run(
            state["selected_flight"],
            state["selected_hotel"],
            state["selected_activities"],
            state["trip_request"].duration_days or 7
        )
        return {
            "itinerary": itinerary,
            **self._log_event(state, "itinerary_agent", "node_itinerary_agent", "execution", "Generated itinerary")
        }

    def node_budget_agent(self, state: TravelState):
        flight_cost = state["selected_flight"].price if state["selected_flight"] else 0.0
        hotel_cost = (state["selected_hotel"].price_per_night * 7) if state["selected_hotel"] else 0.0
        activities_cost = sum(a.estimated_cost for a in state["selected_activities"])
        
        analysis = self.budget_agent.run(
            flight_cost, hotel_cost, activities_cost, state["trip_request"].budget or 6000.0
        )
        return {
            "budget_analysis": analysis,
            **self._log_event(state, "budget_agent", "node_budget_agent", "execution", "Analyzed budget")
        }

    def node_critic_agent(self, state: TravelState):
        critique = self.critic_agent.run(state["itinerary"], state["budget_analysis"])
        return {
            "critique": critique,
            **self._log_event(state, "critic_agent", "node_critic_agent", "execution", "Critiqued plan")
        }

    def node_finalize(self, state: TravelState):
        # Construct final TravelPlan
        plan = TravelPlan(
            summary="Customized travel plan for " + state["trip_request"].destination,
            destination=state["trip_request"].destination,
            duration_days=state["trip_request"].duration_days,
            travelers=state["trip_request"].travelers,
            budget_limit=state["trip_request"].budget,
            estimated_total=state["budget_analysis"].total_cost,
            selected_flight=state["selected_flight"],
            selected_hotel=state["selected_hotel"],
            itinerary=state["itinerary"],
            budget_analysis=state["budget_analysis"],
            quality_check=state["critique"]
        )
        return {
            "final_plan": plan,
            **self._log_event(state, "supervisor", "node_finalize", "finalization", "Final plan generated")
        }

    # --- Routing ---

    def route_after_critic(self, state: TravelState) -> Literal["finalize", "rework"]:
        if state["critique"] and state["critique"].approved:
            return "finalize"
        
        # Increment iteration count for rework
        # Note: In a real LangGraph node we'd do this in a node, but for routing logic
        # we just check the current count.
        if state.get("iteration_count", 0) >= state.get("max_iterations", 3):
            return "finalize"
            
        return "rework"

    def node_rework_orchestrator(self, state: TravelState):
        # This node handles the increment of iterations and determines which agents to rerun
        # For the MVP, we'll simply increment and let the edges handle routing.
        new_count = state.get("iteration_count", 0) + 1
        
        # Log rework
        log = self._log_event(state, "supervisor", "node_rework_orchestrator", "rework", f"Starting iteration {new_count}")
        
        return {
            "iteration_count": new_count,
            **log
        }

    def _build_graph(self):
        builder = StateGraph(TravelState)
        
        builder.add_node("parse_request", self.node_parse_request)
        builder.add_node("flight_agent", self.node_flight_agent)
        builder.add_node("hotel_agent", self.node_hotel_agent)
        builder.add_node("activities_agent", self.node_activities_agent)
        builder.add_node("itinerary_agent", self.node_itinerary_agent)
        builder.add_node("budget_agent", self.node_budget_agent)
        builder.add_node("critic_agent", self.node_critic_agent)
        builder.add_node("rework_orchestrator", self.node_rework_orchestrator)
        builder.add_node("finalize", self.node_finalize)
        
        builder.set_entry_point("parse_request")
        
        # Parallel Specialists
        builder.add_edge("parse_request", "flight_agent")
        builder.add_edge("parse_request", "hotel_agent")
        builder.add_edge("parse_request", "activities_agent")
        
        # Join Specialists -> Itinerary
        builder.add_edge("flight_agent", "itinerary_agent")
        builder.add_edge("hotel_agent", "itinerary_agent")
        builder.add_edge("activities_agent", "itinerary_agent")
        
        builder.add_edge("itinerary_agent", "budget_agent")
        builder.add_edge("budget_agent", "critic_agent")
        
        builder.add_conditional_edges(
            "critic_agent",
            self.route_after_critic,
            {
                "finalize": "finalize",
                "rework": "rework_orchestrator"
            }
        )
        
        # From orchestrator, we rerun all specialists for the MVP
        builder.add_edge("rework_orchestrator", "flight_agent")
        builder.add_edge("rework_orchestrator", "hotel_agent")
        builder.add_edge("rework_orchestrator", "activities_agent")
        
        builder.add_edge("finalize", END)
        
        return builder.compile()
