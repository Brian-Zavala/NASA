import streamlit as st
import requests
from PIL import Image
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO


@st.cache_data(ttl=3600)  # Cache for 1 hour
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


@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_mars_rover_photos(api_key, rover, date_param, camera=None, page=1):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos"
    params = {
        "api_key": api_key,
        "page": page
    }

    if "sol=" in date_param:
        params["sol"] = date_param.split("=")[1]
    elif "earth_date=" in date_param:
        params["earth_date"] = date_param.split("=")[1]

    if camera and camera != "All":
        params["camera"] = camera.lower()

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.RequestException as e:
        return {"error": {"message": f"Failed to fetch data: {str(e)}"}}


@st.cache_data(ttl=3600)  # Cache for 1 hour
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


@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_earth_imagery(api_key, lat, lon, date, dim=0.15):
    url = f"https://api.nasa.gov/planetary/earth/imagery"
    params = {
        "lon": lon,
        "lat": lat,
        "date": date,
        "dim": dim,
        "api_key": api_key
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        image = Image.open(BytesIO(response.content))
        return image, params
    except requests.RequestException as e:
        return {"error": f"Failed to fetch image: {str(e)}"}, None
    except IOError as e:
        return {"error": f"Failed to process image: {str(e)}"}, None


# Function to fetch and display photos
def fetch_and_display_photos(api_key, rover, date_param, camera_param, page):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover.lower()}/photos?{date_param}{camera_param}&page={page}&api_key={api_key}"

    with st.spinner("Fetching Mars Rover photos..."):
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            photos = data.get("photos", [])

            if len(photos) == 0:
                st.warning(f"No photos available for the selected criteria. Try different parameters.")
            else:
                st.success(f"Found {len(photos)} photos")

                # Display some metadata
                if photos:
                    st.subheader("Rover Information")
                    rover_info = photos[0]["rover"]
                    st.write(f"Rover Name: {rover_info['name']}")
                    st.write(f"Landing Date: {rover_info['landing_date']}")
                    st.write(f"Launch Date: {rover_info['launch_date']}")
                    st.write(f"Status: {rover_info['status']}")

                # Display photos
                st.subheader("Photos")
                cols = st.columns(3)
                for i, photo in enumerate(photos):
                    with cols[i % 3]:
                        st.markdown('<div class="responsive-img-container">', unsafe_allow_html=True)
                        st.image(photo["img_src"], caption=f"Photo {i + 1} - Camera: {photo['camera']['full_name']}", use_column_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                # Create a dataframe of all photos for download
                photos_df = pd.DataFrame(photos)
                csv = photos_df.to_csv(index=False)
                st.download_button(
                    label="Download photo data as CSV",
                    data=csv,
                    file_name=f"{rover}_photos.csv",
                    mime="text/csv",
                )
        else:
            st.error(f"Error fetching data: {response.status_code} - {response.text}")


@st.cache_data
def get_camera_options():
    return {
        "FHAZ": "Front Hazard Avoidance Camera",
        "RHAZ": "Rear Hazard Avoidance Camera",
        "MAST": "Mast Camera",
        "CHEMCAM": "Chemistry and Camera Complex",
        "MAHLI": "Mars Hand Lens Imager",
        "MARDI": "Mars Descent Imager",
        "NAVCAM": "Navigation Camera"
    }


@st.cache_data(ttl=3600)  # Cache for 1 hour
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


# Function to load an image from a URL
def load_image_from_url(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))
