"""Generates the animated SVGs for the profile README, in light and dark.

SVGs in a GitHub README render as <img>: CSS and SMIL animations run, scripts and web fonts don't.
Run: python build_svgs.py
"""

import math

THEMES = {
    "light": dict(bg="#f3f5f7", panel="#ffffff", ink="#14213d", ink2="#4a5873", rule="#c3ccd8",
                  ok="#1f7a5c", bad="#b42318", hold="#a15c00", chip="#e3ecf5", term="#0f1726",
                  tink="#e6ebf3", tink2="#8e9bb3"),
    "dark": dict(bg="#0f1726", panel="#162033", ink="#e6ebf3", ink2="#a3b0c6", rule="#3a4a68",
                 ok="#4cc198", bad="#f0806f", hold="#e6a54a", chip="#213152", term="#0a101c",
                 tink="#e6ebf3", tink2="#7d8aa3"),
}
SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"
DUR = 10  # seconds per loop


def cubic_len(p0, p1, p2, p3, n=200):
    def pt(t):
        u = 1 - t
        return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])
    pts = [pt(i / n) for i in range(n + 1)]
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def hero(c: dict) -> str:
    y = 236
    names = ["intake", "gather", "classify", "draft", "verify", "decide"]
    xs = [70 + i * 122 for i in range(6)]  # left edge of each pill
    w = 98
    cx = {n: x + w / 2 for n, x in zip(names, xs)}
    done_x = 70 + 6 * 122
    done_cx = done_x + 49
    yt = y + 34  # track the dispute rides on, under the pills

    # packet path: intake -> verify, loop back to draft, draft -> verify, verify -> done
    a, d, v = cx["intake"], cx["draft"], cx["verify"]
    arc = ((v, yt), (v, yt + 52), (d, yt + 52), (d, yt))
    s1 = v - a
    s2 = cubic_len(*arc)
    s3 = v - d
    s4 = done_cx - v
    total = s1 + s2 + s3 + s4
    path = (f"M{a} {yt} L{v} {yt} C{v} {yt + 52} {d} {yt + 52} {d} {yt} L{v} {yt} L{done_cx} {yt}")
    k = [0, s1 / total, (s1 + s2) / total, (s1 + s2 + s3) / total, 1]
    # time:   start  leave  reach verify  hold(reject)  back at draft  verify again  hold(pass)  done   hold
    times = [0, 0.04, 0.30, 0.42, 0.52, 0.58, 0.68, 0.82, 1]
    points = [0, 0, k[1], k[1], k[2], k[3], k[3], 1, 1]
    kt = ";".join(f"{t:.3f}" for t in times)
    kp = ";".join(f"{p:.4f}" for p in points)

    def blink(on: float, off: float, attr="opacity", vals=("0", "1")) -> str:
        # visible between on and off within each loop
        return (f'<animate attributeName="{attr}" dur="{DUR}s" repeatCount="indefinite" calcMode="discrete" '
                f'keyTimes="0;{on};{off}" values="{vals[0]};{vals[1]};{vals[0]}"/>')

    pills = []
    for n, x in zip(names, xs):
        extra = ""
        if n == "verify":
            extra = (f'<animate attributeName="stroke" dur="{DUR}s" repeatCount="indefinite" calcMode="discrete" '
                     f'keyTimes="0;0.30;0.42;0.58;0.68" values="{c["ink2"]};{c["bad"]};{c["ink2"]};{c["ok"]};{c["ink2"]}"/>'
                     f'<animate attributeName="stroke-width" dur="{DUR}s" repeatCount="indefinite" calcMode="discrete" '
                     f'keyTimes="0;0.30;0.42;0.58;0.68" values="1.5;2.5;1.5;2.5;1.5"/>')
        pills.append(f'<rect x="{x}" y="{y - 17}" width="{w}" height="34" rx="17" fill="{c["panel"]}" '
                     f'stroke="{c["ink2"]}" stroke-width="1.5">{extra}</rect>'
                     f'<text x="{x + w / 2}" y="{y + 5}" text-anchor="middle" font-size="14" fill="{c["ink2"]}">{n}</text>')
    arrows = "".join(
        f'<line x1="{x + w + 4}" y1="{y}" x2="{x + 118}" y2="{y}" stroke="{c["rule"]}" stroke-width="1.5" marker-end="url(#ar)"/>'
        for x in xs)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 384" width="960" height="384" font-family="{SANS}" role="img" aria-label="Shahabaj Sheikh, forward-deployed AI engineer. Animation: a dispute moves through an agent's states; a fabricated amount is rejected at verify, redrafted, verified and shipped with zero fabrications.">
  <defs>
    <marker id="ar" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8z" fill="{c["rule"]}"/></marker>
    <marker id="ah" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8z" fill="{c["hold"]}"/></marker>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>
    <radialGradient id="au1" cx="0.15" cy="0.1" r="0.6">
      <stop offset="0" stop-color="{c["ok"]}" stop-opacity="0.28"/><stop offset="1" stop-color="{c["ok"]}" stop-opacity="0"/>
      <animate attributeName="cx" dur="16s" repeatCount="indefinite" values="0.15;0.55;0.15"/>
    </radialGradient>
    <radialGradient id="au2" cx="0.9" cy="0.0" r="0.55">
      <stop offset="0" stop-color="#6d5dfc" stop-opacity="0.22"/><stop offset="1" stop-color="#6d5dfc" stop-opacity="0"/>
      <animate attributeName="cx" dur="20s" repeatCount="indefinite" values="0.9;0.5;0.9"/>
    </radialGradient>
    <clipPath id="card"><rect width="960" height="384" rx="14"/></clipPath>
  </defs>
  <g clip-path="url(#card)">
    <rect width="960" height="384" fill="{c["bg"]}"/>
    <rect width="960" height="384" fill="url(#au1)"/>
    <rect width="960" height="384" fill="url(#au2)"/>
  </g>

  <text x="70" y="86" font-family="{SERIF}" font-size="46" font-weight="700" fill="{c["ink"]}">Shahabaj Sheikh</text>
  <text x="70" y="124" font-size="20" font-weight="700" fill="{c["ok"]}">Forward Deployed Engineer &amp; AI Solution Architect at DevRev</text>
  <text x="70" y="152" font-size="18" fill="{c["ink2"]}">Agentic systems from discovery to production, where a wrong answer has a cost.</text>
  <line x1="70" y1="176" x2="890" y2="176" stroke="{c["rule"]}"/>

  {arrows}
  {"".join(pills)}

  <!-- retry arc -->
  <line x1="{a}" y1="{yt}" x2="{done_cx}" y2="{yt}" stroke="{c["rule"]}" stroke-width="1" stroke-dasharray="2 4" opacity="0.7"/>
  <path d="M{v} {yt} C{v} {yt + 52} {d} {yt + 52} {d} {yt + 2}" fill="none" stroke="{c["hold"]}" stroke-width="1.5" stroke-dasharray="4 5" marker-end="url(#ah)" opacity="0.6"/>
  <text x="{(v + d) / 2}" y="{yt + 58}" text-anchor="middle" font-size="12" fill="{c["hold"]}" opacity="0.85">rejected, redraft</text>

  <!-- done pill -->
  <g>
    <rect x="{done_x}" y="{y - 22}" width="98" height="44" rx="22" fill="{c["ok"]}" filter="url(#glow)" opacity="0">
      {blink(0.82, 0.995)}
    </rect>
    <rect x="{done_x}" y="{y - 17}" width="98" height="34" rx="17" fill="{c["ok"]}"/>
    <text x="{done_cx}" y="{y + 5}" text-anchor="middle" font-size="14" font-weight="700" fill="{c["bg"]}">shipped</text>
  </g>

  <!-- verifier callouts -->
  <g opacity="0">
    {blink(0.30, 0.44)}
    <rect x="{v - 112}" y="{y - 74}" width="224" height="40" rx="6" fill="{c["panel"]}" stroke="{c["bad"]}"/>
    <text x="{v}" y="{y - 57}" text-anchor="middle" font-size="12.5" font-weight="700" fill="{c["bad"]}">✕ ₹14,041 not on any cited record</text>
    <text x="{v}" y="{y - 41}" text-anchor="middle" font-size="11.5" fill="{c["ink2"]}">verifier blocks the note</text>
  </g>
  <g opacity="0">
    {blink(0.58, 0.72)}
    <rect x="{v - 112}" y="{y - 74}" width="224" height="40" rx="6" fill="{c["panel"]}" stroke="{c["ok"]}"/>
    <text x="{v}" y="{y - 57}" text-anchor="middle" font-size="12.5" font-weight="700" fill="{c["ok"]}">✓ 4 sentences, every value cited</text>
    <text x="{v}" y="{y - 41}" text-anchor="middle" font-size="11.5" fill="{c["ink2"]}">draft 2 passes</text>
  </g>

  <!-- the dispute moving through -->
  <g>
    <animateMotion dur="{DUR}s" repeatCount="indefinite" calcMode="linear" keyTimes="{kt}" keyPoints="{kp}" path="{path}"/>
    <circle r="7" cx="0" cy="0" fill="{c["ink"]}">
      <animate attributeName="fill" dur="{DUR}s" repeatCount="indefinite" calcMode="discrete"
               keyTimes="0;0.30;0.52;0.82" values="{c["ink"]};{c["bad"]};{c["ink"]};{c["ok"]}"/>
    </circle>
    <text x="12" y="4" font-size="11" font-family="{MONO}" fill="{c["ink"]}">D005</text>
  </g>

  <text x="70" y="{yt + 92}" font-size="12" fill="{c["ink2"]}">One dispute through the agent in <tspan font-weight="700">grounded-triage</tspan>, replayed from the 40% fabrication eval run.</text>
