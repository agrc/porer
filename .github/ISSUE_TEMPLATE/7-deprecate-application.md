---
name: (🔐 UGRC internal use) Application deprecation
about: An application is no longer maintained, useful, or is being replaced
title: Deprecate <application>
labels: "deprecation, porter"
assignees: "@steveoh, @eneemann, @rkelson"
---

## Summary

- **Application Name**:
- **Application Urls**
  - Staging:
  - Production:

_A short summary of the situation._

### Action items

1. _Assign a person who should complete the task by replacing `name` with their github `@name`._
1. _Check [x] the box when the task is completed and add the date of completion._
1. _~Strike~ out all items that do not apply._

- [ ] Target delete date (name, set: `2025/00/00`)
- [ ] Update relevant [gis.utah.gov](https://gis.utah.gov/developer/application) application pages (name, completed: `2025/00/00`)
- [ ] Remove application-specific Databases (name, completed: `2025/00/00`)
- [ ] AGRC Projects team drive [folder](https://drive.google.com/drive/folders/0AIVByxAYHd4oUk9PVA) (name, completed: `2025/00/00`)
- [ ] Remove from Application Portfolio Management ([Business Applications](https://workspaces.dts.utah.gov/now/nav/ui/classic/params/target/cmdb_ci_business_app_list.do%3Fsysparm_userpref_module%3D11133b75870003005f9f578c87cb0bfe%26sysparm_view%3Dbusiness_application_readonly) in ServiceNow) (name, completed: `2025/00/00`)
- [ ] Remove Google Analytics property (name, completed: `2025/00/00`)

#### Is there a website?

- [ ] Remove DNS entry (name, completed: `2025/00/00`)
- [ ] Archive source code repository (name, completed: `2025/00/00`)
- [ ] Remove app-specific quad word from Discover system (name, completed: `2025/00/00`)
- [ ] Remove app-specific api key from UGRC API (name, completed: `2025/00/00`)
- [ ] Remove cloud project (name, completed: `2025/00/00`)
- [ ] Remove terraform infrastructure (name, completed: `2025/00/00`)

_Choose one._

- [ ] Remove from the web server (name, completed: `2025/00/00`)
- [ ] Replace app with a static page with information (name, completed: `2025/00/00`)
- [ ] Redirect somewhere else (name, completed: `2025/00/00`)

#### Is there a map service or AGOL item?

- [ ] Stop (name, completed: `2025/00/00`)
- [ ] Delete (name, completed: `2025/00/00`)
- [ ] Unregister Data Store in ArcGIS Server (name, completed: `2025/00/00`)

#### Is there a forklift pallet?

- [ ] Remove repo (name, completed: `2025/00/00`)
  - don't forget to remove the pallet from the current packing slip in receiving!
- [ ] Remove stale data from forklift hashing and receiving (name, completed: `2025/00/00`)
- [ ] Remove row from `data/hashed/changedetection.gdb/TableHashes` (name, completed: `2025/00/00`)

#### Are there service dependencies?

- [ ] Validate that the UGRC API does not query it (name, completed: `2025/00/00`)
- [ ] Validate that UGRC or applications do not reference it (name, completed: `2025/00/00`)

### Notification

- [ ] X (@steveoh)

### Group Task Assignments

1. _Check [x] the box when you have assigned all the tasks relevant to your group._

- [ ] Data Team (@eneemann)
- [ ] Dev Team (@steveoh)
- [ ] Cadastre Team (@rkelson)
