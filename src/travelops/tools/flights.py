from langchain.tools import tool
from travelops.repositories.flights import FlightRepository

flight_repo = FlightRepository()

@tool
def search_flights(origin: str, destination: str):
    """
    Search for available flights between two cities.
    Args:
        origin: The departure city code (e.g., 'SFO').
        destination: The destination city code (e.g., 'HND').
    """
    return flight_repo.search_flights(origin, destination)

@tool
def compare_flights(flight_ids: list[str]):
    """
    Compare a set of flights based on price, duration, and stops.
    Args:
        flight_ids: List of flight IDs to compare.
    """
    results = [flight_repo.get_by_id(fid) for fid in flight_ids]
    return results
