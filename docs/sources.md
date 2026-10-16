# Sources and design references

Reviewed 2026-10-15. These are primary documentation references, not claims of endorsement or device certification.

- [Home Assistant sensor entity and long-term statistics](https://developers.home-assistant.io/docs/core/entity/sensor/#long-term-statistics): `measurement`, `total`, `total_increasing`, reset semantics and units.
- [Home Assistant MQTT sensor](https://www.home-assistant.io/integrations/sensor.mqtt/): availability, expiration and sensor configuration. A cache delivery time must not replace measurement provenance.
- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/): shape of exported state records. This package consumes saved records and does not implement REST access.
- [ESPHome sensor filters](https://esphome.io/components/sensor/#sensor-filters): per-sensor calibration and filtering. A voltage filter cannot establish power accuracy.
- [JSON Schema 2020-12](https://json-schema.org/draft/2020-12): the structural schema vocabulary. Graph and temporal checks additionally run in Python.

The independent project is MIT licensed. Product names identify example device classes; all numeric examples, IDs and illustrations are original synthetic material.
