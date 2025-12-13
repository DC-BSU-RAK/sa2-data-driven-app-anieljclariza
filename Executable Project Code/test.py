import tkinter as tk
from tkinter import scrolledtext, END, messagebox
import requests
from PIL import Image, ImageTk
import os
# CRITICAL FIX: Import quote for safe URL construction
from requests.utils import quote 

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# --- Helper Function (No changes needed, but kept for context) ---
def set_background(window, image_path, width, height):
    """Sets a background image on the main window."""
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
        # messagebox.showerror("File Error", f"Background image not found at '{image_path}'")
    except Exception as e:
        print(f"An error has occured while setting background: {e}")
        # messagebox.showerror("Image Error", f"An error has occured while setting background: {e}")

# --- Dynamic Search Context Function ---
def update_search_context(category_name, fetch_function):
    """Updates the dedicated search button for the current category and runs the default fetch."""
    
    # 1. Update the search button's appearance and action
    search_button.config(
        text=f"Search {category_name}",
        command=lambda: fetch_function(search_var.get())
    )
    
    # 2. Clear the search entry and the text box
    search_var.set("")
    text_box.config(state="normal")
    text_box.delete('1.0', END)
    
    # 3. Run the default fetch function immediately to show all (or first page of) items
    fetch_function()


# --- Data Fetching Functions (All updated to handle URL encoding) ---

def fetch_books(search_term=""):
    """Fetches books from the API, optionally filtered by search term."""
    url = "https://api.potterdb.com/v1/books"
    
    text_box.config(state="normal")
    text_box.delete('1.0', END)
    
    # FIX: URL-encode the search term
    safe_search_term = quote(search_term) 
    
    if search_term:
        # Use filter[title_cont] for case-insensitive contains match
        full_url = f"{url}?filter[title_cont]={safe_search_term}&sort=release_date"
        text_box.insert(END, f"Searching for Books matching: '{search_term}'...\n\n")
    else:
        full_url = f"{url}?sort=release_date"
        text_box.insert(END, "Displaying All Books...\n\n")
        
    try:
        response = requests.get(full_url)
        response.raise_for_status() 
        data = response.json()
        books = data.get('data', [])
        
        if not books:
             text_box.insert(END, "No books found matching your criteria.\n")
             
        for book in books:
            attributes = book.get('attributes', {})
            title = attributes.get('title')
            release_date = attributes.get('release_date')
            pages = attributes.get('pages')
            summary = attributes.get('summary')
            wiki = attributes.get('wiki')
            
            book_info = (
                f"Title: {title}\n"
                f"Release Date: {release_date}\n"
                f"Pages: {pages}\n"
                f"Summary: {summary}\n"
                f"Wiki: {wiki}\n"
                f"\n"
                f"----------\n"
                f"\n"
            )
            text_box.insert(END, book_info)
            
    except requests.exceptions.RequestException as e:
        text_box.insert(END, f"Error fetching data: {e}\n")
    
    text_box.config(state="disabled")
    text_box.place(relx = 0.5, rely = 0.55, anchor=tk.CENTER)


def fetch_movies(search_term=""):
    """Fetches movies from the API, optionally filtered by search term."""
    url = "https://api.potterdb.com/v1/movies"
    
    text_box.config(state="normal")
    text_box.delete('1.0', END)
    
    # FIX: URL-encode the search term
    safe_search_term = quote(search_term)
    
    if search_term:
        # Use filter[title_cont] for case-insensitive contains match
        full_url = f"{url}?filter[title_cont]={safe_search_term}&sort=release_date"
        text_box.insert(END, f"Searching for Movies matching: '{search_term}'...\n\n")
    else:
        full_url = f"{url}?sort=release_date"
        text_box.insert(END, "Displaying All Movies...\n\n")
        
    try:
        response = requests.get(full_url)
        response.raise_for_status() 
        data = response.json()
        movies = data.get('data', [])
        
        if not movies:
             text_box.insert(END, "No movies found matching your criteria.\n")
             
        for movie in movies:
            attributes = movie.get('attributes', {})
            title = attributes.get('title')
            release_date = attributes.get('release_date')
            box_office = attributes.get('box_office')
            budget = attributes.get('budget')
            rating = attributes.get('rating')
            summary = attributes.get('summary')
            trailer = attributes.get('trailer')
            wiki = attributes.get('wiki')
            
            movie_info = (
                f"Title: {title}\n"
                f"Release Date: {release_date}\n"
                f"Box Office: {box_office}\n"
                f"Budget: {budget}\n"
                f"Rating: {rating}\n"
                f"Summary: {summary}\n"
                f"Trailer: {trailer}\n"
                f"Wiki: {wiki}\n"
                f"\n"
                f"----------\n"
                f"\n"
            )
            text_box.insert(END, movie_info)
            
    except requests.exceptions.RequestException as e:
        text_box.insert(END, f"Error fetching data: {e}\n")
    
    text_box.config(state="disabled")
    text_box.place(relx = 0.5, rely = 0.55, anchor=tk.CENTER)


