import tkinter as tk # for gui and shorcut
from tkinter import scrolledtext, END # for scrollbar and END positions
import requests # for fetching data from Database and API
from PIL import Image, ImageTk
import os

# Set window width and window height
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# This function sets the background, accepting respective parameters
def set_background(window, image_path, width, height):
    try:
        img = Image.open(image_path)
        
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

# This fetches the characters category from the database
def fetch_characters():
    text_box.config(state="normal")
    
    entry_value = entry.get().strip()
    
    url = f"https://api.potterdb.com/v1/characters?filter[name_cont]={entry_value}"
    
    text_box.delete('1.0', END)
    
    response = requests.get(f"{url}&sort=name") 
    
    data = response.json()
    characters = data.get('data', [])
    
    for character in characters:
        attributes = character.get('attributes',  {})
        
        name = attributes.get('name',)
        born = attributes.get('born')
        died = attributes.get('died')
        gender = attributes.get('gender')
        species = attributes.get('species')
        nationality = attributes.get('nationality')
        blood_status = attributes.get('blood_status')
        house = attributes.get('house')
        eye_color = attributes.get('eye_color')
        hair_color = attributes.get('hair_color')
        wiki = attributes.get('wiki')
        
        character_info = (
            f"Name: {name}\n"
            
            f"Born: {born}\n"
            
            f"Died: {died}\n"
            
            f"Gender: {gender}\n"
            
            f"Species: {species}\n"
            
            f"Nationality: {nationality}\n"
            
            f"Blood Status: {blood_status}\n"
            
            f"House: {house}\n"
            
            f"Eye Color: {eye_color}\n"
        
            f"Hair Color: {hair_color}\n"
            
            f"Wiki: {wiki}\n"
            
            f"\n"
            
            f"----------\n"
            
            f"\n"
        )
        text_box.insert(END, character_info)
    text_box.config(state="disabled")
    text_box.place(relx = 0.5, rely = 0.5, anchor=tk.CENTER)

# This fetches the spells category from the database
def fetch_spells():
    text_box.config(state="normal")
    
    entry_value = entry.get().strip()
    
    url = f"https://api.potterdb.com/v1/spells?filter[name_cont]={entry_value}"
    
    text_box.delete('1.0', END)
    
    response = requests.get(f"{url}&sort=name") 
    
    data = response.json()
    spells = data.get('data', [])
    
    for spell in spells:
        attributes = spell.get('attributes',  {})
        
        name = attributes.get('name',)
        effect = attributes.get('effect')
        category = attributes.get('category')
        light = attributes.get('light')
        wiki = attributes.get('wiki')
        
        character_info = (
            f"Name: {name}\n"
            
            f"Effect: {effect}\n"
            
            f"Category: {category}\n"
            
            f"Light Color: {light}\n"
            
            f"Wiki: {wiki}\n"
            
            f"\n"
            
            f"----------\n"
            
            f"\n"
        )
        text_box.insert(END, character_info)
    text_box.config(state="disabled")
    text_box.place(relx = 0.5, rely = 0.5, anchor=tk.CENTER)

# This fetches the potions category from the database  
def fetch_potions():
    text_box.config(state="normal")
    
    entry_value = entry.get().strip()
    
    url = f"https://api.potterdb.com/v1/potions?filter[name_cont]={entry_value}"
    
    text_box.delete('1.0', END)
    
    response = requests.get(f"{url}&sort=name") 
    
    data = response.json()
    potions = data.get('data', [])
    
    for potion in potions:
        attributes = potion.get('attributes',  {})
        
        name = attributes.get('name',)
        difficulty = attributes.get('difficulty')
        effect = attributes.get('effect')
        ingredients = attributes.get('ingredients')
        characteristics = attributes.get('characteristics')
        wiki = attributes.get('wiki')
        
        character_info = (
            f"Name: {name}\n"
            
            f"Difficulty: {difficulty}\n"
            
            f"Effect: {effect}\n"
            
            f"Ingredients: {ingredients}\n"
            
            f"Characteristics: {characteristics}\n"
            
            f"Wiki: {wiki}\n"
            
            f"\n"
            
            f"----------\n"
            
            f"\n"
        )
        text_box.insert(END, character_info)
    text_box.config(state="disabled")
    text_box.place(relx = 0.5, rely = 0.5, anchor=tk.CENTER)

# This fetches the books category from the database
def fetch_books():
    text_box.config(state="normal")
    url = "https://api.potterdb.com/v1/books"
    
    text_box.delete('1.0', END)
    
    response = requests.get(f"{url}?sort=release_date") 
    
    data = response.json()
    books = data.get('data', [])
    
    for book in books:
        attributes = book.get('attributes',  {})
        
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
    text_box.config(state="disabled")
    text_box.place(relx = 0.5, rely = 0.5, anchor=tk.CENTER)

# This fetches the movies category from the database    
def fetch_movies():
    text_box.config(state="normal")
    url = "https://api.potterdb.com/v1/movies"
    
    text_box.delete('1.0', END)
    
    response = requests.get(f"{url}?sort=release_date") 
    
    data = response.json()
    movies = data.get('data', [])
    
    for movie in movies:
        attributes = movie.get('attributes',  {})
        
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
    text_box.config(state="disabled")
    text_box.place(relx = 0.5, rely = 0.5, anchor=tk.CENTER)

# icon location
icon = r"Executable Project Code\harry-potter_flaticon.com.png"

# Window creation
main = tk.Tk()
main.title("A Harry Potter Fan's Harry Potter Database Browser")
main.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
main.resizable(0, 0)

# Window icon assignment
window_icon = tk.PhotoImage(file=icon)
main.iconphoto(True, window_icon)

# Set background image
mainMenuBackgroundImage = r"Executable Project Code\valerii-siserg-map3.jpg"
set_background(main, mainMenuBackgroundImage, WINDOW_WIDTH, WINDOW_HEIGHT)

# This creates the text box
text_box = scrolledtext.ScrolledText(
    main,
    wrap = tk.WORD,
    width = 100,
    height = 20,
    font = ("Comic Sans MS", 14)
)

# This creates the entry field
entry = tk.Entry(
    main,
    font = ("Comic Sans MS", 14)
)
entry.place(relx=0.25, rely=0.925, anchor="center")

# This creates the instructions label
instructions = tk.Label(
    main,
    text = "Enter character, spell, or potion\nname on search box on the left side and press\nrespective category button above to search.",
    font = ("Consolas MS", 14)
)
instructions.place(relx = 0.75, rely = 0.925, anchor = "center")

# BUTTONS
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
    command = fetch_spells
)
spellsBtn.place(relx = 0.1, rely = 0.075, anchor = tk.CENTER)

charactersBtn = tk.Button(
    main,
    text = "Characters",
    font = ("Comic Sans MS", 20),
    background = "lightblue",
    command = fetch_characters
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
    background = "lightblue",
    command = fetch_potions
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

# run mainloop to start program
main.mainloop()