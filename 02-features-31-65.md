# Feature Review — Part 2: Features 31–65
### Maintenance · Inspections · Audits · Scheduling · Documents · Forms · Inventory · Analytics

> Legend: ✅ Implemented · 🟡 Started · 🟠 Planned · ❌ Not Found | W=Web · M=Mobile · D=Desktop · BE=Backend

---

## 7. Maintenance Management (Features 28–34)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 28 | Time-based maintenance scheduling | ✅ | 🟡 | 🟡 | ❌ | ✅ | P1 | Core | — | `maintenanceRules` table with `type` enum includes `time_based`. Routes: `POST/GET/PATCH/DELETE /maintenance/rules`. Web shows rules tab with mock data. Auto-schedules next task on completion. |
| 29 | Usage-based maintenance triggers (runtime hours) | 🟠 | ❌ | ❌ | ❌ | 🟠 | P2 | Core | L | `usage_based` type in enum + `trigger_value` field. No IoT runtime input. No mechanism to receive/store usage hours. |
| 30 | Counter-based maintenance triggers (N uses) | 🟠 | ❌ | ❌ | ❌ | 🟠 | P2 | Fancy | M | `counter_based` type in schema. No counter increment route or integration. |
| 31 | Maintenance cost tracking (labor + parts) | ✅ | ❌ | ❌ | ❌ | ✅ | P2 | Core | — | `cost_labor`, `cost_parts` fields in `maintenanceTasks`. `PATCH /maintenance/tasks/:id/complete` accepts and stores costs. `GET /analytics/costs` aggregates them. No UI to enter costs. |
| 32 | Maintenance calendar with overdue highlighting | 🟡 | 🟡 | 🟡 | ❌ | ✅ | P2 | Core | M | Task list exists with due dates. **No calendar view** — just a flat list. Mobile maintenance screen shows tasks. Overdue detection possible from `due_date < now()`. |
| 33 | Monthly maintenance summary auto-emailed | ❌ | ❌ | ❌ | ❌ | ❌ | P2 | Fancy | M | Maintenance worker is an **empty TODO**. No scheduled job infrastructure wired up. |
| 34 | Predictive maintenance indicators (rising frequency) | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | XL | No frequency analysis logic. Would require time-series analysis of maintenance events per asset. |

**Section summary:** Time-based scheduling is the most complete piece. Usage/counter triggers are schema-only and meaningless without an IoT data pipeline. The maintenance worker being a stub is the main blocker — nothing triggers automatically.

---

## 8. Inspections & Compliance (Features 35–40)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 35 | Pre-built regulatory inspection templates | 🟡 | ✅ | ❌ | ❌ | 🟡 | P2 | Core | M | Template CRUD routes exist. `inspectionTemplates` table with `items` JSONB. **No pre-built templates** shipped (PAT, LOLER, etc.). Web shows template cards. Custom templates possible. |
| 36 | Custom inspection form builder | 🟡 | 🟡 | ❌ | ❌ | ✅ | P1 | Core | M | Backend fully supports custom templates with field types: pass_fail, text, number, photo, checkbox. **No drag-and-drop builder UI** on web or mobile. |
| 37 | Pass/fail auto-flagging with work order creation | ❌ | ❌ | ❌ | ❌ | 🟠 | P1 | Core | S | `overall_pass` boolean in `inspections` schema. `PATCH /inspections/:id/complete` accepts it. **No auto work order creation** on fail. Logic gap only — easy to add. |
| 38 | Digital signature capture on inspections | 🟠 | ❌ | ❌ | ❌ | 🟠 | P2 | Core | S | `signature_url` field in schema. No signature capture component on web or mobile. Can add `react-native-signature-canvas` + canvas-to-S3. |
| 39 | Inspection compliance dashboard | ✅ | ✅ | ❌ | ❌ | ✅ | P1 | Core | — | Web inspections page has Compliance Overview card: pass rate %, status counts, color-coded bar. Backend routes supply data. |
| 40 | Offline inspection completion with sync | ❌ | ❌ | ❌ | ❌ | ❌ | P1 | Core | XL | No offline sync engine despite SQLite being available on mobile. Critical for field workers in areas with no signal. |

**Section summary:** Inspection infrastructure is more complete than most sections. Pass/fail → work order creation is a 10-line backend gap. Offline is the hard, high-value missing piece.

---

## 9. Remote Audits (Features 41–44)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 41 | Remote audit requests to field workers | ✅ | ✅ | 🟡 | ❌ | ✅ | P2 | Core | — | `auditRequests` + `auditResponses` tables. `POST /audit-requests`, `POST /audit-requests/:id/respond`. Web has new audit modal. Mobile audit screens exist. |
| 42 | Recurring audit scheduling | 🟠 | ❌ | ❌ | ❌ | 🟠 | P3 | Fancy | M | `due_date` field exists. No recurrence rules, cron logic, or repeat schedule. |
| 43 | Auto-triggered audits (inactivity-based) | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | M | No trigger rules or background job to detect inactivity and create audits. |
| 44 | Discrepancy reporting from audit results | ✅ | ✅ | ❌ | ❌ | ✅ | P2 | Core | — | Response status: `confirmed`, `not_in_possession`, `unknown`. Audit detail page shows discrepancies. No export or investigation workflow. |

**Section summary:** Solid foundation. One-off manual audits work end-to-end. Recurring and auto-triggered audits are missing but are not core to the initial product.

---

