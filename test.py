#!/usr/bin/python3
import inspect
import json
import socket
import sys


NUL = b'\x00'

DEFAULT_CONFIG = {
    'host': 'localhost',
    'port': 7890
}


def test_listens_to_socket_connections(configuration):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((configuration['host'], configuration['port']))
    s.close()


def test_responds_to_pingpong_subscription(configuration):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((configuration['host'], configuration['port']))

    subscriptions = ['@routing/subscribe/reply']
    s.sendall(json.dumps({
        'event': 'routing/subscribe',
        'subscriptions': subscriptions,
        'size': 0,        
    }).encode('utf-8'))
    s.sendall(NUL)

    buf = bytearray()
    while len(buf) == 0 or buf[-1] != 0:
        received = s.recv(1)
        buf.extend(received)

    assert len(buf) > 0
    assert buf[-1] == 0
    response = json.loads(buf[:-1].decode('utf-8'))

    assert response['subscriptions'] == subscriptions
    assert response['event'] == 'routing/subscribe/reply'
    s.close()



if __name__ == '__main__':
    test_functions = [(name, obj) for name, obj in
                      inspect.getmembers(sys.modules[__name__])
                      if inspect.isfunction(obj) and name.startswith('test_')]

    for name, func in test_functions:
        print("Running {}".format(name), file=sys.stderr)
        func(DEFAULT_CONFIG)

    print('GREAT SUCCESS')
