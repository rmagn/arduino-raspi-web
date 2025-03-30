import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("METEOMATICS_USER")
PASSWORD = os.getenv("METEOMATICS_PASS")

def fetch_meteo_previsions(lat, lon):

    now = datetime.utcnow()
    now = now.replace(minute=0, second=0, microsecond=0)
    end = now + timedelta(days=7)

    start_str = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_str = end.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    interval = "PT1H"

    group1 = ",".join([
        "wind_speed_10m:ms", "wind_dir_10m:d", "wind_gusts_10m_1h:ms", "wind_gusts_10m_24h:ms",
        "t_2m:C", "t_max_2m_24h:C", "t_min_2m_24h:C", "msl_pressure:hPa",
        "precip_1h:mm", "precip_24h:mm"
    ])
    group2 = ",".join([
        "weather_symbol_1h:idx", "weather_symbol_24h:idx", "uv:idx",
        "sunrise:sql", "sunset:sql"
    ])

    def request(params):
        url = f"https://api.meteomatics.com/{start_str}--{end_str}:{interval}/{params}/{lat},{lon}/json"
        r = requests.get(url, auth=(USERNAME, PASSWORD))
        r.raise_for_status()
        return r.json()

    data1 = request(group1)
    data2 = request(group2)
    return data1, data2
