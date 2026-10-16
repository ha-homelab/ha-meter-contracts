"""Offline command line interface with localized diagnostics and stable JSON."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime

from . import __version__
from .audit import audit
from .ha_export import overlay_states
from .i18n import LANGUAGES, catalog
from .model import InputError, parse_contract, timestamp
from .reader import load_document


class Parser(argparse.ArgumentParser):
    usage_label = "usage:"

    def format_help(self) -> str:
        return super().format_help().replace("usage:", self.usage_label, 1)

    def error(self, message: str) -> None:
        # argparse messages can contain user input. Emit a bounded generic code.
        raise InputError("cli_arguments")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    lang = "en"
    for i, arg in enumerate(argv):
        if arg == "--lang" and i + 1 < len(argv):
            lang = argv[i + 1]
        elif arg.startswith("--lang="):
            lang = arg.split("=", 1)[1]
    texts = catalog(lang if lang in LANGUAGES else "en")
    as_json = "--json" in argv
    try:
        parser = Parser(description=texts["cli_description"], add_help=False)
        parser.usage_label = texts["cli_usage"]
        parser._positionals.title = texts["cli_positionals"]
        parser._optionals.title = texts["cli_options"]
        parser.add_argument("command", choices=("check", "import-ha"), help=texts["cli_command"])
        parser.add_argument("contract", nargs="?", help=texts["cli_contract"])
        parser.add_argument("--lang", choices=LANGUAGES, default="en", help=texts["cli_lang"])
        parser.add_argument("--at", help=texts["cli_at"])
        parser.add_argument("--json", action="store_true", help=texts["cli_json"])
        parser.add_argument("--ha-states", help=texts["cli_ha"])
        parser.add_argument("--help", "-h", action="help", help=texts["cli_help"])
        parser.add_argument(
            "--version", action="version", version=__version__, help=texts["cli_version"]
        )
        args = parser.parse_args(argv)
        if (
            args.contract is None
            or (args.command == "check" and args.ha_states)
            or (args.command == "import-ha" and (not args.ha_states or args.at))
        ):
            raise InputError("cli_arguments")
        document = load_document(args.contract)
        if args.command == "import-ha":
            result = overlay_states(document, load_document(args.ha_states))
            print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False))
            return 0
        at = timestamp(args.at, "$.at") if args.at else datetime.now(UTC)
        report = audit(parse_contract(document), at=at)
        for finding in report["findings"]:
            finding["message"] = texts[finding["code"]]
        if as_json:
            print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False))
        else:
            print(texts["cli_summary"], json.dumps(report["summary"], sort_keys=True))
            for f in report["findings"]:
                print(
                    f"{f['severity']} {f['code']} {f['path']}: {f['message']} "
                    + json.dumps(f["params"], ensure_ascii=False, sort_keys=True)
                )
            for total in report["sums"]:
                print(texts["cli_sum"], json.dumps(total, ensure_ascii=False, sort_keys=True))
        return int(bool(report["summary"]["error"] or report["summary"]["warning"]))
    except InputError as exc:
        error = {
            "schema_version": 1,
            "error": {
                "code": exc.code,
                "path": exc.path,
                "params": exc.params,
                "message": texts[exc.code],
            },
        }
        if as_json:
            print(json.dumps(error, ensure_ascii=False, sort_keys=True, allow_nan=False))
        else:
            print(f"{exc.code} {exc.path}: {texts[exc.code]}", file=sys.stderr)
        return 2
    except BrokenPipeError:
        return 2


if __name__ == "__main__":
    sys.exit(main())
