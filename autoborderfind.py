from PIL import Image

def main():
    # Load the image
    image = Image.open('image.png')
    pixels = image.load()
    width, height = image.size
    grey = (30, 30, 30)

    # Lists to hold the x and y coordinates of grey pixels
    x_coords = []
    y_coords = []

    # Iterate over each pixel in the image
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            # Handle images with RGBA channels
            if len(pixel) >= 3:
                rgb = pixel[:3]
            else:
                rgb = pixel
            # Check if the pixel matches the specific grey color
            if rgb == grey:
                x_coords.append(x)
                y_coords.append(y)

    # If grey pixels are found, proceed to crop
    if x_coords and y_coords:
        left = min(x_coords)
        right = max(x_coords)
        top = min(y_coords)
        bottom = max(y_coords)

        # Crop the image to the bounding box of grey pixels
        cropped_image = image.crop((left, top, right + 1, bottom + 1))
        cropped_image.save('cropped_image.png')
        print('Cropped image saved as cropped_image.png')
    else:
        print('No grey pixels found in the image.')

if __name__ == '__main__':
    main()
