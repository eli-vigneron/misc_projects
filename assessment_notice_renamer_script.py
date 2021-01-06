# -*- coding: utf-8 -*-
from tika import parser
import os
import glob
import shutil
from os import path
import string
from urllib.request import urlopen
import time
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

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
    :return: roll and address from the PDF
    """

    # ocr library
    headers1 = {'X-Tika-PDFextractInlineImages': 'true'}

    # syntax to read the pdf
    raw = parser.from_file(pth, headers=headers1)
    pdf = raw['content']

    if pdf is None:
        return []

    # Convert double newlines into single newlines
    pdf = pdf.replace('\n\n', '\n')

    # make a list of the pdf text
    pdf = pdf.split('\n')

    # extract the roll number and the address
    roll_address = []
    for i, line in enumerate(pdf):

        if 'ACCOUNT' in line:
            # extract the roll number (replace punctuation, newlines etc.)
            roll = line.strip().split(' ')[-1]
            translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))  # map punctuation to ''
            roll = roll.translate(translator).replace(' ', '')
            roll = roll.lower().replace('noticeaccount', '')
            roll_address.append(roll)

        if 'y Address ' in line:
            try:
                if 'description' in pdf[i + 1].lower():
                    # then there is likely no address provided (condos)
                    # print('No Address')
                    roll_address.append('No Address')
                else:
                    addr = pdf[i + 1]
                    translator = str.maketrans(string.punctuation,
                                               '.' * len(string.punctuation))  # map punctuation to ''
                    addr = addr.translate(translator).replace('.', '')
                    roll_address.append(addr)

            except IndexError:
                pass
    return roll_address


def search(roll):
    """
    :param roll: roll number
    :return: formatted address
    """

    url = "https://maps.edmonton.ca/api/rest/assessment.ashx?request=getasm&arg=" + str(roll).strip() + \
          "&callback=SM._c(%2715%27).success&errCallBack=SM._c(%2715%27).fail&NaCl=1811283294847965"
    f = urlopen(url)
    myfile = f.read()
    asssessment_tab = myfile.decode("utf-8")
    asssessment_tab_list = asssessment_tab.split(',')

    if len(asssessment_tab_list) > 1:
        for i in asssessment_tab_list:
            if "FULLADDRESS" in i:
                fulladdress = i.split(':')[1].replace('"', '')
                fulladdress = fulladdress.replace(' EDMONTON AB  CANADA', '')
                fulladdress = fulladdress.replace(' EDMONTON AB  ', '')
                return fulladdress


class MainClass:

    def __init__(self, master):
        self.parent = master
        self.gui()

        # initialize progress bar
        self.progress_frame = ttk.Frame()
        self.progress_frame.grid(row=5, column=2)
        self.progress = ttk.Progressbar(self.progress_frame, orient="horizontal", length=150, mode="determinate")

    def gui(self):
        # adds in a grip box
        gripframe = ttk.Frame()
        gripframe.grid(row=100, column=100)
        ttk.Sizegrip(gripframe).grid(row=100, column=100)

        # -------------------------------------------------------------------------------------------------------
        # Description Label
        desc_frame = ttk.Frame()
        desc_frame.grid(row=1, column=1, sticky=W)
        desc_label = Label(desc_frame, text="    Select Folder:   ", bg="gray99")
        desc_label.grid(row=1, column=1, sticky=W)

        # -------------------------------------------------------------------------------------------------------
        # open / close button frame
        buttonframe = ttk.Frame()
        buttonframe.grid(row=1, column=2, sticky=W)

        open_excel = ttk.Button(buttonframe, text="Open", command=self.path_formatted_text)
        open_excel.grid(row=1, column=2, sticky=W)

        # -------------------------------------------------------------------------------------------------------
        # close button
        close = ttk.Button(buttonframe, text="Close", command=myGUI.destroy)
        close.grid(row=1, column=3, sticky=W)

        # -------------------------------------------------------------------------------------------------------
        # suffix
        self.Source = StringVar()

        # Suffix label
        suffix_frame = ttk.Frame()
        suffix_frame.grid(row=0, column=1, sticky=W, columnspan=2)
        suffix_label = Label(suffix_frame, text="    Enter Suffix:      ", bg="gray99")
        suffix_label.grid(row=0, column=1, sticky=W)
        suffix_entry = ttk.Entry(suffix_frame, textvariable=self.Source)
        suffix_entry.grid(row=0, column=2, sticky=W, columnspan=3)

    def path_formatted_text(self):
        folder = filedialog.askdirectory()

        if folder == '':
            return 0

        # list containing all the pdf's in the folder (full paths)
        list_of_pdf_paths = find_ext(folder, 'pdf')

        # error log / list of files that could not be found
        error_list = []
        total = len(list_of_pdf_paths)
        count = 0
        # build the above list
        for pth in list_of_pdf_paths:

            # progress_bar that updates on each iteration (visible on the tkinter gui)
            # set the progress bar value
            self.progress["value"] = 0
            self.progress["maximum"] = total
            self.progress.grid(row=3, column=2)
            self.progress["value"] = str(count)
            myGUI.update()

            roll_addr = pdf_to_notice_name(pth)

            try:
                roll_addr.append(search(roll_addr[0]))
            except:
                roll_addr.append('Error')

            time.sleep(1)

            if len(roll_addr) == 3 and roll_addr[-1] != 'null' and roll_addr[-1] is not None:
                formatted_string = roll_addr[0] + ", " + roll_addr[2] + " "+str(self.Source.get().strip())

            elif len(roll_addr) == 2 and roll_addr[-1] != 'null' and roll_addr[-1] is not None:
                formatted_string = roll_addr[0] + ", " + roll_addr[1] + " "+str(self.Source.get().strip())

            else:
                error_list.append(pth)
                count += 1
                continue

            new_pth = pth.replace(pth.split('/')[-1], formatted_string+'.pdf')

            # print(pth, new_pth)
            os.rename(pth, new_pth)
            count += 1

        self.progress_frame.grid_forget()
        myGUI.update()

        # add a label that displays the error log

        # number of errors
        error_count = len(error_list)

        error_frame = ttk.Frame()
        error_frame.grid(row=3, column=1, columnspan=3)

        lbl3 = Label(error_frame, text="Error", bg="gray99")
        lbl3.grid(row=3, column=1)

        txt = Text(error_frame, width=30, height=10)
        txt.grid(row=3, column=2, columnspan=3)
        txt.insert('end', '    --- ' + str(total - error_count) + ' of ' + str(total)+' renamed ---\n')
        txt.insert('end', '\nThe following could not be \nrenamed: \n')


        for error in error_list:
            txt.insert('end','\n'+ error + '\n')

        txt.configure(state='disabled')


if __name__ == '__main__':

    # initialize the GUI
    myGUI = Tk()
    app = MainClass(myGUI)
    myGUI.title('Notice Renamer')
    myGUI['bg'] = "gray99"
    # myGUI.geometry("250x150")
    myGUI.mainloop()
