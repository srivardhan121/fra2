import os
import cv2
from flask import Flask, Response

app = Flask(__name__)

# Ensure the 'captured_images' directory exists
if not os.path.exists('captured_images'):
    os.makedirs('captured_images')

@app.route('/')
def index():
    return "Welcome to the Flask Camera App! Visit /capture to take a photo."

@app.route('/capture', methods=['GET'])
def capture_image():
    # Open the camera (0 is the default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return "Error: Could not open camera."

    # Capture one frame
    ret, frame = cap.read()
    if not ret:
        cap.release()
        return "Error: Failed to capture image."

    # Save the captured frame as an image
    image_path = os.path.join('captured_images', 'captured_image.jpg')
    cv2.imwrite(image_path, frame)

    # Release the camera
    cap.release()

    return f"Image captured and saved at {image_path}"

if __name__ == '__main__':
    app.run(debug=True)
