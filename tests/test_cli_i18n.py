import ast
import json
from pathlib import Path

import pytest

from ha_meter_contracts.cli import main
from ha_meter_contracts.i18n import LANGUAGES, catalog

ROOT = Path(__file__).resolve().parents[1]
AT = ["--at", "2026-01-01T12:00:05Z"]


def test_catalogs_cover_all_findings_and_errors():
    keys = set(catalog("en"))
    for lang in LANGUAGES:
        messages = catalog(lang)
        assert set(messages) == keys
        assert all(isinstance(v, str) and v.strip() for v in messages.values())
    required = set()
    for path in (ROOT / "src/ha_meter_contracts").glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in {"add", "InputError"} and node.args:
                    assert isinstance(node.args[0], ast.Constant)
                    required.add(node.args[0].value)
    assert required <= keys


@pytest.mark.parametrize("lang", LANGUAGES)
def test_localized_help(lang, capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--lang", lang, "--help"])
    assert exc.value.code == 0
    output = capsys.readouterr().out
    assert catalog(lang)["cli_description"] in " ".join(output.split())
    assert catalog(lang)["cli_usage"] in output


@pytest.mark.parametrize("lang", LANGUAGES)
def test_findings_have_translated_message_and_identical_machine_code(lang, capsys):
    assert (
        main(["check", str(ROOT / "examples/kmc-shared-meter.json"), "--json", "--lang", lang, *AT])
        == 1
    )
    data = json.loads(capsys.readouterr().out)
    finding = next(f for f in data["findings"] if f["code"] == "scope_outside")
    assert finding["message"] == catalog(lang)["scope_outside"]
    assert finding["params"] == {"meter": "whole_strip", "scope": "outlet_a"}


def test_cli_clean_exit_and_deterministic_json(capsys):
    args = ["check", str(ROOT / "examples/valid-three-meters.json"), "--json", *AT]
    assert main(args) == 0
    first = capsys.readouterr().out
    assert main(args) == 0
    assert capsys.readouterr().out == first


def test_input_failure_has_safe_machine_error(capsys):
    assert main(["check", "missing-file-with-private-content", "--json", "--lang", "es"]) == 2
    output = capsys.readouterr().out
    assert "missing-file-with-private-content" not in output
    assert json.loads(output)["error"]["code"] == "input_read"


def test_argument_error_is_structured(capsys):
    assert main(["unknown-command-private-value", "--json"]) == 2
    output = capsys.readouterr().out
    assert "unknown-command-private-value" not in output
    assert json.loads(output)["error"]["code"] == "cli_arguments"


def test_import_ha_cli(capsys):
    assert (
        main(
            [
                "import-ha",
                str(ROOT / "examples/ha-contract.json"),
                "--ha-states",
                str(ROOT / "examples/ha-states.synthetic.json"),
            ]
        )
        == 0
    )
    data = json.loads(capsys.readouterr().out)
    assert data["meters"][0]["sample"]["value"] == 720
