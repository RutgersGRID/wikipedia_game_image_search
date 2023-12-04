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

def display_title_checkboxes(titles):
    if 'selected_titles' not in st.session_state:
        st.session_state.selected_titles = {}
    for title in titles:
        # Use session state to store checkbox states
        if title not in st.session_state.selected_titles:
            st.session_state.selected_titles[title] = False
        checked = st.checkbox(title, key=title, value=st.session_state.selected_titles[title])
        st.session_state.selected_titles[title] = checked

def display_images_for_selected_titles():
    for title, is_selected in st.session_state.selected_titles.items():
        if is_selected:
            st.subheader(title)
            image_urls = get_all_image_urls(title)
            if image_urls:
                for url in image_urls:
                    st.image(url)
            else:
                st.write("No images found for this title.")


st.title('Game Cover Art Finder')
game_title_query = st.text_input('Enter a Game Title')

# Preload titles to session state
if 'titles' not in st.session_state:
    st.session_state.titles = []

if st.button('Search Titles'):
    st.session_state.titles = search_titles(game_title_query)

if st.session_state.titles:
    display_title_checkboxes(st.session_state.titles)

if st.button('Get Images for Selected Titles'):
    display_images_for_selected_titles()