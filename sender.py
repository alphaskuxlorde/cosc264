#!/usr/bin/env python3

from contextlib import closing
import socket
import sys
import select

from common import Packet, PacketType, parse_port


def loop(file_in, sock_in, sock_out):
    next_ = 0
    exit_flag = False
    while not exit_flag:
        data = file_in.read(512)
        packet = Packet(PacketType.data, next_, data)
        exit_flag = not data
        processing = True
        while processing:
            try:
                sock_out.send(packet.to_bytes())
            except ConnectionRefusedError:
                print('sender: connection lost')
                return
            ready, _, _ = select.select([sock_in], [], [], 1)
            if not ready:
                continue
            rcvd = sock_in.recv(2**16)
            try:
                exploded = Packet.from_bytes(rcvd)
            except ValueError:
                continue
            if exploded.type_ != PacketType.ack:
                continue
            if exploded.data:
                continue
            if exploded.seqno != next_:
                continue
            next_ = 1 - next_
            processing = False


def main(argv):
    try:
        s_in = parse_port(argv[1])
        s_out = parse_port(argv[2])
        c_s_in = parse_port(argv[3])
        file_name = argv[4]
    except (IndexError, ValueError):
        return 'Usage: {} S_IN S_OUT C_S_IN FILE_NAME'.format(sys.argv[0])
    with open(file_name, 'rb') as file_in, \
            closing(socket.socket(type=socket.SOCK_DGRAM)) as sock_in, \
            closing(socket.socket(type=socket.SOCK_DGRAM)) as sock_out:
        sock_in.bind(('localhost', s_in))
        sock_out.bind(('localhost', s_out))
        sock_out.connect(('localhost', c_s_in))
        loop(file_in, sock_in, sock_out)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
