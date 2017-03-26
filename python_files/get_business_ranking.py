import subprocess
import get_yelp_businesses
import time
import random

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
    scores[biz]=out
    wait_time = random.randint(1, 5)
    time.sleep(wait_time)

for key, value in scores.iteritems():
    print key, value





