<a id="contract-schema-v1"></a>

# 계약 스키마 v1

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../schema.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/schema.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/schema.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/schema.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/schema.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/schema.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/schema.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/schema.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/schema.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/schema.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/schema.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="../it/schema.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/schema.md" lang="ja" dir="ltr">日本語</a> ·
<a href="schema.md" lang="ko" dir="ltr">한국어</a> ·
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
기계가 읽는 [schema.json](../../schema.json)은 구조를 설명합니다. 한계에 관한 기준은 Python 파서이며, `audit`은 JSON Schema가 증명할 수 없는 물리적·시간적 의미를 더합니다. `python3 scripts/generate_schema.py`로 구조 파일을 생성하세요.

<a id="root-and-limits"></a>

## 루트와 한계

필수: 정수 `schema_version: 1`, `scopes`, `meters`. 선택: `sums`이며 기본값은 빈 목록입니다. 모든 계약 단계에서 알 수 없는 필드를 거부합니다. 최대 범위 512개, 계측기 512개, 합계 128개이며 범위와 계측기는 비어 있으면 안 됩니다. 각 합계는 구성원 1–512개를 가집니다. 입력은 UTF-8, 최대 1,048,576바이트, 중첩 깊이 16, 값 노드 20,000개입니다. JSON 중복 키, NaN/Infinity, YAML 별칭/앵커/명시적 태그는 거부합니다. YAML 타임스탬프는 따옴표로 감싸 문자열로 유지하세요.

식별자는 1–96자의 ASCII이며 문자/숫자로 시작하고 이후 문자, 숫자, `.`, `_`, `-`를 허용합니다. ID는 각 컬렉션 안에서 고유하며 범위와 계측기 네임스페이스는 별개입니다. 모든 시각은 `T`와 시간대를 포함합니다. 숫자는 유한하고 불리언이 아니어야 하며, 더 좁은 한계를 명시하지 않았다면 ±10^15 안이어야 합니다.

<a id="physical-scopes"></a>

## 물리 범위

각 범위는 `id`, `kind`(`site`, `circuit`, `strip`, `outlet`, `load`), 선택적인 `parent`를 가집니다. 부모는 존재해야 하며 순환 없는 포리스트를 이뤄야 합니다. 부모에 있는 계측기는 모든 자손을 포함합니다. 범위 종류는 설명용이며 전압, 상, 정격, 배선, 허용 부모를 추론하지 않습니다. 실제 토폴로지는 직접 선언합니다.

<a id="meters"></a>

## 계측기

필수 필드:

- `id`, `scope`: 고유 측정 식별자와 선언한 물리 범위.
- `quantity`: `power`, `energy`, `voltage`, `current`.
- `unit`: 각각 W/kW, Wh/kWh, V, A. 파서는 용어를 받아들이고 감사기는 차원을 확인합니다.
- `kind`: `measured` 또는 `estimated`. 실험실 검증이 아니라 선언입니다.
- `provenance`: 물리 측정 스트림의 안정된 식별자이며 HA/MQTT 표현이 **아닙니다**. 별칭 측정값은 이를 공유합니다. 같은 출처에 부호/물리량/범위가 다르면 충돌이며, 입력 순서와 관계없이 충돌 스트림의 모든 별칭을 합계에 사용할 수 없게 됩니다. 실제로 별개인 물리 흐름 채널에는 별도 출처를 지정하세요.
- `sign`: 소비 전용/유입 전용/유출 전용 크기에는 `nonnegative`, 선언된 양방향 흐름에는 `signed`. 이 릴리스는 어느 물리 방향이 양수인지 추론하지 않습니다.
- `state_class`: `measurement`, `total`, `total_increasing`.
- `freshness_seconds`: 양수인 허용 나이, 0.001–604800초.

