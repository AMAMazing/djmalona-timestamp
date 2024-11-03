from PIL import Image, ImageEnhance, ImageOps
import pytesseract
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

# Enable display to verify each crop and rotation visually
oneheader = process_image(image_path, left=0, right=30, top=0, bottom=607, rotation=-90, display=False)
twoheader = process_image(image_path, left=1155, right=1188, top=59, bottom=665, rotation=90, display=False)

print("One header Text:", oneheader)
print("Two header Text:", twoheader)