</svg>
'''


TRACE = [
    ("$", "python -m grounded_triage run D005 --fabricate 0.4", "cmd"),
    ("", "intake           transaction found", ""),
    ("", "gather_evidence  5 records gathered", ""),
    ("", "classify         duplicate_charge @ 0.95: 1 same-amount charge(s) at the same merchant within 3 days", ""),
    ("", "draft            draft attempt 1", ""),
    ("", "verify           rejected: value_mismatch: amount 14041 not on any cited record", "bad"),
    ("", "draft            draft attempt 2", ""),
    ("", "verify           rejected: value_mismatch: amount 14041 not on any cited record", "bad"),
    ("", "draft            draft attempt 3", ""),
    ("", "verify           unknown_record: cites txn:T00045-R", "bad"),
    ("", "escalate         queued for analyst: draft failed verification after retries", "hold"),
    ("", "done             escalate", ""),
    ("", "", ""),
    ("", "action    escalate   (expected provisional_credit)", "hold"),
]


def terminal(c: dict) -> str:
    """Lines appear one by one, hold, then the loop restarts."""
    n = len(TRACE)
    loop = 13.0
    step = 0.6
    lines = []
    for i, (prompt, text, kind) in enumerate(TRACE):
        on = (0.4 + i * step) / loop
        col = {"bad": c["bad"], "ok": c["ok"], "hold": c["hold"], "cmd": c["tink"]}.get(kind, c["tink2"])
        y = 62 + i * 21
        p = f'<tspan fill="{c["ok"]}">{prompt} </tspan>' if prompt else ""
        lines.append(
            f'<text x="28" y="{y}" font-family="{MONO}" font-size="12.5" fill="{col}" xml:space="preserve">'
            f'{p}{text}'
            f'<animate attributeName="opacity" dur="{loop}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="0;{on:.3f};0.96" values="0;1;0"/></text>'
        )
    h = 62 + n * 21 + 6
    cursor_y = 62 + (n - 1) * 21
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 {h}" width="920" height="{h}" role="img" aria-label="Terminal replay of grounded-triage on dispute D005 with 40% fabrication: three drafts fail verification, so no note ships and the case goes to an analyst.">
  <rect width="920" height="{h}" rx="10" fill="{c["term"]}"/>
  <rect width="920" height="34" rx="10" fill="{c["term"]}"/>
  <line x1="0" y1="34" x2="920" y2="34" stroke="#ffffff" stroke-opacity="0.08"/>
  <circle cx="22" cy="17" r="5.5" fill="#ffffff" fill-opacity="0.18"/>
  <circle cx="40" cy="17" r="5.5" fill="#ffffff" fill-opacity="0.18"/>
  <circle cx="58" cy="17" r="5.5" fill="#ffffff" fill-opacity="0.18"/>
  <text x="460" y="22" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="{c["tink2"]}">grounded-triage</text>
  {"".join(lines)}
  <rect x="28" y="{cursor_y + 8}" width="9" height="3" fill="{c["tink"]}">
    <animate attributeName="opacity" dur="1s" repeatCount="indefinite" values="1;0;1"/>
  </rect>
</svg>
'''


