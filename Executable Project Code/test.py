import tkinter as tk
from tkinter import scrolledtext, END
import requests
from PIL import Image, ImageTk
import os

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# --- Helper Function (No changes needed, but kept for context) ---
def set_background(window, image_path, width, height):
    try:
        img = Image.open(image_path)
        
        # Use Image.Resampling.LANCZOS for newer PIL versions
        # Older versions use Image.LANCZOS
        try:
            resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
        except AttributeError:
            resized_img = img.resize((width, height), Image.LANCZOS)
        
        bg_image = ImageTk.PhotoImage(resized_img)
        
        bg_label = tk.Label(window, image=bg_image)
        bg_label.image = bg_image
        
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
    except FileNotFoundError:
        print(f"Error: Background image not found at '{image_path}'")
    except Exception as e:
        print(f"An error has occured while setting background: {e}")

# --- NEW/MODIFIED FUNCTIONS ---

def get_entry_search_term():
    """Retrieves the value from the global entry widget."""
    return entry_var.get().strip() # Use entry_var to get the value

def run_search():
    """
    Called by the Search button. Gets the term and triggers the API call.
    Note: For a full application, you'd need logic here to know *what*
    the user is currently searching (characters, books, etc.).
    For this example, we assume it searches characters.
    """
    search_term = get_entry_search_term()
    print(f"Searching for: '{search_term}'")
    
    # Placeholder: Call the appropriate fetch function with the search term
    fetch_characters(search_term=search_term) 
    
    # The entry field should only be shown when a search is available
    entry.place(relx=0.25, rely=0.925, anchor="center")
    searchBtn.place(relx = 0.35, rely = 0.925, anchor = tk.CENTER)


def fetch_characters(search_term=""):
    """Fetches characters, optionally filtered by name."""
    text_box.config(state="normal")
    
    url = "https://api.potterdb.com/v1/characters"
    
    # Clear the text box
    text_box.delete('1.0', END)
    
    # 1. CONSTRUCT THE URL WITH THE SEARCH TERM
    # The PotterDB API uses the 'filter' parameter for searching names
    if search_term:
        # Example: search for character where name contains the search term
        # The structure of the PotterDB API for filtering is a bit complex,
        # often requiring a full URL or using specific filter parameters.
        # For simplicity, let's use the 'filter' param if the API supports partial name search:
        # NOTE: Using a simpler, non-API-specific filter here for demonstration.
        # A proper implementation would use `f"{url}?filter[name_cont]={search_term}"`
        # if the API supports Ransack-style filtering.
        
        # Using a simple name filter for demonstration
        api_url = f"{url}?filter[name_cont]={search_term}" 
    else:
        # Fetch all if no search term
        api_url = f"{url}?sort=name" 
        
    try:
        response = requests.get(api_url) 
        response.raise_for_status() # Raise an exception for bad status codes
        
        data = response.json()
        characters = data.get('data', [])
        
        if not characters:
             text_box.insert(END, f"No characters found for search term: '{search_term}'")
             
        for char in characters:
            attributes = char.get('attributes',  {})
            
            name = attributes.get('name', 'N/A')
            species = attributes.get('species', 'N/A')
            house = attributes.get('house', 'N/A')
            summary = attributes.get('summary', 'No summary available')
            wiki = attributes.get('wiki', 'No wiki link')
            
            char_info = (
                f"Name: {name}\n"
                f"Species: {species}\n"
                f"House: {house}\n"
                f"Summary: {summary[:150]}...\n" # Truncate summary for display
                f"Wiki: {wiki}\n"
                f"\n----------\n\n"
            )
            text_box.insert(END, char_info)
            
    except requests.exceptions.RequestException as e:
         text_box.insert(END, f"Error fetching data: {e}")

    text_box.config(state="disabled")
    text_box.place(relx = 0.5, rely = 0.5, anchor=tk.CENTER)

# (The fetch_books and fetch_movies functions are kept below, but simplified
# to remove the duplicate 'entry.place' call and for clean structure)
def fetch_books():
    text_box.config(state="normal")
    url = "https://api.potterdb.com/v1/books"
    text_box.delete('1.0', END)
    
    try:
        response = requests.get(f"{url}?sort=release_date") 
        response.raise_for_status()
        data = response.json()
        books = data.get('data', [])
        
        for book in books:
            attributes = book.get('attributes',  {})
            title = attributes.get('title', 'N/A')
            release_date = attributes.get('release_date', 'N/A')
            pages = attributes.get('pages', 'N/A')
            summary = attributes.get('summary', 'No summary available')
            wiki = attributes.get('wiki', 'No wiki link')
            
            book_info = (
                f"Title: {title}\n"
                f"Release Date: {release_date}\n"
                f"Pages: {pages}\n"
                f"Summary: {summary[:150]}...\n"
                f"Wiki: {wiki}\n"
                f"\n----------\n\n"
            )
            text_box.insert(END, book_info)
    except requests.exceptions.RequestException as e:
         text_box.insert(END, f"Error fetching data: {e}")
         
    text_box.config(state="disabled")
    text_box.place(relx = 0.5, rely = 0.5, anchor=tk.CENTER)
    
