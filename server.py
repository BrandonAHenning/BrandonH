from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
from database import operatorsDB
from passlib.hash import bcrypt
import bcrypt

class MyHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        print("The Option Methods has been activite...")
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Headers","Content-type")
        self.send_header("Access-Control-Allow-Methods","GET, POST, PUT, DELETE, OPTIONS")
        self.end_headers()
        print("it has send the header")
        return

    def do_GET(self):
        #GET 
        if self.path == "/operators":
            self.handleOperators_LIST()
        #RETRIVE
        elif self.path.startswith("/operators"):
            operators_path = self.path.split("/")
            operators_id = operators_path[2]
            self.handleOperators_RETRIVE(operators_id)
        #404
        else:
            self.handleNotFound()

    def do_POST(self):
        #POST
        if self.path == "/operators":
            self.handleOperators_CREATE()
        #SESSIONS
        elif self.path == "/sessions":
            self.loginUser()
        #REGISTER
        elif self.path == "/users":
            self.registerUser()
        #404
        else:
            self.handleNotFound()

    def do_PUT(self):
        #PUT
        if self.path.startswith("/operators"):
            operators_path = self.path.split("/")
            operators_id = operators_path[2]
            self.handleOperators_PUT(operators_id)
        #404
        else:
            self.handleNotFound()

    def do_DELETE(self):
        #DELETE
        if self.path.startswith("/operators"):
            operators_path = self.path.split("/")
            operators_id = operators_path[2]
            self.handleOperators_DELETE(operators_id)
        #404
        else:
            self.handleNotFound()

    def handleNotFound(self):
        self.send_response(404)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("404 Not Found.","utf-8"))


    def handleOperators_LIST(self):
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()


        #Initlize/Create Database
        db = operatorsDB()
        operators = db.getOperators()
        self.wfile.write(bytes(json.dumps(operators),"utf-8"))

        #Get the pictures from database
        

    def handleOperators_CREATE(self):
        self.send_response(201)
        self.send_header('Access-Control-Allow-Origin', '*')
        length = self.headers["content-length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        self.end_headers()

        data = parse_qs(body) #Parse it as a dictonary
        print("DEBUG: " + str(data))

        name = data['name'][0]
        country  = data['country'][0]
        side = data['side'][0]
        weapon = data['weapon'][0]
        age = data['age'][0]

        #Initlize/Create Database
        db = operatorsDB()
        print("The Ops is being Created")
        db.createOperators(name, country, side, weapon, age)

    def handleOperators_RETRIVE(self, operators_id):
        db = operatorsDB()
        op_check = db.retriveOperators(operators_id)

        if op_check is None:
            print("IT IS NONE for RETRIVE")
            self.handleNotFound()
        else:
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            print("IT PAST for RETRIVE opcheck")

            #Initlize/Create Database
            db = operatorsDB()
            operators = db.retriveOperators(operators_id)
            self.wfile.write(bytes(json.dumps(operators),"utf-8"))

    def handleOperators_DELETE(self, operators_id):
        print("DEBUG: It has reach the RETRIVE FUNCTION")
        db = operatorsDB()
        op_check = db.retriveOperators(operators_id)

        if op_check is None:
            print("IT IS NONE")
            self.handleNotFound()
        else:
            print("DEBUG: It about to SEND THE RESPONSE")
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("content-type", "application/x-www-form-urlencoded")
            self.end_headers()
            print("DEBUG: HEADER HAS BEEN SENT")

            #Initlize/Create Database
            db = operatorsDB()
            db.deleteOperators(operators_id)
            print(operators_id + "Operators ID has been deleted from the database")

    def handleOperators_PUT(self, operators_id):
        db = operatorsDB()
        op_check = db.retriveOperators(operators_id)

        if op_check is None:
            print("IT IS NONE for PUT")
            self.handleNotFound()
        else:
            self.send_response(201)
            self.send_header('Access-Control-Allow-Origin', '*')
            length = self.headers["content-length"]
            body = self.rfile.read(int(length)).decode("utf-8") 
            self.end_headers()

            data = parse_qs(body)
            print("PUT DEBUG: " + str(data))

            name = data['name'][0]
            country  = data['country'][0]
            side = data['side'][0]
            weapon = data['weapon'][0]
            age = data['age'][0]

            #Initlize/Create Database
            db = operatorsDB()
            print("The Ops is being modify")
            operators = db.modifyOperators(operators_id, name, country, side, weapon, age)
            
    def registerUser(self):
        length = self.headers["content-length"]
        body = self.rfile.read(int(length)).decode("utf-8")

        data = parse_qs(body) #Parse it as a dictonary
        db = operatorsDB()

        username = data['email'][0] #EMAIL =/= USERNAME, but I have to use it cause of database
        first_name = data['first_name'][0]
        last_name = data['last_name'][0]
        password  = data['password'][0]

        check = db.checkUsername(username)
        if check != None:
            self.handleNotFound()
            print("404 is beinng trigger because a user is already in database for register")
        else:
            self.send_response(201)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            #Take the password, salt it, and assign it as new password
            bytes_password = password.encode()
            hash_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt() )
            print("hasing the password", hash_password)

            #Initlize/Create Database and send put in the database
            db = operatorsDB()
            operators = db.registerUser(username, first_name, last_name, hash_password)
            print(username, " has been succesfully register")

    def loginUser(self):
        length = self.headers["content-length"]
        body = self.rfile.read(int(length)).decode("utf-8") 
        data = parse_qs(body) #Parse it as a dictonary
        username = data['email'][0]
        password = data['password'][0] 

        db = operatorsDB()
        check = db.checkUsername(username)

        print("check is: ", check)
        if check == None:
            self.handleNotFound()
            print("Username/Password Is Not Wrong 1")
        else:
            #Grab password from database, it is bytes
            check_password = check['hash_password']

            #Comapre the given password and hashpassword. They both are in bytes. Not UTF-8
            check = bcrypt.checkpw(password.encode(), check_password)

            if check == False:
                self.handleNotFound()
                print("Username/Password Is Not Wrong 2")
            else:
                self.send_response(201)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                print("You have successfully login for '1 sec' ")



def run():
    listen = ('0.000', 8080)
    server = HTTPServer(listen, MyHandler)
    print('Listening...')
    server.serve_forever()
run()
