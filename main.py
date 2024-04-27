#---------------------------------------------------------------------------------------------------------------
# Program: Team 1 Photo Editor
# Author(s): Samuel Johnson, Gabe Bartek, Ryan Michael, Cole Mason
# Last Updated: 3/19/2024
# Purpose: To edit the color, rotation, and size of image files.
#---------------------------------------------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, simpledialog
from PIL import ImageTk, Image  
from pathlib import Path
from tkinter import font as tkFont
import numpy as np
import os
import cv2

# Declarations: --------------------------------------------------------------------------------

# System:

global CurrentImagePath # The path of the original entered image
global RealImage # The actual image, which will be modified while retaining its original size.

current_image = None
CurrentImagePath = None

# "Dark mode" Palette:

Highlight = "#2B2B2B"
Lightest = "#1F1F1F"
MidLightest = "#2B2B2B"
MidDarkest = "#111111"
Darkest = "#141414"
ButtonColor = MidLightest
DescriptionTextColor = "#FFF"

# Salmon palette (requires label color swapping)

#Highlight = "#8E8D8A"
#Lightest = "#EAE7DC"
#MidLightest = "#D8C3A5"
#MidDarkest = "#E98074"
#Darkest = "#E85A4F"
#ButtonColor = "#D8C3A5"

# Original grayscale color scheme:

#Highlight = "#DFDFDF"
#Lightest = "#898989"
#MidLightest = "#5C5C5C"
#MidDarkest = "#393939"
#Darkest = "#000000"
#ButtonColor = Lightest

# Button design:

BorderWidth = 5
BorderStyle = tk.RAISED
TextColor = "#000000"

root = tk.Tk()
root.geometry("1080x700")
root.title("IMAGE+ Photo Editor")
root.minsize(780, 700)

tkFont.BOLD == 'bold' # Create font object
FONT = tkFont.Font(family='Arial', size=14, weight=tkFont.BOLD)

# Image variables:

IMAGE_PATH = os.path.join(Path(__file__).parent, "IMGs", "")

MaxImageSize = 520 # The largest pixel height or width that the main image can hold

root.iconbitmap(IMAGE_PATH + "Icon.ico")

LogoImage = ImageTk.PhotoImage(Image.open(IMAGE_PATH + "Logo.png"))
SaveImage = ImageTk.PhotoImage(Image.open(IMAGE_PATH + "SaveButton.png"))
LoadButtonImage = ImageTk.PhotoImage(Image.open(IMAGE_PATH + "LoadButton.png"))


BnWButtonImage = ImageTk.PhotoImage(Image.open(IMAGE_PATH + "Button0.png"))
GreyButtonImage = ImageTk.PhotoImage(Image.open(IMAGE_PATH + "Button1.png"))
FlipHButtonImage = ImageTk.PhotoImage(Image.open(IMAGE_PATH + "Button2.png"))
FlipVButtonImage = ImageTk.PhotoImage(Image.open(IMAGE_PATH + "Button3.png"))
ResizeImage = ImageTk.PhotoImage(Image.open(IMAGE_PATH + "Button4.png"))
InvertImage = ImageTk.PhotoImage(Image.open(IMAGE_PATH + "Button5.png"))
CropImage = ImageTk.PhotoImage(Image.open(IMAGE_PATH + "Button6.png"))
RotateImage = ImageTk.PhotoImage(Image.open(IMAGE_PATH + "Button7.png"))
UndoImage = ImageTk.PhotoImage(Image.open(IMAGE_PATH + "Button8.png"))

root.columnconfigure(0, weight=1) # Set the heights of each screen section
root.rowconfigure(0, weight=70)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=700)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=80)

# Functions: --------------------------------------------------------------------------------


def update_current_image(img):
    global current_image
    current_image = img.copy()

def UpdateSizeDisplay(img):
    global ImageSizeDisplay
    height, width, _ = img.shape
    ImageSizeDisplay.config(text=(str(width) + " x " + str(height)))

