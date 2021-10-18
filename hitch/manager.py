from hitch import Hitch
from hitch.macros import Macros
from hitch import HitchUtils
from os import getcwd
from os.path import join as pjoin

class HitchManager(object):
    def __init__(self, username, password, WS_adapter='127.0.0.1', WS_port=4444):
        Macros.manager_server['server']   = Hitch(WS_adapter, WS_port, log=True, logName="manager.log")
        Macros.manager_server['username'] = username
        Macros.manager_server['password'] = password

        async def get_instances_handler(porting):
            
            params = HitchUtils.params(porting)

            response = {"action": "get_instances", "http": Macros.http_servers, "socket": Macros.socket_servers}
            
            responseString = HitchUtils.createPrivateResponse(params.message, response=response)

            await params.socket.send(responseString)

        self.instances       = get_instances_handler

        async def delete_service(porting):
            params = HitchUtils.params(porting)
            if 'username' in params.message and 'password' in params.message:
                if params.message['username'] == Macros.manager_server['username'] and params.message['password'] == Macros.manager_server['password']:
                    if 'service_port' in params.message:
                        if type(params.message['service_port']) == str:
                            HitchUtils.deleteServer(params.message['service_port'])
                            print(f"Deleted service @ port {params.message['service_port']} via HitchManager.")

        self.delete_service  = delete_service


    @HitchUtils.threaded
    def start(self):
        Macros.manager_server['server'].addHandler("get_instances", self.instances)
        Macros.manager_server['server'].addHandler("delete_service", self.delete_service)
        managerLocation = pjoin(getcwd(), "manager.html")
        print(f"Started New Thread. HitchManager is live @ {managerLocation}")
        Macros.manager_server['server'].start()


