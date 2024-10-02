import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import numpy as np
from streamlit import sidebar
from streamlit.components.v1 import components
from streamlit_folium import st_folium, folium_static
from folium import LayerControl
from datetime import datetime, timedelta
from folium.plugins import Draw, MeasureControl
from matplotlib import pyplot as plt
from functions import (fetch_apod_data, fetch_earth_imagery, fetch_eonet_events,
fetch_asteroid_data, fetch_earth_assets, fetch_mars_rover_photos, fetch_epic_data, process_eonet_data)

# Set page config
st.set_page_config(page_title="NASA Data Explorer", page_icon="🚀", layout="wide")

# Hide Streamlit toolbar
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Custom CSS with space theme and glowing text
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    body {
        background-color: #0c0c1d;
        color: #e0e0ff;
        font-family: 'Orbitron', sans-serif;
    }

    .stApp {
        background-image: url('https://wallpaperaccess.com/full/3861869.jpg');
        background-size: cover;
        background-attachment: fixed;
    }

    .title {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #00ffff;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff;
        animation: glow 1.5s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from {
            text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff;
        }
        to {
            text-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff, 0 0 40px #00ffff;
        }
    }

    .sidebar .sidebar-content {
        background-color: rgba(12, 12, 29, 0.8);
    }

    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 20px;
        border: 2px solid #45a049;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 0 10px #4CAF50;
    }

    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.1);
        color: #e0e0ff;
        border: 1px solid #00ffff;
        border-radius: 10px;
    }

    .stSelectbox>div>div>select {
        background-color: rgba(255, 255, 255, 0.1);
        color: #e0e0ff;
        border: 1px solid #00ffff;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Custom CSS
st.markdown("""
<style>
    body {
        font-family: 'Open Sans', sans-serif;
        color: #333333;
    }

    .title {
        color: #1a1a1a;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .sidebar {
        background-color: #f2f2f2;
        padding: 20px;
        border-radius: 10px;
    }

    .sidebar-title {
        color: #1a1a1a;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .api-section {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    .api-title {
        color: #1a1a1a;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .button {
        background-color: #ff5722;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .button:hover {
        background-color: #f44336;
    }

    @media (max-width: 767px) {
        .title {
            font-size: 24px;
        }

        .sidebar-title {
            font-size: 20px;
        }

        .api-title {
            font-size: 22px;
        }

        .button {
            font-size: 14px;
            padding: 8px 16px;
        }
    }
</style>
""", unsafe_allow_html=True)


# Sidebar
sidebar.markdown('<p class="title">Mission Control</p>', unsafe_allow_html=True)
api_key = st.sidebar.text_input("Enter your NASA API key", placeholder="Demo_key", value="kK3QAv8cS9Lcy00gBb8qRiC2Is076W5P96H9cEax", type="password")
api_choice = st.sidebar.selectbox("Choose an API", ["APOD", "Mars Rover Photos", "Asteroids NeoWs", "EPIC", "Earth Imagery", "EONET"])

# Alien animation in sidebar
alien_animation = """
<style>
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0px); }
}
.alien {
    font-size: 80px;
    animation: float 3s ease-in-out infinite;
    text-align: center;
    margin-bottom: -64px;
}
</style>
<div class="alien">👽</div>
"""
st.sidebar.markdown(alien_animation, unsafe_allow_html=True)

# Main app
st.markdown('<p class="title">🌌 Space Explorer 🛸</p>', unsafe_allow_html=True)

if api_choice == "APOD":
    st.header("Astronomy Picture of the Day")

    apod_mode = st.radio("Select APOD mode:", ["Today's APOD", "Specific Date", "Date Range", "Random Images"])

    if apod_mode == "Today's APOD":
        apod_data = fetch_apod_data(api_key)
        if isinstance(apod_data, dict):
            apod_data = [apod_data]  # Convert single dict to list for consistent handling

    elif apod_mode == "Specific Date":
        date = st.date_input("Select a date", datetime.now())
        apod_data = fetch_apod_data(api_key, date=date.strftime("%Y-%m-%d"))
        if isinstance(apod_data, dict):
            apod_data = [apod_data]

    elif apod_mode == "Date Range":
        start_date = st.date_input("Start date", datetime.now() - timedelta(days=7))
        end_date = st.date_input("End date", datetime.now())
        if start_date <= end_date:
            apod_data = fetch_apod_data(api_key, start_date=start_date.strftime("%Y-%m-%d"),
                                        end_date=end_date.strftime("%Y-%m-%d"))
        else:
            st.error("End date must be after start date")
            apod_data = []

    elif apod_mode == "Random Images":
        count = st.number_input("Number of random images", min_value=1, max_value=100, value=5)
        apod_data = fetch_apod_data(api_key, count=count)

    # Display APOD data
    if isinstance(apod_data, list):
        for item in apod_data:
            if "error" in item:
                st.error(item["error"]["message"])
            else:
                st.subheader(item["title"])
                if item["media_type"] == "image":
                    st.image(item["url"], caption=item["title"])
                elif item["media_type"] == "video":
                    st.video(item["url"])
                st.markdown(f"**Date:** {item['date']}")
                st.markdown(f"**Explanation:** {item['explanation']}")
                if "copyright" in item:
                    st.markdown(f"**Copyright:** {item['copyright']}")
                st.markdown("---")
    else:
        st.error("An error occurred while fetching APOD data.")


elif api_choice == "Mars Rover Photos":
    st.header("Mars Rover Photos")
    rover = st.selectbox("Select a rover", ["Curiosity", "Opportunity", "Spirit"])

    # Fetch the latest photos (sol 1000 for example, you may want to adjust this)
    sol = st.number_input("Enter Sol (Martian day)", min_value=0, value=1000, step=1)

    rover_data = fetch_mars_rover_photos(api_key, rover.lower(), sol)

    if "error" in rover_data:
        st.error(rover_data["error"]["message"])
    elif len(rover_data["photos"]) == 0:
        st.warning(f"No photos available for {rover} on Sol {sol}. Try a different Sol.")
    else:
        st.success(f"Found {len(rover_data['photos'])} photos")
        cols = st.columns(3)
        for i, photo in enumerate(rover_data["photos"][:9]):
            with cols[i % 3]:
                st.image(photo["img_src"], caption=f"Camera: {photo['camera']['full_name']}")

        # Display some metadata
        st.subheader("Rover Information")
        if rover_data["photos"]:
            rover_info = rover_data["photos"][0]["rover"]
            st.write(f"Rover Name: {rover_info['name']}")
            st.write(f"Landing Date: {rover_info['landing_date']}")
            st.write(f"Launch Date: {rover_info['launch_date']}")
            st.write(f"Status: {rover_info['status']}")

elif api_choice == "Asteroids NeoWs":
    st.header("Near Earth Objects")
    start_date = st.date_input("Start date", datetime.now())
    end_date = st.date_input("End date", datetime.now() + timedelta(days=7))

    if start_date <= end_date:
        asteroid_data = fetch_asteroid_data(api_key, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

        if "error" in asteroid_data:
            st.error(asteroid_data["error"]["message"])
        else:
            asteroid_counts = []
            for date, asteroids in asteroid_data["near_earth_objects"].items():
                asteroid_counts.append({"date": date, "count": len(asteroids)})

            df = pd.DataFrame(asteroid_counts)
            fig = px.bar(df, x="date", y="count", title="Number of Near Earth Objects by Date")
            st.plotly_chart(fig)

            total_asteroids = sum(df["count"])
            st.metric("Total Near Earth Objects", total_asteroids)

            hazardous_asteroids = sum(1 for date in asteroid_data["near_earth_objects"].values() for asteroid in date if
                                      asteroid["is_potentially_hazardous_asteroid"])
            st.metric("Potentially Hazardous Asteroids", hazardous_asteroids)
    else:
        st.error("End date must be after start date")

elif api_choice == "EPIC":
    st.header("Earth Polychromatic Imaging Camera (EPIC)")
    date = st.date_input("Select a date", datetime.now() - timedelta(days=2))

    epic_data = fetch_epic_data(api_key, date.strftime("%Y-%m-%d"))

    if isinstance(epic_data, dict) and "error" in epic_data:
        st.error(epic_data["error"]["message"])
    elif len(epic_data) == 0:
        st.warning(f"No EPIC images available for {date}")
    else:
        st.success(f"Found {len(epic_data)} EPIC images")
        cols = st.columns(3)
        for i, image in enumerate(epic_data[:9]):
            with cols[i % 3]:
                image_date = datetime.strptime(image["date"], "%Y-%m-%d %H:%M:%S")
                formatted_date = image_date.strftime("%Y/%m/%d")
                image_url = f"https://epic.gsfc.nasa.gov/archive/natural/{formatted_date}/png/{image['image']}.png"
                st.image(image_url, caption=f"Date: {image['date']}")

        # Create a map of image locations
        latitudes = [float(image["centroid_coordinates"]["lat"]) for image in epic_data]
        longitudes = [float(image["centroid_coordinates"]["lon"]) for image in epic_data]
        df = pd.DataFrame({"lat": latitudes, "lon": longitudes})
        fig = px.scatter_geo(df, lat="lat", lon="lon", projection="natural earth")
        fig.update_layout(title="EPIC Image Locations")
        st.plotly_chart(fig)

elif api_choice == "Earth Imagery":
    st.header("Earth Imagery")

    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("Latitude", value=29.78, step=0.01)
    with col2:
        lon = st.number_input("Longitude", value=-95.33, step=0.01)

    date = st.date_input("Select a date (YYYY-MM-DD)", datetime.now() - timedelta(days=30))

    # Create a base map
    m = folium.Map(location=[lat, lon], zoom_start=10)

    # Add drawing support
    draw = Draw(
        draw_options={
            'polyline': False,
            'rectangle': True,
            'polygon': True,
            'circle': True,
            'marker': True,
            'circlemarker': False
        },
        edit_options={'edit': True}
    )
    draw.add_to(m)

    # Add measure control
    MeasureControl(position='topright', primary_length_unit='kilometers').add_to(m)

    # Add layer control
    LayerControl().add_to(m)

    # Display the map
    st_data = st_folium(m, width=725, height=500)

    if st.button("Fetch Earth Imagery"):
        with st.spinner("Fetching Earth imagery..."):
            image = fetch_earth_imagery(api_key, lat, lon, date.strftime("%Y-%m-%d"))
            assets = fetch_earth_assets(api_key, lat, lon, date.strftime("%Y-%m-%d"))

        if image:
            st.image(image, caption="Landsat 8 Imagery", use_column_width=True)

            # Display image metadata
            st.subheader("Image Metadata")
            st.json(assets)

            # Add image overlay to the map
            img_bounds = [[lat - 0.1, lon - 0.1], [lat + 0.1, lon + 0.1]]  # Approximate bounds
            folium.raster_layers.ImageOverlay(
                image=image,
                bounds=img_bounds,
                opacity=0.6,
                name="Landsat 8 Image"
            ).add_to(m)

            # Re-render the map with the new layer
            st_data = st_folium(m, width=725, height=500)

            # Add image analysis features
            st.subheader("Image Analysis")

            # Convert image to numpy array for analysis
            img_array = np.array(image)

            # Display basic image statistics
            st.write(f"Image shape: {img_array.shape}")
            st.write(f"Mean pixel value: {np.mean(img_array):.2f}")
            st.write(f"Standard deviation: {np.std(img_array):.2f}")

            # Add a histogram of pixel values
            fig, ax = plt.subplots()
            ax.hist(img_array.ravel(), bins=256, range=(0, 255))
            ax.set_title("Histogram of Pixel Values")
            ax.set_xlabel("Pixel Value")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

        else:
            st.error("Failed to fetch Earth imagery. Please try a different location or date.")

    # Display information about map interactions
    st.subheader("Map Interaction Data")
    st.write(st_data)

elif api_choice == "EONET":
    st.header("Earth Observatory Natural Event Tracker (EONET)")

    col1, col2, col3 = st.columns(3)
    with col1:
        days = st.slider("Number of days to look back", 1, 365, 30)
    with col2:
        limit = st.slider("Maximum number of events", 100, 2000, 500)
    with col3:
        status = st.selectbox("Event status", ["all", "open", "closed"])

    if st.button("Fetch EONET Data"):
        with st.spinner("Fetching EONET data..."):
            eonet_data = fetch_eonet_events(limit=limit, days=days, status=status)

        if eonet_data and "events" in eonet_data:
            events_df = process_eonet_data(eonet_data)

            if not events_df.empty:
                st.success(f"Successfully fetched {len(events_df)} events")

                # Event categories pie chart
                fig = px.pie(events_df, names="category", title="Event Categories")
                st.plotly_chart(fig)

                # Event timeline
                events_df['date'] = pd.to_datetime(events_df['date'])
                fig_timeline = px.histogram(events_df, x="date", color="category", title="Event Timeline")
                st.plotly_chart(fig_timeline)

                # Filtering options
                st.subheader("Filter Events")
                selected_categories = st.multiselect("Select categories", options=sorted(events_df["category"].unique()))
                min_date = events_df["date"].min().date()
                max_date = events_df["date"].max().date()
                date_range = st.date_input("Select date range", [min_date, max_date])

                # Apply filters
                filtered_df = events_df
                if selected_categories:
                    filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]
                filtered_df = filtered_df[
                    (filtered_df["date"].dt.date >= date_range[0]) & (filtered_df["date"].dt.date <= date_range[1])]

                # Map of events
                st.subheader("Event Map")
                m = folium.Map(location=[0, 0], zoom_start=2)
                for _, event in filtered_df.iterrows():
                    folium.Marker(
                        location=[event["lat"], event["lon"]],
                        popup=f"<b>{event['title']}</b><br>Date: {event['date']}<br><a href='{event['source']}' target='_blank'>More Info</a>",
                        tooltip=f"{event['category']}: {event['title']}"
                    ).add_to(m)
                folium_static(m)

                # Events table
                st.subheader("Filtered Events")
                st.dataframe(filtered_df[["title", "category", "date", "source"]])

                # Download CSV
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download filtered events as CSV",
                    data=csv,
                    file_name="eonet_events_filtered.csv",
                    mime="text/csv",
                )
            else:
                st.warning("No events found for the specified criteria.")
        else:
            st.error("Failed to fetch EONET data or no events found.")


st.sidebar.markdown("---")
st.sidebar.info("This app uses NASA's public APIs to explore various space and Earth science data. Enter your API key for full access, or use key provided for limited access.")
st.sidebar.warning("Note: Using key provided may result in rate limiting.")