"""Dependency-free SVG renderer for extracted candles and Fimathe reference levels."""
from __future__ import annotations
from html import escape
from typing import Any, Dict, List


def render_candles_svg(
    candles: List[Dict[str, Any]],
    *,
    channel_lower: float,
    channel_upper: float,
    neutral_lower: float,
    neutral_upper: float,
    level_50: float,
    symbol: str = "UNKNOWN",
    timeframe: str = "UNKNOWN",
    width: int = 1000,
    height: int = 620,
) -> str:
    """Render a fresh chart from OHLC data; this is not an overlay on the upload."""
    if not candles:
        raise ValueError("At least one candle is required")
    if width < 480 or height < 320:
        raise ValueError("width/height too small for a readable chart")
    for c in candles:
        if not (c["high"] >= max(c["open"], c["close"]) >= min(c["open"], c["close"]) >= c["low"]):
            raise ValueError("Invalid OHLC candle bounds")

    all_prices = [float(c[k]) for c in candles for k in ("high", "low")]
    all_prices += [channel_lower, channel_upper, neutral_lower, neutral_upper, level_50]
    pmin, pmax = min(all_prices), max(all_prices)
    pad = (pmax - pmin) * 0.06 or max(abs(pmax) * 0.001, 0.01)
    pmin, pmax = pmin - pad, pmax + pad
    left, right, top, bottom = 88, width - 30, 76, height - 58
    plot_w, plot_h = right - left, bottom - top

    def y(v: float) -> float:
        return bottom - (v - pmin) / (pmax - pmin) * plot_h

    def line(v: float, label: str, stroke: str, dash: str = "") -> str:
        yy = y(v)
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<line x1="{left}" y1="{yy:.2f}" x2="{right}" y2="{yy:.2f}" '
                f'stroke="{stroke}" stroke-width="2"{dash_attr}/>'
                f'<text x="{right-4}" y="{yy-5:.2f}" text-anchor="end" class="level">{escape(label)} {v:.5f}</text>')

    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>text{font-family:Arial,sans-serif;fill:#e8edf3}.title{font-size:20px;font-weight:700}.sub{font-size:12px;fill:#9ba8b7}.axis{font-size:11px;fill:#aeb8c4}.level{font-size:11px;paint-order:stroke;stroke:#101720;stroke-width:3px;stroke-linejoin:round}.grid{stroke:#2a3543;stroke-width:1}</style>',
        '<rect width="100%" height="100%" fill="#101720"/>',
        f'<text x="{left}" y="32" class="title">Fimathe \u00b7 {escape(symbol)} \u00b7 {escape(timeframe)}</text>',
        '<text x="88" y="52" class="sub">Candles reconstructed from extracted OHLC; not a pixel overlay on the original screenshot</text>',
    ]
    for i in range(6):
        v = pmin + (pmax - pmin) * i / 5
        yy = y(v)
        pieces.append(f'<line x1="{left}" y1="{yy:.2f}" x2="{right}" y2="{yy:.2f}" class="grid"/>')
        pieces.append(f'<text x="{left-10}" y="{yy+4:.2f}" text-anchor="end" class="axis">{v:.5f}</text>')

    pieces.append(f'<rect x="{left}" y="{y(channel_upper):.2f}" width="{plot_w}" height="{max(1, y(channel_lower)-y(channel_upper)):.2f}" fill="#2d7dd2" opacity="0.13"/>')
    pieces.append(f'<rect x="{left}" y="{y(neutral_upper):.2f}" width="{plot_w}" height="{max(1, y(neutral_lower)-y(neutral_upper)):.2f}" fill="#e0a82e" opacity="0.12"/>')
    pieces += [
        line(channel_upper, "CANAL H", "#53a6ff"),
        line(channel_lower, "CANAL L", "#53a6ff"),
        line(neutral_upper, "ZONA NEUTRA H", "#e0a82e", "6 4"),
        line(neutral_lower, "ZONA NEUTRA L", "#e0a82e", "6 4"),
        line(level_50, "50% CANAL", "#c6a0ff", "3 4"),
    ]
    n = len(candles)
    step = plot_w / n
    body_w = max(2.0, min(14.0, step * 0.58))
    for i, c in enumerate(candles):
        x = left + step * (i + 0.5)
        color = "#28c995" if c["close"] >= c["open"] else "#ff6b75"
        pieces.append(f'<line x1="{x:.2f}" y1="{y(c["high"]):.2f}" x2="{x:.2f}" y2="{y(c["low"]):.2f}" stroke="{color}" stroke-width="1.4"/>')
        y1, y2 = y(c["open"]), y(c["close"])
        rect_y, rect_h = min(y1, y2), max(1.5, abs(y2 - y1))
        pieces.append(f'<rect x="{x-body_w/2:.2f}" y="{rect_y:.2f}" width="{body_w:.2f}" height="{rect_h:.2f}" fill="{color}" stroke="{color}"/>')
    pieces += [
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#8491a0"/>',
        f'<text x="{left}" y="{height-20}" class="sub">Mais antigo</text>',
        f'<text x="{right}" y="{height-20}" text-anchor="end" class="sub">Mais recente</text>',
        '<text x="88" y="66" class="sub">Verifique pre\u00e7os e limites estimados contra o print original antes de usar.</text>',
        '</svg>',
    ]
    return "\n".join(pieces)
