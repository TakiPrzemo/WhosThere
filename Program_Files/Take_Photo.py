import cv2 as cv
import os

if __name__ == '__main__':
    DIR = "Photos"
    MIN_INDEX = 0
    MAX_INDEX = 1

    # if do ustawiania indeksowania pliku
    
    #======================================
    person_name = input("Submit persons name: ")

if any(file.startswith(person_name) for file in os.listdir(DIR)):
    existing_files = []
    for file in os.listdir(DIR):
        if re.match(f"{person_name}_[0-9]+\.jpg", file, re.IGNORECASE):
            existing_files.append(file)

    max_index = []
    for file in existing_files:
        number = re.search(r'\d+', file)
        if number:
            number_str = number.group()
            max_index.append(int(number_str))

    max_index = max(max_index)
    if max_index >= MAX_INDEX:
        picture = FIRST_INDEX
    else:
        picture = max_index + FIRST_INDEX      
else:
    picture = FIRST_INDEX
    
    #======================================

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


    camera.release()
    cv.destroyAllWindows()
