<a id="limits-and-trust-boundary"></a>

# Limites et frontière de confiance

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../limits.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/limits.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/limits.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/limits.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/limits.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/limits.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/limits.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="limits.md" lang="fr" dir="ltr">Français</a> ·
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
Il s’agit d’un validateur hors ligne de déclarations, pas d’un contrôleur de protection, d’un instrument de contrôle d’électricien, d’un service de découverte du câblage ni d’une intégration Home Assistant exécutant des actions.

- Une mesure totale ne permet pas de retrouver la puissance simultanée exacte de trois charges inconnues. Des suppositions statistiques seraient des estimations, pas des mesures adaptées à la protection.
- Le périmètre, la provenance, le sens du signe et les déclarations d’étalonnage viennent de l’opérateur. Des déclarations mensongères peuvent rendre structurellement valide un système physique incorrect.
- `complete` signifie complet par rapport aux feuilles déclarées, pas à un câblage vérifié indépendamment. Une marque de remise à zéro de la source est un élément de confiance, pas une attestation du dispositif.
- W, kW, Wh, kWh, V et A sont pris en charge. Ne sont pas modélisés : puissance réactive/apparente, algèbre triphasée, saturation des CT, transformateurs de tension, débordement des compteurs ou tarifs.
- Les membres d’une somme sont des compteurs directs, pas d’autres sommes. Les sommes de puissance exigent des horodatages alignés. Les sommes d’énergie exigent une origine explicite commune des compteurs et des échantillons alignés.
- Les valeurs sont des nombres flottants finis. Ce n’est pas une comptabilité décimale de qualité facturation. Les facteurs d’étalonnage sont enregistrés, pas appliqués.
- Seuls un échantillon courant et un précédent facultatif sont vérifiés. Ce n’est ni une base historique, ni un détecteur d’anomalies ou de dérive, ni un audit complet de l’intégrité des compteurs.
- Les horodatages source HA doivent exister et représenter réellement l’acquisition. Les heures de réception du cache ne sont pas acceptées silencieusement en remplacement.
- Le chargement JSON/YAML est borné ; l’API de bibliothèque `audit` attend un `Contract` produit par l’analyseur. Ne construisez pas de dataclasses arbitraires mal formées à partir d’objets non fiables.
- L’entrée fichier n’accepte que les fichiers ordinaires. Elle rejette les liens symboliques du dernier composant, FIFO, dispositifs et répertoires, ouvre sans blocage et vérifie le descripteur ouvert avant lecture. Les plateformes sans `O_NOFOLLOW` et `O_NONBLOCK` refusent les fichiers ; utilisez-y `ha_meter_contracts.reader.loads_document` avec une chaîne déjà bornée. Les liens symboliques des répertoires parents ne constituent pas une frontière de bac à sable. La limite d’octets reste applicable si le fichier grossit pendant sa lecture.
- Une réussite ne prouve ni le fonctionnement physique d’un relais, d’une vanne, d’un moteur, ni le débit d’une pompe ou la sécurité électrique. Aucune réparation ni nouvelle tentative automatique n’est effectuée.

Les entrées et sorties peuvent contenir des identifiants d’entités et heures fournis par l’opérateur. Gardez privés les contrats et exports réels. Le dépôt ne contient que des exemples synthétiques. Le programme n’envoie pas de données, mais rediriger son rapport vers un service externe relève du choix de l’opérateur.
