"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import cv2
from gaze_tracking import GazeTracking
val =[]
# Blinking = []
# right = []
# left=[]
# center=[]
def mouth_aspect_ratio(mouth):
	# compute the euclidean distances between the two sets of
	# vertical mouth landmarks (x, y)-coordinates
	A = dist.euclidean(mouth[2], mouth[10]) # 51, 59
	B = dist.euclidean(mouth[4], mouth[8]) # 53, 57

	# compute the euclidean distance between the horizontal
	# mouth landmark (x, y)-coordinates
	C = dist.euclidean(mouth[0], mouth[6]) # 49, 55

	# compute the mouth aspect ratio
	mar = (A + B) / (2.0 * C)

	# return the mouth aspect ratio
	return mar

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=False, default='shape_predictor_68_face_landmarks.dat',
	help="path to facial landmark predictor")
ap.add_argument("-w", "--webcam", type=int, default=0,
	help="index of webcam on system")
args = vars(ap.parse_args())

# define one constants, for mouth aspect ratio to indicate open mouth
MOUTH_AR_THRESH = 0.70

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# grab the indexes of the facial landmarks for the mouth
(mStart, mEnd) = (49, 68)

# start the video stream thread
print("[INFO] starting video stream thread...")

time.sleep(1.0)

frame_width = 640
frame_height = 360
def ply():

        gaze = GazeTracking()
        webcam = cv2.VideoCapture(0)

        while True:
        # We get a new frame from the webcam
            _, frame = webcam.read()
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # detect faces in the grayscale frame
            rects = detector(gray, 0)

            # loop over the face detections
            for rect in rects:
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                # extract the mouth coordinates, then use the
                # coordinates to compute the mouth aspect ratio
                mouth = shape[mStart:mEnd]

                mouthMAR = mouth_aspect_ratio(mouth)
                mar = mouthMAR
                # compute the convex hull for the mouth, then
                # visualize the mouth
                mouthHull = cv2.convexHull(mouth)
                
                cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
                cv2.putText(frame, "MAR: {:.2f}".format(mar), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Draw text if mouth is open
                if mar > MOUTH_AR_THRESH:
                    print('hi')
                    print(MOUTH_AR_THRESH)
                    print(mar)
                    val.append('mouth')
                    # cv2.putText(frame, "Mouth is Open!", (30,60),
                    # cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
            # Write the frame into the file 'output.avi'
            

            # if the `q` key was pressed, break from the loop
            
                    # We send this frame to GazeTracking to analyze it
            gaze.refresh(frame)

            frame = gaze.annotated_frame()
            text = ""

            if gaze.is_blinking():
                text = "Blinking"
                val.append(text)

            elif gaze.is_right():
                text = "Looking right"
                val.append(text)

            elif gaze.is_left():
                text = "Looking left"
                val.append(text)

            elif gaze.is_center():
                text = "Looking center"
                val.append(text)


            cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

            left_pupil = gaze.pupil_left_coords()
            right_pupil = gaze.pupil_right_coords()
            cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

            cv2.imshow("Demo", frame)

            if cv2.waitKey(1) == 13:
                return val
                break