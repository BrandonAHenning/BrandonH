import os, base64

class SessionStore:

    def __init__(self):
        #file cabinet, one per session
        self.sessions = {}
        return

    def generateSessionId(self):
        rnum = os.urandom(32)
        tstr = base64.b64encode(rnum).decode("utf-8")
        return rstr

    def createSession(self):
        sessionId = self.generateSessionId()
        #add a new session (dictionary) to the file cabinet (dictionary)
        # use the generate session ID
        self.sessions[sessionId] = {} #self.sessions = {azv58930454: {}, fdfd78ahfdl: {}, ...}
        return sessionId

    def getSession(self, sessionId):
        if sessionId in self.sessions:
            #return existing session by ID
            return self.sessions[sessionId]
        else:
            #return None if ID is invalid
            return None
