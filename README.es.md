# HA Meter Contracts

Valida sin conexión el significado físico de las mediciones, las sumas y la vigencia de las muestras. Lee JSON/YAML; no necesita token de HA, no accede a la red ni envía órdenes.

[English](README.md) · [Русский](README.ru.md) · [Deutsch](README.de.md)

Un medidor de una regleta no mide por separado la bomba conectada. Dos representaciones de un mismo transformador de corriente no son mediciones independientes. El programa detecta estos errores en la topología declarada.

![Topología sintética](docs/images/topology.svg)

## Instalación

Python 3.11 o posterior; desde el código fuente descargado:

```sh
python3 -m venv .venv
.venv/bin/python3 -m pip install .
.venv/bin/ha-meter-contracts check examples/valid-three-meters.json --at 2026-01-01T12:00:05Z --lang es
.venv/bin/ha-meter-contracts check examples/duplicate-emporia.json --at 2026-01-01T12:00:05Z --json --lang es
```

El primer ejemplo sintético da 720 W. El segundo detecta una fuente duplicada y termina intencionadamente con código 1. Sin `--at` se usa la hora UTC actual. No se afirma publicación en PyPI ni pruebas físicas de dispositivos.

## Interfaz

`--lang es` traduce la ayuda y los diagnósticos. Los campos JSON, códigos, rutas y parámetros no cambian de idioma. Código 0: sin errores ni advertencias; 1: hay hallazgos; 2: entrada o argumentos inválidos. Una suma no fiable devuelve `null` / `unavailable`, nunca un cero inventado.

Comprueba ciclos, referencias, solapamientos, procedencia duplicada, unidades, signos, reinicios, antigüedad, desfase temporal y calibración por magnitud. Una estimación sigue marcada `estimated`. Calibrar voltaje no calibra potencia.

## Exportación de HA guardada

```sh
.venv/bin/ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
.venv/bin/ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --lang es
```

El mapeo exige un atributo con la hora original de medición. Las fechas de actualización de HA no la sustituyen. No hay cliente de HA en vivo.

[Uso en inglés](docs/usage.md) · [Esquema](docs/schema.md) · [Diagnóstico](docs/troubleshooting.md) · [Límites](docs/limits.md) · [Wiki](wiki/Home.md)

Los datos e ilustraciones son sintéticos. La herramienta valida declaraciones, no descubre el cableado real ni sustituye la protección eléctrica. Pruebas: `python3 -m pytest -q` tras instalar `.[dev]`. Licencia MIT.
