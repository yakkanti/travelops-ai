from typing import List, Optional
import json
from pathlib import Path
from travelops.models import FlightOption

class FlightRepository:
    def __init__(self, data_path: str = "data/flights.json"):
        self.data_path = Path(data_path)

    def _load_data(self) -> List[dict]:
        if not self.data_path.exists():
            return []
        with open(self.data_path, "r") as f:
            return json.load(f)

    def search_flights(self, origin: str, destination: str) -> List[FlightOption]:
        data = self._load_data()
        results = [
            FlightOption(**item) 
            for item in data 
            if item["origin"].upper() == origin.upper() and item["destination"].upper() == destination.upper()
        ]
        return results

    def get_by_id(self, flight_id: str) -> Optional[FlightOption]:
        data = self._load_data()
        for item in data:
            if item["flight_id"] == flight_id:
                return FlightOption(**item)
        return None