def Resizer(img):
    height, width, _ = img.shape
    
    # Determine resizing factor
    if height > MaxImageSize and width < MaxImageSize:
        multiplier = MaxImageSize / height
    elif width > MaxImageSize and height < MaxImageSize:
        multiplier = MaxImageSize / width
    elif width > MaxImageSize and height > MaxImageSize:
        multiplier = MaxImageSize / max(height, width)
    else:
        multiplier = 1
    # Resize the image
    img = cv2.resize(img, None, fx=multiplier, fy=multiplier, interpolation=cv2.INTER_AREA)
    return img


def LoadImage():
    global CurrentImagePath, MainImage, current_image, RealImage  # Declare MainImage as a global variable
    # Open the file directory and allow image selection
    file_path = filedialog.askopenfilename( 
        initialdir=os.getcwd(),
        title="Select an image",
        filetypes=(("PNG files", "*.png"),)  # Specify the allowed file types
    )
    if file_path and file_path.lower().endswith((".png", ".PNG")):
        img = cv2.imread(file_path)
        UpdateSizeDisplay(img)
        RealImage = img
        img = Resizer(img)
        # Convert OpenCV image to PIL Image
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        photo = ImageTk.PhotoImage(img)
        # Set global variables and update MainImage picture
        CurrentImagePath = file_path
        print(CurrentImagePath)
        update_current_image(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))  # Update current image
        MainImage.config(image=photo)
        MainImage.image = photo

def SaveAsImage():
    global RealImage

    if current_image is not None:
        FilePath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if FilePath:  # Check if the user entered a file path
            
            image = cv2.cvtColor(RealImage, cv2.COLOR_BGR2RGB)
            photo = Image.fromarray(image)
            photo.save(FilePath)

def convert_to_black_and_white():
    global current_image, MainImage, RealImage

    if current_image is not None:
        # Dummy version modifications:
        gray_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY) # Set the image to grayscale to avoid color channel inconsistency.
        ret, BinaryImage = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY) # Re-assign pixels based on value.
        BinaryImage = cv2.cvtColor(BinaryImage, cv2.COLOR_GRAY2RGB)

        # Real image modifications:
        gray_real_image = cv2.cvtColor(RealImage, cv2.COLOR_BGR2GRAY) # Set the image to grayscale to avoid color channel inconsistency.
        ret, BinaryRealImage = cv2.threshold(gray_real_image, 127, 255, cv2.THRESH_BINARY) # Re-assign pixels based on value.
        RealImage = cv2.cvtColor(BinaryRealImage, cv2.COLOR_GRAY2RGB)

        current_image = BinaryImage # Set the global current image variable to the updated image.
        pil_img = Image.fromarray(BinaryImage)
        
        # Create a PhotoImage from the PIL Image
        photo = ImageTk.PhotoImage(pil_img)
        
        # Update the image displayed in the MainImage widget
        MainImage.config(image=photo)
        MainImage.image = photo  # Keep a reference to prevent garbage collection
        

def convert_to_grayscale():
    global current_image, MainImage, RealImage
    
    if current_image is not None:
        
        # Dummy version modifications:
        gray_img = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY) # Convert the current image to grayscale
        gray_img_rgb = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2RGB) # Convert grayscale image to RGB for display
        current_image = gray_img_rgb

        # Real version modifications:
        gray_real_img = cv2.cvtColor(RealImage, cv2.COLOR_BGR2GRAY) # Convert the current image to grayscale
        gray_real_img_rgb = cv2.cvtColor(gray_real_img, cv2.COLOR_GRAY2RGB) # Convert grayscale image to RGB for display
        RealImage = gray_real_img_rgb
        
        # Display dummy version:
        pil_img = Image.fromarray(gray_img_rgb)
        photo = ImageTk.PhotoImage(pil_img)
        MainImage.config(image=photo)
        MainImage.image = photo

