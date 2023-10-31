from GenreGenius import genre_genius_gui, scrape_imdb_data

if __name__ == "__main__":
    pages = [1, 51]  
    scrape_imdb_data(pages)
    genre_genius_gui()
