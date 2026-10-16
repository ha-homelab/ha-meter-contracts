# Contributing

Use Python 3.11+ and install `.[dev]` in a virtual environment. Run pytest, Ruff check/format and the two deterministic generators documented in README. Add a minimal synthetic regression for each semantic change. Update all four locale catalogs whenever adding a diagnostic, and preserve machine codes/parameters or document a versioned break.

Keep network access and actuator code outside this validator. Do not contribute actual household exports, credentials, hostnames, floorplans or device IDs. Fixture times and labels should clearly be synthetic. Distinguish declared correctness from physical acceptance.

Changes should use a focused feature branch and pull request, with signed commits and required CI passing. GitHub Actions dependencies must be pinned to immutable full commit SHAs. Do not push directly to main. Follow the repository's current publication process; package version, root `version`, and release tag must agree.

English, Russian, German and Spanish corrections are welcome. CLI catalogs require key parity; machine fields intentionally remain language-independent. Major semantic changes also need EN/RU guide updates.


## Feedback and review

Use [GitHub Issues](https://github.com/ha-homelab/ha-meter-contracts/issues) for bug reports,
questions and enhancement proposals; existing issues and pull requests retain
searchable discussion. Include the source revision, expected/actual behavior and
a minimal synthetic reproducer. English reports are welcome. Security reports
follow [SECURITY.md](SECURITY.md), and all participation follows our
[Code of Conduct](CODE_OF_CONDUCT.md).

Contributions are under the repository's MIT license. Submit only material you
have the right to contribute. Follow Python PEP 8 and the repository's Ruff
configuration. Every new major feature and behavior fix requires automated tests,
including a negative or regression case; update the interface documentation and
changelog in the same pull request. Run tests without Python optimization so
assertions remain enabled. The maintainer reviews the diff, test evidence and
open comments before a normal merge. Automated reviews assist this process.

See [RELEASING.md](RELEASING.md) for build and source-version instructions,
[GOVERNANCE.md](GOVERNANCE.md) for responsibilities, and
[ROADMAP.md](ROADMAP.md) for planned work.
