from logging import basicConfig, DEBUG
from websockets import serve as WS_SERVE
from asyncio import new_event_loop, set_event_loop
from hitch.server import serverHandler
from uuid import uuid1
from hitch.macros import Macros
from hitch.utils import HitchUtils

class Hitch(object):
    """
    Hitch Handler Porting:  (self.message, self.client, self.socket)
    """
    def __init__(
        self,
        address="127.0.0.1",
        port=8440,
        loggingLevel=20,
        server_max_size=9000000,
        server_ping_timeout=None,
        ssl_context=None
        ):

        self.serverHandler = serverHandler
        self.clients       = {}
        self.running       = False
        self.address       = address
        self.port          = port

        self.config = dict(
            address=address,
            port=port,
            loggingLevel=loggingLevel,
            server_max_size=server_max_size,
            server_ping_timeout=server_ping_timeout,
            ssl=ssl_context
            )


        # Starts new event loop
        self.loop = new_event_loop()
        set_event_loop(self.loop)

        self.server = WS_SERVE(
            self.serverHandler,
            self.config['address'],
            self.config['port'],
            max_size=self.config['server_max_size'],
            ping_timeout=self.config['server_ping_timeout']
            )

        # Add to servers Macro, unique by port
        Macros.socket_servers[str(self.port)] = {
            'handlers': [],
            'clients':  {}
        }


    # UPDATE CONFIG
    def updateConfig(self, key, value):
        if key in self.config:
            self.config[key] = value

    # UPDATE HANDLERS LIST
    def addHandler(self, actionName, function):
        Macros.socket_servers[str(self.port)]['handlers'].append({'name': actionName, 'function': function})
    

    # START SERVER
    @HitchUtils.threaded
    def start(self):

        self.running = True

        self.loop.run_until_complete(self.server)

        print(f"Started New Thread. Starting Websocket Server @ ws/s://{self.config['address']}:{self.config['port']}...")

        self.loop.run_forever()