def convert_to_flip_h():
    global current_image, MainImage, RealImage

    if current_image is not None:

        # Dummy version modifications:
        BinaryImage = cv2.flip(current_image, 1) # Flip the image
        current_image = BinaryImage

        # Real image modifications:
        BinaryRealImage = cv2.flip(RealImage, 1) # Flip the image
        RealImage = BinaryRealImage

        # Display dummy version:
        BinaryImage = cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(BinaryImage)
        photo = ImageTk.PhotoImage(pil_img)
        MainImage.config(image=photo)
        MainImage.image = photo

def convert_to_flip_v():
    global current_image, MainImage, RealImage

    if current_image is not None:

        # Dummy version modifications:
        BinaryImage = cv2.flip(current_image, 0) # Flip the image
        current_image = BinaryImage

        # Real version modifications:
        BinaryRealImage = cv2.flip(RealImage, 0) # Flip the image
        RealImage = BinaryRealImage

        # Display dummy version:
        BinaryImage = cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(BinaryImage)
        photo = ImageTk.PhotoImage(pil_img)
        MainImage.config(image=photo)
        MainImage.image = photo

def convert_to_scaled():
    global current_image, MainImage, RealImage

    if current_image is not None:
        pass

def convert_to_inverted():
    global current_image, MainImage, RealImage

    if current_image is not None:
        # Dummy version modifications:
        b, g, r = cv2.split(current_image)
        inverted_b = 255 - b # Invert each color channel...
        inverted_g = 255 - g
        inverted_r = 255 - r
        inverted_image = cv2.merge((inverted_b, inverted_g, inverted_r)) # ...and stitch them together again.
        current_image = inverted_image

        # Real version modifications:
        b, g, r = cv2.split(RealImage)
        inverted_b = 255 - b
        inverted_g = 255 - g
        inverted_r = 255 - r
        inverted_real_image = cv2.merge((inverted_b, inverted_g, inverted_r))
        RealImage = inverted_real_image
        
        # Display dummy version:
        inverted_image = cv2.cvtColor(inverted_image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(inverted_image)
        photo = ImageTk.PhotoImage(pil_img)
        MainImage.config(image=photo)
        MainImage.image = photo

def convert_to_randomized():
    global current_image, MainImage, RealImage

    if current_image is not None:
        # Dummy version modifications:
        b, g, r = cv2.split(current_image)
        random_b = np.random.randint(0, 256)
        random_g = np.random.randint(0, 256)
        random_r = np.random.randint(0, 256)
        
        b = np.clip(b + random_b, 0, 255).astype(np.uint8)
        g = np.clip(g + random_g, 0, 255).astype(np.uint8)
        r = np.clip(r + random_r, 0, 255).astype(np.uint8)
        inverted_image = cv2.merge((b, g, r))
        current_image = inverted_image

        # Real version modifications:
        b, g, r = cv2.split(RealImage)

        inverted_b = np.clip(b + random_b, 0, 255).astype(np.uint8)
        inverted_g = np.clip(g + random_g, 0, 255).astype(np.uint8)
        inverted_r = np.clip(r + random_r, 0, 255).astype(np.uint8)
        inverted_real_image = cv2.merge((inverted_b, inverted_g, inverted_r))
        RealImage = inverted_real_image
        
        # Display dummy version:
        inverted_image = cv2.cvtColor(inverted_image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(inverted_image)
        photo = ImageTk.PhotoImage(pil_img)
        MainImage.config(image=photo)
        MainImage.image = photo

def GetInput(DotNumber, Direction):
    global RealImage
    height, width, _ = RealImage.shape
    
    # Get the first number input
    if (Direction == "height"):
        Input = simpledialog.askinteger("Input", f"Enter the " + Direction + " of the " + DotNumber + " point (0 - " + str(height) + "):", parent=root, minvalue=0, maxvalue=height)
    else:
        Input = simpledialog.askinteger("Input", f"Enter the " + Direction + " of the " + DotNumber + " point (0 - " + str(width) + "):", parent=root, minvalue=0, maxvalue=width)
    if Input is None:  # Check if user cancels the dialog
        return None, None
    return Input

def convert_to_rotated():
    global current_image, MainImage, RealImage

    if current_image is not None:

        current_image = cv2.rotate(current_image, cv2.ROTATE_90_CLOCKWISE) # Dummy version
        RealImage = cv2.rotate(RealImage, cv2.ROTATE_90_CLOCKWISE) # Real version
        UpdateSizeDisplay(RealImage) # Change the width x height display

        rotated_img = cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB) # Convert the rotated image to RGB (OpenCV uses BGR)
        pil_img = Image.fromarray(rotated_img) # Convert the OpenCV image to a PIL Image
        photo = ImageTk.PhotoImage(pil_img)
        MainImage.config(image=photo)
        MainImage.image = photo

def reset_image():
    global current_image, MainImage, CurrentImagePath, RealImage
    
    if current_image is not None:
        img = cv2.imread(CurrentImagePath)
        RealImage = img
        UpdateSizeDisplay(RealImage) # Change the width x height display
        img = Resizer(img)
        current_image = img
        img = cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB)

        # Convert the OpenCV image to a PIL Image
        pil_img = Image.fromarray(img)
        
        # Create a PhotoImage from the PIL Image
        photo = ImageTk.PhotoImage(pil_img)

        # Update the image displayed in the MainImage widget
        MainImage.config(image=photo)
        MainImage.image = photo  # Keep a reference to prevent garbage collection



