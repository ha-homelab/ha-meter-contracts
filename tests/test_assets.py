import importlib.util
import json
import re
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def test_schema_matches_generator():
    assert (
        json.loads((ROOT / "schema.json").read_text()) == module("generate_schema").build_schema()
    )


def test_diagrams_reproduce_and_have_no_active_or_external_content(tmp_path):
    diagrams = module("generate_diagrams")
    diagrams.ROOT = tmp_path
    diagrams.generate()
    for path in tmp_path.glob("*.svg"):
        assert path.read_bytes() == (ROOT / "docs/images" / path.name).read_bytes()
        svg = ElementTree.fromstring(path.read_text())
        assert svg.find("{http://www.w3.org/2000/svg}title") is not None
        assert svg.find("{http://www.w3.org/2000/svg}desc") is not None
        assert "Synthetic" in path.read_text()
        for element in svg.iter():
            assert element.tag.split("}")[-1] not in {"script", "image", "foreignObject"}
            assert not any(k.startswith("on") or k.endswith("href") for k in element.attrib)


def test_documentation_relative_links_resolve():
    docs = list(ROOT.glob("*.md")) + list((ROOT / "docs").rglob("*.md"))
    for path in docs:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            assert (path.parent / target.split("#")[0]).exists(), (path, target)


def test_version_is_consistent():
    import tomllib

    from ha_meter_contracts import __version__

    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    assert project["version"] == __version__ == (ROOT / "version").read_text().strip()
