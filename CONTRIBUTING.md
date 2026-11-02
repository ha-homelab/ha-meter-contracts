# Contributing

Use Python 3.11+ and use the locked development environment below. Run pytest, Ruff check/format and the two deterministic generators documented in README. Add a minimal synthetic regression for each semantic change. Update all four locale catalogs whenever adding a diagnostic, and preserve machine codes/parameters or document a versioned break.

Keep network access and actuator code outside this validator. Do not contribute actual household exports, credentials, hostnames, floorplans or device IDs. Fixture times and labels should clearly be synthetic. Distinguish declared correctness from physical acceptance.

Changes should use a focused feature branch and pull request, with signed commits and required CI passing. GitHub Actions dependencies must be pinned to immutable full commit SHAs. Do not push directly to main. Follow the repository's current publication process; package version, root `version`, and release tag must agree.

English, Russian, German and Spanish corrections are welcome. CLI catalogs require key parity; machine fields intentionally remain language-independent. The complete guides and checked-in wiki pages cover 24 documentation languages; semantic changes require matching updates in every edition. See [translation maintenance](docs/translations.md) for source digests, exact examples, RTL layout and checks.


## Reproduce the CI environment

CI uses Python 3.12. In an activated Python 3.12 virtual environment, install the
committed hash lock before installing this checkout:

```sh
python -m pip install --only-binary=:all: --require-hashes -r requirements-ci.txt
python -m pip install --no-index --no-deps --no-build-isolation -e .
python -m pip check
python -m pytest -q
python -m ruff check --select E4,E7,E9,F src tests tools
python tools/check_docs.py
python -m build --no-isolation
```

`requirements-ci.txt` includes the runtime requirements from `pyproject.toml`,
the development tools from `requirements-ci.in`, and the exact build backend.
The local package and source/wheel builds cannot silently resolve another build
environment. CI installs the checkout non-editably; editable installation above
is for local development only.

When changing dependencies, keep `setuptools` in `requirements-ci.in` aligned
with `[build-system].requires`. Regenerate with uv 0.12.7 and review every version
and hash change before running the commands above:

```sh
uv pip compile pyproject.toml requirements-ci.in --universal --python-version 3.12 --generate-hashes --output-file requirements-ci.txt
```

The tests compare each reviewed tool pin with both the lock and the installed
environment, so changing an input requires refreshing and installing the lock.
Commit the inputs and generated lock together. Do not remove hash verification,
allow dependency resolution in the local install, or restore build isolation to
work around an incomplete lock.

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
