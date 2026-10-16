# Contributing

Use Python 3.11+ and install `.[dev]` in a virtual environment. Run pytest, Ruff check/format and the two deterministic generators documented in README. Add a minimal synthetic regression for each semantic change. Update all four locale catalogs whenever adding a diagnostic, and preserve machine codes/parameters or document a versioned break.

Keep network access and actuator code outside this validator. Do not contribute actual household exports, credentials, hostnames, floorplans or device IDs. Fixture times and labels should clearly be synthetic. Distinguish declared correctness from physical acceptance.

Changes should use a focused feature branch and pull request, with signed commits and required CI passing. GitHub Actions dependencies must be pinned to immutable full commit SHAs. Do not push directly to main. Follow the repository's current publication process; package version, root `version`, and release tag must agree.

English, Russian, German and Spanish corrections are welcome. CLI catalogs require key parity; machine fields intentionally remain language-independent. Major semantic changes also need EN/RU guide updates.
