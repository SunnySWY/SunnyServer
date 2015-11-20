import asyncio
import struct
from   basetool.baseconstant import HEAD_FORMAT

class EchoServerProtocol(asyncio.Protocol):
    HEAD_LENGTH = struct.calcsize(HEAD_FORMAT)
    def __init__(self):
        self.transport      = None
        self.recieve_data   = ''.encode()
        self.wait_callbacks = {}
        self.sequence       = 0
        
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        self.peer_host, self.peer_port = peername
        print('Connection from {0}'.format(peername))
        self.transport = transport
        
    def remote_call(self, message_data):
        print('Remote call is called')
        future = asyncio.Future()
        _head = struct.pack(HEAD_FORMAT, self.sequence, len(message_data))
        self.transport.write(_head + message_data.encode())
        #print(self.sequence, future)
        self.wait_callbacks[self.sequence] = future
        return future
    
    def send_only(self, message_data):
        _head = struct.pack(HEAD_FORMAT, self.sequence, len(message_data))
        self.transport.write(_head + message_data.encode())        

    def data_received(self, data):
        print('Get Receive!')
        self.recieve_data += data
        buffer_length = len(self.recieve_data)
        while buffer_length >= self.HEAD_LENGTH:
            _seq_id, _body_len = struct.unpack(HEAD_FORMAT, self.recieve_data[:self.HEAD_LENGTH])
            #print(_body_len, type(_body_len), self.HEAD_LENGTH, type(self.HEAD_LENGTH))
            _message_end = self.HEAD_LENGTH + _body_len
            if buffer_length < buffer_length:
                self.recieve_data = ''
                return
            call_backs =  self.wait_callbacks.get(int(_seq_id), None)
            #print(_seq_id, self.wait_callbacks)
            if self.peer_port != 8888:
                self.send_only(self.recieve_data[self.HEAD_LENGTH:_body_len].decode())
            elif not call_backs:
                print('wrong')
            else:
                print('sequence check',self.sequence)
                _data = self.recieve_data[self.HEAD_LENGTH:_body_len]
                #print(repr(_body_len), repr(data.decode()))
                call_backs.set_result(data.decode())
            self.sequence += 1
            self.recieve_data = self.recieve_data[_message_end:]
            buffer_length = len(self.recieve_data)
        
    def connection_lost(self, exc):
        pass

