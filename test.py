import tkinter as tk
from tkinter import scrolledtext, END
import requests
import json

# --- Constants ---
POTTERDB_API_URL = "https://api.potterdb.com/v1/books" 

def fetch_and_display_books():
    """Fetches book data from PotterDB API and displays it in the Tkinter Text widget."""
    
    # 1. Clear previous content
    results_text.delete('1.0', END)
    results_text.insert(END, "Fetching data from PotterDB...")

    try:
        # 2. Make the API Request
        # We use a filter to get a manageable amount of data (e.g., the first 5 books)
        response = requests.get(f"{POTTERDB_API_URL}?page[size]=5&sort=number")
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # 3. Parse the JSON Response
        data = response.json()
        
        # Clear the "Fetching..." message
        results_text.delete('1.0', END)
        results_text.insert(END, "--- PotterDB Book Details (First 5) ---\n\n")

        # 4. Extract and Format Data
        books = data.get('data', [])
        
        for book in books:
            # PotterDB uses the JSON:API format. Attributes are nested under 'attributes'.
            attributes = book.get('attributes', {})
            
            # Extract key details
            number = attributes.get('number', 'N/A')
            title = attributes.get('title', 'N/A')
            release_date = attributes.get('release_date', 'N/A')
            pages = attributes.get('pages', 'N/A')
            
            # Format the output string
            book_info = (
                f"Book #{number}: {title}\n"
                f"  Release Date: {release_date}\n"
                f"  Pages: {pages}\n"
                f"----------------------------------------\n"
            )
            
            # 5. Insert data into the Tkinter Text widget
            results_text.insert(END, book_info)

    except requests.exceptions.RequestException as e:
        # Handle connection errors or bad responses
        error_message = f"\nError fetching data: {e}"
        results_text.delete('1.0', END) # Clear previous content
        results_text.insert(END, error_message)
        
    except json.JSONDecodeError:
        error_message = "\nError: Could not decode JSON response."
        results_text.delete('1.0', END)
        results_text.insert(END, error_message)
    except Exception as e:
        error_message = f"\nAn unexpected error occurred: {e}"
        results_text.delete('1.0', END)
        results_text.insert(END, error_message)

# --- Tkinter GUI Setup ---

# Initialize the main window
root = tk.Tk()
root.title("PotterDB API Viewer")
root.geometry("600x400") # Set a default size

# Create a button to trigger the data fetch
fetch_button = tk.Button(
    root, 
    text="Fetch Harry Potter Book Details", 
    command=fetch_and_display_books, # Link the button to the function
    font=('Arial', 12, 'bold')
)
fetch_button.pack(pady=10)

# Create a ScrolledText widget for displaying results 
# (This is better than a simple Label/Text as API responses can be long)
results_text = scrolledtext.ScrolledText(
    root, 
    wrap=tk.WORD, # Wrap lines at word boundaries
    width=70, 
    height=15, 
    font=('Courier New', 10)
)
results_text.pack(padx=10, pady=10)

# Add an initial message
results_text.insert(END, "Click the button to load book details...")

# Start the Tkinter event loop
root.mainloop()