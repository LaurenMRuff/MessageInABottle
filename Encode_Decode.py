# AUTHOR: Lauren Ruff
# Email: ruffl@oregonstate.edu
# Assignment: 6, minimum viable product (MVP)
# Due Date: February 14 2022
# Version: 1.0
# File: Encode_Decode.py
# Description: This file will contain the algorithm for encoding or decoding a message from a photo


def encode(img, msg):
    # open the image for appending, write the message to the image, close the image, and return the image
    e_img = open(img, mode='a')
    e_img.write(msg)
    e_img.close()

    return e_img


def decode(img):
    # open the image for reading, read the message from the image, close the image, and return the message
    d_img = open(img, mode='r')
    d_msg = d_img.read()

    d_img.close()

    return d_msg

