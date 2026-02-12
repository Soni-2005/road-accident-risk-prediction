import requests

def get_ip_location():
    """
    Returns (lat, lon, city) using IP-based geolocation.
    Works without browser permissions.
    """
    try:
        response = requests.get("https://ipapi.co/json/", timeout=5)
        data = response.json()

        lat = data.get("latitude")
        lon = data.get("longitude")
        city = data.get("city", "Unknown location")

        if lat is None or lon is None:
            return None

        return lat, lon, city

    except Exception:
        return None
