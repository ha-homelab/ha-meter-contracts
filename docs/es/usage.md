<a id="usage"></a>

# Uso

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../usage.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/usage.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/usage.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/usage.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/usage.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="usage.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/usage.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/usage.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/usage.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/usage.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/usage.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="../it/usage.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/usage.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/usage.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/usage.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="../pl/usage.md" lang="pl" dir="ltr">Polski</a> ·
<a href="../pt/usage.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/usage.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/usage.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/usage.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/usage.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/usage.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/usage.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/usage.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="audit"></a>

## Auditoría

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` acepta una marca ISO 8601 con zona horaria. El valor predeterminado es el UTC actual. Con la misma entrada, tiempo e idioma, la salida JSON es determinista. Una muestra es reciente hasta su límite inclusivo `freshness_seconds`; solo caduca después. Una muestra futura es inválida, sin tolerancia implícita de desfase de reloj.

Códigos de salida: 0 = sin errores/advertencias; 1 = hallazgo semántico o de calidad de muestra; 2 = error de entrada/CLI. La información, como un alias sin uso, no hace fallar la comprobación. `--json` escribe tanto informes como objetos de error de entrada en stdout. Sin él, el texto de auditoría va a stdout y los errores de entrada a stderr. Una tubería de salida rota devuelve 2.

No utilice `|| true` en CI para ocultar hallazgos. Los ejemplos intencionadamente inválidos deben comprobar explícitamente la salida 1. Ayuda y versión salen con 0. `import-ha` siempre escribe un contrato JSON; `--json` no cambia su esquema.

<a id="python-library"></a>

## Biblioteca Python

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` crea dataclasses inmutables; `InputError` expone `code`, `path`, `params`. Use este analizador en toda frontera de entrada no fiable. `audit` espera un `Contract` validado y no traduce hallazgos. La CLI añade valores `message` localizados. En la biblioteca, el llamante elige explícitamente el tiempo de evaluación. Ninguna API modifica la entrada ni escribe archivos.

<a id="offline-home-assistant-adapter"></a>

## Adaptador Home Assistant sin conexión

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

Mapee `entity_id` y `timestamp_attribute` en cada medidor deseado. La exportación es una matriz de estados HA con `entity_id`, `state` y `attributes`. El atributo mapeado debe contener la hora ISO original de medida, con zona horaria. `attributes.unit_of_measurement` debe tener la misma dimensión; W/kW y Wh/kWh se convierten a la unidad del contrato.

Solo se copian los valores mapeados y tiempos de origen. Se ignoran otros atributos, incluidos nombres amigables. Una muestra estrictamente más reciente pasa la existente a `previous`. Repetir el mismo valor con la misma hora de origen es idempotente; una muestra anterior o un valor distinto con la misma hora se rechaza como `ha_sample_order`. Entidades ausentes y estados `unknown`/`unavailable` borran la muestra; no se convierten en cero. Falta de hora de origen, unidad incompatible, valor mal formado o ID de entidad duplicado hacen fallar la importación con 2. Los medidores sin mapeo no cambian. Los contratos privados pueden contener IDs de entidades; los ejemplos públicos usan identificadores sintéticos.

Una exportación HA habitual suele carecer de hora de origen original. En ese caso el adaptador se niega deliberadamente a inventarla. Obtenga datos fechados del dispositivo o mantenga el medidor como no disponible. Las horas de recepción/actualización de HA no demuestran la adquisición del dispositivo. El adaptador nunca conecta a `/api/states` ni lee un token. No copia marcas de reinicio de energía desde HA; añada evidencia de reinicio verificada por separado antes de sumar energía.

<a id="suggested-workflow"></a>

## Flujo recomendado

1. Declare el árbol de ámbitos físicos y la procedencia con la documentación del cableado.
2. Empiece con un medidor y un ejemplo sintético fijo.
3. Exporte solo observaciones necesarias a un archivo privado.
4. Audite y revise cada hallazgo antes de cambiar una automatización dependiente.
5. Conserve los tiempos originales y evidencia de calibración durante migraciones.

Este paquete no repara, cambia nombres de entidades, reinicia dispositivos ni despliega automatizaciones.
