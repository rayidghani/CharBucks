import boto3
import configparser
import csv
from yelp_helper import get_image_from_url
import base64
import binascii
import urllib


def main():
	ACCESS_KEY_ID = ''
	ACCESS_SECRET_KEY = ''
	config = configparser.RawConfigParser()
	config.read('/Users/rayid/.aws/credentials')
	ACCESS_KEY_ID = config.get('rayidpersonal', 'aws_access_key_id') 
	ACCESS_SECRET_KEY = config.get('rayidpersonal', 'aws_secret_access_key') 

	imglogfile='../data/imgscores.log'
	session = boto3.Session(
	aws_access_key_id=ACCESS_KEY_ID,
	aws_secret_access_key=ACCESS_SECRET_KEY
	)

	with open(imglogfile, 'r') as file:
		csvreader = csv.reader(file)
		for row in csvreader:
			print(row[3])
			filename = a=urllib.parse.quote(row[3],'')
			#base64.b64decode('aHR0cDovL2V4YW1wbGUuY29tL2hlcmUvdGhlcmUvaW5kZXguaHRtbA==')
			if get_image_from_url(row[3], 'image.jpg'):
				s3 = boto3.resource('s3')    
				s3.Bucket('rayid-personal').upload_file('image.jpg','latteart-images/'+filename)
			else:
				print("error")



if __name__ == '__main__':
	main()
