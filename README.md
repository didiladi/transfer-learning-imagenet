
# Transfer Learning

This repo contains the code for the execise in the course KDDM2 at Graz, University of Technology.


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
pip3 install setuptools Cython numpy tensorflow opencv-python
python3 setup.py build_ext --inplace
```


