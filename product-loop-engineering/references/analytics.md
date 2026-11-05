# Analytics: instrumented by default

Every journey unit ships the analytics events for what it builds. The milestone's last unit turns those events into a dashboard, reports, or saved queries. Dev and prod send to separate analytics projects with separate keys, so test traffic never pollutes real metrics.

`CONFIG.md` keys: `ANALYTICS_PLATFORM` (where events go), `ANALYTICS_ACCESS` (the MCP or API used to query it), `ACQUISITION_ANALYTICS` (prod acquisition property), `ANALYTICS_CATALOGUE` (path of the event catalogue).

| Phase | What happens |
| :--- | :--- |
| 0 Setup | A human creates the accounts and keys |
| 1 Plan, skeleton unit | Analytics, session replay and the test kit go in the skeleton |
| 1 Plan, every journey unit | Contract section C lists events; an `[Instrumentation]` T scenario asserts them |
| 3 Tests first | The `[Instrumentation]` test is written and fails |
| 4 Build | Events go through one `track()` seam; new events join the catalogue |
| 5 Verify | Offline test passes; live arrival confirmed in the dev project |
| P0 checkpoint | Hypothesis-metric events confirmed arriving |
| Last unit (reporting) | Dashboards, reports, saved queries |

## Phase 0: accounts and keys (human only)

Separate **dev** and **prod** projects in `ANALYTICS_PLATFORM`, plus a prod `ACQUISITION_ANALYTICS` property, each with its own key. The dev key goes in the local `.env`, the prod key in the host's secret settings. The agent never reads either; code picks the key by environment. Stop and ask for these; never work around a missing one.

## Skeleton unit

- Analytics and session replay initialized with the Phase 0 keys (dev key locally, prod key only in production).
- **Analytics test kit**:
  - an event catalogue at `ANALYTICS_CATALOGUE`: every event name with its required properties and types. `track()` raises on unknown events or properties in dev/test and drops them in prod;
  - a fake sink with an `assert_tracked(event, **props)` helper;
  - a browser fixture that intercepts the analytics platform's endpoints and decodes what the page sends;
  - a test that every contract's Instrumentation events match the catalogue both ways;
  - a test that every catalogue event is asserted by at least one test.
- Third-party browser libraries are vendored (a pinned copy served by the app) so browser tests run them with endpoints intercepted. Blocking all network hides "library never initialised" bugs.

## Unit contracts (Phase 1, Part C)

- Section C lists the events the unit emits: name, trigger, properties.
- Journey units: one view event and one primary-action event per capability. P0 journeys also emit the events behind the spec's hypothesis metric.
- Every journey unit has an `[Instrumentation]` T scenario: drive the unit's flows and assert each listed event and its properties through the fake sink (server) and the intercepted analytics requests (browser). New events go into the catalogue in the same unit.
- The reporting unit lists the dashboards and queries it builds instead of events.
- `check_loop.py plan` fails a journey unit with no events or no `[Instrumentation]` T scenario, and a plan whose last unit isn't reporting.

## Build (Phase 4)

Emit every event through one analytics seam, a single `track()` wrapper, so tests can assert events with a fake sink and no vendor SDK call is scattered through UI code. Add each new event to the catalogue with its properties.

## Verify (Phase 5)

- **Offline**: the `[Instrumentation]` T scenario passes and the catalogue is in sync.
- **Live arrival** is also required when `ANALYTICS_ACCESS` names an MCP or API and a dev key is set. The orchestrator triggers the unit's events against the **dev** project, tagged with a run id, then queries the platform through `ANALYTICS_ACCESS` and confirms each arrived with its listed properties. Record the result in the verdict. It is never part of the offline test command.

## P0 checkpoint and reporting

- After the last P0 unit, confirm the hypothesis-metric events are arriving.
- The last unit builds the dashboard, reports, or saved queries over the events from earlier units, through the analytics platform's API or MCP.
