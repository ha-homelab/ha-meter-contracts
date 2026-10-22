<a id="usage"></a>

# Utilização

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../usage.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/usage.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/usage.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/usage.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/usage.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/usage.md" lang="es" dir="ltr">Español</a> ·
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
<a href="usage.md" lang="pt" dir="ltr">Português</a> ·
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

## Auditoria

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` aceita um tempo ISO 8601 com fuso horário. O valor predefinido é o UTC atual. Com a mesma entrada, tempo e língua, o JSON é determinístico. Uma amostra permanece recente até ao limite inclusivo de `freshness_seconds`; só fica obsoleta depois. Uma amostra futura é inválida, sem tolerância implícita ao desvio dos relógios.

Códigos de saída: 0 = sem erros/avisos; 1 = problema semântico ou de qualidade da amostra; 2 = erro de entrada/CLI. Informações como um alias não utilizado não provocam falha. `--json` escreve relatórios e objetos de erro de entrada em stdout. Sem a opção, o texto da auditoria vai para stdout e os erros de entrada para stderr. Uma saída por pipe interrompida devolve 2.

Não use `|| true` em CI para ocultar resultados. Exemplos intencionalmente inválidos devem verificar explicitamente a saída 1. Ajuda e versão devolvem 0. `import-ha` escreve sempre um contrato JSON; `--json` não altera esse esquema.

<a id="python-library"></a>

## Biblioteca Python

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` cria dataclasses imutáveis; `InputError` expõe `code`, `path`, `params`. Use o parser em cada fronteira de entrada não fiável. `audit` espera um `Contract` validado e não traduz ocorrências. A CLI acrescenta valores `message` localizados. Na biblioteca, o chamador escolhe explicitamente o instante de avaliação. Nenhuma API altera a entrada ou escreve ficheiros.

<a id="offline-home-assistant-adapter"></a>

## Adaptador offline Home Assistant

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

Mapeie `entity_id` e `timestamp_attribute` em cada medidor pretendido. A exportação é um array de estados HA com `entity_id`, `state` e `attributes`. O atributo mapeado tem de conter o tempo ISO original da medição com fuso horário. `attributes.unit_of_measurement` tem de ter a mesma dimensão; W/kW e Wh/kWh são convertidos para a unidade do contrato.

Só valores mapeados e tempos da origem são copiados. Outros atributos, incluindo nomes amigáveis, são ignorados. Uma amostra estritamente mais recente move a existente para `previous`. Repetir o mesmo valor com o mesmo tempo de origem é idempotente; uma amostra mais antiga ou valor contraditório no mesmo instante é rejeitado como `ha_sample_order`. Entidades ausentes e estados `unknown`/`unavailable` apagam a amostra; não viram zero. Tempo ausente, unidade incompatível, valor malformado ou ID de entidade duplicado fazem a importação falhar com 2. Medidores não mapeados ficam inalterados. Contratos privados podem conter IDs de entidades; exemplos públicos usam identificadores sintéticos.

Uma exportação HA normal frequentemente não contém o tempo original. Nesse caso, o adaptador recusa deliberadamente inventá-lo. Obtenha dados do dispositivo com tempo ou deixe o medidor indisponível. Tempos de receção/atualização HA não provam aquisição no dispositivo. O adaptador nunca se liga a `/api/states` nem lê tokens. Não copia marcadores de reinicialização de energia do HA; acrescente evidência verificada separadamente antes de somar energia.

<a id="suggested-workflow"></a>

## Procedimento sugerido

1. Declare a árvore de âmbitos físicos e a proveniência das origens a partir da documentação da instalação.
2. Comece com um medidor e um exemplo sintético fixo.
3. Exporte apenas as observações necessárias para um ficheiro privado.
4. Execute a auditoria e reveja cada ocorrência antes de mudar automações dependentes.
5. Preserve os tempos originais e a evidência de calibração durante migrações.

O pacote não executa correções, renomeia entidades, reinicializa dispositivos ou implementa automações.
