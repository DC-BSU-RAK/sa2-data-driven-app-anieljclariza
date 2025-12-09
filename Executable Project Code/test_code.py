import tkinter as tk # for gui
from tkinter import * # import everything from tkinter
import requests # for api
from PIL import Image, ImageTk # for setting background image

main = tk.Tk()

window_icon = tk.PhotoImage(file=r"Executable Project Code\harry-potter_flaticon.com.png")

background_image = Image.open(r"Executable Project Code\valerii-siserg-map3.jpg")
background_image = background_image.resize((900, 700))
background_photo = ImageTk.PhotoImage(background_image)

main.title("A Harry Potter fan's Harry Potter Database Program")
main.iconphoto(True, icon)
main.geometry("900x700")
main.config()
main.resizable(0,0)

onlyFrame = Frame(main)
onlyFrame.place(relwidth=1, relheight=1)

backgroundLabel = Label(onlyFrame)
backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)
backgroundLabel.config(image=background_photo)

def switch_frame(frame):
    frame.tkraise()

switch_frame(onlyFrame)

mainloop()