import cv2
import numpy as np

# Load the image or video
def load_image(path):
    image = cv2.imread(path)
    return image

def load_video(path):
    video = cv2.VideoCapture(path)
    return video

# Convert the image to HSV color space
def convert_to_hsv(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return hsv

# Define the range of colors for black and white shirts
def define_color_ranges():
    black_lower = np.array([0, 0, 0])
    black_upper = np.array([180, 255, 50])
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([180, 50, 255])
    return black_lower, black_upper, white_lower, white_upper

# Detect the color of the shirt
def detect_shirt_color(hsv, black_lower, black_upper, white_lower, white_upper):
    black_mask = cv2.inRange(hsv, black_lower, black_upper)
    white_mask = cv2.inRange(hsv, white_lower, white_upper)
    return black_mask, white_mask

# Detect the number on the uniform
def detect_number(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w)/h
        if area > 100 and aspect_ratio > 2 and aspect_ratio < 5:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            return image
    return image

# Main function
def main():
    path = 'image.jpg'  # replace with your image or video path
    image = load_image(path)
    hsv = convert_to_hsv(image)
    black_lower, black_upper, white_lower, white_upper = define_color_ranges()
    black_mask, white_mask = detect_shirt_color(hsv, black_lower, black_upper, white_lower, white_upper)
    cv2.imshow('Black Mask', black_mask)
    cv2.imshow('White Mask', white_mask)
    image = detect_number(image)
    cv2.imshow('Number Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()