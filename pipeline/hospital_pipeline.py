from hospitals.location import get_coords
from hospitals.hospital_search import get_closest_facilities_safe
from hospitals.distance import process_overpass_results
from prompts.emergency_prompt import emergency_build_prompt
from llm.response_generator import run_chain

async def hospital_pipeline(query, user_id="user_1"):
    user_lat, user_lon = await get_coords()
    overpass_data = get_closest_facilities_safe(user_lat, user_lon, radius=20000)
    print(overpass_data)
    print(type(overpass_data))
    response = process_overpass_results(overpass_data, user_lat, user_lon)
    prompt = emergency_build_prompt()
    response = run_chain(prompt, {
        "query": query,
        "closest_hospitals": response
    }, user_id)

    return response