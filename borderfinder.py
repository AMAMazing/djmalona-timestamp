import cv2
from tkinter import Tk, Scale, Button, Label, Frame, HORIZONTAL, IntVar

# Initialize Tkinter
root = Tk()
root.title("Image Cropper Controls")

# Load the image
image_path = 'image.png'    
img = cv2.imread(image_path)
img_height, img_width = img.shape[:2]

# Initial crop settings using IntVar after root is created
crop_left = IntVar(value=0)
crop_right = IntVar(value=img_width)
crop_top = IntVar(value=0)
crop_bottom = IntVar(value=img_height)
rotation = IntVar(value=90)

def update_image():
    """Update the displayed image with the current crop and rotation, maintaining aspect ratio."""
    # Ensure crop boundaries are valid
    if crop_left.get() < crop_right.get() and crop_top.get() < crop_bottom.get():
        cropped_img = img[crop_top.get():crop_bottom.get(), crop_left.get():crop_right.get()]

        # Check if the cropped image has content
        if cropped_img.size == 0:
            print("Warning: The cropped area is empty. Adjust crop boundaries.")
            return

        # Rotate the cropped image
        if rotation.get() == 90:
            rotated_img = cv2.rotate(cropped_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif rotation.get() == -90:
            rotated_img = cv2.rotate(cropped_img, cv2.ROTATE_90_CLOCKWISE)
        else:
            rotated_img = cropped_img

        # Resize with maintained aspect ratio
        max_display_size = 400
        h, w = rotated_img.shape[:2]
        scale = max_display_size / max(h, w)
        new_w, new_h = int(w * scale), int(h * scale)
        display_img = cv2.resize(rotated_img, (new_w, new_h))

        # Display the image in an OpenCV window
        cv2.imshow("Cropped Image", display_img)
    else:
        print("Invalid crop boundaries. Adjust the sliders or buttons.")

def print_coordinates():
    """Print the current crop coordinates and rotation."""
    print(f"Crop Coordinates: left={crop_left.get()}, right={crop_right.get()}, "
          f"top={crop_top.get()}, bottom={crop_bottom.get()}, rotation={rotation.get()}")

def increment(var, value):
    """Increment or decrement a variable and update the image."""
    var.set(var.get() + value)
    update_image()

# Frame for the controls
controls_frame = Frame(root)
controls_frame.pack()

# Helper function to create slider with increment/decrement buttons
def create_control_with_slider(label_text, var, from_, to, command):
    label = Label(controls_frame, text=label_text)
    label.pack()

    # Frame for slider and fine adjustment buttons
    control_frame = Frame(controls_frame)
    control_frame.pack()

    # Decrement button
    Button(control_frame, text="-", command=lambda: increment(var, -1)).pack(side="left")

    # Slider for coarse adjustments
    slider = Scale(control_frame, from_=from_, to=to, orient=HORIZONTAL, variable=var, command=lambda v: command())
    slider.pack(side="left")

    # Increment button
    Button(control_frame, text="+", command=lambda: increment(var, 1)).pack(side="right")

# Create controls for crop boundaries and rotation
create_control_with_slider("Left", crop_left, 0, img_width, update_image)
create_control_with_slider("Right", crop_right, 0, img_width, update_image)
create_control_with_slider("Top", crop_top, 0, img_height, update_image)
create_control_with_slider("Bottom", crop_bottom, 0, img_height, update_image)
create_control_with_slider("Rotation", rotation, -90, 90, update_image)

# Print coordinates button
Button(root, text="Print Coordinates", command=print_coordinates).pack()

# Display the initial cropped image
update_image()

# Run the Tkinter main loop
root.mainloop()

# Close the OpenCV window when done
cv2.destroyAllWindows()
