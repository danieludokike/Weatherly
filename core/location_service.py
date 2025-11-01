
import requests


class LocationService:
    @staticmethod
    def get_current_city():
        """
        Returns a tuple (city_name, lat, lon)
        using IP-based geolocation from ip-api.com
        """
        try:
            r = requests.get("http://ip-api.com/json", timeout=5)
            data = r.json()
            if data.get("status") == "success":
                city = data.get("city", "Unknown")
                lat = data.get("lat")
                lon = data.get("lon")
                return city, lat, lon
            else:
                raise ValueError(f"Location lookup failed: {data.get('message')}")
        except Exception as e:
            print("Location detection failed:", e)
            # fallback to a Madrid
            return "Madrid", 40.4168, -3.7038

