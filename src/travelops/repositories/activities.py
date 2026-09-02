from typing import List, Optional
import json
from pathlib import Path
from travelops.models import ActivityOption

class ActivityRepository:
    def __init__(self, data_path: str = "data/activities.json"):
        self.data_path = Path(data_path)

    def _load_data(self) -> List[dict]:
        if not self.data_path.exists():
            return []
        with open(self.data_path, "r") as f:
            return json.load(f)

    def search_activities(self, city: str, categories: Optional[List[str]] = None) -> List[ActivityOption]:
        data = self._load_data()
        results = []
        for item in data:
            if item["city"].lower() == city.lower():
                if categories and item["category"] not in categories:
                    continue
                results.append(ActivityOption(**item))
        return results

    def get_by_id(self, activity_id: str) -> Optional[ActivityOption]:
        data = self._load_data()
        for item in data:
            if item["activity_id"] == activity_id:
                return ActivityOption(**item)
        return None
