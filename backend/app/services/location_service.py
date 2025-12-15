import json
import os
from typing import List, Dict, Optional

class LocationService:
    """Service to handle Rwanda administrative locations and school mapping"""
    
    def __init__(self):
        self.locations_data = None
        self.load_locations()
    
    def load_locations(self):
        """Load Rwanda locations from JSON file or use fallback data"""
        try:
            locations_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "..", "rwanda-locations-json-master", "locations.json"
            )
            with open(locations_path, 'r', encoding='utf-8') as f:
                self.locations_data = json.load(f)
        except Exception as e:
            print(f"Error loading locations: {e}, using fallback data")
            # Fallback Rwanda locations data
            self.locations_data = {
                "provinces": [
                    {
                        "name": "Kigali City",
                        "districts": [
                            {"name": "Gasabo"},
                            {"name": "Kicukiro"},
                            {"name": "Nyarugenge"}
                        ]
                    },
                    {
                        "name": "Southern Province",
                        "districts": [
                            {"name": "Kamonyi"},
                            {"name": "Muhanga"},
                            {"name": "Ruhango"},
                            {"name": "Nyanza"},
                            {"name": "Huye"},
                            {"name": "Nyamagabe"},
                            {"name": "Gisagara"},
                            {"name": "Nyaruguru"}
                        ]
                    },
                    {
                        "name": "Western Province",
                        "districts": [
                            {"name": "Karongi"},
                            {"name": "Rutsiro"},
                            {"name": "Rubavu"},
                            {"name": "Nyabihu"},
                            {"name": "Ngororero"},
                            {"name": "Rusizi"},
                            {"name": "Nyamasheke"}
                        ]
                    },
                    {
                        "name": "Northern Province",
                        "districts": [
                            {"name": "Rulindo"},
                            {"name": "Gakenke"},
                            {"name": "Musanze"},
                            {"name": "Burera"},
                            {"name": "Gicumbi"}
                        ]
                    },
                    {
                        "name": "Eastern Province",
                        "districts": [
                            {"name": "Rwamagana"},
                            {"name": "Nyagatare"},
                            {"name": "Gatsibo"},
                            {"name": "Kayonza"},
                            {"name": "Kirehe"},
                            {"name": "Ngoma"},
                            {"name": "Bugesera"}
                        ]
                    }
                ]
            }
    
    def get_provinces(self) -> List[Dict]:
        """Get all provinces"""
        return [{"name": p["name"]} for p in self.locations_data.get("provinces", [])]
    
    def get_districts(self, province_name: str) -> List[Dict]:
        """Get all districts in a province"""
        for province in self.locations_data.get("provinces", []):
            if province["name"] == province_name:
                return [{"name": d["name"]} for d in province.get("districts", [])]
        return []
    
    def get_schools_by_district(self, db, province: str, district: str) -> List:
        """Get all TVET/TSS schools in a district"""
        from ..models.school import School
        return db.query(School).filter(
            School.province == province,
            School.district == district
        ).all()
    
    def validate_location(self, province: str, district: str) -> bool:
        """Validate if a location combination exists"""
        districts = self.get_districts(province)
        return any(d["name"] == district for d in districts)

# Singleton instance
location_service = LocationService()
