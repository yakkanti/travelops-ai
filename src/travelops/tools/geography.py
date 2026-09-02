from langchain.tools import tool

@tool
def estimate_travel_time(origin_zone: str, destination_zone: str):
    """
    Estimate travel time between two zones in a city.
    Args:
        origin_zone: Starting neighborhood or zone.
        destination_zone: Ending neighborhood or zone.
    """
    if origin_zone.lower() == destination_zone.lower():
        return "Short (15-30 mins)"
    
    # Simplified logic for Phase 1
    return "Medium (30-60 mins)"
