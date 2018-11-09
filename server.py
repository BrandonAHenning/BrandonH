from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
from database import operatorsDB
from passlib.hash import bcrypt
import bcrypt
from session_store import SessionStore
from http import cookies

#GLOBAL VAR
gSessionStore = SessionStore() #inital {}

#CLASS
class MyHandler(BaseHTTPRequestHandler):

    def load_cookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
            print("COOKIE IS FOUND")
        else:
            self.cookie = cookies.SimpleCookie()
            print("NO COOKIE FOUND")

    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString() )

    def loadSession(self):
        #Goal: assign self.session according to session Id
        self.load_cookie() #try to load it
        print("Cookie is: ", self.cookie)
        if "session_Id" in self.cookie:
            session_Id = self.cookie["session_Id"].value
            self.session = gSessionStore.getSession(session_Id)
            if self.session == None:
                print("self.sesson == None")
                #Client Has no session ID that match
                session_Id = gSessionStore.createSession()
                self.session = gSessionStore.getSession(session_Id)
                self.cookie["session_Id"] = session_Id #IS SELF.SESSION THE RIGHT ONE?
        else:
            #Client Has no session Id yet
            session_Id = gSessionStore.createSession()
            print("Create ID, your id is now: ", session_Id)
            self.session = gSessionStore.getSession(session_Id)
            print("No session id found in Cookie. Cookie SHOULD have self.session now = ", self.session)
            self.cookie["session_Id"] = session_Id

        print("\nSESSIONS ID: ", self.session)
        print("Group of SESSIONS: ",gSessionStore.sessions)
        print("-----------------------------------------------------")


    def do_OPTIONS(self):
        self.loadSession()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Headers","Content-type")
        self.send_header("Access-Control-Allow-Methods","GET, POST, PUT, DELETE, OPTIONS")
        self.end_headers()
        print("it has send the header")
        return

    def do_GET(self):
        self.loadSession()
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
        self.loadSession()
        #POST
        if self.path == "/operators":
            self.handleOperators_CREATE()
        #REGISTER
        elif self.path == "/users":
            self.registerUser()
        #SESSIONS
        elif self.path == "/sessions":
            self.loginUser()
        #404
        else:
            self.handleNotFound()

    def do_PUT(self):
        self.loadSession()
        #PUT
        if self.path.startswith("/operators"):
            operators_path = self.path.split("/")
            operators_id = operators_path[2]
            self.handleOperators_PUT(operators_id)
        #404
        else:
            self.handleNotFound()

    def do_DELETE(self):
        self.loadSession()
        #DELETE
        if self.path.startswith("/operators"):
            operators_path = self.path.split("/")
            operators_id = operators_path[2]
            self.handleOperators_DELETE(operators_id)
        #SESSIONS
        elif self.path == "/sessions":
            self.logoutUser()
        #404
        else:
            self.handleNotFound()

    def handleNotFound(self):
        self.send_response(404)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("404 Not Found.","utf-8"))

    def handleAuthenticationFail(self):
        self.send_response(401)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("404 Not Found.","utf-8"))

    def handleCantCreate(self):
        self.send_response(422)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("404 Not Found.","utf-8"))

    def handleOperators_LIST(self):
        if "user_Id" not in self.session:
            print("Not login")
            self.handleAuthenticationFail()
        else:   
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.end_headers()

            #Initlize/Create Database
            db = operatorsDB()
            operators = db.getOperators()
            self.wfile.write(bytes(json.dumps(operators),"utf-8"))

            #Get the pictures from database
        

    def handleOperators_CREATE(self):
        if "user_Id" not in self.session:
            print("Not login")
            self.handleAuthenticationFail()
        else:
            self.send_response(201)
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
        if "user_Id" not in self.session:
            print("Not login")
            self.handleAuthenticationFail()
        else:
            db = operatorsDB()
            op_check = db.retriveOperators(operators_id)

            if op_check is None:
                print("IT IS NONE for RETRIVE")
                self.handleNotFound()
            else:
                self.send_response(200)
                self.send_header("content-type", "application/json")
                self.end_headers()
                print("IT PAST for RETRIVE opcheck")

                #Initlize/Create Database
                db = operatorsDB()
                operators = db.retriveOperators(operators_id)
                self.wfile.write(bytes(json.dumps(operators),"utf-8"))

    def handleOperators_DELETE(self, operators_id):
        if "user_Id" not in self.session:
            print("Not login")
            self.handleAuthenticationFail()
        else:
            print("DEBUG: It has reach the RETRIVE FUNCTION")
            db = operatorsDB()
            op_check = db.retriveOperators(operators_id)

            if op_check is None:
                print("IT IS NONE")
                self.handleNotFound()
            else:
                print("DEBUG: It about to SEND THE RESPONSE")
                self.send_response(200)
                self.send_header("content-type", "application/x-www-form-urlencoded")
                self.end_headers()
                print("DEBUG: HEADER HAS BEEN SENT")

                #Initlize/Create Database
                db = operatorsDB()
                db.deleteOperators(operators_id)
                print(operators_id + "Operators ID has been deleted from the database")

    def handleOperators_PUT(self, operators_id):
        if "user_Id" not in self.session:
            print("Not login")
            self.handleAuthenticationFail()
        else:
            db = operatorsDB()
            op_check = db.retriveOperators(operators_id)

            if op_check is None:
                print("IT IS NONE for PUT")
                self.handleNotFound()
            else:
                self.send_response(201)
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
            self.handleCantCreate()
            print("422 is beinng trigger because a user is already in database for register")
        else:
            self.send_response(201)
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
        print("made it")
        length = self.headers["content-length"]
        body = self.rfile.read(int(length)).decode("utf-8") 
        data = parse_qs(body) #Parse it as a dictonary
        username = data['email'][0]
        password = data['password'][0] 

        db = operatorsDB()
        user = db.checkUsername(username)

        if user == None:
            self.handleAuthenticationFail()
            print("username")
        else:
            #Grab password from database, it is bytes
            user_password = user['hash_password']

            #Comapre the given password and hashpassword. They both are in bytes. Not UTF-8
            check = bcrypt.checkpw(password.encode(), user_password)
            print("made it2")

            if check == False:
                self.handleAuthenticationFail()
                print("password")
            else:
                self.send_response(201)
                self.session["user_Id"] = user["id"]
                self.end_headers()
                print("made it 3")

    def logoutUser(self):
        if "user_Id" in self.session:
            self.send_response(200)
            self.session.pop("user_Id", None) #BAD CAUSE IT MIGHT LOG EVERY ONE OUT
            #IT WORKS ACTUALLY, BUT THE OLD SESSION STILL EXIST. YOU MIGHT WANT TO
            #DELETE THE OLD SESSION.
            self.end_headers()
        else:
            self.handleAuthenticationFail()

    def end_headers(self): #everytime a end_headers appear in code, make it so it send cookie before hand.
        self.send_cookie()
        self.send_header('Access-Control-Allow-Origin', self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", 'true')
        BaseHTTPRequestHandler.end_headers(self)

def run():
    listen = ('0.000', 8080)
    server = HTTPServer(listen, MyHandler)
    print('Listening...')
    server.serve_forever()
run()
