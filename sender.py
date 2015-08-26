#!/usr/bin/env python3

from contextlib import closing
import socket
import sys
import select

from common import Packet, PacketType, parse_port


def loop(file_in, sock_in, sock_out):
    next_ = 0
    exitFlag = False
    while not exitFlag:
        data = file_in.read(512)
        n = len(data)
        if n == 0:
            packetBuffer = Packet(PacketType.data, next_, b'')
            exitFlag = True
        else:
            packetBuffer = Packet(PacketType.data, next_, data)
        processing = True
        while processing:
            sock_out.send(packetBuffer)
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
    try:
        with open(file_name, 'rb') as file_in, \
                closing(socket.socket(type=socket.SOCK_DGRAM)) as sock_in, \
                closing(socket.socket(type=socket.SOCK_DGRAM)) as sock_out:
            sock_in.bind(('localhost', s_in))
            sock_out.bind(('localhost', s_out))
            sock_out.connect(('localhost', c_s_in))
            loop(file_in, sock_in, sock_out)
    except IOError as e:
        return str(e)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
