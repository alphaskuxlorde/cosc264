#!/usr/bin/env python3

from contextlib import closing
import socket
import sys

from common import Packet, PacketType, parse_port


def loop(file_out, sock_in, sock_out):
    expected = 0
    while True:
        raw_rcvd = sock_in.recv(4096)
        try:
            rcvd = Packet.from_bytes(raw_rcvd)
        except ValueError:
            continue
        if rcvd.type_ != PacketType.data:
            continue
        if rcvd.seqno != expected:
            ack = Packet(PacketType.ack, rcvd.seqno, b'')
            sock_out.send(ack.to_bytes())
        else:
            ack = Packet(PacketType.ack, rcvd.seqno, b'')
            sock_out.send(ack.to_bytes())
            expected = 1 - expected
            if rcvd.data:
                file_out.write(rcvd.data)
            else:
                break


def main(argv):
    try:
        r_in = parse_port(argv[1])
        r_out = parse_port(argv[2])
        c_r_in = parse_port(argv[3])
        file_name = argv[4]
    except (IndexError, ValueError):
        return 'Usage: {} R_IN R_OUT C_R_IN FILE_NAME'.format(sys.argv[0])
    with open(file_name, 'xb') as file_out, \
            closing(socket.socket(type=socket.SOCK_DGRAM)) as sock_in, \
            closing(socket.socket(type=socket.SOCK_DGRAM)) as sock_out:
        sock_in.bind(('localhost', r_in))
        sock_out.bind(('localhost', r_out))
        sock_out.connect(('localhost', c_r_in))
        loop(file_out, sock_in, sock_out)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
