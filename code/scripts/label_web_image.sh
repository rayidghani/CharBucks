curl $1 > latteart_model/images_to_label/image.jpg
python scripts/label_image.py latteart_model/images_to_label/image.jpg