def fetch_characters(search_term=""):
    """Fetches characters from the API, optionally filtered by search term."""
    url = "https://api.potterdb.com/v1/characters"
    
    text_box.config(state="normal")
    text_box.delete('1.0', END)
    
    # FIX: URL-encode the search term
    safe_search_term = quote(search_term)
    
    if search_term:
        # Use filter[name_cont] for searching characters by name
        full_url = f"{url}?filter[name_cont]={safe_search_term}&sort=name"
        text_box.insert(END, f"Searching for Characters matching: '{search_term}'...\n\n")
    else:
        # Limit default display to avoid fetching thousands of results at once
        full_url = f"{url}?page[size]=20&sort=name" 
        text_box.insert(END, "Displaying 20 main Characters (Search above for more)...\n\n")
        
    try:
        response = requests.get(full_url)
        response.raise_for_status() 
        data = response.json()
        characters = data.get('data', [])
        
        if not characters:
             text_box.insert(END, "No characters found matching your criteria.\n")
             
        for character in characters:
            attributes = character.get('attributes', {})
            
            name = attributes.get('name')
            house = attributes.get('house')
            species = attributes.get('species')
            patronus = attributes.get('patronus')
            blood_status = attributes.get('blood_status')
            wiki = attributes.get('wiki')
            
            character_info = (
                f"Name: {name}\n"
                f"House: {house if house else 'N/A'}\n"
                f"Species: {species if species else 'N/A'}\n"
                f"Patronus: {patronus if patronus else 'N/A'}\n"
                f"Blood Status: {blood_status if blood_status else 'N/A'}\n"
                f"Wiki: {wiki}\n"
                f"\n"
                f"----------\n"
                f"\n"
            )
            text_box.insert(END, character_info)
            
    except requests.exceptions.RequestException as e:
        text_box.insert(END, f"Error fetching data: {e}\n")
    
    text_box.config(state="disabled")
    text_box.place(relx = 0.5, rely = 0.55, anchor=tk.CENTER)


def fetch_spells(search_term=""):
    """Fetches spells from the API, optionally filtered by search term."""
    url = "https://api.potterdb.com/v1/spells"
    
    text_box.config(state="normal")
    text_box.delete('1.0', END)
    
    # FIX: URL-encode the search term
    safe_search_term = quote(search_term) 
    
    if search_term:
        # Filter for spells by name
        full_url = f"{url}?filter[name_cont]={safe_search_term}&sort=name" 
        text_box.insert(END, f"Searching for Spells matching: '{search_term}'...\n\n")
    else:
        full_url = f"{url}?sort=name"
        text_box.insert(END, "Displaying All Spells...\n\n")
        
    try:
        response = requests.get(full_url)
        response.raise_for_status() 
        data = response.json()
        spells = data.get('data', [])
        
        if not spells:
             text_box.insert(END, "No spells found matching your criteria.\n")
             
        for spell in spells:
            attributes = spell.get('attributes', {})
            
            name = attributes.get('name')
            category = attributes.get('category')
            effect = attributes.get('effect')
            wiki = attributes.get('wiki')
            
            spell_info = (
                f"Spell: {name}\n"
                f"Category: {category if category else 'N/A'}\n"
                f"Effect: {effect if effect else 'N/A'}\n"
                f"Wiki: {wiki}\n"
                f"\n----------\n\n"
            )
            text_box.insert(END, spell_info)
            
    except requests.exceptions.RequestException as e:
        text_box.insert(END, f"Error fetching data: {e}\n")
    
    text_box.config(state="disabled")
    text_box.place(relx = 0.5, rely = 0.55, anchor=tk.CENTER)


