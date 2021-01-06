import tika
tika.initVM()
from tika import parser
import re
from operator import itemgetter

parsed = parser.from_file('.../hott-online-1198-geeccc59.pdf')

book = parsed["content"].split("\n")

def counter_of_data(thing):
    theorems = []
    theorem_numbers = []

    for line in book:
        if thing in line[:len(thing)+2]:
            theorems.append(line[:len(thing)+8])

    for i in theorems:
        number = i.replace(thing+' ', '')
        number1 = number.split(" ")[0].strip()
        if number1[-1] is ".":
            number1=number1[:len(number1)-1]
        theorem_numbers.append(thing+ " " + number1+".")
        theorem_numbers.append(thing + " " + number1)

    total_count = 0
    thm_freq = []
    for number in theorem_numbers:
        for line in book:
            total_count+=str(line).count(number)

        thm_freq.append((number, total_count))
        total_count = 0

    thm_freq.sort(key=itemgetter(1), reverse=True)
    for item in thm_freq:
        print(item)


counter_of_data("Example")
