import face_recognition
import numpy as np

def compareTwo(image1_path, image2_path):
    # Load the images using face_recognition
    image1 = face_recognition.load_image_file(image1_path)
    image2 = face_recognition.load_image_file(image2_path)

    # Get face encodings
    face_encodings1 = face_recognition.face_encodings(image1)
    face_encodings2 = face_recognition.face_encodings(image2)
    
    if not face_encodings1:
        return "No face found in the first image."
    if not face_encodings2:
        return "No face found in the second image."
     # Calculate face distances
    face_distances = np.linalg.norm(np.array(face_encodings1) - np.array(face_encodings2), axis=1)
    if face_distances[0] < 0.6:        
        return "The same person appears in both images."    
    else:
        return "Different people appear in the two images."
    
        