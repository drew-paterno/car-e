# CAR-e

## Setting up the Code

### Dependencies

This code was built using Python 3.10 on Windows 10. Working on MacOS/Linux has not been tested.
Python should be added to your PATH variable.
Run "python --version" in a command prompt to check if it is active
Run "pip --version" in a command prompt to check if it is active
Other modules imported are already installed in the native package. No need to explicitly install them.
Elevated Peer has a "doc.json" file. It contains the genesis block. If this information gets corrupted you will not be able
to move forward with the code. Please ensure that you make no modifications to any files before the intial run.

### **Setup**
Unzip the file into any folder on your local machine. 
The code has to be set up in 3 different directories which represent 3 different nodes on the network.
The elevated peer has the ability to manipulate the blockchain, peer1 and peer2 do not.
There will be files on the main directory that can be used to demonstrate the functionality.
If for any reason, elevatedPeer is unable to connected to blockchain.py please eliminate the pycache folder
in the same directory and restart the program again. The pycache folder helps make the connection between the two modules
and will not be present before you run "elevatedPeer.py" for the first time.

### **Passwords**
Enter the password enclosed in ' ' when prompted by the file in front of it.
elevatedPeer.py - 'admin'
peer1.py - 'peer1'
peer2.py - 'peer2'
These codes are not visible in the code. You will not be able to find them elsewhere. 
I did not add the functionality to change the password, to make sure if you have.


### **Typical execution format of each Script**
1. Ask for password. - Authentication
2. Ask if User needs to Send, Recieve or Exit. Calls functions accordingly
3. Peers can only recieve the blockchain, Elevated Peers can receive only the data.
4. Ask sender to locate the file for upload
5. Upload and Recieve between peers
6. Abort the connection
7. Go to Step 2.

----------------------------------------------------------------------------------------------------------------------


## Running the Program

[Tutorial/Demo](https://www.youtube.com/watch?v=P7s4JZPbnhE)

### **Elevated Peer**

To start the elevated peer from the command line, change into the elevated peer directory, and run the following command. Please note you can enter any valid IP/Port combination.

`python3 elevatedPeer.py localhost 50000`

You will then be prompted for the admin password, which is recorded above in the 'Passwords' section of the doc. After entering a valid password, you will then be able to see valid connections between the elevatedPeer and its peers.

**NOTE:** Each instance of the elevatedPeer represents one network. A future goal of this project is to expand the ability to have multiple elevatedPeers dictating over the same blockchain (and same network).

### **Peer**

To run a peer, change into either one of the peer directories on the command line, and run the following command. Please note that in order to connect to the elevated peer you set up from the previous step, whatever IP/Port combo you use must be the same for this command.

`python3 peer.py localhost 50000`

You will then be prompted to enter a username, and then be asked to either create an acccount, or enter existing credentials. Please note that passwords persist between sessions, and the only way to reset all entered data is to set the `doc.json` files to how they are in this commit. In the future, there should be more robust error handling.


----------------------------------------------------------------------------------------------------------------------

## Known Issues
1. If a client does not send any file to the server, the connection will remain active and never end.
	Solution: Introduce a timeout functionality and warn the client to send a file before elapsed time.
	Issues: If timeout does occur, the client is unable to figure out that the connection was interrupted and when it does eventually send a file, 
		it received an error that the connection is actively refused.
