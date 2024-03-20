#---------------------------------------------------------------------------------------------------------------
# Program: Team 1 Photo Editor
# Author(s): Samuel Johnson - - -
# Last Updated: 3/19/2024
# Purpose: To edit the color, rotation, and size of image files.
#---------------------------------------------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk,Image  
from pathlib import Path
from tkinter import font as tkFont
import os

# Declarations: --------------------------------------------------------------------------------

# System:

global CurrentImagePath # The path of the original entered image

ArrayOfTempObjects = [] # Stores each temp object location for deletion

# Palette:

Highlight = "#DFDFDF"
Lightest = "#898989"
MidLightest = "#5C5C5C"
MidDarkest = "#393939"
Darkest = "#000000"

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

# Open file dialogue to get image file, then place the resized dummy version of this image in the editor.
def LoadImage():
    global CurrentImagePath
    # Open the file directory and allow image selection
    file_path = filedialog.askopenfilename( 
        initialdir=os.getcwd(),
        title="Select an image",
        filetypes=(("PNG files", "*.png"),)  # Specify the allowed file types
    )
    if file_path and file_path.lower().endswith((".png", ".PNG")):
        img = Image.open(file_path)
        photo = ImageTk.PhotoImage(img)
        multiplyer = 1
        # Check if image fits within the boundaries of the MainImage element
        if photo.height() > MaxImageSize and photo.width() < MaxImageSize: # If the image is only too tall
            multiplyer = MaxImageSize / photo.height()
        elif photo.width() > MaxImageSize and photo.height() < MaxImageSize: # If the image is only too wide
            multiplyer = MaxImageSize / photo.width()
        elif photo.width() > MaxImageSize and photo.height() > MaxImageSize: # If the image both too tall and too wide
            if photo.height() > photo.width():
                multiplyer = MaxImageSize / photo.height()
            else:
                multiplyer = MaxImageSize / photo.width()
        # Resize the image file if necessary
        new_width = int(photo.width() * multiplyer)
        new_height = int(photo.height() * multiplyer)
        img = img.resize((new_width, new_height), Image.ADAPTIVE)
        photo = ImageTk.PhotoImage(img)
        # Set global variables and update MainImage picture
        CurrentImagePath = file_path
        MainImage.config(image=photo)
        MainImage.image = photo

# Frame setup: --------------------------------------------------------------------------------

TopFrame = ttk.Frame(root)
TopFrame.columnconfigure(0, weight=1)
TopFrame.columnconfigure(1, weight=1)
TopFrame.columnconfigure(2, weight=12)
TopFrame.columnconfigure(3, weight=3)
TopFrame.rowconfigure(0, weight=1)
TopFrame.grid(row=0, column=0, sticky="NWES")

MiddleShadow = ttk.Frame(root)
MiddleShadow.grid(row=1, column=0, sticky="NWES")

MiddleFrame = ttk.Frame(root)
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

LoadButton = tk.Button(TopFrame, image=LoadButtonImage, bg=Lightest, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT, command=LoadImage)
SaveButton = tk.Button(TopFrame, image=SaveImage, bg=Lightest, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT)
HeaderImage = tk.Label(TopFrame, bg=Lightest, fg=TextColor, font=FONT, image=LogoImage)
HeaderText = tk.Label(TopFrame, text="       PHOTO EDITOR  ", bg=Lightest, fg=TextColor, font=FONT)

LoadButton.grid(row=0, column=0, sticky="NWES")
SaveButton.grid(row=0, column=1, sticky="NWES")
HeaderImage.grid(row=0, column=2, sticky="NWES")
HeaderText.grid(row=0, column=3, sticky="NWES")

# Middle section: --------------------------------------------------------------------------------

ShadowLabel1 = tk.Label(MiddleShadow, bg=MidDarkest)
ShadowLabel1.pack(fill="both", side="top", expand=True)

MainImage = tk.Label(MiddleFrame, image=None, bg=Darkest)
MainImage.pack(fill="both", side="top", expand=True)

