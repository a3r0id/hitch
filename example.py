from hitch import Hitch, HitchUtils, HitchHttpServer

from logging import DEBUG

from hitch.manager import HitchManager

# Start an HTTP server to serve our document.
# This document will create the socket connection if we so choose. 
httpServer = HitchHttpServer(content=open('example.html', "r").read())

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

# Create the instance
hitch = Hitch(log=True, loggingLevel=DEBUG, port=8441)

# Add our handler
hitch.addHandler("hello", hello)

# Start the server
hitch.start()

# Start a manager server 
manager = HitchManager("admin", "password123")

manager.start()


















