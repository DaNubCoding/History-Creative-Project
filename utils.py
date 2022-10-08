from constants import VEC
import colorsys

inttup = lambda tup: tuple((int(tup[0]), int(tup[1])))
intvec = lambda vec: VEC((int(vec[0]), int(vec[1])))

def hsv_to_rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))