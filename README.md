
# YOLO v2 - Transfer Learning

This repo contains the code for the execise in the course KDDM2 at Graz, University of Technology.

The task was to use transfer learning to train the tiny yolo nn-architecture (this is a convolutional neural network (CNN)) with a set of own labels. Transfer learning is a technique of using an already pre-trained neural network for a different set of labels. This approach works surprisingly well because the first layers of the neural network detect low-level features, like edges, lines, or shapes, which can be used to detect different objects as well.

## YOLO

The term YOLO stands for "You Only Look Once" and it depicts an algorithm where a fixed set of bounding boxes is used to detect objects. Prior approaches in the field of computer vision required a sliding window which was used on the picture on every possible position. This algorithm had the downside, that it required a lot more computational effort to detect (and localize) objects within an image.

**TODO more about YOLO**

## Purpose of this project


# Aproach

## Data Engineering

Aquiring the necessary training data was definitely the hardest part of this project. It required several iterations, until the acquired data could be used for training the neural network. Read more about the data downloading, cleaning and preparation in [data](https://github.com/didiladi/transfer-learning-imagenet/tree/master/data).

## Training

For training the neural network, the open source project [darkflow]() was used. It ports the original YOLO implementation [darknet]() to Tensorflow and was included wihin this repo as a git submodule. The included fork of darkmodule is located [here]().

Darkflow was modified to give some more error information in case it encounters an invalid image file. Additionally, there was some code added to handle the fact that the original imagenet annotation data does not contain file extensions. Now it correctly handles this special case.

Training was performed on the cloud on a machine with just CPUs. GPUs would have been nice, but time was not a limiting factor for me. So it didn't really matter that it took quite a long time to produce the needed machine learnign models.

## Evaluation

As explained within the data engineering section, the script [train-test-split-images.py]() was used to divide data into 80% training data, 10% dev (validation) data, and  10% test data. The dev data was used to evaluate the hyperparameters and to decide on how to split the labels for training (how many models). After this phase was finished, the dev (validation) set was added to the training data in order to maximize the amount of used training data.

Training with darkflow automatically produces checkpoint files from time to time. The script [eval.py] was used for evaluating these checkpoints in an automated fashion. For each ckeckpoint it took all the test data and performed a prediction with the given model for each image. It then produced a score between 0 and 1 to depict the overall accuracy. 0 means that the object never appeared within the test data of the given label, 1 means that the abject was always correcty located within the test data.

During training it became quite obvious, that there are several objects which are harder to detect than others. E.g. a strawberry can be detected quite easily, whereas a barrow can be considered as hard to detect. The following image depicts the accuracy of the first five labels (strawberry, barrow, shopping cat, tractor, and fig):

## Results


# Installation & Build

```
wget https://github.com/git-lfs/git-lfs/releases/download/v2.4.2/git-lfs-linux-amd64-2.4.2.tar.gz
tar -xvzf git-lfs-linux-amd64-2.4.2.tar.gz

git clone https://github.com/didiladi/transfer-learning-imagenet.git

cd transfer-learning-imagenet/

bash ../git-lfs-2.4.2/install.sh 

git lfs pull
git submodule init
git submodule update

sudo apt-get install -y build-essential python3-dev libsm6 libxext6 libxrender-dev

cd darkflow
pip3 install setuptools Cython numpy tensorflow opencv-python pandas psutil
python3 setup.py build_ext --inplace
```


# Train the network yourself

### Download the data

I uploaded the training / dev (validation) / test data for the 3 models into three different zip files which can be obtained at Google Drive:

[train-1.zip](https://drive.google.com/open?id=1dLrnUDBHiVCd6BF71Tb9mn7xSk1NIGFY)

[train-2.zip](https://drive.google.com/open?id=1dAJj8aKTOIpLCkLQxwj8UesvfLC0nBUl)

[train-3.zip](https://drive.google.com/open?id=1_qc7wO64GZ957plpWoS5f8IWCwXK4Yfd)

**Important:** I don't own the rights to any of these images. If you use them in any way, it is your own responibility to take care of checking/aquiring the rights to use them.

### Run darkflow the first time

```
./flow --model cfg/<model-filename>.cfg --train --dataset <train-data-folder> --annotation <train-data-annotation-folder> --load ../weights/tiny-yolo-voc.weights --labels <path-to-labels-file>
```

### Run darkflow and load the last checkpoint

```
./flow --model cfg/<model-filename>.cfg --train --dataset <train-data-folder> --annotation <train-data-annotation-folder> --load -1 --labels <path-to-labels-file>
```

# Train on a remote server

If you want to run the training in the cloud (I would highly recommend this option), you can add a cronjob for the evaluation script:

```
crontab -e

# Add the following line to the file to run the evaluation script every 15 minutes:
*/15 * * * * cd <path>/transfer-learning-imagenet/darkflow && python3.6 eval.py
```

As soon as you are satisfied with the results, run the following command to turn the checkpoint fie into a deployable .pb file:

```
flow --model cfg/<model-filename>.cfg --load -1 --savepb
```

Now the model (```.meta```, and ```.pb``` file) ends up in folder ```darkflow/built-graph/```. You can download it from your remote server by using ```scp```:

```
scp <user>@<server>:<path>/transfer-learning-imagenet/darkflow/built_graph/<model-filename>.pb <destination-folder>
scp <user>@<server>:<path>/transfer-learning-imagenet/darkflow/built_graph/<model-filename>.meta <destination-folder>
```

