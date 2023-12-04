import streamlit as st
import requests

def search_titles(query):
    session = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json"
    }
    response = session.get(url=URL, params=params)
    data = response.json()
    return [result['title'] for result in data['query']['search']]


def get_all_image_urls(game_title):
    session = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": game_title,
        "prop": "images"
    }
    response = session.get(url=URL, params=params)
    data = response.json()

    image_urls = []
    pages = data['query']['pages']
    for _, page in pages.items():
        if 'images' in page:
            for image in page['images']:
                image_title = image['title']
                image_info_params = {
                    "action": "query",
                    "format": "json",
                    "titles": image_title,
                    "prop": "imageinfo",
                    "iiprop": "url"
                }
                image_info_response = session.get(url=URL, params=image_info_params)
                image_info_data = image_info_response.json()
                for _, img_data in image_info_data['query']['pages'].items():
                    if 'imageinfo' in img_data:
                        image_urls.append(img_data['imageinfo'][0]['url'])

    return image_urls

def display_search_results():
    game_title_query = st.text_input('Enter a Game Title')
    if st.button('Search Titles'):
        titles = search_titles(game_title_query)
        if titles:
            return st.selectbox('Select a Title', titles)
        else:
            st.write("No titles found.")
    return None

def display_images_for_title(title):
    if title and st.button('Get Images'):
        image_urls = get_all_image_urls(title)
        if image_urls:
            for url in image_urls:
                st.image(url)
        else:
            st.write("No images found for this title.")

st.title('Game Cover Art Finder')
selected_title = display_search_results()
display_images_for_title(selected_title)
