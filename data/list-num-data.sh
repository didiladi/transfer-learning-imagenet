#!/bin/sh

for dir in ./images/*/
do
    dir=${dir%*/}
    echo ${dir}: `ls -l ${dir}/* | wc -l`
done