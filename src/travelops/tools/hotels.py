from langchain.tools import tool
from travelops.repositories.hotels import HotelRepository

hotel_repo = HotelRepository()

@tool
def search_hotels(city: str):
    """
    Search for hotels in a specific city.
    Args:
        city: The city to search for hotels in.
    """
    return hotel_repo.search_hotels(city)

@tool
def compare_hotels(hotel_ids: list[str]):
    """
    Compare a set of hotels based on price, rating, and amenities.
    Args:
        hotel_ids: List of hotel IDs to compare.
    """
    results = [hotel_repo.get_by_id(hid) for hid in hotel_ids]
    return results
