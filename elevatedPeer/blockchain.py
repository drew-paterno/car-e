import datetime
import hashlib
import json
import os

class Blockchain:
    def __init__(self):
        self.chain = list()
        
    def createBlock(self, proof, data):
        block = { 'index': self.getLastIndex(),
                    'timestamp': str(datetime.datetime.now()),
                    'proof': self.proofOfWork(proof),
                    'data': {
                        'make': data[0],
                        'model': data[1],
                        'year': data[2],
                        'userID': data[3],
                        'password': data[4],
                        'carID': data[5],
                        'emissionSinceLast': data[6]
                    },
                    'currentHash': self.newHash(data),
                    'previousHash': self.getLastHash() }
        self.chain.append(block)
        self.writeToFile()

    def proofOfWork(self, previousProof):
        newProof = 1
        checkProof = False
        while checkProof is False:
            hashOperation = hashlib.sha256(str(newProof**2 - previousProof**2).encode()).hexdigest()
            if hashOperation[:3] == '000':
                checkProof = True
            else:
                newProof += 1
        return newProof

    def newHash(self, data):
        encodedBlock = (str(self.getLastHash()) + str(data)).encode()
        return hashlib.sha256(encodedBlock).hexdigest()
        
    def writeToFile(self):
        filename="doc.json"
        openType = "r+"
        with open(filename, openType) as f:
            y = list(json.load(f))
            y.append(self.chain[-1])
        f = open(filename,"w")
        json.dump(y, f, indent = 4)
        f.close()

    def getLastIndex(self):
        filename = "doc.json"
        file = open(filename, "r")
        f = str(file.readlines())
        start = f.rindex("index") + 8
        end = start+1
        while (f[end] != ","):
            end = end + 1
        return int(f[start:end])+1

    def getLastProof(self):
        filename = "doc.json"
        file = open(filename, "r")
        f = str(file.readlines())
        start = f.rindex("proof") + 8
        end = start+1
        while (f[end] != ","):
            end = end + 1
        return int(f[start:end])

    def getLastHash(self):
        filename = "doc.json"
        file = open(filename, "r")
        f = str(file.readlines())
        start = f.rindex("currentHash") + 15
        end = start+1
        while (f[end] != ","):
            end = end + 1
        return f[start:end-1]

    def execute(data=""):
        blockchain = Blockchain()
        blockchain.createBlock(proof = blockchain.getLastProof(), data=data)
