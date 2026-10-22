<a id="usage"></a>

# 사용법

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
<a href="usage.md" lang="ko" dir="ltr">한국어</a> ·
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

## 감사

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at`은 시간대가 있는 ISO 8601 타임스탬프를 받습니다. 기본값은 현재 UTC입니다. 입력, 시각, 언어가 같으면 JSON 출력은 결정적입니다. 샘플은 `freshness_seconds` 경계를 포함하여 최신이며, 그 경계를 넘은 뒤에만 오래된 값이 됩니다. 미래 샘플은 무효이고 암묵적인 시계 오차 허용은 없습니다.

종료 코드: 0은 오류/경고 없음, 1은 의미 또는 샘플 품질 발견, 2는 입력/CLI 오류입니다. 쓰지 않는 별칭 같은 정보 항목은 검사를 실패시키지 않습니다. `--json`은 감사 보고서와 입력 오류 객체 모두를 stdout에 출력합니다. 없으면 감사 텍스트는 stdout, 입력 오류는 stderr로 갑니다. 출력 파이프가 끊어지면 2를 반환합니다.

CI에서 발견 사항을 숨기려고 `|| true`를 사용하지 마세요. 의도적으로 잘못된 예제는 종료 1을 명시적으로 확인해야 합니다. 도움말과 버전은 0으로 끝납니다. `import-ha`는 항상 JSON 계약을 출력하며 `--json`이 스키마를 바꾸지는 않습니다.

<a id="python-library"></a>

## Python 라이브러리

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract`는 동결된 dataclass를 만들며 `InputError`는 `code`, `path`, `params`를 노출합니다. 신뢰할 수 없는 입력 경계마다 이 파서를 사용하세요. `audit`은 검증된 `Contract`를 기대하고 발견 사항을 번역하지 않습니다. CLI가 현지화된 `message` 값을 추가합니다. 라이브러리에서는 호출자가 평가 시각을 명시적으로 선택합니다. 두 API 모두 입력을 변경하거나 파일을 쓰지 않습니다.

<a id="offline-home-assistant-adapter"></a>

## 오프라인 Home Assistant 어댑터

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

원하는 계측기마다 `entity_id`와 `timestamp_attribute`를 매핑하세요. 내보내기는 `entity_id`, `state`, `attributes`가 있는 HA 상태 객체 배열입니다. 매핑된 속성은 원본의 시간대 포함 ISO 측정 시각을 담아야 합니다. `attributes.unit_of_measurement`는 차원이 같아야 하며 W/kW와 Wh/kWh는 계약 단위로 변환됩니다.

매핑된 값과 소스 시각만 복사합니다. 친숙한 이름을 포함한 다른 속성은 무시합니다. 엄격히 더 최신인 샘플은 기존 샘플을 `previous`로 옮깁니다. 같은 소스 시각의 같은 값을 재생하는 것은 멱등입니다. 더 오래된 샘플이나 같은 시각에 다른 값은 `ha_sample_order`로 거부합니다. 없는 엔터티와 `unknown`/`unavailable` 상태는 샘플을 지우며 0이 되지 않습니다. 소스 시각 누락, 호환되지 않는 단위, 잘못된 값, 중복 엔터티 ID는 종료 2로 가져오기를 실패시킵니다. 매핑하지 않은 계측기는 그대로입니다. 비공개 계약에는 엔터티 ID가 있을 수 있지만 공개 예제는 합성 식별자를 사용합니다.

일반 HA 내보내기에는 원본 소스 시각이 없는 경우가 많습니다. 그 경우 어댑터는 의도적으로 시각을 만들어내지 않습니다. 시각이 있는 기기 데이터를 확보하거나 계측기를 사용 불가로 두세요. HA 수신/갱신 시각은 기기 취득 시각을 증명하지 않습니다. 어댑터는 `/api/states`에 연결하거나 토큰을 읽지 않습니다. HA에서 전력량 리셋 표식을 복사하지 않으므로 전력량 합계를 내기 전에 검증된 리셋 증거를 별도로 추가하세요.

<a id="suggested-workflow"></a>

## 권장 작업 흐름

1. 배선 문서에서 물리 범위 트리와 소스 출처를 선언하세요.
2. 계측기 하나와 고정된 합성 예제로 시작하세요.
3. 필요한 관측값만 비공개 파일에 내보내세요.
4. 하위 자동화를 바꾸기 전에 감사하고 각 발견을 검토하세요.
5. 마이그레이션 중 원본 소스 시각과 교정 증거를 보존하세요.

이 패키지는 수정 조치, 엔터티 이름 변경, 기기 리셋, 자동화 배포를 수행하지 않습니다.