ShadowLabel2 = tk.Label(EndShadow, bg=Highlight)
ShadowLabel2.pack(fill="both", side="top", expand=True)

# Bottom buttons: --------------------------------------------------------------------------------

ButtonColor = Lightest # Change this value to affect all bottom buttons

Separator1 = tk.Label(BottomFrame, text="          ", bg=ButtonColor) # Makes space on the bottom row
Separator1.pack(fill="both", expand=True, side="left")

BAndWButton = tk.Button(BottomFrame, image=BnWButtonImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT)
BAndWButton.pack(fill="both", expand=True, side="left")
GreyscaleButton = tk.Button(BottomFrame, image=GreyButtonImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT)
GreyscaleButton.pack(fill="both", expand=True, side="left")
FHorizButton = tk.Button(BottomFrame, image=FlipHButtonImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT)
FHorizButton.pack(fill="both", expand=True, side="left")
FVertiButton = tk.Button(BottomFrame, image=FlipVButtonImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT)
FVertiButton.pack(fill="both", expand=True, side="left")
ResizeButton = tk.Button(BottomFrame, image=ResizeImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT)
ResizeButton.pack(fill="both", expand=True, side="left")
InvertButton = tk.Button(BottomFrame, image=InvertImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT)
InvertButton.pack(fill="both", expand=True, side="left")
CropButton = tk.Button(BottomFrame, image=CropImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT)
CropButton.pack(fill="both", expand=True, side="left")
RotateButton = tk.Button(BottomFrame, image=RotateImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT)
RotateButton.pack(fill="both", expand=True, side="left")
ResetButton = tk.Button(BottomFrame, image=UndoImage, bg=ButtonColor, relief=BorderStyle, bd=BorderWidth, fg=TextColor, font=FONT)
ResetButton.pack(fill="both", expand=True, side="left")

Separator2 = tk.Label(BottomFrame, text="          ", bg=ButtonColor) # Makes space on the bottom row
Separator2.pack(fill="both", expand=True, side="left")

# Bottom Text Descriptions and padding:

Separator3 = tk.Label(BottomDescriptions, text="          ", bg=ButtonColor)
Separator3.pack(fill="both", expand=True, side="left")

BAndLDescription = tk.Label(BottomDescriptions, text="Black & White", bg=ButtonColor)
BAndLDescription.pack(fill="both", expand=True, side="left")
GrayDescription = tk.Label(BottomDescriptions, text="   Grayscale   ", bg=ButtonColor)
GrayDescription.pack(fill="both", expand=True, side="left")
FlipHDescription = tk.Label(BottomDescriptions, text="Horizontal Flip", bg=ButtonColor)
FlipHDescription.pack(fill="both", expand=True, side="left")
FlipVDescription = tk.Label(BottomDescriptions, text=" Vertical Flip ", bg=ButtonColor)
FlipVDescription.pack(fill="both", expand=True, side="left")
ScaleDescription = tk.Label(BottomDescriptions, text="         Scale      ", bg=ButtonColor)
ScaleDescription.pack(fill="both", expand=True, side="left")
InvertDescription = tk.Label(BottomDescriptions, text="    Invert Color ", bg=ButtonColor)
InvertDescription.pack(fill="both", expand=True, side="left")
CropDescription = tk.Label(BottomDescriptions, text="  Crop Image ", bg=ButtonColor)
CropDescription.pack(fill="both", expand=True, side="left")
RotateDescription = tk.Label(BottomDescriptions, text="  Rotate Image ", bg=ButtonColor)
RotateDescription.pack(fill="both", expand=True, side="left")
UndoDescription = tk.Label(BottomDescriptions, text="  Reset Image    ", bg=ButtonColor)
UndoDescription.pack(fill="both", expand=True, side="left")

Separator4 = tk.Label(BottomDescriptions, text="          ", bg=ButtonColor)
Separator4.pack(fill="both", expand=True, side="left")

root.mainloop()
