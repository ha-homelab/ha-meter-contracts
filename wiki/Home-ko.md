<a id="ha-meter-contracts-wiki"></a>

# HA Meter Contracts 위키

<!-- language-navigation:start -->
<p dir="ltr">
<a href="Home.md" lang="en" dir="ltr">English</a> ·
<a href="Home-ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="Home-bn.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="Home-cs.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="Home-de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="Home-es.md" lang="es" dir="ltr">Español</a> ·
<a href="Home-fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="Home-fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="Home-he.md" lang="he" dir="rtl">עברית</a> ·
<a href="Home-hi.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="Home-id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="Home-it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="Home-ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="Home-ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="Home-nl.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="Home-pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="Home-pt.md" lang="pt" dir="ltr">Português</a> ·
<a href="Home-ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="Home-th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="Home-tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="Home-uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="Home-vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="Home-zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="Home-zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
물리 계측기 의미, 합산 토폴로지, 샘플 품질을 오프라인으로 검증합니다. 기기 연결이나 명령은 없습니다.

- [빠른 시작](https://github.com/ha-homelab/ha-meter-contracts/wiki/Usage-ko)
- [계약과 보고서](https://github.com/ha-homelab/ha-meter-contracts/wiki/Contract-ko)
- [문제 해결](https://github.com/ha-homelab/ha-meter-contracts/wiki/Troubleshooting-ko)

멀티탭 전체 계측기는 집계 하나입니다. MQTT 사본은 두 번째 독립 계측기가 아닙니다. 사용 불가는 0이 아닙니다. 이런 구별이 첫 릴리스의 핵심입니다.

위키 소스는 주 저장소에서 버전 관리합니다. 같은 릴리스의 `docs/` 아래에서 완전한 안내서를 24개 문서 언어로 제공하며 위키는 해당 기준 안내서로 연결합니다. CLI는 지원하는 메시지 언어 네 개를 유지합니다.
