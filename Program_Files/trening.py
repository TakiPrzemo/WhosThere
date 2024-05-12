import face_recognition
import os
import yaml

DIR = r'Zdjecia'
known_face_names = []
known_face_encodings = []

try:
    for file in os.listdir(DIR):
        image_path = os.path.join(DIR, file)
        name = os.path.splitext(os.path.basename(image_path))[0]
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding.tolist())
        known_face_names.append(name)

    with open('known_faces.yml', 'w') as f:
        yaml.dump({'names': known_face_names, 'encodings': known_face_encodings}, f)
    print("---------Trening end---------")
except IndexError:
    print("Zdjęcie jest zbyt rozmazane, powtórz serię!")