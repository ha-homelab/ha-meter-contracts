<a id="troubleshooting"></a>

# Resolução de problemas

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../troubleshooting.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/troubleshooting.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/troubleshooting.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/troubleshooting.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/troubleshooting.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/troubleshooting.md" lang="es" dir="ltr">Español</a> ·
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
<a href="troubleshooting.md" lang="pt" dir="ltr">Português</a> ·
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

## Uma extensão de três tomadas não produz três leituras de potência

`scope_outside` significa que um resultado individual pedido usa uma medição mais abrangente. Mantenha uma entidade para toda a extensão. Para potência individual, precisa de medições independentes com âmbito correto. Um relé ligado não prova que a carga consome; uma bomba a consumir eletricidade não prova caudal de água.

<a id="a-migrated-sensor-doubles-the-total"></a>

## Um sensor migrado duplica o total

`alias_stream` sozinho é informativo. `duplicate_stream` significa que ambas as cópias estão na soma. Dê às cópias do mesmo CT a mesma proveniência e mantenha apenas uma na soma. Não mude a proveniência só para silenciar a verificação.

![Uma origem e duas representações](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## Não há soma numérica apesar de valores plausíveis

Verifique `sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap`. Atualize a origem real e conserve o tempo de aquisição. Aumentar a idade permitida muda a política, não repara a medição. Uma soma completa é avaliada contra as folhas declaradas: verifique também a declaração.

![Cronologia sintética da qualidade das amostras](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## A energia diminuiu à meia-noite

A descida pode ser uma reinicialização real, substituição ou correção. Declare a política e acrescente `reset_at` de evidência real da origem. O tempo de uma repetição HA não é um marcador de reinicialização. `total_increasing` não serve para energia líquida com sinal. Contadores com origens diferentes não são somados.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## A tensão parece calibrada mas os watts diferem

A calibração é específica da grandeza. Corrigir tensão não valida corrente, relação de fase, potência ou energia acumulada. O campo do fator é apenas documental: os valores já devem conter a correção pretendida.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## YAML falha embora outro parser o aceite

Coloque tempos entre aspas, remova aliases/âncoras/etiquetas personalizadas e chaves duplicadas, use números finitos. Campos desconhecidos são erros para detetar gralhas. Os limites aplicam-se aos dois formatos. Use JSON no intercâmbio se escalares YAML ambíguos causarem problemas.

<a id="ha-import-fails-on-timestamps"></a>

## A importação HA falha nos tempos

Configure `timestamp_attribute` para um atributo real do tempo de medição. `last_reported` prova apenas receção pelo HA. Sem tempo da origem, a ferramenta não pode estabelecer atualidade; deixe a amostra indisponível. Não há tokens ou ligações a diagnosticar: a importação é offline.

<a id="safe-issue-report"></a>

## Relato seguro de problemas

Inclua versões do pacote/Python, códigos estáveis, contrato sintético mínimo, `--at` escolhido, resultado esperado e real. Não anexe a exportação HA completa, tokens, morada real, horários domésticos ou IDs privados de dispositivos. No exemplo de reprodução, 0 W e amostra indisponível devem continuar distintos.
