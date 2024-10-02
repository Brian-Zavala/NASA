import requests
import json

def get_data(api_key):
    raw_response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}').text
    response = json.loads(raw_response)
    return response

def get_date(response):
    return response.get('date', 'Date not available')

def get_explanation(response):
    return response.get('explanation', 'Explanation not available')

def get_hdurl(response):
    return response.get('hdurl', response.get('url', 'Image URL not available'))

def get_media_type(response):
    return response.get('media_type', 'unknown')

def get_service_version(response):
    return response.get('service_version', 'Service version not available')

def get_title(response):
    return response.get('title', 'Title not available')

def get_url(response):
    return response.get('url', 'URL not available')