import socket
import os
from blockchain import Blockchain
from emissionsDatabase import Database
import time
import getpass
import threading
import hashlib
import sys
import json
import socket
from _thread import *
from datetime import datetime
from colorama import Fore, Back
from colorama import init as colorama_init

# Init and set options ""
colorama_init(autoreset=True)

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
password = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

if len(sys.argv) != 3:
    print(f"{Fore.RED}INVALID INPUT: elevatedPeer.py [ip address] [port number]")
    sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])

lock = threading.Lock()

def writeData(addr, data):
    lock.acquire()
    Blockchain.execute(data)
    lock.release()
    print(addr, f"{Fore.GREEN}Data successfully added to the blockchain")

def recieveNewData(user_connection, addr, user, userPass):
    #print("\n------Start of recieveNewData function------\n")

    correct_info = False
    while correct_info == False:
        received = user_connection.recv(BUFFER_SIZE).decode()
        rawData = received.split(SEPARATOR)
      
        try:
            make = rawData[0]
            model = rawData[1]
            year = rawData[2]
            carID = rawData[3]
            v, emissionRate = Database.search(make, model, year, addr)
            correct_info = True   
        except Exception as e:
            #print(addr, "Error recieving file info: ", e, ", Sending dataNAK")
            user_connection.send("dataNAK".encode())
            
    if not v:
        user_connection.send("carNotFound".encode())
        resp = user_connection.recv(BUFFER_SIZE).decode().split(SEPARATOR)
        if(resp[0] == "1"):
            Database.add2Database(make,model,year,int(resp[1]),addr)
    else:
        user_connection.send("dataACK".encode())
        
    emissionSinceLast = -1
    data = make+SEPARATOR+model+SEPARATOR+year+SEPARATOR+user+SEPARATOR+userPass+SEPARATOR+carID+SEPARATOR+str(emissionSinceLast)

    #print(addr, "Data recieved, sending dataACK")
    writeData(addr, data.split(SEPARATOR))
    #print("\n------End of recieveNewData function------\n")

##### TODO #####
def recieveUpdatedData(user_connection, addr, user, userPass):
    #print("\n------Start of recieveUpdatedData function------\n")

    correct_info = False
    while correct_info == False:
        received = user_connection.recv(BUFFER_SIZE).decode()
        rawData = received.split(SEPARATOR)
        try:
            km = rawData[0]
            carID = rawData[1]
            userID = user
            with open("doc.json", "r") as doc:
                data = json.load(doc)
                for item in reversed(data):
                    if(item['data'] == "Genesis Block"):
                        user_connection.send('blockchainERR'.encode())
                        return
                    elif(item['data']['userID'] == userID and item['data']['carID'] == carID):
                        make = item['data']['make']
                        model = item['data']['model']
                        year = item['data']['year']
                        break
            v, emissionRate = Database.search(make, model, year, addr)
            correct_info = True
        except Exception as e:
            #print(addr, "Error recieving file info: ", e, ", Sending dataNAK")
            user_connection.send("dataNAK".encode())
        
    try:
        emissionSinceLast = int(km)*int(emissionRate)
    except Exception as e:
        print(addr, f"{Fore.RED}Invalid data detected.")
        emissionSinceLast = -1
    data = make+SEPARATOR+model+SEPARATOR+year+SEPARATOR+userID+SEPARATOR+userPass+SEPARATOR+carID+SEPARATOR+str(emissionSinceLast)

    #print(addr, "Data recieved, sending dataACK")
    user_connection.send("dataACK".encode())
    writeData(addr, data.split(SEPARATOR))
    #print("\n------End of recieveUpdatedData function------\n")

def sendData(user_connection, addr):
    #print("\n------Start of sendData function------\n")
    filename = "doc.json"
    filesize = int(os.path.getsize(filename))
    
    fileInfoSent = False
    while not fileInfoSent:
        info = filename+SEPARATOR+str(filesize)
        user_connection.send(info.encode())
        resp = user_connection.recv(BUFFER_SIZE).decode()
        if(resp == "dataACK"):
            fileInfoSent = True
            
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            user_connection.sendall(bytes_read)
    print(addr, f"{Fore.GREEN}File {filename} succesfully sent")
    #print("\n------End of sendData function------\n")

def verify(user_connection, addr):
    rawInput = user_connection.recv(BUFFER_SIZE)
    userInput = rawInput.decode().split(SEPARATOR)
    
    connectType = userInput[0]
    user = userInput[1]
    hashedPassword = userInput[2]
    
    if(connectType == "1"):
        with open("doc.json", "r") as doc:
            data = json.load(doc)
            for item in reversed(data):
                if(item['data'] == "Genesis Block"):
                    user_connection.send("3".encode()) # Existing user does not exist.
                    return False, "", ""
                elif(item['data']['userID'] == user):
                    if(item['data']['password'] == hashedPassword):
                        user_connection.send("1".encode()) # Correct password for existing user.
                        return True, user, hashedPassword
                    else:
                        user_connection.send("2".encode()) # Incorrect password for existing user.
                        return False, "", ""
    elif(connectType == "2"):
        with open("doc.json", "r") as doc:
            data = json.load(doc)
            for item in reversed(data):
                if(item['data'] == "Genesis Block"):
                    user_connection.send("0".encode()) # New user
                    return True, user, hashedPassword
                elif(item['data']['userID'] == user):
                    user_connection.send("4".encode()) # New username already exists.
                    return False, "", ""
    else:
        user_connection.send("5".encode()) # Unknown error
        return False, "", ""        

