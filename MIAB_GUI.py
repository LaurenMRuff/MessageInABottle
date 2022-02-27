# AUTHOR: Lauren Ruff
# Email: ruffl@oregonstate.edu
# Assignment: 8, Integration
# Due Date: February 28, 2022
# Version: 1.0
# File: MIAB_GUI.py
# Description: This file contains the code for creating the GUI the user will interact with and eventually will include
#              all button functionality

import os.path
import tkinter as tk
from tkinter import ttk, Text, filedialog, Entry, StringVar
from PIL import Image, ImageTk
import webbrowser

miab_gui_service = tk.Tk()

welcome_frame = tk.Frame(miab_gui_service)
encode_frame = tk.Frame(miab_gui_service)
decode_frame = tk.Frame(miab_gui_service)
help_frame = tk.Frame(miab_gui_service)


# ----------------- SCREENS -----------------
def welcome_screen_on():

    welcome_frame.rowconfigure(0, weight=1)
    welcome_frame.rowconfigure(1, weight=1)
    welcome_frame.rowconfigure(2, weight=1)
    welcome_frame.rowconfigure(3, weight=1)
    welcome_frame.columnconfigure(0, weight=1)
    welcome_frame.columnconfigure(1, weight=1)

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
    # remove the welcome screen widgets
    welcome_frame.forget()


def encode_screen_on():
    # turn other screens off
    welcome_screen_off()
    decode_screen_off()
    help_screen_off()

    # create the grid
    encode_frame.rowconfigure(0, weight=1)
    encode_frame.rowconfigure(1, weight=1)
    encode_frame.rowconfigure(2, weight=1)
    encode_frame.rowconfigure(3, weight=1)
    encode_frame.columnconfigure(0, weight=1)
    encode_frame.columnconfigure(1, weight=1)

    # get the image
    img_path_e = get_image()

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
    encode_frame.forget()


def decode_screen_on():
    # turn other screens off
    welcome_screen_off()
    encode_screen_off()
    help_screen_off()

    # create the grid
    decode_frame.rowconfigure(0, weight=1)
    decode_frame.rowconfigure(1, weight=1)
    decode_frame.rowconfigure(2, weight=1)
    decode_frame.rowconfigure(3, weight=1)
    decode_frame.columnconfigure(0, weight=1)
    decode_frame.columnconfigure(1, weight=1)

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
    decode_frame.forget()


def help_screen_on():
    # turn other screens off
    welcome_screen_off()
    decode_screen_off()
    encode_screen_off()

    help_link = "https://www.mygreatlearning.com/blog/image-steganography-explained/"

    # create the grid
    help_frame.rowconfigure(0, weight=1)
    help_frame.rowconfigure(1, weight=7)
    help_frame.rowconfigure(2, weight=1)
    help_frame.rowconfigure(3, weight=1)
    help_frame.columnconfigure(0, weight=1)
    help_frame.columnconfigure(1, weight=1)

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
    help_frame.forget()


def back_btn_press():
    welcome_screen_on()
    encode_screen_off()
    decode_screen_off()
    help_screen_off()


# ----------------- IMG DISPLAY -----------------
def get_image():
    # will get image from partner's image service

    img_path = "./MIAB_DEFAULT.jpg"

    return img_path


def get_crop_size(w, h):
    if w == h:
        # if the image is already square, return the current height and width
        return 0, 0, w, h

    elif w > h:

        # if the width is longer than the height, crop the width
        diff = (w - h) // 2

        upper = diff
        lower = w - diff

        return 0, upper, h, lower

    else:
        # h > w
        # if the height is taller than the width, crop the height
        diff = (h - w) // 2

        left = diff
        right = h - diff

        return 0, left, w, right


def load_img(label, path):
    default = 'Click ''Browse'' to select an image'
    default_msg = ttk.Label(miab_gui_service,
                            text=default,
                            font=("Garamond", 12))

    if path != "":

        default_msg.grid_forget()

        # crop the image to be a square
        resize = (340, 340)
        img = Image.open(path)

        w, h = img.size

        size_tuple = get_crop_size(w, h)

        img = img.crop(size_tuple)

        img2 = ImageTk.PhotoImage(img.resize(resize))
        label.Image = img2
        label.configure(image=img2)

        label.grid(column=0, row=1, sticky=tk.N)

    else:
        default_msg.grid(column=0, row=1)


# ----------------- STEGANOGRAPHY -----------------
def encode_msg_press():
    pass


def decode_msg_press():
    pass


