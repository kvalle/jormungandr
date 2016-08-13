#!/usr/bin/env python3
# encoding: utf-8

def to_bitlist(v, length=32):
    """Convert a number into an list representing its bit pattern"""
    return [(v >> i) & 1 for i in reversed(range(length))]

def from_bitlist(bitlist):
    """Convert a bit pattern (list) back into a number"""
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit
    return out

def first_n_set(n, length=32):
    """Return a number with the first n bits set"""
    return ((1 << n) - 1) << (length - n)

def setbit(n, bit, length=32):
    return n | 1 << (length - bit)

def unsetbit(n, bit, length=32):
    return n & ~(1 << (length - bit))
