docker stop latte
docker rm latte
docker run -it -d -v ~/Projects/CharBucks/python_files/:/latteart/ -w /latteart --name="latte" rayid/tensorflow:image-class
./go.sh
