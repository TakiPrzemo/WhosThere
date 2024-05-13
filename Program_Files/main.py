import face_recognition
import cv2 as cv
import numpy as np
import yaml

def face_confidence(face_distance, face_match_threshold):
    range = 1.0 - face_match_threshold
    linear_val = (1.8 * face_distance) / (range * 2.0)
    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + "%"
    else:
        value = (linear_val + ((1.0 - linear_val) * pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + "%"
        
        
with open('known_faces.yml', 'r') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    known_face_names = data['names']
    known_face_encodings = np.array(data['encodings'])

face_loc = []
face_encodings = []
face_names = []
process_this_frame = True


video_capture = cv.VideoCapture(0)

while True:
    ret, frame = video_capture.read()

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
    
    cv.namedWindow('Video', cv.WINDOW_GUI_NORMAL)
    cv.imshow('Video', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv.destroyAllWindows()
