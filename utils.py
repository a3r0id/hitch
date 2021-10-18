from json import dumps
from threading import Thread

from hitch.macros import Macros

class HitchUtils:

    @staticmethod
    class params(object):
        """
        self.message, self.client, self.socket
        """
        # > Arg: Porting Tuple
        # > Object:
        # self.message, self.client, self.socket
        def __init__(self, porting):
            self.message, self.client, self.socket = porting

    @staticmethod
    def createPrivateResponse(parsed_message, response={}):
        """
        ### Creates a response string of the response payload.
        ### Validates arbitrary input from client.
        ### ** Non-System json keys such as 'id' will not be validated by this utility! **
        """
        if type(parsed_message) != dict:
            raise TypeError("\"parsed_message\" should be type \"dict\".")

        bufferMessage = {}

        # Validate ID
        if 'id' in parsed_message:
            if type(parsed_message['id']) == str:
                bufferMessage['id'] = parsed_message['id']

        # Validate ID
        if 'hasCallback' in parsed_message:
            if type(parsed_message['hasCallback']) == bool:
                bufferMessage['hasCallback'] = parsed_message['hasCallback']

        bufferMessage.update(response)

        return dumps(bufferMessage, default=str)
    
    @staticmethod
    def exampleHTTPRequestHandler(self):

        # Send response code
        self.send_response(200)
        #Send Content Type
        self.send_header('Content-type', "text/html")
        # Send end-header bytes
        self.end_headers()
        # Send a custom response
        self.wfile.write(bytes("<h1>Hello World!</h1>", "utf-8"))

    # https://stackoverflow.com/a/19846691/12376447
    @staticmethod
    def threaded(fn):
        """
        Allows a classmethod to be threaded while keeping context of the same instance from the original thread.
        """
        def wrapper(*args, **kwargs):
            thread = Thread(target=fn, args=args, kwargs=kwargs)
            thread.start()
            return thread
        return wrapper
    
    @staticmethod
    def deleteServer(port):
        
        if str(port) in Macros.socket_servers:
            del Macros.socket_servers[str(port)]

        elif str(port) in Macros.http_servers:
            del Macros.http_servers[str(port)]
            
            
