import subprocess
import get_yelp_businesses
import time
import random
import sys

# takes a location as input and returns 2 numbers or each business
# number of latte art images, total number of images

location = sys.argv[1]

if location is None:
    location = "chicago"

bizids = get_yelp_businesses.get_business_ids_from_api(location)
imgdir ='latteart/images_to_label/'

scores = {}
for biz in bizids:
    
    cmd_to_call = "python get_yelp_images.py '" + biz + "' '" + imgdir + "'"
    #print cmd_to_call
    p = subprocess.Popen(cmd_to_call, shell=True, stdout = subprocess.PIPE)
    out,err = p.communicate()
   #subprocess.call(cmd_to_call)
    cmd_to_call = "python label_dir.py '" + imgdir + "'"
    #print cmd_to_call
    p = subprocess.Popen(cmd_to_call, shell=True, stdout = subprocess.PIPE)
    out,err = p.communicate()
    bizurl = 'http://www.yelp.com/biz/' + biz
    scores[bizurl]=out
    wait_time = random.randint(1, 5)
    time.sleep(wait_time)

for key, value in scores.iteritems():
    print key, value





