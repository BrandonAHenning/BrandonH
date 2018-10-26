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

    def deleteOperators(self, operators_id):
        self.cursor.execute('DELETE from operators WHERE id = ?', [operators_id])
        return self.connection.commit()

    #Works
    def createOperators(self, name, country, side, weapon, age):
        self.cursor.execute("INSERT INTO operators (name, country, side, weapon, age) VALUES (?,?,?,?,?)", [name, country, side, weapon, age])
        return self.connection.commit()

    def modifyOperators(self, operators_id, name, country, side, weapon, age):
        self.cursor.execute("UPDATE operators SET name = ?, country = ?, side = ?, weapon = ?, age = ? WHERE id = ?", [name, country, side, weapon, age, operators_id])
        return self.connection.commit()

    def checkUsername(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username= ?", [username])
        return self.cursor.fetchone()

    def registerUser(self, username, first_name, last_name, hash_password):
        self.cursor.execute("INSERT INTO users (username, first_name, last_name, hash_password) VALUES (?,?,?,?)", [username, first_name, last_name, hash_password))
        return self.conncetion.commit()

    def loginUser(self, username, hash_password):
        self.cursor.execute("SELECT * FROM users WHERE username= ? AND hash_password = ?", [username, hash_password])
        return self.cursor.fetchone()


