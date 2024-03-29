from flask import Flask, render_template, request, redirect, session 
import csv
import os
import base64
from datetime import datetime
server = Flask(__name__)

room_files_path = str(os.getenv('ROOM_FILES_PATH'))
users_path = str(os.getenv('USERS_PATH'))
server.secret_key="chatApp@Chaya_Lipshitz"

def chechUserExist(username,password):
   with open(users_path, "r") as usersExist:
        users=csv.reader(usersExist)
        for user in users:
            if(user[0] == username and decode_password(user[1]) == password):
                return True 
        return False 

#encode password
def encode_password(user_pass):
    pass_bytes = user_pass.encode('ascii')
    base64_bytes = base64.b64encode(pass_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

#decode password
def decode_password(user_pass):
    base64_bytes = user_pass.encode('ascii')
    pass_bytes = base64.b64decode(base64_bytes)
    user_pass = pass_bytes.decode('ascii')
    return user_pass
@server.route("/", methods=['GET','POST'])
def index(): 
    return redirect('/register')

@server.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if(chechUserExist(username, password)):
            session['username'] = username
            return redirect('lobby')
        else:
            #return redirect('error/'+ static_folder) #"wrong usernaname or pass" + str(static_folder)       
            return "wrong usernaname or password"       
    return render_template('login.html')

@server.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if(chechUserExist(username, password)):
            return "username and pass already exist"
        else:
            encrypted_password = encode_password(password)
        #כתיבה לקובץ
            with open(users_path, 'w') as file:
                writer = csv.writer(file)
                writer.writerow([username, encrypted_password])
            return redirect('login')
    return render_template('register.html')

@server.route('/lobby', methods = ['POST','GET'])
def lobby():
   rooms = os.listdir('rooms/')
   if request.method == 'POST':
        new_room = request.form['new_room'] + '.txt'
        if (str(new_room)) in rooms:
            #print("exist in:" )
            return "exist"
        else:
            file = open(room_files_path + new_room, 'w+')
            file.close()
            rooms.append(new_room)
   all_rooms=[x[:-4] for x in rooms]
   return render_template("lobby.html", all_rooms = all_rooms) 

@server.route('/logout', methods = ['POST','GET'])
def logout():
    session.pop('username', None)
    return redirect('register')  

@server.route("/chat/<room>")
def chat(room):
    return render_template('chat.html', room=room)

@server.route('/api/chat/<room>', methods = ['GET','POST'])
def manage_chat(room):
    file_path=room_files_path + room +'.txt'
    user= session.get('username')
    if user==None:
        user="guest"
    if request.method == 'POST':
        user_mssage= request.form['msg']
        #message in format:  [2023-08-21 11:00:11] yuval: hello
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        full_message= '\n' + "[" + dt_string + "] " + user + ": " + user_mssage 
        with open(file_path, 'a+') as file:
            file.write(full_message)
            file.close()
    if os.path.getsize(file_path) == 0:
        content = str(user) + ", No messages yet"
    else:
        with open(file_path, 'r+') as f:
            content = f.read() 
            f.close()
    return content

@server.route("/api/chat/clear/<room>", methods = ['POST'])
def clear(room):    
    # username = session['username']
    # with open(f'{room_files_path}{room}.txt', 'r') as file:
    #     lines = file.readlines()
    #     print(lines)
    # lines = str(filter(lambda line: len(line)>=3 and line.split(' ')[2] != username, lines))
    # with open(f'{room_files_path}/{room}.txt', 'w') as file:
    #     file.writelines(lines)
    # # messages=getMessages(room)
    # return lines
    with open(f'{room_files_path}{room}.txt', 'w') as file:
        file.write("")
        
    
if __name__ == "__main__":
    server.run(host='0.0.0.0')