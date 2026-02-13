import requests

def get_coordinates(place_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place_name,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "route-safety-analyzer"
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if len(data) == 0:
        return None

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])

    return lat, lon

def fetch_nearby_data(lat, lon, radius=500):
    overpass_url = "https://overpass-api.de/api/interpreter"


    query = f"""
    [out:json];
    (
      node["amenity"="restaurant"](around:{radius},{lat},{lon});
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      node["amenity"="police"](around:{radius},{lat},{lon});
      node["shop"](around:{radius},{lat},{lon});
    );
    out;
    """

    try:
        response = requests.post(
            overpass_url,
            data=query,
            timeout=30
        )

        # If API fails, don't crash
        if response.status_code != 200:
            print("Overpass error:", response.status_code)
            return {"elements": []}

        return response.json()

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return {"elements": []}



def extract_counts(osm_data):
    elements = osm_data.get("elements", [])

    shops = 0
    restaurants = 0
    hospitals = 0
    police = 0
    open_24_7 = 0

    for el in elements:
        tags = el.get("tags", {})

        if tags.get("amenity") == "restaurant":
            restaurants += 1

        if tags.get("amenity") == "hospital":
            hospitals += 1

        if tags.get("amenity") == "police":
            police += 1

        if "shop" in tags:
            shops += 1

        # Check 24/7 places
        if tags.get("opening_hours") == "24/7":
            open_24_7 += 1

    return {
        "shops": shops,
        "restaurants": restaurants,
        "hospitals": hospitals,
        "police": police,
        "open_24_7": open_24_7
    }



def fetch_data(place_name):
    coords = get_coordinates(place_name)

    if not coords:
        return None

    lat, lon = coords
    osm_data = fetch_nearby_data(lat, lon)
    counts = extract_counts(osm_data)

    return counts


def search_places(query):
    url = "https://nominatim.openstreetmap.org/search"
    
    params = {
        "q": query,
        "format": "json",
        "limit": 5
    }

    headers = {
        "User-Agent": "route-safety-analyzer"
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    places = []
    for item in data:
        places.append({
            "display_name": item["display_name"],
            "lat": float(item["lat"]),
            "lon": float(item["lon"])
        })

    return places






