import asyncio
import socket

import ohneio


NUL = b'\x00'


def read_upto_nul(buffer):
    '''Read data up to nul "character" in the buffer.

    If his string is not available in the buffer, wait for it.
    '''
    def wait_for_nul():
        while True:
            data = yield from ohneio.peek()
            pos = data.find(NUL)
            if pos > 0:
                return pos
            yield from ohneio.wait()

    pos = yield from wait_for_nul()
    data = yield from ohneio.read(pos + len(s))
    return data


class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()


# @ohneio.protocol
# def echo():
#     while True:
#         line = yield from read_upto(NEW_LINE)
#         yield from ohneio.write(line)



def main():
    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 7890)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    main()
