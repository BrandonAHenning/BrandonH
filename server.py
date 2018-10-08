from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
from database import operatorsDB

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/operators":
            self.handleOperators_LIST()
        elif self.path.startswith("/operators"):
            operators_path = self.path.split("/")
            operators_id = operators_path[2]
            if self.handleOperators_RETRIVE(operators_id) is None:
                self.handleNotFound()
                #I KEEP GETTING SYNTAX ERROR, BUT DON'T KNOW WHY.
            else:
                self.handleOperators_RETRIVE(operators_id)
        else:
            self.handleNotFound()

    def do_POST(self):
        if self.path == "/operators":
            self.handleOperators_CREATE()
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
        
    #Can PRINT out the 1 Operators in Python, but not showing in Postman
    def handleOperators_RETRIVE(self, operators_id):
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        #Initlize/Create Database
        db = operatorsDB()
        operators = db.retriveOperators(operators_id)
        self.wfile.write(bytes(json.dumps(operators),"utf-8"))
        #^^^ Only apply nulls, and doesn't write.

    def handleOperators_CREATE(self):
        self.send_response(201)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("content-type", "application/x-www-form-urlencoded")
        length = self.headers["content-length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        self.end_headers()

        data = parse_qs(body) #Parse it as a dictonary

        name = data['name'][0]
        country  = data['country'][0]
        gadget = data['gadget'][0]
        weapon = data['weapon'][0]
        age = data['age'][0]

        #Initlize/Create Database
        db = operatorsDB()
        db.createOperators(name, country, gadget, weapon, age)

def run():
    listen = ('0.000', 8080)
    server = HTTPServer(listen, MyHandler)
    print('Listening...')
    server.serve_forever()
run()
