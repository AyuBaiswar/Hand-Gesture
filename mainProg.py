from sqlite3 import *
from keras.models import load_model
import cv2
import numpy as np
from collections import deque
import math
import pyautogui
import subprocess
import os

def mainFunc(url):
	c= connect("clist.db")
	cur = c.cursor()

	x=26
	def fetcher(x):
		cur.execute("select paath from clist where alph = %r"%(str(letters[x])))
		cm = cur.fetchall()
		for i in cm:
			exec(i[0])
			


	# Load the models built in the previous steps
	mlp_model = load_model('emnist_mlp_model.h5')
	cnn_model = load_model('emnist_cnn_model.h5')

	# Letters lookup
	letters = { 1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j',
	11: 'k', 12: 'l', 13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't',
	21: 'u', 22: 'v', 23: 'w', 24: 'x', 25: 'y', 26: 'z', 27: '-'}

	#detect face can be added here
	#sloppy detection occurs
	#detect face and put a rectangle

	if(url!='0'):
		#url=0
		#url = 'http://192.168.1.36:8080/video'
		cap = cv2.VideoCapture(str(url))
	else:
		cap = cv2.VideoCapture(int(url))

	lower = np.array([80, 135, 85], dtype = "uint8")
	upper = np.array([255, 180, 135], dtype = "uint8")

	# Define Black Board
	blackboard = np.zeros((480,640,3), dtype=np.uint8)
	alphabet = np.zeros((200, 200, 3), dtype=np.uint8)


	points = deque(maxlen=512)


	# Define prediction variables
	prediction1 = 26
	prediction2 = 26

	index = 0


	while True:
		_ , frame = cap.read()
		frame = cv2.flip(frame,1)

		conv = cv2.cvtColor( frame , cv2.COLOR_BGR2YCR_CB )
		skin = cv2.inRange( conv , lower , upper )
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
		#skin = cv2.erode(skin, kernel, iterations = 2)
		#skin = cv2.dilate(skin, kernel, iterations = 2)
		
		skin = cv2.morphologyEx( skin , cv2.MORPH_CLOSE , kernel )

		# blur the mask to help remove noise, then apply the
		# mask to the frame
		skin = cv2.GaussianBlur(skin, (3, 3), 0)
		skinr = cv2.bitwise_and(frame, frame, mask = skin)
		


		contours , _ = cv2.findContours( skin , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE )
		contour = contours[0]

		if len(contours) > 0:
			
			contourr = sorted(contours , key = cv2.contourArea , reverse = True)
			contour = contourr[0]
			hull = cv2.convexHull(contour , returnPoints = False)
			
			
		if cv2.contourArea(contour) > 7000 and cv2.contourArea(contour) < 15000:
			defects = cv2.convexityDefects(contour, hull)
			cv2.drawContours(frame,contour ,-1,(255,0,0), thickness = 5)

			((a, b), radius) = cv2.minEnclosingCircle(contour)


	        # Get the moments to calculate the center of the contour (in this case Circle)
			M = cv2.moments(contour)
			center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

					


			#inner cicle
			if defects is not None and center is not None:
				s = defects[:, 0][:, 0]
				cx, cy = center

				x = np.array(contour[s][:, 0][:, 0], dtype=np.float)
				y = np.array(contour[s][:, 0][:, 1], dtype=np.float)

				xp = cv2.pow(cv2.subtract(x, cx), 2)
				yp = cv2.pow(cv2.subtract(y, cy), 2)
				dist = cv2.sqrt(cv2.add(xp, yp))

				dist_max_i = np.argmin(dist)

				if dist_max_i < len(s):
					farthest_defect = s[dist_max_i]
					farthest_point = tuple(contour[farthest_defect][0])
					fare = math.sqrt((farthest_point[0]-center[0])**2 + (farthest_point[1]-center[1])**2)

					if(int(radius)-int(fare)<40):
			        	# Draw the circle around the contour
						cv2.circle(frame, (int(a), int(b)), int(radius), (0, 255, 255), 2)
						cv2.circle(frame, (int(a) , int(b)), int(fare), [0, 0, 255], 2)





			count_defects = 0

			for i in range(defects.shape[0]):
				s, e, f, d = defects[i, 0]
				start = tuple(contour[s][0])
				end = tuple(contour[e][0])
				far = tuple(contour[f][0])

				a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
				b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
				c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
				angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

	            # if angle > 90 draw a circle at the far point
				if angle <= 90:
					count_defects += 1
					cv2.circle(frame, far, 1, [0, 0, 255], -1)

				cv2.line(frame, start, end, [0, 255, 0], 2)

	        # Print number of fingers
			if count_defects == 0:
				cv2.putText(frame, "1", (400, 470), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,0,255),2)
			elif count_defects == 1:
				cv2.putText(frame, "2", (400, 470), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,0,255), 2)        
			elif count_defects == 2:
				cv2.putText(frame, "3", (400, 470), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,0,255), 2)          
			elif count_defects == 3:
				cv2.putText(frame, "4", (400, 470), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,0,255), 2)      
			elif count_defects == 4:
				cv2.putText(frame, "Gesture", (400, 470), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,255,0), 2)

				points.appendleft(center)

				#connecting points using line
				for i in range(1, len(points)):
					if points[i - 1] is None or points[i] is None:
						continue                    
					cv2.line(frame, points[i - 1], points[i], (0, 0, 0), 2)	
			else:
				pass
		
		else:
			if len(points) != 0:
				blackboard_gray = cv2.cvtColor(blackboard, cv2.COLOR_BGR2GRAY)
				blur1 = cv2.medianBlur(blackboard_gray, 15)
				blur1 = cv2.GaussianBlur(blur1, (5, 5), 0)
				thresh1 = cv2.threshold(blur1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
				(blackboard_cnts, _) = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
				if len(blackboard_cnts) >= 1:
					cnt = sorted(blackboard_cnts, key = cv2.contourArea, reverse = True)[0]

					if cv2.contourArea(cnt) > 1000:
						x, y, w, h = cv2.boundingRect(cnt)
						alphabet = blackboard_gray[y-10:y + h + 10, x-10:x + w + 10]
						newImage = cv2.resize(alphabet, (28, 28))
						newImage = np.array(newImage)
						newImage = newImage.astype('float32')/255

						prediction1 = mlp_model.predict(newImage.reshape(1,28,28))[0]
						prediction1 = np.argmax(prediction1)

						prediction2 = cnn_model.predict(newImage.reshape(1,28,28,1))[0]
						prediction2 = np.argmax(prediction2)

	            # Empty the points deque and the blackboard
				points = deque(maxlen=512)
				blackboard = np.zeros((480, 640, 3), dtype=np.uint8)

	    # Connect the points with a line
		for i in range(1, len(points)):
				if points[i - 1] is None or points[i] is None:
					continue                    
				cv2.line(frame, points[i - 1], points[i], (0, 0, 0), 2)
				cv2.line(blackboard, points[i - 1], points[i], (255, 255, 255), 8)

    	# Put the result on the screen
		p1= prediction1
		p2= prediction2
		cv2.putText(frame, "Multilayer Perceptron : " + str(letters[int(p1)+1]), (10, 450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7,(255, 255, 255), 2)
		cv2.putText(frame, "Convolution Neural Network:  " + str(letters[int(p2)+1]), (10, 470), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (255, 255, 255), 2)
		if(str(letters[int(prediction1)+1]) == str(letters[int(prediction2)+1]) and prediction2 != 26): 
			fetcher(int(prediction1)+1)
			prediction1 = 26
			prediction2 = 26
			points = deque(maxlen=512)
			blackboard = np.zeros((480, 640, 3), dtype=np.uint8)	
    	#cv2.imshow("dil",dil)
		cv2.imshow("ero",skinr)
   
		#cv2.imshow("clo",clo)
		#cv2.imshow("mask",mask)
		#cv2.imshow("final",final)
		cv2.imshow("fl",frame)

		# show the skin in the image along with the mask


		# if the 'q' key is pressed, stop the loop
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break


	cap.release()
	cv2.destroyAllWindows()