import requests

def find_nearest_agrovets(api_key, location, radius=50000, keyword="agrovet"):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    params = {
        "location": location,  # Latitude and Longitude of Nairobi center
        "radius": radius,
        "keyword": keyword,
        "key": api_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json().get("results", [])
        print(f"result:{results}")
        return results
    else:
        print(f"Error: Received status code {response.status_code}. Response: {response.text}")
        return None

def get_place_details(api_key, place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    params = {
        "place_id": place_id,
        "fields": "name,vicinity,formatted_phone_number",
        "key": api_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        result = response.json().get("result", {})
        return result
    else:
        print(f"Error: Received status code {response.status_code}. Response: {response.text}")
        return None
    
def generate_google_maps_link(place_id):
    return f"https://www.google.com/maps/place/?q=place_id:{place_id}"
  
def generate_photo_url(photo_reference, api_key):
    return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
