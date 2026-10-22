<a id="troubleshooting"></a>

# Dépannage

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../troubleshooting.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/troubleshooting.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/troubleshooting.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/troubleshooting.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/troubleshooting.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/troubleshooting.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/troubleshooting.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="troubleshooting.md" lang="fr" dir="ltr">Français</a> ·
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

## Une multiprise à trois sorties ne produit pas trois mesures de puissance

`scope_outside` signifie qu’un résultat individuel demandé utilise une mesure plus large. Gardez une entité pour toute la multiprise. Ajoutez des mesures indépendantes aux périmètres corrects si une puissance individuelle est nécessaire. Un relais activé ne prouve pas que sa charge consomme ; une pompe consommant de l’électricité ne prouve pas que l’eau circule.

<a id="a-migrated-sensor-doubles-the-total"></a>

## Un capteur migré double le total

`alias_stream` seul est informatif. `duplicate_stream` signifie que les deux copies figurent dans une somme. Donnez la même provenance aux copies d’un même CT et n’en gardez qu’une dans la somme. Ne changez pas la provenance uniquement pour faire taire le contrôle.

![Une source et deux représentations](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## Pas de somme numérique malgré des nombres individuellement plausibles

Vérifiez `sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap`. Actualisez la source d’origine et préservez son heure d’acquisition. Allonger la fraîcheur admissible change une politique, pas une mesure. Une somme complète est jugée par rapport aux feuilles déclarées ; examinez aussi la déclaration.

![Chronologie synthétique de qualité des échantillons](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## L’énergie a diminué à minuit

Une baisse peut être une véritable remise à zéro, un remplacement ou une correction. Déclarez la politique et ajoutez `reset_at` à partir de preuves réelles de la source. L’heure à laquelle HA a rejoué la valeur n’est pas une marque de remise à zéro. `total_increasing` ne convient pas à l’énergie nette signée. Deux compteurs d’origines différentes ne sont pas additionnés.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## La tension semble étalonnée mais les watts diffèrent

L’étalonnage est propre à chaque grandeur. Corriger la tension ne valide ni courant, relation de phase, puissance ou énergie accumulée. Le champ facteur n’est que documentaire : les valeurs doivent déjà inclure la correction voulue.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## YAML échoue alors qu’un autre analyseur l’accepte

Mettez les horodatages entre guillemets, retirez alias/ancres/balises personnalisées et clés dupliquées, et utilisez des nombres finis. Les champs inconnus sont des erreurs afin de détecter les fautes de frappe. Les limites concernent les deux formats. Préférez JSON pour l’échange si les scalaires YAML ambigus sont gênants.

<a id="ha-import-fails-on-timestamps"></a>

## L’import HA échoue sur les horodatages

Définissez `timestamp_attribute` sur un véritable attribut d’heure de mesure. `last_reported` ne prouve que la réception par HA. Sans temps source, l’outil ne peut établir la fraîcheur ; laissez l’échantillon indisponible. Aucun jeton ou réseau n’est à dépanner puisque l’import est hors ligne.

<a id="safe-issue-report"></a>

## Signalement sûr

Incluez versions du paquet/Python, codes stables, contrat synthétique minimal, `--at` choisi, résultat attendu et résultat réel. Ne joignez pas d’export HA complet, jeton, adresse réelle, horaires domestiques ou identifiants privés d’appareils. Le cas reproductible doit distinguer 0 W d’un échantillon indisponible.
