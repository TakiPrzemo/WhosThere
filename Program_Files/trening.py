import face_recognition
import os
import yaml
import tkinter as tk
from tkinter import messagebox

if __name__ == "__main__":
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