# AUTHOR: Lauren Ruff
# Email: ruffl@oregonstate.edu
# Assignment: 6, minimum viable product (MVP)
# Due Date: February 14 2022
# Version: 1.0
# File: MAIB_GUI.py
# Description: This file contains the code for creating the GUI the user will interact with and eventually will include
#              all button functionality
import getpass
import tkinter as tk
from tkinter import ttk, Text, filedialog
from PIL import Image, ImageTk
import webbrowser

miab_gui_service = tk.Tk()

help_link = "https://www.mygreatlearning.com/blog/image-steganography-explained/"

# know which window is open
encode_on = False
decode_on = False
help_on = False

# welcome screen widgets
welcome_label_1 = ttk.Label(
    miab_gui_service,
    text='Welcome to Message in a Bottle!',
    font=("Garamond", 24))
welcome_label_2 = ttk.Label(
    miab_gui_service,
    text='Click the buttons below to get started or the help button to learn more!',
    font=("Garamond", 14))
back_btn = ttk.Button(miab_gui_service,
                      text='back')
help_btn = ttk.Button(miab_gui_service,
                      text='help')
encode_btn = ttk.Button(miab_gui_service,
                        text="encode a message")
decode_btn = ttk.Button(miab_gui_service,
                        text="decode a message")

# encode screen widgets
encode_label = ttk.Label(miab_gui_service,
                         text="Encode a Message",
                         font=("Garamond", 18))
# DEFAULT IMAGE - WILL BE SELECTED BY IMAGE SERVICE LATER
img_path = "./MsgInABottle_DEFAULT_IMAGE.png"
img_label = tk.Label()
browse_btn = ttk.Button(miab_gui_service,
                        text='Browse')
user_input = Text(miab_gui_service,
                  height=18.5,
                  width=40,
                  wrap='word')
encode_msg_btn = ttk.Button(miab_gui_service,
                            text='Encode Message')
export_btn = ttk.Button(miab_gui_service,
                        text='Export')
email_btn = ttk.Button(miab_gui_service,
                       text='Email')

# decode screen widgets
decode_label = ttk.Label(miab_gui_service,
                         text="Decode a Message",
                         font=("Garamond", 18))
msg_output = Text(miab_gui_service,
                  height=18.5,
                  width=40,
                  wrap='word')
decode_msg_btn = ttk.Button(miab_gui_service,
                            text='Decode Message')
reply_btn = ttk.Button(miab_gui_service,
                       text='Reply')
default = 'Click ''Browse'' to select an image'
default_msg = ttk.Label(miab_gui_service,
                        text=default,
                        font=("Garamond", 12))

# help screen widgets
encode_help = ttk.Label(miab_gui_service,
                        text='These are the instructions for encoding a message in an image',
                        font=("Garamond", 16),
                        wraplength=400)
decode_help = ttk.Label(miab_gui_service,
                        text='These are the instructions for decoding a message from an image',
                        font=("Garamond", 16),
                        wraplength=400)
more_info = ttk.Label(miab_gui_service,
                      text='Click this link for more information on steganography:',
                      font=("Garamond", 14))
more_info_link = ttk.Label(miab_gui_service,
                           text=help_link,
                           font=("Garamond", 16),
                           foreground='blue')


def close_welcome():
    welcome_label_1.grid_forget()
    welcome_label_2.grid_forget()
    encode_btn.grid_forget()
    decode_btn.grid_forget()

    back_btn.grid(column=0, row=0, ipadx=3, ipady=3, padx=7, pady=7, sticky=tk.NW)


def open_welcome():
    # welcome screen widgets

    miab_gui_service.rowconfigure(1, weight=1)

    welcome_label_1.grid(column=0, row=1, columnspan=2)
    welcome_label_2.grid(column=0, row=2, columnspan=2, sticky=tk.N)
    encode_btn.grid(column=0, row=3, ipadx=7, ipady=7, sticky=tk.N)
    decode_btn.grid(column=1, row=3, ipadx=7, ipady=7, sticky=tk.N)

    back_btn.grid_forget()


def close_encode():
    global encode_on
    if encode_on:
        # if the encode page is visible
        encode_label.grid_forget()
        # img_label.configure(image=img)
        img_label.grid_forget()
        user_input.grid_forget()
        browse_btn.grid_forget()
        encode_msg_btn.grid_forget()
        export_btn.grid_forget()
        email_btn.grid_forget()

        encode_on = False


