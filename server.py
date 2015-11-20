import asyncio
from   basetool.serverbase import EchoServerProtocol

class SunnyServer:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.createServer()
        self.mainRun()
    
    def createServer(self):
        coro = self.loop.create_server(EchoServerProtocol, '127.0.0.1', 8888)
        print('================')
        print('= Server start =')
        print('================')
        return self.loop.run_until_complete(coro)
    
    def mainRun(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        
    def __del__(self):
        self.loop.close()
    
SunnyServer()