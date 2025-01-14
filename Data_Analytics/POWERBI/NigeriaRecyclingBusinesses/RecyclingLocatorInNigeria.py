import googlemaps
from typing import List, Dict
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
import re
from time import sleep
import pandas as pd
import os

class RecyclingBusiness:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
        self.materials = set()
        self.website_materials = {}
        self.phone = None
        self.website = None
        self.rating = None
        self.opening_hours = []
        self.coordinates = {}
        self.place_id = None
        self.service_keywords = []  # For storing service keywords
        self.address_components = {}  # For storing detailed address components

    def analyze_business_type(self):
        """Analyze business name and description for material hints"""
        name_lower = self.name.lower()
        
        material_indicators = {
            'plastic': ['plastic', 'pet', 'polymer', 'hdpe', 'ldpe', 'pvc'],
            'metal': ['metal', 'scrap', 'aluminum', 'steel', 'copper', 'iron'],
            'paper': ['paper', 'cardboard', 'newspaper', 'magazine'],
            'glass': ['glass', 'bottles'],
            'electronics': ['electronic', 'e-waste', 'computer', 'phone', 'laptop'],
            'batteries': ['battery', 'batteries', 'accumulator'],
            'automotive': ['car', 'automotive', 'vehicle', 'auto parts'],
            'organic': ['organic', 'compost', 'food waste', 'green waste'],
            'textile': ['textile', 'clothing', 'fabric', 'clothes', 'garment'],
            'general': ['recycling center', 'waste management', 'collection center']
        }
        
        for material, indicators in material_indicators.items():
            if any(indicator in name_lower for indicator in indicators):
                self.materials.add(material)

    def to_dict(self) -> Dict:
        """Convert business object to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'address': self.address,
            'coordinates': self.coordinates,
            'place_id': self.place_id,
            'materials': list(self.materials),
            'website_materials': self.website_materials,
            'phone': self.phone,
            'website': self.website,
            'rating': self.rating,
            'opening_hours': self.opening_hours,
            'service_keywords': self.service_keywords,
            'address_components': self.address_components
        }

class EnhancedRecyclingFinder:
    def __init__(self, api_key: str):
        self.client = googlemaps.Client(key=api_key)

    def analyze_website_content(self, url: str) -> Dict:
        """Analyze business website for recycling materials information"""
        if not url:
            return {}
            
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            materials = {
                'plastic': ['plastic', 'PET', 'HDPE', 'PVC', 'LDPE', 'PP', 'PS'],
                'metal': ['metal', 'aluminum', 'steel', 'copper', 'iron', 'scrap metal'],
                'paper': ['paper', 'cardboard', 'newspaper', 'magazine'],
                'glass': ['glass', 'bottles'],
                'electronics': ['electronics', 'e-waste', 'computers', 'phones', 'electronic waste'],
                'batteries': ['batteries', 'battery'],
                'automotive': ['automotive', 'car parts', 'vehicle'],
                'organic': ['organic waste', 'compost', 'food waste'],
                'textile': ['textile', 'clothing', 'fabric', 'clothes'],
                'hazardous': ['hazardous', 'chemical', 'paint', 'oil']
            }
            
            found_materials = {}
            text_content = soup.get_text().lower()
            
            for category, keywords in materials.items():
                matches = []
                for keyword in keywords:
                    if keyword.lower() in text_content:
                        matches.append(keyword)
                if matches:
                    found_materials[category] = matches
                    
            return found_materials
            
        except Exception as e:
            print(f"Error analyzing website {url}: {str(e)}")
            return {}

    def search_businesses(self, location: str, radius: int = 5000) -> List[RecyclingBusiness]:
        """Search for recycling businesses with enhanced material analysis"""
        try:
            # Geocode the location
            geocode_result = self.client.geocode(location)
            
            if not geocode_result:
                raise ValueError(f"Could not find location: {location}")
            
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            
            print(f"\nSearch center coordinates: {lat}, {lng}")
            
            # Search for recycling businesses
            places_result = self.client.places_nearby(
                location=(lat, lng),
                radius=radius,
                keyword='recycling',
                type='establishment'
            )
            
            businesses = []
            
            # Process each result
            for place in places_result.get('results', []):
                place_details = self.client.place(place['place_id'])['result']
                
                business = RecyclingBusiness(
                    name=place.get('name'),
                    address=place_details.get('formatted_address')
                )
                
                # Capture coordinates
                business.coordinates = {
                    'lat': place['geometry']['location']['lat'],
                    'lng': place['geometry']['location']['lng']
                }
                business.place_id = place['place_id']
                
                # Store detailed address components
                if 'address_components' in place_details:
                    business.address_components = {
                        component['types'][0]: component['long_name']
                        for component in place_details['address_components']
                    }
                
                business.phone = place_details.get('formatted_phone_number')
                business.website = place_details.get('website')
                business.rating = place.get('rating')
                business.opening_hours = place_details.get('opening_hours', {}).get('weekday_text', [])
                
                # Analyze business type from name
                business.analyze_business_type()
                
                # If website available, analyze content
                if business.website:
                    print(f"Analyzing website for: {business.name}")
                    business.website_materials = self.analyze_website_content(business.website)
                    business.materials.update(business.website_materials.keys())
                    sleep(1)
                
                businesses.append(business)
                
            return businesses
            
        except Exception as e:
            print(f"Error in search: {str(e)}")
            return []

def main():
    # Replace with your Google API key
    GOOGLE_API_KEY = 'AIzaSyD9oDr8SfflDfoRYGTS2iovGmsmSM3toSY'
    
    finder = EnhancedRecyclingFinder(GOOGLE_API_KEY)
    
    try:
        # Read the Excel file
        excel_file = "nigeria_states_lga.xlsx"
        df = pd.read_excel(excel_file)
        
        # Ensure output directory exists
        output_dir = "NigeriaStateLGA_recyclers"
        os.makedirs(output_dir, exist_ok=True)
        
        for _, row in df.iterrows():
            state = row['state']
            lga = row['LGA']
            location = f"{lga}, {state}, Nigeria"
            
            print(f"\nSearching for recycling businesses in {location}...")
            results = finder.search_businesses(location)
            
            filename = os.path.join(output_dir, f"{state}_{lga}.json").replace(' ', '_').lower()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([business.to_dict() for business in results], f, indent=2, ensure_ascii=False)
            
            print(f"Data for {location} saved to {filename}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
