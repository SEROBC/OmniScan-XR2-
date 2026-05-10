import face_recognition

def encode_face(image_path):
    img = face_recognition.load_image_file(image_path)
    return face_recognition.face_encodings(img)[0]

def match_face(known, unknown):
    return face_recognition.compare_faces([known], unknown)[0]