PHASES = [
    ("Discovery", ("volumes, error budgets,", "who signs off")),
    ("Build + eval", ("labelled history,", "gates written in the SOW")),
    ("Shadow", ("runs on live cases,", "analysts don't see it")),
    ("Assist", ("analysts accept,", "edit or override")),
    ("Automate", ("one category", "at a time")),
]


def phases(c: dict) -> str:
    loop = 9.0
    w = 960
    seg = (w - 140) / len(PHASES)
    parts = []
    for i, (name, note) in enumerate(PHASES):
        x = 70 + i * seg
        on = (0.3 + i * 1.2) / loop
        parts.append(f'''
  <g>
    <circle cx="{x + 8}" cy="58" r="8" fill="{c["panel"]}" stroke="{c["ink2"]}" stroke-width="1.5">
      <animate attributeName="fill" dur="{loop}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{on:.3f};0.97" values="{c["panel"]};{c["ok"]};{c["panel"]}"/>
      <animate attributeName="stroke" dur="{loop}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{on:.3f};0.97" values="{c["ink2"]};{c["ok"]};{c["ink2"]}"/>
    </circle>
    <text x="{x}" y="98" font-size="16" font-weight="700" fill="{c["ink"]}">{name}</text>
    <text x="{x}" y="120" font-size="12.5" fill="{c["ink2"]}">{note[0]}</text>
    <text x="{x}" y="138" font-size="12.5" fill="{c["ink2"]}">{note[1]}</text>
  </g>''')
    end = 70 + (len(PHASES) - 1) * seg + 8
    fill_to = (0.3 + (len(PHASES) - 1) * 1.2) / loop
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 160" width="{w}" height="160" font-family="{SANS}" role="img" aria-label="How an engagement runs: discovery, build and eval, shadow mode, assist, then automate one category at a time. Each phase is gated on numbers.">
  <rect width="{w}" height="160" rx="14" fill="{c["bg"]}"/>
  <text x="70" y="30" font-size="12.5" fill="{c["ink2"]}">How an engagement runs. Each step is gated on numbers, not dates.</text>
  <line x1="78" y1="58" x2="{end}" y2="58" stroke="{c["rule"]}" stroke-width="2"/>
  <line x1="78" y1="58" x2="78" y2="58" stroke="{c["ok"]}" stroke-width="2.5">
    <animate attributeName="x2" dur="{loop}s" repeatCount="indefinite" keyTimes="0;0.033;{fill_to:.3f};0.97;1" values="78;78;{end};{end};78"/>
  </line>
  {"".join(parts)}
