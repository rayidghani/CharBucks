#!/bin/bash
if [ $# -lt 1 ]; then
    echo $0: usage: myscript business_name verbose 
    exit 1
fi

if [ $# -lt 2 ]; then
    verbose=0 
fi

bizname=$1
verbose=$2
imgdir='latteart_model/images_to_label/'
threshold='0.6'
model_dir='latteart_model'

python scripts/get_yelp_images.py $bizname $imgdir
python scripts/label_dir.py $imgdir $model_dir $threshold $verbose

