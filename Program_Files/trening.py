import face_recognition
import os
import yaml
from tkinter import messagebox
import tkinter as tk
import tkinter.font as font
import time

def train():
    DIR = r'Photos'
    known_face_names = []
    known_face_encodings = []

    try:
        for file in os.listdir(DIR):
            if (file[-4:] == ".jpg"):
                image_path = os.path.join(DIR, file)
                name = os.path.splitext(os.path.basename(image_path))[0]
                image = face_recognition.load_image_file(image_path)
                face_encoding = face_recognition.face_encodings(image)[0]
                known_face_encodings.append(face_encoding.tolist())
                known_face_names.append(name)

        with open('known_faces.yml', 'w') as f:
            yaml.dump({'names': known_face_names, 'encodings': known_face_encodings}, f)
            messagebox.showinfo("Success", "Photos saved successfully!")
    except IndexError:
        messagebox.showerror("Error", "Photos are too blurry, please repeat the series!")
    r.destroy()

def exit_program():
    r.destroy()

r = tk.Tk()
r.title('Training')
myFont = font.Font(size=60)

button_process = tk.Button(r, text='Process pictures', width=20, height=5, command=train)
button_process['font'] = myFont
button_process.pack(padx=10, pady=10)

button_exit = tk.Button(r, text='Exit', width=20, height=5, command=exit_program)
button_exit['font'] = myFont
button_exit.pack(padx=10, pady=10)

def colorLoop():
    colorIndex = int(time.time() * 100)%300
    r = max(-abs((colorIndex%300)-100)+100,0)*255//100
    g = max(-abs(((colorIndex+100)%300)-100)+100,0)*255//100
    b = max(-abs(((colorIndex+200)%300)-100)+100,0)*255//100
    return f'#{r:02x}{g:02x}{b:02x}'

def ButtonUpdate():
    color = colorLoop()
    button_process.config(activeforeground=color, fg=color)
    button_exit.config(activeforeground=color, fg=color)
    r.after(50, ButtonUpdate)

ButtonUpdate()

r.mainloop()