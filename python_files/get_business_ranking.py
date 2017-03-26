import subprocess
import time
import random
import sys
import logging
import get_yelp_businesses

# takes a location as input and returns 2 numbers or each business
# number of latte art images, total number of images

THRESHOLD = 0.6
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

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

    logger.info('Starting to get %s businesses for %s', num_of_businesses_to_get, location)
    all_bizids = get_yelp_businesses.get_business_ids_from_api(location, num_of_businesses_to_get)
    # remove buzinesses with non ascii characters
    bizids =  [b for b in all_bizids if is_ascii(b)]
    logger.info('Got %s businesses for %s', len(bizids), location)
    
    if len(bizids) > 0:
        imgdir ='latteart/images_to_label/'
        scores = {}
        for biz in bizids:
            logger.info('Processing %s', biz)  
            logger.info('Getting images for %s and putting them in %s', biz, imgdir) 
            cmd_to_call = "python get_yelp_images.py '" + biz + "' '" + imgdir + "'"
            logger.debug('calling %s', cmd_to_call)
            p = subprocess.Popen(cmd_to_call, shell=True, stdout = subprocess.PIPE)
            out,err = p.communicate()
            logger.info('Labeling images in directory %s with threshold %s', imgdir, THRESHOLD) 
            cmd_to_call = "python label_dir.py '" + imgdir + "' " + str(THRESHOLD)
            logger.debug('calling %s', cmd_to_call)
            p = subprocess.Popen(cmd_to_call, shell=True, stdout = subprocess.PIPE)
            out,err = p.communicate()
            bizurl = 'http://www.yelp.com/biz/' + biz
            scores[bizurl]=out
            logger.info('Scoring %s with score %s', biz, out)
            wait_time = random.randint(1, 5)
            logger.info('waiting %s seconds to process next business...',wait_time)
            time.sleep(wait_time)

        for key, value in scores.iteritems():
            print key, value
    else:
        logger.error('No businesses returned by get_business_ids_from_api', exc_info=True)

if __name__ == "__main__":
    main(sys.argv[1:])


