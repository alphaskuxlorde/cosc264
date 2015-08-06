#!/usr/bin/env python3

from contextlib import closing
import socket
import sys

from common import Packet, PacketType, parse_port


def loop(file_in, sock_in, sock_out):
    pass


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
