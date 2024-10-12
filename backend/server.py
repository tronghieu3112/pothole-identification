from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64

app = Flask(__name__)

#test server is running
@app.route("/photos", methods = ['GET'])
def photos():
    return jsonify({ "photos": ["Photo1", "Photo2", "Photo3"] })

#save image from client
@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        # Get the base64 encoded image data from the request
        data = request.get_json()
        image_data = data['image']

        return jsonify({'message': 'Server processed successfully', 'processed_image': image_data})

    except Exception as e:
        print(f'Error processing image: {e}')
        return jsonify({'error': 'Failed to process image'}), 500

if __name__ == "__main__":
    app.run(host = '192.168.2.9', port=3000, debug=True)