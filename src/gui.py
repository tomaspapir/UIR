import os
from tkinter import *
from tkinter import messagebox

from PIL import Image
from knn import nearest_neighbours, open_file


# executing after clicking the classify button
# saves the number image and classifies it for the model
def classify_callback(canvas, model):
    filename = "image"
    canvas.postscript(file=filename + '.eps')
    img = Image.open(filename + '.eps')
    img = img.resize((28, 28))
    img.save(filename + '.png', 'png')
    img.close()
    os.remove(filename + '.eps')
    pixel_count_switch = False

    model_file = open_file(model + '.csv')
    first_line = next(model_file)

    if "pixel" in first_line[1]:
        pixel_count_switch = True

    number = nearest_neighbours(model_file, filename + ".png", 5, pixel_count_switch)
    messagebox.showinfo("Odhadnute cislo", "Nakreslene cislo je: " + str(number))
    clear_callback(canvas)


# painting on the canvas
def paint(event, canvas):
    x1, y1, = (event.x - 1), (event.y - 1)
    x2, y2, = (event.x + 20), (event.y + 20)
    canvas.create_rectangle(x1, y1, x2, y2, fill="#FFFFFF", outline="#FFFFFF")


# clears the canvas
def clear_callback(w):
    w.delete('all')
    w.create_rectangle(2, 2, 368, 368, outline="#000000", fill="#000000")


# creation of the gui with the number canvas and buttons
def create_gui(model):
    canvas_width = 368
    canvas_height = 368

    window = Tk()
    window.title("Prosim nakreslete pozadovane cislo")
    window.geometry("640x480")
    window.resizable(False, False)

    bottom_frame = Frame(window)
    bottom_frame.pack(side=BOTTOM)

    w = Canvas(window, width=canvas_width, height=canvas_height)
    w.create_rectangle(2, 2, 368, 368, outline="#000000", fill="#000000")

    classify_button = Button(bottom_frame, text="Klasifikovat", command=lambda: classify_callback(w, model))
    classify_button.config(height=2, width=10)
    classify_button.pack(side=LEFT)

    clear_button = Button(bottom_frame, text="Smazat platno", command=lambda: clear_callback(w))
    clear_button.config(height=2, width=10)
    clear_button.pack(side=RIGHT)

    w.pack(side=TOP)
    w.bind("<B1-Motion>", lambda event, obj=w: paint(event, w))

    window.mainloop()

