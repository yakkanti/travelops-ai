import argparse
import sys
import json
from travelops.graph import TravelGraph
from travelops.models import TripRequest

def main():
    parser = argparse.ArgumentParser(description="TravelOps AI CLI")
    parser.add_argument("command", choices=["plan"], help="Command to run")
    parser.add_argument("request", help="Trip request text")
    parser.add_argument("--mock", action="store_true", help="Run in mock mode")
    
    args = parser.parse_args()
    
    if args.command == "plan":
        # Set environment variable for mock mode
        import os
        if args.mock:
            os.environ["LLM_PROVIDER"] = "mock"
            
        graph_executor = TravelGraph()
        app = graph_executor.workflow
        
        initial_state = {
            "trip_request": TripRequest(raw_text=args.request),
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
        
        print("\n--- ✈️  TravelOps AI is planning your trip... ---\n")
        
        final_state = app.invoke(initial_state)
        
        plan = final_state.get("final_plan")
        trace = final_state.get("execution_trace", [])
        
        print("==== EXECUTION TRACE ====")
        for event in trace:
            print(f"[{event.timestamp}] {event.agent} @ {event.node}: {event.summary}")
        
        print("\n==== FINAL TRAVEL PLAN ====")
        if plan:
            print(f"Destination: {plan.destination}")
            print(f"Duration: {plan.duration_days} days")
            print(f"Budget: {plan.budget_limit} USD")
            print(f"Estimated Total: {plan.estimated_total} USD")
            print("\n--- Flights ---")
            if plan.selected_flight:
                print(f"Recommended: {plan.selected_flight.airline} - {plan.selected_flight.price} USD")
            else:
                print("No flight recommended.")
                
            print("\n--- Hotel ---")
            if plan.selected_hotel:
                print(f"Recommended: {plan.selected_hotel.name} - {plan.selected_hotel.price_per_night}/night")
            else:
                print("No hotel recommended.")
            print("\n--- Itinerary ---")
            for day in plan.itinerary.days:
                print(f"\nDay {day.day_number}:")
                for item in day.items:
                    print(f"  - {item.time_period}: {item.activity} ({item.location})")
            
            print("\n--- Budget Analysis ---")
            print(f"Total: {plan.budget_analysis.total_cost} USD")
            print(f"Remaining: {plan.budget_analysis.remaining} USD")
            print(f"Over Budget: {plan.budget_analysis.is_over_budget}")
            
            print("\n--- Quality Check ---")
            print(f"Approved: {plan.quality_check.approved}")
            print(f"Summary: {plan.quality_check.summary}")
        else:
            print("Failed to generate a final plan.")

if __name__ == "__main__":
    main()
