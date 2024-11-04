import pytesseract
from PIL import Image, ImageEnhance, ImageOps
import matplotlib.pyplot as plt

# Define function to preprocess, crop, rotate, and extract text
def process_image(image_path, left, right, top, bottom, rotation, display=False):
    # Load image
    img = Image.open(image_path)
    
    # Crop and rotate
    cropped_img = img.crop((left, top, right, bottom))
    rotated_img = cropped_img.rotate(rotation, expand=True)
    
    # Display the cropped and rotated image for verification
    if display:
        plt.imshow(rotated_img)
        plt.title(f"Cropped and Rotated Image: Left={left}, Right={right}, Top={top}, Bottom={bottom}, Rotation={rotation}")
        plt.axis('off')
        plt.show()
    
    # Preprocessing: Convert to grayscale, increase contrast, and sharpen
    gray_img = ImageOps.grayscale(rotated_img)
    contrast_enhancer = ImageEnhance.Contrast(gray_img)
    enhanced_img = contrast_enhancer.enhance(2)  # Adjust contrast as needed
    sharpness_enhancer = ImageEnhance.Sharpness(enhanced_img)
    preprocessed_img = sharpness_enhancer.enhance(2)  # Adjust sharpness as needed

    # Extract text with Tesseract
    custom_config = r'--oem 3 --psm 6'  # You can experiment with different PSM modes
    text = pytesseract.image_to_string(preprocessed_img, config=custom_config)
    return text

image_path = 'image.png'

displayrest = True

# Enable display to verify each crop and rotation visually
oneheader = process_image(image_path, left=0, right=30, top=0, bottom=607, rotation=-90, display=displayrest)
onesub = process_image(image_path, left=25, right=48, top=466, bottom=606, rotation=-90, display=displayrest)
twoheader = process_image(image_path, left=1155, right=1188, top=59, bottom=665, rotation=90, display=displayrest)
twosub = process_image(image_path, left=1132, right=1159, top=60, bottom=200, rotation=90, display=displayrest)

print("One header Text:", oneheader)
print("One sub Text:", onesub)
print("Two header Text:", twoheader)
print("Two sub Text:", twosub)

