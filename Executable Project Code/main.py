import tkinter as tk
from tkinter import scrolledtext, END
# Note: You can typically omit 'from tkinter import *' if you use 'tk.' prefix
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

icon = r"Executable Project Code\harry-potter_flaticon.com.png"

main = tk.Tk()
main.title("A Harry Potter Fan's Harry Potter Database Browser")
main.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
main.resizable(0, 0)

window_icon = tk.PhotoImage(file=icon)
main.iconphoto(True, window_icon)

mainMenuBackgroundImage = r"Executable Project Code\valerii-siserg-map3.jpg"

set_background(main, mainMenuBackgroundImage, WINDOW_WIDTH, WINDOW_HEIGHT)

text_box = scrolledtext.ScrolledText(
    main,
    wrap = tk.WORD,
    width = 100,
    height = 20,
    font = ("Comic Sans MS", 14)
)

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
    background = "lightblue"
)
spellsBtn.place(relx = 0.1, rely = 0.075, anchor = tk.CENTER)

charactersBtn = tk.Button(
    main,
    text = "Characters",
    font = ("Comic Sans MS", 20),
    background = "lightblue"
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

main.mainloop()