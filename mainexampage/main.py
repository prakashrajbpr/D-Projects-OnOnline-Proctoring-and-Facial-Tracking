from flask import Flask, render_template, Response
from flask import Flask,url_for,request,render_template,redirect,session,jsonify
import sqlite3
from flask_login import logout_user
from camera import VideoCamera,value
import webbrowser
import sys
import time
from flask_login import logout_user
import example
import pyautogui
from example import ply
import re
from face_detection import face_register,face_reg

out = []
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './media'

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
val1 =[]
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
r = 0
l = 0
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
                    val1.append('mouth')
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
                val1.append(text)

            elif gaze.is_right():
                text = "Looking right"
                val1.append(text)


            elif gaze.is_left():
                text = "Looking left"
                val1.append(text)
                

            elif gaze.is_center():
                text = "Looking center"
                val1.append(text)


            cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

            left_pupil = gaze.pupil_left_coords()
            right_pupil = gaze.pupil_right_coords()
            cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

            cv2.imshow("Demo", frame)

            if cv2.waitKey(1) == 13:
                return val1
                break
app.secret_key="Rudy"
@app.route('/')
def user():
    return render_template('user_page.html')

@app.route('/register', methods=["GET","POST"])
def reg():
    uname=None
    pwd=None
    cpwd=None
    ema=None
    msg="Register successfully"
    if request.method=='POST':
        uname=request.form['txt']
        pwd=request.form['passw']
        cpwd=request.form['cpassw']
        ema=request.form['em']
        t_id=request.form['id']
        gender=request.form['gender']
        payment=request.form['payment']
        print(payment)
        print(gender)
        import sqlite3
        table_name = 'studentregsiter'
        conn = sqlite3.connect("carparking.db")
        print('hi')
        #  conn = sqlite3.connect("carparking.db")
        r=conn.cursor()
        e=conn.cursor()
        id_num=conn.cursor()
        r.execute("select name from studentregsiter ")
        e.execute("select ema from studentregsiter ")
        id_num.execute("select id from studentregsiter ")
        rows=r.fetchall()
        rows_e=r.fetchall()
        rows_id=r.fetchall()
        for i in rows :
            for j in i:
                # print(i)
                if uname == j:
                    msg='already username registeredser'
                    return render_template('registraion.html',msg=msg)
                else:
                    pass    
        for i in rows_e:
            for j in i:
                if ema == j:
                    msg='already email registered'
                    return render_template('registraion.html',msg=msg)
                else:
                    pass   
        for i in rows_id:
            for j in i:
                if id == j:
                    msg='already id registered'
                    return render_template('registraion.html',msg=msg)
                else:
                    pass                             
        c = conn.cursor()
        c_1 = conn.cursor()

        c.execute('insert into '+table_name+'  values (?,?,?,?,?,?,?)',(uname,pwd,cpwd,ema,t_id,gender,payment))
        val = face_register(t_id)

        modalexam = 'null'
        mainexam = 'null'
        c_1.execute('create table if not exists mark (name varchar(50),id varchar(50),value varchar(50),malpartice varchar(50),allmark varchar(50))')
        value = 'null'
        allmark = 'null'
        malpartice = 'null'

        c_1.execute('insert into mark values (?,?,?,?,?)',(uname,t_id,value,allmark,malpartice))

        conn.commit()
        conn.close()
        return redirect(url_for('login'))
        # return render_template('registraion.html',msg=msg)
    return render_template('registraion.html')
@app.route('/login',methods=["GET","POST"])
def login():
    username=None
    password=None
    err="Invalid username and password"
    if request.method=='POST':
        session['username']=request.form['uname']
        session['vid']=request.form['pwd']
        id=request.form['id']

        username=request.form['uname']
        print(username)
        password=request.form['pwd']
        conn = sqlite3.connect("carparking.db")
        r=conn.cursor()
        r.execute("select name,pwd from studentregsiter where name=? and pwd=?",(username,password))
        rows=r.fetchall()
        print(rows)
        val = face_reg(id)
        if val == 'Authorized':
            if len(rows)!=0:
                for i in rows:
                    if i[0]==username and i[1]==password:
                        print(username)
                        session['logged_in'] = True
                        return redirect(url_for('student'))
                        return render_template('student.html',username=username)
            else:
                return render_template('login.html',err=err)



       



        else:
            return render_template('login.html',err=err)
    return render_template('login.html')
