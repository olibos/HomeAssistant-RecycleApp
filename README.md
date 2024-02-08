# Home Assistant RecycleApp Integration
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=olibos_HomeAssistant-RecycleApp&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=olibos_HomeAssistant-RecycleApp)

Integrate [RecycleApp](https://recycleapp.be/) into your Home Assistant.

## Installation
* Install HACS Repository:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=olibos&repository=HomeAssistant-RecycleApp&category=integration)
* Restart Home Assistant
* Install the Integration:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=recycle_app)
* Complete the setup process:

![image](https://user-images.githubusercontent.com/6031263/210235247-a685013c-5dc9-49c5-a8a0-372d08a215fb.png)

## Date Format
By default, dates are in Home Assistant date format: %Y-%m-%d

You can customize the format in the `configure` of the device:

![image](https://github.com/olibos/HomeAssistant-RecycleApp/assets/6031263/7eec3a92-4d72-4908-aa15-72aec30446fc)

The formatting is based on [Python date formatting](https://docs.python.org/3/library/datetime.html#format-codes).

## Usage Samples

### Dashboard with next pickups
With [entity-filter](https://www.home-assistant.io/dashboards/entity-filter/):
![entity-filter](docs/images/entity-filter.png)
```yaml

type: entity-filter
entities:
  - sensor.pmc
  - sensor.papier
  - sensor.dechets_non_recyclables_sac
  - sensor.dechets_biodegradables
state_filter:
  - operator: <=
    value: 1
    attribute: days
card:
  type: entities
```

### Templates
![templates](docs/images/templates.png)

### Tomorrow's Pickup(s)
#### Template helper
![tomorrows](docs/images/tomorrow.png)
#### Code:
```jinja
{% set tomorrow_pickups = namespace(entities=[]) %}
{% set collect_types = ['sensor.dechets_non_recyclables_sac', 'sensor.pmc', 'sensor.papier'] %}
{% for collect_type in collect_types %}
  {% if state_attr(collect_type, 'days') == 1 %}
    {% set tomorrow_pickups.entities = tomorrow_pickups.entities + [state_attr(collect_type, 'friendly_name')] %}
  {% endif %}
{% endfor %}
{{ tomorrow_pickups.entities |join(' - ') }}
```

#### Notification
```yml
alias: Waste collection
description: ""
trigger:
  - platform: time
    at: "19:00:00"
condition:
  - condition: template
    value_template: >-
      {% if is_state('sensor.tomorrow_s_pickup_s', '') %}false{% else %}true{%
      endif %}
action:
  - service: notify.mobile_app_poco_f5
    data:
      message: Tomorrow waste collection of {{states('sensor.tomorrow_s_pickup_s')}}
mode: single
```
Thanks to [@MathiasVandePol](https://github.com/MathiasVandePol) for the sample.

## Bug, ideas?
If some collections are missing, you find a bug or have enhancement ideas don't hesitate to open an [issue](https://github.com/olibos/HomeAssistant-RecycleApp/issues/new).
