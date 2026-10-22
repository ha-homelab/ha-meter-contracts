<a id="contract-schema-v1"></a>

# Schéma de contrat v1

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../schema.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/schema.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/schema.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/schema.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/schema.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/schema.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/schema.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="schema.md" lang="fr" dir="ltr">Français</a> ·
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
Le [schema.json](../../schema.json) lisible par machine décrit la structure. L’analyseur Python fait autorité sur les limites ; `audit` ajoute une sémantique physique et temporelle que JSON Schema ne peut pas prouver. Générez le fichier structurel avec `python3 scripts/generate_schema.py`.

<a id="root-and-limits"></a>

## Racine et limites

Obligatoires : entier `schema_version: 1`, `scopes`, `meters`. Facultatif : `sums` (vide par défaut). Les champs inconnus sont rejetés à chaque niveau. Jusqu’à 512 périmètres, 512 compteurs et 128 sommes ; périmètres et compteurs ne doivent pas être vides. Chaque somme comporte 1–512 membres. Entrée UTF-8, au plus 1 048 576 octets, profondeur 16 et 20 000 nœuds de valeurs. Les clés JSON dupliquées, NaN/Infinity et alias/ancres/balises explicites YAML sont rejetés. Mettez les dates YAML entre guillemets pour conserver des chaînes.

Les identifiants ont 1–96 caractères ASCII, commencent par une lettre/un chiffre puis contiennent lettres, chiffres, `.`, `_`, `-`. Ils sont uniques dans chaque collection ; les espaces de noms des périmètres et compteurs sont séparés. Toutes les heures incluent `T` et un fuseau. Les nombres sont finis, non booléens, dans ±10^15 sauf limite plus étroite.

<a id="physical-scopes"></a>

## Périmètres physiques

Chaque périmètre comporte `id`, `kind` (`site`, `circuit`, `strip`, `outlet`, `load`) et éventuellement `parent`. Les parents doivent exister et former une forêt sans cycle. Un compteur sur un parent couvre tous ses descendants. Les types de périmètre sont descriptifs : ils n’infèrent ni tension, phases, caractéristiques nominales, câblage ou parents autorisés. Vous déclarez la topologie réelle.

<a id="meters"></a>

## Compteurs

Champs obligatoires :

- `id`, `scope` : identifiant de mesure unique et périmètre physique déclaré.
- `quantity` : `power`, `energy`, `voltage`, `current`.
- `unit` : respectivement W/kW, Wh/kWh, V, A. L’analyseur accepte le vocabulaire ; l’auditeur vérifie la dimension.
- `kind` : `measured` ou `estimated`. C’est une déclaration, pas une vérification en laboratoire.
- `provenance` : identité stable du flux physique de mesures, **pas** de sa représentation HA/MQTT. Les alias la partagent. Un signe/une grandeur/un périmètre différent avec une même provenance crée un conflit ; chaque alias de ce flux devient indisponible pour les sommes, quel que soit l’ordre d’entrée. Choisissez des provenances séparées pour des canaux physiques réellement distincts.
- `sign` : `nonnegative` pour une amplitude uniquement de consommation/importation/exportation ; `signed` pour un flux bidirectionnel déclaré. Cette version n’infère pas quel sens physique est positif.
- `state_class` : `measurement`, `total`, `total_increasing`.
- `freshness_seconds` : âge admissible positif, 0.001–604800 secondes.

`reset` facultatif : `never`, `periodic`, `device_restart`, `unknown`, `not_applicable` (par défaut). L’énergie exige une politique explicite différente de `not_applicable` et une classe d’état de type total. L’énergie signée ne peut pas utiliser `total_increasing`. Les autres grandeurs exigent `measurement` et `not_applicable`.

`sample`, `previous` facultatifs : null ou objet contenant `value` (nombre ou null), `measured_at` et éventuellement `reset_at`. Le précédent doit être plus ancien. Une baisse de compteur non négatif exige une marque de remise à zéro entre les échantillons ; `never` la rejette. `reset_at` ne doit pas être postérieur à son échantillon et ne concerne que l’énergie. Une sémantique de remise à zéro inconnue produit un avertissement. Un compteur net signé peut légitimement diminuer ; son origine correcte reste la responsabilité du producteur.

`calibration` facultatif : `quantity`, `factor` positif (10^-12–10^12), identifiant synthétique/privé `reference`, `verified_at`. Cela enregistre une preuve pour cette grandeur précise. Les valeurs sont **déjà étalonnées** : le validateur ne réapplique jamais le facteur. Un étalonnage futur ou de tension sur un compteur de puissance est invalide. L’absence d’étalonnage ne prouve pas la précision et n’est pas automatiquement une erreur.

`entity_id`, `timestamp_attribute` facultatifs : correspondance HA hors ligne ; voir [utilisation](usage.md#offline-home-assistant-adapter).

<a id="sums"></a>

## Sommes

Obligatoires : `id`, `scope` cible, liste des identifiants de compteurs dans `meters`, `quantity` (`power` ou `energy`), `coverage` (`partial` ou `complete`). `max_skew_seconds` facultatif : 0–604800, valeur par défaut 2.

Les membres doivent appartenir au périmètre cible, avoir des dimensions et une sémantique de signe compatibles, utiliser des flux physiques différents et ne pas se chevaucher comme parent/enfant ou périmètres identiques. Une somme complète couvre chaque **périmètre feuille déclaré** sous sa cible. Le câblage non déclaré ne peut pas être détecté. Une somme partielle indique explicitement sa couverture partielle. Les sommes imbriquées ne sont pas prises en charge ; les membres référencent toujours des compteurs.

Chaque membre doit fournir des données valides et fraîches ; leurs acquisitions doivent respecter le décalage admissible. L’énergie exige en plus des origines `reset_at` explicites identiques. Cela vérifie l’alignement déclaré, pas la précision de l’accumulation historique. Les sommes sont converties en W ou Wh. Les sommes de courant et tension ne sont volontairement pas prises en charge, leur sens dépendant de la topologie du circuit.

Une somme numérique est indisponible dès qu’une preuve obligatoire ou un contrôle sémantique échoue. Les estimations se propagent sous `kind: estimated`. Deux alias peuvent coexister dans l’inventaire mais pas contribuer tous deux à une somme. Aucun total n’est inféré pour des prises individuelles non mesurées.

<a id="report-v1"></a>

## Rapport v1

Racine : `schema_version`, heure d’évaluation `at` normalisée en UTC, nombres par gravité dans `summary`, `findings` triés et `sums`. Chaque constat comprend `code`, `severity`, `path` de type JSON, `params` structurés ; la CLI ajoute `message`. Chaque somme contient `id`, `scope`, `quantity`, `unit` de base, `value`, `status`, `kind`, `coverage`. Une valeur inconnue est JSON null, jamais NaN.
