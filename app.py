from flask import Flask, render_template, request, session, flash, Response
import re
import cv2
from onlineproctor import head_pose_detect, detect_phone_person, detect_faces_wc
import torch
import os
import pickle
import face_recognition
import pandas as pd


app= Flask(__name__)

app.secret_key= 'your secret key'

images={}
encoding={}

if (os.path.exists("face_images")==0):
    os.mkdir("face_images")

if os.path.exists('known_face_names.txt'):
    with open('known_face_names.txt','rb') as fp:
        known_face_names=pickle.load(fp)
else:
    known_face_names=[]

if os.path.exists('known_face_encodings.txt'):
    with open('known_face_encodings.txt','rb') as fp:
        known_face_encodings=pickle.load(fp)
else:
    known_face_encodings=[]



model= torch.hub.load('ultralytics/yolov5', 'yolov5s')
index = 0

def make_encoding(username,known_face_encodings, file_path):
    images[username]=face_recognition.load_image_file(file_path)
    encoding[username]=face_recognition.face_encodings(images[username])[0]
    known_face_encodings.append(encoding[username])

def generate_frames(model, known_face_encodings,known_face_names):
    camera = cv2.VideoCapture(0)
    candidates = pd.read_csv('candidates.csv')
    global index
    username = candidates[candidates.id == index].username.values[0]
    while True:
        ## read the camera frame
        
        success,frame=camera.read()
        if not success:
            break
        else:
            left, right, top, bottom, name= detect_faces_wc(known_face_encodings,known_face_names, frame) # detecting and recognising faces
            if(name!= -1):
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                if(name != username):
                    cv2.putText(frame, 'Unknown', (left + 6, bottom - 6),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
                    cv2.putText(frame, "Unknown person detected", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                else:
                    cv2.putText(frame, name, (left + 6, bottom - 6),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
            head_pos_text= head_pose_detect(frame) # detecting head position and raising alerts
            if head_pos_text!='Forward': 
                cv2.putText(frame, head_pos_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            obj_det_text= detect_phone_person(model, frame) # detecting phone and multiple person
            if obj_det_text!=' ':
                cv2.putText(frame, obj_det_text, (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()
    cv2.destroyAllWindows()


@app.route("/", methods=["GET", "POST"])
def register():
    msg=""
    if (os.path.exists("candidates.csv")):
        candidates = pd.read_csv('candidates.csv')
    else:
        candidates = pd.DataFrame(columns = ['id', 'username', 'password', 'gender'])
    if request.method=="POST" :
        #Fetching data from registeration page
        files= request.files["filename"]
        username=request.form["Username"]
        password=request.form["psw"]
        gender= request.form["gender"]
        if (candidates[candidates.username == username].shape[0] != 0):
            msg = 'Account already exists !'
            flash("Account already exists !")
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
            flash(msg)
        elif not username or not password or not gender:
            msg = 'Please fill out the form !'
            flash(msg)
        else:
            known_face_names.append(username)
            file_path = os.path.join("face_images",username+"."+files.filename.split('.')[1])
            files.save(file_path)
            make_encoding(username,known_face_encodings, file_path)
            with open('known_face_names.txt', 'wb') as fp:
                pickle.dump(known_face_names,fp)
            with open('known_face_encodings.txt', 'wb') as fp:
                pickle.dump(known_face_encodings,fp)
            new_row = {'id': candidates.shape[0] + 1,'username' : username, 'password' : password, 'gender' : gender}
            global index
            index = candidates.shape[0] + 1
            candidates = candidates.append(new_row, ignore_index = True)
            candidates.to_csv('candidates.csv', index=False)
            
            return render_template("dashboard.html", name=username, msg=msg)

        
    return render_template("register.html", msg=msg)


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ''
    candidates = pd.read_csv('candidates.csv')
    if request.method=="POST" and 'Username' in request.form and 'psw' in request.form: # fetching information from login page
        username= request.form["Username"]
        password=request.form["psw"]
        person = candidates[(candidates.username == username) & (candidates.password == password)].head(1)
        if person.shape[0] > 0:
            session['loggedin'] = True
            session['id'] = int(person['id'].values[0])
            global index
            index = int(person['id'].values[0])
            session['username'] = person['username'].values[0]
            return render_template("dashboard.html", name=username)
        else:
            msg = 'Incorrect username / password !'
            
    return render_template("login.html", msg=msg)


@app.route("/student_profile",  methods=["GET", "POST"])
def student_profile():
    if request.method=="POST":
        return render_template("test.html")
    else:
        global index
        candidates = pd.read_csv('candidates.csv')
        name = candidates[candidates.id == index].username.values[0]
        return render_template("dashboard.html", name=name)

@app.route("/test")
def test():
    return Response(generate_frames(model, known_face_encodings,known_face_names),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ =='__main__':
    app.run(debug=True)