
# YOLO v2 - Transfer Learning

This repo contains the code for the execise in the course KDDM2 at Graz, University of Technology.

The task was to use transfer learning to train the tiny yolo nn-architecture (this is a convolutional neural network (CNN)) with a set of own labels. Transfer learning is a technique of using an already pre-trained neural network for a different set of labels. This approach works surprisingly well because the first layers of the neural network detect low-level features, like edges, lines, or shapes, which can be used to detect different objects as well.

The term YOLO stands for "You Only Look Once" and it depicts an algorithm where a fixed set of bounding boxes is used to detect objects. Prior approaches in the field of computer vision required a sliding window which was used on the picture on every possible position. This algorithm had the downside, that it required a lot more computational effort to detect (and localize) objects within an image.



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
pip3 install setuptools Cython numpy tensorflow opencv-python pandas
python3 setup.py build_ext --inplace
```

# Data Engineering

Read more about the data downloading, cleaning and preparation in [folder data](https://github.com/didiladi/transfer-learning-imagenet/tree/master/data).

# Train the network yourself

### Download the data

I uploaded the training / dev (validation) / test data for the 3 models into three different zip files which can be obtained at Google Drive:

[train-1.zip](https://drive.google.com/open?id=1dLrnUDBHiVCd6BF71Tb9mn7xSk1NIGFY)
[train-2.zip](https://drive.google.com/open?id=1dAJj8aKTOIpLCkLQxwj8UesvfLC0nBUl)
[train-3.zip](https://drive.google.com/open?id=1_qc7wO64GZ957plpWoS5f8IWCwXK4Yfd)

**Important:** I don't own the rights to any of these images. If you use them in any way, it is your own responibility to take care of checking/aquiring the rights to use them.

### Run darkflow the first time


### Run darkflow and load the last checkpoint



# Evaluation and Results

