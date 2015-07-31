"""Tests for ``common`` module."""

import pytest

from common import *


def test_packet_roundtrip():
    data = 'Ice cold\x00flambé'.encode('utf-8')
    original = Packet(PacketType.data, 424242, data)
    assert Packet.from_bytes(original.to_bytes()) == original


def test_valid_port():
    assert parse_port('4242') == 4242
    assert parse_port('1024') == 1024
    assert parse_port('64000') == 64000


def test_invalid_port():
    with pytest.raises(ValueError):
        parse_port('')
    with pytest.raises(ValueError):
        parse_port('ducks')
    with pytest.raises(ValueError):
        parse_port('1023')
    with pytest.raises(ValueError):
        parse_port('64001')
    with pytest.raises(ValueError):
        parse_port('-1')
