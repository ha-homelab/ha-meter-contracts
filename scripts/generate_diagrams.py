"""Reproduce original, static SVG explanations from synthetic data only."""

from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1] / "docs" / "images"
INK, MUTED, BLUE, RED, GREEN = "#172b3a", "#526574", "#175f9b", "#a52a2a", "#22664a"


def text(x, y, value, size=18, color=INK, weight="400"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
        f'font-weight="{weight}">{escape(value)}</text>'
    )


def box(x, y, w, h, title, subtitle, color=BLUE):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
        f'fill="#f7f9fb" stroke="{color}" stroke-width="2"/>'
        + text(x + 18, y + 32, title, 20, color, "600")
        + text(x + 18, y + 61, subtitle, 17, MUTED)
    )


def line(x1, y1, x2, y2, color=BLUE, dashed=False):
    return (
        f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" '
        f'stroke-width="2.5"' + (' stroke-dasharray="6 5"' if dashed else "") + "/>"
    )


def diagram(name, title, desc, content):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 510" '
        f'role="img" aria-labelledby="title desc">\n<title id="title">{escape(title)}</title>'
        f'<desc id="desc">{escape(desc)}</desc>'
        '<rect width="1100" height="510" fill="white"/>'
        '<g font-family="system-ui, sans-serif">'
        + text(36, 44, title, 26, INK, "650")
        + content
        + text(36, 486, "Synthetic example · HA Meter Contracts · MIT", 14, MUTED)
        + "</g></svg>\n"
    )
    (ROOT / name).write_text(svg)


def generate():
    content = text(36, 77, "One meter covers every outlet below its physical scope.", 18, MUTED)
    content += box(60, 210, 300, 95, "Whole-strip meter", "720 W total", GREEN)
    for y, title, subtitle in (
        (110, "Outlet A", "Individual power unknown"),
        (230, "Outlet B", "Individual power unknown"),
        (350, "Outlet C", "Individual power unknown"),
    ):
        content += line(360, 257, 690, y + 40)
        content += box(690, y, 345, 85, title, subtitle)
    content += text(400, 168, "Covers all three", 18, BLUE)
    content += text(55, 369, "Valid claim: strip total = 720 W", 19, GREEN, "600")
    content += text(55, 407, "Invalid claim: outlet A = 720 W", 19, RED, "600")
    content += text(55, 440, "No per-outlet values can be inferred from this total.", 17, MUTED)
    diagram(
        "topology.svg",
        "Physical scope: a strip is not one outlet",
        "One 720 W whole-strip meter covers outlets A, B and C. "
        "Their individual powers are unknown.",
        content,
    )

    content = text(
        36, 77, "Different transport paths can represent the same measurement.", 18, MUTED
    )
    content += box(40, 210, 245, 90, "One physical CT", "provenance: ct_stream_a")
    content += box(380, 120, 285, 90, "Direct representation", "0.8 kW = 800 W")
    content += box(380, 300, 285, 90, "Bridge representation", "800 W")
    content += line(285, 255, 380, 165) + line(285, 255, 380, 345)
    content += line(663, 165, 790, 255, RED) + line(663, 345, 790, 255, RED)
    content += box(790, 210, 265, 90, "Do not add both", "1600 W is double-counted", RED)
    content += text(380, 259, "Same source, not two loads", 18, MUTED)
    content += text(
        40,
        444,
        "Keep both in an inventory if useful; select one representation in a sum.",
        20,
        GREEN,
    )
    diagram(
        "duplicate-stream.svg",
        "Provenance: prevent double counting",
        "A direct 0.8 kW reading and an 800 W bridge reading have the same provenance. "
        "Summing them is invalid.",
        content,
    )

    content = text(
        36, 77, "Synthetic UTC samples · freshness budget 30 s · evaluate at 12:00:00", 18, MUTED
    )
    content += '<rect x="500" y="100" width="300" height="320" fill="#edf5ef"/>'
    content += line(800, 97, 800, 425, BLUE, True)
    for y, name, x, label, color in (
        (150, "Fresh", 750, "11:59:55 · age 5 s", GREEN),
        (250, "Stale", 200, "11:59:00 · age 60 s", RED),
        (350, "Future", 900, "12:00:10 · invalid", RED),
    ):
        content += text(36, y + 6, name, 20, color, "600")
        content += line(175, y, 1000, y, MUTED)
        content += f'<circle cx="{x}" cy="{y}" r="8" fill="{color}"/>'
        content += text(max(180, min(x - 95, 855)), y + 35, label, 17, color)
    content += text(500, 116, "Accepted age window", 17, GREEN)
    content += text(810, 116, "Evaluation", 17, BLUE)
    content += text(
        175, 447, "A cache replay cannot move an old measurement into the fresh window.", 19, INK
    )
    diagram(
        "sample-quality.svg",
        "Sample quality: keep the original measurement time",
        "At noon with a 30 second budget, an 11:59:55 sample is fresh, "
        "an 11:59:00 sample stale, and a 12:00:10 sample invalid.",
        content,
    )


if __name__ == "__main__":
    generate()
