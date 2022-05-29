# A-EYE (Online Proctoring System)
Online Education has its own advantage and disadvantage. On one hand, it has made life easier by allowing students to access their study material anytime and anywhere, on the other hand, it has hampered the overall process and quality of exams because of various malpractices. In order to avoid these malpractices, I have developed an AI-based proctoring system that will keep track of a candidate's activity and will raise alert messages if any malpractice is observed.

A-EYE is an AI-based proctoring system. It has following features.
- Basic registration and login page
- Student dashboard page
- Test page which will switch the video cam on and keep an eye on the candidate. It is capable of recognizing the candidate, detecting  the mobile phone and head positions, and raising alert messages if any malpractice is observed.

# User Guide
Steps to run this on your local computer:
- You need to have Python installed on your device to run this. You can download Python from [here](https://www.python.org/downloads/)

- Make a folder in your local computer where you want to save the files

- Clone this repository by typing the following command in the powershell of created folder
```
git clone https://github.com/Nidhi15-02/A-EYE--Online-Proctoring-System-
```
- Go to the folder formed by cloning the github repository
```
cd <path to the cloned repo>
```
- Make a new virtual environment in python in the folder in which this repository is saved and Active the Environment.
```
pip install virtualenv
python -m venv <myenvname> 
path\to\venv\Scripts\Activate.ps1  (Run this line with your path to activate the virtual environment)
```
- Download the requirements of the environment using
```
pip install -r requirements.txt
```
- Now run the website
```
flask run
```

# Important Instructions
- Rename your image by your first name before uploading it on the registration page. Also use your recent image in which your face is clearly visible(passport size image recommended). Supported formats are .png, .jpg, .jpeg
- Make sure that you are sitting in a properly lightened room where your face is clearly visible

# Methodology
The main model consist of three functions:

- head_pose_detect(): This function uses six face landmarks i.e nose tip, chin, left and right end points of eyes and lips to detect the position of the head. This functions detects whether the person is looking left aur right and accordingly raise alert message.

- detect_face_wc(): This function detect face on the webcam,and then compares the face with the image uploaded while registering, checks whether both the images match and even returns the co-ordinates of the face of the person. It raises an alert message if the faces do not match. It helps in recognising whether the person giving the exam is same as the person from whose account the exam is opened.

- detect_phone_person():This function makes use of YOLOv5 model to detect if the candidate is using phone.

# Website Screenshots
![Register Page](https://github.com/Nidhi15-02/A-EYE--Online-Proctoring-System-/blob/main/Register_page.png?raw=true)
![Login Page](https://github.com/Nidhi15-02/A-EYE--Online-Proctoring-System-/blob/main/Login_page.png?raw=true)
![Dashboard Page](https://github.com/Nidhi15-02/A-EYE--Online-Proctoring-System-/blob/main/Dashboard_page.png?raw=true)
![test Page](https://github.com/Nidhi15-02/A-EYE--Online-Proctoring-System-/blob/main/test_page.png?raw=true)

# Limitations
- It cannot detect the occluded faces
- Video FPS is low due to lack of computational resources.

