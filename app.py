from flask import Flask, request, jsonify
import face_recognition
import numpy as np

from helpers.s3Aws import uploadImage, getImage, deleteImage

app = Flask(__name__)

@app.route('/delete-image', methods=['DELETE'])
def delete_image():
    print("Entro en la petición")
    filename = request.args.get('filename')
    try:
        deleteImage(filename)
        return jsonify({'message': f'Successfully deleted {filename}'}), 200
    except Exception as e:
        error_message = f'Error deleting {filename}: {str(e)}'
        print(error_message) 
        return jsonify({'error': error_message}), 500
    

@app.route('/get-image', methods=['GET'])
def get_image():
    filename = request.args.get('filename')
    destination_path = 'temp.jpg'  # Temporary file to store the downloaded image
    try:
       return getImage(filename,destination_path)                
    except Exception as e:
        error_message = f'Error downloading {filename}, {str(e)}'
        print(error_message)  # Optional: Log the error message
        return jsonify({'error': error_message}), 500

@app.route('/upload_image1', methods=['POST'])
def upload_image1():    
    try:
        print("upload image")
        image1 = face_recognition.load_image_file(request.files['image'].stream)
        face_encodings1 = face_recognition.face_encodings(image1)        
        if not face_encodings1:
            return jsonify({"message": "No face found in the first image."}), 400
        return jsonify({"message": "First image uploaded successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload_image2', methods=['POST'])
def upload_image2():    
    try:
        image2 = face_recognition.load_image_file(request.files['image'].stream)
        face_encodings2 = face_recognition.face_encodings(image2)        
        if not face_encodings2:
            return jsonify({"message": "No face found in the second image."}), 400
        return jsonify({"message": "Second image uploaded successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/compare_images', methods=['POST'])
def compare_images():
    try:
        # Load the first image
        temp1 = request.files['image1']
        temp1.save("temp1.jpg")
        image1 = face_recognition.load_image_file(request.files['image1'].stream)
        face_encodings1 = face_recognition.face_encodings(image1)

        # Load the second image
        temp2 = request.files['image2']
        temp2.save("temp2.jpg")
        image2 = face_recognition.load_image_file(request.files['image2'].stream)
        face_encodings2 = face_recognition.face_encodings(image2)

        if not face_encodings1:
            return jsonify({"message": "No face found in the first image."}), 400

        if not face_encodings2:
            return jsonify({"message": "No face found in the second image."}), 400

        # Calculate face distances
        face_distances = np.linalg.norm(np.array(face_encodings1) - np.array(face_encodings2), axis=1)

        if face_distances[0] < 0.6:
            uploadImage("temp1.jpg")
            uploadImage("temp2.jpg")
            return jsonify({"message": "The same person appears in both images."}), 200
        else:
            return jsonify({"message": "Different people appear in the two images."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host= "0.0.0.0", debug=True)
