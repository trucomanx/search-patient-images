
# Text to string
from pathlib import Path
def text_to_string(filename):
    string=Path(filename).read_text()
    string = string.replace('\n', '')
    return string;


# Open file in write mode
def save_list_string_in(lista,filename):
    with open(filename, 'w') as fp:
        for item in lista:
            # write each item on a new line
            fp.write("%s\n" % item)

# Load file 
def load_list_string_from(filename):
    # empty list to read list from a file
    names = []

    # open file and read the content in a list
    with open(filename, 'r') as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            names.append(x)

    # display list
    return names

import os
# Create target Directory if don't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
        print("Directory " , directory ,  " Created ")