선택적인 `reset`: `never`, `periodic`, `device_restart`, `unknown`, `not_applicable`(기본값). 전력량은 `not_applicable`이 아닌 명시적 정책과 누적형 상태 클래스를 요구합니다. 부호 있는 전력량은 `total_increasing`을 사용할 수 없습니다. 다른 물리량은 `measurement`와 `not_applicable`을 요구합니다.

선택적인 `sample`, `previous`: null 또는 `value`(수 또는 null), `measured_at`, 선택적인 `reset_at`을 포함한 객체입니다. 이전 샘플은 더 오래되어야 합니다. 음수가 아닌 카운터가 감소하면 샘플 사이의 리셋 표식이 필요하며 `never`는 감소를 거부합니다. `reset_at`은 해당 샘플보다 늦을 수 없고 전력량에만 적용됩니다. 알 수 없는 카운터 리셋 의미는 경고를 만듭니다. 부호 있는 순량 카운터는 정상적으로 감소할 수 있지만 올바른 기점은 여전히 생산자의 책임입니다.

선택적인 `calibration`: `quantity`, 양수 `factor`(10^-12–10^12), 합성/비공개 `reference` 식별자, `verified_at`. 정확히 그 물리량의 증거만 기록합니다. 샘플 값은 **이미 교정된 값**이므로 검증기가 계수를 다시 적용하지 않습니다. 미래 교정이나 전력 계측기에 대한 전압 교정은 무효입니다. 교정이 없다고 정확성이 증명되지는 않으며 자동으로 오류가 되는 것도 아닙니다.

선택적인 `entity_id`, `timestamp_attribute`: 오프라인 HA 매핑이며 [사용법](usage.md#offline-home-assistant-adapter)을 참고하세요.

<a id="sums"></a>

## 합계

필수: `id`, 대상 `scope`, `meters`의 계측기 ID 목록, `quantity`(`power` 또는 `energy`), `coverage`(`partial` 또는 `complete`). 선택적인 `max_skew_seconds`: 0–604800, 기본값 2.

구성원은 대상 범위 안에 있고, 차원과 부호 의미가 일치하고, 서로 다른 물리 스트림을 사용하며, 부모/자식 또는 동일 범위로 겹치지 않아야 합니다. 완전한 합계는 대상 아래의 모든 **선언된 잎 범위**를 포함해야 합니다. 선언하지 않은 배선은 탐지할 수 없습니다. 부분 합계는 부분적인 범위라고 명시적으로 보고합니다. 중첩 합계는 지원하지 않으며 구성원은 항상 계측기를 참조합니다.

모든 구성원에 유효하고 최신인 데이터가 있어야 하며 취득 시각은 허용된 차이 이내여야 합니다. 전력량은 추가로 동일한 명시적 `reset_at` 기점을 요구합니다. 이것은 선언된 정렬을 확인하며 과거 카운터 누적의 정확성을 확인하지 않습니다. 합계는 W 또는 Wh로 변환됩니다. 전류와 전압 합계는 회로 토폴로지에 따라 의미가 달라 의도적으로 지원하지 않습니다.

필수 증거 또는 의미 검사 중 하나라도 실패하면 숫자 합계는 사용할 수 없습니다. 추정값은 `kind: estimated`로 전파됩니다. 별칭 둘은 목록에 공존할 수 있지만 둘 다 합계에 기여할 수는 없습니다. 측정하지 않은 개별 콘센트의 총량을 추론하지 않습니다.

<a id="report-v1"></a>

## 보고서 v1

루트: `schema_version`, UTC로 정규화한 평가 시각 `at`, 심각도별 수를 담은 `summary`, 정렬된 `findings`, `sums`. 각 발견은 `code`, `severity`, JSON 형식 `path`, 구조화된 `params`를 포함하며 CLI가 `message`를 추가합니다. 각 합계는 `id`, `scope`, `quantity`, 기본 `unit`, `value`, `status`, `kind`, `coverage`를 포함합니다. 알 수 없는 값은 JSON null이며 NaN은 절대 사용하지 않습니다.
