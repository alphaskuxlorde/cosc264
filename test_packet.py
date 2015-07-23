"""Tests for ``packet`` module."""

from packet import *


def test_roundtrip():
    data = 'Ice cold\x00flambé'.encode('utf-8')
    original = Packet(PacketType.data, 424242, data)
    assert Packet.from_bytes(original.to_bytes()) == original
