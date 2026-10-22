<a id="limits-and-trust-boundary"></a>

# 제한과 신뢰 경계

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../limits.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/limits.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/limits.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/limits.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/limits.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/limits.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/limits.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/limits.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/limits.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/limits.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/limits.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="../it/limits.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/limits.md" lang="ja" dir="ltr">日本語</a> ·
<a href="limits.md" lang="ko" dir="ltr">한국어</a> ·
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
이것은 오프라인 선언 검증기입니다. 보호 제어기, 전기 기술자의 시험 장비, 배선 탐색 서비스 또는 동작을 실행하는 Home Assistant 통합이 아닙니다.

- 총측정값 하나로 알 수 없는 부하 세 개의 정확한 동시 전력을 복원할 수 없습니다. 통계적 추측은 추정값이지 보호용 등급의 측정값이 아닙니다.
- 범위, 출처, 부호 방향, 교정 선언은 운영자가 제공합니다. 거짓 선언은 물리적으로 잘못된 시스템을 구조적으로 유효하게 보이게 할 수 있습니다.
- `complete`는 선언된 잎 노드를 기준으로 완전하다는 뜻이며 배선을 독립 검증했다는 뜻이 아닙니다. 소스 리셋 표식은 신뢰하는 증거이지 기기 증명이 아닙니다.
- W, kW, Wh, kWh, V, A를 지원합니다. 무효/피상 전력, 삼상 대수, CT 포화, 전압 변성기, 카운터 순환, 요금은 모델링하지 않습니다.
- 합계 구성원은 직접 계측기이며 다른 합계가 아닙니다. 전력 합계는 정렬된 타임스탬프를, 전력량 합계는 공통의 명시적 카운터 기점과 정렬된 샘플을 요구합니다.
- 값은 유한한 부동소수점 수입니다. 요금 정산 수준의 십진 회계 시스템이 아닙니다. 교정 계수는 기록만 하고 적용하지 않습니다.
- 현재 샘플과 선택적인 이전 샘플만 확인합니다. 이력 데이터베이스, 이상 탐지기, 드리프트 탐지기, 전체 카운터 무결성 감사가 아닙니다.
- HA 소스 타임스탬프는 존재해야 하며 실제 취득 시간을 나타내야 합니다. 캐시 수신 시각을 조용히 대체값으로 받아들이지 않습니다.
- JSON/YAML 로딩에는 한계가 있습니다. 라이브러리의 `audit` API는 파서가 만든 `Contract`를 기대합니다. 신뢰할 수 없는 객체로 임의의 잘못된 dataclass를 만들지 마세요.
- 파일 입력은 일반 파일만 허용합니다. 마지막 경로 요소의 심볼릭 링크, FIFO, 기기, 디렉터리를 거부하고 비차단 방식으로 연 뒤 읽기 전에 열린 디스크립터를 확인합니다. `O_NOFOLLOW`와 `O_NONBLOCK`이 없는 플랫폼은 파일 입력을 거부합니다. 그런 곳에서는 이미 크기를 제한한 문자열에 `ha_meter_contracts.reader.loads_document`를 사용하세요. 부모 디렉터리의 심볼릭 링크는 샌드박스 경계가 아닙니다. 읽는 중 파일이 커져도 바이트 한계를 강제합니다.
- 검사 통과가 물리 릴레이, 밸브, 모터, 펌프 유량 또는 전기 안전을 증명하지 않습니다. 자동 수리나 재시도를 수행하지 않습니다.

입출력에 운영자가 제공한 엔터티 ID와 시각이 포함될 수 있습니다. 실제 계약/내보내기는 비공개로 유지하세요. 저장소에는 합성 예제만 있습니다. 프로그램은 데이터를 업로드하지 않지만, 보고서를 외부 서비스로 리다이렉트하는 것은 운영자의 선택입니다.
