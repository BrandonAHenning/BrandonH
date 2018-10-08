import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class operatorsDB():
    #Works
    def __init__(self):
        print("Connecting to DB...")
        self.connection = sqlite3.connect("operators.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    #Works
    def __del__(self):
        print("Disconnecting from DB...")
        self.connection.close()

    #Works
    def getOperators(self):
        self.cursor.execute('SELECT * FROM operators')
        return self.cursor.fetchall()
    
    #Works
    def retriveOperators(self, operators_id):
        self.cursor.execute('SELECT * from operators WHERE id = ?', [operators_id])
        return self.cursor.fetchone()

    #Works
    def createOperators(self, name, country, gadget, weapon, age):
        self.cursor.execute("INSERT INTO operators (name, country, gadget, weapon, age) VALUES (?,?,?,?,?)", [name, country, gadget, weapon, age])
        self.connection.commit()






