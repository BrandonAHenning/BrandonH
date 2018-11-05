import os, base64

class SessionStore:

    def __init__(self):
        #file cabinet, one per session
        self.sessions = {}
        return

    def generateSessionId(self):
        rnum = os.urandom(32)
        tstr = base64.b64encode(rnum).decode("utf-8")
        print("Generating Session ID")
        return tstr

    def createSession(self):
        sessionId = self.generateSessionId()
        #add a new session (dictionary) to the file cabinet (dictionary)
        # use the generate session ID
        self.sessions[sessionId] = {} #self.sessions = {azv58930454: {}, fdfd78ahfdl: {}, ...}
        print("Creating a Session with the assicoate ID")
        return sessionId

    def getSession(self, sessionId):
        if sessionId in self.sessions:
            #return existing session by ID
            print("Session ID does exist within Self.Sessions")
            return self.sessions[sessionId]
        else:
            #return None if ID is invalid
            print("Session ID does NOT exist within Self.Session")
            return None
