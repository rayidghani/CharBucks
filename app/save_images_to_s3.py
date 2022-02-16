import boto3
import configparser
import csv
from yelp_helper import get_image_from_url
import base64
import binascii
import urllib
import botocore

def main():
#	ACCESS_KEY_ID = ''
#	ACCESS_SECRET_KEY = ''
#	config = configparser.RawConfigParser()
#	config.read('/Users/rayid/.aws/credentials')
#	ACCESS_KEY_ID = config.get('rayidpersonal', 'aws_access_key_id') 
#	ACCESS_SECRET_KEY = config.get('rayidpersonal', 'aws_secret_access_key') 

	imglogfile='../data/imgscores.log'
	s3bucket='rayid-personal'
	directory='latteart-images/'
	imgdir ='latteart-images/'
	


	session = boto3.Session(profile_name='rayidpersonal')
#	aws_access_key_id=ACCESS_KEY_ID,
#	aws_secret_access_key=ACCESS_SECRET_KEY
#
#	)
	s3 = boto3.resource('s3') 

	with open(imglogfile, 'r') as file:
		csvreader = csv.reader(file)
		for row in csvreader:
			print(row[3])
			filename = a=urllib.parse.quote(row[3],'')
			#base64.b64decode('aHR0cDovL2V4YW1wbGUuY29tL2hlcmUvdGhlcmUvaW5kZXguaHRtbA==')
			try:
				s3.Object(s3bucket, directory+filename).load()
			except botocore.exceptions.ClientError as e:
				if e.response['Error']['Code'] == "404":
					# The object does not exist.
					if get_image_from_url(row[3], 'image.jpg'):   
						s3.Bucket(s3bucket).upload_file('image.jpg',directory+filename)
					else:
						print("error")
				else:
					# Something else has gone wrong.
					raise
			else:
				# The object does exist.
				print("exists")
			


if __name__ == '__main__':
	main()
