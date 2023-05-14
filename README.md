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

## Migration from v1.x to >= v1.5.0
This new version will retrieve labels and color from Fostplus API.

You need to migrate the data structure of this integration, you should see this warning in HA logs:
![image](https://user-images.githubusercontent.com/6031263/214088093-a8bd21c4-0ba1-4570-982c-5242ab1f8078.png)

To update:
- Settings
- Devices
- Select this integration
- Click on "Configure" and in the popup click "Submit"

To validate, restart HA and the warning should be erased.

If you've multiple addresses configured, repeat the same process for each address.

Normally, all existing sensor should keep their IDs.

## Breaking changes V2
In V2, the old data structure is completely removed, so please update it before 😉

## Bug, ideas?
If some collections are missing, you find a bug or have enhancement ideas don't hesitate to open an [issue](https://github.com/olibos/HomeAssistant-RecycleApp/issues/new).
