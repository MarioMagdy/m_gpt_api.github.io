# Import cv2
import cv2

# Define a function that takes an image data as an input and returns a modified image data as an output
def edit_image(image_data):
    # Convert the image data to grayscale using cv2
    image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
    # Calculate the mean pixel value of the image using cv2
    mean = cv2.mean(image_data)
    # Take the average of the four values in the tuple
    mean = sum(mean) / 4
    # Return the modified image data and the mean pixel value
    return image_data, mean