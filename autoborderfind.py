import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def auto_crop_image(image_path, border_color=(30, 30, 30), tolerance=10000, display=False):
    # Load the image
    img = cv2.imread(image_path)
    
    # Convert to grayscale and apply a threshold to highlight the border
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Identify the largest contour, assuming it represents the main content area
    main_contour = max(contours, key=cv2.contourArea)
    
    # Get bounding box coordinates around the main content
    x, y, w, h = cv2.boundingRect(main_contour)
    
    # Crop the image using the bounding box
    cropped_img = img[y:y+h, x:x+w]
    
    # Display the cropped image if needed
    if display:
        plt.imshow(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
        plt.title("Cropped Image")
        plt.axis('off')
        plt.show()
    
    return cropped_img, (x, y, w, h)

def save_cropped_image(cropped_img, output_path='cropped_image.png'):
    # Save the cropped image
    cv2.imwrite(output_path, cropped_img)
    print(f"Cropped image saved to {output_path}")

# Define the path to your input image
image_path = 'image.png'

# Auto-crop the image to remove the border
cropped_img, coordinates = auto_crop_image(image_path, display=True)

# Save the cropped image
save_cropped_image(cropped_img)