def fetch_movies():
    text_box.config(state="normal")
    url = "https://api.potterdb.com/v1/movies"
    text_box.delete('1.0', END)
    
    try:
        response = requests.get(f"{url}?sort=release_date") 
        response.raise_for_status()
        data = response.json()
        movies = data.get('data', [])
        
        for movie in movies:
            attributes = movie.get('attributes',  {})
            title = attributes.get('title', 'N/A')
            release_date = attributes.get('release_date', 'N/A')
            box_office = attributes.get('box_office', 'N/A')
            summary = attributes.get('summary', 'No summary available')
            wiki = attributes.get('wiki', 'No wiki link')
            
            movie_info = (
                f"Title: {title}\n"
                f"Release Date: {release_date}\n"
                f"Box Office: {box_office}\n"
                f"Summary: {summary[:150]}...\n"
                f"Wiki: {wiki}\n"
                f"\n----------\n\n"
            )
            text_box.insert(END, movie_info)
    except requests.exceptions.RequestException as e:
         text_box.insert(END, f"Error fetching data: {e}")
         
    text_box.config(state="disabled")
    text_box.place(relx = 0.5, rely = 0.5, anchor=tk.CENTER)


# --- MAIN APPLICATION SETUP ---

icon = r"Executable Project Code\harry-potter_flaticon.com.png"
mainMenuBackgroundImage = r"Executable Project Code\valerii-siserg-map3.jpg"


main = tk.Tk()
main.title("A Harry Potter Fan's Harry Potter Database Browser")
main.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
main.resizable(0, 0)

window_icon = tk.PhotoImage(file=icon)
main.iconphoto(True, window_icon)

set_background(main, mainMenuBackgroundImage, WINDOW_WIDTH, WINDOW_HEIGHT)

text_box = scrolledtext.ScrolledText(
    main,
    wrap = tk.WORD,
    width = 100,
    height = 20,
    font = ("Comic Sans MS", 14)
)

# 2. CREATE A STRINGVAR TO STORE THE ENTRY VALUE
entry_var = tk.StringVar(main) 
entry_var.set("Enter a character name...") # Set a placeholder text

entry = tk.Entry(
    main,
    textvariable = entry_var, # Link the StringVar to the Entry widget
    width = 25,
    font = ("Comic Sans MS", 14)
)

searchBtn = tk.Button(
    main,
    text = "Search: ",
    font = ("Comic Sans MS", 20),
    command = run_search # 3. LINK THE SEARCH BUTTON TO THE NEW FUNCTION
)

# BUTTONS (Only place widgets that should be visible immediately)
quitBtn = tk.Button(
    main,
    text = "Quit",
    font = ("Comic Sans MS", 20),
    command = main.quit,
    background = "salmon"
)
quitBtn.place(relx = 0.65, rely = 0.925, anchor = tk.CENTER) # Moved for better layout

spellsBtn = tk.Button(
    main,
    text = "Spells",
    font = ("Comic Sans MS", 20),
    background = "lightblue"
)
spellsBtn.place(relx = 0.1, rely = 0.075, anchor = tk.CENTER)

charactersBtn = tk.Button(
    main,
    text = "Characters",
    font = ("Comic Sans MS", 20),
    background = "lightblue",
    command = lambda: fetch_characters() # Call with no term to get all
)
charactersBtn.place(relx = 0.3, rely = 0.075, anchor = tk.CENTER)

moviesBtn = tk.Button(
    main,
    text = "Movies",
    font = ("Comic Sans MS", 20),
    background = "lightblue",
    command = fetch_movies
)
moviesBtn.place(relx = 0.5, rely = 0.075, anchor = tk.CENTER)

potionsBtn = tk.Button(
    main,
    text = "Potions",
    font = ("Comic Sans MS", 20),
    background = "lightblue"
)
potionsBtn.place(relx = 0.7, rely = 0.075, anchor = tk.CENTER)

booksBtn = tk.Button(
    main,
    text = "Books",
    font = ("Comic Sans MS", 20),
    background = "lightblue",
    command = fetch_books
)
booksBtn.place(relx = 0.9, rely = 0.075, anchor = tk.CENTER)

# Place the search entry and button (they should be visible when the app starts)
entry.place(relx=0.25, rely=0.925, anchor="center")
searchBtn.place(relx = 0.35, rely = 0.925, anchor = tk.CENTER)


main.mainloop()