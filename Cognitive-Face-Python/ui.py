 #import pandas as pd
import time
import cognitive_face as CF
from gtts import gTTS
import os
import random

# Replace with a valid subscription key (keeping the quotes in place).

#key_data=pd.read_csv("key_data.txt", delim_whitespace=True, skipinitialspace=True)
key_dat = open('key_data.txt',mode='r')
KEY = key_dat.read()
CF.Key.set(KEY)

# Replace with your regional Base URL
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)

# You can use this example JPG or replace the URL below with your own URL to a JPEG image.
#img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
#img1_url = 'Images\IMG_0835.jpg'
#img2_url = 'Images\IMG_0836.jpg'

choose_group_again = True
def add_person():
    speak_text = "HELLO! PLEASE ADD PERSON"
    language = 'en'
    myobj = gTTS(text=speak_text, lang=language, slow=False)
    myobj.save("add.mp3")
    os.system("mpg321 add.mp3 > /dev/null 2>&1")
    print("ADD PERSON\n\n")
    print("Choose which group you want to add the person to : ")
    groups = CF.person_group.lists()
    for index in groups:
       print(index["name"])
    print("")
    correct_group = False
    req_name = ""
    req_group_name = input("Enter name : ")
    for index in groups:
        if index["name"] == req_group_name:
            correct_group = True
            print(index["name"] + " has beeen chosen")
        else:
            print("No such group found")
    print(correct_group)
    if correct_group:
        req_name = input("Enter name of person to be added to " + req_group_name + " ")
        print(req_name)
        CF.person.create(req_group_name,req_name)
        speak_text = "HELLO! PERSON HAS BEEN ADDED"
        language = 'en'
        myobj = gTTS(text=speak_text, lang=language, slow=False)
        myobj.save("added.mp3")
        os.system("mpg321 added.mp3 > /dev/null 2>&1")
        add_face()
    else:
        choose_again = input("Choose group again? ")
        if choose_again == "Yes" or choose_again == "Y" or choose_again == "T":
            print("")
            print("")
            add_person()

do_train = False
def train_group():
    speak_text = "HELLO! TIME TO TRAIN A GROUP"
    language = 'en'
    myobj = gTTS(text=speak_text, lang=language, slow=False)
    myobj.save("train.mp3")
    os.system("mpg321 train.mp3 > /dev/null 2>&1")
    print("TRAIN GROUP\n\n")
    global do_train
    groups = CF.person_group.lists()
    for index in groups:
       print(index["name"])
    print("")
    correct_group = False
    group_to_train=input("Choose group to train : ")
    for index in groups:
        if index["name"] == group_to_train:
            correct_group = True
            print(index["name"] + " has beeen chosen")
    print(correct_group)
    if correct_group:
        print("Training group " + group_to_train)
        CF.person_group.train(group_to_train)
        speak_text = "HELLO! GROUP HAS BEEN TRAINED"
        language = 'en'
        myobj = gTTS(text=speak_text, lang=language, slow=False)
        myobj.save("trained.mp3")
        os.system("mpg321 trained.mp3 > /dev/null 2>&1")
    else:
        choose_again = input("Choose group again? ")
        if choose_again == "Yes" or choose_again == "Y" or choose_again == "T":
            print("")
            print("")
            train_group()

