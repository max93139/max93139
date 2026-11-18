#!/usr/bin/env python3
"""Render the project cards in assets/cards/ as SVG, in a dark and a light variant.

Edit PROJECTS below and run `python3 scripts/build_cards.py`. GitHub strips CSS from
README markdown but keeps it inside SVG images, which is why the cards are images.
"""

from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "cards"
W, H = 460, 262
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "dark": {"bg": "#0d1117", "panel": "#161b22", "border": "#30363d", "title": "#f0f6fc",
             "text": "#c9d1d9", "muted": "#8b949e", "chip": "#21262d", "chip_text": "#c9d1d9"},
    "light": {"bg": "#ffffff", "panel": "#f6f8fa", "border": "#d0d7de", "title": "#1f2328",
              "text": "#31363c", "muted": "#59636e", "chip": "#eaeef2", "chip_text": "#31363c"},
}

PROJECTS = [
    {
        "slug": "delivery", "title": "Delivery Admin Panel", "accent": ("#f97316", "#facc15"),
        "badge": "INT20H 2026", "summary": "B2B logistics admin with regional tax-jurisdiction rules and streaming CSV/PDF imports.",
        "metrics": [("11 / 84", "hackathon place"), ("24 h", "build sprint")],
        "role": "Frontend lead", "stack": ["NestJS", "React", "PostgreSQL", "Prisma", "Turborepo"],
    },
    {
        "slug": "hotspot", "title": "Hotspot Harmony", "accent": ("#ef4444", "#f59e0b"),
        "badge": "NASA Space Apps 2026", "summary": "One comparable record of MODIS + VIIRS satellite fire detections, with a burning calendar and a 3D globe.",
        "metrics": [("4.3–8.0%", "calibration WAPE"), ("348", "pytest + Vitest tests")],
        "role": "Team lead · React / MapLibre app", "stack": ["Python", "FastAPI", "DuckDB", "React", "MapLibre"],
    },
    {
        "slug": "aev", "title": "Automated Estate Valuation", "accent": ("#22c55e", "#14b8a6"),
        "badge": "Featured by KNU", "summary": "Real-estate valuation SaaS: map analytics, data pipelines and PDF valuation reports.",
        "metrics": [("13.8%", "MdAPE, was 25.2%"), ("ONNX + H3", "CatBoost booster")],
        "role": "Main developer · team of 2", "stack": ["NestJS", "React", "Leaflet", "PostGIS", "CatBoost"],
    },
    {
        "slug": "shop", "title": "Shop AI Manager", "accent": ("#a855f7", "#ec4899"),
        "badge": "E-commerce", "summary": "Telegram bot storefront (grammY) and a Next.js admin in one Turborepo monorepo.",
        "metrics": [("Monobank", "signed webhooks"), ("Nova Poshta", "API waybills"), ("E2E", "tests in CI")],
        "role": "Solo project", "stack": ["NestJS", "Next.js", "grammY", "Prisma", "Turborepo"],
    },
    {
        "slug": "social", "title": "Social Network", "accent": ("#3b82f6", "#06b6d4"),
        "badge": "Real-time", "summary": "Messenger with voice messages, swipe-to-reply, Redis throttling and encrypted key envelopes.",
        "metrics": [("85+", "Vitest + E2E tests"), ("WebSockets", "Socket.io + Redis")],
        "role": "Real-time chat on the web client", "stack": ["Next.js", "NestJS", "Socket.io", "Redis", "PostgreSQL"],
    },
    {
        "slug": "car", "title": "Car Parser & Alerts", "accent": ("#0ea5e9", "#6366f1"),
        "badge": "Data pipeline", "summary": "Watches the used-car market: deduplication, reseller detection and instant Telegram alerts.",
        "metrics": [("519", "pytest tests"), ("CI", "push · PR · schedule")],
        "role": "Solo project", "stack": ["Python", "Playwright", "Neon Postgres", "Telegram"],
    },
    {
        "slug": "cryptarc", "title": "CryptArc", "accent": ("#8b5cf6", "#22d3ee"),
        "badge": "Algorithms", "summary": "Encrypting archiver where every codec is hand-written: Huffman, LZSS, Deflate, BWT, LZW, arithmetic.",
        "metrics": [("8", "hand-written codecs"), ("600+", "xUnit tests"), ("AES-GCM", "+ Argon2id")],
        "role": "Avalonia UI · core fixes · benchmarks", "stack": ["C#", ".NET 10", "Avalonia", "xUnit"],
    },
]


def wrap(text, limit):
    lines, line = [], ""
    for word in text.split():
        if len(line) + len(word) + 1 > limit and line:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + [line] if line else lines


def text_width(s, size):
    return len(s) * size * 0.56


def card(p, t):
    a1, a2 = p["accent"]
    gid = f"g-{p['slug']}"
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(p["title"])}">',
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{a1}"/><stop offset="1" stop-color="{a2}"/></linearGradient></defs>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="5" rx="2.5" fill="url(#{gid})"/>',
        f'<text x="22" y="40" font-family="{FONT}" font-size="19" font-weight="700" fill="{t["title"]}">{escape(p["title"])}</text>',
    ]
    bw = text_width(p["badge"], 11) + 18
    out += [
        f'<rect x="{W - 22 - bw:.0f}" y="24" width="{bw:.0f}" height="22" rx="11" fill="url(#{gid})" opacity="0.18"/>',
        f'<text x="{W - 22 - bw / 2:.0f}" y="39" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="{a1}">{escape(p["badge"])}</text>',
    ]
    for i, line in enumerate(wrap(p["summary"], 62)[:2]):
        out.append(f'<text x="22" y="{70 + i * 19}" font-family="{FONT}" font-size="13" fill="{t["text"]}">{escape(line)}</text>')

    n = len(p["metrics"])
    gap = 10
    mw = (W - 44 - gap * (n - 1)) / n
    for i, (value, label) in enumerate(p["metrics"]):
        x = 22 + i * (mw + gap)
        size = 22 if text_width(value, 22) < mw - 20 else 16
        out += [
            f'<rect x="{x:.0f}" y="108" width="{mw:.0f}" height="62" rx="10" fill="{t["panel"]}" stroke="{t["border"]}"/>',
            f'<text x="{x + 12:.0f}" y="138" font-family="{FONT}" font-size="{size}" font-weight="800" fill="url(#{gid})">{escape(value)}</text>',
            f'<text x="{x + 12:.0f}" y="158" font-family="{FONT}" font-size="11" fill="{t["muted"]}">{escape(label)}</text>',
        ]

    out.append(f'<text x="22" y="198" font-family="{FONT}" font-size="12" fill="{t["muted"]}">Role · <tspan fill="{t["text"]}" font-weight="600">{escape(p["role"])}</tspan></text>')

    x = 22
    for tech in p["stack"]:
        cw = text_width(tech, 11.5) + 16
        if x + cw > W - 22:
            break
        out += [
            f'<rect x="{x:.0f}" y="218" width="{cw:.0f}" height="26" rx="6" fill="{t["chip"]}"/>',
            f'<text x="{x + cw / 2:.0f}" y="235" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{t["chip_text"]}">{escape(tech)}</text>',
        ]
        x += cw + 7
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for p in PROJECTS:
        for name, theme in THEMES.items():
            (OUT / f"{p['slug']}-{name}.svg").write_text(card(p, theme), encoding="utf-8")
    print(f"{len(PROJECTS) * len(THEMES)} cards written to {OUT}")


if __name__ == "__main__":
    main()