</svg>
'''


import json

STACK = json.load(open("stack.json"))


def stack(c: dict) -> str:
    """Categorised icon wall. Tiles rise in row by row; a light sweep crosses each row."""
    tile, gap, label_w = 74, 14, 150
    rows = len(STACK)
    row_h = tile + 40
    w = 960
    h = 20 + rows * row_h
    loop = 12.0
    out = [f'<defs><linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0"/>'
           f'<stop offset="0.5" stop-color="#ffffff" stop-opacity="0.10"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient></defs>']
    k = 0
    for r, row in enumerate(STACK):
        y0 = 14 + r * row_h
        out.append(f'<text x="24" y="{y0 + tile / 2 + 5}" font-size="14" font-weight="700" fill="{c["ink"]}">{row["cat"]}</text>')
        out.append(f'<line x1="24" y1="{y0 + tile / 2 + 16}" x2="{label_w - 20}" y2="{y0 + tile / 2 + 16}" stroke="{c["ok"]}" stroke-width="2"/>')
        for i, it in enumerate(row["items"]):
            x = label_w + i * (tile + gap + 120)
            on = (0.2 + k * 0.18) / loop
            k += 1
            hexc = it["hex"].lower()
            fill = c["ink"] if hexc in ("000000", "191919", "222222") else "#" + hexc
            glyph = (f'<g transform="translate({x + tile / 2 - 18} {y0 + tile / 2 - 18}) scale(1.5)"><path d="{it["path"]}" fill="{fill}"/></g>'
                     if it["path"] else
                     f'<text x="{x + tile / 2}" y="{y0 + tile / 2 + 6}" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" fill="{c["ok"]}">LGBM</text>')
            out.append(f"""
  <g>
    <animate attributeName="opacity" dur="{loop}s" repeatCount="indefinite" keyTimes="0;{on:.3f};{on + 0.04:.3f};0.97;1" values="0;0;1;1;0"/>
    <animateTransform attributeName="transform" type="translate" dur="{loop}s" repeatCount="indefinite" keyTimes="0;{on:.3f};{on + 0.04:.3f};1" values="0 10;0 10;0 0;0 0"/>
    <rect x="{x}" y="{y0}" width="{tile}" height="{tile}" rx="18" fill="{c["panel"]}" stroke="{c["rule"]}"/>
    {glyph}
    <text x="{x + tile + 14}" y="{y0 + tile / 2 + 5}" font-size="14" fill="{c["ink2"]}">{it["label"]}</text>
  </g>""")

    names = ", ".join(it["label"] for row in STACK for it in row["items"])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{SANS}" role="img" aria-label="Stack: {names}">
  <rect width="{w}" height="{h}" rx="14" fill="{c["bg"]}"/>
  {"".join(out)}
</svg>
"""


# Industries. Client names stay out; only the industry and the kind of work.
INDUSTRIES = [
    ("plane", "Airline", ["Deterministic 14-state orchestrator,", "21 skills across CRM, reservations,", "payments and messaging"], "production-grade"),
    ("bank", "Banking", ["Fraud investigation; every finding", "cited to its source record;", "zero fabrications at scale"], "production-grade"),
    ("card", "Fintech", ["Service-ops automation for IT, HR,", "finance and promo workflows,", "humans keep the approvals"], "production-grade"),
    ("box", "Consumer goods", ["Vendor share, beat-plan adherence,", "GST cost modelling and route", "optimisation workflows"], "production-grade"),
    ("car", "Automotive", ["LightGBM demand forecasting,", "taken through staged delivery"], "production-grade"),
    ("scale", "Legal", ["Founded Legit.ai, a multi-model", "AI platform for lawyers, sold to", "paying customers"], "founder"),
]

GLYPHS = {
    # simple line icons on a 24x24 grid
    "plane": "M2 14l20-7-6 13-4-5-5 3 1-5z",
    "bank": "M3 9l9-5 9 5M5 10v7M9.5 10v7M14.5 10v7M19 10v7M3 20h18",
    "card": "M3 6h18v12H3zM3 10h18M7 15h4",
    "box": "M3 7l9-4 9 4v10l-9 4-9-4zM3 7l9 4 9-4M12 11v10",
    "car": "M4 16v-4l2-5h12l2 5v4M4 16h16M7 16v2M17 16v2M7 12h0M17 12h0M6 12h12",
    "scale": "M12 3v18M6 21h12M4 8h16M4 8l-2 6h6zM20 8l-2 6h6zM12 3l-8 5M12 3l8 5",
}


def industries(c: dict) -> str:
    cols, card_w, card_h, gap = 3, 290, 150, 20
    w = 960
    rows = (len(INDUSTRIES) + cols - 1) // cols
    h = 30 + rows * (card_h + gap)
    loop = 10.0
    out = []
    for i, (g, name, lines, tag) in enumerate(INDUSTRIES):
        x = 24 + (i % cols) * (card_w + gap)
        y = 14 + (i // cols) * (card_h + gap)
        on = (0.2 + i * 0.25) / loop
        accent = c["ok"] if tag == "production-grade" else "#6d5dfc"
        tw = 16 + len(tag) * 7.2
        out.append(f"""
  <g>
    <animate attributeName="opacity" dur="{loop}s" repeatCount="indefinite" keyTimes="0;{on:.3f};{on + 0.05:.3f};0.97;1" values="0;0;1;1;0"/>
    <animateTransform attributeName="transform" type="translate" dur="{loop}s" repeatCount="indefinite" keyTimes="0;{on:.3f};{on + 0.05:.3f};1" values="0 12;0 12;0 0;0 0"/>
    <rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="14" fill="{c["panel"]}" stroke="{c["rule"]}"/>
    <circle cx="{x + 38}" cy="{y + 40}" r="22" fill="{accent}" fill-opacity="0.14"/>
    <g transform="translate({x + 26} {y + 28})"><path d="{GLYPHS[g]}" fill="none" stroke="{accent}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></g>
    <text x="{x + 74}" y="{y + 36}" font-size="17" font-weight="700" fill="{c["ink"]}">{name}</text>
    {"".join(f'<text x="{x + 74}" y="{y + 58 + j * 17}" font-size="12" fill="{c["ink2"]}">{t}</text>' for j, t in enumerate(lines))}
    <rect x="{x + 74}" y="{y + 112}" width="{tw}" height="22" rx="11" fill="{accent}" fill-opacity="0.16"/>
    <circle cx="{x + 84}" cy="{y + 123}" r="3.5" fill="{accent}">
      <animate attributeName="r" dur="2s" repeatCount="indefinite" values="3.5;5;3.5"/>
      <animate attributeName="fill-opacity" dur="2s" repeatCount="indefinite" values="1;0.4;1"/>
    </circle>
    <text x="{x + 94}" y="{y + 127.5}" font-size="11.5" font-weight="700" fill="{accent}">{tag}</text>
  </g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{SANS}" role="img" aria-label="Production-grade work by industry. Airline: deterministic 14-state orchestrator with 21 skills across CRM, reservations, payments and messaging. Banking: fraud investigation with every finding cited to its record, zero fabrications across thousands of transactions. Fintech: service-operations automation with human approvals. Consumer goods: vendor share, beat-plan adherence, GST cost modelling and route optimisation. Automotive: LightGBM demand forecasting. Legal: founded Legit.ai.">
  <rect width="{w}" height="{h}" rx="14" fill="{c["bg"]}"/>
  {"".join(out)}
</svg>
"""


METRICS = [
    (14, "", "years in enterprise software"),
    (21, "", "skills in one orchestrator"),
    (0, "", "fabrications, thousands of txns"),
    (6, "", "industries in production"),
]


def metrics(c: dict) -> str:
    w, h = 960, 116
    loop = 12.0
    seg = (w - 48) / len(METRICS)
    out = []
    for i, (n, suffix, label) in enumerate(METRICS):
        x = 24 + i * seg + 20
        frames = sorted(set([0, round(n * 0.25), round(n * 0.5), round(n * 0.75), n])) if n else [0]
        start = (0.3 + i * 0.4) / loop
        stepf = 0.07 / loop * 10
        color = c["ok"] if i == 2 else c["ink"]
        for j, v in enumerate(frames):
            t_on = start + j * stepf / len(frames)
            last = j == len(frames) - 1
            t_off = 0.97 if last else start + (j + 1) * stepf / len(frames)
            base = "1" if last else "0"
            out.append(f'<text x="{x}" y="58" font-family="{SERIF}" font-size="42" font-weight="700" fill="{color}" opacity="{base}">{v:,}<tspan font-size="22" fill="{c["ink2"]}">{suffix}</tspan>'
                       f'<animate attributeName="opacity" dur="{loop}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{t_on:.4f};{t_off:.4f}" values="0;1;0"/></text>')
        out.append(f'<text x="{x}" y="86" font-size="13" fill="{c["ink2"]}">{label}</text>')
        if i:
            out.append(f'<line x1="{24 + i * seg}" y1="22" x2="{24 + i * seg}" y2="94" stroke="{c["rule"]}"/>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{SANS}" role="img" aria-label="14 years in enterprise software; 21 skills in one production orchestrator; zero fabrications across thousands of transactions; 6 industries in production.">
  <rect width="{w}" height="{h}" rx="14" fill="{c["bg"]}"/>
  {"".join(out)}
</svg>
"""


CODE = [
    [("kw", "class "), ("cls", "Shahabaj"), ("p", "("), ("cls", "ForwardDeployedEngineer"), ("p", "):")],
    [("p", "    based_in  = "), ("str", '"Gurugram, India"')],
    [("p", "    role      = "), ("str", '"Forward Deployed Engineer"')],
    [("p", "    also      = "), ("str", '"AI Solution Architect"')],
    [("p", "    at        = "), ("str", '"DevRev"')],
    [("p", "    years     = "), ("num", "14")],
    [("p", "    domains   = ["), ("str", '"airline"'), ("p", ", "), ("str", '"banking"'), ("p", ", "), ("str", '"fintech"'), ("p", ", "), ("str", '"pricing"'), ("p", "]")],
    [("p", "    speaks    = ["), ("str", '"English"'), ("p", ", "), ("str", '"Hindi"'), ("p", ", "), ("str", '"Bengali"'), ("p", "]")],
    [],
    [("kw", "    def "), ("fn", "engage"), ("p", "(self, client):")],
    [("p", "        problem = self."), ("fn", "discover"), ("p", "(client)")],
    [("p", "        agent = self."), ("fn", "build"), ("p", "(problem)")],
    [("kw", "        while not "), ("p", "self."), ("fn", "evals"), ("p", "(agent)."), ("fn", "meet"), ("p", "(client.gates):")],
    [("p", "            agent = self."), ("fn", "improve"), ("p", "(agent)")],
    [("kw", "        return "), ("p", "self."), ("fn", "ship"), ("p", "(agent, mode="), ("str", '"shadow"'), ("p", ")")],
]


def code_card(c: dict) -> str:
    col = {"kw": "#c792ea", "cls": "#ffcb6b", "fn": "#82aaff", "str": "#c3e88d", "num": "#f78c6c", "p": c["tink"]}
    loop = 16.0
    w, lh = 560, 22
    h = 52 + len(CODE) * lh + 14
    rows = []
    for i, toks in enumerate(CODE):
        y = 60 + i * lh
        on = (0.3 + i * 0.35) / loop
        spans = "".join(f'<tspan fill="{col[k]}">{t.replace("<", "&lt;")}</tspan>' for k, t in toks)
        rows.append(f'<text x="52" y="{y}" font-family="{MONO}" font-size="13" xml:space="preserve">{spans}'
                    f'<animate attributeName="opacity" dur="{loop}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{on:.3f};0.97" values="0;1;0"/></text>'
                    f'<text x="22" y="{y}" font-family="{MONO}" font-size="12" fill="{c["tink2"]}" opacity="0.6">{i + 1}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="About me, written as a Python class: based in Gurugram, Forward Deployed Engineer and AI Solution Architect at DevRev, 14 years, airline, banking, fintech and pricing; engages by discovering, building, iterating until evals pass the client's gates, then shipping in shadow mode.">
  <rect width="{w}" height="{h}" rx="10" fill="{c["term"]}"/>
  <line x1="0" y1="34" x2="{w}" y2="34" stroke="#ffffff" stroke-opacity="0.08"/>
  <circle cx="22" cy="17" r="5.5" fill="#ffffff" fill-opacity="0.18"/>
  <circle cx="40" cy="17" r="5.5" fill="#ffffff" fill-opacity="0.18"/>
  <circle cx="58" cy="17" r="5.5" fill="#ffffff" fill-opacity="0.18"/>
  <text x="{w / 2}" y="22" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="{c["tink2"]}">about_me.py</text>
  {"".join(rows)}
</svg>
'''


