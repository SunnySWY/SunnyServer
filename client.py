import asyncio
from   basetool.serverbase import EchoServerProtocol

class SunnyClient:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        _, self.p = self.createClient()
        asyncio.ensure_future(self.doSomething())
        self.mainRun()
    
    def createClient(self):
        coro = self.loop.create_connection(EchoServerProtocol, '127.0.0.1', 8888)
        return self.loop.run_until_complete(coro)
    
    @asyncio.coroutine
    def doSomething(self):
        for _ in range(10):
            test = yield from self.p.remote_call('test', args=[1,2,3])
            print('get call back!!!', test)
    
    def mainRun(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        
    def __del__(self):
        self.loop.close()
        
SunnyClient()