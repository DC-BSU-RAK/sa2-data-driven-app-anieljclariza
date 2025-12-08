import tkinter as tk
from tkinter import *
import requests

main = tk.Tk()

icon = tk.PhotoImage(file=r"Executable Project Code\harry-potter_flaticon.com.png")

main.title("A Harry Potter fan's Harry Potter Database")
main.iconphoto(True, icon)
main.geometry("1024x768")
main.resizable(0,0)

response = requests.get("https://api.potterdb.com/v1/characters?filter[house]=gryffindor")
    
def button():
    if response.status_code == 200:
        data = response.json()
    
    characters = data.get("data", [])
    
    output = f"Total characters: {len(characters)}"
    
    for c in characters:
        attrs = c["attributes"]
        
        output += (
            f"Name: {attrs.get('name')}\n"
            f"House: {attrs.get('house')}\n"
            f"Species: {attrs.get('species')}\n"
            f"===\n"
        )
    
    hpLabel.config(text={output})

pressMe = Button(main, text="Click me", command=lambda:button())
pressMe.pack(fill=BOTH)

hpLabel = Label(main, text="")
hpLabel.pack(side=BOTTOM, fill=BOTH, expand=True)

mainloop()