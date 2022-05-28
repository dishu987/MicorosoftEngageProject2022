from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import StudentName
from .forms import CreateNewList,studentRegistration
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
import face_recognition
import cv2
import numpy as np
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
import os
# Create your views here.
#This is function for Encoding Sensitive URL Information
def Enc(num):
    data = str(num)
    # conversion Chart
    conversion_code = {
	    #numbers
	    '1':'z','2':'a','3':'b','4':'c','5':'d','6':'e','7':'f','8':'g','9':'h','0':'i', 
    }
    # Creating converted output
    converted_data = ""
    for i in range(0, len(data)):
	    if data[i] in conversion_code.keys():
		    converted_data += conversion_code[data[i]]
	    else:
		    converted_data += data[i]

        # Printing converted output
    return converted_data
#This is function for Decoding Sensitive URL Information
def Dec(MSG):
    conversion_code = {
	    #numbers
	    'z':'1','a':'2','b':'3','c':'4','d':'5','e':'6','f':'7','g':'8','h':'9','i':'0', 
    }
    # Creating converted output
    converted_data = ""
    for i in range(0, len(MSG)):
	    if MSG[i] in conversion_code.keys():
		    converted_data += conversion_code[MSG[i]]
	    else:
		    converted_data += MSG[i]
        # Printing converted output
    return converted_data

#Student Page(Scanner Page)
def student(response):
    context = {
        'username':response.user.username,
        'temp':False,
        'nav2' : 'Sign Up',
    }
    return render(response,"main/student.html",context)

#This is manual page
def manual(response):
    context = {
        'username':response.user.username,
        'temp':False,
        'nav2' : 'Sign Up',
    }
    return render(response,"main/manual.html",context)
#home page
def home(response):
    logout(response)
    students = StudentName.objects.filter(present=True).order_by('updated').reverse()
    if response.user.is_anonymous:
        context = {"message": "You are not logged in"}
        context["entry"] = ""
        context["nav1"] = "Student Login"
        context["link1"] = "login"
        context["nav2"] = "Sign Up"
        context["link2"] ="loginProf"
        context["students"] = students
    else:
        context = {"message": f"You are logged in as {response.user.username}"}
        context["entry"] = response.user.username
        context["nav2"] = f"Logout ({response.user.username})"
        context["link2"] = "/loginProf/"
        context["students"] = students
    return render(response, "main/home.html",context)

#this is secure professor deshboar panel
def secureLog(request):
    students = StudentName.objects.all().values()
    if request.method == "POST":
        if request.POST.get("first") == 'first':
            submitted_form = studentRegistration(request.POST, request.FILES)
            if submitted_form.is_valid():
                submitted_form.save()
                messages.info(request,'Conratulations! Saved.')
            else:
                messages.error(request,'Error! You make mistake to fill information.')
        elif request.POST.get("second")=='second':
            ID = request.POST.get("ID")
            record = StudentName.objects.get(id = ID)
            record.delete()
            messages.warning(request,'Warning! Deleted Successfuly.')
        elif request.POST.get("third")=='third':
            ID1 = request.POST.get("ID1")
            Encd = Enc(ID1)
            Url = 'edit/'+Encd
            return redirect(Url)
        elif request.POST.get("forth")=='forth':
            st = StudentName.objects.all()
            for x in st:
                x.present=False
                x.save()
            messages.success(request,'Reseted Successfuly!')
        return redirect('secureLog')
   
    fm = studentRegistration()
    context = {
        'students':students,
        'username':request.user.username,
        'temp':True,
        'form':fm,
    }
    return render(request, 'main/secureLog.html',context)

#this is login page for professor
def loginProf(request):
    temp = False
    logout(request)
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            temp=True
            fm = studentRegistration(request.POST,request.FILES)
            context = {
                'username':request.user.username,
                'temp':True,
                'fm':fm,
            }
            return redirect('/secureLog/',context)
        else:
            temp=False
            messages.error(request,'Error! Wrong username or password.')
    form = UserCreationForm()
    if request.user.is_anonymous:
        context = {"message": "You are not logged in"}
        context["form"]=form
        context["entry"] = ""
        context["nav1"] = "Student Login"
        context["link1"] = "login"
        context["nav2"] = "Sign Up"
        context["link2"] = "loginProf"
    else:
        context = {"message": f"You are logged in as {request.user.username}"}
        context["entry"] = request.user.username
        context["form"]=form
        context["nav2"] = f"Logout ({request.user.username})"
        context["link2"] = "loginProf"
    return render(request, "main/loginProf.html",context)
#signout page
def signout(request):
    logout(request)
    return redirect('home')

#Core : Using OpenCV-py and Face-recognition-py
def scan(request):
    known_face_encodings = []
    known_face_names = []
    #get all students objects informations
    profiles = StudentName.objects.all()
    #add name of student and image encodings in containers...
    for profile in profiles:
        person = profile.image
        image_of_person = face_recognition.load_image_file(f'media/{person}')
        person_face_encoding = face_recognition.face_encodings(image_of_person)[0]
        known_face_encodings.append(person_face_encoding)
        known_face_names.append(f'{person}'[:-4])
    #capture video from camera of by help of OpenCV-py
    video_capture = cv2.VideoCapture(0)
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
	    
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding)
                name = "Unknown"
		
                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
		#if face encodings matches with camera image encodings
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    profile = StudentName.objects.get(Q(image__icontains=name))
	            #name variable is equal to that student name(it will be use to dispay on camera window)
                    name = profile.name
		    #make attendance true of that student
                    profile.present = True
		    #set time
                    profile.updated = timezone.now()
		    #save object
                    profile.save()
                face_names.append(name)

        process_this_frame = not process_this_frame
	#show name on camera window
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 0.5, (255, 255, 255), 1)

        cv2.imshow('Face-Recognition', frame)
	#if press q then camera window will close
        if cv2.waitKey(1) == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return redirect('home')

#this is edit page
def edit(request,id):
    #first decode id from url
    ID = Dec(id)
    #convert into decimal
    ID1 = int(ID,10)
    #get that student by id
    record = StudentName.objects.get(id = ID1)
    if request.method == "POST":
        submitted_form = studentRegistration(request.POST, request.FILES,instance=record)
        if submitted_form.is_valid():
            submitted_form.save()
            messages.success(request,'Conratulations! Saved.')
        else:
            messages.error(request,'Error! you fill something wrong.')
    else:
        messages.warning(request,'Warning! Fill only valid information.')
    G = record.gender
    A = False
    B = False
    C = False
    if G=="Male":
        A = True
    elif G=="Female":
        B = True
    elif G=="Not Specified":
        C = True
    context = {
        'username':request.user.username,
        'temp':True,
        'record':record,
        'Male':A,
        'Female':B,
        'NS':C,
    }
    return render(request, "main/edit.html",context)
