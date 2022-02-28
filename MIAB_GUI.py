# AUTHOR: Lauren Ruff
# Email: ruffl@oregonstate.edu
# Assignment: 8, Integration
# Due Date: February 28, 2022
# Version: 1.1
# File: MIAB_GUI.py
# Description: This file contains the code for creating the GUI the user will interact with in encode messages into
#              images and decode messages from images.

import os.path
import tkinter as tk
from tkinter import ttk, Text, filedialog, Entry
from PIL import Image, ImageTk
import webbrowser
import time

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

    # add the widgets to the screen
    help_btn.grid(row=0, column=1, ipadx=3, ipady=3, padx=7, pady=7, sticky=tk.NE)
    welcome_label_1.grid(row=1, column=0, columnspan=2)
    welcome_label_2.grid(row=2, column=0, columnspan=2)
    encode_btn.grid(row=3, column=0,  ipadx=7, ipady=7, sticky=tk.N)
    decode_btn.grid(row=3, column=1, ipadx=7, ipady=7, sticky=tk.N)

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
    print(img_path_e)

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
                              command=lambda: browse_btn_press(img_label_e))
    encode_msg_btn = ttk.Button(encode_frame,
                                text='Encode Message',
                                command=lambda: encode_msg_press())
    export_btn = ttk.Button(encode_frame,
                            text='Export',
                            command=lambda: export_btn_press(img_path_e))
    email_btn = ttk.Button(encode_frame,
                           text='Email',
                           command=lambda: email_btn_press(img_path_e))
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

    # creating other widgets
    user_input_e.grid(column=1, row=1, sticky=tk.N)
    user_input_e.insert('1.0', "This is a default message. Delete me and write your own!")
    browse_btn_e.grid(column=0, row=1, ipady=5, sticky=tk.S)
    encode_msg_btn.grid(column=1, row=1, ipady=5, sticky=tk.S)
    export_btn.grid(column=0, row=3, ipady=5)
    email_btn.grid(column=1, row=3, ipady=5)
    help_btn.grid(column=1, row=0, ipadx=3, ipady=3, padx=7, pady=7, sticky=tk.NE)
    back_btn.grid(column=0, row=0, ipadx=3, ipady=3, padx=7, pady=7, sticky=tk.NW)

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

    # create the grid
    row_column_config(decode_frame)

    decode_label = ttk.Label(decode_frame,
                             text="Decode a Message",
                             font=("Garamond", 18))
    img_label_d = tk.Label(decode_frame)
    browse_btn_d = ttk.Button(decode_frame,
                              text='Browse',
                              command=lambda: browse_btn_press(img_label_d))
    user_input_d = Text(decode_frame,
                        height=18.5,
                        width=40,
                        wrap='word')
    decode_msg_btn = ttk.Button(decode_frame,
                                text='Decode Message',
                                command=lambda: decode_msg_press())
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

    load_img(img_label_d, "")

    # put widgets in frame
    back_btn.grid(column=0, row=0, ipadx=3, ipady=3, padx=7, pady=7, sticky=tk.NW)
    user_input_d.grid(column=1, row=1, sticky=tk.N)
    user_input_d.insert('1.0', 'The decoded message will appear here')
    user_input_d.config(state=tk.DISABLED)

    browse_btn_d.grid(column=0, row=1, ipady=5, sticky=tk.S)
    decode_msg_btn.grid(column=1, row=1, ipady=5, sticky=tk.S)
    reply_btn.grid(column=0, row=3, columnspan=2, ipady=5)
    help_btn.grid(column=1, row=0, ipadx=3, ipady=3, padx=7, pady=7, sticky=tk.NE)

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

    encode_help = ttk.Label(help_frame,
                            text='These are the instructions for encoding a message in an image',
                            font=("Garamond", 16),
                            wraplength=400)
    decode_help = ttk.Label(help_frame,
                            text='These are the instructions for decoding a message from an image',
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

    encode_help.grid(column=0, row=1, sticky=tk.N)
    decode_help.grid(column=1, row=1, sticky=tk.N)
    more_info.grid(column=0, row=2, columnspan=2, sticky=tk.S)
    more_info_link.grid(column=0, row=3, columnspan=2, ipadx=2, sticky=tk.N)
    more_info_link.bind("<Button-1>", lambda e: hyperlink())
    back_btn.grid(column=0, row=0, ipadx=3, ipady=3, padx=7, pady=7, sticky=tk.NW)

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

    left = 0    # x
    upper = 0   # y
    right = w   # x
    lower = h   # y

    if w == h:
        # if the image is already square, do nothing
        pass

    elif w > h:  # if x > y

        # if the width is longer than the height, crop the width
        diff = (w - h) // 2

        left = diff
        right = w - diff

    else:  # h > w: if y > x
        # if the height is taller than the width, crop the height
        diff = (h - w) // 2

        upper = diff
        lower = h - diff

    # return the tuple
    return left, upper, right, lower


def load_img(label, path):
    """
    this function loads the image into the GUI. It also calls the get_crop_size method to crop the image to a square
    :param label: either encode or decode, depending on which window is open
    :param path: the path to the image
    """

    # default for the 'decode' window - no photo will be preemptively chosen
    default = 'Click ''Browse'' to select an image'
    default_msg = ttk.Label(decode_frame,
                            text=default,
                            font=("Garamond", 12))

    if path != "":  # if there is an image path

        # forget the default message
        default_msg.grid_forget()

        # open the image
        img = Image.open(path)

        # crop the image
        w, h = img.size
        size_tuple = get_crop_size(w, h)
        img = img.crop(size_tuple)

        # resize the image so it fits in the GUI window
        resize = (340, 340)
        img2 = ImageTk.PhotoImage(img.resize(resize))

        # add the image to the grid
        label.Image = img2
        label.configure(image=img2)
        label.grid(column=0, row=1, sticky=tk.N)

    else:
        # else, add the default message to the grid
        default_msg.grid(column=0, row=1)


# ----------------- STEGANOGRAPHY -----------------
# ----------------- NEED TO IMPLEMENT -----------------
def encode_msg_press():
    pass


def decode_msg_press():
    pass


# ----------------- BUTTON FUNC -----------------
def email_btn_press(img_path):
    """
    This function opens a popup window that allows the user to enter information that will be used by the email service
    to send an email. The sender email and recipient email are required.
    :param img_path: the path to the image with the encoded message
    """
    # create the window
    email_popup = tk.Tk()
    email_popup.geometry("550x350")
    email_popup.eval('tk::PlaceWindow . center')
    miab_gui_service.resizable(False, False)

    # configure the grid
    email_popup.columnconfigure(0, weight=1)
    email_popup.columnconfigure(1, weight=1)
    email_popup.rowconfigure(0, weight=1)
    email_popup.rowconfigure(1, weight=1)
    email_popup.rowconfigure(2, weight=1)
    email_popup.rowconfigure(3, weight=1)
    email_popup.rowconfigure(4, weight=2)

    def write_to_file(s, r, sub, msg):
        """
        inner function that takes the users input from the GUI, stores it in a file, and waits for the email to be sent
        :param s: sender's email
        :param r: recipient's email
        :param sub: subject line for the email
        :param msg: body of the email
        :return: nothing, used to stop execution of this method
        """

        if s is None or r is None:
            # check that the user has entered a sender and recipient email
            popup("sender and recipient email are required!")
            return

        # data to store in the file as a string
        data = s + '\n' + r + '\n' + sub + '\n' + img_path + '\n' + msg

        # file paths to look for
        file_path = os.environ["USERPROFILE"] + "\\Desktop\\email_service_data\\email_data.txt"
        success_file = os.environ["USERPROFILE"] + "\\Desktop\\email_service_data\\success.txt"
        fail_file = os.environ["USERPROFILE"] + "\\Desktop\\email_service_data\\fail.txt"

        with open(file_path, 'w') as e_data:
            # write data to the file
            e_data.write(data)

        # destroy the email popup
        email_popup.destroy()

        while not os.path.exists(success_file) or not os.path.exists(fail_file):
            # wait for a file path to exist before returning to normal function
            time.sleep(1)

        if os.path.exists(success_file):
            os.remove(success_file)

        if os.path.exists(fail_file):
            os.remove(fail_file)

        return

        # if os.path.exists(success_file):
        #     popup("Email successfully sent")
        # elif os.path.exists(success_file):
        #     popup("Email failed to send")

    s_email_entry = Entry(email_popup, width=45)
    s_email_entry.delete(0, tk.END)

    r_email_entry = Entry(email_popup, width=45)
    r_email_entry.delete(0, tk.END)

    subject_entry = Entry(email_popup, width=70)
    subject_entry.delete(0, tk.END)

    message_entry = Text(email_popup, height=5, width=60)
    # message_entry.delete("start", "end")

    send_button = ttk.Button(email_popup,
                             text="Send",
                             command=lambda: write_to_file(s_email_entry.get(),
                                                           r_email_entry.get(),
                                                           subject_entry.get(),
                                                           message_entry.get("1.0", "end-1c"))
                             )

    cancel_btn = ttk.Button(email_popup, text='Cancel', command=lambda: email_popup.destroy())

    # add widgets into window grid
    ttk.Label(email_popup,
              text="Please fill out the following information to send your email:").grid(row=0,
                                                                                         column=0,
                                                                                         columnspan=2,
                                                                                         sticky=tk.N)
    ttk.Label(email_popup, text="Sender's Email:").grid(row=1, column=0, sticky=tk.N)
    s_email_entry.grid(row=1, column=0, sticky=tk.S)
    ttk.Label(email_popup, text="Recipient's Email:").grid(row=1, column=1, sticky=tk.N)
    r_email_entry.grid(row=1, column=1, sticky=tk.S)
    ttk.Label(email_popup, text="Subject:").grid(row=2, column=0, columnspan=2, sticky=tk.N)
    subject_entry.grid(row=2, column=0, columnspan=2, sticky=tk.S)
    ttk.Label(email_popup, text="Message:").grid(row=3, column=0, columnspan=2, sticky=tk.N)
    message_entry.grid(row=3, column=0, columnspan=2, sticky=tk.S)
    send_button.grid(row=4, column=0)
    cancel_btn.grid(row=4, column=1)

    # show window
    email_popup.mainloop()


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
    else:
        # else tell the user no image was selected and do nothing
        popup("No image selected")


def export_btn_press(file_path):
    """
    This function opens a file dialog that allows the user to export an image at the given path
    :param file_path: the file path to the image
    """
    # browse for an image file

    # COMMENT: adapted from the source link for saving a file
    # DATE: February 14, 2022
    # SOURCE: https://www.geeksforgeeks.org/python-asksaveasfile-function-in-tkinter/

    initial_dir = os.environ["USERPROFILE"] + "\\Desktop"

    # open the file dialog to the users desktop, only allow images to be saved as .png or .jpg
    file_loc = filedialog.asksaveasfilename(title='Save your image',
                                            initialdir=initial_dir,
                                            filetypes=[(".png", ".png"), (".jpg", ".jpg")])
    if file_loc != "":
        # if the file location is not empty, save the image
        img_open = Image.open(file_path)
        img_open.save(file_loc)

        popup("Image successfully saved!")

    else:
        # else, print an error that the image was not saved
        popup("Image not saved")


# ----------------- GENERIC "POP-UP" GUI -----------------
def popup(msg):
    """
    This is a generic popup for success and error messages to be shown to the user
    :param msg: the message to be printed in the popup
    """
    popup_wind = tk.Tk()
    popup_wind.geometry("200x50")
    popup_wind.eval('tk::PlaceWindow . center')
    miab_gui_service.resizable(False, False)
    popup_wind.title("")
    ttk.Label(popup_wind, text=msg).pack()

    popup_wind.mainloop()

    # window will be destroyed after 5 seconds if the user does not click the x button
    popup_wind.after(5000, lambda: popup_wind.destroy())  # destroy window after 5 seconds


# ----------------- THE GUI -----------------
def MIAB_GUI():
    # custom for MIAB - icon and title
    miab_gui_service.title("Message in a Bottle")
    miab_gui_service.iconbitmap("./MIAB_icon.ico")
    miab_gui_service.resizable(False, False)

    window_height = 700
    window_width = 900

    # code that centers the window on the computer screen
    # CITATION: adapted from source link for centering a tkinter window on any computer screen
    # DATE: February 13, 2022
    # SOURCE: https://www.pythontutorial.net/tkinter/tkinter-window/

    # get screen height and width
    screen_height = miab_gui_service.winfo_screenheight()
    screen_width = miab_gui_service.winfo_screenwidth()

    # calculate x and y offsets using screen h/w and gui h/w
    center_wind_x = int(screen_width / 2 - window_width / 2)
    center_wind_y = int(screen_height / 2 - window_height / 2)

    miab_gui_service.geometry(f'{window_width}x{window_height}+{center_wind_x}+{center_wind_y}')

    # open the welcome screen widgets
    welcome_screen_on()

    # displays the window
    miab_gui_service.mainloop()


if __name__ == "__main__":
    MIAB_GUI()
