# Feature Review — Part 1: Features 1–30
### Asset Registry · Locations · Check-in/out · Work Orders

> Legend: ✅ Implemented · 🟡 Started · 🟠 Planned · ❌ Not Found | W=Web · M=Mobile · D=Desktop · BE=Backend

---

## 1. Asset Registry (Features 1–8)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 1 | Asset CRUD with photos & custom fields | 🟡 | 🟡 | 🟡 | ❌ | ✅ | P0 | Core | — | Routes complete. Web/mobile pages exist but render **mock data**, not wired to real API. Custom field editing missing from create/edit forms. |
| 2 | Auto-generated QR codes with batch printing | 🟡 | ❌ | ❌ | ❌ | ✅ | P0 | Core | S | QR generation route complete (`GET /assets/:id/qr`). Batch PDF printing not implemented. No display UI. |
| 3 | NFC tag and barcode association | 🟠 | ❌ | ❌ | ❌ | 🟠 | P2 | Core | M | Schema has `nfc_tag_id` field. No barcode field. No scan-to-link logic. NFC reading not wired to adapters. |
| 4 | Kit/bundle management | ❌ | ❌ | ❌ | ❌ | ❌ | P2 | Core | L | No parent-child asset relationship in schema. No bundle CRUD. |
| 5 | Asset templates for quick creation | ❌ | ❌ | ❌ | ❌ | ❌ | P2 | Fancy | M | Nothing in schema or routes. Would need a `assetTemplates` table + prefill logic. |
| 6 | Warranty tracking with expiration alerts | 🟠 | 🟡 | ❌ | ❌ | 🟠 | P1 | Core | S | `warranty_expiry` field in schema. Detail page shows it. **No alert/notification** when expiry approaches. |
| 7 | Depreciation calculation | ❌ | ❌ | ❌ | ❌ | ❌ | P2 | Fancy | M | `cost_basis` field exists but no amortization logic. No depreciation schedule or book-value calculation. |
| 8 | Insurance data tracking | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | S | Currently handled via custom fields (mock data shows "Insurance Policy"). No dedicated schema fields. |

**Section summary:** Core asset data model is solid. QR generation works. UI not connected to real data. Kit/bundle and templates completely absent.

---

## 2. Asset Onboarding (Features 9–11)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 9 | Excel/CSV bulk import with column mapping | 🟡 | ❌ | ❌ | ❌ | 🟡 | P1 | Core | M | Backend has `POST /assets/import` accepting JSON array (max 500). No CSV parser. No column-mapping UI. |
| 10 | ERP sync import | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | XL | No integration routes or schema. Requires third-party connectors. |
| 11 | Duplicate detection on import | ❌ | ❌ | ❌ | ❌ | ❌ | P1 | Core | S | No serial-number/name deduplication logic in import route. Easy to add as a DB query before insert. |

**Section summary:** Import infrastructure started server-side. CSV parsing and the web UI for mapping columns are the missing pieces. Duplicate detection is a quick win.

---

## 3. Asset Lifecycle (Features 12–13)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 12 | Asset lifecycle event log (immutable, append-only) | ✅ | 🟡 | ❌ | ❌ | ✅ | P0 | Core | — | `assetEvents` table with 11 event types. `GET /assets/:id/events` route. `logAssetEvent()` helper called on all mutations. Web detail page renders mock timeline — not wired to real endpoint. |
| 13 | Full asset dossier PDF export | ❌ | ❌ | ❌ | ❌ | ❌ | P1 | Core | M | No PDF library configured. No export route. Export button placeholder visible in web UI. |

**Section summary:** The event log is one of the strongest pieces of the backend. PDF export is completely missing — needed for compliance use cases.

---

