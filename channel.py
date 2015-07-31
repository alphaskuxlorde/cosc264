""""Sets up the channel program"""

import sys
import select
import socket
import random

from common import Packet, parse_port


CSIN, CSOUT, CRIN, CROUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
SIN = sys.argv[5]
RIN = sys.argv[6]
P_RATE = float(sys.argv[7])


def main(argv):
    csin_n, csout_n, crin_n, crout_n = all_ports(CSIN, CSOUT, CRIN, CROUT)
    sin, rin = SIN, RIN
    if len(set(csin_n, csout_n, crin_n, crout_n, sin, rin)) != 6:
        raise ValueError("Port numbers must all be distinct")
    # This could be moved out of main(), checking the argvs instead.
    p = P_RATE
    csin = socket.socket(type=socket.SOCK_DGRAM)
    csin.bind(("", csin_n))
    csout = socket.socket(type=socket.SOCK_DGRAM)
    csout.bind(("", csout_n))
    crin = socket.socket(type=socket.SOCK_DGRAM)
    crin.bind(("", crin_n))
    crout = socket.socket(type=socket.SOCK_DGRAM)
    crout.bind(("", crout_n))
    csout.connect(("", sin))
    crout.connect(("", rin))
    while True:
        ready, _, _ = select.select([csin, crin], [], [])
        for nodule in ready:
            clump = nodule.recv(2**16)
            if nodule == csin:
                try:
                    Packet.from_bytes(clump)
                    u = random.random() < p
                    if u:
                        continue
                    else:
                        crout.send(clump)
                except ValueError:
                    continue
            elif nodule == crin:
                try:
                    Packet.from_bytes(clump)
                    u = random.random() < p
                    if u:
                        continue
                    else:
                        csout.send(clump)
                except ValueError:
                    continue


def all_ports(csin, csout, crin, crout):
    new_csin = parse_port(scin)
    new_csout = parse_port(csout)
    new_crin = parse_port(crin)
    new_crout = parse_port(crout)
    return new_csin, new_csout, new_crin, new_crout


if __name__ == "__main__":
    main(sys.argv)
