# Complete guide translations

The four full guides and four checked-in wiki pages below are available in the
24 documentation languages used by [ha-homelab](https://github.com/ha-homelab).
Each edition preserves the complete procedures, limits, evidence requirements
and troubleshooting. English is the canonical source.

This documentation coverage does not change the CLI: message catalogs remain
English, Russian, German and Spanish. Root README editions retain those four
languages. Keep executable examples unchanged; do not invent unsupported
`--lang` options.

| Language | Limits | Contract schema | Usage | Troubleshooting | Wiki |
| --- | --- | --- | --- | --- | --- |
| English | [Open](limits.md) | [Open](schema.md) | [Open](usage.md) | [Open](troubleshooting.md) | [Open](../wiki/Home.md) |
| العربية | [Open](ar/limits.md) | [Open](ar/schema.md) | [Open](ar/usage.md) | [Open](ar/troubleshooting.md) | [Open](../wiki/Home-ar.md) |
| বাংলা | [Open](bn/limits.md) | [Open](bn/schema.md) | [Open](bn/usage.md) | [Open](bn/troubleshooting.md) | [Open](../wiki/Home-bn.md) |
| Čeština | [Open](cs/limits.md) | [Open](cs/schema.md) | [Open](cs/usage.md) | [Open](cs/troubleshooting.md) | [Open](../wiki/Home-cs.md) |
| Deutsch | [Open](de/limits.md) | [Open](de/schema.md) | [Open](de/usage.md) | [Open](de/troubleshooting.md) | [Open](../wiki/Home-de.md) |
| Español | [Open](es/limits.md) | [Open](es/schema.md) | [Open](es/usage.md) | [Open](es/troubleshooting.md) | [Open](../wiki/Home-es.md) |
| فارسی | [Open](fa/limits.md) | [Open](fa/schema.md) | [Open](fa/usage.md) | [Open](fa/troubleshooting.md) | [Open](../wiki/Home-fa.md) |
| Français | [Open](fr/limits.md) | [Open](fr/schema.md) | [Open](fr/usage.md) | [Open](fr/troubleshooting.md) | [Open](../wiki/Home-fr.md) |
| עברית | [Open](he/limits.md) | [Open](he/schema.md) | [Open](he/usage.md) | [Open](he/troubleshooting.md) | [Open](../wiki/Home-he.md) |
| हिन्दी | [Open](hi/limits.md) | [Open](hi/schema.md) | [Open](hi/usage.md) | [Open](hi/troubleshooting.md) | [Open](../wiki/Home-hi.md) |
| Bahasa Indonesia | [Open](id/limits.md) | [Open](id/schema.md) | [Open](id/usage.md) | [Open](id/troubleshooting.md) | [Open](../wiki/Home-id.md) |
| Italiano | [Open](it/limits.md) | [Open](it/schema.md) | [Open](it/usage.md) | [Open](it/troubleshooting.md) | [Open](../wiki/Home-it.md) |
| 日本語 | [Open](ja/limits.md) | [Open](ja/schema.md) | [Open](ja/usage.md) | [Open](ja/troubleshooting.md) | [Open](../wiki/Home-ja.md) |
| 한국어 | [Open](ko/limits.md) | [Open](ko/schema.md) | [Open](ko/usage.md) | [Open](ko/troubleshooting.md) | [Open](../wiki/Home-ko.md) |
| Nederlands | [Open](nl/limits.md) | [Open](nl/schema.md) | [Open](nl/usage.md) | [Open](nl/troubleshooting.md) | [Open](../wiki/Home-nl.md) |
| Polski | [Open](pl/limits.md) | [Open](pl/schema.md) | [Open](pl/usage.md) | [Open](pl/troubleshooting.md) | [Open](../wiki/Home-pl.md) |
| Português | [Open](pt/limits.md) | [Open](pt/schema.md) | [Open](pt/usage.md) | [Open](pt/troubleshooting.md) | [Open](../wiki/Home-pt.md) |
| Русский | [Open](ru/limits.md) | [Open](ru/schema.md) | [Open](ru/usage.md) | [Open](ru/troubleshooting.md) | [Open](../wiki/Home-ru.md) |
| ไทย | [Open](th/limits.md) | [Open](th/schema.md) | [Open](th/usage.md) | [Open](th/troubleshooting.md) | [Open](../wiki/Home-th.md) |
| Türkçe | [Open](tr/limits.md) | [Open](tr/schema.md) | [Open](tr/usage.md) | [Open](tr/troubleshooting.md) | [Open](../wiki/Home-tr.md) |
| Українська | [Open](uk/limits.md) | [Open](uk/schema.md) | [Open](uk/usage.md) | [Open](uk/troubleshooting.md) | [Open](../wiki/Home-uk.md) |
| Tiếng Việt | [Open](vi/limits.md) | [Open](vi/schema.md) | [Open](vi/usage.md) | [Open](vi/troubleshooting.md) | [Open](../wiki/Home-vi.md) |
| 简体中文 | [Open](zh-Hans/limits.md) | [Open](zh-Hans/schema.md) | [Open](zh-Hans/usage.md) | [Open](zh-Hans/troubleshooting.md) | [Open](../wiki/Home-zh-Hans.md) |
| 繁體中文 | [Open](zh-Hant/limits.md) | [Open](zh-Hant/schema.md) | [Open](zh-Hant/usage.md) | [Open](zh-Hant/troubleshooting.md) | [Open](../wiki/Home-zh-Hant.md) |

## Updating a guide

1. Edit the English source and every matching edition in the same pull request.
   Preserve all instructions, cautions, examples, limits and distinctions between
   declarations and physical verification. Do not replace full guides with summaries.
2. Keep commands, executable blocks, machine identifiers, values and external
   references exact. Translate prose and link labels. Links to the eight guide
   families point to the same-language edition; stable English HTML anchors keep
   section links valid even when headings are translated.
3. Retain the single language-navigation marker pair below the title. Arabic,
   Persian and Hebrew prose uses an explicit right-to-left container. Commands
   and navigation remain left-to-right; blank lines around HTML containers are
   required for GitHub Markdown rendering.
4. After reviewing all translations, update the corresponding source digest in
   [translations.json](translations.json). The `digest` function in
   `tools/doc_translations.py` calculates SHA-256 of UTF-8 source content after
   removing only generated navigation and surrounding whitespace. Internal
   whitespace, including blank lines inside executable examples, is preserved.
   Updating a digest acknowledges human/agent review; it does not translate text.
5. Run `python3 tools/doc_translations.py --write` to refresh navigation only,
   then `python3 tools/check_docs.py` and `python3 -m pytest -q`.

The existing CI checks all 192 pages, exact executable blocks and inline
identifiers, heading/list structure, stable anchors, localized link destinations,
complete navigation, RTL direction and source digests. It also checks local
Markdown/HTML link targets and SVG syntax. Automated structure checks cannot
establish linguistic accuracy or physical measurement correctness; review prose
and representative rendered pages as well.

## Wiki publication

The checked-in `wiki/` documents are versioned with the four full `docs/` guides.
Their concise scope is intentional: they link to the full matching-language
guide. Keep their translations complete with respect to the English wiki page.
GitHub serves a separate wiki repository; committing these files updates the
versioned source only. Publish reviewed wiki files through the existing separate
wiki publishing process when needed.

[languages.json](languages.json) defines the language catalog and
[translations.json](translations.json) defines the eight source families. The
navigation tool does not generate or overwrite translated prose.
