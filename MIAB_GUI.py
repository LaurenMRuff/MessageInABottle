# AUTHOR: Lauren Ruff
# Email: ruffl@oregonstate.edu
# Assignment: 10, Portfolio
# Due Date: March 18, 2022
# Version: 3.0, Release
# File: MIAB_GUI.py
# Description: This file contains the code for creating the GUI the user will interact with in encode messages into
#              images and decode messages from images.

import os.path
import tkinter as tk
from tkinter import ttk, Text, filedialog
from PIL import Image, ImageTk
import webbrowser
from Encode_Decode import encode, decode, popup, center_screen
import sys

# tkinter object and frames
miab_gui_service = tk.Tk()

welcome_frame = tk.Frame(miab_gui_service)
encode_frame = tk.Frame(miab_gui_service)
decode_frame = tk.Frame(miab_gui_service)
help_frame = tk.Frame(miab_gui_service)


# ----------------- GRID CONFIG -----------------
def row_column_config(frame):
    """
    configures the rows and columns of the passed frame
    :param frame: widget frame, either welcome, encode, decode, or help frame
    """

    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)
    frame.rowconfigure(3, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)


# ----------------- SCREENS -----------------
def welcome_screen_on():
    """
    turns the welcome screen widgets on
    """

    row_column_config(welcome_frame)

    # welcome screen widgets
    welcome_label_1 = ttk.Label(
        welcome_frame,
        text='Welcome to Message in a Bottle!',
        font=("Garamond", 24))
    welcome_label_2 = ttk.Label(
        welcome_frame,
        text='Click the buttons below to get started or the help button to learn more!',
        font=("Garamond", 14))
    encode_btn = ttk.Button(welcome_frame,
                            text="encode a message",
                            command=lambda: encode_screen_on())
    decode_btn = ttk.Button(welcome_frame,
                            text="decode a message",
                            command=lambda: decode_screen_on())
    help_btn = ttk.Button(welcome_frame,
                          text='help',
                          command=lambda: help_screen_on())

    # add the widgets to the frame
    help_btn.grid(row=0, column=1, ipadx=3, ipady=3, padx=7, pady=7, sticky=tk.NE)
    welcome_label_1.grid(row=1, column=0, columnspan=2)
    welcome_label_2.grid(row=2, column=0, columnspan=2)
    encode_btn.grid(row=3, column=0, ipadx=7, ipady=7, sticky=tk.N)
    decode_btn.grid(row=3, column=1, ipadx=7, ipady=7, sticky=tk.N)

    # add the frame to the window
    welcome_frame.pack(fill=tk.BOTH, expand=True)


def welcome_screen_off():
    """
    turns the welcome screen widgets off
    """

    welcome_frame.forget()


def encode_screen_on():
    """
    turns the encode screen widgets on
    """

    # turn other screens off
    welcome_screen_off()
    decode_screen_off()
    help_screen_off()

    # create the grid
    row_column_config(encode_frame)

    # get the image
    img_path_e = get_image()

    def getImgPath():
        # store the image path
        nonlocal img_path_e
        img_path_e = browse_btn_press(img_label_e)

    def getEncodedImgPath():
        # store the new encoded image path and display the image
        nonlocal img_path_e
        img_path_e = encode_msg_press(user_input_e.get("1.0", tk.END), img_path_e)
        load_img(img_label_e, img_path_e)

    # create the widgets
    encode_label = ttk.Label(encode_frame,
                             text="Encode a Message",
                             font=("Garamond", 18))
    img_label_e = tk.Label(encode_frame)
    user_input_e = Text(encode_frame,
                        height=18.5,
                        width=40,
                        wrap='word')
    browse_btn_e = ttk.Button(encode_frame,
                              text='Browse',
                              command=lambda: getImgPath())
    encode_msg_btn = ttk.Button(encode_frame,
                                text='Encode Message',
                                command=lambda: getEncodedImgPath())
    help_btn = ttk.Button(encode_frame,
                          text='help',
                          command=lambda: help_screen_on())
    back_btn = ttk.Button(encode_frame,
                          text='back',
                          command=lambda: back_btn_press())

    encode_label.grid(column=0, row=0, columnspan=2)

    # load the image
    load_img(img_label_e, img_path_e)

    # reset from decode screen being on
    user_input_e.config(state=tk.NORMAL)
    user_input_e.delete("1.0", "end")

    # adding the widgets to the frame
    help_btn.grid(column=1, row=0, ipadx=3, ipady=3, padx=7, pady=7, sticky=tk.NE)
    back_btn.grid(column=0, row=0, ipadx=3, ipady=3, padx=7, pady=7, sticky=tk.NW)
    user_input_e.grid(column=1, row=1, sticky=tk.N)
    user_input_e.insert('1.0', "This is a default message. Delete me and write your own, then click the \"Encode "
                               "Message\" button to encode your message in the selected image!")
    browse_btn_e.grid(column=0, row=1, ipady=5, sticky=tk.S)
    encode_msg_btn.grid(column=1, row=1, ipady=5, sticky=tk.S)

    # add the frame to the window
    encode_frame.pack(fill=tk.BOTH, expand=True)


