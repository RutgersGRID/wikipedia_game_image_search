Game Cover Art Finder from Wikipedia
---------------------

Overview:
---------
Game Cover Art Finder is a Streamlit-based web application that allows users to search for video game titles and view their cover art images fetched from Wikipedia. The application provides an easy and intuitive interface for searching game titles and displaying relevant images.

Features:
---------
- Search Functionality: Users can search for video game titles.
- Image Display: The application displays all available cover art images from Wikipedia for each selected game title.
- Multiple Selections: Users can select multiple titles and view images for all selected games.

Installation and Usage:
-----------------------
To run Game Cover Art Finder, you need to have Python installed on your system along with the dependencies managed by Poetry.

Prerequisites:
- Python 3
- Poetry

> To install Poetry:
  $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

Setting Up the Project:
1. Clone this repository or download the source code.
2. Navigate to the directory containing the application.
3. Install the dependencies using Poetry:
   $ poetry install

Running the Application:
1. Activate the Poetry environment:
   $ poetry shell
2. Run the application using Streamlit:
   $ streamlit run app.py
3. The application should open in your default web browser.

How to Use:
-----------
1. Enter a Game Title: Type the name of the video game in the search box.
2. Search Titles: Click on the 'Search Titles' button to fetch game titles from Wikipedia.
3. Select Titles: Check the checkboxes next to the game titles for which you want to view cover art.
4. Get Images: Click on the 'Get Images for Selected Titles' button to display the cover art images for the selected games.

Contributions:
---------------
Contributions to the Game Cover Art Finder are welcome. Please feel free to fork the repository, make changes, and create a pull request.

License:
--------
This project is open-source and available under the Apache 2.0 License.

Acknowledgments:
----------------
- This project uses the Wikipedia API to fetch game titles and images.
- Streamlit for providing the framework to build this interactive web application.
- Poetry for managing Python dependencies.

Note:
-----
This README is a template and can be modified to add more details or instructions specific to the project.