def fetch_potions(search_term=""):
    """Fetches potions from the API, optionally filtered by search term."""
    url = "https://api.potterdb.com/v1/potions"
    
    text_box.config(state="normal")
    text_box.delete('1.0', END)
    
    # FIX: URL-encode the search term
    safe_search_term = quote(search_term)
    
    if search_term:
        # Filter for potions by name
        full_url = f"{url}?filter[name_cont]={safe_search_term}&sort=name"
        text_box.insert(END, f"Searching for Potions matching: '{search_term}'...\n\n")
    else:
        full_url = f"{url}?sort=name"
        text_box.insert(END, "Displaying All Potions...\n\n")
        
    try:
        response = requests.get(full_url)
        response.raise_for_status() 
        data = response.json()
        potions = data.get('data', [])
        
        if not potions:
             text_box.insert(END, "No potions found matching your criteria.\n")
             
        for potion in potions:
            attributes = potion.get('attributes', {})
            
            name = attributes.get('name')
            effect = attributes.get('effect')
            ingredients = attributes.get('ingredients')
            wiki = attributes.get('wiki')
            
            potion_info = (
                f"Potion: {name}\n"
                f"Effect: {effect if effect else 'N/A'}\n"
                f"Ingredients: {ingredients if ingredients else 'N/A'}\n"
                f"Wiki: {wiki}\n"
                f"\n----------\n\n"
            )
            text_box.insert(END, potion_info)
            
    except requests.exceptions.RequestException as e:
        text_box.insert(END, f"Error fetching data: {e}\n")
    
    text_box.config(state="disabled")
    text_box.place(relx = 0.5, rely = 0.55, anchor=tk.CENTER)


# --- Main Window Setup ---

icon = r"Executable Project Code\harry-potter_flaticon.com.png"
mainMenuBackgroundImage = r"Executable Project Code\valerii-siserg-map3.jpg"

main = tk.Tk()
main.title("A Harry Potter Fan's Harry Potter Database Browser")
main.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
main.resizable(0, 0)

# Set Icon
try:
    window_icon = tk.PhotoImage(file=icon)
    main.iconphoto(True, window_icon)
except tk.TclError:
    print("Warning: Could not load window icon.")


# Set Background
set_background(main, mainMenuBackgroundImage, WINDOW_WIDTH, WINDOW_HEIGHT)


# --- Search Bar and Text Box Widgets ---

# Variable to hold the text input from the search bar
search_var = tk.StringVar() 

# Entry widget for the search term
search_entry = tk.Entry(
    main,
    textvariable=search_var, 
    font=("Comic Sans MS", 16),
    width=50
)
search_entry.place(relx=0.5, rely=0.18, anchor=tk.CENTER)

# Dedicated Search button (Its command is set by update_search_context)
search_button = tk.Button(
    main,
    text="Search...", 
    font=("Comic Sans MS", 16),
    background="lightgreen",
    # Initial command is set when a category is clicked
)
search_button.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

# Text Box to display results
text_box = scrolledtext.ScrolledText(
    main,
    wrap = tk.WORD,
    width = 100,
    height = 20,
    font = ("Comic Sans MS", 14)
)
# Place the text box lower to accommodate the search bar
text_box.place(relx = 0.5, rely = 0.55, anchor=tk.CENTER)


# --- Category Buttons (UPDATED COMMANDS) ---

quitBtn = tk.Button(
    main,
    text = "Quit",
    font = ("Comic Sans MS", 20),
    command = main.quit,
    background = "salmon"
)
quitBtn.place(relx = 0.5, rely = 0.925, anchor = tk.CENTER)

spellsBtn = tk.Button(
    main,
    text = "Spells",
    font = ("Comic Sans MS", 20),
    background = "lightblue",
    command = lambda: update_search_context("Spells", fetch_spells) 
)
spellsBtn.place(relx = 0.1, rely = 0.075, anchor = tk.CENTER)

charactersBtn = tk.Button(
    main,
    text = "Characters",
    font = ("Comic Sans MS", 20),
    background = "lightblue",
    command = lambda: update_search_context("Characters", fetch_characters)
)
charactersBtn.place(relx = 0.3, rely = 0.075, anchor = tk.CENTER)

moviesBtn = tk.Button(
    main,
    text = "Movies",
    font = ("Comic Sans MS", 20),
    background = "lightblue",
    command = lambda: update_search_context("Movies", fetch_movies)
)
moviesBtn.place(relx = 0.5, rely = 0.075, anchor = tk.CENTER)

potionsBtn = tk.Button(
    main,
    text = "Potions",
    font = ("Comic Sans MS", 20),
    background = "lightblue",
    command = lambda: update_search_context("Potions", fetch_potions) 
)
potionsBtn.place(relx = 0.7, rely = 0.075, anchor = tk.CENTER)

booksBtn = tk.Button(
    main,
    text = "Books",
    font = ("Comic Sans MS", 20),
    background = "lightblue",
    command = lambda: update_search_context("Books", fetch_books)
)
booksBtn.place(relx = 0.9, rely = 0.075, anchor = tk.CENTER)


# --- Run Main Loop ---
main.mainloop()