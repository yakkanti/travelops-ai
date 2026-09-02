from langchain.tools import tool
from travelops.repositories.activities import ActivityRepository

activity_repo = ActivityRepository()

@tool
def search_activities(city: str, categories: list[str] = None):
    """
    Search for activities in a city, optionally filtered by categories.
    Args:
        city: The city to search for activities in.
        categories: Optional list of categories (e.g., ['food', 'culture']).
    """
    return activity_repo.search_activities(city, categories)

@tool
def filter_activities(activity_ids: list[str], min_rating: float = 0.0):
    """
    Filter a list of activities based on a minimum rating.
    Args:
        activity_ids: List of activity IDs to filter.
        min_rating: Minimum rating threshold.
    """
    results = [activity_repo.get_by_id(aid) for aid in activity_ids]
    return [a for a in results if a and a.rating >= min_rating]