def close_decode():
    global decode_on
    if decode_on:
        # if the decode page is visible

        decode_label.grid_forget()
        img_label.grid_forget()
        user_input.grid_forget()
        browse_btn.grid_forget()
        decode_msg_btn.grid_forget()
        reply_btn.grid_forget()
        default_msg.grid_forget()

        decode_on = False


def close_help():
    global help_on
    if help_on:
        miab_gui_service.rowconfigure(1, weight=1)

        # add the help screen widgets
        encode_help.grid_forget()
        decode_help.grid_forget()
        more_info.grid_forget()
        more_info_link.grid_forget()

        help_on = False


def encode_press():

    # close other screen widgets
    close_welcome()
    close_decode()
    close_help()

    global encode_on
    encode_on = True

    clearToTextInput()

    encode_label.grid(column=0, row=0, columnspan=2)

    # load the image
    load_img(img_path)

    # all other widgets
    user_input.grid(column=1, row=1, sticky=tk.N)
    user_input.insert('1.0', "This is a default message. Delete me and write your own!")
    browse_btn.grid(column=0, row=1, ipady=5, sticky=tk.S)
    encode_msg_btn.grid(column=1, row=1, ipady=5, sticky=tk.S)
    export_btn.grid(column=0, row=3, ipady=5)
    email_btn.grid(column=1, row=3, ipady=5)

    browse_btn.configure(command=lambda: browse_press())
    encode_msg_btn.configure(command=lambda: non_func_press("this button will encode the message into the image"))
    export_btn.configure(command=lambda: export_press(img_path))
    email_btn.configure(command=lambda: non_func_press("this button will email the message into a recipient"))


def get_crop_size(w, h):
    if w == h:
        # if the image is already square, return the current height and width
        return [0, 0, w, h]

    elif w > h:

        # if the width is longer than the height, crop the width
        diff = (w - h) // 2

        upper = diff
        lower = w - diff

        return [0, upper, h, lower]

    else:
        # h > w
        # if the height is taller than the width, crop the height
        diff = (h - w) // 2

        left = diff
        right = h - diff

        return [0, left, w, right]


def load_img(path):

    if path != "":
        # crop the image to be a square
        resize = (340, 340)
        img_to_crop = Image.open(path)

        w, h = img_to_crop.size

        size_tuple = get_crop_size(w, h)

        cropped = img_to_crop.crop(size_tuple)

        img = ImageTk.PhotoImage(cropped.resize(resize))
        img_label.Image = img
        img_label.configure(image=img)

        img_label.grid(column=0, row=1, sticky=tk.N)

    else:
        default_msg.grid(column=0, row=1)


def non_func_press(msg):
    popup = tk.Tk()
    popup.geometry('300x100')
    popup.eval('tk::PlaceWindow . center')
    popup.title("placeholder popup")
    ttk.Label(popup, text=msg).pack()


def encode_msg_press():
    pass


def email_press():
    pass


def decode_press():

    global decode_on
    decode_on = True

    # remove the welcome screen widgets
    close_welcome()
    close_encode()
    close_help()
    clearToTextInput()

    decode_label.grid(column=0, row=0, columnspan=2)

    load_img("")

    # all other widgets
    user_input.grid(column=1, row=1, sticky=tk.N)
    user_input.insert('1.0', 'The decoded message will appear here')
    user_input.config(state=tk.DISABLED)

    browse_btn.grid(column=0, row=1, ipady=5, sticky=tk.S)
    decode_msg_btn.grid(column=1, row=1, ipady=5, sticky=tk.S)
    reply_btn.grid(column=0, row=3, columnspan=2, ipady=5)

    browse_btn.configure(command=lambda: browse_press())
    decode_msg_btn.configure(command=lambda: non_func_press("this button will decode the message from the image"))
    reply_btn.configure(command=lambda: encode_press())


def help_press():
    global help_on
    help_on = True

    # remove the welcome screen widgets
    close_welcome()
    close_encode()
    close_decode()

    miab_gui_service.rowconfigure(1, weight=7)

    # add the help screen widgets
    encode_help.grid(column=0, row=1, sticky=tk.N)
    decode_help.grid(column=1, row=1, sticky=tk.N)
    more_info.grid(column=0, row=2, columnspan=2, sticky=tk.S)
    more_info_link.grid(column=0, row=3, columnspan=2, ipadx=2, sticky=tk.N)
    more_info_link.bind("<Button-1>", lambda e: hyperlink(help_link))


