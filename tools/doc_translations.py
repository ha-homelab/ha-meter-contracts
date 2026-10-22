#!/usr/bin/env python3
"""Validate complete guide translations and refresh language navigation only."""

import argparse
import hashlib
import json
import posixpath
import re
from collections import Counter
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- language-navigation:start -->"
END = "<!-- language-navigation:end -->"
NAV = re.compile(r"\n*" + re.escape(START) + r".*?" + re.escape(END) + r"\n*", re.S)
FENCES = re.compile(r"^```[^\n]*\n.*?^```[^\n]*$", re.M | re.S)
LINKS = re.compile(r"!?\[[^\]]*\]\(([^\s)]+)\)")


def content(text):
    """Exclude generated navigation without changing executable whitespace."""
    return NAV.sub("\n\n", text).strip()


def digest(text):
    return hashlib.sha256(content(text).encode("utf-8")).hexdigest()


def localized(source, code):
    path = PurePosixPath(source)
    if code == "en":
        return source
    if path.parts[0] == "docs":
        return str(path.parent / code / path.name)
    return str(path.with_name(f"{path.stem}-{code}.md"))


def navigation(source, code, languages):
    links = []
    for language in languages:
        target = posixpath.relpath(
            localized(source, language["code"]),
            posixpath.dirname(localized(source, code)),
        )
        links.append(
            f'<a href="{target}" lang="{language["code"]}" '
            f'dir="{language.get("dir", "ltr")}">{language["label"]}</a>'
        )
    return START + '\n<p dir="ltr">\n' + " ·\n".join(links) + "\n</p>\n" + END


def translated_link(url, source, code, sources):
    wiki = "https://github.com/ha-homelab/ha-meter-contracts/wiki/"
    blob = "https://github.com/ha-homelab/ha-meter-contracts/blob/main/"
    if url.startswith(wiki):
        page = url[len(wiki) :]
        return url + "-" + code if code != "en" and f"wiki/{page}.md" in sources else url
    if url.startswith(blob):
        page = url[len(blob) :]
        return blob + localized(page, code) if page in sources else url
    if re.match(r"^[a-z][a-z\d+.-]*:|^#|^//", url, re.I):
        return url
    base, separator, fragment = url.partition("#")
    target = posixpath.normpath(posixpath.join(posixpath.dirname(source), base))
    if target in sources:
        target = localized(target, code)
    return (
        posixpath.relpath(target, posixpath.dirname(localized(source, code))) + separator + fragment
    )


def structure(text):
    prose = FENCES.sub("", content(text))
    return {
        "executable blocks": FENCES.findall(content(text)),
        "inline identifiers": Counter(re.findall(r"`([^`\n]+)`", prose)),
        "heading levels": re.findall(r"^(#{1,6}) ", prose, re.M),
        "list structure": re.findall(r"^([-*]|\d+\.) ", prose, re.M),
        "stable anchors": re.findall(r'<a id="([^"]+)"></a>', prose),
    }


def check_translations(root=ROOT):
    manifest = json.loads((root / "docs/translations.json").read_text(encoding="utf-8"))
    languages = json.loads((root / "docs/languages.json").read_text(encoding="utf-8"))
    sources = manifest["sources"]
    errors = []
    for source, expected_digest in sources.items():
        path = root / source
        if not path.is_file():
            errors.append(f"Missing guide: {source}")
            continue
        original = path.read_text(encoding="utf-8")
        if digest(original) != expected_digest:
            errors.append(f"{source}: source changed; review translations and update digest")
        expected_structure = structure(original)
        original_links = LINKS.findall(FENCES.sub("", content(original)))
        for language in languages:
            code = language["code"]
            name = localized(source, code)
            path = root / name
            if not path.is_file():
                errors.append(f"Missing guide: {name}")
                continue
            text = path.read_text(encoding="utf-8")
            if (
                text.count(START) != 1
                or text.count(END) != 1
                or navigation(source, code, languages) not in text
            ):
                errors.append(f"{name}: incomplete or stale language navigation")
            actual_structure = structure(text)
            for key, expected in expected_structure.items():
                if actual_structure[key] != expected:
                    errors.append(f"{name}: {key} differ from the complete English guide")
            expected_links = Counter(
                translated_link(url, source, code, sources) for url in original_links
            )
            if Counter(LINKS.findall(FENCES.sub("", content(text)))) != expected_links:
                errors.append(f"{name}: guide links differ from the expected language edition")
            if language.get("dir") == "rtl":
                if f'<div lang="{code}" dir="rtl">\n\n' not in text:
                    errors.append(
                        f"{name}: missing right-to-left prose container or Markdown spacing"
                    )
                for block in actual_structure["executable blocks"]:
                    if '<div dir="ltr">\n\n' + block + "\n\n</div>" not in text:
                        errors.append(f"{name}: executable block is not left-to-right")
    return errors


def sync_navigation(root=ROOT, write=False):
    manifest = json.loads((root / "docs/translations.json").read_text(encoding="utf-8"))
    languages = json.loads((root / "docs/languages.json").read_text(encoding="utf-8"))
    errors, updates = [], []
    for source in manifest["sources"]:
        for language in languages:
            code = language["code"]
            name = localized(source, code)
            path = root / name
            if not path.is_file():
                errors.append(f"Missing guide: {name}")
                continue
            text = path.read_text(encoding="utf-8")
            if (
                text.count(START) != 1
                or text.count(END) != 1
                or text.index(START) > text.index(END)
            ):
                errors.append(f"{name}: expected one ordered navigation marker pair")
                continue
            updated = (
                text[: text.index(START)]
                + navigation(source, code, languages)
                + text[text.index(END) + len(END) :]
            )
            if text != updated:
                if write:
                    updates.append((path, updated))
                else:
                    errors.append(f"{name}: stale language navigation")
    if not errors:
        for path, text in updates:
            path.write_text(text, encoding="utf-8")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="refresh navigation only")
    args = parser.parse_args()
    failures = sync_navigation(write=args.write)
    if not failures:
        failures = check_translations()
    if failures:
        raise SystemExit("\n".join(failures))
    print("PASS: complete guide languages, navigation and source contracts.")
