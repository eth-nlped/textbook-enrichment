from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import fig_utils

legend_lines = [
    Line2D([0], [0], lw=2, marker="s", color=fig_utils.COLORS[0]),
    Line2D([0], [0], lw=2, marker="s", color=fig_utils.COLORS[1]),
    Line2D([0], [0], lw=2, marker="s", color=fig_utils.COLORS[2]),
    Line2D([0], [0], lw=2, marker="s", color=fig_utils.COLORS[3]),
    Line2D([0], [0], lw=2, marker="s", color=fig_utils.COLORS[4]),
]

plt.axis('off')
plt.legend(
    legend_lines, ['Local', 'Global', "C", "D", "E"],
    loc="lower left", ncol=5,
)
# TODO: proper cropping
plt.tight_layout(pad=0)
plt.show()