import streamlit as st
import requests
import PIL as Image
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO


# Helper functions
def fetch_apod_data(api_key, date=None, start_date=None, end_date=None, count=None, thumbs=False):
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    params = {}
    if date:
        params['date'] = date
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    if count:
        params['count'] = count
    if thumbs:
        params['thumbs'] = 'true'

    response = requests.get(url, params=params)
    return response.json()


def fetch_mars_rover_photos(api_key, rover, sol):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos"
    params = {
        "sol": sol,
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    return response.json()


def fetch_asteroid_data(api_key, start_date, end_date):
    url = f"https://api.nasa.gov/neo/rest/v1/feed"
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    return response.json()


def fetch_epic_data(api_key, date):
    url = f"https://api.nasa.gov/EPIC/api/natural/date/{date}?api_key={api_key}"
    response = requests.get(url)
    return response.json()


def fetch_eonet_events(limit=1000, days=365, status="all"):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    url = "https://eonet.gsfc.nasa.gov/api/v3/events"
    params = {
        "limit": limit,
        "start": start_date.strftime("%Y-%m-%d"),
        "end": end_date.strftime("%Y-%m-%d"),
        "status": status
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching EONET data: {e}")
        return None


def process_eonet_data(eonet_data):
    events = []
    for event in eonet_data["events"]:
        category = event["categories"][0]["title"] if event["categories"] else "Uncategorized"

        for geometry in event["geometry"]:
            if geometry["type"] == "Point":
                lat, lon = geometry["coordinates"][1], geometry["coordinates"][0]
                events.append({
                    "id": event["id"],
                    "title": event["title"],
                    "category": category,
                    "date": geometry["date"],
                    "lat": lat,
                    "lon": lon,
                    "source": event.get("sources", [{}])[0].get("url", "N/A")
                })

    return pd.DataFrame(events)


def fetch_earth_data_search(query, limit=10):
    url = f"https://cmr.earthdata.nasa.gov/search/collections.json?keyword={query}&page_size={limit}"
    response = requests.get(url)
    return response.json()


def fetch_earth_imagery(api_key, lat, lon, date, dim=0.025):
    url = f"https://api.nasa.gov/planetary/earth/imagery"
    params = {
        "lon": lon,
        "lat": lat,
        "date": date,
        "dim": dim,
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        return None


def fetch_earth_assets(api_key, lat, lon, date):
    url = f"https://api.nasa.gov/planetary/earth/assets"
    params = {
        "lon": lon,
        "lat": lat,
        "date": date,
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    return response.json()
