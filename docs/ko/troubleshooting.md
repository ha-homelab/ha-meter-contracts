<a id="troubleshooting"></a>

# 문제 해결

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
<a href="troubleshooting.md" lang="ko" dir="ltr">한국어</a> ·
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

## 콘센트 세 개인 멀티탭에서 전력 측정값 세 개를 얻을 수 없음

`scope_outside`는 요청한 개별 결과에 더 넓은 측정값을 사용한다는 뜻입니다. 멀티탭 전체 엔터티 하나를 유지하세요. 개별 전력이 필요하면 독립적이고 범위가 올바른 측정을 추가하세요. 릴레이가 켜졌다고 부하가 전력을 소비한다는 증거가 되지 않으며, 펌프가 전기를 소비한다고 물이 흐른다는 증거도 되지 않습니다.

<a id="a-migrated-sensor-doubles-the-total"></a>

## 이전한 센서가 총량을 두 배로 만듦

`alias_stream`만 있으면 정보입니다. `duplicate_stream`은 두 사본이 합계에 들어갔다는 뜻입니다. 같은 CT 사본에는 같은 출처를 주고 합계에는 하나만 두세요. 검사 경고를 없애려고 출처를 바꾸지 마세요.

![소스 하나와 표현 둘](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## 개별 숫자가 그럴듯하지만 합계 숫자가 없음

`sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap`을 확인하세요. 원본 소스를 갱신하고 취득 시각을 보존하세요. 최신성 예산을 늘리는 것은 정책 변경이지 측정 수리가 아닙니다. 완전한 합계는 선언된 잎 범위를 기준으로 판단하므로 선언도 검토하세요.

![합성 샘플 품질 타임라인](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## 자정에 전력량이 감소함

감소는 실제 리셋, 교체, 정정일 수 있습니다. 정책을 선언하고 실제 소스 증거로부터 `reset_at`을 추가하세요. HA가 값을 재생한 시각은 리셋 표식이 아닙니다. `total_increasing`은 부호 있는 순전력량에 적합하지 않습니다. 기점이 다른 두 카운터는 합산하지 않습니다.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## 전압은 교정된 것 같지만 와트가 여전히 다름

교정은 물리량별입니다. 전압 보정이 전류, 위상 관계, 전력, 누적 전력량을 검증하지 않습니다. 계수 필드는 문서화용일 뿐이며 값에는 이미 의도한 보정이 포함되어야 합니다.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## 다른 파서가 허용하는 YAML이 실패함

타임스탬프를 따옴표로 감싸고 별칭/앵커/사용자 정의 태그와 중복 키를 제거하며 유한한 수를 사용하세요. 오타를 잡도록 알 수 없는 필드는 오류입니다. 두 형식 모두 한계가 적용됩니다. 모호한 YAML 스칼라가 불편하면 교환에 JSON을 쓰세요.

<a id="ha-import-fails-on-timestamps"></a>

## HA 가져오기가 타임스탬프 때문에 실패함

`timestamp_attribute`를 실제 측정 시각 속성으로 지정하세요. `last_reported`는 HA가 수신했다는 것만 증명합니다. 소스 시각이 없으면 이 도구는 최신성을 확인할 수 없으므로 샘플을 사용 불가로 두세요. 가져오기는 오프라인이므로 토큰이나 네트워크 연결을 디버깅할 일은 없습니다.

<a id="safe-issue-report"></a>

## 안전한 이슈 보고

패키지/Python 버전, 안정적인 발견 코드, 최소 합성 계약, 선택한 `--at`, 기대 결과와 실제 결과를 포함하세요. 전체 HA 내보내기, 토큰, 실제 주소, 가정 일정, 비공개 기기 식별자는 첨부하지 마세요. 재현 예제는 0 W 값과 사용 불가 샘플을 구별해야 합니다.
