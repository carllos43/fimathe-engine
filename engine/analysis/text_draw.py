"""Desenho textual estilo grafico de velas + linhas Fimathe."""
from __future__ import annotations
from typing import List, Optional, Dict, Tuple
from engine.analysis.chart_overlay import OverlayResult, build_overlay

def _fmt(p: float) -> str:
    return f"{p:.5f}"

def draw_overlay_text(ov: OverlayResult, height: int = 34) -> str:
    prices = [ov.reference_lower, ov.reference_upper, ov.neutral_lower, ov.neutral_upper,
              ov.level_50_reference, ov.level_50_neutral, ov.level_50_union, ov.stop]
    for e in ov.expansions_down:
        prices += [e["lower"], e["upper"]]
    for e in ov.expansions_up:
        prices.append(e["price"])
    if ov.entry_hypothesis is not None:
        prices.append(ov.entry_hypothesis)
    if ov.subcycle is not None:
        prices.append(ov.subcycle)
    if ov.current_price is not None:
        prices.append(ov.current_price)
    for p in ov.fatiamento_depth2:
        prices.append(p)
    lo, hi = min(prices), max(prices)
    pad = (hi - lo) * 0.06
    lo, hi = lo - pad, hi + pad
    span = hi - lo
    if span <= 0:
        return "Nao foi possivel desenhar."

    def row_for(price: float) -> int:
        return max(0, min(height - 1, int(round(((hi - price) / span) * (height - 1)))))

    annotations: Dict[int, List[Tuple[int, str]]] = {i: [] for i in range(height)}
    def tag(price, text, priority=5):
        annotations[row_for(price)].append((priority, text))

    tag(ov.stop, "X STOP", 0)
    tag(ov.neutral_upper, "ZN^", 2)
    tag(ov.reference_upper, "H==", 1)
    tag(ov.level_50_reference, "50%REF", 3)
    tag(ov.reference_lower, "L==", 1)
    tag(ov.neutral_lower, "ZNv", 2)
    if ov.entry_hypothesis is not None:
        tag(ov.entry_hypothesis, "* ENTRADA", 0)
    if ov.subcycle is not None:
        tag(ov.subcycle, "o SUBCICLO", 3)
    for e in sorted(ov.expansions_down, key=lambda x: x["mult"]):
        tag(e["lower"], f"@ TAKE {e['mult']}x", 2)
    for e in sorted(ov.expansions_up, key=lambda x: x["mult"]):
        tag(e["price"], f"@ ALVO^{e['mult']}x", 2)
    if ov.current_price is not None:
        tag(ov.current_price, ">> PRECO", 0)
    for r in annotations:
        annotations[r].sort(key=lambda x: x[0])

    ref_top, ref_bot = row_for(ov.reference_upper), row_for(ov.reference_lower)
    zn_top, zn_bot = row_for(ov.neutral_upper), row_for(ov.neutral_lower)
    stop_row = row_for(ov.stop)
    entry_row = row_for(ov.entry_hypothesis) if ov.entry_hypothesis else -1
    cur_row = row_for(ov.current_price) if ov.current_price else -1
    BODY = 8
    lines = []
    w = 72
    lines.append("=" * w)
    lines.append(f"  Fimathe | {ov.symbol} {ov.timeframe} | bias {ov.direction_bias}")
    lines.append(f"  Canal == {_fmt(ov.reference_lower)} -- {_fmt(ov.reference_upper)}  amp {_fmt(ov.amplitude)}")
    lines.append(f"  Neutra -- {_fmt(ov.neutral_lower)} -- {_fmt(ov.neutral_upper)}")
    lines.append("-" * w)
    for i in range(height):
        price_at = hi - (i / (height - 1)) * span
        if ref_top <= i <= ref_bot:
            body = "=" * BODY if i in (ref_top, ref_bot) else "#" * BODY
        elif zn_top <= i <= zn_bot:
            body = "-" * BODY if i in (zn_top, zn_bot) else "." * BODY
        else:
            body = " " * BODY
        if i == stop_row:
            body = "X" * BODY
        if i == entry_row:
            body = "*" + body[1:-1] + "*" if BODY >= 3 else body
        if i == cur_row:
            body = ">" + body[1:-1] + "<" if BODY >= 3 else body
        ann = "  ".join(a[1] for a in annotations[i][:3]) if annotations[i] else ""
        lines.append(f"  |{body}| {_fmt(price_at)}  {ann}")
    lines.append("-" * w)
    lines.append("  #/= Canal   .= Zona Neutra   X=STOP   *=ENTRADA   @=TAKE   >=preco")
    if ov.current_price is not None:
        lines.append(f"  Agora {_fmt(ov.current_price)} -> {ov.position_vs_reference} | {ov.position_vs_neutral}")
    lines.append("=" * w)
    return "\n".join(lines)


def analyze_and_draw(lower, upper, *, symbol="UNKNOWN", timeframe="M15",
                     direction_bias="down", current_price=None, height=34) -> str:
    ov = build_overlay(lower, upper, symbol=symbol, timeframe=timeframe,
                       direction_bias=direction_bias, current_price=current_price)
    return draw_overlay_text(ov, height=height) + "\n\n" + ov.summary_text()