# ----------------- BUTTON FUNC -----------------
def email_btn_press(img_path):
    # create the window
    email_popup = tk.Tk()
    email_popup.geometry("350x250")
    email_popup.eval('tk::PlaceWindow . center')

    # configure the grid
    email_popup.columnconfigure(0, weight=1)
    email_popup.columnconfigure(1, weight=1)
    email_popup.rowconfigure(0, weight=3)
    email_popup.rowconfigure(1, weight=3)
    email_popup.rowconfigure(2, weight=1)

    def write_to_file(s, r, sub, msg):
        data = s + '\n' + r + '\n' + sub + '\n' + img_path + '\n' + msg
        file_path = os.path.abspath("email_service_data/email_data.txt")
        with open(file_path, 'w') as e_data:
            e_data.write(data)

    # create widgets
    sender = recipient = e_sub = e_msg = StringVar()
    s_email_entry = Entry(email_popup, textvariable=sender, width=50)
    s_email_entry.delete(0, tk.END)

    r_email_entry = Entry(email_popup, textvariable=recipient, width=50)
    r_email_entry.delete(0, tk.END)

    subject_entry = Entry(email_popup, textvariable=e_sub, width=50)
    subject_entry.delete(0, tk.END)

    message_entry = Entry(email_popup, textvariable=e_msg, width=50)
    message_entry.delete(0, tk.END)

    send_button = ttk.Button(email_popup, text="Send", command=lambda: write_to_file(sender.get(), recipient.get(),
                                                                                     e_sub.get(), e_msg.get()))

    cancel_btn = ttk.Button(email_popup, text='Cancel', command=lambda: email_popup.destroy())

    # pack widgets into window
    ttk.Label(email_popup,
              text="Please fill out the following information to send your email:").grid(row=0,
                                                                                         column=0,
                                                                                         columnspan=2,
                                                                                         sticky=tk.N)
    ttk.Label(email_popup, text="Sender's Email:").grid(row=1, column=0, sticky=tk.N)
    s_email_entry.grid(row=1, column=0)
    ttk.Label(email_popup, text="Recipient's Email:").grid(row=1, column=1, sticky=tk.N)
    r_email_entry.grid(row=1, column=1)
    ttk.Label(email_popup, text="Subject:").grid(row=2, column=0, columnspan=2, sticky=tk.N)
    subject_entry.grid(row=2, column=0)
    ttk.Label(email_popup, text="Message:").grid(row=2, column=1, columnspan=2, sticky=tk.N)
    message_entry.grid(row=2, column=1)
    send_button.grid(row=3, column=0)
    cancel_btn.grid(row=3, column=1)

    # show window
    email_popup.mainloop()


def browse_btn_press(label):
    # browse for a png file
    # COMMENT: adapted from the source link for opening a browse window for files
    # DATE: February 14, 2022
    # SOURCE: https://docs.python.org/3/library/dialog.html,
    #         https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
    #
    # initial_dir = "C:/Users/" + str(getpass.getuser()) + "/Desktop"
    #
    # filename = filedialog.askopenfilename(title='Select an Image',
    #                                       initialdir=initial_dir,
    #                                       filetypes=[(".png, .jpg", ".png .jpg")])
    #
    #
    # if filename != "":
    #     # if a file is selected, open the image and format it, otherwise do nothing
    #     load_img(filename)
    #     return filename
    popup("Will browse for image")


def export_btn_press(path):
    # browse for a png file

    # COMMENT: adapted from the source link for saving a file
    # DATE: February 14, 2022
    # SOURCE: https://www.geeksforgeeks.org/python-asksaveasfile-function-in-tkinter/

    initial_dir = os.path.abspath("/Desktop")

    file_loc = filedialog.asksaveasfilename(title='Save your image',
                                            initialdir=initial_dir,
                                            filetypes=[(".png", ".png")])
    if file_loc != "":

        img_open = Image.open(path)
        img_open.save(file_loc)

        popup("Image successfully saved!")

    else:
        popup("Image not saved")


# ----------------- GENERAL "POP-UP" GUI -----------------
def popup(msg):
    popup_wind = tk.Tk()
    popup_wind.geometry("350x100")
    popup_wind.eval('tk::PlaceWindow . center')
    popup_wind.title("")
    ttk.Label(popup_wind, text=msg).pack()

    popup_wind.after(5000, lambda: popup_wind.destroy())  # destroy window after 5 seconds

    popup_wind.mainloop()


# ----------------- THE GUI -----------------
def MIAB_GUI():
    # custom for MIAB - icon and title
    miab_gui_service.title("Message in a Bottle")
    miab_gui_service.iconbitmap("./MIAB_icon.ico")

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
