"""Regressions for complete guide parity and generated language navigation."""

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "doc_translations", Path(__file__).resolve().parents[1] / "tools/doc_translations.py"
)
docs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(docs)

SOURCE = """<a id="guide"></a>

# Guide

Use `--check`.

## Run

- Retain source time.

[Reference](https://example.invalid/reference)

```sh
cat <<'EOF'
first


second
EOF
```
"""


def fixture(root, rtl=False):
    code = "ar" if rtl else "ja"
    languages = [
        {"code": "en", "label": "English", "dir": "ltr"},
        {"code": code, "label": "العربية" if rtl else "日本語", "dir": "rtl" if rtl else "ltr"},
    ]
    (root / "docs" / code).mkdir(parents=True)
    (root / "docs/languages.json").write_text(json.dumps(languages), encoding="utf-8")
    for lang in ("en", code):
        body = SOURCE
        if rtl and lang == code:
            block = docs.FENCES.findall(body)[0]
            body = body.replace(block, '</div>\n\n<div dir="ltr">\n\n' + block + "\n\n</div>")
            body = '<div lang="ar" dir="rtl">\n\n' + body
        body += "\n" + docs.navigation("docs/guide.md", lang, languages) + "\n"
        (root / docs.localized("docs/guide.md", lang)).write_text(body, encoding="utf-8")
    (root / "docs/translations.json").write_text(
        json.dumps({"sources": {"docs/guide.md": docs.digest(SOURCE)}}), encoding="utf-8"
    )
    return root / f"docs/{code}/guide.md"


def test_whitespace_inside_executable_sample_is_significant():
    changed = SOURCE.replace("first\n\n\nsecond", "first\n\nsecond")
    assert docs.digest(SOURCE) != docs.digest(changed)
    assert (
        docs.structure(SOURCE)["executable blocks"] != docs.structure(changed)["executable blocks"]
    )
    assert docs.digest(SOURCE) == docs.digest(SOURCE + "\n" + docs.START + "\nnew nav\n" + docs.END)


@pytest.mark.parametrize(
    ("before", "after", "expected"),
    [
        ("first\n\n\nsecond", "first\n\nsecond", "executable blocks"),
        ("--check", "--write", "inline identifiers"),
        ("## Run", "Run", "heading levels"),
        ("- Retain", "Retain", "list structure"),
        ('id="guide"', 'id="renamed"', "stable anchors"),
        ("https://example.invalid/reference", "https://example.invalid/other", "guide links"),
        ("日本語", "missing", "language navigation"),
    ],
)
def test_translation_regressions_are_rejected(tmp_path, before, after, expected):
    translated = fixture(tmp_path)
    assert docs.check_translations(tmp_path) == []
    translated.write_text(
        translated.read_text(encoding="utf-8").replace(before, after), encoding="utf-8"
    )
    assert any(expected in error for error in docs.check_translations(tmp_path))


def test_source_prose_drift_requires_translation_review(tmp_path):
    fixture(tmp_path)
    source = tmp_path / "docs/guide.md"
    source.write_text(
        source.read_text(encoding="utf-8").replace("Use", "Always use"), encoding="utf-8"
    )
    assert any("source changed" in error for error in docs.check_translations(tmp_path))


def test_missing_page_prevents_partial_navigation_write(tmp_path):
    translated = fixture(tmp_path)
    source = tmp_path / "docs/guide.md"
    source.write_text(
        source.read_text(encoding="utf-8").replace("English", "stale"), encoding="utf-8"
    )
    before = source.read_text(encoding="utf-8")
    translated.unlink()
    assert any("Missing guide" in error for error in docs.sync_navigation(tmp_path, write=True))
    assert source.read_text(encoding="utf-8") == before


@pytest.mark.parametrize("removed", ['<div lang="ar" dir="rtl">', '<div dir="ltr">'])
def test_rtl_prose_and_executable_direction_are_checked(tmp_path, removed):
    translated = fixture(tmp_path, rtl=True)
    assert docs.check_translations(tmp_path) == []
    translated.write_text(
        translated.read_text(encoding="utf-8").replace(removed, ""), encoding="utf-8"
    )
    assert any(
        "right-to-left" in error or "left-to-right" in error
        for error in docs.check_translations(tmp_path)
    )


def test_localized_paths_are_platform_independent():
    assert docs.localized("docs/usage.md", "ja") == "docs/ja/usage.md"
    assert docs.localized("wiki/Home.md", "ja") == "wiki/Home-ja.md"
    assert (
        docs.translated_link(
            "usage.md#offline-home-assistant-adapter", "docs/schema.md", "ja", {"docs/usage.md": ""}
        )
        == "usage.md#offline-home-assistant-adapter"
    )
    assert docs.translated_link("../schema.json", "docs/schema.md", "ja", {}) == "../../schema.json"


def test_rtl_container_needs_markdown_spacing(tmp_path):
    translated = fixture(tmp_path, rtl=True)
    body = translated.read_text(encoding="utf-8")
    translated.write_text(body.replace('dir="rtl">\n\n', 'dir="rtl">\n'), encoding="utf-8")
    assert any("Markdown spacing" in error for error in docs.check_translations(tmp_path))


def test_unicode_guides_under_ascii_default_encoding(tmp_path):
    fixture(tmp_path)
    script = """
import importlib.util
import json
import sys
from pathlib import Path
spec = importlib.util.spec_from_file_location('doc_translations', sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(json.dumps(module.check_translations(Path(sys.argv[2]))))
"""
    result = subprocess.run(
        [sys.executable, "-c", script, SPEC.origin, str(tmp_path)],
        env={**os.environ, "LC_ALL": "C", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"},
        capture_output=True,
        check=True,
    )
    assert json.loads(result.stdout.decode("ascii")) == []
