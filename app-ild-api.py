import wikipediaapi
import streamlit as st

wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='GameImage/1.0'
)

def get_game_cover_image(game_title):
    page = wiki_wiki.page(game_title)
    if page.exists():
        # Extracting image links from the page
        image_links = [url for url in page.images if "cover" in url.lower()]  # Filter for cover images
        if image_links:
            return image_links[0]  # Return the first cover image found
    return None


st.title('Game Cover Art Finder')

game_title = st.text_input('Enter a Game Title')

if st.button('Search'):
    image_url = get_game_cover_image(game_title)
    if image_url:
        st.image(image_url)
    else:
        st.write("Cover art not found.")

