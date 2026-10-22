<a id="troubleshooting"></a>

# Solución de problemas

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../troubleshooting.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/troubleshooting.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/troubleshooting.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/troubleshooting.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/troubleshooting.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="troubleshooting.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/troubleshooting.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/troubleshooting.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/troubleshooting.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/troubleshooting.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/troubleshooting.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="../it/troubleshooting.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/troubleshooting.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/troubleshooting.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/troubleshooting.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="../pl/troubleshooting.md" lang="pl" dir="ltr">Polski</a> ·
<a href="../pt/troubleshooting.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/troubleshooting.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/troubleshooting.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/troubleshooting.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/troubleshooting.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/troubleshooting.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/troubleshooting.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/troubleshooting.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="a-three-outlet-strip-cannot-produce-three-power-readings"></a>

## Una regleta de tres tomas no produce tres medidas de potencia

`scope_outside` significa que un resultado individual solicitado usa una medida más amplia. Conserve una entidad de toda la regleta. Añada medidas independientes con ámbito correcto si necesita potencia individual. Un relé encendido no demuestra consumo de su carga; una bomba que consume electricidad no demuestra que fluya agua.

<a id="a-migrated-sensor-doubles-the-total"></a>

## Un sensor migrado duplica el total

`alias_stream` por sí solo es informativo. `duplicate_stream` significa que ambas copias aparecen en una suma. Dé la misma procedencia a copias del mismo CT y conserve solo una en la suma. No cambie la procedencia únicamente para silenciar la comprobación.

![Una fuente y dos representaciones](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## No hay suma numérica pese a valores individuales plausibles

Revise `sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap`. Actualice la fuente original y conserve su tiempo de adquisición. Ampliar la antigüedad permitida cambia la política, no repara una medida. La suma completa se juzga contra hojas declaradas; revise también la declaración.

![Cronología sintética de calidad de muestras](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## La energía bajó a medianoche

Una bajada puede ser un reinicio real, sustitución o corrección. Declare la política y añada `reset_at` desde evidencia real de la fuente. La hora en que HA repitió un valor no es una marca de reinicio. `total_increasing` no es adecuado para energía neta con signo. No se suman dos contadores con orígenes distintos.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## La tensión parece calibrada pero los vatios difieren

La calibración es por magnitud. Corregir tensión no valida corriente, relación de fase, potencia ni energía acumulada. El campo del factor es solo documentación: los valores deben contener ya la corrección prevista.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## YAML falla aunque otro analizador lo acepte

Entrecomille fechas, elimine alias/anclas/etiquetas personalizadas y claves duplicadas, y use números finitos. Los campos desconocidos son errores para detectar erratas. Los límites se aplican a ambos formatos. Use JSON para intercambio si los escalares ambiguos de YAML resultan incómodos.

<a id="ha-import-fails-on-timestamps"></a>

## La importación HA falla por las fechas

Asigne a `timestamp_attribute` un atributo real de hora de medida. `last_reported` solo demuestra recepción por HA. Sin hora de origen esta herramienta no puede establecer frescura; deje la muestra como no disponible. No hay problema de token o conexión que depurar porque la importación es sin conexión.

<a id="safe-issue-report"></a>

## Informe de incidencia seguro

Incluya versiones del paquete/Python, códigos estables, un contrato sintético mínimo, el `--at` elegido, resultado esperado y resultado real. No adjunte una exportación HA completa, token, dirección real, horarios domésticos ni identificadores privados de dispositivos. El reproducer debe distinguir 0 W de una muestra no disponible.
