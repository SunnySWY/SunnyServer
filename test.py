import asyncio

async def test1():
    print ('test1')
    return 1
    
async def test2(num):
    print ('test2')
    return num
    
async def test3(num):
    print ('test3')
    return num
    
@asyncio.coroutine    
def _all():  
    yield from asyncio.ensure_future(test1())
    yield from asyncio.ensure_future(test2())
    yield from asyncio.ensure_future(test3())
    
loop = asyncio.get_event_loop()
asyncio.ensure_future(_all())
loop.run_forever()
loop.close()