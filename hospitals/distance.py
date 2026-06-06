import geopandas as gpd
from pyproj import Geod

def process_overpass_results(data, user_lat, user_lon):
    elements = data.get('elements', [])

    features = []
    geod = Geod(ellps="WGS84")

    for elem in elements:
        if elem['type'] == 'node':
            e_lon, e_lat = elem['lon'], elem['lat']
        elif 'center' in elem:
            e_lon, e_lat = elem['center']['lon'], elem['center']['lat']
        else:
            continue
            
        _, _, distance = geod.inv(user_lon, user_lat, e_lon, e_lat)
        
        tags = elem.get('tags', {})
        name = tags.get('name', tags.get('name:ar', 'Unnamed Facility'))
        hospital_type = tags.get('amenity', 'hospital')
    
        features.append({
            'Name': name, 
            'Distance (km)': round(distance / 1000, 2),
            'Type': hospital_type,
        })

    gdf = gpd.GeoDataFrame(features)
    gdf = gdf.sort_values(by='Distance (km)').reset_index(drop=True)
    return gdf