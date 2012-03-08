from colorsys import rgb_to_hsv, hsv_to_rgb

def hexify(rgb):
    return "#%02x%02x%02x" % rgb

def dehexifiy(hrgb):
    r = hrgb[1:3]
    g = hrgb[3:5]
    b = hrgb[5:7]
    return (int(r,16), int(g,16), int(b,16))

def hsv2rgb((h,s,v)):
    r,g,b = hsv_to_rgb(h,s,v)
    return tuple(int(round(c*255)) for c in [r,g,b])

def rgb2hsv((r,g,b)):
    return (rgb_to_hsv(r/255.0, g/255.0, b/255.0))

def adjust_to_background(color, source_bg, target_bg):
    h,s,v = rgb2hsv(color)
    source_v = rgb2hsv(source_bg)[2]
    target_v = rgb2hsv(target_bg)[2]
    new_v = abs(target_v - (1 - (v - source_v)))
    return hsv2rgb((h, s, new_v))

if __name__ == "__main__":
    import sys
    print hexify(adjust_to_background(*map(dehexifiy, sys.argv[1:])))

