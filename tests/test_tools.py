import pytest
from travelops.tools.flights import search_flights, compare_flights
from travelops.tools.hotels import search_hotels, compare_hotels
from travelops.tools.activities import search_activities, filter_activities
from travelops.tools.geography import estimate_travel_time

def test_flight_tools():
    res = search_flights.invoke({"origin": "SFO", "destination": "HND"})
    assert len(res) > 0
    assert res[0].airline == "Japan Air"
    
    res_comp = compare_flights.invoke({"flight_ids": ["FL-TYO-001"]})
    assert len(res_comp) == 1
    assert res_comp[0].flight_id == "FL-TYO-001"

def test_hotel_tools():
    res = search_hotels.invoke({"city": "Tokyo"})
    assert len(res) > 0
    assert res[0].city == "Tokyo"
    
    res_comp = compare_hotels.invoke({"hotel_ids": ["HT-TYO-001"]})
    assert len(res_comp) == 1
    assert res_comp[0].hotel_id == "HT-TYO-001"

def test_activity_tools():
    res = search_activities.invoke({"city": "Tokyo", "categories": ["food"]})
    assert len(res) > 0
    assert res[0].category == "food"
    
    res_filt = filter_activities.invoke({"activity_ids": ["ACT-TYO-001"], "min_rating": 4.0})
    assert len(res_filt) == 1
    assert res_filt[0].rating >= 4.0

def test_geography_tools():
    res = estimate_travel_time.invoke({"origin_zone": "Shinjuku", "destination_zone": "Shinjuku"})
    assert "Short" in res
    
    res = estimate_travel_time.invoke({"origin_zone": "Shinjuku", "destination_zone": "Shibuya"})
    assert "Medium" in res
