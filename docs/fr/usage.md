<a id="usage"></a>

# Utilisation

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../usage.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/usage.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/usage.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/usage.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/usage.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/usage.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/usage.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="usage.md" lang="fr" dir="ltr">Français</a> ·
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

## Audit

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` accepte un horodatage ISO 8601 avec fuseau. Par défaut, il s’agit de l’heure UTC courante. À entrée, heure et langue identiques, le JSON est déterministe. Un échantillon reste frais jusqu’à la limite `freshness_seconds` incluse, puis devient périmé. Un échantillon futur est invalide, sans tolérance implicite de décalage d’horloge.

Codes de sortie : 0 = aucune erreur/aucun avertissement ; 1 = constat sémantique ou de qualité d’échantillon ; 2 = erreur d’entrée/CLI. Une information, tel un alias inutilisé, ne fait pas échouer la vérification. `--json` place rapports et objets d’erreur d’entrée sur stdout. Sans cette option, le rapport texte va sur stdout et les erreurs d’entrée sur stderr. Un tube de sortie rompu renvoie 2.

N’utilisez pas `|| true` en CI pour masquer les constats. Les exemples volontairement invalides doivent vérifier explicitement le code 1. Aide et version renvoient 0. `import-ha` écrit toujours un contrat JSON ; `--json` n’en change pas le schéma.

<a id="python-library"></a>

## Bibliothèque Python

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` crée des dataclasses immuables ; `InputError` expose `code`, `path`, `params`. Utilisez cet analyseur à chaque frontière d’entrée non fiable. `audit` attend un `Contract` validé et ne traduit pas les constats. La CLI ajoute les valeurs `message` localisées. Dans la bibliothèque, l’appelant choisit explicitement l’heure d’évaluation. Aucune API ne modifie l’entrée ni n’écrit de fichiers.

<a id="offline-home-assistant-adapter"></a>

## Adaptateur Home Assistant hors ligne

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

Associez `entity_id` et `timestamp_attribute` à chaque compteur voulu. L’export est un tableau d’objets d’état HA avec `entity_id`, `state` et `attributes`. L’attribut associé doit contenir l’heure de mesure ISO d’origine avec fuseau. `attributes.unit_of_measurement` doit avoir la même dimension ; W/kW et Wh/kWh sont convertis dans l’unité du contrat.

Seules les valeurs associées et les temps source sont copiés. Les autres attributs, dont les noms conviviaux, sont ignorés. Un échantillon strictement plus récent déplace l’existant dans `previous`. Rejouer la même valeur avec le même horodatage source est idempotent ; un échantillon plus ancien ou une valeur différente au même horodatage est rejetée comme `ha_sample_order`. Les entités absentes et états `unknown`/`unavailable` effacent l’échantillon sans devenir zéro. Un temps source absent, une unité incompatible, une valeur mal formée ou un identifiant d’entité dupliqué fait échouer l’import avec 2. Les compteurs non associés restent inchangés. Les contrats privés peuvent contenir des identifiants d’entités ; les exemples publics emploient des identifiants synthétiques.

Un export HA ordinaire n’a souvent pas d’horodatage source d’origine. L’adaptateur refuse alors volontairement d’en inventer un. Obtenez des données d’appareil horodatées ou conservez le compteur indisponible. Les heures de réception/mise à jour HA ne prouvent pas l’acquisition par l’appareil. L’adaptateur ne se connecte jamais à `/api/states` et ne lit pas de jeton. Il ne copie pas les marques de remise à zéro d’énergie depuis HA ; ajoutez une preuve vérifiée séparément avant de sommer l’énergie.

<a id="suggested-workflow"></a>

## Procédure conseillée

1. Déclarez l’arbre des périmètres physiques et la provenance des sources à partir de la documentation du câblage.
2. Commencez par un compteur et un exemple synthétique fixe.
3. Exportez uniquement les observations nécessaires dans un fichier privé.
4. Auditez et examinez chaque constat avant de changer une automatisation en aval.
5. Préservez temps source et preuves d’étalonnage lors des migrations.

Ce paquet ne répare rien, ne renomme pas d’entités, ne réinitialise pas d’appareils et ne déploie pas d’automatisations.
