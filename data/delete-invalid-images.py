
import os
from readlabels import *
from PIL import Image
import sys


def rename_images_if_necessary(labels):
    """ Renames images which have a query string (?) in their file names 

    Since our downloading functionality wasn't correctly handing the query string,
    we need to do some additional post-processing and file renaming.

    """

    for element in labels:

        wnid, _ = element
        folder_name = IMAGE_FOLDER_NAME + wnid

        files = os.listdir(folder_name)

        for file in files:

            if "?" not in file:
                continue

            os.rename(folder_name + "/" + file, folder_name + "/" + file)


def collect_invalid_images(labels):
    """ Collects all non-valid image files

    "labels" the processed classes and theit corresponding labels 

    This function tries to open the image with the Image module. If this fails, we know that the image is
    invalid and it should be deleted. This method is harmless, it just returns the files which
    were invalid.

    ATTENTION: 
    """

    invalid_image_files = []

    for element in labels:

        wnid, _ = element
        folder_name = IMAGE_FOLDER_NAME + wnid

        files = os.listdir(folder_name)

        for file in files:
            try:
                Image.open(folder_name + "/" + file)
            except IOError:
                invalid_image_files.append(folder_name + "/" + file)

    return invalid_image_files


def query_yes_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    This functionw as stolen from:
        https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def delete_invalid_files(invalid_files):
    """ Delets off passed files from the disk. No further confirmation will be asked

    "invalid_files" the files to delete

    ATTENTION: This is no joke! This function WILL delete the given files.
    """

    for element in invalid_image_files:
        os.remove(element)


if __name__ == '__main__':

    labels = read_labels('labels.txt')
    rename_images_if_necessary(labels)
    invalid_image_files = collect_invalid_images(labels)

    if len(invalid_image_files) > 0:

        print("I'm going to delete the following files:\n")

        for element in invalid_image_files:
            print(element)

        print("---------------------------------------------------")
        doDelete = query_yes_no('Do you really want to delete these files?')

        if doDelete:
            delete_invalid_files(invalid_image_files)
