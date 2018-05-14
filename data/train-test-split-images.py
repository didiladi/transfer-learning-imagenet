
import os
from readlabels import *
import numpy as np
from sklearn.model_selection import train_test_split

NEW_TRAIN_FOLDER_NAME = IMAGE_FOLDER_NAME + "train/"
NEW_DEV_FOLDER_NAME = IMAGE_FOLDER_NAME + "dev/"
NEW_TEST_FOLDER_NAME = IMAGE_FOLDER_NAME + "test/"


def collect_image_names(wnid):
    """ Returns an array with all the image files in a wnid folder """

    folder_name = IMAGE_FOLDER_NAME + wnid
    return os.listdir(folder_name)


def move_files_to_folder(image_names, src_folder_name, dest_folder_name):
    """ Moves image files from one folder to another """

    for file in image_names:
        os.rename(src_folder_name + file, dest_folder_name + file)


if __name__ == '__main__':

    labels = read_labels('labels.txt')

    for element in labels:
        wnid, label = element

        all_image_names = collect_image_names(wnid)

        # Split the data into 80% train, 10% dev (validation), and  10% test:
        X_train, X_test = train_test_split(
            all_image_names, shuffle=False, test_size=0.2)
        X_dev, X_test = train_test_split(X_test, shuffle=False, test_size=0.5)

        print("Moving files of label " + label +
              " to new train/dev/test destinations")

        old_folder_name = IMAGE_FOLDER_NAME + wnid

        # Move the files:
        move_files_to_folder(X_train, old_folder_name, NEW_TRAIN_FOLDER_NAME)
        move_files_to_folder(X_dev, old_folder_name, NEW_DEV_FOLDER_NAME)
        move_files_to_folder(X_test, old_folder_name, NEW_TEST_FOLDER_NAME)
