<a id="contract-schema-v1"></a>

# Esquema de contrato v1

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../schema.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/schema.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/schema.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/schema.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/schema.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/schema.md" lang="es" dir="ltr">Español</a> ·
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
<a href="schema.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/schema.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/schema.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/schema.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/schema.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/schema.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/schema.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/schema.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
O [schema.json](../../schema.json) legível por máquina descreve a estrutura. O parser Python é a autoridade para os limites; `audit` acrescenta semântica física e temporal que JSON Schema não pode provar. Gere o ficheiro estrutural com `python3 scripts/generate_schema.py`.

<a id="root-and-limits"></a>

## Raiz e limites

Obrigatórios: inteiro `schema_version: 1`, `scopes`, `meters`. Opcional: `sums` (vazio por predefinição). Campos desconhecidos são rejeitados em todos os níveis. Máximo de 512 âmbitos, 512 medidores e 128 somas; âmbitos e medidores não podem estar vazios. Cada soma tem 1–512 membros. Entrada UTF-8, máximo de 1.048.576 bytes, profundidade 16 e 20.000 nós de valor. Chaves JSON duplicadas, NaN/Infinity e aliases/âncoras/etiquetas explícitas YAML são rejeitados. Coloque os tempos YAML entre aspas para continuarem a ser cadeias.

Os identificadores têm 1–96 caracteres ASCII: primeiro letra/dígito, depois letras, dígitos, `.`, `_`, `-`. Os IDs são únicos em cada coleção; âmbitos e medidores têm espaços de nomes separados. Todos os tempos incluem `T` e fuso horário. Os números são finitos, não booleanos, dentro de ±10^15, salvo limites mais estritos.

<a id="physical-scopes"></a>

## Âmbitos físicos

Cada âmbito tem `id`, `kind` (`site`, `circuit`, `strip`, `outlet`, `load`) e `parent` opcional. Os pais têm de existir e formar uma floresta acíclica. Um medidor num pai abrange todos os descendentes. Os tipos de âmbito são descritivos: não deduzem tensão, fases, valores nominais, cablagem ou pais permitidos. A topologia real é declarada pelo utilizador.

<a id="meters"></a>

## Medidores

Campos obrigatórios:

- `id`, `scope`: identificador único da leitura e âmbito físico declarado.
- `quantity`: `power`, `energy`, `voltage`, `current`.
- `unit`: respetivamente W/kW, Wh/kWh, V, A. O parser aceita o vocabulário; o auditor verifica a dimensão.
- `kind`: `measured` ou `estimated`. É uma declaração, não uma verificação de laboratório.
- `provenance`: identidade estável do fluxo físico de medições, **não** da representação HA/MQTT. Leituras alias partilham-na. Sinais/grandezas/âmbitos diferentes com uma proveniência criam um conflito; todos os aliases desse fluxo ficam indisponíveis para somas, independentemente da ordem da entrada. Use proveniências diferentes para canais físicos realmente distintos.
- `sign`: `nonnegative` para magnitudes apenas de consumo/importação/exportação; `signed` para um fluxo bidirecional declarado. Esta versão não deduz qual direção física é positiva.
- `state_class`: `measurement`, `total`, `total_increasing`.
- `freshness_seconds`: idade máxima positiva, 0.001–604800 segundos.

`reset` opcional: `never`, `periodic`, `device_restart`, `unknown`, `not_applicable` (predefinição). Energia exige uma política explícita diferente de `not_applicable` e uma classe de estado de tipo total. Energia com sinal não pode usar `total_increasing`. As restantes grandezas exigem `measurement` e `not_applicable`.

`sample`, `previous` opcionais: null ou objeto com `value` (número ou null), `measured_at`, `reset_at` opcional. A amostra anterior tem de ser mais antiga. Uma descida de contador não negativo exige um marcador de reinicialização entre amostras; `never` rejeita-o. `reset_at` não pode ser posterior à sua amostra e aplica-se apenas à energia. Semântica de reinicialização desconhecida gera aviso. Um contador líquido com sinal pode diminuir legitimamente; a origem correta continua a ser responsabilidade do produtor.

`calibration` opcional: `quantity`, `factor` positivo (10^-12–10^12), identificador sintético/privado `reference`, `verified_at`. Regista evidência para essa grandeza exata. Os valores estão **já calibrados**: o validador nunca reaplica o fator. Calibração futura ou calibração de tensão num medidor de potência é inválida. A ausência de calibração não prova exatidão nem é automaticamente um erro.

`entity_id`, `timestamp_attribute` opcionais: mapeamento HA offline; consulte [utilização](usage.md#offline-home-assistant-adapter).

<a id="sums"></a>

## Somas

Obrigatórios: `id`, `scope` de destino, lista de IDs de medidores em `meters`, `quantity` (`power` ou `energy`), `coverage` (`partial` ou `complete`). `max_skew_seconds` opcional: 0–604800, predefinição 2.

Os membros devem pertencer ao âmbito de destino, ter dimensões e semântica de sinal compatíveis, usar fluxos físicos distintos e não se sobrepor como pai/filho ou âmbitos idênticos. Uma soma completa cobre cada **âmbito folha declarado** sob o destino. Cablagem não declarada não pode ser detetada. Uma soma parcial declara explicitamente cobertura parcial. Somas aninhadas não são suportadas; os membros referem sempre medidores.

Todos os membros têm de ter dados válidos e recentes; os tempos de aquisição devem estar dentro do desvio permitido. Energia exige também origens `reset_at` explícitas idênticas. Isto verifica o alinhamento declarado, não a exatidão da acumulação histórica. As somas são convertidas para W ou Wh. Somas de corrente e tensão são intencionalmente excluídas, porque dependem da topologia do circuito.

Uma soma numérica fica indisponível se faltar evidência exigida ou falhar uma verificação semântica. Estimativas propagam-se como `kind: estimated`. Dois aliases podem coexistir no inventário, mas não podem ambos contribuir para uma soma. Não se deduz qualquer total para tomadas individuais não medidas.

<a id="report-v1"></a>

## Relatório v1

Raiz: `schema_version`, instante de avaliação `at` normalizado em UTC, contagens por gravidade em `summary`, `findings` ordenados e `sums`. Cada ocorrência contém `code`, `severity`, `path` em estilo JSON, `params` estruturados; a CLI acrescenta `message`. Cada soma contém `id`, `scope`, `quantity`, `unit` base, `value`, `status`, `kind`, `coverage`. Valores desconhecidos são JSON null, nunca NaN.
