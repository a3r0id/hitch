from websockets import serve as WS_SERVE
from asyncio import new_event_loop, set_event_loop
from json import loads
from hit

async def serverHandler(websocket, path): 

    # REGISTER CLIENT
    CLIENT = Client(websocket) 
    Macros.socke[str(websocket.port)]['clients'][CLIENT.uuid] = CLIENT

    try:



        # MESSAGE LOOP
        async for message in websocket:

            try:
                parsed = loads(message)
            except:
                pass

            print(parsed)

    finally:
        print("disconected!")
        pass


address="127.0.0.1"
port=8441

# Starts new event loop
loop = new_event_loop()
set_event_loop(loop)

server = WS_SERVE(
    serverHandler,
    address,
    port
    )

loop.run_until_complete(server)
print(f"Started New Thread.")
loop.run_forever()