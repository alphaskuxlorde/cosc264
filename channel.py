#!/usr/bin/env python3
""""Sets up the channel program"""

import sys
import select
import socket
import random

from common import Packet, parse_port


def loop(sender_in, sender_out, receiver_in, receiver_out, p_rate):
    while True:
        ready, _, _ = select.select([sender_in, receiver_in], [], [])
        for sock in ready:
            raw_packet = sock.recv(2**16)
            if random.random() < p_rate:
                continue
            elif sock == sender_in:
                try:
                    receiver_out.send(raw_packet)
                except ConnectionRefusedError:
                    print('channel: lost connection to receiver')
                    return
                else:
                    print('sender->receiver:', Packet.from_bytes(raw_packet))
            elif sock == receiver_in:
                try:
                    sender_out.send(raw_packet)
                except ConnectionRefusedError:
                    print('channel: lost connection to sender')
                    return
                else:
                    print('receiver->sender:', Packet.from_bytes(raw_packet))


def main(argv):
    try:
        c_s_in, c_s_out, c_r_in, c_r_out, s_in, r_in = map(parse_port, argv[1:7])
        p_rate = float(argv[7])
    except (IndexError, ValueError):
        return ('Usage: {} C_S_IN C_S_OUT C_R_IN C_R_OUT S_IN R_IN P_RATE'
                .format(argv[0]))
    sender_in = socket.socket(type=socket.SOCK_DGRAM)
    sender_in.bind(('localhost', c_s_in))
    sender_out = socket.socket(type=socket.SOCK_DGRAM)
    sender_out.bind(('localhost', c_s_out))
    receiver_in = socket.socket(type=socket.SOCK_DGRAM)
    receiver_in.bind(('localhost', c_r_in))
    receiver_out = socket.socket(type=socket.SOCK_DGRAM)
    receiver_out.bind(('localhost', c_r_out))
    sender_out.connect(('localhost', s_in))
    receiver_out.connect(('localhost', r_in))
    loop(sender_in, sender_out, receiver_in, receiver_out, p_rate)
    sender_in.close()
    sender_out.close()
    receiver_in.close()
    receiver_out.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