def client_thread(user_connection, addr):
    while True: 
        print("")
        print(addr, f"{Fore.YELLOW}Waiting for request.")
        inputFromUser = user_connection.recv(BUFFER_SIZE)
        if (inputFromUser.decode('utf-8') != "5"):
            print(addr, "User input:", inputFromUser.decode('utf-8'))
        if (inputFromUser.decode('utf-8') == "1a"):
            user_connection.send("dataACK".encode())
            print(addr, f"{Fore.MAGENTA}Verifying User Credentials.")
            v, user, userPass = verify(user_connection,addr)
            if(not v):
                print(addr, f"{Fore.MAGENTA}Authentication Failed. Ending thread.")
                user_connection.close()
                break
            print(addr, f"{Fore.MAGENTA}User %s Authenticated."%user)       
            recieveNewData(user_connection, addr, user, userPass)
        elif (inputFromUser.decode('utf-8') == "1b"):
            user_connection.send("dataACK".encode())
            print(addr, f"{Fore.MAGENTA}Verifying User Credentials.")
            v, user, userPass = verify(user_connection,addr)
            if(not v):
                print(addr, f"{Fore.MAGENTA}Authentication Failed. Ending thread.")
                user_connection.close()
                break
            print(addr, f"{Fore.MAGENTA}User %s Authenticated."%user)       
            recieveUpdatedData(user_connection, addr, user, userPass)
        elif (inputFromUser.decode('utf-8') == "2"):
            sendData(user_connection, addr)
        elif (inputFromUser.decode('utf-8') == "5") or (not inputFromUser):
            user_connection.sendall(str.encode('CONNECTION CLOSED'))
            print(addr, f"{Fore.MAGENTA}Client disconnected. Ending thread")
            user_connection.close()
            break
        else:
            print(addr, f"{Fore.MAGENTA}Invalid Option.")

def connectToPeers():
    print(f"{Fore.GREEN}Launching server with host: ", host, f"{Fore.GREEN}, port: ", port)
    try:
        server = socket.socket()
        server.bind((host, port))
        server.listen()
    except Exception as e:
        print(f"{Fore.RED}Could not open open server Error: ", e, f"{Fore.RED}, programme will now end.")
        exit()

    print(f"{Fore.LIGHTBLUE_EX}+"+f"{Fore.YELLOW}Server open.".center(78, '-')+f"{Fore.LIGHTBLUE_EX}+")
    while True:
        print(f"{Fore.BLUE}Waiting for new peer to connect ...\n")
        user, addr = server.accept()
        print(f"{Fore.BLUE}New user: ", addr, f"{Fore.BLUE}, Passing user to thread.\n")
        start_new_thread(client_thread, (user, addr))

def authenticate():
    print(f"{Fore.CYAN}\n\n\n\n***************************************************************************************************************")
    print(f"{Fore.CYAN}***************************************************************************************************************")
    print(f"{Fore.CYAN}***************************************************************************************************************")
    print(f"{Fore.CYAN}***************************************************************************************************************")
    name = '''
 .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |     ______   | || |      __      | || |  _______     | || |              | || |  _________   | |
| |   .' ___  |  | || |     /  \     | || | |_   __ \    | || |              | || | |_   ___  |  | |
| |  / .'   \_|  | || |    / /\ \    | || |   | |__) |   | || |    ______    | || |   | |_  \_|  | |
| |  | |         | || |   / ____ \   | || |   |  __ /    | || |   |______|   | || |   |  _|  _   | |
| |  \ `.___.'\  | || | _/ /    \ \_ | || |  _| |  \ \_  | || |              | || |  _| |___/ |  | |
| |   `._____.'  | || ||____|  |____|| || | |____| |___| | || |              | || | |_________|  | |
| |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
'''
    name = name.center(100)
    print(f"{Fore.CYAN}%s"% name)
    print(f"{Fore.CYAN}***************************************************************************************************************")
    print(f"{Fore.CYAN}***************************************************************************************************************")
    print(f"{Fore.CYAN}***************************************************************************************************************")
    print(f"{Fore.CYAN}***************************************************************************************************************\n\n\n")
    c = '+'
    h = '-'
    v = '|'
    print(f"{Fore.LIGHTBLUE_EX}%s{Fore.LIGHTMAGENTA_EX}"% c+ f"{Fore.LIGHTMAGENTA_EX}Before proceeding please verify the Username and Password".center(78, h)+f"{Fore.LIGHTBLUE_EX}%s"% c)
    print (f"{Fore.LIGHTBLUE_EX}%s"% c + f"{Fore.LIGHTBLUE_EX}-" * 73 + f"{Fore.LIGHTBLUE_EX}%s"% c)
    usernameInput = getpass.getuser()
    print(f"{Fore.LIGHTMAGENTA_EX}Welcome: {usernameInput}")
    passwordInput = getpass.getpass(f"{Fore.LIGHTMAGENTA_EX}Password:")
    print(f"{Fore.LIGHTBLUE_EX}%s"% c+f"{Fore.LIGHTBLACK_EX}Authenticating...".center(78, h)+f"{Fore.LIGHTBLUE_EX}%s"% c)
    testing = (passwordInput).encode()
    passwordInput = str(hashlib.sha256(testing).hexdigest())
    if (password == passwordInput):
        print(f"{Fore.LIGHTBLUE_EX}%s"% c+f"{Fore.GREEN}Password correct.".center(78, h)+f"{Fore.LIGHTBLUE_EX}%s"% c)
        connectToPeers()
    else:
        print(f"{Fore.LIGHTBLUE_EX}%s"% c+f"{Fore.RED}Authentication failed. Program will now exit."f"+{Fore.LIGHTBLUE_EX}%s"% c)
    print(f"{Fore.CYAN}***************************************************************************************************************\n\n\n")

authenticate()

# filename = "doc.json"
# filesize = os.path.getsize(filename)
# print(filesize)
