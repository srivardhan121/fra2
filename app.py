import cv2
from flask import Flask, jsonify, send_from_directory
import os

# Initialize the Flask app
app = Flask(__name__)

# Ensure a folder for saving captured images exists
captured_images_dir = 'captured_images'
if not os.path.exists(captured_images_dir):
    os.makedirs(captured_images_dir)

@app.route('/')
def welcome():
    return "Welcome to the Flask Camera App! Visit /capture to take a photo."

@app.route('/capture', methods=['GET'])
def capture():
    # Open the default camera (camera index 0)
    camera = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not camera.isOpened():
        return jsonify({'error': 'Could not open the camera.'}), 500

    # Capture a single frame from the camera
    ret, frame = camera.read()

    # If frame capture failed, return an error
    if not ret:
        camera.release()
        return jsonify({'error': 'Failed to capture image.'}), 500

    # Save the captured image to the captured_images folder
    image_filename = 'captured_image.jpg'
    image_path = os.path.join(captured_images_dir, image_filename)
    cv2.imwrite(image_path, frame)

    # Release the camera after capturing the image
    camera.release()

    # Return the image URL in the response (make sure to serve it correctly)
    return jsonify({'message': 'Image captured successfully', 'image_url': f'/{captured_images_dir}/{image_filename}'})


# Route to serve the captured image from captured_images folder
@app.route('/captured_images/<path:filename>')
def send_image(filename):
    return send_from_directory(captured_images_dir, filename)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
