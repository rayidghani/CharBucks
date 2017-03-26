import subprocess
import time
import random
import sys
import get_yelp_businesses

# takes a location as input and returns 2 numbers or each business
# number of latte art images, total number of images

THRESHOLD = 0.6

def main(argv):
    """Function used to get scores for n shops in a location

    Args:
        argv[1]: location (can be city, zip, lat long string)
        argv[2]: number of business to get and score

    Returns:
        Returns a string with scores for each location and the url
    """
    
    location = sys.argv[1]
    num_of_businesses_to_get = sys.argv[2]

    if location is None:
        location = "chicago"

    bizids = get_yelp_businesses.get_business_ids_from_api(location, num_of_businesses_to_get)
    imgdir ='latteart/images_to_label/'

    scores = {}
    for biz in bizids:        
        cmd_to_call = "python get_yelp_images.py '" + biz + "' '" + imgdir + "'"
        p = subprocess.Popen(cmd_to_call, shell=True, stdout = subprocess.PIPE)
        out,err = p.communicate()
        cmd_to_call = "python label_dir.py '" + imgdir + "' " + str(THRESHOLD)
        p = subprocess.Popen(cmd_to_call, shell=True, stdout = subprocess.PIPE)
        out,err = p.communicate()
        bizurl = 'http://www.yelp.com/biz/' + biz
        scores[bizurl]=out
        wait_time = random.randint(1, 5)
        time.sleep(wait_time)

    for key, value in scores.iteritems():
        print key, value

if __name__ == "__main__":
   main(sys.argv[1:])