def encode_screen_off():
    """
    turns the encode screen widgets off
    """

    encode_frame.forget()


def decode_screen_on():
    """
    turns the decode screen widgets on
    """

    # turn other screens off
    welcome_screen_off()
    encode_screen_off()
    help_screen_off()
    path = ""
    msg = "Click \"Decode Message\" to decode the message from the selected image. " \
          "The decoded message will appear here."

    def get_img_path():
        # stores the path of the current image
        nonlocal path
        path = browse_btn_press(img_label_d)

    def get_decoded_msg():
        # runs the decode_msg_press function and adds it to the text widget
        nonlocal msg, user_input_d
        msg = decode_msg_press(path)
        user_input_d.config(state=tk.NORMAL)
        user_input_d.delete(1.0, "end")
        user_input_d.insert(1.0, msg)
        user_input_d.config(state=tk.DISABLED)

    # create the grid
    row_column_config(decode_frame)

    # create labels and buttons
    decode_label = ttk.Label(decode_frame,
                             text="Decode a Message",
                             font=("Garamond", 18))
    img_label_d = tk.Label(decode_frame)
    browse_btn_d = ttk.Button(decode_frame,
                              text='Browse',
                              command=lambda: get_img_path())
    user_input_d = Text(decode_frame,
                        height=18.5,
                        width=40,
                        wrap='word')
    decode_msg_btn = ttk.Button(decode_frame,
                                text='Decode Message',
                                command=lambda: get_decoded_msg())
    reply_btn = ttk.Button(decode_frame,
                           text='Reply',
                           command=lambda: encode_screen_on())
    help_btn = ttk.Button(decode_frame,
                          text='help',
                          command=lambda: help_screen_on())
    back_btn = ttk.Button(decode_frame,
                          text='back',
                          command=lambda: back_btn_press())

    decode_label.grid(column=0, row=0, columnspan=2)

    # put widgets in frame
    load_img(img_label_d, path)

    back_btn.grid(column=0, row=0, ipadx=3, ipady=3, padx=7, pady=7, sticky=tk.NW)
    user_input_d.grid(column=1, row=1, sticky=tk.N)
    user_input_d.insert('1.0', msg)
    user_input_d.config(state=tk.DISABLED)

    browse_btn_d.grid(column=0, row=1, ipady=5, sticky=tk.S)
    decode_msg_btn.grid(column=1, row=1, ipady=5, sticky=tk.S)
    reply_btn.grid(column=0, row=3, columnspan=2, ipady=5)
    help_btn.grid(column=1, row=0, ipadx=3, ipady=3, padx=7, pady=7, sticky=tk.NE)

    # add the frame to the window
    decode_frame.pack(fill=tk.BOTH, expand=True)


def decode_screen_off():
    """
    turns the decode screen widgets off
    """

    decode_frame.forget()


