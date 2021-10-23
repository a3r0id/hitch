# Hitch
 
Hitch is a Websocket service framework that simplifies the process of aligning backend with frontend development. Quickly create multi-service (HTTP/WS) web applications with real-time communication to backend IO. Create custom handlers and callbacks to create seamless apps in a fraction of time compared to other framework workflows.

Both Hitch's Python backend objects and it's Javascript object are totally asynchronous and support message/response handling in real-time.

Developers tend to have a hard time synchronizing message responses using vanilla websocket libraries due to the lack of built-in IO accountability, Hitch handles all of this for you.

Hitch is still in it's early stages and is recommended for *Development Only*.

I would absolutely accept help with open arms so feel free to reach out to me on [Twitter](https://twitter.com/rec0ndev) if you are interested in contributing/collaborating! 

# Setup (Development)

> #### Create A Project Directory 
`$ mkdir /home/myHitchProject`
`$ cd /home/myHitchProject`

**! Then extract the contents of `hitch-master/src` to our project directory. !**

> #### Create A [Virtual Environment](https://docs.python.org/3/library/venv.html) (Recommended)
`$ python -m venv myHitchProjectVenv`
`$ .\myHitchProjectVenv\Scripts\activate`

> #### Install Requirements
`$ pip install requirements.txt`

## Example: "Hello World"

#### Showing: 

> **Static HTTP server implementation**

> **Service-wide logging**

> **Websocket server implementation**

> **HitchManager Implementation**

#### Python (Server/s)

```py
from hitch import Hitch, HitchUtils, HitchHttpServer, HitchManager
from logging import basicConfig, DEBUG


# Start an HTTP server to serve our document.
# This document will create the socket connection if we so choose. 
httpServer = HitchHttpServer(content=open('example.html', "r").read())


# Initialize debug logging
basicConfig(filename="hitch.log", level=DEBUG)


# Example Socket Handler
async def hello(porting):

    # Unloading handler params (self.message, self.client, self.socket)
    params = HitchUtils.params(porting)

    # Some basic server-side Validation
    # If we `return` then the message is effectively dropped.
    if 'name' not in params.message: return
    if type('name') != str: return

    # Create our response
    response = {
        "message": f"Hello, {params.message['name']}!"
    }

    # Create an automatic response to the client.
    # Due to the fact that the message is ONLY going back to this client we can safely pass the client/messageID back to the client, if need be.
    # This utility essentially updates our response with required information to fullfil a client's callback. This is how the Javascript client knows when/how to handle a response from the server. 
    responseString = HitchUtils.createPrivateResponse(params.message, response=response)

    # Send the message to the client
    await params.socket.send(responseString)


# Create the Hitch instance
# Server adapter defaults to 127.0.0.1
hitch = Hitch(port=8441)

# Add our handler that we defined above
hitch.addHandler("hello", hello)

# Start Hitch
hitch.start()


#### Hitch Manager ####

# Create/start a HitchManager instance 
# HitchManager defaults to port 4444 and can be accessed directly from the file titled "manager.html".
manager = HitchManager("admin", "password123")
manager.start()

```

###### Output:
```cmd
Started New Thread. Starting HTTP/S Server @ http://127.0.0.1:80...
Started New Thread. Starting Websocket Server @ ws/s://127.0.0.1:8441...
Started New Thread. HitchManager is live @ C:\Users\User\Desktop\myHitchProject\manager.html...
Started New Thread. Starting Websocket Server @ ws/s://127.0.0.1:4444...
```



#### HTML/Javascript (Client)

```js
<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]>      <html class="no-js"> <!--<![endif]-->
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>Hitch Hello Example</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="js/hitch.js"></script>
    </head>
    <body>

            <label for="name">Enter Your Name</label>
            <input type="text" id="name">
            <button id="sub">Submit</button> 
        
        <script>
            // Initialize our HitchClient instance
            let hitchClient = new HitchClient("ws://" + location.hostname + ":8441/");
            // Our onClick handler
            document.getElementById("sub").onclick = () => {
                // Get the clients input (name)
                let usersName = document.getElementById("name").value;
                if (usersName.length > 1){
                    // Send our message to the server,
                    hitchClient.send( "hello", data={
                    name: usersName
                    // Designate a callback to handle the response message from the server, when the time comes.
                    }, callback = (data) => {
                        // We should see an alert containing our response message from the server.
                        alert(data.message)
                    })
                }
            };
        </script>

    </body>
</html>
```