import streamlit as st
import requests
import pandas as pd
import re

# Define the user agent for requests
USER_AGENT = 'WikiGameImageSearch/1.0 (https://github.com/rianders/rianders-wikipedia_game_image_search; contact via GitHub)'

def search_titles(query):
    URL = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json"
    }
    response = requests.get(url=URL, headers={'User-Agent': USER_AGENT}, params=params)
    data = response.json()
    return [result['title'] for result in data['query']['search']]

def get_game_info(game_title):
    URL = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": game_title,
        "prop": "wikitext",
        "format": "json"
    }

    response = requests.get(url=URL, headers={'User-Agent': USER_AGENT}, params=params)
    data = response.json()

    if 'error' in data:
        print(f"Error fetching page data: {data['error'].get('info')}")
        return None

    wikitext = data['parse']['wikitext']['*']

    infobox_start = wikitext.find("{{Infobox")
    if infobox_start == -1:
        return None

    # Search for the section containing "modes" or the end of the infobox
    infobox_end = wikitext.find("| modes", infobox_start)
    if infobox_end == -1:
        infobox_end = wikitext.find("}}", infobox_start)
    else:
        # Find the end of the line for the "modes" section
        infobox_end = wikitext.find("\n", infobox_end)

    if infobox_end == -1 or infobox_end < infobox_start:
        return None

    infobox_text = wikitext[infobox_start:infobox_end]

    # Basic parsing of the infobox wikitext
    infobox = {}
    for line in infobox_text.split('\n'):
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()

            # Remove any wiki markup
            value = re.sub(r'\[\[|\]\]', '', value)  # Remove [[...]] markup
            value = re.sub(r'<.*?>', '', value)     # Remove <...> markup
            value = re.sub(r'\{.*?\}', '', value)   # Remove {...} markup

            infobox[key] = value

    return infobox

def get_all_image_urls(game_title):
    URL = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": game_title,
        "prop": "imageinfo",
        "iiprop": "url",
        "generator": "images",
        "gimlimit": "max",  # Adjust the limit as needed
        "format": "json"
    }

    response = requests.get(url=URL, headers={'User-Agent': USER_AGENT}, params=params)
    data = response.json()

    image_urls = []
    pages = data.get('query', {}).get('pages', {})
    for page_id, page in pages.items():
        if 'imageinfo' in page:
            for imageinfo in page['imageinfo']:
                image_urls.append(imageinfo['url'])

    return image_urls




def display_title_checkboxes(titles):
    if 'selected_titles' not in st.session_state:
        st.session_state.selected_titles = {}
    for title in titles:
        if title not in st.session_state.selected_titles:
            st.session_state.selected_titles[title] = False
        checked = st.checkbox(title, key=title, value=st.session_state.selected_titles[title])
        st.session_state.selected_titles[title] = checked

def display_images_for_selected_titles():
    for title, is_selected in st.session_state.selected_titles.items():
        if is_selected:
            st.subheader(title)
            
            # Fetch and display game information
            game_info = get_game_info(title)
            if game_info:
                # Transpose the dictionary into a DataFrame
                game_info_df = pd.DataFrame([game_info])
                st.table(game_info_df)
            else:
                st.write("No detailed information found for this title.")

            # Fetch and display images
            image_urls = get_all_image_urls(title)
            if image_urls:
                for url in image_urls:
                    st.image(url)
            else:
                st.write("No images found for this title.")

st.title('Game Cover Art Finder')
game_title_query = st.text_input('Enter a Game Title')

if st.button('Search Titles'):
    # Resetting the titles and selected titles
    st.session_state.titles = search_titles(game_title_query)
    st.session_state.selected_titles = {title: False for title in st.session_state.titles}

# Display the search results as checkboxes
if 'titles' in st.session_state and st.session_state.titles:
    display_title_checkboxes(st.session_state.titles)

if st.button('Get Images for Selected Titles'):
    display_images_for_selected_titles()