def verify_face():
    yes_zingers = [
    "HELLO! YOU HAVE BEEN IDENTIFIED",
    "OHHH! YOU HAVE BEEN GRANTED ACCESS TO THE SYSTEM",
    "HELLO! ACCESS HAS BEEN GRANTED TO YOU",
    "GOOD JOB, ACCESS HAS BEEN GIVEN TO YOU"
    "WELL DONE! YOU ARE VERIFIED"
    ]
    no_zingers = [
    "INTRUDER ALERT! INTRUDER ALERT! INTRUDER ALERT!",
    "YOU HAVE NOT BEEN GRANTED ACCESS",
    "ILLEGAL PERSON HAS ENTERED",
    "NOT APPROVED HERE! PLEASE LEAVE",
    "SECURITY! SECURITY! THIS PERSON IS NOT AUTHORIZED TO BE HERE"
    ]
    random_num = random.randint(0,4)
    print(random_num)
    isIdentified = False
    speak_text = "HELLO! TIME TO IDENTIFY A FACE"
    language = 'en'
    myobj = gTTS(text=speak_text, lang=language, slow=False)
    myobj.save("identify.mp3")
    os.system("mpg321 identify.mp3 > /dev/null 2>&1")
    print(speak_text + "\n\n")
    groups = CF.person_group.lists()
    for index in groups:
       print(index["name"])
    print("")
    correct_group = False
    group_to_train = input("Choose group to identify from : ")
    for index in groups:
        if index["name"] == group_to_train:
            correct_group = True
            print(index["name"] + " has beeen chosen")
    if correct_group:
        print(correct_group)
        img_link = input("Choose image link to verify : ")
        face_to_verify = CF.face.detect(img_link)
        req_face_id = face_to_verify[0]["faceId"]
        #print(req_face_id)
        people_in_group = CF.person.lists(group_to_train)
        for index in people_in_group:
            rate_confidence = CF.face.verify(face_id = req_face_id, person_group_id=group_to_train, person_id= index["personId"])
            print(index["name"] + " : "+str(100*rate_confidence["confidence"]) + "% similar")
            if(rate_confidence["isIdentical"] == True):
                isIdentified = True
                print("Person verified is " + index["name"])
                print(rate_confidence["confidence"]*100)
                speak_text = "HELLO! THE PERSON IS " + index["name"] + "......" + yes_zingers[random_num]
                language = 'en'
                myobj = gTTS(text=speak_text, lang=language, slow=False)
                myobj.save("identifed.mp3")
                os.system("mpg321 identifed.mp3 > /dev/null 2>&1")
    else:
        choose_again = input("Choose group again? ")
        if choose_again == "Yes" or choose_again == "Y" or choose_again == "T":
            print("")
            print("")
            verify_face()
    if isIdentified == False:
        print("Person not identifed")
        speak_text = "HELLO!" + no_zingers[random_num]
        language = 'en'
        myobj = gTTS(text=speak_text, lang=language, slow=False)
        myobj.save("unidentifed.mp3")
        os.system("mpg321 unidentifed.mp3 > /dev/null 2>&1")

def add_face():
    speak_text = "PLEASE ADD FACE"
    language = 'en'
    myobj = gTTS(text=speak_text, lang=language, slow=False)
    myobj.save("add_face.mp3")
    os.system("mpg321 add_face.mp3 > /dev/null 2>&1")
    print("ADD FACE\n\n")
    print("Choose which group you want to add the face to : ")
    groups = CF.person_group.lists()
    for index in groups:
       print(index["name"])
    print("")
    correct_group = False
    req_name = ""
    req_group_name = input("Enter name of group : ")
    for index in groups:
        if index["name"] == req_group_name:
            correct_group = True
            print(index["name"] + " has beeen chosen" + "Tareq was right")
    print(correct_group)
    print(req_group_name)
    if correct_group:
        add_face_to_group(req_group_name)
    else:
        choose_again = input("Choose group again? ")
        if choose_again == "Yes" or choose_again == "Y" or choose_again == "T":
            print("")
            print("")
            add_face()

def add_face_to_group(req_group_name):
    req_person_id = 0
    people_in_group = CF.person.lists(req_group_name)
    for index in people_in_group:
        print(index["name"])
    req_name = input("Enter name of person to which face should be added to in " + req_group_name + " : ")
    for index in people_in_group:
        if index["name"] == req_name:
            req_person_id = index["personId"]
    add_face_to_person(req_group_name,req_person_id,req_name)
    add_face_again = input("Put another image for same person? : ")
    if add_face_again == "Yes" or add_face_again == "Y" or add_face_again == "T":
        add_face_to_person(req_group_name,req_person_id,req_name)
        add_face_again = input("Put another image for same person? : ")
        if add_face_again == "Yes" or add_face_again == "Y" or add_face_again == "T":
            add_face_to_person(req_group_name,req_person_id,req_name)
            add_face_again = input("Put another image for same person? : ")
            if add_face_again == "Yes" or add_face_again == "Y" or add_face_again == "T":
                add_face_to_person(req_group_name,req_person_id,req_name)
                add_face_again = input("Put another image for same person? : ")
                if add_face_again == "Yes" or add_face_again == "Y" or add_face_again == "T":
                    add_face_to_person(req_group_name,req_person_id,req_name)
                    add_face_again = input("Put another image for same person? : ")
                    if add_face_again == "Yes" or add_face_again == "Y" or add_face_again == "T":
                        add_face_to_person(req_group_name,req_person_id,req_name)


