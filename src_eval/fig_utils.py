import matplotlib as mpl
from cycler import cycler

FONT_MONOSPACE = {'fontname': 'monospace'}
MARKERS = "o^s*DP1"
COLORS = [
    "darkseagreen",
    "salmon",
    "cornflowerblue",
    "seagreen",
    "orange",
    "lightpink",
    "dimgray",
]
COLORS_FIRE = ["#9c2963", "#282e9b", "#fb9e07"]

mpl.rcParams['axes.prop_cycle'] = cycler(color=COLORS)
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['lines.markersize'] = 7
mpl.rcParams['axes.linewidth'] = 1.5