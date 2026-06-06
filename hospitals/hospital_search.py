import requests
from app.config import OVERPASS_URL

def get_closest_facilities_safe(lat, lon, radius=20000):
    
    
    headers = {
        'User-Agent': 'Medical_Assistant',
        'Referer': 'https://overpass-turbo.eu/'
    }

    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"~"hospital|clinic"](around:{radius}, {lat}, {lon});
      way["amenity"~"hospital|clinic"](around:{radius}, {lat}, {lon});
    );
    out center;
    """
    
    try:
        response = requests.get(OVERPASS_URL, params={'data': query}, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return data 
        else:
            return f"{response.status_code}: {response.text}"
            
    except Exception as e:
        return e