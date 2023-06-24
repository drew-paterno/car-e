
import sqlite3

MAX_EMISSION = 223

class Database:

    def search(make,model,year,addr):
        con = sqlite3.connect('edata.db')
        cur = con.cursor()
        cur.execute("SELECT Enedc, Eqltp FROM emissions WHERE make = '%s' and model = '%s' and year = '%s'" % (make, model, year))
        emissionData = cur.fetchone()
        if(emissionData == None):
            #print(addr, "WARNING: Input Vehicle does not exist in Database...Assigning max Emission Value")
            return False, MAX_EMISSION
        endec = emissionData[0]
        eqltp = emissionData[1]
        if(endec == ''):
            endec = 0
        if(eqltp == ''):
            eqltp = 0         
        if(endec >= eqltp):
            return True, endec
        else:
            return True, eqltp
    
    def add2Database(make,model,year,emission,addr):
        con = sqlite3.connect('edata.db')
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO Emissions (make,model,year,enedc,eqltp) VALUES ('%s', '%s', '%s', '%s', 0)" % (make,model,year,emission))
        except Exception as e:
            print(addr, "There was an error adding a vehicle to the database: %s"%e)
        con.commit()
        
