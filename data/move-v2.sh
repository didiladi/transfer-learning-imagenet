#!/bin/bash

display_usage() { 
	echo -e "\nUsage:\nsh move-v2.sh path-to-label-file.txt old-index new-index" 
	echo -e "\neg:\nsh move-v2.sh ../darkflow/labels-v2-1.txt 1 1 \n" 
} 

# if less than two arguments supplied, display usage 
if [  $# -le 1 ] 
then 
	display_usage
	exit 1
fi 
 
# check whether user had supplied -h or --help . If yes display usage 
if [[ ( $# == "--help") ||  $# == "-h" ]] 
then 
	display_usage
	exit 0
fi 

# create all the needed folders:
mkdir -p images/train-v2-$3
mkdir -p images/train-annotations-v2-$3
mkdir -p images/test-v2-$3
mkdir -p images/test-annotations-v2-$3

file=$1

while IFS= read -r label; do

    printf 'Copying label %s\n' "$label"

    # copy the training images:
    cp -n images/train-$2/$label* images/train-v2-$3/
    cp -n images/train-annotations-$2/$label* images/train-annotations-v2-$3/

    # copy the dev images to training:
    cp -n images/dev-$2/$label* images/train-v2-$3/
    cp -n images/dev-annotations-$2/$label* images/train-annotations-v2-$3/

    # copy the test images to test
    cp -n images/test-$2/$label* images/test-v2-$3/
    cp -n images/test-annotations-$2/$label* images/test-annotations-v2-$3/

done < "$file"
