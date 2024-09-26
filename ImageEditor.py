#Welcome to the Enhanced Image Editing Tool code!
#Before using this image editor code please remember to install Pillow
#by typing 'python -m pip install --upgrade Pillow' in the terminal

#The editing tool will ask about features the user would like to edit from the pictures
#with yes or no questions and give ranges for each feature the user will input to edit the images
#The code will show the user a preview of the edited image before confirming the save.
#There is a retry option to edit the images again until the desired edits are obtained.
#If the user is editing more than one image at the same time,
#the code will ask to keep the changes and save each image individually.
#Please edit the code line 132 and 133 for your desired input and output folders.

#I hope you enjoy editing your pictures as much as I did coding this image editor!

from PIL import Image, ImageEnhance, ImageFilter
import os
from datetime import datetime


# Function to get user inputs for custom image editing parameters
def get_user_inputs():
    adjustments = {}

    # Brightness
    if input("Do you want to adjust brightness? (yes/no, default = no): ").lower() == 'yes':
        brightness = float(input("Brightness (range: 0.0 to 3.0, default = 1.0): ") or 1.0)
        adjustments['brightness'] = brightness

    # Contrast
    if input("Do you want to adjust contrast? (yes/no, default = no): ").lower() == 'yes':
        contrast = float(input("Contrast (range: 0.0 to 3.0, default = 1.0): ") or 1.0)
        adjustments['contrast'] = contrast

    # Sharpness
    if input("Do you want to adjust sharpness? (yes/no, default = no): ").lower() == 'yes':
        sharpness = float(input("Sharpness (range: 0.0 to 3.0, default = 1.0): ") or 1.0)
        adjustments['sharpness'] = sharpness

    # Blur
    if input("Do you want to apply blur? (yes/no, default = no): ").lower() == 'yes':
        blur = float(input("Blur (range: 0 to 10, default = 0): ") or 0)
        adjustments['blur'] = blur

    # Rotation
    if input("Do you want to rotate the image? (yes/no, default = no): ").lower() == 'yes':
        rotation = int(input("Rotation (degrees, range: 0 to 360, default = 0): ") or 0)
        adjustments['rotation'] = rotation

    # Resize
    if input("Do you want to resize the image? (yes/no, default = no): ").lower() == 'yes':
        width = int(input("Resize width (in pixels, default = 800px): ") or 800)
        height = int(input("Resize height (in pixels, default = 800px): ") or 800)
        adjustments['resize'] = (width, height)

    # Saturation
    if input("Do you want to adjust saturation? (yes/no, default = no): ").lower() == 'yes':
        saturation = float(input("Saturation (range: 0.0 to 3.0, default = 1.0): ") or 1.0)
        adjustments['saturation'] = saturation

    # Black and White
    if input("Do you want to convert to black and white? (yes/no, default = no): ").lower() == 'yes':
        adjustments['convert_to_bw'] = True
    else:
        adjustments['convert_to_bw'] = False

    return adjustments


# Function to apply custom edits to an image
def edit_image(img, adjustments):
    # Convert to black and white if selected
    if adjustments.get('convert_to_bw', False):
        img = img.convert('L')

    # Adjust brightness if specified
    if 'brightness' in adjustments:
        brightness_enhancer = ImageEnhance.Brightness(img)
        img = brightness_enhancer.enhance(adjustments['brightness'])

    # Adjust contrast if specified
    if 'contrast' in adjustments:
        contrast_enhancer = ImageEnhance.Contrast(img)
        img = contrast_enhancer.enhance(adjustments['contrast'])

    # Adjust sharpness if specified
    if 'sharpness' in adjustments:
        sharpness_enhancer = ImageEnhance.Sharpness(img)
        img = sharpness_enhancer.enhance(adjustments['sharpness'])

    # Apply blur if specified
    if 'blur' in adjustments:
        img = img.filter(ImageFilter.GaussianBlur(adjustments['blur']))

    # Rotate if specified
    if 'rotation' in adjustments:
        img = img.rotate(adjustments['rotation'], expand=True)

    # Resize if specified
    if 'resize' in adjustments:
        img = img.resize(adjustments['resize'])

    # Adjust saturation if specified
    if 'saturation' in adjustments and img.mode != 'L':
        color_enhancer = ImageEnhance.Color(img)
        img = color_enhancer.enhance(adjustments['saturation'])

    return img


# Function to save the edited image
def save_image(img, filename, pathOut):
    # Convert image mode if it's RGBA to RGB for saving as JPEG
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_name = os.path.splitext(filename)[0]
    counter = 0
    output_file = f'{pathOut}/{clean_name}_{timestamp}_edit_{counter}.jpg'
    while os.path.exists(output_file):
        counter += 1
        output_file = f'{pathOut}/{clean_name}_{timestamp}_edit_{counter}.jpg'

    img.save(output_file)
    print(f"Image saved as: {output_file}")


## ****** Input and Output Folder Location of the Images ******
def process_images(adjustments, batch_mode):
    #By default the input is a file named 'imgs'on the same file as the ImageEditor.py is.
    #The user can edit here any address they would like to use as Input and Output or the edited images.
    path = './imgs'          #This location is the file where the images to be edited are located
    pathOut = './editedImgs' #This location is the file where the edited images will be saved

    # If the output file doesn't exist then it will be created
    if not os.path.exists(pathOut):
        os.makedirs(pathOut)

    for filename in os.listdir(path):
        img = Image.open(f"{path}/{filename}")
        original_img = img.copy()  # Keep a copy for undo

        # Apply custom edits
        img = edit_image(img, adjustments)

        # Preview and allow undo if not in batch mode
        if not batch_mode:
            img.show()
            undo = input("Undo the last edit? (yes/no): ").lower()
            if undo == 'yes':
                original_img.show()
                img = original_img

            save = input("Save the image? (yes/no/retry): ").lower()
            if save == 'retry':
                adjustments = get_user_inputs()
                process_images(adjustments, batch_mode=False)
                break
            elif save == 'yes':
                save_image(img, filename, pathOut)
            else:
                print("Changes discarded.")
        else:
            # Automatically save in batch mode
            save_image(img, filename, pathOut)


# Main program
def main():
    print("Welcome to the Enhanced Image Editing Tool!")

    # Ask if the user wants to run batch mode
    batch_mode = input(
        "Would you like to process all images automatically without preview? (yes/no): ").lower() == 'yes'

    # Get custom editing parameters
    adjustments = get_user_inputs()

    # Process images
    process_images(adjustments, batch_mode)

    print("\nAll images have been processed.")


if __name__ == "__main__":
    main()