from json import loads
from hitch.client import Client 
from hitch.macros import Macros
from json import dumps
from datetime import datetime

async def serverHandler(websocket, path): 

    # REGISTER CLIENT
    CLIENT = Client(websocket) 
    Macros.socket_servers[str(websocket.port)]['clients'][CLIENT.uuid] = CLIENT

    try:

        # RESPOND AFTER SOCKET REGISTERED
        await websocket.send(dumps({
            "action": "init_event",
            "message": "Websocket Is Open"
        }))

        print("%s -- [%s] Country: %s [%s -> %s] -" % (CLIENT.address, datetime.now(), CLIENT.country, CLIENT.origin, path,))

        # MESSAGE LOOP
        async for message in websocket:

            try:
                parsed = loads(message)
            except:
                # Message is not valid JSON! Indicator of abuse, instantly deletes client from clients and closes connection.
                del Macros.socket_servers[str(websocket.port)]['clients'][CLIENT.uuid]
                return

            if parsed is not None:
                if 'action' in parsed:
                    for handler in Macros.socket_servers[str(websocket.port)]['handlers']:
                        if handler['name'] == parsed['action']:
                            await handler['function']( (parsed, None, websocket) )
                            break

    finally:
        # When client disconnects
        try:
            del Macros.socket_servers[str(websocket.port)]['clients'][CLIENT.uuid]
        except:
            pass
        pass