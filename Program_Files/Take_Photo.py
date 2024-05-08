import cv2 as cv
import os

if __name__ == '__main__':
    DIR = "Photos"
    MIN_INDEX = 0
    MAX_INDEX = 1

    # if do ustawiania indeksowania pliku

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
