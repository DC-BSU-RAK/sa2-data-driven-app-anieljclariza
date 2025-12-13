import tkinter as tk
from tkinter import scrolledtext, END
# Note: You can typically omit 'from tkinter import *' if you use 'tk.' prefix
import requests
from PIL import Image, ImageTk
import os

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

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
    url = "https://api.potterdb.com/v1/books"
    
    text_box.delete('1.0', END)
    text_box.insert(END, "Fetching ALL book attributes from PotterDB...\n")
    
    try:
        # Fetching a small page size (e.g., 5) to keep the text box manageable
        response = requests.get(f"{url}?sort=number&page[size]=5") 
        response.raise_for_status() 
        
        data = response.json()
        books = data.get('data', [])
        
        text_box.delete('1.0', END)
        text_box.insert(END, "--- Harry Potter Books (Displaying All Attributes) ---\n\n")
        
        # Outer loop: Iterates through each Book object
        for book in books:
            # Corrected: Key is 'attributes'
            attributes = book.get('attributes', {})
            
            # Use 'id' from the main book object for a unique identifier
            book_id = book.get('id', 'N/A')
            
            # Start of the book block
            text_box.insert(END, f"========== BOOK ID: {book_id} ==========\n")
            
            # Inner loop: Iterates through ALL key-value pairs in the 'attributes' dictionary
            # .items() returns both the key (name) and the value (data)
            for name, value in attributes.items():
                
                # Format the attribute name (key) for better readability
                display_name = name.replace('_', ' ').title()
                
                # Handle potentially long or complex values (like HTML strings) by showing them partially
                if isinstance(value, str) and len(value) > 70:
                    display_value = value[:70] + "..."
                else:
                    display_value = value
                    
                # Insert the formatted key and value
                attribute_info = f"  {display_name}: {display_value}\n"
                text_box.insert(END, attribute_info)
            
            # Separator between books
            text_box.insert(END, "========================================\n\n")

    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching data: {e}"
        text_box.delete('1.0', END)
        text_box.insert(END, error_message)
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        text_box.delete('1.0', END)
        text_box.insert(END, error_message)
        
    # Place the text box (If it wasn't placed in the main setup)
    text_box.place(relx = 0.5, rely = 0.5, anchor=tk.CENTER)

# Note: Remember to call this function via your Tkinter button command
# booksBtn = tk.Button(..., command=fetch_books)
        
# --- Main Application Setup (No changes needed, but kept for context) ---
icon = r"Executable Project Code\harry-potter_flaticon.com.png"

main = tk.Tk()
main.title("A Harry Potter Fan's Harry Potter Database Browser")
main.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
main.resizable(0, 0)

# Check if icon file exists before setting it
if os.path.exists(icon):
    window_icon = tk.PhotoImage(file=icon)
    main.iconphoto(True, window_icon)
else:
    print(f"Warning: Icon file not found at '{icon}'. Skipping icon setting.")


mainMenuBackgroundImage = r"Executable Project Code\valerii-siserg-map3.jpg"

set_background(main, mainMenuBackgroundImage, WINDOW_WIDTH, WINDOW_HEIGHT)

# The text box should be placed after its creation, usually before mainloop
text_box = scrolledtext.ScrolledText(
    main,
    wrap = tk.WORD,
    width = 90,
    height = 45,
    font = ("Comic Sans MS", 12)
)
text_box.insert(END, "Press 'Books' to load data...")

# --- Buttons (No changes needed, but kept for context) ---
quitBtn = tk.Button(
    main,
    text="Quit",
    font=("Comic Sans MS", 20),
    command=main.quit, # Use main.quit() for cleaner exit
    background="salmon"
)
quitBtn.place(relx = 0.5, rely = 0.85, anchor = tk.CENTER)

spellsBtn = tk.Button(
    main,
    text="Spells",
    font=("Comic Sans MS", 20),
    background = "lightblue"
)
spellsBtn.place(relx = 0.5, rely = 0.6, anchor = tk.CENTER)

charactersBtn = tk.Button(
    main,
    text="Characters",
    font=("Comic Sans MS", 20),
    background = "lightblue"
)
charactersBtn.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

moviesBtn = tk.Button(
    main,
    text="Movies",
    font=("Comic Sans MS", 20),
    background = "lightblue"
)
moviesBtn.place(relx = 0.35, rely = 0.5, anchor = tk.CENTER)

potionsBtn = tk.Button(
    main,
    text="Potions",
    font=("Comic Sans MS", 20),
    background = "lightblue"
)
potionsBtn.place(relx = 0.5, rely = 0.4, anchor = tk.CENTER)

booksBtn = tk.Button(
    main,
    text="Books",
    font=("Comic Sans MS", 20),
    background = "lightblue",
    command=fetch_books # Link to the corrected function
)
booksBtn.place(relx = 0.65, rely = 0.5, anchor = tk.CENTER)

main.mainloop()