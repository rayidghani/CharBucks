import boto3
import configparser
import csv
from yelp_helper import get_image_from_url
import base64
import binascii
import urllib
import botocore
import pandas as pd

def main():
#	ACCESS_KEY_ID = ''
#	ACCESS_SECRET_KEY = ''
#	config = configparser.RawConfigParser()
#	config.read('/Users/rayid/.aws/credentials')
#	ACCESS_KEY_ID = config.get('rayidpersonal', 'aws_access_key_id') 
#	ACCESS_SECRET_KEY = config.get('rayidpersonal', 'aws_secret_access_key') 

	imglogfile='../data/imgscores.log'
	s3bucket='rayid-personal'
	imgdir ='latteart-images/'
	
	with open(imglogfile, 'r') as file:
		lines = file.readlines()
    	for line in lines:
    		extract=re.match("^.*(http.*?)\,(.*?)$",a)
			url=extract.group(1)
			score=float(extract.group(2))
			print("%s,%s",url,extract.group(2))


