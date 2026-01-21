import re
from collections import OrderedDict

# === Load file ===
with open("gtowiz.txt", "r", encoding="utf-8") as f:
    html = f.read()

RAISE_RGB = "rgb(233, 150, 122)"
CALL_RGB  = "rgb(143, 188, 139)"

# Match each hand cell
cell_pattern = re.compile(
    r'style="([^"]*background-image:[^"]*background-size:[^"]*?)"[^>]*>(.*?)<div[^>]*class="rtc_title">([^<]+)',
    re.DOTALL | re.IGNORECASE
)

def parse_legend_numbers(cell_html):
    legend_match = re.search(r'<div[^>]*class="rtc_graph_legend[^"]*"[^>]*>(.*?)</div>\s*</div>', cell_html, re.DOTALL)
    if not legend_match:
        return []
    legend_html = legend_match.group(1)
    return [float(x) for x in re.findall(r'</span>\s*<span[^>]*>([\d.]+)</span>', legend_html)]

def extract_layers(style_text):
    gradients = re.findall(r'linear-gradient\([^)]+\)', style_text)
    colors = [re.search(r'(rgb\([^)]+\))', g).group(1) for g in gradients if re.search(r'(rgb\([^)]+\))', g)]
    size_match = re.search(r'background-size:\s*([^;]+);', style_text)
    percents = []
    if size_match:
        for part in size_match.group(1).split(","):
            m = re.search(r'([\d.]+)%', part)
            if m:
                percents.append(float(m.group(1)))
    return colors, percents

hands = OrderedDict()

for match in cell_pattern.finditer(html):
    style_block = match.group(1)
    cell_html = match.group(2)
    hand = match.group(3).strip()

    legend_vals = parse_legend_numbers(cell_html)
    if legend_vals:
        while len(legend_vals) < 3:
            legend_vals.append(0.0)
        raise_pct, call_pct, fold_pct = legend_vals[:3]
    else:
        colors, percents = extract_layers(style_block)
        raise_pct = call_pct = 0.0
        if len(colors) >= 2 and len(percents) >= 2:
            if RAISE_RGB in colors[0]:
                raise_pct = percents[0]
            if CALL_RGB in colors[1]:
                if percents[1] < 100:
                    call_pct = percents[1]
                else:
                    call_pct = max(0.0, 100.0 - raise_pct)
        elif len(colors) == 1:
            if RAISE_RGB in colors[0]:
                raise_pct = 100.0
            elif CALL_RGB in colors[0]:
                call_pct = 100.0
        fold_pct = max(0.0, 100.0 - raise_pct - call_pct)

    hands[hand] = (round(raise_pct, 1), round(call_pct, 1), round(fold_pct, 1))

# === Sort for GTO+ ===
rank_order = "AKQJT98765432"
def sort_key(h):
    if len(h) == 2:
        return (rank_order.index(h[0]), rank_order.index(h[1]), 0)
    return (rank_order.index(h[0]), rank_order.index(h[1]), 0 if h.endswith("s") else 1)

sorted_hands = sorted(hands.keys(), key=sort_key)

# === Helper: format like [x]Hand[/x] ===
def gto_format(action_index):
    parts = []
    for hand in sorted_hands:
        pct = hands[hand][action_index]
        parts.append(f"[{pct}]{hand}[/{pct}]")
    return ",".join(parts)

# === Write files ===
with open("raise_range.txt", "w", encoding="utf-8") as r:
    r.write(gto_format(0))
with open("call_range.txt", "w", encoding="utf-8") as c:
    c.write(gto_format(1))
with open("fold_range.txt", "w", encoding="utf-8") as f:
    f.write(gto_format(2))

print(f" Wrote {len(hands)} hands to raise_range.txt, call_range.txt, and fold_range.txt")
for h in ["ATs", "98s", "AKs"]:
    if h in hands:
        r, c, f = hands[h]
        print(f"{h} -> Raise {r:.1f}%  Call {c:.1f}%  Fold {f:.1f}%")