def back_press():

    close_encode()
    close_decode()
    close_help()

    open_welcome()


def browse_press():
    # browse for a png file
    # COMMENT: adapted from the source link for opening a browse window for files
    # DATE: February 14 2022
    # SOURCE: https://docs.python.org/3/library/dialog.html,
    #         https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/

    initial_dir = "C:/Users/" + str(getpass.getuser()) + "/Desktop"

    filename = filedialog.askopenfilename(title='Select an Image',
                                          initialdir=initial_dir,
                                          filetypes=[(".png, .jpg", ".png .jpg")])

    if filename != "":
        # if a file is selected, open the image and format it, otherwise do nothing
        load_img(filename)


def reply_press():
    # calls email service
    # email service opens it's own GUI?
    pass


def export_press(img):
    # browse for a png file
    # COMMENT: adapted from the source link for saving a file
    # DATE: February 14 2022
    # SOURCE: https://www.geeksforgeeks.org/python-asksaveasfile-function-in-tkinter/

    initial_dir = "C:/Users/" + str(getpass.getuser()) + "/Desktop"

    file_loc = filedialog.asksaveasfilename(title='Save your image',
                                            initialdir=initial_dir,
                                            filetypes=[(".png", ".png"),
                                                       (".jpg", ".jpg")],
                                            defaultextension=[("image", ".png"),
                                                              ("image", ".jpg")])
    if file_loc != "":

        img.save(file_loc)

        popup = tk.Tk()
        popup.geometry("200x50")
        popup.eval('tk::PlaceWindow . center')
        popup.title("")
        ttk.Label(popup, text="Image successfully saved!").pack()
        popup.mainloop()

    else:

        popup = tk.Tk()
        popup.geometry("200x50")
        popup.eval('tk::PlaceWindow . center')
        popup.title("")
        ttk.Label(popup, text="Image not saved").pack()
        popup.mainloop()


def hyperlink(url):
    # CITATION: adapted from source link for opening a link in python
    # DATE: February 13 2022
    # SOURCE: https://www.tutorialspoint.com/how-to-create-a-hyperlink-with-a-label-in-tkinter
    webbrowser.open_new(url)

    # change the color of the link to indicate it was clicked
    more_info_link.configure(foreground="purple")


def clearToTextInput():
    user_input.delete("1.0", "end")


def MIAB_GUI():
    # custom for MIAB - icon and title
    miab_gui_service.title("Message in a Bottle")
    miab_gui_service.iconbitmap("./MIAB_icon.ico")
    miab_gui_service.resizable(False, False)

    window_height = 700
    window_width = 900

    # code that centers the window on the computer screen
    # CITATION: adapted from source link for centering a tkinter window on any computer screen
    # DATE: February 13 2022
    # SOURCE: https://www.pythontutorial.net/tkinter/tkinter-window/

    # get screen height and width
    screen_height = miab_gui_service.winfo_screenheight()
    screen_width = miab_gui_service.winfo_screenwidth()

    # calculate x and y offsets using screen h/w and gui h/w
    center_wind_x = int(screen_width / 2 - window_width / 2)
    center_wind_y = int(screen_height / 2 - window_height / 2)

    miab_gui_service.geometry(f'{window_width}x{window_height}+{center_wind_x}+{center_wind_y}')

    # configure the grid
    miab_gui_service.columnconfigure(0, weight=1)
    miab_gui_service.columnconfigure(1, weight=1)
    miab_gui_service.rowconfigure(0, weight=1)
    miab_gui_service.rowconfigure(1, weight=1)
    miab_gui_service.rowconfigure(2, weight=1)
    miab_gui_service.rowconfigure(3, weight=1)

    open_welcome()

    help_btn.grid(column=1, row=0, ipadx=3, ipady=3, padx=7, pady=7, sticky=tk.NE)

    # commands for each button
    encode_btn.configure(command=lambda: encode_press())
    decode_btn.configure(command=lambda: decode_press())
    help_btn.configure(command=lambda: help_press())
    back_btn.configure(command=lambda: back_press())

    # displays the window
    miab_gui_service.mainloop()


if __name__ == "__main__":
    MIAB_GUI()
