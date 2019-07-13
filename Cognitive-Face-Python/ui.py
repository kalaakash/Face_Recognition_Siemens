import pandas as pd
import time
import cognitive_face as CF

# Replace with a valid subscription key (keeping the quotes in place).

key_data=pd.read_csv("key_data.txt", delim_whitespace=True, skipinitialspace=True)
KEY = key_data.columns[0]
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
    print("ADD PERSON \n\n")
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
            correct_group = False
            print("No such group found")
    print(correct_group)
    if correct_group:
        req_name = input("Enter name of person to be added to " + req_group_name + " ")
        print(req_name)
        CF.person.create(req_group_name,req_name)
        add_face()
    else:
        choose_again = input("Choose group again? ")
        if choose_again == "Yes" or choose_again == "Y" or choose_again == "T":
            print("")
            print("")
            add_person()
        
do_train = False
def train_group():
    print("TRAIN GROUP \n\n")
    global do_train
    groups = CF.person_group.lists()
    for index in groups:
       print(index["name"])
    print("")
    correct_group = False
    group_to_train = input("Choose group to train : ")
    for index in groups:
        if index["name"] == group_to_train:
            correct_group = True
            print(index["name"] + " has beeen chosen")
        else:
            correct_group = False
            print("No such group found")
    print(correct_group)
    if correct_group:
        print("Training group " + group_to_train)
        CF.person_group.train(group_to_train)
    else:
        choose_again = input("Choose group again? ")
        if choose_again == "Yes" or choose_again == "Y" or choose_again == "T":
            print("")
            print("")
            train_group()
    
def verify_face():
    print("VERIFY PERSON \n\n") 
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
        else:
            correct_group = False
            print("No such group found")
    if correct_group:
        print(correct_group)
        img_link = input("Choose image link to verify : ")
        face_to_verify = CF.face.detect(img_link)
        req_face_id = face_to_verify[0]["faceId"]
        #print(req_face_id)
        people_in_group = CF.person.lists(group_to_train)
        for index in people_in_group:
            rate_confidence = CF.face.verify(face_id = req_face_id, person_group_id=group_to_train, person_id= index["personId"])
            print(rate_confidence["confidence"])
            if(rate_confidence["isIdentical"] == True):
                print("Person verified is " + index["name"])
                print(rate_confidence["confidence"]*100)
    else:
        choose_again = input("Choose group again? ")
        if choose_again == "Yes" or choose_again == "Y" or choose_again == "T":
            print("")
            print("")
            verify_face()

def add_face():
    print("ADD FACE \n\n")
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
            print(index["name"] + " has beeen chosen")
        else:
            correct_group = False
            print("No such group found")
    print(correct_group)
    if correct_group:
        req_person_id = 0
        people_in_group = CF.person.lists(req_group_name)
        for index in people_in_group:
            print(index["name"])
        req_name = input("Enter name of person to which face should be added to in " + req_group_name + " : ")
        for index in people_in_group:
            if index["name"] == req_name:
                req_person_id = index["personId"]
        img_link = input("Choose image link to verify : ")
        CF.person.add_face(img_link,req_group_name,req_person_id)
        print("Face added to person " + req_name)
        print("")
    else:
        choose_again = input("Choose group again? ")
        if choose_again == "Yes" or choose_again == "Y" or choose_again == "T":
            print("")
            print("")
            add_face()

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
    print("\nWELCOME TO FACE RECOGNITION UI")
    print("Choose one of the options")
    print("")
    print("1.Add person to a person group")
    print("2.Add face to person")
    print("3.Train person group")
    print("4.Identify person in image")
    print("5.Exit")
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
    elif num_sel==5:
        print("EXITING UI")
        time.sleep(1)
        continue_UI=False
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