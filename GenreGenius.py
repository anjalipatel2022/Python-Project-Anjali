import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import scrolledtext 

# Constants
GENRES = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Drama", "Family", "Fantasy", "History",
          "Horror", "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Sport", "Thriller", "War", "Western"]
MIN_RECOMMENDATIONS = 1
MAX_RECOMMENDATIONS = 10

# Global variables
selected_genre = ""
number_of_movies = 0
final_movie_data = None

# Scrape IMDb data
def scrape_imdb_data(pages):
    global final_movie_data
    final_movie_data = pd.DataFrame()

    for page_number in pages:
        for genre in GENRES:
            imdb_url = f"https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres={genre}&sort=user_rating,desc&start={page_number}&ref_=adv_nxt"
            headers = {"Accept-Language": "en-US, en;q=0.5"}
            results = requests.get(imdb_url, headers=headers)
            movie_soup = BeautifulSoup(results.text, "html.parser")
            movie_data_list = []
            movie_divs = movie_soup.find_all("div", class_="lister-item mode-advanced")
            for container in movie_divs:
                genre_info = container.find('span', class_='genre').text.strip()
                genres = [genre.strip() for genre in genre_info.split(',')]
                combined_genres = ', '.join(genres)
                movie_name = container.h3.a.text
                release_year = container.h3.find('span', class_='lister-item-year').text
                runtime_element = container.p.find('span', class_='runtime')
                movie_runtime = runtime_element.text if runtime_element else '-'
                imdb_rating = float(container.strong.text)

                movie_data_list.append({
                    'genre': genre,
                    'movie_genre': combined_genres,
                    'movie_name': movie_name,
                    'movie_year': release_year,
                    'movie_runtime': movie_runtime,
                    'movie_imdb_rating': imdb_rating
                })

            genre_movie_data_df = pd.DataFrame(movie_data_list)
            final_movie_data = pd.concat([final_movie_data, genre_movie_data_df], ignore_index=True)

    final_movie_data['movie_year'] = final_movie_data['movie_year'].str.extract('(\d{4})').fillna(0).astype(int)

# Recommend movies
def movie_recommender(selected_genre, number_of_movies):
    genre_movies = final_movie_data[final_movie_data['genre'] == selected_genre]

    # Calculate a weighted score based on IMDb ratings and release year
    genre_movies['weighted_score'] = ((genre_movies['movie_imdb_rating'] * genre_movies['movie_year']) / 100)

    # Sort the movies by the weighted score in descending order
    all_movies = genre_movies.sort_values(by='weighted_score', ascending=False)
    
    filtered_movies = all_movies[['movie_name', 'movie_imdb_rating', 'movie_year']].head(50)

    # Shuffle the top movies to randomize the selection
    top_movies = filtered_movies.sample(frac=0.2)
 
    top_movies = top_movies[['movie_name', 'movie_imdb_rating', 'movie_year']].head(number_of_movies)
    return top_movies

# GUI
def genre_genius_gui():
    root = tk.Tk()
    root.title("GenreGenius : A Movie Recommender")

    # Labels for genre selection and movie recommendations
    tk.Label(root, text="Select a genre of your choice:",bg="light blue",fg="black").grid(row=0, column=0)
    tk.Label(root, text="Enter the number of movie recommendations you want (1-10):",bg="light blue",fg="black").grid(row=0, column=5)

    # Variable to store the selected genre
    set_value = tk.StringVar()
    set_value.set(GENRES[0])
    selected_genre = str(set_value.get())

    # Function to handle genre selection
    def get_input(selected_value):
        selected_genre = str(selected_value)
        print(selected_genre)

    # RadioButtons for genre selection
    for i, genre in enumerate(GENRES):
        row, column = i % 10, i // 10
        print(set_value.get())
        tk.Radiobutton(root, text=genre, variable=set_value, value=genre, command=lambda : get_input(set_value.get())).grid(row=row + 1, column=column, sticky="W",pady=5)

    # Entry widget for number of movie recommendations
    e = tk.Entry(root, width=4, borderwidth=5)
    e.grid(row=0, column=6, columnspan=2, padx=5, pady=7)

    # Text widget to display recommendations
    recommendation_list = scrolledtext.ScrolledText(root, height=10, width=75, borderwidth=5)
    recommendation_list.grid(row=3, column=4, columnspan=3, rowspan=3)

    # Functions to handle button click, fetch recommendations and errors
    def print_suggestion():
        selected_movies = movie_recommender(selected_genre, number_of_movies)
        for movie in selected_movies.values:
            movie_name, imdb_rating, movie_year = movie
            recommendation_list.insert(tk.END, f"{movie_name} (IMDb Rating: {imdb_rating:.1f}, Release Year: {movie_year})\n")
            recommendation_list.configure(font = ('Consolas', 10))
        recommendation_list.config(state=tk.DISABLED)

    warning = tk.Label(root, text="")
    def button_click(value):
        global number_of_movies
        try:
            recommendation_list.config(state=tk.NORMAL)
            recommendation_list.delete('1.0', tk.END)
            number_of_movies = int(value)
            print(number_of_movies)
            if selected_genre and MIN_RECOMMENDATIONS <= number_of_movies <= MAX_RECOMMENDATIONS:
                warning.config(text="")
                warning.grid(row=1, column=5)
                print_suggestion()
            
            # Handling the error condition when use enters value beyond the range
            else:
                raise ValueError("Number of movies is out of range")
        except ValueError:
            warning.config(text="Please Enter a value between 1 to 10",fg="red")
            warning.grid(row=1, column=5)
        except Exception as e:
            warning.config(text="An error occurred. Please try again.", fg="red")
            warning.grid(row=1, column=5)

    # Button Widget to get recommendations
    tk.Button(root, text="Click here for Recommendations", bg="light blue", fg="black", command=lambda: button_click(e.get() if e.get() else 0)).grid(row=2, column=5)
  
    # Start the GUI main loop
    root.mainloop()