## 4. Locations (Features 14–16)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 14 | Location hierarchy (warehouse → shelf → compartment) | ✅ | ✅ | ❌ | ❌ | ✅ | P0 | Core | — | `locations.parent_id` self-referential FK. GET supports `parentId` filter. Web shows full hierarchical tree. Mobile has no location browser. |
| 15 | Virtual locations (vehicles, containers) | ✅ | ✅ | ❌ | ❌ | ✅ | P1 | Core | — | `location_type` enum includes `vehicle`, `zone`. CRUD complete. |
| 16 | GPS coordinates per location | 🟠 | ❌ | ❌ | ❌ | 🟠 | P2 | Core | M | `gps_lat`, `gps_lng` double precision fields in schema. Accepted in create/update routes. No map UI, no geolocation capture. |

**Section summary:** Location management is one of the more complete areas. GPS is schema-ready but needs a map view to be useful.

---

## 5. Check-in / Check-out (Features 17–20)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 17 | QR scan check-in / check-out (< 5 seconds) | 🟡 | ❌ | 🟡 | ❌ | ✅ | P0 | Core | S | Camera adapter functional. **Critical stub:** lookup uses `code.startsWith('ASSET-')` hardcoded prefix — no actual API call to validate asset. Navigation can 404. |
| 18 | Person-to-person transfer without warehouse return | ✅ | ❌ | 🟡 | ❌ | ✅ | P1 | Core | — | `POST /checkouts` and `POST /checkouts/:id/return` implemented. Mobile check-in modal exists. No explicit transfer-to-person UI. |
| 19 | Full custody chain audit trail | ✅ | 🟡 | ❌ | ❌ | ✅ | P0 | Core | — | `GET /checkouts/assets/:assetId/history` returns full chain. Web renders mock history. Mobile has no history view. |
| 20 | Overdue return tracking with escalation | 🟡 | ❌ | ❌ | ❌ | 🟡 | P1 | Core | S | `GET /checkouts/overdue` works. Analytics counts active checkouts. **No notifications/escalation fired** — maintenance worker is an empty TODO. |

**Section summary:** The check-in/out *backend* is functional. The mobile scanner — the primary entry point for this flow — has a critical stub that prevents it from working. This is the single highest-priority fix.

---

## 6. Work Orders (Features 21–27)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 21 | No-auth issue reporting via QR code (public form) | ❌ | ❌ | ❌ | ❌ | ❌ | P0 | Core | M | All routes require JWT. No public endpoint. No unauthenticated form page. A key differentiator — anyone with a QR label can report issues. |
| 22 | Work order lifecycle management | ✅ | ✅ | ✅ | ❌ | ✅ | P0 | Core | — | Full CRUD + status flow (open → assigned → in_progress → on_hold → resolved → closed). Web and mobile list + detail views exist. Web likely on mock data. |
| 23 | Threaded conversations within work orders | ✅ | 🟡 | ✅ | ❌ | ✅ | P1 | Core | — | `workOrderComments` table. `POST /work-orders/:id/comments`. Web renders mock comments. Mobile renders real comments with author/timestamp. |
| 24 | Photo/video/voice attachment on work orders | ❌ | ❌ | ❌ | ❌ | ❌ | P1 | Core | M | No attachment table or route linked to work orders. `documents` table exists but not linked to WOs. |
| 25 | Supplier integration for external repair routing | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | XL | No supplier table, no external portal, no supplier-facing routes. |
| 26 | Recurring work order automation | ❌ | ❌ | ❌ | ❌ | ❌ | P2 | Fancy | L | No recurrence rules for work orders. Maintenance rules handle recurrence but are a separate entity. |
| 27 | Work order analytics (resolution time, cost, frequency) | 🟡 | 🟡 | ❌ | ❌ | 🟡 | P2 | Core | M | `GET /analytics/overview` returns open WO count. No resolution time, cost per WO, or recurring issue detection. Web analytics page uses mock data. |

**Section summary:** Work order CRUD is solid. The no-auth public form is completely missing — it's a core differentiator that enables external reporters to file issues without an account. Attachments on WOs are also absent.
