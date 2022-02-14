# run.py

from app import batch_process_locations



model_dir = 'latteart_model_files/'
data_dir = 'data/'
imgdir ='images/'
threshold = 0.6
bizlogfile=data_dir+'bizscores.log'
imglogfile=data_dir+'imgscores.log'
locationfile=data_dir+'locations.txt'

if __name__ == '__main__':
    batch_process_locations.batch_process_locations(locationfile,0,0)

