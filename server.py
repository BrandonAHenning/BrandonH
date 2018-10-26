from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
from database import operatorsDB
from passlib.hash import bcrypt

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
        print("I made it to the PUT function")
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
            
    def registerUser(self, username):

        ##############This will be it own function. It will be in do_CREATE, do_GET or LoginUser? 
        ####You need to check just the username again and then password for Login. If/then if 
        db = operatorsDB()
        check = db.checkUsername(username)
        if check == None:
            return True #There is no Email with that, you can go on.
        else:
            return False #404, it exists. Send the warning message.
         ##############
        


        #Where this function will really start
        self.send_response(201)
        self.send_header('Access-Control-Allow-Origin', '*')
        length = self.headers["content-length"]
        body = self.rfile.read(int(length)).decode("utf-8")

        data = parse_qs(body) #Parse it as a dictonary

        username = data['username'][0]
        first_name = data['first_name'][0]
        last_name = data['last_name'][0]
        password  = data['password'][0]

        #Take the password, salt it, and assign it as new password
        bytes_password = password.encode()
        hash_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt() )

        #Initlize/Create Database and send put in the database
        db = operatorsDB()
        operators = db.registerUser(username, first_name, last_name, hash_password)

    def loginUser(self, username, password)

        #Take the password, salt it, and assign it as new password
        bytes_password = password.encode()
        hash_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt() )

        db = operatorsDB()
        check = db.loginUser(username, hash_password)

def run():
    listen = ('0.000', 8080)
    server = HTTPServer(listen, MyHandler)
    print('Listening...')
    server.serve_forever()
run()