# @app.route('/logout')
# def logout():
#     session.pop('username',None)
#     return redirect(url_for('index'))
@app.route("/logout")
def logout():
    # logout_user()
    session.pop('username',None)

    return redirect(url_for('login'))
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/study')
def study_view():
    return render_template('study.html')

@app.route('/study_1')
def study_view_2():
    return render_template('study_1.html')

@app.route('/study_2')
def study_view_3():
    return render_template('study_2.html')

@app.route('/study_3')
def study_view_4():
    return render_template('study_3.html')


@app.route('/student_result/<value>')
def std_view(value):
    print(value)
    row = session["row"]
    pyautogui.press('enter')
    print(val1)
    Result = value
    blink = val1.count('Blinking')
    left = val1.count('Looking left') +1
    right = val1.count('Looking right')+1
    center = val1.count('Looking center')
    return render_template('student_result.html',blink=blink,left=left,right=right,center=center,Result=Result,rows=row)

# @app.route('/study_1')
# def study_view():
#     return render_template('study_1.html')
    
# @app.route('/study_2')
# def study_view():
#     return render_template('study_2.html')
# @app.route('/study_3')
# def study_view():
#     return render_template('study_3.html')    

@app.route('/blink')
def blink_view():
    user = session['username']
    print(user)
    conn = sqlite3.connect("carparking.db")
    ss=conn.cursor()
    ss.execute("select name,value from mark ")
    slotrow=ss.fetchall()
    for i ,j in slotrow:
        if user == i:
            sql="""update mark set value = ? where name = ?"""
            ss.execute(sql,['sleep',i])
            conn.commit() 
        print(i)
    return render_template('value_blink.html')    

@app.route('/exam')
def exam_view():
    return render_template('New/menu.html')

@app.route('/question')
def question_view():
    print('hi')
    # gen(VideoCamera())
    # video_feed()
    return render_template('New/question.html')

# @app.route('/exam')
# def exam():
#     return render_template('newindex.html')
@app.route('/moniter')
def moniter():
    a =ply()
    # out = a
    print('hi',val1)
    out.append(a)
    print(a)
    pass

@app.route('/student')
def student():
    login=False
    if 'username' in session:
        login=True
        user_name = session["username"]
        pwd = session['vid']
        conn = sqlite3.connect("carparking.db")
        r=conn.cursor()
        r.execute("select * from studentregsiter where name=? and pwd=?",(user_name,pwd))
        rows=r.fetchall()
        print(rows)
        session["row"] = rows[0]
        return render_template('student.html',login=login,username=user_name,rows=rows[0])
    return render_template('student.html',login=login)


    
# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



# @app.route('/video_feed')
# def video_feed():
#     user = session['username']
#     value(user)
#     return Response(gen(VideoCamera()),value(user),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')



# def main():
#     #sites=r"website.txt"
#     #sites="http://0.0.0.0:5000/"
#     #browser ="chrome"
#     chrome_path=r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
#     webbrowser.register("chrome",None,webbrowser.BackgroundBrowser(chrome_path))
#     web = webbrowser.get("chrome")
#     webbrowser.open_new_tab("http://localhost:5000/")
#     '''with open(sites) as fobj:
#         try:
#             for num,url in enumerate(fobj):
#                 web.open_new_tab(url.strip())
#                 time.sleep(1)
#         except Exception as e:
#             print(e)'''
# from flask_login import logout_user

# ...

# @app.route('/logout')
# def logout_view():
#     logout_user()
#     return redirect(url_for('index'))


@app.route('/valdiate',methods=['POST'])
def val():
    val_1 = request.form['val_1']
    val_2 = request.form['val_2']
    val_3 = request.form['val_3']
    conn=sqlite3.connect("carparking.db")
    l=conn.cursor()
    l.execute("select question,answer from question")
    val =l.fetchall()
    # for i,j in val:

    count = 0
    print(val)
    print('done')
    return jsonify({'success':'success'})
# @app.route('/question')
# def question():
#     conn=sqlite3.connect("carparking.db")
#     l=conn.cursor()
#     l.execute("select question from question")
#     val =l.fetchall()
#     one  = []
#     two = [ ]
#     qu  = []
#     for i in val:
#       print(i)
#       j = str(i)
#       v = j[2:-3]
#       print(v)
#       qu.append(v)

#     print(type(qu))
#     print(qu)
#     return render_template('question.html',qu=qu)

if __name__ == '__main__':
    app.run(host='localhost')
