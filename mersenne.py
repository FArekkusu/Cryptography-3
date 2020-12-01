import numpy as np

class MersenneTwister:
    def __init__(self):
        self.w = 32
        self.n = 624
        self.m = 397
        self.r = 31
        self.u = 11
        self.s = 7
        self.t = 15
        self.l = 18
        self.a = 0x9908B0DF
        self.d = 0xFFFFFFFF
        self.b = 0x9D2C5680
        self.c = 0xEFC60000
        self.f = 1812433253
        self.index = 624
        self.lower_mask = (1 << self.r) - 1
        self.upper_mask = get_lower_bits(~self.lower_mask, self.w)
        self.state = None
    
    def initialize_state(self, seed):
        self.state = [0] * self.n
        self.state[0] = get_lower_bits(seed, self.w)
        for i in range(1, self.n):
            self.state[i] = get_lower_bits(self.f * (self.state[i-1] ^ (self.state[i-1] >> (self.w - 2))) + i, self.w)
    
    def twist(self):
        for i in range(self.n):
            x = (self.state[i] & self.upper_mask) + (self.state[(i+1)%self.n] & self.lower_mask)
            y = x >> 1
            if x & 1:
                y = y ^ self.a
            self.state[i] = self.state[(i + self.m) % self.n] ^ y
        self.index = 0

    def generate(self):
        if self.state is None:
            raise "State is not initialized"
        if self.index >= self.n:
            self.twist()
        y = self.state[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ ((y >> self.l))
        self.index += 1
        return get_lower_bits(y, self.w)

def get_lower_bits(n, w):
    return n & ((1 << w) - 1)

def reverse_shift_4(r):
    a = np.array([0] * 32)
    a[:18] = r[:18]
    a[18:] = r[18:] ^ a[:14]
    return a

def reverse_shift_3(r):
    a = np.array([0] * 32)
    a[17:] = r[17:]
    a[2:17] = r[2:17] ^ (a[17:] & np.array([1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0]))
    a[:2] = r[:2] ^ (a[15:17] & np.array([1, 1]))
    return a

def reverse_shift_2(r):
    a = np.array([0] * 32)
    a[25:] = r[25:]
    a[18:25] = r[18:25] ^ (a[25:] & np.array([0, 1, 0, 1, 1, 0, 1]))
    a[11:18] = r[11:18] ^ (a[18:25] & np.array([0, 1, 1, 0, 0, 0, 1]))
    a[4:11] = r[4:11] ^ (a[11:18] & np.array([1, 1, 0, 1, 0, 0, 1]))
    a[:4] = r[:4] ^ (a[7:11] & np.array([1, 0, 0, 1]))
    return a

def reverse_shift_1(r):
    a = np.array([0] * 32)
    a[:11] = r[:11]
    a[11:22] = r[11:22] ^ a[:11]
    a[22:] = r[22:] ^ a[11:21]
    return a

def reverse_shifts(y):
    to_binary_digits = lambda n: np.array(([0] * 31 + list(map(int, f"{n:b}")))[-32:])
    from_binary_digits = lambda a: int("".join(map(str, a.tolist())), 2)

    y = to_binary_digits(y)

    y = reverse_shift_4(y)
    y = reverse_shift_3(y)
    y = reverse_shift_2(y)
    y = reverse_shift_1(y)

    return from_binary_digits(y)