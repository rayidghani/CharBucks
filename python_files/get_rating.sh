#!/bin/bash
if [ $# -ne 1 ]; then
    echo $0: usage: myscript name
    exit 1
fi

bizname=$1
imgdir='latteart/images_to_label/'
threshold='0.6'

python get_yelp_images.py $bizname $imgdir
python label_dir.py $imgdir $threshold

