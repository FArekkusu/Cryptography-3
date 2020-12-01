from casino_requests import register, make_bet
from lcg import LCG, find_mul, find_inc
from mersenne import MersenneTwister, reverse_shifts

def break_lcg(user_id):
    mode = "Lcg"

    states = [make_bet(mode, user_id, 1, 0)["realNumber"] for _ in range(3)]
    mod = 2**32
    mul = find_mul(states, mod)
    inc = find_inc(states, mod, mul)
    lcg = LCG(states[-1], mod, mul, inc)

    make_bet(mode, user_id, 1, lcg.generate())
    make_bet(mode, user_id, 1_000, lcg.generate())
    print(make_bet(mode, user_id, 1_000_000, lcg.generate()))

def break_mt(user_id, break_better_mt):
    mode = "Better" * break_better_mt + "Mt"

    mersenne_twister = MersenneTwister()
    mersenne_twister.state = [reverse_shifts(make_bet(mode, user_id, 1, 0)["realNumber"]) for _ in range(624)]

    make_bet(mode, user_id, 1, mersenne_twister.generate())
    make_bet(mode, user_id, 1_000, mersenne_twister.generate())
    print(make_bet(mode, user_id, 1_000_000, mersenne_twister.generate()))

if __name__ == "__main__":
    user_id = input("Enter user id: ")
    registration_result = register(user_id)

    if "error" in registration_result:
        print(registration_result["error"])
    else:
        print("Starting...\n")
        break_lcg(user_id)
        break_mt(user_id, False)
        break_mt(user_id, True)