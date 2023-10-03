from flask import Flask, request, jsonify
from helpers.deleteFiles import delete_images
from helpers.imageProducer import send_images_to_queue
from helpers.s3Aws import getImage, deleteImage

app = Flask(__name__)

@app.route('/kyc-api/delete-image', methods=['DELETE'])
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
    

@app.route('/kyc-api/get-image', methods=['GET'])
def get_image():
    filename = request.args.get('filename')
    destination_path = 'temp.jpg'  # Temporary file to store the downloaded image
    try:
       return getImage(filename,destination_path)                
    except Exception as e:
        error_message = f'Error downloading {filename}, {str(e)}'
        print(error_message)  # Optional: Log the error message
        return jsonify({'error': error_message}), 500


@app.route('/kyc-api/compare_images', methods=['POST'])
def compare_images():
    try:
        # Save the first image
        temp1 = request.files['image1']
        temp1.save("temp1.jpg")        
        
        # Save the second image
        temp2 = request.files['image2']
        temp2.save("temp2.jpg")
        
        #Send the images to the queue
        send_images_to_queue("temp1.jpg","temp2.jpg", "267364")
        delete_images(["temp1.jpg", "temp2.jpg" ])
        return jsonify({"message": "Images sent for processing."})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host= "0.0.0.0", debug=True, port=3000)
