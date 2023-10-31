# GenreGenius : A Movie Recommender

GenreGenius is an intuitive movie recommendation application that harnesses the power of IMDb data to provide users with tailored movie suggestions. Users can select their preferred genre and specify the number of movie recommendations they want.

## Features

- Genre Selection: Users can choose a genre from 20 different movie genres such as  Action, Adventure, Comedy, Drama, and many more.
- Customizable Recommendations: Users can specify the number of movie recommendations they want ranging from 1 to 10.
- Weighted Scoring: The application calculates a weighted score for movies based on IMDb ratings and release years. This ensures that movie recommendations are both highly rated and relatively recent.
- Randomized Selection: To keep recommendations fresh, GenreGenius shuffles the list of top-rated movies, preventing users from receiving the same suggestions repeatedly.
- User-Friendly Interface: The application provides a clean and intuitive graphical user interface using Tkinter, making it easy for users to navigate and obtain movie recommendations.
- Error Handling: GenreGenius includes error handling to address common user input errors such as input beyond allowed range, value error.
- Display IMDb Data: The application displays recommended movies with essential information, such as movie names, IMDb ratings and release years.


## Steps Involved

- Web Scraping and parsing: Sending HTTP request to  IMDb website to extract information such as movie name, movie genre, release year and IMDB rating.
- Data Processing : Using pandas to clean, process and filter the dataframe.
- Graphical User Interface (GUI) : Creating a user interface which takes input through radio buttons and entry widget and dispalying the recommended movies in a text widget.

## Tech

- Python: The core programming language used for developing GenreGenius.
- Pandas: A powerful data manipulation and analysis library in Python, used for handling and processing movie data.
- Beautiful Soup: A Python library for web scraping, used to extract movie information from IMDb web pages.
- Tkinter: The standard Python interface library for creating graphical user interfaces (GUIs). It's used to design and develop the user interface for GenreGenius.
- Requests: A Python library for making HTTP requests to fetch data from websites.

## Prerequisites

- Python 3.7 or higher
- Pacakages required are requests, bs4, pandas, tkinter. The specific versions of pacakges are mentioned in requirements.txt file

## Installation

- Install required packages using: 
```pip install -r requirements.txt```

## How to run

- Clone the repository:
```git clone https://github.com/anjalipatel2022/Python-Project-Anjali.git```
- Run the chatbot by executing main.py:  
```python main.py```
- GUI will take some time to open, once up select one genre of your choice by clicking on the radio button. (Note: You can only select one genre at a time.)
- Enter the number of movie recommendation you want. (Note: You can enter a number between 1 to 10. If you enter a number beyond this range or a non-numeric value an error message will be displayed on UI)
- Click the button to see The recommended movies in the GUI along with Imdb rating and release year
- close the GUI once you have got the recommendations


    
