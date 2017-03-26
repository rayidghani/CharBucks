import subprocess
container_id = 'latte'

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def get_score(image_url):
    classify_cmd = "'/latteart/label_web_image.sh " + str(image_url) + "'"
    cmd = "docker exec " + container_id + " sh -c " + classify_cmd 
    p = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
    out,err = p.communicate()
    return out

def get_biz_score(bizid):
    if is_ascii(bizid):
        classify_cmd = "'/latteart/get_rating.sh " + str(bizid) + "'"
        cmd = "docker exec " + container_id + " sh -c " + classify_cmd
        p = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
        out,err = p.communicate()
        return out
    else:
        return "bizid has non ascii characters"

def get_biz_scores_from_location(location, limit):
    classify_cmd = "'python /latteart/get_business_ranking.py " + str(location) + " " + str(limit) + "'"
    cmd = "docker exec " + container_id + " sh -c " + classify_cmd
    print cmd
    p = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
    out,err = p.communicate()
    return out