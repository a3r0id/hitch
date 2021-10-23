from hitch import Hitch, HitchUtils, HitchHttpServer, HitchManager
from logging import basicConfig, DEBUG

# Start an HTTP server to serve our document.
# This document will create the socket connection if we so choose. 
httpServer = HitchHttpServer(content=open('example.html', "r").read())

basicConfig(filename="hitch.log", level=DEBUG)

# Example Socket Handler
async def hello(porting):

    params = HitchUtils.params(porting)

    if 'name' not in params.message:
        return
    
    if type('name') != str:
        return

    response = {
        "message": f"Hello, {params.message['name']}!"
    }

    responseString = HitchUtils.createPrivateResponse(params.message, response=response)

    await params.socket.send(responseString)

# Create the Hitch instance
hitch = Hitch(port=8441)

# Add our handler
hitch.addHandler("hello", hello)

# Start the server
hitch.start()

# Create a manager server instance 
manager = HitchManager("admin", "password123")

# Start the manager
manager.start()


















