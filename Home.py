import base64
import io
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from PIL import Image
from streamlit_folium import st_folium, folium_static
from datetime import datetime, timedelta
from functions import (fetch_apod_data, fetch_earth_imagery, fetch_eonet_events,
fetch_asteroid_data, fetch_earth_assets, fetch_and_display_photos, fetch_epic_data, process_eonet_data)

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
st.sidebar.markdown('<p class="title">Mission Control</p>', unsafe_allow_html=True)
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

    rover = "Curiosity"  # We're focusing only on Curiosity

    search_type = st.radio("Search by", ["Martian Sol", "Earth Date"])

    if search_type == "Martian Sol":
        sol = st.number_input("Enter Sol (Martian day)", min_value=0, value=1000, step=1)
        date_param = f"sol={sol}"
    else:
        earth_date = st.date_input("Select Earth Date")
        date_param = f"earth_date={earth_date}"

    cameras = {
        "FHAZ": "Front Hazard Avoidance Camera",
        "RHAZ": "Rear Hazard Avoidance Camera",
        "MAST": "Mast Camera",
        "CHEMCAM": "Chemistry and Camera Complex",
        "MAHLI": "Mars Hand Lens Imager",
        "MARDI": "Mars Descent Imager",
        "NAVCAM": "Navigation Camera"
    }

    camera = st.selectbox("Select Camera (optional)", ["All"] + list(cameras.keys()))
    camera_param = f"&camera={camera.lower()}" if camera != "All" else ""

    page = st.number_input("Page", min_value=1, value=1, step=1, key="page_number")

    # Fetch photos when any parameter changes
    fetch_and_display_photos(api_key, rover, date_param, camera_param, page)

