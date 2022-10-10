from constants import VEC

inttup = lambda tup: tuple((int(tup[0]), int(tup[1])))
intvec = lambda vec: VEC((int(vec[0]), int(vec[1])))

def sign(num: int | float) -> int:
    """Returns the sign of the num (+/-) as -1, 0, or 1"""
    return (num > 0) - (num < 0)