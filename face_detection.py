import cv2, sys, numpy, os
from random import randint
from face_liveness_detection_Anti_spoofing_master.face_anti_spoofing import liveness

def face_register(voter_id):
    print(voter_id)
    
    print('importing liveness')
    haar_file =r"C:\Users\RECS3\Desktop\Online-Proctoring-and-Facial-Tracking--master\haarcascade_frontalface_default.xml"
    datasets = './datasets'  
    sub_data = voter_id

    path = os.path.join(datasets, sub_data) 


    folder_count = 0  # type: int

    input_path = r"C:\Users\RECS3\Desktop\Online-Proctoring-and-Facial-Tracking--master\datasets"
    for folders in os.listdir(input_path):
        folder_count += 1


    if folder_count == 0:
        webcam = cv2.VideoCapture(0)
        val = liveness(webcam)
        if val == 'fail':
            print('your not allowed to register')
            webcam.release()
            cv2.destroyAllWindows()
            return 'your not allowed to register'
           
        else:
            if not os.path.isdir(path):
                os.mkdir(path)   
            (width, height) = (130, 100)   
            face_cascade=cv2.CascadeClassifier(haar_file)  
            count = 1
            while count<100:  
                (_, im) = webcam.read() 
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
                faces = face_cascade.detectMultiScale(gray, 1.3, 4) 
                for (x, y, w, h) in faces: 
                    cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2) 
                    face = gray[y:y + h, x:x + w] 
                    face_resize = cv2.resize(face, (width, height)) 
                    cv2.imwrite('% s/% s.png' % (path, count), face_resize) 
                count += 1
                cv2.imshow('OpenCV', im) 
                key = cv2.waitKey(10) 
                if key == 27: 
                    break
            webcam.release()
            cv2.destroyAllWindows()
            return 'your allowed to register'
        webcam.release()
        cv2.destroyAllWindows()
    else:
        size = 4
        haar_file ="D:\crt_project\smart_voting_CRT\haarcascade_frontalface_default.xml"
        datasets = './datasets'
        print('Recognizing Face Please Be in sufficient Lights...') 
        (images, lables, names, id) = ([], [], {}, 0) 
        for (subdirs, dirs, files) in os.walk(datasets): 
            for subdir in dirs: 
                names[id] = subdir 
                subjectpath = os.path.join(datasets, subdir) 
                for filename in os.listdir(subjectpath): 
                    path = subjectpath + '/' + filename 
                    lable = id
                    images.append(cv2.imread(path, 0)) 
                    lables.append(int(lable)) 
                id += 1
        (width, height) = (130, 100) 
        (images, lables) = [numpy.array(lis) for lis in [images, lables]] 
        model = cv2.face.LBPHFaceRecognizer_create() 
        model.train(images, lables) 
        face_cascade = cv2.CascadeClassifier(haar_file) 
        webcam = cv2.VideoCapture(0)

        su=1
        er=1
        while True: 
            (_, im) = webcam.read() 
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
            faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
            for (x, y, w, h) in faces: 
                cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2) 
                face = gray[y:y + h, x:x + w] 
                face_resize = cv2.resize(face, (width, height)) 
                prediction = model.predict(face_resize) 
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3) 
                if prediction[1]<70:
                    cv2.putText(im, '% s - %.0f' % (names[prediction[0]], prediction[1]), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 
                    su+=1
                else:
                    cv2.putText(im, 'not recognized',  (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 
                    er+=1
            cv2.imshow('OpenCV', im) 
            key = cv2.waitKey(10)  
            if key == 27: 
                break
            elif su==30:
                print("Already Registered")
                webcam.release()
                cv2.destroyAllWindows()
                return 'Already Registered'
                
            elif er==100:
                path = os.path.join(datasets, sub_data) 
                if not os.path.isdir(path):
                    os.mkdir(path)   
                (width, height) = (130, 100)   
                face_cascade=cv2.CascadeClassifier(haar_file)  
                val = liveness(webcam)
                print(val)
                if val == 'fail':
                    print('your not allowed to register')
                    return 'your not allowed to register'
                else:
                    count = 1
                    while count<109:  
                        (_, im) = webcam.read() 
                        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
                        faces = face_cascade.detectMultiScale(gray, 1.3, 4) 
                        for (x, y, w, h) in faces: 
                            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2) 
                            face = gray[y:y + h, x:x + w] 
                            face_resize = cv2.resize(face, (width, height)) 
                            cv2.imwrite('% s/% s.png' % (path, count), face_resize) 
                        count += 1
                        cv2.imshow('OpenCV', im) 
                        key = cv2.waitKey(10) 
                        if key == 27: 
                            break
                    webcam.release()
                    cv2.destroyAllWindows()
                    return 'your allowed to register'
                webcam.release()
                cv2.destroyAllWindows()
                break

def face_reg(name):
    size = 4
    haar_file ="D:\crt_project\smart_voting_CRT\haarcascade_frontalface_default.xml"
    datasets = './datasets'
    print('Recognizing Face Please Be in sufficient Lights...') 
    (images, lables, names, id) = ([], [], {}, 0) 
    for (subdirs, dirs, files) in os.walk(datasets): 
        for subdir in dirs: 
            names[id] = subdir 
            subjectpath = os.path.join(datasets, subdir) 
            for filename in os.listdir(subjectpath): 
                path = subjectpath + '/' + filename 
                lable = id
                images.append(cv2.imread(path, 0)) 
                lables.append(int(lable)) 
            id += 1
    (width, height) = (130, 100) 
    (images, lables) = [numpy.array(lis) for lis in [images, lables]] 
    print(images)
    model = cv2.face.LBPHFaceRecognizer_create() 
    model.train(images, lables) 
    face_cascade = cv2.CascadeClassifier(haar_file) 
    webcam = cv2.VideoCapture(0)
    su=1
    er=1
    while True: 
        (_, im) = webcam.read() 
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
        faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
        for (x, y, w, h) in faces: 
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2) 
            face = gray[y:y + h, x:x + w] 
            face_resize = cv2.resize(face, (width, height)) 
            prediction = model.predict(face_resize) 
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3) 
            if prediction[1]<70:
                cv2.putText(im, '% s - %.0f' % (names[prediction[0]], prediction[1]), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 
                su+=1
                if su==30:
                    if names[prediction[0]] == name :
                        return 'Authorized'
                    else:
                        return 'Invalid User'
            else:
                cv2.putText(im, 'not recognized',  (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 
                er+=1
                if er==50:
                    return 'Unauthorized' 
        cv2.imshow('OpenCV', im) 
        key = cv2.waitKey(10) 
        if key == 27: 
            break
    webcam.release()
    cv2.destroyAllWindows()


