import tkinter as tk
from tkinter import *
import requests

main = tk.Tk()

icon = tk.PhotoImage(file=r"Executable Project Code\harry-potter_flaticon.com.png")

main.title("A Harry Potter fan's Harry Potter Database")
main.iconphoto(True, icon)
main.geometry("1024x768")
main.resizable(0,0)

response = requests.get("https://api.potterdb.com/v1/characters?filter[name_cont]=Harry James Potter")
    
def button():
    if response.status_code == 200:
        data = response.json()
    
    characters = data.get("data", [])
    
    output = f"Total characters: {len(characters)}"
    
    for c in characters:
        attrs = c["attributes"]
        
        output += (
            f"Name: {attrs.get('name')}"
            f"House: {attrs.get('house')}"
            f"Species: {attrs.get('species')}"
            f"==="
        )
    
    hpLabel.config(text={output})

pressMe = Button(main, text="Harry James Potter", command=lambda:button())
pressMe.pack(expand=True, fill=BOTH)

hpLabel = Label(main, text="")
hpLabel.pack(side=BOTTOM ,expand=True, fill=BOTH)

mainloop()