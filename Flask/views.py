#Contains the routings and the view functions
<<<<<<< HEAD
from doctest import OutputChecker


=======
import re
from datetime import datetime
from sys import flags


from flask import Flask, render_template,flash
>>>>>>> 6677cb7c8687b8510af5e5a8a6484260c790aee7

from flask import Flask, render_template, request, redirect
from . import app

#database
import sqlite3 as sql

#Plot graph imports
import datetime as DT
import matplotlib.pyplot as plt

import cv2
from threading import *
import time

@app.route("/")
@app.route("/home/")
def home():
    # print("helllloooooo")
    return render_template("home.html")

#---------------------------------open focusing function
#*******the time they focus

focusedTime = 0
notfocusedTime = 0

@app.route("/focuz")
def focuz():
     
    face_cascade = cv2.CascadeClassifier('Flask/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    def focus():
        global isFocus
        isFocus = True
    
      
    def run():
        
        global isFocus,focusedTime,notfocusedTime,state
        state= True
        
        
            
        while state:
             
            startTimer=time.time()
            isFocus = False
    # Read the frame
            _, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                if len(faces)<2:
                    focus()
               
            
               # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
               
        # change state if has face
               
               
            if isFocus == False:
                print("You are not focusing")
                endTimer=time.time()
                notfocusedTime += (endTimer-startTimer) 
            else:
                print("You are okay")
                endTimer=time.time()
                focusedTime += (endTimer-startTimer)
            
         
            
            k = cv2.waitKey(1) & 0xff
            if k==27:
                break
    
    
    # showmsg()
    run()
    # print("You have focused :", str(int(focusedTime)),'s')
    # print("You have not focused :", str(int(notfocusedTime)),'s')  
    return "Get back to continue"

# @app.route("/showmsg")
# def showmsg():
    
#     flash("You have started FOCUZ","info")
#     return render_template("home.html")
    
@app.route("/stop")
def stop():
    
    global state,focusedTime,notfocusedTime
    state=False
    flash("You have stopped FOCUZ","info")
    flash("You have focused : "+ str(int(focusedTime))+'s')
    flash("You have not focused : "+ str(int(notfocusedTime))+'s')
    focusedTime=0
    notfocusedTime=0  
    return render_template("home.html")


@app.route("/luckydraw")
def luckydraw():
    return render_template("luckydraw.html")

@app.route("/setting")
def setting():
    return render_template("setting.html")

#Get block website info
#Hostpath
hostsPath = r"C:\Windows\System32\drivers\etc\hosts"
reroute = "127.0.0.1"


@app.route('/setting', methods = ["POST", "GET"])
def add_website():
    if request.method == "POST":
        new_website = request.form['website']

        add_blocked_website("queena1234@gmail.com",new_website)

        with open(hostsPath, 'r+') as file:
            content = file.read()
            for site in get_blocked_website_list("queena1234@gmail.com"):
                if site in content:
                    pass
                else:
                    file.write(reroute + " " + site + "\n")
            return redirect("/setting")
    else:
        website = get_blocked_website_list("queena1234@gmail.com")
        return render_template("setting.html", website = website)



    
            
            
    


#-------------------- DATABASE FUNCTIONS -----------------------
#USER INFO
def create_users_info():
    #Create database file/connect to it
    conn = sql.connect("Flask/static/Databases/database.db")

    #Create table
    #username + email (unique) + password + icon_photo
    conn.execute("""CREATE TABLE user (username TEXT, email TEXT PRIMARY KEY, password TEXT, icon_photo TEXT)""")
    cur = conn.cursor()
    print("table created")
    
    #DEMO user
    insert_query = """INSERT INTO user (username, email, password, icon_photo)
                                       VALUES (?,?,?,?)"""
    cur.execute(insert_query, ("imcoolthanks", "queena1234@gmail.com", "1234", "/static/Assets/user_icons/default.jpg"))
    print("user added")

    conn.commit()

    conn.close()

def login(email, password):
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    try:
        query = 'SELECT password FROM user WHERE email = ?'
        cur.execute(query, (email,))
    except:
        print("Invalid Email Address.")

    true_password = cur.fetchall()[0][0]

    if password == true_password:
        print("Logged in")
    else:
        print("Wrong Password")

    conn.close()

def sign_up(username, email, password):
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()
    
    insert_query = """INSERT INTO user (username, email, password, icon_photo)
                                       VALUES (?,?,?,?)"""
    cur.execute(insert_query, (username, email, password, "/static/Assets/user_icons/default.jpg"))
    print("user added")

    conn.commit()
    conn.close()


#BLOCKED WEBSITE
def create_blocked_website():
    #blocked_website(email,seq_no,url)
    #select url from blocked_website where email = ?;

    #Create database file/connect to it
    conn = sql.connect("Flask/static/Databases/database.db")

    #Create table
    #email,seq_no,url
    conn.execute("""CREATE TABLE blocked_website (email TEXT, url TEXT )""")
    print("table created")

    #DEMO 
    cur = conn.cursor()
    insert_query = """INSERT INTO blocked_website (email, url)
                                       VALUES (?,?)"""
    cur.execute(insert_query, ("queena1234@gmail.com", "https://www.youtube.com/"))
    print("user added")

    conn.commit()

    conn.close()

    print("Loading completed")
#return list of all blocked website
def get_blocked_website_list(email):
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    try:
        query = 'SELECT url FROM blocked_website WHERE email = ?'
        cur.execute(query, (email,))
    except:
        print("Invalid Email Address.")

    rows = cur.fetchall()
    url_list = []

    for i in rows:
        url_list.append(i[0])

    conn.close()

    return url_list

def add_blocked_website(email, url):
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    insert_query = """INSERT INTO blocked_website (email, url)
                                       VALUES (?,?)"""
    cur.execute(insert_query, (email, url))
    conn.commit()

    conn.close()

def remove_blocked_website(email, url):
    
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    delete_query = "DELETE FROM blocked_website WHERE email = ? and url = ?"
    cur.execute(delete_query, (email, url))
    conn.commit()

    conn.close()

#FOCUS TIME
def create_focus_time():
    #focus_time(email,days_ago,hours)
    #select url from blocked_website where email = ?;

    #Create database file/connect to it
    conn = sql.connect("Flask/static/Databases/database.db")

    #Create table
    #email, days_ago, hours
    conn.execute("""CREATE TABLE focus_time (email TEXT, days_ago INTEGER, hours INTEGER )""")
    print("table created")

    #DEMO
    cur = conn.cursor()
    insert_query = """INSERT INTO focus_time (email, days_ago, hours)
                                       VALUES (?,?,?)"""
    for i in range(7):                                   
        cur.execute(insert_query, ("queena1234@gmail.com", i, i))
    print("user added")

    conn.commit()
    conn.close()
#Update Focus time at end of day !!!CHANGE
def insert_focus_time(email, today_hours):
    #Create database file/connect to it
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    #find the one thats a week ago and update that value
    query = "UPDATE focus_time SET hours = "+str(today_hours)+" where email = ? and days_ago = 0"
    cur.execute(query, (email, ))

    conn.commit()
    conn.close()

#execute when 12am
def update_all_focus_time():
    #Create database file/connect to it
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    #all +1
    query = "UPDATE focus_time SET days_ago = days_ago + 1"
    cur.execute(query)

    query = "update focus_time set days_ago = REPLACE(days_ago, 7, 0)"
    cur.execute(query)

    #find the one thats a week ago and update that value
    query = "UPDATE focus_time SET hours = 0 where days_ago = 0"
    cur.execute(query)

    conn.commit()
    conn.close()

#graph
def graph(email):    
    today = DT.date.today()

    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    #get username
    query = 'SELECT username FROM user WHERE email = ?'
    cur.execute(query, (email,))
    username = cur.fetchall()[0][0]

    #get focus_time
    query = 'SELECT hours FROM focus_time WHERE email = ?'
    cur.execute(query, (email,))
    rows = cur.fetchall()
    focus_time = []

    for i in rows:
        focus_time.append(i[0])

    conn.close()

    #Get x-axis data
    days = []
    for i in range(7):
        d = today - DT.timedelta(days=(6-i))
        days.append(d.strftime("%m/%d"))

    #Plot average line
    average = sum(focus_time) / len(focus_time)

    #Plot the 2 graphs
    plt.plot(days, focus_time)
    plt.axhline(y=average, color='r', linestyle='--')

    #Graph settings
    plt.axis([0, 6, 0, max(focus_time)+1]) #set axis
    plt.xlabel('Date')
    plt.ylabel('Number of hours focusing')
    plt.title('Past 7 Days Stats')

    #Save Graph
    plt.savefig('Flask/static/Assets/graphs/'+username+'.png')


#USED FOR DEBUGGING
def list_all():
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    tables = ["user", "blocked_website", "focus_time"]

    for t in tables:
        print(t+":")
        cur.execute("SELECT * FROM "+t)

        rows = cur.fetchall()

        for row in rows:
            print(row)

        print("\n")

#Delete and restart with basic DEMOs
def reset_database():
    create_blocked_website()
    create_focus_time()
    create_users_info()
    list_all()




    