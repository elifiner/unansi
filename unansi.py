#!/usr/bin/python -u
import re
import sys
import cgi

# Those colors are the ones used by the Ubuntu default configuration (Tango).
# They look well on a black background. To convert them to pleasing colors
# on a white background (fitting a web page), I wrote the dark2light function.

COLORS = {
    0 : "#333333",
    1 : "#cc0000",
    2 : "#4e9a06",
    3 : "#c4a000",
    4 : "#3465a4",
    5 : "#75507b",
    6 : "#06989a",
    7 : "#dddddd",
    9 : "#aaaaaa",
}

BRIGHT_COLORS = {
    0 : "#555555",
    1 : "#ef2929",
    2 : "#8ae234",
    3 : "#fce94f",
    4 : "#729fcf",
    5 : "#ad7fa8",
    6 : "#34e2e2",
    7 : "#eeeeee",
    9 : "#ffffff",
}

BG_COLORS = {
    0 : "#333333",
    1 : "#cc0000",
    2 : "#4e9a06",
    3 : "#c4a000",
    4 : "#3465a4",
    5 : "#75507b",
    6 : "#06989a",
    7 : "#dddddd",
    9 : "#000000",
}

def dark2light(color):
    import colorsys
    if color[0] == "#":
        color = color[1:]
    assert(len(color) == 6)
    r,g,b = (int(color[0:2],16)/255.0, int(color[2:4],16)/255.0, int(color[4:6],16)/255.0)
    h,s,v = colorsys.rgb_to_hsv(r,g,b)
    rr,gg,bb = colorsys.hsv_to_rgb(h,s,1-v/2)
    return "#%02x%02x%02x" % tuple(map(int, [rr*255, gg*255, bb*255]))

class AnsiReplacer(object):
    def __init__(self):
        self.spanClosed = True

    def __call__(self, m):
        params = [p for p in m.group(1).split(";") if p]
        if not params:
            self.spanClosed = True
            return "</span>"
        color = 0
        bg = 0
        bright = False
        for p in params:
            p = int(p)
            if 30 <= p <= 37:
                color = p
            elif 40 <= p <= 47:
                bg = p
            elif p == 1:
                bright = True
        colors = BRIGHT_COLORS if bright else COLORS
        color = colors.get(color-30, colors[9])
        bg = BG_COLORS.get(bg-40, BG_COLORS[9])
        new_color = dark2light(color)
        new_bg = dark2light(bg)
        span = "<span style='color:%s; background-color: %s; font-weight: %s'>" % (new_color, new_bg, "bold" if bright else "normal")
        if not self.spanClosed:
            span = "</span>" + span
        self.spanClosed = False
        return span

if __name__ == "__main__":
    print "<html><body style='color:%s;'><pre>" % dark2light(COLORS[9])
    for line in sys.stdin.readlines():
        line = cgi.escape(line)
        html = re.sub("\x1b\[([0-9;]*?)m", AnsiReplacer(), line)
        sys.stdout.write(html)
    print "</pre></body></html>"
