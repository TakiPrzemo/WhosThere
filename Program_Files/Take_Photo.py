import cv2 as cv
import os
import re

if __name__ == '__main__':
    DIR = "Photos"
    FIRST_INDEX = 0
    MAX_INDEX = 9

    # if do ustawiania indeksowania pliku

    # ======================================
    person_name = input("Submit user's name: ")

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

        max_index = max(index_list) + 1
        next_index = max_index

        if next_index >= MAX_INDEX:
            picture_index = FIRST_INDEX
            max_index = MAX_INDEX
        else:
            picture_index = next_index + FIRST_INDEX

    else:
        picture_index = FIRST_INDEX
        max_index = FIRST_INDEX

    # ======================================

    camera = cv.VideoCapture(0)

    if not (camera.isOpened()):
        print("ERR: camera not connected")
    else:
        while True:
            ret, video = camera.read()
            cv.namedWindow("Who's there", cv.WINDOW_GUI_NORMAL)
            cv.imshow("Adding new user", video)

            # wychodzenie z aplikacji
            if cv.waitKey(1) == ord('q'):
                break

            # robienie zdjęć spacją
            elif cv.waitKey(1) == ord(' '):
                file_name = f"{person_name.capitalize()}_{picture_index}.jpg"

                save_path = os.path.join(DIR, file_name)

                cv.imwrite(save_path, video)
                print(f"Photo saved ({max_index + 1}/{MAX_INDEX + 1}): {file_name}")
                picture_index += 1

                if max_index < MAX_INDEX:
                    max_index += 1

                if picture_index > MAX_INDEX:
                    picture_index = FIRST_INDEX
                else:
                    picture_index += FIRST_INDEX

    camera.release()
    cv.destroyAllWindows()
