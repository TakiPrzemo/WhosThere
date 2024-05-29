import face_recognition
import cv2 as cv
import numpy as np
import yaml
import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
import os


def face_confidence(face_distance, face_match_threshold):
    range = 1.0 - face_match_threshold
    linear_val = (1.8 * face_distance) / (range * 2.0)
    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + "%"
    else:
        value = (linear_val + ((1.0 - linear_val) * pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + "%"

def grantAccess():
    if (os.name == "nt"):
        os.system('mspaint Open.jpg')
    else:
        os.system('eog Open.jpg')


def callback() -> None:
    camera.release()
    root.destroy()


if __name__ == '__main__':
    with open('known_faces.yml', 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        known_face_names = data['names']
        known_face_encodings = np.array(data['encodings'])

    face_loc = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    root = tk.Tk()
    root.title("Who's there")
    root.protocol("WM_DELETE_WINDOW", callback)

    left_frame = LabelFrame(root, width=200)
    left_frame.pack(side=LEFT, fill=Y)
    left_frame.pack_propagate(False)
    # do left_frame dodajemy przyciski i inne elementy interfejsu

    # przyciski jako testowe elementy (do usunięcia)
    button_1 = tk.Button(left_frame, text="Przycisk 1")
    button_1.pack()

    button_2 = tk.Button(left_frame, text="Przycisk 2")
    button_2.pack()

    right_frame = Frame(root)
    right_frame.pack(side=RIGHT, expand=TRUE, fill=BOTH)

    camera_preview = tk.Label(right_frame)
    camera_preview.pack()

    exit_button = tk.Button(left_frame, text="Wyjście", command=callback)
    exit_button.pack(side=BOTTOM, pady=10)

    found = False

    camera = cv.VideoCapture(0)

    while True:

        ret, frame = camera.read()

        if not ret:
            break

        if process_this_frame:
            small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv.cvtColor(small_frame, cv.COLOR_BGR2RGB)

            face_loc = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_loc)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "?????"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    confidence = face_confidence(face_distances[best_match_index], 0.8)
                    face_names.append(f'{name[:-2]} {confidence}')
                    if not found:
                        grantAccess()
                        found = True
                else:
                    face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), text in zip(face_loc, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            if text.startswith("?????"):
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)

            cv.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv.FILLED)
            cv.putText(frame, text, (left + 6, bottom - 6), cv.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)

        frame_arr = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = Image.fromarray(frame_arr)
        image = ImageTk.PhotoImage(frame)
        camera_preview.configure(image=image)

        root.update()

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv.destroyAllWindows()
    root.mainloop()
