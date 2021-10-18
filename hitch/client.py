from datetime import datetime, timedelta
from uuid     import uuid1

class Client(object):
    """
    The base class-object for client management.
    """
    def __init__(self, websocket):

        # TIME KEEPING
        self.start = datetime.now()

        # LAST ACK
        self.last_ack = None

        # RATE-LIMITING
        self.last_command_time = datetime.now() - timedelta(seconds=10)

        # UUID
        self.uuid = str(uuid1())

        # INRINSINCS
        self.websocket = websocket

        # HEADER PARSED INFO
        self.address = None
        self.country = None
        self.user_agent = None
        self.origin = None
        self.sec_opts = {
            'sec-websocket-extensions': None,
        }
        
        self.cookie = None
    
        # PARSE HEADERS
        for key in self.websocket.request_headers:

            if (key.lower() == 'cf-connecting-ip'):
                self.address = self.websocket.request_headers[key]
                
            elif (key.lower() == 'cf-ipcountry'):
                self.country = self.websocket.request_headers[key]

            elif (key.lower() == 'user-agent'):
                self.user_agent = self.websocket.request_headers[key]

            elif (key.lower() == 'origin'):
                self.origin = self.websocket.request_headers[key]      

            elif (key.lower() == 'sec-websocket-key'):
                self.sec_opts['sec-websocket-key'] = self.websocket.request_headers[key]      

            elif (key.lower() == 'sec-websocket-extension'):
                self.sec_opts['sec-websocket-extension'] = self.websocket.request_headers[key]  

            elif (key.lower() == 'sec-websocket-version'):
                self.sec_opts['sec-websocket-version'] = self.websocket.request_headers[key]      

            elif (key.lower() == 'cookie'):
                self.cookie = self.websocket.request_headers[key]      
                
        if self.address is None:
            self.address = (self.websocket.remote_address)  

