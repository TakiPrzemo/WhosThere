import cv2 as cv
import re
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import face_recognition
from PIL import Image
from PIL import ImageTk
import os
from typing import Tuple, Union, List


def callback() -> None:
    camera.release()
    root.destroy()


def save_photo(name: str, photo_counting: [int, int], max_index: int, first_index: int, photo_dir: str,
               frame_to_save, widget, window, label, button) -> None:
    button.config(state=DISABLED)
    if (name == ""):
        tk.messagebox.showinfo("Save photo", "Enter username")
    else:
        if not(os.path.exists(os.path.join(photo_dir, f"{name}_0.jpg"))):
            result = tk.messagebox.askokcancel("Save photo",
                                               f"Do you want to add new user : {name}")
        if (os.path.exists(os.path.join(photo_dir, f"{name}_0.jpg")) or result):
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
                    update_photo_counter(photo_counter_label, photo_counting[0], MAX_INDEX)
                    photo_counting[1] += 1

                if photo_counting[0] > max_index:
                    update_photo_counter(photo_counter_label, photo_counting[0], MAX_INDEX)
                    photo_counting[0] = first_index
                else:
                    update_photo_counter(photo_counter_label, photo_counting[0], MAX_INDEX)
                    photo_counting[0] += first_index
                    
                    
                
                
                

    button.config(state=NORMAL)


def delete_photos(name: str, photo_counting: [int, int], first_index: int, photo_dir: str) -> None:
    if (name == ""):
        tk.messagebox.showinfo("Delete photos", "Enter username")
    elif (photo_counting[1] == 0):
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
            update_photo_counter(photo_counter_label, photo_counting[0], MAX_INDEX)


def show_widget(widget, label, window, message: str, color: str) -> None:
    widget.pack()
    widget.config(width=window.winfo_width(), height=window.winfo_width() // 20)
    label.config(text=message, bg=color)
    window.update()
    widget.after(1000, widget.pack_forget())


def get_existing_names(photo_path: str) -> Union[Tuple[str, ...], Tuple[None]]:
    res = ()
    for file_name in os.listdir(photo_path):
        if (file_name[-4:] == ".jpg"):
            if (file_name[:-6] not in res):
                res += (file_name[:-6],)
    return res


def count_users(name: str, photo_dir: str, max_index: int, first_index: int) -> List[int]:
    res = [0, 0]
    if(name != ""):
        if any(file.startswith(name) for file in os.listdir(photo_dir)):
            existing_files = []
            for file in os.listdir(photo_dir):
                if re.match(f"{name}_[0-9]+\.jpg", file, re.IGNORECASE):
                    existing_files.append(file)
            index_list = [-1]
            for file in existing_files:
                number = re.search(r'\d+', file)
                if number:
                    number_str = number.group()
                    index_list.append(int(number_str))

            res[1] = max(index_list) + 1
            res[0] = res[1]

            if res[0] >= max_index:
                res[0] = first_index
                res[1] = max_index
            else:
                res[0] = res[0] + first_index

        else:
            res[0] = first_index
            res[1] = first_index
    else:
        res = [first_index,first_index]

    return res

def update_photo_counter(label: tk.Label, current_count: int, max_count: int) -> None:
    label.config(text=f"{current_count}/{max_count + 1}")

if __name__ == '__main__':

    DIR = "Photos"
    FIRST_INDEX = 0
    MAX_INDEX = 9
    user_photo_data = [0,0]
    frame_raw = None
    names_set = get_existing_names(DIR)
    person_name = ""

    root = tk.Tk()
    root.title("Manage users")
    root.protocol("WM_DELETE_WINDOW", callback)

    main_window = Frame(root)
    main_window.pack(side=TOP, fill=BOTH)

    left_frame = Frame(main_window, width=200)
    left_frame.pack(side=LEFT, fill=Y)
    left_frame.pack_propagate(False)
    # do left_frame dodajemy przyciski i inne elementy interfejsu

    right_frame = Frame(main_window)
    right_frame.pack(side=RIGHT, expand=TRUE, fill=BOTH)

    save_info = tk.Frame(root)
    save_info.pack_propagate(False)
    save_info.pack(side=BOTTOM, expand=TRUE, fill=BOTH)

    save_info_text = tk.Label(save_info, text="Photo Saved", bg="green", fg="white", font=("Arial", 16, "bold"))
    save_info_text.pack(expand=TRUE, fill=BOTH)

    save_info.pack_forget()


    def update_suggestions(*args) -> None:
        if (user_name.get() == ""):
            name_suggestions['values'] = names_set
        else:
            newvalues = [i for i in names_set if user_name.get() in i]
            name_suggestions['values'] = newvalues

    user_name = tk.StringVar()
    user_name.trace('w', update_suggestions)

    name_suggestions = ttk.Combobox(left_frame, width=22, textvariable=user_name)
    name_suggestions.grid(row=0, column=0)
    name_suggestions['values'] = names_set

    name_suggestions.pack()

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
                         command=lambda: show_widget(save_info, save_info_text, root, "test " + person_name + str(user_photo_data[0]) + str(user_photo_data[1]), "blue")
                         )
    button_3.pack()
    # ==========
    
    photo_counter_label = tk.Label(left_frame, text="0/10", font=("Arial", 16, "bold"))
    photo_counter_label.pack(pady=10)
    
    photo_counter_text = tk.Label(left_frame, text="Number of pictures", font=("Arial", 12))
    photo_counter_text.pack()

    camera_preview = tk.Label(right_frame)
    camera_preview.pack()

    camera = cv.VideoCapture(0)

    if not (camera.isOpened()):
        print("ERR: camera not connected")
    else:
        while True:
            if (user_name.get() != ""):
                if(user_name.get() != person_name):
                    #print(f"person_name updated to: {user_name.get()}")
                    user_photo_data = count_users(user_name.get(), DIR, MAX_INDEX, FIRST_INDEX)
                    update_photo_counter(photo_counter_label, user_photo_data[1], MAX_INDEX)
                person_name = user_name.get()
                if person_name in names_set:
                    update_photo_counter(photo_counter_label, user_photo_data[1] + 1, MAX_INDEX)
            else:
                person_name = ""

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