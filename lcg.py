class LCG:
    def __init__(self, state, mod, mul, inc):
        self.state = state
        self.mod = mod
        self.mul = mul
        self.inc = inc
    
    def generate(self):
        r = (self.state * self.mul + self.inc) % self.mod
        if r & 2**31:
            r -= self.mod
        self.state = r
        return self.state

def find_inc(states, mod, mul):
    return (states[1] - states[0] * mul) % mod

def find_mul(states, mod):
    return (states[2] - states[1]) * pow(states[1] - states[0], -1, mod) % mod