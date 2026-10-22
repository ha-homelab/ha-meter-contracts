<a id="limits-and-trust-boundary"></a>

# Límites y frontera de confianza

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../limits.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/limits.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/limits.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/limits.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/limits.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="limits.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/limits.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/limits.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/limits.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/limits.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/limits.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="../it/limits.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/limits.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/limits.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/limits.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="../pl/limits.md" lang="pl" dir="ltr">Polski</a> ·
<a href="../pt/limits.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/limits.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/limits.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/limits.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/limits.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/limits.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/limits.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/limits.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
Es un validador de declaraciones sin conexión, no un controlador de protección, un instrumento de pruebas de electricista, un servicio de descubrimiento del cableado ni una integración de Home Assistant que ejecute acciones.

- Una medida total no permite recuperar la potencia simultánea exacta de tres cargas desconocidas. Las conjeturas estadísticas serían estimaciones, no medidas aptas para protección.
- El operador declara el alcance, la procedencia, el sentido del signo y la calibración. Las declaraciones falsas pueden hacer que un sistema físicamente inválido parezca estructuralmente válido.
- `complete` significa completo respecto a las hojas declaradas, no respecto a un cableado verificado de forma independiente. Una marca de reinicio de la fuente es evidencia de confianza, no una atestación del dispositivo.
- Se admiten W, kW, Wh, kWh, V y A. No se modelan potencia reactiva/aparente, álgebra trifásica, saturación de CT, transformadores de tensión, desbordamiento de contadores ni tarifas.
- Los miembros de una suma son medidores directos, no otras sumas. Las sumas de potencia requieren marcas temporales alineadas. Las de energía requieren un origen de contador explícito común y muestras alineadas.
- Los valores son números finitos de coma flotante. No es un sistema contable decimal apto para facturación. Los factores de calibración se registran, no se aplican.
- Solo se comprueba una muestra actual y una anterior opcional. No es una base histórica, un detector de anomalías o deriva ni una auditoría completa de integridad del contador.
- Las marcas temporales de origen de HA deben existir y representar realmente la adquisición. No se aceptan silenciosamente fechas de recepción de caché como sustitutas.
- La carga JSON/YAML está acotada; la API de biblioteca `audit` espera un `Contract` producido por el analizador. No construya dataclasses arbitrarias mal formadas a partir de objetos no fiables.
- La entrada de archivos acepta solo archivos regulares. Rechaza enlaces simbólicos en el último componente, FIFO, dispositivos y directorios; abre sin bloqueo y comprueba el descriptor abierto antes de leer. Las plataformas sin `O_NOFOLLOW` y `O_NONBLOCK` rechazan la entrada de archivos; allí utilice `ha_meter_contracts.reader.loads_document` con una cadena ya acotada. Los enlaces simbólicos en directorios superiores no son una frontera de aislamiento. El límite de bytes se mantiene aunque el archivo crezca durante la lectura.
- Un resultado aprobado no demuestra el funcionamiento físico de relés, válvulas, motores, caudal de bombas ni seguridad eléctrica. No se realizan reparaciones ni reintentos automáticos.

Las entradas y salidas pueden contener identificadores de entidades y tiempos suministrados por el operador. Mantenga privados los contratos y exportaciones reales. El repositorio solo incluye ejemplos sintéticos. El programa no sube datos, pero redirigir su informe a un servicio externo es decisión del operador.
