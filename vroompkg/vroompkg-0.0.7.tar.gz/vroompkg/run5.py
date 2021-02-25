#python3 run3.py --prototxt deploy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel --shape-predictor shape_predictor_68_face_landmarks.data
#python3 run3.py --method 2 --smiling_video smiling2.mp4 --default_photo defaultphoto.jpg
# import the necessary packages
#from imutils import face_utils
#from scipy.spatial import distance as dist


import argparse
import csv
import cv2
from datetime import date
from datetime import datetime
#import detect as det
from . import detect as det
from . import src_path
import dlib
import imutils
from imutils import face_utils
from imutils.video import FileVideoStream
from imutils.video import VideoStream
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import time
import requests
import json

# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold
#EYE_AR_THRESH = 0.3
#EYE_AR_CONSEC_FRAMES = 3
# initialize the frame counters and the total number of blinks
#COUNTER = 0
#TOTAL = 0

#def filepaths():
#		head =os.getcwd()
#		folder_check = os.path.isdir(head)
#		if folder_check:
#			return head
#		else:
#			return os.path.dirname(head)
def vroom(args):

	vr = Vroom(args)
	#if(args["method"]=="1"):
	#	vr.calibrate(args["smiling_video"])
	#else:
	vr.webcam([src_path+"/defaultpic.png",src_path+"/smilepic.png",src_path+"/squintpic.png",src_path+"/widepic.png"])
	with open(Vroom.report_file_name, newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in spamreader:
			print(', '.join(row))
	engagement = vr.engagement
	indexes = [0]*len(engagement)

	for i in range(0, len(indexes)):
		indexes[i] = i
	plt.scatter(indexes, engagement)
	#plt.show()
	plt.savefig(date.today().strftime("%m-%d-%y") + ".png")#vr.report_file_name+'.png')


class Vroom:

	#create facial landmark predictor
	predictor = dlib.shape_predictor(src_path + "/shape_predictor_68_face_landmarks.dat") #/Users/manasi/Documents/zoom2/shape_predictor_68_face_landmarks.dat")
	# load our serialized model from disk
	print("[INFO] loading model...")
	net = cv2.dnn.readNetFromCaffe(src_path + "/deploy.prototxt.txt", src_path + "/res10_300x300_ssd_iter_140000.caffemodel")
	time.sleep(2.0)
	report_file_name = date.today().strftime("%m-%d-%y") + '.csv'


	def __init__(self, args):
		self.faces = []
		self.landmarks = []
		self.engagement = [0] #over all frames
		self.args = args

	def calibrate(self, video_path):
		print("[INFO] starting file video stream...")
		vs = FileVideoStream(path=video_path).start() #"/Users/manasi/Documents/data/smiling1.mp4").start()
		fileStream = True
		#vs = VideoStream(src = 0).start()
		#fileStream = False
		time.sleep(2.0)
		#mouths = []
		while True:
			if not vs.more():
				break
			frame = vs.read()
			if frame is None:
				break
			frame = imutils.resize(frame, width = 400)
			# get frame dimensions and convert it to a blob
			(h, w) = frame.shape[:2]
			blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

			# pass the blob through the network and obtain the detections and predictions
			Vroom.net.setInput(blob)
			detections = Vroom.net.forward()
			initial_ar = 0
			# loop over the detections
			for i in range(0, detections.shape[2]):
				# filter out weak detections by ensuring the confidence > minimum confidence
				confidence = detections[0, 0, i, 2]
				if confidence < .5:
					continue

				# compute the coordinates of the bounding box for the object
				box = detections[0, 0, i, 3:7]*np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				self.faces.append((startX, startY, endX, endY))

				shape = Vroom.predictor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), dlib.rectangle(startX, startY, endX, endY))
				shape = face_utils.shape_to_np(shape)
				self.landmarks.append(shape)

				text = "{:.2f}%".format(confidence*100)
				if(startY - 10 > 10):
					y = startY - 10 
				else:
					startY + 10
				cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2) #face
				for (x, y) in shape:
					cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
					cv2.putText(frame, text, (startX, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2) # face confidence
			cv2.imshow("Frame", frame)
			#print(n)
			key = cv2.waitKey(1) & 0xFF

			# if the 'q' key is pressed, break
			if key == ord("q"):
				break
		# cleanup
		cv2.destroyAllWindows() 
		vs.stop()

	def w_thres(self, first, second):
		threshold = ((self.landmarks[0][first][0]-self.landmarks[0][second][1])/(self.faces[0][2]-self.faces[0][0]))
		print("threshold")
		print(threshold)
		return threshold

	def writeAnalytics(file_name, rows, names, values, engagement):
		print(names)
		print(values)
		with open(file_name, 'w', newline='') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',',quotechar='\'', quoting=csv.QUOTE_MINIMAL)
			for num in range(0, rows):
				spamwriter.writerow([names[num],values[num]])


	def changePFP(self, filename):
		userid = self.args["userid"]
		jwt_token = args["token"] #'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6ImFSendZNDNfUnplNGlYZ21iOXQ0VGciLCJleHAiOjE2NDU2MDMyMDAsImlhdCI6MTYxNDA3MzY1MX0.UsS38GiCM2Xgw3MXduE9gREE3GKr_acv62RyC_8ahrI'
		filepath = src_path + '/' + filename #'/Users/manasiganti/Downloads/zoom2' + filename

		url = 'https://api.zoom.us/v2/users/{0}/picture'.format(userid)

		headers = {'Authorization': 'Bearer {}'.format(jwt_token),
		           'Accept': 'application/json',
		           }
		files = {'pic_file': open(filepath, 'rb')}

		response = requests.post(url, files=files, headers=headers)
		print(response.content)

	def isMeetingOver(self):
		import http.client

		conn = http.client.HTTPSConnection("api.zoom.us")

		headers = { 'authorization': ("Bearer " + args["token"])}

		conn.request("GET", "/v2/meetings/" + self.args["meetingid"], headers=headers)

		res = conn.getresponse()
		data = res.read()

		obj = json.loads(data.decode("utf-8"))
		try:
			print(obj["status"])
		except KeyError as e:
			return True
		if(obj["status"] == "waiting"):
			return True
		return False
		#return(data["status"] != "started")


	def webcam(self, pictures):
		print("[INFO] starting video stream...")
		vs = VideoStream(srcs = 0).start()
		time.sleep(2.0)
		if os.path.exists(Vroom.report_file_name):
			os.remove(Vroom.report_file_name)
		else:
			print("hi.csv does not exist")
		n = -1 #frame counting
		m = 0 #smile counting
		w = 0 #wide eyed counting
		s = 0 #squint counting
		close = 0 #close up counting
		far = 0 #far away counting
		frame1 = 0 #initial frame
		variables = [] #for reporting
		values = []
		# loop over the frames from the video stream
		net = Vroom.net
		predictor = Vroom.predictor
		while True:
			n+=1;
			self.engagement.append(0)

			real_frame = vs.read()
			if real_frame is None:
				break
			real_frame = imutils.resize(real_frame, width = 400)
			if n==0:
				frame1 = real_frame

			file_name = "defaultpic.jpg"

			isWide = det.Detect(Vroom.net, Vroom.predictor).wide(real_frame)
			isSquint = det.Detect(Vroom.net, Vroom.predictor).squint(real_frame)
			isSmile = det.Detect(Vroom.net, Vroom.predictor).smile(real_frame, .4)

			if isSmile: 
				m+= 1
				self.engagement[n] += 1
				file_name = ("smilepic.png")
			elif isWide:
				w+=1
				self.engagement[n] += 1
				file_name = ("widepic.png")

			elif isSquint:
				s+=1
				self.engagement[n] -= 1
				file_name = ("squintpic.png")

			else:
				file_name = ("defaultpic.png")

			size_diff = det.Detect(Vroom.net, Vroom.predictor).size_difference(real_frame, frame1)
			#CLOSE
			if size_diff > 1.5:
				close += 1
				self.engagement[n] += 1
			#FAR
			elif size_diff < .75:
				far += 1
				self.engagement[n] -= 1

			#show
			frame = cv2.imread(src_path + '/' + file_name)
			frame = imutils.resize(frame, width = 400)
			cv2.imshow("Frame", frame)
			self.changePFP(file_name)
			if(self.isMeetingOver()):
				break

			print(self.engagement)
		variables = ["SMILE %", "WiDe %","sQuInt %", "close %", "FAR %"]
		if n != 0:
			values = [(m/n)*100, (w/n)*100, (s/n)*100, (close/n)*100, (far/n)*100]
		else:
			values = [0,0,0,0,0]
		Vroom.writeAnalytics(Vroom.report_file_name, len(variables), variables, values, self.engagement)
		# cleanup
		cv2.destroyAllWindows()
		vs.stop()

