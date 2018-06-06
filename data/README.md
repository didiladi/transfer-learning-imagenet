
# Acquiring of training data

Since we want to continue training of our yolo weights with a different set of 45 labels, we need to aquire training data for these new classes. The new classes from the set of 1000 imagenet classes are:

```
n07745940 229 strawberry
n02797295 258 barrow
n04204347 259 shopping_cart
n04465501 289 tractor
n07753113 321 fig
n07753275 322 pineapple
n13133613 329 ear
n03372029 356 flute 
n03481172 375 hammer
n02951585 377 can_opener
n04208210 380 shovel
n01514859 384 hen
n01608432 397 kite 
n01855672 420 goose
n02007558 425 flamingo
n04152593 510 screen 
n03793489 511 mouse 
n03544143 525 hourglass 
n04356056 535 sunglasses 
n03692522 536 loupe 
n04004767 556 printer 
n02948072 591 candle 
n04456115 594 torch 
n03207941 667 dishwasher 
n03063689 674 coffeepot 
n04398044 675 teapot 
n03661043 687 library
n04081281 694 restaurant 
n02776631 704 bakery 
n04326547 724 stone_wall 
n07716358 739 zucchini 
n03594734 748 jean 
n03814906 755 necklace
n02823428 777 beer_bottle
n02909870 820 bucket
n02843684 839 birdhouse 
n04033901 862 quill
n03676483 867 lipstick 
n03291819 879 envelope 
n04584207 899 wig 
n04548362 928 wallet 
n06596364 930 comic_book 
n07873807 948 pizza 
n04409515 970 tennis_ball 
n04254777 986 sock 
```

## Downloading the images and bounding boxes

Since I'm too lazy to label all the trainign data myself, I used the pre-labelled imgages which are osed on imagenet. However, since this project is somewhat semi-commercial, we cannot download the images directy from the imagenet website, since it states, that images downloaded from there must only be used for educational purposes. However, luckily they provide a list of URLs where the images originally came from. That's why I wrote a little python script which downloads them from its original source. Together with the bounding box annotations from imagenet, we have our trainign data:

```
cd data
python download-images.py
```

## Cleaning the data

Since a lot of servers don't provice a correct http status code response, we downloaded a lot of data which is in fact no image. In most cases the image will be filled with an HTML 404 webpage. This is the reason why we need to perform some data cleaning, to filter out (delete) the invalid images.

For the record: A correct http status code would be 404 (unavailable) or at least a redirect (302) if the image is not available.

The python script ```delete-invalid-images.py``` tries to open each image file within the ```images``` folder. If opening the image fails, we know that it has an invalid format. Now all the invalid image paths are collected in an array and the program asks for user input whether the images can be deleted.

**Attention:** check the output of the script before pressing ```y```. It is strongly recommended to pipe the outpout (std out) of the program additionally into a file and inspect some of the invalid files manually:

```
python delete-invalid-images.py | tee out.txt
```

## The downloaded data

Downloading of the image files took several days on my laptop. Why didi it take so long? It was done gracefully, we only made one image-request per second. Sadly, approximately 50% of the original images are not avaialable any more. However, we still acquired a lot of training data. The size of all images combined is more than 6GB. The following listing displays the amount of images we downloaded per class:


```
./images/n01514859: 878
./images/n01608432: 701
./images/n01855672: 1209
./images/n02007558: 1246
./images/n02776631: 1115
./images/n02797295: 1302
./images/n02823428: 1391
./images/n02843684: 1517
./images/n02909870: 1101
./images/n02948072: 993
./images/n02951585: 477
./images/n03063689: 964
./images/n03207941: 1333
./images/n03291819: 806
./images/n03372029: 1098
./images/n03481172: 998
./images/n03544143: 590
./images/n03594734: 1379
./images/n03661043: 984
./images/n03676483: 927
./images/n03692522: 379
./images/n03793489: 925
./images/n03814906: 1092
./images/n04004767: 1040
./images/n04033901: 621
./images/n04081281: 989
./images/n04152593: 479
./images/n04204347: 1434
./images/n04208210: 951
./images/n04254777: 1773
./images/n04326547: 1384
./images/n04356056: 737
./images/n04398044: 1575
./images/n04409515: 899
./images/n04456115: 427
./images/n04465501: 1573
./images/n04548362: 1070
./images/n04584207: 915
./images/n06596364: 561
./images/n07716358: 987
./images/n07745940: 1445
./images/n07753113: 1246
./images/n07753275: 1564
./images/n07873807: 1470
./images/n13133613: 898
```

## Preparing the data for training:

Darkflow expects the annotations and images to be in just one folder. That's why we need to get rid of the intermediate class folders (e.g. "n13133613/"). We also need to split the data into a train/test set in order to be able to evaluate how well our new models perform. Since our network architecture is based on tiny yolo, we can't use all the class labels within one model (the original tiny yolo has just 20 VOC classes). That's why we will train 3 different neural nets, each using 15 classes.

