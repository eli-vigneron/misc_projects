import tika

tika.initVM()
from tika import parser
import re
from operator import itemgetter
import tika
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


def find_ext(dr, ext):
    """
    :param dr: directory path
    :param ext: desired file extensions to be found (no .)
    :return: list containing the paths to the files
    """
    file_list = glob.glob(path.join(dr, "*.{}".format(ext)))
    return [i.replace("\\", '/') for i in file_list]


def acaa_roll_extract(pth):
    parsed = parser.from_file(pth)

    try:
        book = parsed["content"].split("\n")
    except AttributeError:
        # print(pth)
        return 0
    book = list(filter(None, book))
    index_to_slice = 0
    for k, entry in enumerate(book):

        if "Tax Roll" in entry:
            index_to_slice = k
            # print(index_to_slice)
            break

    book = book[int(index_to_slice): int(index_to_slice)+4]

    for i, line in enumerate(book):
        match = re.findall(r'([\d,]+)', line)
        for k in match:
            if len(k) >= 7 and len(k) < 12:
                if k[0] != '0':
                    roll= k
                    old_pth = pth.split("/")[-1]
                    old_pth = "...2019/Signed ACAA/" + old_pth

                    new_pth = "...2019/Signed ACAA/" + roll + " signed ACAA.pdf"
                    #print(old_pth, new_pth)
                    # print(roll)

                    try:
                        os.rename(old_pth, new_pth)

                    except:
                        print(pth)
                        continue

                    # os.rename(old_pth, new_pth_los)


def main():
    list_of_acaas = find_ext(".../pdf rename 2/test/acaas local", 'pdf')

    for acaa in list_of_acaas:
        acaa_roll_extract(acaa)


if __name__ == "__main__":
    main()
