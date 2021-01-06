# -*- coding: utf-8 -*-
from tika import parser
import os
import glob
import shutil
from os import path
import string

"""
Program that renames Assessment Notice PDF's
Desired output form is: roll, address 'Notice 2019'
    Step 1: OCR the notices
    Step 2: Run program
"""


def find_ext(dr, ext):
    """
    :param dr: directory path
    :param ext: desired file extensions to be found (no .)
    :return: list containing the paths to the files
    """
    file_list = glob.glob(path.join(dr, "*.{}".format(ext)))
    return [i.replace("\\", '/') for i in file_list]


def pdf_to_notice_name(pth):
    """
    takes the full path to the pdf and returns a formatted string
    with the following information: roll, address 'Notice 2019'
    :param pth: path to the pdf
    :return: formatted title
    """

    headers = {'X-Tika-PDFextractInlineImages': 'true'}

    # syntax to read the pdf
    raw = parser.from_file(pth, headers=headers)
    pdf = raw['content']

    # Convert double newlines into single newlines
    pdf = pdf.replace('\n\n', '\n')

    # make a list of the pdf text
    pdf = pdf.split('\n')

    # extract the roll number and the address
    # also want the address
    roll_address = []
    for i, line in enumerate(pdf):

        if 'ACCOUNT' in line:
            # extract the roll number (replace punctuation, newlines etc.)
            roll = line.strip().split(' ')[-1]
            translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))    # map punctuation to ''
            roll = roll.translate(translator).replace(' ', '')
            roll = roll.lower().replace('noticeaccount', '')
            roll_address.append(roll)

        if 'y Address ' in line:
            try:

                if 'description' in pdf[i+1].lower():
                    # then there is likely no address provided (condos)
                    #print('No Address')
                    roll_address.append('No Address')
                else:
                    addr = pdf[i + 1]
                    translator = str.maketrans(string.punctuation,
                                               '.' * len(string.punctuation))  # map punctuation to ''
                    addr = addr.translate(translator).replace('.','')
                    #print(addr)
                    roll_address.append(addr)

            except IndexError:
                pass
    return roll_address


def main():

    list_of_pdf_paths = find_ext('.../pdf rename 2', 'pdf')

    # list that will be of the form [..., [path, title], ...]
    list_of_pdf_paths_and_titles = []

    # build the above list
    for pth in list_of_pdf_paths:
        print(pdf_to_notice_name(pth))

        # list_of_pdf_paths_and_titles.append([pth, ', '.join(pdf_to_notice_name(pth))])

    for i in list_of_pdf_paths_and_titles:
        print(i)


if __name__ == '__main__':
    main()

