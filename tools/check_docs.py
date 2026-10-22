#!/usr/bin/env python3
"""Check documentation languages, relative links and original SVG syntax."""

import re
import subprocess
from pathlib import Path
from urllib.parse import unquote
from xml.etree import ElementTree as ET

from doc_translations import check_translations

root = Path(__file__).resolve().parents[1]
paths = [
    root / p
    for p in subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
    if p
]
paths = sorted(set(paths) | set(root.glob("docs/*/*.md")) | set(root.glob("wiki/*.md")))
errors = check_translations(root)
for name in (
    "README.md",
    "README.ru.md",
    "README.de.md",
    "README.es.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "wiki/Home.md",
    "wiki/_Sidebar.md",
    "docs/translations.md",
):
    if not (root / name).is_file():
        errors.append("Missing " + name)
for path in paths:
    if path.suffix == ".svg":
        try:
            ET.parse(path)
        except ET.ParseError:
            errors.append("Invalid SVG " + str(path.relative_to(root)))
    if path.suffix != ".md":
        continue
    body = re.sub(
        r"^```[^\n]*\n.*?^```[^\n]*$", "", path.read_text(encoding="utf-8"), flags=re.M | re.S
    )
    links = re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', body)
    links.extend(re.findall(r'<a\b[^>]*\bhref="([^"]+)"', body))
    for link in links:
        if re.match(r"^[a-z][a-z\d+.-]*:|^#|^//", link, re.I):
            continue
        dest = unquote(link.split("#")[0]).strip("<>")
        if not dest:
            continue
        target = path.parent / dest
        if "wiki" in path.relative_to(root).parts and not target.suffix:
            target = target.with_suffix(".md")
        if not target.resolve().is_relative_to(root):
            errors.append(str(path.relative_to(root)) + ": link escapes repository " + dest)
        elif not target.exists():
            errors.append(str(path.relative_to(root)) + ": broken relative link " + dest)
if errors:
    raise SystemExit("\n".join(errors))
print("PASS: 24-language complete guides, source contracts, relative links and SVG XML.")
