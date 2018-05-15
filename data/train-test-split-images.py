
import os
from readlabels import *
import numpy as np
from sklearn.model_selection import train_test_split

OLD_ANNOTATION_FOLDER_NAME = './Annotation/'

NEW_TRAIN_FOLDER_NAME = IMAGE_FOLDER_NAME + "train/"
NEW_DEV_FOLDER_NAME = IMAGE_FOLDER_NAME + "dev/"
NEW_TEST_FOLDER_NAME = IMAGE_FOLDER_NAME + "test/"

NEW_TRAIN_ANNOTATIONS_FOLDER_NAME = IMAGE_FOLDER_NAME + "train-annotations/"
NEW_DEV_ANNOTATIONS_FOLDER_NAME = IMAGE_FOLDER_NAME + "dev-annotations/"
NEW_TEST_ANNOTATIONS_FOLDER_NAME = IMAGE_FOLDER_NAME + "test-annotations/"


def collect_image_names(wnid):
    """ Returns an array with all the image files in a wnid folder """

    folder_name = IMAGE_FOLDER_NAME + wnid
    return os.listdir(folder_name)


def move_files_to_folder(image_names, src_folder_name, dest_folder_name):
    """ Moves image files from one folder to another """

    # Create dirs if they don't exist
    os.makedirs(os.path.dirname(dest_folder_name), exist_ok=True)

    for file in image_names:
        print(src_folder_name + file)
        print(dest_folder_name + file)
        #os.rename(src_folder_name + file, dest_folder_name + file)


def move_annotation_files_to_folder(image_names, src_folder_name, dest_folder_name):
    """ Moves annotation files from one folder to another """

    # Create dirs if they don't exist
    os.makedirs(os.path.dirname(dest_folder_name), exist_ok=True)

    for file in image_names:

        image_file_without_extension = file[:file.index(".")]
        annotation_file_name = image_file_without_extension + ".xml"

        print(src_folder_name + annotation_file_name)
        print(dest_folder_name + annotation_file_name)
        # os.rename(src_folder_name + annotation_file_name,
        #          dest_folder_name + annotation_file_name)


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

        old_image_folder_name = IMAGE_FOLDER_NAME + wnid + "/"

        # Move the image files:
        move_files_to_folder(
            X_train, old_image_folder_name, NEW_TRAIN_FOLDER_NAME)
        move_files_to_folder(X_dev, old_image_folder_name, NEW_DEV_FOLDER_NAME)
        move_files_to_folder(X_test, old_image_folder_name,
                             NEW_TEST_FOLDER_NAME)

        old_annotation_folder_name = OLD_ANNOTATION_FOLDER_NAME + wnid + "/"

        # Move the annotations:
        move_annotation_files_to_folder(
            X_train, old_annotation_folder_name, NEW_TRAIN_ANNOTATIONS_FOLDER_NAME)
        move_annotation_files_to_folder(
            X_dev, old_annotation_folder_name, NEW_DEV_ANNOTATIONS_FOLDER_NAME)
        move_annotation_files_to_folder(
            X_test, old_annotation_folder_name, NEW_TEST_ANNOTATIONS_FOLDER_NAME)
