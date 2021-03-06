import numpy as np
import requests
from pathlib import Path
import time
import re
from urllib.parse import urljoin
import tarfile
import os
from readlabels import *

MAPPING_API = 'http://www.image-net.org/api/text/imagenet.synset.geturls.getmapping?wnid='
BOUNDING_BOX_API = 'http://www.image-net.org/api/download/imagenet.bbox.synset?wnid='


def download_bounding_boxes(labels):
    """ Downloads the boundig boxes from the imagenet website

    This function downloads the files to './<wnid>.tar.gz', <wnid> is the internal
    id of the given label (e.g. strawberry has wnid 'n07745940')

    Since imagenet uses meta refreshes, the code is capable of following the redirect
    once. A recursive strategy is currently not needed, hence not implemented.

    ATTENTION: Files which were already downloaded before are automatiaclly skipped.
    """

    print("Downloading bounding boxes")

    file_names = []
    meta_refresh_regex = re.compile(
        '<meta[^>]*?url=(.*?)["\']', re.IGNORECASE)

    for element in labels:

        wnid, label = element

        file_name = './' + wnid + '.tar.gz'
        my_file = Path(file_name)

        # to prevent downloading the same file multiple times:
        if not my_file.exists():

            url = BOUNDING_BOX_API + wnid
            response = requests.get(url)

            # imagenet uses a meta refresh:
            match = meta_refresh_regex.search(response.text)
            if match:
                url = urljoin(url, match.groups()[0].strip())
                response = requests.get(url)

            print("   Getting bounding box for '" + label +
                  "', http status code: " + str(response.status_code))

            with open(file_name, 'wb') as f:
                f.write(response.content)

            file_names.append(file_name)

            # We want to be good citizens:
            time.sleep(5)

    return file_names


def extract_bounding_boxes(downloaded_files):
    """ Extracts the bounding box files (*.tar.gz) """

    print("Extracting bounding boxes")

    for fname in downloaded_files:

        if (fname.endswith("tar.gz")):
            tar = tarfile.open(fname, "r:gz")
            tar.extractall()
            tar.close()
        elif (fname.endswith("tar")):
            tar = tarfile.open(fname, "r:")
            tar.extractall()
            tar.close()


def download_image_mapping_files(labels):
    """ Downloads the class mappings from the imagenet website

    The mappings are one file per class which contains the name of the image (used in
    the bounding boxes) and the URL where to find the image.

    The files are stored in './mappings/<wnid>.txt'

    ATTENTION: Files which were already downloaded before are automatiaclly skipped.
    """

    print("Downloading image mapping files")

    # Create dirs if they don't exist
    os.makedirs(os.path.dirname('./mappings/'), exist_ok=True)

    for element in labels:

        wnid, label = element
        file_name = './mappings/' + wnid + '.txt'

        my_file = Path(file_name)

        # to prevent downloading the same file multiple times:
        if not my_file.exists():

            response = requests.get(MAPPING_API + wnid)

            print("   Getting mappings for '" + label +
                  "', http status code: " + str(response.status_code))

            with open(file_name, 'wb') as f:
                f.write(response.content)

            # We want to be good citizens:
            time.sleep(5)


def download_image_files(labels):
    """ Downloads the actual image files from the mapping-defined URLs

    The files are stored in './images/<wnid>/<image-id>.<image-file-ending>'

    ATTENTION: Files which were already downloaded before are automatiaclly skipped.
    """

    print("Downloading image files")

    for element in labels:

        wnid, label = element

        # Create dirs if they don't exist
        os.makedirs(os.path.dirname(
            IMAGE_FOLDER_NAME + wnid + '/'), exist_ok=True)

        mapping_file_name = './mappings/' + wnid + '.txt'
        label_file = open(mapping_file_name, 'r')
        lines = label_file.readlines()
        label_file.close()

        print("   Getting " + str(len(lines)) +
              " images for class '" + label + "'")

        for line in lines:

            if " " not in line:
                continue

            name, url = line.split(' ')
            file_ending = (url.split(".")[-1]).rstrip('\n')
            file_name = IMAGE_FOLDER_NAME + wnid + '/' + name + "." + file_ending

            my_file = Path(file_name)

            # to prevent downloading the same file multiple times:
            if not my_file.exists():

                print("      " + line.rstrip('\n'))

                # We don't allow redirects because flickr could have removed the image in the meanwhile
                # And we don't want to incluse the generic 'image not found image' into the training data

                try:
                    response = requests.get(
                        url, allow_redirects=False, verify=False, timeout=10)

                    if response.status_code == 200:
                        with open(file_name, 'wb') as f:
                            f.write(response.content)
                    else:
                        print("   File: '" + file_name +
                              "' could not be downloaded, http status code: " + str(response.status_code))
                except:
                    print("   File: '" + file_name +
                          "' could not be downloaded")

                # We want to be good citizens:
                time.sleep(1)


if __name__ == '__main__':

    labels = read_labels('labels.txt')

    downloaded_files = download_bounding_boxes(labels)
    extract_bounding_boxes(downloaded_files)

    download_image_mapping_files(labels)
    download_image_files(labels)
