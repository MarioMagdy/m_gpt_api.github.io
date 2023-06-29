# Import Flask, request, cv2, edit, and base64
from flask import Flask, request, render_template
import cv2
import numpy as np
from edits import edit_image
import base64
import automated_gptv0_03

# Create an instance of the Flask class
app = Flask(__name__)

# Define a route for the home page
@app.route("/")
def home():
    # Render the index.html template without any variables
    return render_template("index.html")

# Define a route for the upload page
@app.route("/upload", methods=["POST"])
def upload():
    # Get the uploaded image from the request
    sage = automated_gptv0_03.gpt("sage1")
    resp  = sage.use_gpt("how are you")
    image = request.files["image"]
    # Read the image data using cv2
    image_data = cv2.imdecode(np.frombuffer(image.read(), np.uint8), -1)
    # Edit the image data and get the mean pixel value using your function
    image_data, mean = edit_image(image_data)
    # Encode the image data as JPEG using cv2
    _, image_data = cv2.imencode(".jpg", image_data)
    # Encode the image data as base64 using base64
    image_data = base64.b64encode(image_data.tobytes()).decode()
    # Render the index.html template with the image data and the mean pixel value as variables

    return render_template("index.html", image=image_data, mean=mean,gpt_val = resp)

# Run the app if this file is executed as the main script
if __name__ == "__main__":
    app.run()