def help_screen_on():
    """
    turns the help screen widgets on
    """

    # turn other screens off
    welcome_screen_off()
    decode_screen_off()
    encode_screen_off()

    help_link = "https://www.mygreatlearning.com/blog/image-steganography-explained/"

    # create the grid
    row_column_config(help_frame)
    help_frame.rowconfigure(1, weight=7)

    encode_help_text = "Instructions to Encode a Message: \n\n" \
                       "1. An image is pre-populated for you to use, or click the \"browse\" button to select an " \
                       "image of your own!\n\n" \
                       "2. Delete the default text from the text box on the left and type in your own message.\n\n" \
                       "3. When both the image and message are ready, click the \"Encode\" button below the text box." \
                       "\n\n" \
                       "4. If the message was encoded, you will receive a popup message.\n\n" \
                       "5. You will find your encoded image on your desktop in a folder called EncodedMessages with " \
                       "a file name that ends in \"_encoded\""
    decode_help_text = "Instructions to Decode a Message: \n\n" \
                       "1. Click the \"browse\" button to select an image that has an encoded message.\n\n" \
                       "2. Click \"Decode\" to run the image through the decoding algorithm and extract the message." \
                       "\n\n" \
                       "3. The decoded message will appear in the text box on the right hand side of the screen.\n\n" \
                       "4. If you wish to reply to the message immediately, click \"Reply\" and you will be taken to " \
                       "the Encode a Message screen.\n" \

    # create the widgets
    encode_help = ttk.Label(help_frame,
                            text=encode_help_text,
                            font=("Garamond", 16),
                            wraplength=400)
    decode_help = ttk.Label(help_frame,
                            text=decode_help_text,
                            font=("Garamond", 16),
                            wraplength=400)
    more_info = ttk.Label(help_frame,
                          text='Click this link for more information on steganography:',
                          font=("Garamond", 14))
    more_info_link = ttk.Label(help_frame,
                               text=help_link,
                               font=("Garamond", 16),
                               foreground='blue')
    back_btn = ttk.Button(help_frame,
                          text='back',
                          command=lambda: back_btn_press())

    def hyperlink():
        # CITATION: adapted from source link for opening a link in python
        # DATE: February 13, 2022
        # SOURCE: https://www.tutorialspoint.com/how-to-create-a-hyperlink-with-a-label-in-tkinter
        webbrowser.open_new(help_link)

        # change the color of the link to indicate it was clicked
        more_info_link.configure(foreground="purple")

    miab_gui_service.rowconfigure(1, weight=1)

    # add widgets to the frame
    encode_help.grid(column=0, row=1, sticky=tk.N)
    decode_help.grid(column=1, row=1, sticky=tk.N)
    more_info.grid(column=0, row=2, columnspan=2, sticky=tk.S)
    more_info_link.grid(column=0, row=3, columnspan=2, ipadx=2, sticky=tk.N)
    more_info_link.bind("<Button-1>", lambda e: hyperlink())
    back_btn.grid(column=0, row=0, ipadx=3, ipady=3, padx=7, pady=7, sticky=tk.NW)

    # add frame to the window
    help_frame.pack(fill=tk.BOTH, expand=True)


def help_screen_off():
    """
    turns the help screen widgets off
    """
    help_frame.forget()


def back_btn_press():
    """
    turns on the welcome screen and turns off all other screens when the pack button is pressed
    """
    welcome_screen_on()
    encode_screen_off()
    decode_screen_off()
    help_screen_off()


# ----------------- IMG DISPLAY -----------------
def get_image():
    """
    This function gets an image from my teammates image scraping service. If the image scraping service fails, a default
    image is available
    :return: path to the image
    """

    # will get image from partner's image service

    img_dir = os.environ["USERPROFILE"] + "\\Desktop\\Image_Scraper"

    # look for a png or jpg file in the given directory. If none are found, use the default image
    for file in os.listdir(img_dir):
        if file.endswith(".png") or file.endswith(".jpg"):
            return img_dir + "\\" + file

    # if no image path is returned, return the path to the default image
    img_path = "./MIAB_DEFAULT.jpg"

    return img_path


