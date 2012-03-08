#!/usr/bin/python -u
import re
import sys

COLORS = {
    0 : "#2e3436",
    1 : "#cc0000",
    2 : "#4e9a06",
    3 : "#c4a000",
    4 : "#3465a4",
    5 : "#75507b",
    6 : "#06989a",
    7 : "#d3d7cf",
    9 : "#aaaaaa",
}

BRIGHT_COLORS = {
    0 : "#555753",
    1 : "#ef2929",
    2 : "#8ae234",
    3 : "#fce94f",
    4 : "#729fcf",
    5 : "#ad7fa8",
    6 : "#34e2e2",
    7 : "#eeeeec",
    9 : "#ffffff",
}

BG_COLORS = {
    0 : "#2e3436",
    1 : "#cc0000",
    2 : "#4e9a06",
    3 : "#c4a000",
    4 : "#3465a4",
    5 : "#75507b",
    6 : "#06989a",
    7 : "#d3d7cf",
    9 : "#ffffff",
}

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
            if 30 <= p <= 37 or p == 39:
                color = p
            elif 40 <= p <= 47 or p == 49:
                bg = p
            elif p == 1:
                bright = True
        colors = BRIGHT_COLORS if bright else COLORS
        color = colors.get(color-30)
        bg = BG_COLORS.get(bg-40)
        span = "<span style='color:%s; background-color:%s; font-weight: %s'>" % (color, bg, "bold" if bright else "normal")
        if not self.spanClosed:
            span = "</span>" + span
        self.spanClosed = False
        return span

if __name__ == "__main__":
    print "<html><body style='background-color:#000000; color:#aaaaaa;'><pre>"
    for line in sys.stdin.readlines():
        html = re.sub("\x1b\[([0-9;]*?)m", AnsiReplacer(), line)
        sys.stdout.write(html)
    print "</pre></body></html>"
