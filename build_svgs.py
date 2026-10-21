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
  <text x="70" y="124" font-size="19" fill="{c["ink2"]}">Forward-deployed AI engineer. I take agentic systems from discovery to production</text>
  <text x="70" y="150" font-size="19" fill="{c["ink2"]}">inside enterprises where a wrong answer has a cost.</text>
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

ICONS = json.load(open("icons.json"))


def stack(c: dict) -> str:
    """Self-hosted icon wall. Tiles fade in left to right once per loop."""
    names = list(ICONS)
    tile, gap = 78, 18
    cols = len(names)
    w = cols * tile + (cols - 1) * gap + 40
    h = tile + 58
    loop = 12.0
    out = []
    for i, n in enumerate(names):
        x = 20 + i * (tile + gap)
        hexc = ICONS[n]["hex"]
        fill = "#" + hexc
        if hexc.lower() in ("191919", "000000"):
            fill = c["ink"]
        on = (0.2 + i * 0.12) / loop
        out.append(f'''
  <g>
    <animate attributeName="opacity" dur="{loop}s" repeatCount="indefinite" keyTimes="0;{on:.3f};{on + 0.03:.3f};0.97;1" values="0;0;1;1;0"/>
    <rect x="{x}" y="10" width="{tile}" height="{tile}" rx="16" fill="{c["panel"]}" stroke="{c["rule"]}"/>
    <g transform="translate({x + tile / 2 - 18} {10 + tile / 2 - 18}) scale(1.5)"><path d="{ICONS[n]["path"]}" fill="{fill}"/></g>
    <text x="{x + tile / 2}" y="{tile + 34}" text-anchor="middle" font-size="12.5" fill="{c["ink2"]}">{n}</text>
  </g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{SANS}" role="img" aria-label="Stack: {", ".join(names)}">
  {"".join(out)}
</svg>
'''


CODE = [
    [("kw", "class "), ("cls", "Shahabaj"), ("p", "("), ("cls", "ForwardDeployedEngineer"), ("p", "):")],
    [("p", "    based_in  = "), ("str", '"Gurugram, India"')],
    [("p", "    role      = "), ("str", '"AI Solutions Architect @ DevRev"')],
    [("p", "    years     = "), ("num", "14")],
    [("p", "    domains   = ["), ("str", '"airlines"'), ("p", ", "), ("str", '"banking"'), ("p", ", "), ("str", '"fintech"'), ("p", ", "), ("str", '"pricing"'), ("p", "]")],
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
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="About me, written as a Python class: based in Gurugram, AI Solutions Architect at DevRev, 14 years, airlines, banking, fintech and pricing; engages by discovering, building, iterating until evals pass the client's gates, then shipping in shadow mode.">
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
    print("wrote all svgs x light/dark")