## 10. Equipment Scheduling & Reservations (Features 45–49)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 45 | Equipment reservation calendar | ✅ | ✅ | ✅ | ❌ | ✅ | P1 | Core | — | `reservations` table. Full CRUD routes. `GET /assets/:assetId/availability`. Web has Gantt-style calendar (month/week/day views). Mobile has reservation list + new form. |
| 46 | Double-booking conflict detection | ✅ | ✅ | ❌ | ❌ | ✅ | P1 | Core | — | `POST /reservations` checks overlapping `start_at`/`end_at` and returns 409 on conflict. Web respects this. |
| 47 | Reservation approval workflow | ✅ | ✅ | ❌ | ❌ | ✅ | P1 | Core | — | Status flow: pending → approved/rejected. Only manager/admin/owner can approve (`requireRole` check). `approved_by` field set on approval. |
| 48 | Day-before return reminder for reservations | ❌ | ❌ | ❌ | ❌ | ❌ | P2 | Core | M | No reminder job. Would require maintenance/notification worker to be functional first. |
| 49 | Project/cost center assignment on reservations | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | S | No `project_id` or `cost_center` field in reservations schema. Easy schema addition when needed. |

**Section summary:** Reservations are the best-implemented section in the codebase. Conflict detection and approval workflow both work. Reminders blocked by the broken notification worker.

---

## 11. Document Management (Features 50–53)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 50 | Per-asset document storage with categories | ✅ | ✅ | ❌ | ❌ | ✅ | P1 | Core | — | `documents` table with `asset_id`, `category` (Manual, Inspection, Photo, Warranty, etc.), S3 storage. Routes: `GET/POST /assets/:assetId/documents`. Web page supports drag-drop upload with file type icons. |
| 51 | Type-level shared documents (manual per model) | 🟡 | 🟡 | ❌ | ❌ | 🟡 | P2 | Core | M | Category field exists. No route or schema to attach a document to an asset *category* rather than individual asset. |
| 52 | Document version control | 🟠 | 🟡 | ❌ | ❌ | 🟠 | P2 | Fancy | M | `version` field (default 1) in schema. Web shows version history UI with version numbers. No API for versioning — uploading a new doc creates a new row, not a new version of existing. |
| 53 | In-browser document preview | 🟠 | 🟠 | ❌ | ❌ | ❌ | P2 | Core | S | Preview modal scaffolding exists in web UI. Not functional. Easy to implement with `<iframe>` for PDFs or `<img>` for images using the presigned S3 URL. |

**Section summary:** Document upload and storage are solid. Preview is a quick win (a few lines of iframe/img). Versioning needs an API redesign but the schema field is already there.

---

## 12. Custom Forms & Checklists (Features 54–57)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 54 | No-code form builder (drag-and-drop) | 🟡 | ❌ | ❌ | ❌ | ✅ | P2 | Core | L | Backend fully supports `formTemplates` with JSONB `fields` (text, number, select, checkbox, date, file). No drag-and-drop builder UI anywhere. |
| 55 | Conditional logic in forms | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | L | No conditional field logic in schema or API. Would need `conditions` array in field schema. |
| 56 | Form responses stored per asset in lifecycle folder | ✅ | ❌ | ❌ | ❌ | ✅ | P2 | Core | — | `formResponses` table with `asset_id`, `template_id`, `data` JSONB. Routes functional. No web or mobile UI to submit responses. |
| 57 | Form response PDF export | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | M | No PDF library. No export route. |

**Section summary:** Forms are a backend-only implementation. No user-facing interface to build or fill forms. The data model is solid but the feature is invisible to users.

---

## 13. Parts & Consumable Inventory (Features 58–62)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 58 | Parts/consumable inventory with stock levels | ✅ | ✅ | ❌ | ❌ | ✅ | P2 | Core | — | `parts` + `partStock` tables. Full CRUD. Web inventory page with search/filter by category. |
| 59 | Low-stock alerts | ✅ | ✅ | ❌ | ❌ | ✅ | P2 | Core | — | `min_quantity` field. Web shows "Low stock" badge and warning banner listing parts below threshold. Alert notification not fired (notification worker is a stub). |
| 60 | Parts consumption linked to work orders | 🟡 | ❌ | ❌ | ❌ | 🟡 | P2 | Core | S | `POST /parts/:id/consume` decrements stock. **No link to a work order or maintenance task** — consumption is anonymous. |
| 61 | Multi-location stock tracking | ✅ | ✅ | ❌ | ❌ | ✅ | P2 | Core | — | `partStock.location_id` FK. Stock can be tracked per location. UI shows it. |
| 62 | Purchase order creation and approval | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | XL | No PO schema or routes. Low-stock alerts display in UI but don't trigger any procurement workflow. |

**Section summary:** Inventory is one of the strongest sections. Low-stock display works. The missing piece is linking consumption to work orders/maintenance tasks for traceability.

---

## 14. Analytics & Reporting (Features 63–65)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 63 | Organization overview dashboard | ✅ | ✅ | 🟡 | ❌ | ✅ | P0 | Core | — | `GET /analytics/overview` returns assets by status, active checkouts, open WOs, overdue maintenance. Web dashboard is server-rendered with real data. Mobile analytics screen basic. |
| 64 | Asset utilization rate reporting | ✅ | ✅ | ❌ | ❌ | ✅ | P1 | Core | — | `GET /analytics/utilization` computes utilization % over configurable period. Shown in web KPI cards. |
| 65 | Total cost of ownership per asset | 🟡 | 🟡 | ❌ | ❌ | 🟡 | P2 | Core | M | `GET /analytics/costs` aggregates maintenance labor + parts. **Purchase price and depreciation not included** — not a true TCO. |

**Section summary:** Core analytics are working and server-rendered (real data). TCO is incomplete without acquisition and depreciation cost components.