def get_crop_size(w, h):
    """
    This function calculates the new coordinates of the cropped image based on the images width and height
    :param w: image width
    :param h: image height
    :return: a tuple of the calculated (left, upper, right, lower) coordinates
    """

    # (left, upper) is the (x, y) coordinates of the upper left corner of the image
    # (w, h) is the (x, y) coordinates of the lower right corner of the image
    left = 0
    upper = 0
    right = w
    lower = h

    if w > h:
        # if the width is longer than the height, crop the width
        left = (w - h) // 2
        right = w - ((w - h) // 2)

    elif h > w:
        # if the height is taller than the width, crop the height
        upper = (h - w) // 2
        lower = h - ((h - w) // 2)

    # return the tuple
    return left, upper, right, lower


def load_img(label, path):
    """
    this function loads the image into the GUI. It also calls the get_crop_size method to crop the image to a square
    :param label: either encode or decode, depending on which window is open
    :param path: the path to the image
    """

    # default for the 'decode' window - no photo will be preemptively chosen
    default = 'Click \"Browse\" to select an image'

    if path != "":  # if there is an image path

        label.configure(text="")

        # open the image
        img = Image.open(path)

        # crop the image
        w, h = img.size
        size_tuple = get_crop_size(w, h)

        if size_tuple[2] != w and size_tuple[3] != h:
            # if the image needs to be cropped, crop it and save
            img = img.crop(size_tuple)
            img.save(path)

        # resize the image so it fits in the GUI window
        resize = (340, 340)
        img2 = ImageTk.PhotoImage(img.resize(resize))

        # add the image to the grid
        label.Image = img2
        label.configure(image=img2)
        label.grid(column=0, row=1, sticky=tk.N)

    else:
        # else add the default message to the label
        label.configure(text=default,
                        font=("Garamond", 16))
        label.grid(column=0, row=1)


# ----------------- STEGANOGRAPHY -----------------
def encode_msg_press(msg, img_path):
    """
    Sends a string message and the image path to the encode function
    opens the export button dialog on success
    :param msg: message to be encoded into the image
    :param img_path: path to the image
    """

    # get the new path, if a new path is found, the message was encoded successfully, return the path
    new_path = encode(msg, img_path)

    if img_path != new_path:
        popup("Message successfully encoded!")

    return new_path


def decode_msg_press(img_path):
    """
    Sends an image path that contains a message to the decode function
    :param img_path: the path to the image
    :return: the message that was in the image as a string
    """

    if img_path == "":
        # if the image path is empty, print message to user
        popup("No image found to decode. Please select an image.")
    else:
        # else, decode the image in the path
        msg = decode(img_path)

        if msg == -1:
            popup("Selected image does not contain a message")
        else:
            return msg


# ----------------- BUTTON FUNC -----------------
def browse_btn_press(frame):
    """
    This function opens a file dialog that allows the user to select an image (.png or .jpg)
    :param frame: either encode or decode, whichever window is open
    """
    # COMMENT: adapted from the source link for opening a browse window for files
    # DATE: February 14, 2022
    # SOURCE: https://docs.python.org/3/library/dialog.html,
    #         https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/

    initial_dir = os.environ["USERPROFILE"] + "\\Desktop"

    filename = filedialog.askopenfilename(title='Select an Image',
                                          initialdir=initial_dir,
                                          filetypes=[(".png, .jpg", ".png .jpg")])

    if filename != "":
        # if a file is selected, open the image and format it
        load_img(frame, filename)
        return filename
    else:
        # else tell the user no image was selected and do nothing
        popup("No image selected")


# ----------------- THE GUI -----------------
def MIAB_GUI():
    # custom for MIAB - icon and title
    miab_gui_service.title("Message in a Bottle")
    miab_gui_service.iconbitmap("./MIAB_icon.ico")
    miab_gui_service.resizable(False, False)

    window_height = 700
    window_width = 900

    # center the screen
    center_screen(miab_gui_service, window_width, window_height)

    # open the welcome screen widgets
    welcome_screen_on()

    # displays the window
    miab_gui_service.mainloop()


if __name__ == "__main__":
    try:
        MIAB_GUI()
    except KeyboardInterrupt:
        sys.exit(0)
