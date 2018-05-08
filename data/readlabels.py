
IMAGE_FOLDER_NAME = './images/'


def read_labels(file_name='labels.txt'):
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
