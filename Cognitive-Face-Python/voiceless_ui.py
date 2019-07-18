'''
This is a project by Aakash Kalantre and it is to use the Microsoft Face API and urls using imgbb.
There are 6 main options mentioned in main() and this is a simple CLI for the product.

It can be used in access control to sensitive documents or resources on entry into specific areas ina a factory
using a phtograph that needs to be taken and it's upload time can be verified and then allowed to access a resource.

Please contact using email through kalaaki@gmail.com or aakash.kalantre@student.manchester.ac.uk

There is are pre-requisites to understanding how this project works.
 - Use of REST APIs
 - Use of python3 and it's syntax
 - Understanding basics of API and how http is implemented in Python

In Images refer to IMG_0967.jpg to understand infrastructure of Person Group and Person
'''
#Using time to pause between switching choices in main
import time

#Library wuth files needed for connecting to the API
import cognitive_face as CF

#to import calls to linux operating system
import os

#Used in creating zingers in verify_face()
import random

#reading from a file which contains the key.
#Can save that file as protected with specified user access
key_dat = open('key_data.txt',mode='r')
KEY = key_dat.read()
CF.Key.set(KEY)

# Replace with your regional Base URL based on API
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)

#bpp;eam tp check if group should be checked again
choose_group_again = True

#Method to add a person to an existing person group
def add_person():
    print("\nADD PERSON\n\n")
    print("Choose which group you want to add the person to : ")
    #method in person_group to get a list of all the person_groups
    #present on the API model online
    groups = CF.person_group.lists()
    for index in groups:
       print(index["name"])
    print("")
    correct_group = False
    req_name = ""
    req_group_name = input("Enter name : ")
    #To check if the group entered by the user is correct
    for index in groups:
        if index["name"] == req_group_name:
            correct_group = True
            print(index["name"] + " has beeen chosen")
    #print(correct_group) to print if the group was correct or not
    if correct_group:
        req_name = input("Enter name of person to be added to " + req_group_name + " ")
        print(req_name)
        #method in person to create a new person
        CF.person.create(req_group_name,req_name)
        add_face()
    else:
        choose_again = input("Choose group again? ")
        if choose_again == "Yes" or choose_again == "Y" or choose_again == "T":
            print("")
            add_person()

#boolean to check if we should train a RecognitionModel
do_train = False

#method to train a group
def train_group():
    print("TRAIN GROUP\n\n")
    global do_train
    #method in person_group to get a list of all the person_groups
    #present on the API model online
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
    #print(correct_group)
    if correct_group:
        print("Training group " + group_to_train)
        #Method in pers_group to train a specific person group
        CF.person_group.train(group_to_train)
    else:
        choose_again = input("Choose group again? ")
        if choose_again == "Yes" or choose_again == "Y" or choose_again == "T":
            print("")
            print("")
            train_group()

#method to identify a person while printing out the similarity %s for every person
def verify_face():
    #zingers chosen at random for fun
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
    #print(random_num)
    isIdentified = False
    speak_text = "HELLO! TIME TO IDENTIFY A FACE"
    print(speak_text + "\n\n")
    #method in person_group to get a list of all the person_groups
    #present on the API model online
    groups = CF.person_group.lists()
    for index in groups:
       print(index["name"])
    print("")
    correct_group = False
    group_to_train = input("Choose group to identify from : ")
    for index in groups:
        if index["name"] == group_to_train:
            correct_group = True
            print(index["name"] + " has beeen chosen\n\n")
    if correct_group:
        print(correct_group)
        img_link = input("Choose image link to verify : ")
        #Method in person which returns a faceID and the faceRectangle
        face_to_verify = CF.face.detect(img_link)
        req_face_id = face_to_verify[0]["faceId"]
        people_in_group = CF.person.lists(group_to_train)
        for index in people_in_group:
            rate_confidence = CF.face.verify(face_id = req_face_id, person_group_id=group_to_train, person_id= index["personId"])
            print(index["name"] + " : "+str(100*rate_confidence["confidence"]) + "% similar")
            if(rate_confidence["isIdentical"] == True):
                isIdentified = True
                print("Person verified is " + index["name"])
                print(rate_confidence["confidence"]*100)
                speak_text = "THE PERSON IS " + index["name"] + "......" + yes_zingers[random_num]
                print(speak_text)
    else:
        choose_again = input("Choose group again? ")
        if choose_again == "Yes" or choose_again == "Y" or choose_again == "T":
            print("")
            print("")
            verify_face()
    #if the person has not been verified
    if isIdentified == False:
        print("Person not identifed")
        speak_text = no_zingers[random_num]
        print(speak_text)

#Method to add a face
def add_face():
    print("ADD FACE\n\n")
    print("Choose which group you want to add the face to : ")
    #method in person_group to get a list of all the person_groups
    #present on the API model online
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
    print("")
    if correct_group:
        add_face_to_group(req_group_name)
    else:
        choose_again = input("Choose group again? ")
        if choose_again == "Yes" or choose_again == "Y" or choose_again == "T":
            print("")
            print("")
            add_face()

#method to add a face to a particular group
def add_face_to_group(req_group_name):
    req_person_id = 0
    people_in_group = CF.person.lists(req_group_name)
    for index in people_in_group:
        print(index["name"])
    req_name = input("\nEnter name of person to which face should be added to in " + req_group_name + " : ")
    for index in people_in_group:
        if index["name"] == req_name:
            req_person_id = index["personId"]
    #Allows the user to enter multiple images at a time
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

#Method to add a person in a specified group
def add_face_to_person(req_group_name,req_person_id,req_name):
    img_link = input("Choose image link to insert : ")
    CF.person.add_face(img_link,req_group_name,req_person_id)
    print("Face added to person " + req_name)
    print("")

#Method to add a new person group
def add_group():
    print("ADD GROUP\n\n")
    req_group_name = input("Enter name : ")
    confirm_entry_grp = input("Are you sure you want to enter new person group with name " + req_group_name + "?\n")
    if confirm_entry_grp == "Yes" or confirm_entry_grp == "y" or confirm_entry_grp == "Y" or confirm_entry_grp == "T":
        CF.person_group.create(person_group_id = req_group_name, name=req_group_name, user_data="Data and images for the person with name " + req_group_name)
    else:
        print("Group has NOT been entered")


#A while loop running forever until option exit is chosen
continue_UI = True
while(continue_UI):
    os.system("clear")
    print("WELCOME TO FACE RECOGNITION UI")
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
        time.sleep(4)
    elif num_sel==2:
        add_face()
        time.sleep(5)
    elif num_sel==3:
        train_group()
        time.sleep(2)
    elif num_sel ==4:
        verify_face()
        time.sleep(5)
    elif num_sel ==5:
        add_group()
        time.sleep(3)
    elif num_sel==6:
        print("EXITING UI")
        time.sleep(1)
        continue_UI=False
    else:
        print("Re-enter option\n\n")

'''
Future checks
 - If existing person in a group can be copied or moved to another group
 - GUI for interactiveness
 - Voice inputs using Microsofts's API
'''