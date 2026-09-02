from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from travelops.graph import TravelGraph
from travelops.models import TripRequest

app = FastAPI(title="TravelOps AI API")
graph_executor = TravelGraph()

class PlanRequest(BaseModel):
    request: str

class PlanResponse(BaseModel):
    plan: Any
    trace: list
    iterations: int

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/plan")
async def plan_trip(req: PlanRequest):
    try:
        initial_state = {
            "trip_request": TripRequest(raw_text=req.request),
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
        
        final_state = graph_executor.workflow.invoke(initial_state)
        
        return {
            "plan": final_state.get("final_plan"),
            "trace": final_state.get("execution_trace", []),
            "iterations": final_state.get("iteration_count", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
