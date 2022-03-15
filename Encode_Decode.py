# AUTHOR: Lauren Ruff
# Email: ruffl@oregonstate.edu
# Assignment: 10, Portfolio
# Due Date: March 18, 2022
# Version: 3.1, Release
# File: Encode_Decode.py
# Description: This file contains the algorithm for encoding or decoding a message from a photo (png or jgp) adapted
#              from a Geeks2Geeks article. Source Code can be found at the SOURCE link. It also contains functions for
#              generating popups and centering windows on the screen
#
# Source: https://www.geeksforgeeks.org/image-based-steganography-using-python/

import cv2
from file_read_backwards import FileReadBackwards
import os
import tkinter as tk
from tkinter import ttk


# ----------------- GENERIC "POP-UP" GUI -----------------
def popup(msg):
    """
    This is a generic popup for success and error messages to be shown to the user
    :param msg: the message to be printed in the popup
    """
    popup_wind = tk.Tk()
    w, h = 300, 30

    # get screen height and width
    center_screen(popup_wind, w, h)

    popup_wind.title("")
    ttk.Label(popup_wind, text=msg).pack()

    popup_wind.mainloop()

    # window will be destroyed after 5 seconds if the user does not click the x button
    popup_wind.after(5000, lambda: popup_wind.destroy())  # destroy window after 5 seconds


# ----------------- SCREEN CONFIG FUNCTION(S) -----------------
def center_screen(frame, w, h):
    # code that centers the window on the computer screen
    # CITATION: adapted from source link for centering a tkinter window on any computer screen
    # DATE: February 13, 2022
    # SOURCE: https://www.pythontutorial.net/tkinter/tkinter-window/

    # get screen height and width
    screen_height = frame.winfo_screenheight()
    screen_width = frame.winfo_screenwidth()

    # calculate x and y offsets using screen h/w and gui h/w
    center_wind_x = int(screen_width / 2 - w / 2)
    center_wind_y = int(screen_height / 2 - h / 2)

    frame.geometry(f'{w}x{h}+{center_wind_x}+{center_wind_y}')
    frame.resizable(False, False)


# ----------------- ENCODE FUNCTION(S) -----------------
def encode(msg, img_path):
    # open the image and create a copy in the encoded_images location
    img = cv2.imread(img_path)
    head_tail = os.path.split(img_path)
    ext = os.path.splitext(head_tail[1])
    enc_file_loc = os.environ["USERPROFILE"] + "\\Desktop\\EncodedMessages\\" + ext[0] + "_encoded" + ext[1]
    cv2.imwrite(enc_file_loc, img)

    msg_str = "\n" + msg.strip() + "\n" + str(len(msg.strip()))

    # append it to the end of the image file, save and close the image
    with open(enc_file_loc, "a") as f:
        f.write(msg_str)
    f.close()

    return enc_file_loc


# ----------------- DECODE FUNCTION(S) -----------------
def decode(img_path):
    # open the file for reading and get the last line in the file

    char_count = 0
    msg_chars = 0
    decoded_msg = ''

    with FileReadBackwards(img_path, encoding="utf-8") as f:
        for line in f:
            if msg_chars == 0:
                try:
                    msg_chars = int(line)

                except UnicodeDecodeError:
                    return -1

            else:
                char_count += len(line)

                decoded_msg = str(line) + decoded_msg

                if char_count == msg_chars:
                    break
    f.close()

    return decoded_msg
