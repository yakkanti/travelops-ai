import json
import pytest
from travelops.graph import TravelGraph
from travelops.models import TripRequest

def load_cases():
    with open("eval/cases.json", "r") as f:
        return json.load(f)

@pytest.mark.parametrize("case", load_cases())
def test_evaluation_case(case):
    graph_executor = TravelGraph()
    app = graph_executor.workflow
    
    initial_state = {
        "trip_request": TripRequest(raw_text=case["request"]),
        "assumptions": [],
        "flight_results": [],
        "hotel_results": [],
        "activity_results": [],
        "selected_flight": None,
        "selected_hotel": None,
        "selected_activities": [],
        "itinerary": None,
        "budget_analysis": None,
        "critique": None,
        "agent_results": [],
        "rework_requests": [],
        "iteration_count": 0,
        "max_iterations": 3,
        "final_plan": None,
        "execution_trace": []
    }
    
    final_state = app.invoke(initial_state)
    plan = final_state.get("final_plan")
    
    assert plan is not None
    assert plan.destination == case["expected"]["destination"]
    if case["expected"]["budget_max"]:
        assert plan.budget_limit == case["expected"]["budget_max"]
