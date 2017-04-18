import subprocess
container_id = 'latte'
curpath = 'python_files/'
docker = 0

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def get_score(image_url):
    if (docker):
        classify_cmd = "'/latteart/label_web_image.sh " + str(image_url) + "'"
        cmd = "docker exec " + container_id + " sh -c " + classify_cmd
    else:
        cmd = curpath + "label_web_image.sh " + str(image_url)
    p = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
    out,err = p.communicate()
    return out

def get_biz_score(bizid, verbose):
    if is_ascii(bizid):
        if (docker):
            classify_cmd = "'/latteart/get_rating.sh " + str(bizid) + " " + str(verbose) + "'"
            cmd = "docker exec " + container_id + " sh -c " + classify_cmd
        else:
            cmd = curpath + "get_rating.sh " + str(bizid) + " " + str(verbose)
        p = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
        out,err = p.communicate()
        print out
        return out
    else:
        return "bizid has non ascii characters"

def get_biz_scores_from_location(location, limit, verbose):
    if (docker):
        classify_cmd = "'python /latteart/get_business_ranking.py " + str(location) + " " + str(limit) + " " + str(verbose) + "'"
        cmd = "docker exec " + container_id + " sh -c " + classify_cmd
        print cmd
    else:
        cmd = "python get_business_ranking.py " + str(location) + " " + str(limit) + " " + str(verbose)
    p = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
    out,err = p.communicate()
    return out
