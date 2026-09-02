from typing import List, Optional
import json
from pathlib import Path
from travelops.models import HotelOption

class HotelRepository:
    def __init__(self, data_path: str = "data/hotels.json"):
        self.data_path = Path(data_path)

    def _load_data(self) -> List[dict]:
        if not self.data_path.exists():
            return []
        with open(self.data_path, "r") as f:
            return json.load(f)

    def search_hotels(self, city: str) -> List[HotelOption]:
        data = self._load_data()
        results = [
            HotelOption(**item) 
            for item in data 
            if item["city"].lower() == city.lower()
        ]
        return results

    def get_by_id(self, hotel_id: str) -> Optional[HotelOption]:
        data = self._load_data()
        for item in data:
            if item["hotel_id"] == hotel_id:
                return HotelOption(**item)
        return None
