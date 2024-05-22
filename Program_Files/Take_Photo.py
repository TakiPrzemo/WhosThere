import cv2 as cv
import re
import tkinter as tk
from tkinter import *
from tkinter import messagebox

import face_recognition
from PIL import Image
from PIL import ImageTk
import os


def callback() -> None:
    camera.release()
    root.destroy()


def save_photo(name: str, photo_counting: [int, int], max_index: int, first_index: int, photo_dir: str,
               frame_to_save, widget, window, label, button) -> None:
    button.config(state=DISABLED)
    file_name = f"{name.capitalize()}_{photo_counting[0]}.jpg"

    try:
        face_recognition.face_encodings(frame_to_save)[0]
    except IndexError:
        # print("Photo is too blurry, repeat the shot!")
        show_widget(widget, label, window, "Photo is too blurry, repeat the shot!", color="red")
        button.config(state=NORMAL)
    else:
        save_path = os.path.join(photo_dir, file_name)

        cv.imwrite(save_path, frame_to_save)
        # print(f"Photo saved ({photo_counting[1] + 1}/{MAX_INDEX + 1}): {file_name}")
        show_widget(widget, label, window, "Photo saved", color="green")
        photo_counting[0] += 1

        if photo_counting[1] < max_index:
            photo_counting[1] += 1

        if photo_counting[0] > max_index:
            photo_counting[0] = first_index
        else:
            photo_counting[0] += first_index

        button.config(state=NORMAL)


def delete_photos(name: str, photo_counting: [int, int], first_index: int, photo_dir: str) -> None:
    if (photo_counting[1] == 0):
        tk.messagebox.showinfo("Delete photos", "No photos to delete")
    else:
        result = tk.messagebox.askokcancel("Delete photos",
                                           f"Do you want to delete all photos assigned to user: {name}")
        if (result):
            for i in range(first_index, photo_counting[1]):
                path = os.path.join(photo_dir, f"{name.capitalize()}_{i}.jpg")
                if (os.path.exists(path)):
                    os.remove(path)
            tk.messagebox.showinfo("Delete photos", f"Deleted {photo_counting[1]} photos")
            photo_counting[:] = [first_index, first_index]


def show_widget(widget, label, window, message: str, color: str) -> None:
    widget.pack()
    widget.config(width=window.winfo_width(), height=window.winfo_width() // 20)
    label.config(text=message, bg=color)
    window.update()
    widget.after(1000, widget.pack_forget())


if __name__ == '__main__':

    DIR = "Photos"
    FIRST_INDEX = 0
    MAX_INDEX = 9
    user_photo_data = [FIRST_INDEX, FIRST_INDEX]
    person_name = input("Submit user's name: ")
    frame_raw = None

    root = tk.Tk()
    root.title("Manage users")
    root.protocol("WM_DELETE_WINDOW", callback)

    main_window = Frame(root)
    main_window.pack(side=TOP, fill=BOTH)

    left_frame = Frame(main_window, width=200)
    left_frame.pack(side=LEFT, fill=Y)
    left_frame.pack_propagate(False)
    # do left_frame dodajemy przyciski i inne elementy interfejsu

    right_frame = Frame(main_window, background="red")
    right_frame.pack(side=RIGHT, expand=TRUE, fill=BOTH)

    save_info = tk.Frame(root)
    save_info.pack_propagate(False)
    save_info.pack(side=BOTTOM, expand=TRUE, fill=BOTH)

    save_info_text = tk.Label(save_info, text="Photo Saved", bg="green", fg="white", font=("Arial", 16, "bold"))
    save_info_text.pack(expand=TRUE, fill=BOTH)

    save_info.pack_forget()

    # przyciski jako testowe elementy (do usunięcia)
    button_1 = tk.Button(left_frame,
                         text="Test zapisz",
                         command=lambda: save_photo(person_name, user_photo_data, MAX_INDEX, FIRST_INDEX, DIR,
                                                    frame_raw, save_info, root, save_info_text, button_1)
                         )
    button_1.pack()

    button_2 = tk.Button(left_frame,
                         text="Usun",
                         command=lambda: delete_photos(person_name, user_photo_data, FIRST_INDEX, DIR)
                         )
    button_2.pack()

    button_3 = tk.Button(left_frame,
                         text="test hide",
                         command=lambda: show_widget(save_info, save_info_text, root, "test", "blue")
                         )
    button_3.pack()
    # ==========

    camera_preview = tk.Label(right_frame)
    camera_preview.pack()

    # if do ustawiania indeksowania pliku

    # ======================================

    if any(file.startswith(person_name) for file in os.listdir(DIR)):
        existing_files = []
        for file in os.listdir(DIR):
            if re.match(f"{person_name}_[0-9]+\.jpg", file, re.IGNORECASE):
                existing_files.append(file)
        index_list = []
        for file in existing_files:
            number = re.search(r'\d+', file)
            if number:
                number_str = number.group()
                index_list.append(int(number_str))

        user_photo_data[1] = max(index_list) + 1
        user_photo_data[0] = user_photo_data[1]

        if user_photo_data[0] >= MAX_INDEX:
            user_photo_data[0] = FIRST_INDEX
            user_photo_data[1] = MAX_INDEX
        else:
            user_photo_data[0] = user_photo_data[0] + FIRST_INDEX

    else:
        user_photo_data[0] = FIRST_INDEX
        user_photo_data[1] = FIRST_INDEX

    # ======================================

    camera = cv.VideoCapture(0)

    if not (camera.isOpened()):
        print("ERR: camera not connected")
    else:
        while True:
            ret, frame_raw = camera.read()

            if not ret:
                break

            frame_arr = cv.cvtColor(frame_raw, cv.COLOR_BGR2RGB)
            frame = Image.fromarray(frame_arr)
            image = ImageTk.PhotoImage(frame)
            camera_preview.configure(image=image)

            root.update()

    camera.release()
    root.mainloop()
