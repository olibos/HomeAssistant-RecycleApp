# API Fair Use Policy & Information for FostPlus / RecycleApp

This document outlines how the **Home Assistant RecycleApp Integration** interacts with the RecycleApp.be API, the technical measures implemented to ensure respectful, minimal resource usage, and contact information for upstream administrators.

---

## About This Integration

The [Home Assistant RecycleApp Integration](https://github.com/olibos/HomeAssistant-RecycleApp) is an open-source, non-commercial community project. It enables residents in Belgium to view their local waste collection schedules (PMC/PMD, paper/cardboard, residual waste, etc.) and recycling park opening hours within their personal [Home Assistant](https://www.home-assistant.io/) home automation setups.

---

## Background & Incident Context (Issue #132)

In March 2026, the integration experienced upstream blocking by FostPlus (tracked in [Issue #132](https://github.com/olibos/HomeAssistant-RecycleApp/issues/132)) due to an elevated request volume. 

An investigation identified two primary causes:
1. **Redundant API client instances**: Separate integration components and setup steps instantiated multiple API client instances, resulting in repeated configuration discovery requests (`/config/app.settings.json`) and session re-creation.
2. **Calendar event polling**: When calendar entities were used with Home Assistant automations or calendar dashboard views, Home Assistant's default calendar polling invoked `async_get_events` approximately every 15 minutes, repeatedly querying the upstream API for event data.

---

## Technical Mitigations & Fair-Use Architecture

To resolve these issues and ensure minimal footprint on FostPlus infrastructure, the following architectural controls are in place:

### 1. Shared Singleton Client & Session Reuse
The API client (`FostPlusApi`) is implemented as a shared singleton across the entire integration.
- Connection discovery (`app.settings.json`) is performed once per runtime lifecycle rather than on every entity action.
- An underlying HTTP session is reused with keep-alive connections, gzip compression, and thread-safe initialization.

### 2. Coordinator-Cached Calendar Events
Calendar events for the standard 8-week collection horizon are served directly from the integration's in-memory `DataUpdateCoordinator` cache.
- The ~15-minute polling loop from Home Assistant automation triggers no longer hits the upstream API.
- Remote API calls are only made when queries fall outside the cached 8-week window.

### 3. Daily Midnight Refresh Cadence
Data is scheduled to update once per day (at midnight) via Home Assistant's `DataUpdateCoordinator`.
- Collection schedules rarely change day-to-day, making a 24-hour polling interval sufficient for accurate notifications.

### 4. Exponential Backoff on Failure
If an upstream request encounters network issues or errors:
- The integration applies exponential backoff starting at 5 minutes and doubling up to a cap of 1 hour (`_get_next_retry`).
- This prevents hammering upstream servers during temporary outages or maintenance windows.

### 5. Transparent User-Agent Identification
All HTTP requests sent by this integration include an explicit, identifiable `User-Agent` header:
```text
RecycleApp-HomeAssistant/<version> (+https://github.com/olibos/HomeAssistant-RecycleApp/blob/main/docs/api-fair-use.md)
```
This allows upstream infrastructure teams to clearly identify traffic originating from this integration and reference this fair-use statement.

---

## Contact & Collaboration for Upstream Maintainers

I deeply appreciate FostPlus providing the RecycleApp service, which helps Belgian citizens sort and recycle their waste responsibly.

If you are an administrator, developer, or infrastructure engineer at FostPlus / RecycleApp and notice any behavior, traffic volume, or header patterns that cause operational concerns:

- **GitHub Issues**: Please open an issue at [https://github.com/olibos/HomeAssistant-RecycleApp/issues](https://github.com/olibos/HomeAssistant-RecycleApp/issues). Issues are monitored actively and upstream concerns are treated as top priority.
- **Maintainer**: [@olibos](https://github.com/olibos)

I am fully committed to cooperating with upstream maintainers, adhering to recommended rate limits, and implementing any architectural adjustments needed to maintain respectful API usage.
