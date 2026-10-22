<a id="contract-schema-v1"></a>

# Esquema de contrato v1

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../schema.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/schema.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/schema.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/schema.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/schema.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="schema.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/schema.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/schema.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/schema.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/schema.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/schema.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="../it/schema.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/schema.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/schema.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/schema.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="../pl/schema.md" lang="pl" dir="ltr">Polski</a> ·
<a href="../pt/schema.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/schema.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/schema.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/schema.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/schema.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/schema.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/schema.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/schema.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
El archivo legible por máquinas [schema.json](../../schema.json) describe la estructura. El analizador Python es la autoridad para los límites; `audit` añade semántica física y temporal que JSON Schema no puede demostrar. Genere el archivo estructural con `python3 scripts/generate_schema.py`.

<a id="root-and-limits"></a>

## Raíz y límites

Obligatorios: entero `schema_version: 1`, `scopes`, `meters`. Opcional: `sums` (vacío por defecto). Los campos desconocidos se rechazan en todos los niveles. Hasta 512 ámbitos, 512 medidores y 128 sumas; ámbitos y medidores no pueden estar vacíos. Cada suma tiene 1–512 miembros. La entrada es UTF-8, como máximo 1.048.576 bytes, profundidad 16 y 20.000 nodos de valores. Se rechazan claves JSON duplicadas, NaN/Infinity y alias/anclas/etiquetas explícitas YAML. Entrecomille las fechas YAML para mantenerlas como cadenas.

Los identificadores tienen 1–96 caracteres ASCII: comienzan por letra/dígito y continúan con letras, dígitos, `.`, `_`, `-`. Son únicos dentro de cada colección; ámbitos y medidores tienen espacios de nombres separados. Todos los tiempos incluyen `T` y zona horaria. Los números son finitos, no booleanos, y están entre ±10^15 salvo un límite más estrecho.

<a id="physical-scopes"></a>

## Ámbitos físicos

Cada ámbito tiene `id`, `kind` (`site`, `circuit`, `strip`, `outlet`, `load`) y `parent` opcional. Los padres deben existir y formar un bosque acíclico. Un medidor en un padre cubre todos sus descendientes. Los tipos son descriptivos: no infieren tensión, fases, valores nominales, cableado ni padres permitidos. Usted declara la topología real.

<a id="meters"></a>

## Medidores

Campos obligatorios:

- `id`, `scope`: identificador único de medida y ámbito físico declarado.
- `quantity`: `power`, `energy`, `voltage`, `current`.
- `unit`: respectivamente W/kW, Wh/kWh, V, A. El analizador acepta el vocabulario; el auditor verifica la dimensión.
- `kind`: `measured` o `estimated`. Es una declaración, no una verificación de laboratorio.
- `provenance`: identidad estable del flujo físico de medidas, **no** de su representación HA/MQTT. Las lecturas alias la comparten. Un signo/magnitud/ámbito distinto con la misma procedencia es un conflicto; todos los alias de ese flujo quedan excluidos de sumas, sin depender del orden de entrada. Use procedencias separadas para canales de flujo realmente distintos.
- `sign`: `nonnegative` para magnitudes solo de consumo/importación/exportación; `signed` para flujo bidireccional declarado. Esta versión no infiere qué dirección física es positiva.
- `state_class`: `measurement`, `total`, `total_increasing`.
- `freshness_seconds`: presupuesto de antigüedad positivo, 0.001–604800 segundos.

`reset` opcional: `never`, `periodic`, `device_restart`, `unknown`, `not_applicable` (predeterminado). Energía requiere una política explícita distinta de `not_applicable` y una clase de estado de tipo total. La energía con signo no puede usar `total_increasing`. Las otras magnitudes necesitan `measurement` y `not_applicable`.

`sample`, `previous` opcionales: null o un objeto con `value` (número o null), `measured_at` y `reset_at` opcional. La muestra anterior debe ser más antigua. Una bajada de contador no negativo requiere una marca de reinicio entre muestras; `never` la rechaza. `reset_at` no puede ser posterior a su muestra y solo se aplica a energía. La semántica desconocida de reinicio produce una advertencia. Un contador neto con signo puede bajar legítimamente; su base correcta sigue siendo responsabilidad del productor.

`calibration` opcional: `quantity`, `factor` positivo (10^-12–10^12), identificador sintético/privado `reference`, `verified_at`. Registra evidencia para esa magnitud exacta. Los valores **ya están calibrados**: el validador nunca reaplica el factor. Una calibración futura o de tensión en un medidor de potencia es inválida. La ausencia de calibración no demuestra precisión ni es automáticamente un error.

`entity_id`, `timestamp_attribute` opcionales: mapeo HA sin conexión; consulte [uso](usage.md#offline-home-assistant-adapter).

<a id="sums"></a>

## Sumas

Obligatorios: `id`, `scope` objetivo, lista de identificadores de medidores en `meters`, `quantity` (`power` o `energy`), `coverage` (`partial` o `complete`). `max_skew_seconds` opcional: 0–604800, predeterminado 2.

Los miembros deben estar dentro del ámbito objetivo, tener dimensiones y semántica de signo compatibles, usar flujos físicos distintos y no superponerse como padre/hijo ni ámbitos idénticos. Una suma completa debe cubrir cada **ámbito hoja declarado** bajo su objetivo. El cableado no declarado no se detecta. Una suma parcial informa explícitamente de cobertura parcial. No se admiten sumas anidadas; los miembros siempre referencian medidores.

Cada miembro debe tener datos válidos y recientes; sus tiempos de adquisición deben respetar el desfase permitido. Energía requiere además orígenes explícitos `reset_at` idénticos. Se comprueba la alineación declarada, no la precisión de la acumulación histórica. Las sumas se convierten a W o Wh. No se admiten deliberadamente sumas de corriente y tensión, porque su significado depende de la topología del circuito.

Una suma numérica no está disponible si falla cualquier evidencia requerida o comprobación semántica. Las estimaciones se propagan como `kind: estimated`. Dos alias pueden coexistir en el inventario, pero no contribuir ambos a una suma. No se infiere un total para tomas individuales no medidas.

<a id="report-v1"></a>

## Informe v1

Raíz: `schema_version`, instante de evaluación `at` normalizado a UTC, recuentos de gravedad en `summary`, `findings` ordenados y `sums`. Cada hallazgo contiene `code`, `severity`, `path` de estilo JSON y `params` estructurados; la CLI añade `message`. Cada suma contiene `id`, `scope`, `quantity`, `unit` base, `value`, `status`, `kind`, `coverage`. Los valores desconocidos son JSON null, nunca NaN.
