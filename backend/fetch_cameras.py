import requests
import json
import random

def fetch_real_cameras():
    url = "https://overpass-api.de/api/interpreter"
    query = """
    [out:json];
    node["man_made"="surveillance"](12.7,77.4,13.2,77.8);
    out;
    """
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'ProjectDrishti/1.0'
    }
    print("Fetching cameras from OSM...")
    response = requests.post(url, data={'data': query}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        elements = data.get('elements', [])
        print(f"Fetched {len(elements)} real cameras from OpenStreetMap. Assigning street names...")
        
        cameras = []
        for idx, el in enumerate(elements):
            severity = round(random.uniform(20.0, 95.0), 1)
            if severity > 70: color = 'bg-primary'
            elif severity > 50: color = 'bg-orange-500'
            else: color = 'bg-yellow-500'
            
            tags = el.get('tags', {})
            name = tags.get('name')
            
            if not name:
                streets = ["MG Road", "Brigade Road", "Koramangala 80ft Road", "Outer Ring Road", "Indiranagar 100ft Road", "HSR Layout Sector 2", "Whitefield Main Road", "Marathahalli Bridge", "Silk Board Junction", "Electronic City Phase 1", "Hebbal Flyover", "Malleswaram 8th Cross", "Jayanagar 4th Block", "Bannerghatta Road", "Hosur Road"]
                locations = ["Signal", "Junction", "Traffic Cam", "Speed Camera", "Checkpost", "Intersection"]
                name = f"{random.choice(streets)} {random.choice(locations)} {random.randint(1, 100)}"
                
            if "surveillance" in tags and "Surveillance Node" in name:
                name += f" ({tags['surveillance']})"
                
            cameras.append({
                "id": str(el['id']),
                "name": name,
                "severity": severity,
                "change": round(random.uniform(-10.0, 10.0), 1),
                "violations": int(severity * random.uniform(1.5, 3.0)),
                "lat": el['lat'],
                "lng": el['lon'],
                "color": color
            })
            
        cameras.sort(key=lambda x: x["severity"], reverse=True)
        for i, c in enumerate(cameras):
            c["rank"] = i + 1
            
        with open("real_cameras.json", "w") as f:
            json.dump(cameras, f)
            
        print("Saved to real_cameras.json")
    else:
        print("Failed to fetch:", response.status_code, response.text)

if __name__ == "__main__":
    fetch_real_cameras()
