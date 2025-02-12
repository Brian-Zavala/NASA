# NASA Data Explorer 🚀

Welcome to the NASA Data Explorer! This application allows you to explore various space and Earth science data using NASA's public APIs. Whether you're interested in astronomy, Mars rover photos, near-Earth objects, or natural events, this app provides an interactive way to discover and visualize the data.

## Features

- **Astronomy Picture of the Day (APOD)**: View the latest APOD, search for specific dates, date ranges, or random images.
- **Mars Rover Photos**: Explore photos taken by the Curiosity rover on Mars by Martian Sol or Earth date.
- **Near-Earth Objects (Asteroids NeoWs)**: Discover near-Earth objects, visualize their size distribution, and explore individual asteroids.
- **Earth Polychromatic Imaging Camera (EPIC)**: View images of Earth taken by the EPIC instrument on the DSCOVR spacecraft.
- **Earth Imagery**: Fetch and visualize Landsat 8 imagery for any location on Earth.
- **Earth Observatory Natural Event Tracker (EONET)**: Track natural events such as wildfires, storms, and volcanic eruptions.

## Installation

To run the NASA Data Explorer locally, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/Brian-Zavala/NASA.git
    cd NASA
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```sh
    streamlit run Home.py
    ```

## Usage

1. **API Key**: Enter your NASA API key in the sidebar. You can use the provided demo key for limited access or obtain your own key from [NASA API Portal](https://api.nasa.gov/).

2. **Choose an API**: Select the API you want to explore from the dropdown menu in the sidebar.

3. **Explore Data**: Interact with the various inputs and visualizations to explore the data provided by NASA.

## Screenshots

![NASA](https://live.staticflickr.com/65535/53555272470_5b297dac3f_b.jpg)
## Dependencies

- **Streamlit**: An app framework for Machine Learning and Data Science projects.
- **Pandas**: Data manipulation and analysis library.
- **Plotly**: Interactive graphing library.
- **Folium**: Python library for visualizing geospatial data.
- **PIL**: Python Imaging Library for image processing.

## Contributing

We welcome contributions to improve the NASA Data Explorer! Here are some ways you can contribute:

- **Report Issues**: If you find a bug, please report it by opening an issue on GitHub.
- **Suggest Features**: If you have an idea for a new feature or improvement, let us know by opening an issue.
- **Pull Requests**: If you want to contribute code, fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- NASA for providing the amazing data and APIs used in this application.
