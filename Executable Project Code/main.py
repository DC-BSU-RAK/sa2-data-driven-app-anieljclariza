import tkinter as tk
from tkinter import *
import requests

main = tk.Tk()

icon = tk.PhotoImage(file=r"Executable Project Code\harry-potter_flaticon.com.png")

main.title("A Harry Potter fan's Harry Potter Database")
main.iconphoto(True, icon)
main.geometry("800x600")
main.resizable(0,0)

response = requests.get("https://api.potterdb.com/v1/characters?filter[name_cont]=Weasley")

if response.status_code == 200:
    data = response.json()
    
    characters = data.get("data", [])
    
    print(f"Total characters: {len(characters)}")
    
    for c in characters:
        attrs = c["attributes"]
        print(f"Name: {attrs.get('name')}")
        print(f"House: {attrs.get('house')}")
        print(f"Species: {attrs.get('species')}")
        print("===")
else:
    print("Error: ", response.status_code)