def add_face_to_person(req_group_name,req_person_id,req_name):
    img_link = input("Choose image link to insert : ")
    CF.person.add_face(img_link,req_group_name,req_person_id)
    print("Face added to person " + req_name)
    print("")
    speak_text = "HELLO! FACE HAS BEEN ADDED TO PERSON " + req_name
    language = 'en'
    myobj = gTTS(text=speak_text, lang=language, slow=False)
    myobj.save("face_aaded.mp3")
    os.system("mpg321 face_aaded.mp3  > /dev/null 2>&1")

def add_group():
    speak_text = "HELLO! PLEASE ADD GROUP"
    language = 'en'
    myobj = gTTS(text=speak_text, lang=language, slow=False)
    myobj.save("add_grp.mp3")
    os.system("mpg321 add_grp.mp3 > /dev/null 2>&1")
    print("ADD GROUP\n\n")
    req_group_name = input("Enter name : ")
    confirm_entry_grp = input("Are you sure you want to enter new person group with name " + req_group_name + "?\n")
    if confirm_entry_grp == "Yes" or confirm_entry_grp == "y" or confirm_entry_grp == "Y" or confirm_entry_grp == "T":
        speak_text = "HELLO! THE GROUP HAS NOT BEEN ADDED"
        print(speak_text)
        CF.person_group.create(person_group_id = req_group_name, name=req_group_name, user_data="Data and images for the person with name " + req_group_name)
    else:
        print("Group has NOT been entered")
        speak_text = "HELLO! THE GROUP HAS NOT BEEN ADDED"
    language = 'en'
    myobj = gTTS(text=speak_text, lang=language, slow=False)
    myobj.save("added_grp.mp3")
    os.system("mpg321 added_grp.mp3 > /dev/null 2>&1")

'''
img_link = input("Choose image link to verify : ")
face_to_verify = CF.face.detect(img_link)
req_face_id = face_to_verify[0]["faceId"]
#print(req_face_id)
people_in_group = CF.person.lists('group_aakash')
for index in people_in_group:
    print(index["personId"])
    rate_confidence = CF.face.verify(face_id=req_face_id, person_group_id='group_aakash',person_id= index["personId"])
    if(rate_confidence["isIdentical"] == True):
        print("Person verified is " + index["name"])
        print(rate_confidence["confidence"]*100)
        '''


continue_UI = True
while(continue_UI):
    os.system("clear")
    speak_text = "HELLO! WELCOME TO FACE RECOGNITION UI"
    language = 'en'
    myobj = gTTS(text=speak_text, lang=language, slow=False)
    myobj.save("welcome.mp3")
    os.system("mpg321 welcome.mp3 > /dev/null 2>&1")
    print("\n" + speak_text)
    print("Choose one of the options")
    print("")
    print("1.Add person to a person group")
    print("2.Add face to person")
    print("3.Train person group")
    print("4.Identify person in image")
    print("5.Add group")
    print("6.Exit")
    print("")
    num_sel = int(input("Choose option no. : "))
    if num_sel==1:
        add_person()
        time.sleep(3)
    elif num_sel==2:
        add_face()
        time.sleep(3)
    elif num_sel==3:
        train_group()
        time.sleep(3)
    elif num_sel ==4:
        verify_face()
        time.sleep(3)
    elif num_sel ==5:
        add_group()
        time.sleep(3)
    elif num_sel==6:
        print("EXITING UI")
        time.sleep(1)
        continue_UI=False
        speak_text = "LEAVING UI! THANK YOU"
        language = 'en'
        myobj = gTTS(text=speak_text, lang=language, slow=False)
        myobj.save("exit.mp3")
        os.system("mpg321 exit.mp3 > /dev/null 2>&1")
    else:
        print("Re-enter option\n\n")

#verify_face()

'''
people_in_group = CF.person.lists('group_aakash')
#print(people_in_group)
for index in people_in_group:
    #print(index["name"])
    rate_confidence = CF.face.verify(face_id = '229e3ecc-f4c8-4708-8308-de59426b7422',person_group_id="group_aakash",person_id= index["personId"])
    if(rate_confidence["isIdentical"] == True):
        print(rate_confidence["confidence"])
        print(index["name"])
'''
'''
people_in_group = CF.person.lists('group_aakash')
for index in people_in_group:
    print(index["name"])
'''
#print(CF.person.lists('group_aakash'))
#print(CF.person_group.get('group_aakash'))
#train_group()
#add_person()

'''
faces = {}

faces = CF.face.detect(img1_url)
faces.append(CF.face.detect(img2_url)[0])
#print(faces)
print(faces[0])
print(faces[1])
'''