# Frame setup: --------------------------------------------------------------------------------

TopFrame = tk.Canvas(root)
TopFrame.columnconfigure(0, weight=1)
TopFrame.columnconfigure(1, weight=1)
TopFrame.columnconfigure(2, weight=12)
TopFrame.columnconfigure(3, weight=3)
TopFrame.rowconfigure(0, weight=1)
TopFrame.grid(row=0, column=0, sticky="NWES")

MiddleShadow = ttk.Frame(root)
MiddleShadow.grid(row=1, column=0, sticky="NWES")

MiddleFrame = ttk.Frame(root, width=520, height=520)
MiddleFrame.grid(row=2, column=0, sticky="NWES")

EndShadow = ttk.Frame(root)
EndShadow.grid(row=3, column=0, sticky="NWES")

BottomFrame = ttk.Frame(root)
BottomFrame.columnconfigure(0, weight=1)
BottomFrame.grid(row=4, column=0, sticky="NWES")

BottomDescriptions = ttk.Frame(root)
BottomDescriptions.columnconfigure(0, weight=1)
BottomDescriptions.grid(row=5, column=0, sticky="NWES")

# Top section and buttons: --------------------------------------------------------------------------------

LoadButton = tk.Button(TopFrame, image=LoadButtonImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT, command=LoadImage)
SaveButton = tk.Button(TopFrame, image=SaveImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT, command=SaveAsImage)
HeaderImage = tk.Label(TopFrame, bg=Lightest, fg=TextColor, font=FONT, image=LogoImage)
HeaderText = tk.Label(TopFrame, text="       PHOTO EDITOR  ", bg=Lightest, fg="#3F3F3F", font=FONT)

LoadButton.grid(row=0, column=0, sticky="NWES")
SaveButton.grid(row=0, column=1, sticky="NWES")
HeaderImage.grid(row=0, column=2, sticky="NWES")
HeaderText.grid(row=0, column=3, sticky="NWES")

# Middle section: --------------------------------------------------------------------------------

ShadowLabel1 = tk.Label(MiddleShadow, bg=MidDarkest)
ShadowLabel1.pack(fill="both", side="top", expand=True)
global ImageSizeDisplay
ImageSizeDisplay = tk.Label(MiddleShadow, bg=Darkest, fg="#FFF", text="0 x 0")
ImageSizeDisplay.pack(fill="both", side="top", expand=True)

MainImage = tk.Label(MiddleFrame, image=None, bg=Darkest)
MainImage.pack(fill="both", side="top", expand=True)

ShadowLabel2 = tk.Label(EndShadow, bg=Highlight)
ShadowLabel2.pack(fill="both", side="top", expand=True)



# Bottom buttons: --------------------------------------------------------------------------------

