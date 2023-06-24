----------------------------------------------------------------------------------------------------------------------

Hello there!

-------------------Dependencies-------------------
This code was built using Python 3.10 on Windows 10. Working on MacOS/Linux has not been tested.
Python should be added to your PATH variable.
Run "python --version" in a command prompt to check if it is active
Run "pip --version" in a command prompt to check if it is active
Other modules imported are already installed in the native package. No need to explicitly install them.
Elevated Peer has a "doc.json" file. It contains the genesis block. If this information gets corrupted you will not be able
to move forward with the code. Please ensure that you make no modifications to any files before the intial run.
-------------------Dependencies-------------------


----------------------------------------------------------------------------------------------------------------------


-------------------Setting up the Code-------------------
Unzip the file into any folder on your local machine. 
The code has to be set up in 3 different directories which represent 3 different nodes on the network.
The elevated peer has the ability to manipulate the blockchain, peer1 and peer2 do not.
There will be files on the main directory that can be used to demonstrate the functionality.
If for any reason, elevatedPeer is unable to connected to blockchain.py please eliminate the pycache folder
in the same directory and restart the program again. The pycache folder helps make the connection between the two modules
and will not be present before you run "elevatedPeer.py" for the first time.
-------------------Setting up the Code-------------------


----------------------------------------------------------------------------------------------------------------------


-------------------Passwords-------------------
Enter the password enclosed in ' ' when prompted by the file in front of it.
elevatedPeer.py - 'admin'
peer1.py - 'peer1'
peer2.py - 'peer2'
These codes are not visible in the code. You will not be able to find them elsewhere. 
I did not add the functionality to change the password, to make sure if you have.
-------------------Passwords-------------------


----------------------------------------------------------------------------------------------------------------------


-------------------Typical execution format of each Script-------------------
1. Ask for password. - Authentication
2. Ask if User needs to Send, Recieve or Exit. Calls functions accordingly
3. Peers can only recieve the blockchain, Elevated Peers can receive only the data.
4. Ask sender to locate the file for upload
5. Upload and Recieve between peers
6. Abort the connection
7. Go to Step 2.
-------------------Typical execution format of each Script-------------------


----------------------------------------------------------------------------------------------------------------------


-------------------Running the Program-------------------
To run this code on your laptop open the Command Prompt in the elevatedPeer and peer1 directories.
"--elevatedPeer" signifies that this command is run on the elevatedPeer Command Prompt.
"--peer1" signifies that this command is run on the peer1 Command Prompt.
exact codes are enclosed within " " and and extra instruction within ().
Any instruction is to help you type the correct command and not to written onto the console.

"python elevatedPeer.py" --elevatedPeer
"admin" (On the prompt enter the password) --elevatedPeer
(The password will not be visible to you as you type it.) --elevatedPeer
"2" (To recieve the data) --elevatedPeer
(Press Enter if asked to continue recieving and open the next port for the new client) --elevatedPeer
(The script will now broadcast an IP Address and Port Number that a peer can connect to) --elevatedPeer
(If a client connects, program will ask if you would like to proceed with opening new ports) -- elevatedPeer
(IF YOU FORGET TO PRESS ENTER THE PROGRAM WILL NOT PROCEED FURTHER) --elevatedPeer

"python peer1.py" --peer1
"peer1" (On the prompt enter the password) --peer1
"1" (To send the data) --peer1
"127.0.2.2" (Enter the IP Address - This should be visible on the command prompt of elevatedPeer) --peer1
"5000" (Enter the port number as displayed on the elevatedPeer command prompt) --peer1

Connection has been made at this point.

(Enter the full address of the file you have to transfer) --peer1
(for me the address was C:\Users\apnat\Desktop\CN\sampleData.txt) 
(You should be able to transfer any file, make sure the file has text data before uploading)

(File has been recieved and added to the blockchain) --elevatedPeer

"3" (to exit) --elevatedPeer
"3" (to exit) --peer1

You can now go and open doc.json in the elevatedPeer directory to see that the data has been succesfully added to the blockchain file.
Originally I planned on using a json format for data but due to various limitations as detailed in the report this could be implemented.
You can explore multiple functionalities of the code using different text files to transfer data in between.
The implementation should be able to transfer all types of files but garbage data might be written for files which have no text.

Similar functionality can also be demonstrated between peer1 and peer2
Follow the instructions on the command prompt and you should be able to follow through without any complications
-------------------Running the Program-------------------


----------------------------------------------------------------------------------------------------------------------


-------------------Issues-------------------
1. If a client does not send any file to the server, the connection will remain active and never end.
	Solution: Introduce a timeout functionality and warn the client to send a file before elapsed time.
	Issues: If timeout does occur, the client is unable to figure out that the connection was interrupted and when it does eventually send a file, 
		it received an error that the connection is actively refused.
-------------------Issues-------------------

----------------------------------------------------------------------------------------------------------------------