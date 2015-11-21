import asyncio
import struct
import functools
from   pickle                import dumps, loads
from   basetool.baseconstant import HEAD_FORMAT, INFORM, CALL, ANSWER
from   handler               import testhandler

class EchoServerProtocol(asyncio.Protocol):
    HEAD_LENGTH = struct.calcsize(HEAD_FORMAT)
    def __init__(self):
        self.transport      = None
        self.recieve_data   = ''.encode()
        self.wait_callbacks = {}
        self.sequence       = 0
        self.loop           = asyncio.get_event_loop()
        
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        self.peer_host, self.peer_port = peername
        print('Connection from {0}'.format(peername))
        self.transport = transport
        
    def remote_call(self, func_name, args):
        print('Remote call is called')
        future = asyncio.Future()
        message_data = dumps((func_name, args))
        self.send_only(message_data, CALL)
        self.wait_callbacks[self.sequence] = future
        return future
    
    def send_only(self, message_data, message_type):
        _head = struct.pack(HEAD_FORMAT, self.sequence, message_type, len(message_data))
        self.transport.write(_head + message_data)        

    def data_received(self, data):
        self.recieve_data += data
        buffer_length = len(self.recieve_data)
        while buffer_length >= self.HEAD_LENGTH:
            _seq_id, _message_type, _body_len = struct.unpack(HEAD_FORMAT, self.recieve_data[:self.HEAD_LENGTH])
            _message_end = self.HEAD_LENGTH + _body_len
            if buffer_length < buffer_length:
                self.recieve_data = ''
                return
            self.loop.call_soon_threadsafe(self.pick_method, _seq_id, _message_type, self.recieve_data[self.HEAD_LENGTH:_message_end])
            self.sequence += 1
            self.recieve_data = self.recieve_data[_message_end:]
            buffer_length = len(self.recieve_data)
            
    def pick_method(self, _seq_id, message_type, message_data):
        if message_type == CALL:
            _func_name, args = loads(message_data)
            if not hasattr(testhandler, _func_name):
                print('Wrong Remote Call method!!!')
                return
            this_function = getattr(testhandler, _func_name)
        elif message_type == INFORM:
            _func_name, args = loads(message_data)
            if not hasattr(testhandler, _func_name):
                print('Wrong acknowledge method!!!')
                return 
            this_function = getattr(testhandler, _func_name)
            this_function(args)
        elif message_type == ANSWER:
            if not self.wait_callbacks.has_key(_seq_id):
                print('Wrong callback method!!!')
                return
            self.wait_callbacks[_seq_id].set_result(loads(message_data))
        
    def connection_lost(self, exc):
        pass

