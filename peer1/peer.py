import socket
import os
import getpass
import hashlib
import sys
import datetime
from datetime import timedelta
from datetime import datetime
import json
from colorama import Fore, Back
from colorama import init as colorama_init

# Init and set options ""
colorama_init(autoreset=True)

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
run_client = True

username = ""
password = ""
connectType = ""

if len(sys.argv) != 3:
    print(f"{Fore.RED}INVALID INPUT: peer.py [ip address] [port number]")
    sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])


def recieveData(client):
    #print("\n------Start of recieveData function------\n")
    dataReceived = False
    while not dataReceived:
        try:
            data = client.recv(BUFFER_SIZE).decode()
            #print("Data recieved: ", received)
            received = data.split(SEPARATOR)
            filename = received[0]
            filesize = int(received[1])
            print("filename: ", filename, ", filesize: ", filesize)
            client.send("dataACK".encode())
            dataReceived = True
        except Exception as e:
            client.send("dataNAK".encode())
    with open(filename, "wb") as f:
        while True:
            bytes_read = client.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            if sys.getsizeof(bytes_read) <= BUFFER_SIZE:
                break
    print(f"File {filename} received successfully")
    #print("\n------End of recieveData function------\n")

def calculateStats():
    userTotal = 0
    monthTotalGlobal = 0
    monthTotalUser = 0
    weekTotalGlobal = 0
    weekTotalUser = 0
    with open("doc.json", "r") as doc:
        data = json.load(doc)
        for item in reversed(data):
            user = False
            if(item['data'] == "Genesis Block"):
                break
            else:
                if(item['data']['emissionSinceLast'] == "-1"):
                    continue
                if(item['data']['userID'] == username):
                    user = True
                    userTotal += int(item['data']['emissionSinceLast'])
                now = datetime.now()
                old = datetime.strptime(item['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
                diff = now - old
                if(diff <= timedelta(weeks=1)):
                    weekTotalGlobal += int(item['data']['emissionSinceLast'])
                    if(user):
                        weekTotalUser += int(item['data']['emissionSinceLast'])
                if(diff <= timedelta(weeks=4)):
                    monthTotalGlobal += int(item['data']['emissionSinceLast'])
                    if(user):
                        monthTotalUser += int(item['data']['emissionSinceLast'])
                        
    print(f"{Fore.LIGHTGREEN_EX}GLOBAL STATS".center(77,'-')+f"{Fore.LIGHTMAGENTA_EX}")
    print(f"{Fore.LIGHTMAGENTA_EX}Monthly Total Emissions:".rjust(46,'-'), monthTotalGlobal, "(g Co2)".ljust(26,'-'))
    print(f"{Fore.LIGHTMAGENTA_EX}Weekly Total Emissions:".rjust(46,'-'), weekTotalGlobal, "(g Co2)".ljust(26,'-'))
    print(f"{Fore.LIGHTGREEN_EX}"+f"{Fore.LIGHTGREEN_EX}USER STATS".center(77,'-'))
    print(f"{Fore.LIGHTMAGENTA_EX}Lifetime Total Emissions:".rjust(46,'-'), userTotal, "(g Co2)".ljust(26,'-'))
    print(f"{Fore.LIGHTMAGENTA_EX}Monthly Total Emissions:".rjust(46,'-'), monthTotalUser, "(g Co2)".ljust(26,'-'))
    print(f"{Fore.LIGHTMAGENTA_EX}Weekly Total Emissions:".rjust(46,'-'), weekTotalUser, "(g Co2)".ljust(26,'-'))
    
    if(weekTotalGlobal == 0):
        weekPercent = 0
    else:
        weekPercent = (weekTotalUser/weekTotalGlobal)*100
        
    if(monthTotalGlobal == 0):
        monthPercent = 0
    else:
        monthPercent = (monthTotalUser/monthTotalGlobal)*100
    
    print(f"{Fore.LIGHTMAGENTA_EX}Weekly Contribution:".rjust(46,'-'), weekPercent, "%".ljust(26,'-'))
    print(f"{Fore.LIGHTMAGENTA_EX}Monthly Contribution:".rjust(46,'-'), monthPercent, "%".ljust(26,'-'))
    

def sendNewData(client):
    #print("\n------Start of sendNewData function------\n")
    
    make = str(input(f"{Fore.LIGHTCYAN_EX}Enter the make of your vehicle: "))
    model = str(input(f"{Fore.LIGHTCYAN_EX}Enter the model of your vehicle: "))
    year = str(input(f"{Fore.LIGHTCYAN_EX}Enter the year of your vehicle: "))
    carID = str(input(f"{Fore.LIGHTCYAN_EX}Enter a unique ID for this vehicle: "))
    
    data = make+SEPARATOR+model+SEPARATOR+year+SEPARATOR+carID

    dataACK = False
    while dataACK == False:
        print(f"{Fore.YELLOW}Sending Server data")
        client.send(data.encode())
        ACK = client.recv(BUFFER_SIZE).decode()
        if ACK == 'dataACK':
            dataACK = True
        elif ACK == 'carNotFound':
            print(f"{Fore.LIGHTCYAN_EX}Car not found in database.")
            print(f"{Fore.LIGHTCYAN_EX}1. Add car to database with emission rate.")
            print(f"{Fore.LIGHTCYAN_EX}2. Use max emission rate.")
            userInput = str(input("Invalid Input. Enter here: "))
            while(userInput != "1" and userInput != "2"):
                userInput = str(input("Invalid Input. Enter here: "))
            if userInput == "1":
                rawInput = str(input(f"{Fore.LIGHTCYAN_EX}Enter the emission rate (g/km) for this vehicle: "))
                while True:
                    try:
                        emissionRate = int(rawInput)
                        break
                    except Exception as e:
                        rawInput = str(input("Invalid Input. Enter here: "))
                data = userInput+SEPARATOR+str(emissionRate)
            else:
                data = userInput+SEPARATOR+" "
            client.send(data.encode())
            dataACK = True
                    
    print(f"{Fore.GREEN}Data successfully sent")
    #print("\n------End of sendNewData function------\n")
    
def sendUpdatedData(client):
    #print("\n------Start of sendUpdatedData function------\n")
    
    carID = str(input(f"{Fore.LIGHTCYAN_EX}Enter the carID of the car you wish to update: "))
    km = str(input(f"{Fore.LIGHTCYAN_EX}Enter how many kilometers you have traveled since your last entry: "))
    
    data = km+SEPARATOR+carID

    dataACK = False
    while dataACK == False:
        print(f"{Fore.YELLOW}Sending Server data")
        client.send(data.encode())
        ACK = client.recv(BUFFER_SIZE).decode()
        if ACK == 'dataACK':
            dataACK = True
        elif ACK == 'dataNAK':
            continue
        elif ACK == 'blockchainERR':
            print(f"{Fore.YELLOW}User", username, f"{Fore.RED}does not have a vehicle with ID %s in the Blockchain. Please use option (a) to enter data for a new vehicle."%carID)
            return
    
    print(f"{Fore.GREEN}Data successfully sent")
    #print("\n------End of sendUpdatedData function------\n")

def validateChain():
    filename="doc.json"
    openType = "r+"
    try:
        with open(filename, openType) as f:
            y = list(json.load(f))
        flag = False
        for i in range(1,len(y)):
            testHash = hashlib.sha256(str(int(y[i]["proof"])**2-int(y[i-1]["proof"])**2).encode()).hexdigest()
            if(y[i]["previousHash"] != y[i-1]["currentHash"] or testHash[:3]!="000"):
                print("Blockchain invalid at Block " + str(y[i]["index"]))
                flag = True
                break
        if (not flag):
            print(f"{Fore.GREEN}Blockchain Valid")
    except Exception as e:
        print(f"{Fore.RED}Could not validate blockchain\n Error: ",e)
    return
    
def recieveOrSendData():
    global connectType
    while True:
        print(f"{Fore.LIGHTYELLOW_EX}\nEnter the option number to send new data to a server or request update on blockchain".center(78,'-'))
        print(f"{Fore.LIGHTCYAN_EX}"+f"{Fore.LIGHTCYAN_EX}Option 1: Send Data".center(78,'-'))
        print(f"{Fore.LIGHTCYAN_EX}Option 2: Recieve Updated Blockchain".center(78,'-'))
        print(f"{Fore.LIGHTCYAN_EX}Option 3: Calculate Stats Using Local Blockchain".center(78,'-'))
        print(f"{Fore.LIGHTCYAN_EX}Option 4: Validate Current Blockchain".center(78,'-'))
        print(f"{Fore.LIGHTCYAN_EX}Option 5: Close Application".center(78,'-'))
        inputFromUser = str(input("Enter here: "))
        if (inputFromUser == "5"):
            print("The program will now exit.")
            break
        elif (inputFromUser == "4"):
            validateChain()
        elif (inputFromUser == "3"):
            calculateStats()
        elif (inputFromUser == "1" or inputFromUser == "2"):
            try:
                client = socket.socket()
                client.connect((host, port))
                print(f"{Fore.GREEN}Connected to server successfully.")
            except Exception as e:
                print(f"{Fore.RED}Error connecting to server: Please try again", e)
                continue
            if (inputFromUser == "1"):
                print(f"{Fore.LIGHTYELLOW_EX}\n")
                print(f"{Fore.LIGHTYELLOW_EX}Enter the option letter for the following sub-options".center(78,'-')+f"{Fore.LIGHTCYAN_EX}")
                print(f"{Fore.LIGHTCYAN_EX}Option a: Enter New Vehicle".center(78,'-'))
                print(f"{Fore.LIGHTCYAN_EX}Option b: Enter Kilometers Traveled Since Last Entry (in most recently added vehicle)".center(78,'-'))
                inputFromUser = str(input("Enter here: "))
                if(inputFromUser == "a"):
                    client.send(str.encode("1a"))
                    if client.recv(BUFFER_SIZE).decode() != "dataACK":
                        print(f"{Fore.RED}Unknown Error.")
                        return
                    if not authenticate(client):
                        client.close()
                        return
                    sendNewData(client)
                    connectType = "1"
                elif (inputFromUser == "b"):
                    client.send(str.encode("1b"))
                    if client.recv(BUFFER_SIZE).decode() != "dataACK":
                        print(f"{Fore.RED}Unknown Error.")
                        return
                    if not authenticate(client):
                        client.close()
                        return
                    sendUpdatedData(client)
                else:
                    print(f"{Fore.RED}Invalid Option.")
            elif (inputFromUser == "2"):
                client.send(str.encode("2"))
                recieveData(client)
            client.send(str.encode("5"))
            print(f"{Fore.RED}Connection is terminated.")
            client.close()
        else :
            print(f"{Fore.RED}Invalid Option.")
    return
    
def authenticate(client):
    global username, password, connectType
    data = connectType+SEPARATOR+username+SEPARATOR+password
    client.send(str.encode(data))
    rc = client.recv(BUFFER_SIZE).decode()
    
    c = '+'
    h = '-'
    v = '|'
    
    if(rc == "0"): # New User
        print(f"{Fore.LIGHTBLUE_EX}%s"% c+f"{Fore.GREEN}Authentication Successful.".center(78, h)+f"{Fore.LIGHTBLUE_EX}%s"% c)
        return True
    elif(rc == "1"): # Existing User, Correct Password
        print(f"{Fore.LIGHTBLUE_EX}%s"% c+f"{Fore.GREEN}Authentication Successful.".center(78, h)+f"{Fore.LIGHTBLUE_EX}%s"% c)
        return True
    elif(rc == "2"): # Existing User, Incorrect Password
        print(f"{Fore.LIGHTBLUE_EX}%s"% c+f"{Fore.RED}Authentication failed: Incorrect Password. Program will now exit."f"+{Fore.LIGHTBLUE_EX}%s"% c)
        return False
    elif(rc == "3"): # Existing User, User does not exist
        print(f"{Fore.LIGHTBLUE_EX}%s"% c+f"{Fore.RED}Authentication failed: User does not exist. Program will now exit."f"+{Fore.LIGHTBLUE_EX}%s"% c)
        return False
    elif(rc == "4"):
        print(f"{Fore.LIGHTBLUE_EX}%s"% c+f"{Fore.RED}Authentication failed: User already exists. Program will now exit."f"+{Fore.LIGHTBLUE_EX}%s"% c)
        return False
    else:
        print(f"{Fore.LIGHTBLUE_EX}%s"% c+f"{Fore.RED}Authentication failed: Unknown Error."f"+{Fore.LIGHTBLUE_EX}%s"% c)
        return False
    
def initialize():
    global username, password, connectType
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
    
    username = str(input(f"{Fore.LIGHTMAGENTA_EX}Enter username: "))
    print((f"{Fore.LIGHTYELLOW_EX}Do you have an exisiting account under username: %s?"% username).center(78,'-'))
    print(f"{Fore.LIGHTCYAN_EX}1. Yes".center(78,'-'))
    print(f"{Fore.LIGHTCYAN_EX}2. No".center(78,'-'))
    connectType = str(input("Enter here: "))
    while(connectType != "1" and connectType != "2"):
        connectType = str(input("Invalid Input. Enter here: "))
    passwordInput = getpass.getpass(f"{Fore.LIGHTMAGENTA_EX}Password:")
    
    password = str(hashlib.sha256(passwordInput.encode()).hexdigest())
    
    recieveOrSendData()
    
    print(f"{Fore.CYAN}***************************************************************************************************************\n\n\n")

initialize()
