# HA Meter Contracts

Offline-Prüfung der physikalischen Bedeutung von Messwerten, ihrer Addierbarkeit und Aktualität. JSON/YAML; kein HA-Token, kein Netzwerkzugriff, keine Gerätebefehle.

[English](README.md) · [Русский](README.ru.md) · [Español](README.es.md)

Ein Gesamtzähler einer Steckdosenleiste misst nicht die einzelne Pumpe. Zwei Darstellungen desselben Stromwandlers sind keine unabhängigen Messungen. Der Validator erkennt solche Fehler anhand der deklarierten Topologie.

![Synthetische Topologie](docs/images/topology.svg)

## Installation und Beispiel

Python 3.11+; im heruntergeladenen Quellverzeichnis:

```sh
python3 -m venv .venv
.venv/bin/python3 -m pip install .
.venv/bin/ha-meter-contracts check examples/valid-three-meters.json --at 2026-01-01T12:00:05Z --lang de
.venv/bin/ha-meter-contracts check examples/duplicate-emporia.json --at 2026-01-01T12:00:05Z --json --lang de
```

Das erste synthetische Beispiel ergibt 720 W. Das zweite meldet doppelte Herkunft und endet absichtlich mit Status 1. Ohne `--at` wird die aktuelle UTC-Zeit verwendet. Eine Veröffentlichung auf PyPI oder Geräteprüfung wird nicht behauptet.

## Schnittstelle

`--lang de` übersetzt Hilfe und Befunde. JSON-Schlüssel, Codes, Pfade und Parameter bleiben sprachunabhängig. Status 0: keine Fehler/Warnungen; 1: Befunde vorhanden; 2: Eingabe- oder Aufruffehler. Ungültige Summen bleiben `null` / `unavailable`.

Geprüft werden Zyklen, fehlende Bereiche, überlappende Zähler, gemeinsame Herkunft, Einheiten, Vorzeichen, Rücksetzungen, Messalter, Zeitversatz und die Messgröße einer Kalibrierung. Schätzungen bleiben `estimated`. Spannungskalibrierung belegt keine Leistungskalibrierung.

## Gespeicherter HA-Export

```sh
.venv/bin/ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
.venv/bin/ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --lang de
```

Die Zuordnung muss ein echtes Quellzeit-Attribut nennen. HA-Änderungszeitstempel werden nicht als Messzeit verwendet. Es gibt keinen Live-HA-Client.

[Englische Bedienung](docs/usage.md) · [Schema](docs/schema.md) · [Fehlersuche](docs/troubleshooting.md) · [Grenzen](docs/limits.md) · [Wiki](wiki/Home.md)

Alle Daten und Abbildungen sind synthetisch. Das Werkzeug validiert Angaben; es erkennt keine reale Verdrahtung und ersetzt keinen Geräteschutz. Tests: `python3 -m pytest -q` nach Installation von `.[dev]`. MIT-Lizenz.