def project_card(c: dict, kind: str) -> str:
    w, h = 560, 200
    if kind == "triage":
        title, sub = "grounded-triage", "State-machine agent for bank card-dispute triage"
        loop = 8.0
        bars = []
        for i, (label, val, color) in enumerate([("fabrications injected", 36, c["bad"]), ("caught by verifier", 36, c["hold"]), ("unverified notes shipped", 0, c["ok"])]):
            y = 92 + i * 26
            full = 300 * val / 36
            bars.append(f'''
  <text x="24" y="{y + 11}" font-size="12.5" fill="{c["ink2"]}">{label}</text>
  <rect x="200" y="{y}" width="300" height="14" rx="7" fill="{c["chip"]}"/>
  <rect x="200" y="{y}" width="{full}" height="14" rx="7" fill="{color}">
    <animate attributeName="width" dur="{loop}s" repeatCount="indefinite" keyTimes="0;{0.05 + i * 0.12:.2f};{0.25 + i * 0.12:.2f};0.95;1" values="0;0;{full};{full};0"/>
  </rect>
  <text x="{510}" y="{y + 11}" font-size="13" font-weight="700" fill="{color}">{val}</text>''')
        body = "".join(bars)
        tags = ["Python", "React + TypeScript", "live dashboard"]
    else:
        title, sub = "Legit.ai", "Multi-model AI platform for lawyers"
        body = f'''
  <text x="24" y="104" font-size="14" fill="{c["ink"]}">Built it, sold it to paying customers, didn't raise.</text>
  <text x="24" y="130" font-size="14" fill="{c["ink2"]}">Code is private. Happy to walk through the</text>
  <text x="24" y="150" font-size="14" fill="{c["ink2"]}">architecture and what I'd do differently.</text>'''
        tags = ["founder", "multi-model", "legal"]
    tx = 24
    tag_svg = []
    for t in tags:
        tw = 14 + len(t) * 7
        tag_svg.append(f'<rect x="{tx}" y="{h - 34}" width="{tw}" height="22" rx="11" fill="{c["chip"]}"/>'
                       f'<text x="{tx + tw / 2}" y="{h - 19}" text-anchor="middle" font-size="11.5" fill="{c["ink2"]}">{t}</text>')
        tx += tw + 8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{SANS}" role="img" aria-label="{title}: {sub}">
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="{c["panel"]}" stroke="{c["rule"]}"/>
  <rect x="0.5" y="0.5" width="6" height="{h - 1}" rx="3" fill="{c["ok"] if kind == "triage" else "#6d5dfc"}"/>
  <text x="24" y="40" font-family="{SERIF}" font-size="24" font-weight="700" fill="{c["ink"]}">{title}</text>
  <text x="24" y="64" font-size="13.5" fill="{c["ink2"]}">{sub}</text>
  {body}
  {"".join(tag_svg)}