Separator1 = tk.Label(BottomFrame, text="          ", bg=Lightest) # Makes space on the bottom row
Separator1.pack(fill="both", expand=True, side="left")

BAndWButton = tk.Button(BottomFrame, image=BnWButtonImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT, command=convert_to_black_and_white)
BAndWButton.pack(fill="both", expand=True, side="left")
GreyscaleButton = tk.Button(BottomFrame, image=GreyButtonImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT, command=convert_to_grayscale)
GreyscaleButton.pack(fill="both", expand=True, side="left")
FHorizButton = tk.Button(BottomFrame, image=FlipHButtonImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT, command=convert_to_flip_h)
FHorizButton.pack(fill="both", expand=True, side="left")
FVertiButton = tk.Button(BottomFrame, image=FlipVButtonImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT, command=convert_to_flip_v)
FVertiButton.pack(fill="both", expand=True, side="left")
ResizeButton = tk.Button(BottomFrame, image=ResizeImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT)
ResizeButton.pack(fill="both", expand=True, side="left")
InvertButton = tk.Button(BottomFrame, image=InvertImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT, command=convert_to_inverted)
InvertButton.pack(fill="both", expand=True, side="left")
CropButton = tk.Button(BottomFrame, image=CropImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT, command=convert_to_randomized)
CropButton.pack(fill="both", expand=True, side="left")
RotateButton = tk.Button(BottomFrame, image=RotateImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT, command=convert_to_rotated)
RotateButton.pack(fill="both", expand=True, side="left")
ResetButton = tk.Button(BottomFrame, image=UndoImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT, command=reset_image)
ResetButton.pack(fill="both", expand=True, side="left")

Separator2 = tk.Label(BottomFrame, text="          ", bg=Lightest) # Makes space on the bottom row
Separator2.pack(fill="both", expand=True, side="left")

# Bottom Text Descriptions and padding:

Separator3 = tk.Label(BottomDescriptions, text="          ", bg=Lightest)
Separator3.pack(fill="both", expand=True, side="left")

BAndLDescription = tk.Label(BottomDescriptions, text="Black & White", bg=Lightest, fg=DescriptionTextColor)
BAndLDescription.pack(fill="both", expand=True, side="left")
GrayDescription = tk.Label(BottomDescriptions, text="   Grayscale   ", bg=Lightest, fg=DescriptionTextColor)
GrayDescription.pack(fill="both", expand=True, side="left")
FlipHDescription = tk.Label(BottomDescriptions, text="Horizontal Flip", bg=Lightest, fg=DescriptionTextColor)
FlipHDescription.pack(fill="both", expand=True, side="left")
FlipVDescription = tk.Label(BottomDescriptions, text=" Vertical Flip ", bg=Lightest, fg=DescriptionTextColor)
FlipVDescription.pack(fill="both", expand=True, side="left")
ScaleDescription = tk.Label(BottomDescriptions, text="         Scale      ", bg=Lightest, fg=DescriptionTextColor)
ScaleDescription.pack(fill="both", expand=True, side="left")
InvertDescription = tk.Label(BottomDescriptions, text="    Invert Color ", bg=Lightest, fg=DescriptionTextColor)
InvertDescription.pack(fill="both", expand=True, side="left")
CropDescription = tk.Label(BottomDescriptions, text="  Pop Image ", bg=Lightest, fg=DescriptionTextColor)
CropDescription.pack(fill="both", expand=True, side="left")
RotateDescription = tk.Label(BottomDescriptions, text="  Rotate Image ", bg=Lightest, fg=DescriptionTextColor)
RotateDescription.pack(fill="both", expand=True, side="left")
UndoDescription = tk.Label(BottomDescriptions, text="  Reset Image    ", bg=Lightest, fg=DescriptionTextColor)
UndoDescription.pack(fill="both", expand=True, side="left")

Separator4 = tk.Label(BottomDescriptions, text="          ", bg=Lightest)
Separator4.pack(fill="both", expand=True, side="left")

root.mainloop()