elif api_choice == "Asteroids NeoWs":
    st.header("Near Earth Objects")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", datetime.now())
    with col2:
        end_date = st.date_input("End date", datetime.now() + timedelta(days=7))

    if start_date <= end_date:
        with st.spinner("Fetching asteroid data..."):
            asteroid_data = fetch_asteroid_data(api_key, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

        if "error" in asteroid_data:
            st.error(asteroid_data["error"]["message"])
        else:
            asteroid_counts = []
            all_asteroids = []
            for date, asteroids in asteroid_data["near_earth_objects"].items():
                asteroid_counts.append({"date": date, "count": len(asteroids)})
                all_asteroids.extend(asteroids)

            df = pd.DataFrame(asteroid_counts)

            # Bar chart of asteroid counts
            fig = px.bar(df, x="date", y="count", title="Number of Near Earth Objects by Date")
            st.plotly_chart(fig)

            total_asteroids = sum(df["count"])
            hazardous_asteroids = sum(1 for asteroid in all_asteroids if asteroid["is_potentially_hazardous_asteroid"])

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Near Earth Objects", total_asteroids)
            with col2:
                st.metric("Potentially Hazardous Asteroids", hazardous_asteroids)

            # Asteroid size distribution with names
            st.subheader("Asteroid Size Distribution")
            size_data = [{"name": asteroid["name"],
                          "size": asteroid["estimated_diameter"]["meters"]["estimated_diameter_max"],
                          "hazardous": asteroid["is_potentially_hazardous_asteroid"]}
                         for asteroid in all_asteroids]
            size_df = pd.DataFrame(size_data)
            fig_size = px.scatter(size_df, x="size", y="name", color="hazardous",
                                  labels={'size': 'Estimated Max Diameter (meters)', 'name': 'Asteroid Name',
                                          'hazardous': 'Potentially Hazardous'},
                                  title="Asteroid Sizes",
                                  hover_data=["size"])
            fig_size.update_layout(height=600)
            st.plotly_chart(fig_size)

            # Closest approaches
            st.subheader("Closest Approaches")
            closest_approaches = sorted(all_asteroids, key=lambda x: float(
                x["close_approach_data"][0]["miss_distance"]["kilometers"]))[:5]
            for asteroid in closest_approaches:
                st.write(f"Asteroid: {asteroid['name']}")
                st.write(f"Close approach date: {asteroid['close_approach_data'][0]['close_approach_date']}")
                st.write(
                    f"Miss distance: {float(asteroid['close_approach_data'][0]['miss_distance']['kilometers']):.2f} km")
                st.write("---")

            # Size comparison visualization
            st.subheader("Asteroid Size Comparison")
            selected_asteroids = st.multiselect("Select asteroids to compare",
                                                options=[asteroid['name'] for asteroid in all_asteroids],
                                                default=[asteroid['name'] for asteroid in all_asteroids[:5]])

            if selected_asteroids:
                comparison_data = [
                    {
                        "name": asteroid['name'],
                        "size": asteroid["estimated_diameter"]["meters"]["estimated_diameter_max"],
                        "hazardous": asteroid["is_potentially_hazardous_asteroid"]
                    }
                    for asteroid in all_asteroids if asteroid['name'] in selected_asteroids
                ]
                comparison_df = pd.DataFrame(comparison_data)
                fig_comparison = px.bar(comparison_df, x="name", y="size", color="hazardous",
                                        labels={'size': 'Estimated Max Diameter (meters)', 'name': 'Asteroid Name',
                                                'hazardous': 'Potentially Hazardous'},
                                        title="Asteroid Size Comparison")
                fig_comparison.update_layout(xaxis={'categoryorder': 'total descending'})
                st.plotly_chart(fig_comparison)

            # Individual asteroid explorer
            st.subheader("Explore Individual Asteroids")
            selected_asteroid = st.selectbox("Select an asteroid", [asteroid['name'] for asteroid in all_asteroids])
            asteroid_info = next(asteroid for asteroid in all_asteroids if asteroid['name'] == selected_asteroid)

            col1, col2 = st.columns([1, 2])
            with col1:
                # Display a generic asteroid image
                st.image("https://www.nasa.gov/sites/default/files/thumbnails/image/asteroid20180605-16.jpg",
                         caption="Generic Asteroid Image (NASA)")
            with col2:
                st.json(asteroid_info)

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

    # Initialize session state variables
    if 'earth_image' not in st.session_state:
        st.session_state.earth_image = None
    if 'earth_image_date' not in st.session_state:
        st.session_state.earth_image_date = None
    if 'earth_image_assets' not in st.session_state:
        st.session_state.earth_image_assets = None
    if 'earth_image_params' not in st.session_state:
        st.session_state.earth_image_params = None

    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("Latitude", value=29.78, step=0.01)
    with col2:
        lon = st.number_input("Longitude", value=-95.33, step=0.01)

    date = st.date_input("Select a date (YYYY-MM-DD)", datetime.now() - timedelta(days=30))

    # Add a slider for image resolution
    dim = st.slider("Image Resolution (degrees)", min_value=0.01, max_value=0.3, value=0.15, step=0.01,
                    help="Higher values result in a larger area but lower resolution. Lower values give higher resolution but cover a smaller area.")

    # Create a map to show the selected location
    location_map = folium.Map(location=[lat, lon], zoom_start=4)
    folium.Marker([lat, lon], popup="Selected Location").add_to(location_map)
    st_folium(location_map, width=425, height=325)

    if st.button("Fetch Earth Imagery"):
        with st.spinner("Fetching Earth imagery..."):
            image_result, params = fetch_earth_imagery(api_key, lat, lon, date.strftime("%Y-%m-%d"), dim)
            assets = fetch_earth_assets(api_key, lat, lon, date.strftime("%Y-%m-%d"))

        if isinstance(image_result, dict) and "error" in image_result:
            st.error(image_result["error"])
        elif isinstance(image_result, Image.Image):
            # Store the image, date, assets, and params in session state
            st.session_state.earth_image = image_result
            st.session_state.earth_image_date = date
            st.session_state.earth_image_assets = assets
            st.session_state.earth_image_params = params
            st.success("Image fetched successfully!")
        else:
            st.error("Unexpected result when fetching the image. Please try again.")

    # Display the image if it exists in session state
    if st.session_state.earth_image is not None:
        st.image(st.session_state.earth_image, caption=f"Landsat 8 Imagery (Date: {st.session_state.earth_image_date})",
                 use_column_width=True)

        # Display image information
        st.subheader("Image Information")
        image_width, image_height = st.session_state.earth_image.size
        st.write(f"Image dimensions: {image_width}x{image_height} pixels")
        st.write(f"Resolution: {st.session_state.earth_image_params['dim']} degrees")

        approx_km = st.session_state.earth_image_params['dim'] * 111  # Approximate km per degree
        st.write(f"Approximate area covered: {approx_km:.2f}km x {approx_km:.2f}km")

        # Display image metadata
        if st.session_state.earth_image_assets is not None:
            st.subheader("Image Metadata")
            st.json(st.session_state.earth_image_assets)

        # Convert PIL Image to bytes for download
        img_byte_arr = io.BytesIO()
        st.session_state.earth_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Provide a download button for the image
        st.download_button(
            label="Download Image",
            data=img_byte_arr,
            file_name="earth_imagery.png",
            mime="image/png"
        )

        # Create a base map for the image overlay
        m = folium.Map(location=[lat, lon], zoom_start=10)

        # Convert PIL Image to base64 for Folium
        buffered = io.BytesIO()
        st.session_state.earth_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Add image overlay to the map
        img_bounds = [
            [lat - st.session_state.earth_image_params['dim'] / 2,
             lon - st.session_state.earth_image_params['dim'] / 2],
            [lat + st.session_state.earth_image_params['dim'] / 2, lon + st.session_state.earth_image_params['dim'] / 2]
        ]
        folium.raster_layers.ImageOverlay(
            image=f"data:image/png;base64,{img_str}",
            bounds=img_bounds,
            opacity=0.6,
            name="Landsat 8 Image"
        ).add_to(m)

        # Display the map with the image overlay
        st.subheader("Image Overlay on Map")
        st_folium(m, width=725, height=500)
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