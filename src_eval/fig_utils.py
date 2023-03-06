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

PRETTY_NAME = {
    "bleu": "BLEU",
    "chrf": "ChrF",
    "ter": "TER",
    "meteor": "METEOR",
    "comet": "COMET",
    "bleurt": "BLEURT",

    "conf_exp": "exp(conf$_t$)",
    "conf_var": "Var($\{$conf$_{h_i} | h_i \in H \}$)",
    "conf_exp_var": "Var($\{\exp($conf$_{h_i}) | h_i \in H \}$)",
    "conf_raw": "conf.",
    "conf": "conf$_t$",

    # hypothesis variance
    "h1_hx_bleu_avg": "avg($\{BLEU(t, h_i) | h_i \in H \}$)",
    "h1_hx_bleu_var": "Var($\{BLEU(t, h_i) | h_i \in H \}$)",
    "hx_hx_bleu_avg": "avg($\{BLEU(h_i, h_j) | h_i, h_j \in H, i \\neq j \}$)",
    "hx_hx_bleu_var": "Var($\{BLEU(h_i, h_j) | h_i, h_j \in H, i \\neq j \}$)",

    # lenght-based things
    "len_raw": "$|s|+|t|$",
    "|t_i|_var": "Var($\{|h_i|| h_i \in H\}$)",
    "|s|": "$|s|$",
    "|t|": "$|t|$",
    "|s|+|t|": "$|s|+|t|$",
    "|s|-|t|": "$|s|-|t|$",
    "|s|/|t|": "$|s|/|t|$",

    # models
    "mbert": "mBERT",
    "tfidf": "LR TF-IDF",
    "lr_multi": "LR Multi",
    "me_text": "ME text",
    "me_all": "ME all",

    "wmt21-comet-qe-mqm": "COMET-QE  ",
    "zscore": "human",
}