</svg>
'''


DIVIDER_W = 960


def divider(c: dict) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {DIVIDER_W} 6" width="{DIVIDER_W}" height="6" role="presentation">
  <defs><linearGradient id="g" x1="0" x2="1">
    <stop offset="0" stop-color="{c["ok"]}" stop-opacity="0"/><stop offset="0.5" stop-color="{c["ok"]}"/><stop offset="1" stop-color="#6d5dfc" stop-opacity="0"/>
    <animate attributeName="x1" dur="6s" repeatCount="indefinite" values="-0.6;0.6;-0.6"/>
    <animate attributeName="x2" dur="6s" repeatCount="indefinite" values="0.4;1.6;0.4"/>
  </linearGradient></defs>
  <rect y="2" width="{DIVIDER_W}" height="2" rx="1" fill="url(#g)"/>
</svg>
'''


if __name__ == "__main__":
    for name, c in THEMES.items():
        open(f"header-{name}.svg", "w").write(hero(c))
        open(f"terminal-{name}.svg", "w").write(terminal(c))
        open(f"phases-{name}.svg", "w").write(phases(c))
        open(f"stack-{name}.svg", "w").write(stack(c))
        open(f"about-{name}.svg", "w").write(code_card(c))
        open(f"card-triage-{name}.svg", "w").write(project_card(c, "triage"))
        open(f"card-legit-{name}.svg", "w").write(project_card(c, "legit"))
        open(f"divider-{name}.svg", "w").write(divider(c))
        open(f"industries-{name}.svg", "w").write(industries(c))
        open(f"metrics-{name}.svg", "w").write(metrics(c))
    print("wrote all svgs x light/dark")
