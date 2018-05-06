import numpy as np
import requests
from pathlib import Path
import time
import re
from urllib.parse import urljoin
import tarfile

MAPPING_API = 'http://www.image-net.org/api/text/imagenet.synset.geturls.getmapping?wnid='
BOUNDING_BOX_API = 'http://www.image-net.org/api/download/imagenet.bbox.synset?wnid='


def read_labels(file_name):
    """ Loads the labels of the imagenet synsets which should be downloaded

    The labels are returned as a matrix with the size [n, 2]

        n is the number of labels
        2 is for the 2 attributes id (e.g. n07745940) and label name (e.g. strawberry)

    E.g. [['n07745940', 'strawberry'], ['n03947888', 'pirate'], ['n02797295', 'barrow']]
    """

    print("Reading desired labels")

    label_file = open(file_name, 'r')
    lines = label_file.readlines()
    label_file.close()

    result = []

    for line in lines:
        wnid, _, label = line.split(' ', 2)
        result.append([wnid, label.rstrip(' \n')])

    return result


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

    for element in labels:

        wnid, label = element
        meta_refresh_regex = re.compile(
            '<meta[^>]*?url=(.*?)["\']', re.IGNORECASE)

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


def download_image_files(labels):
    print("Downloading image files")


if __name__ == '__main__':

    labels = read_labels('labels.txt')

    downloaded_files = download_bounding_boxes(labels)
    extract_bounding_boxes(downloaded_files)

    download_image_files(labels)
