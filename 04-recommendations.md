# Orbit — Recommendations
### External Code Review | Prioritised Actions for Stakeholders

---

## A. Top 10: Do These Now (P0/P1 — Blockers)

These features either break core user flows, create security/legal exposure, or block large sections of downstream features.

| # | What | Why Now | Effort | Unblocks |
|---|------|---------|--------|---------|
| 1 | **Fix QR scanner asset lookup** | The scanner hardcodes `code.startsWith('ASSET-')` — it never calls the API. The primary user interaction (scan → check-out) is non-functional. | S (1–2 days) | Feature 17, entire check-in/out flow |
| 2 | **Implement notification worker** | 3 of 4 background workers are empty `console.warn` stubs. No push notifications, no webhook dispatch, no maintenance alerts ever fire. This blocks ~20 downstream features. | M (1 week) | Features 20, 33, 48, 59, 69, 73, 94 |
| 3 | **Fix web session validation** | `apps/web/middleware.ts` only checks if the session cookie *exists* — it never validates the JWT. Any user with a stale or forged cookie gets full access. | S (1–2 days) | Security baseline |
| 4 | **Implement token refresh on mobile** | `AuthProvider.tsx` stores tokens but never calls the refresh-token grant. When the 15-minute access token expires, the user is silently broken with no recovery. | S (2–3 days) | All authenticated mobile flows |
| 5 | **Wire web frontend to real API** | Most web pages render hardcoded mock data arrays. The backend is built — they just need to be connected. Assets, work orders, inspections, maintenance all affected. | M (1–2 weeks) | All web features appearing "implemented" |
| 6 | **Build the public QR issue-reporting form** | Any person can scan a QR code on an asset and should get a public form to file an issue — no account required. Currently all routes require JWT. This is a core product differentiator. | M (3–5 days) | Features 21, 77 |
| 7 | **Wire GPS capture to scan/checkout** | `expo-location` is available, schema has `gps_lat`/`gps_lng` on `assetEvents`. Capturing GPS at scan is 10 lines of code — just missing the call. Critical for "last known location" accuracy. | S (1 day) | Feature 85, location tracking |
| 8 | **Add GDPR data export + deletion routes** | No `/users/:id/export` or `/users/:id/delete` endpoints exist. GDPR Articles 17 and 20 are **legally required** for EU deployment. Without this, Orbit cannot legally operate in the EU. | M (3–5 days) | Feature 107, legal compliance |
| 9 | **Add OpenAPI/Swagger documentation** | Hono has first-class OpenAPI support (`@hono/zod-openapi`). The REST API exists but has zero documentation. Needed for third-party integrations, enterprise sales, and public API offering. | M (3–5 days) | Feature 93, enterprise sales |
| 10 | **Add the PWA manifest and service worker** | `next-pwa` is in the stack but not configured. Without it, Orbit has no web-app install experience and no offline caching on web. Blocks all users who won't install the native app. | S (1–2 days) | Feature 83, web reach |

---

## B. Top 10: Started but Easy to Finish

These features have partial implementation in place and can be completed quickly with focused work.

| # | What | Current State | What's Missing | Effort |
|---|------|--------------|----------------|--------|
| 1 | **In-browser document preview** (Feature 53) | Preview modal scaffolding exists in web UI | Add `<iframe src={presignedUrl}>` for PDFs, `<img>` for images. The presigned URL is already returned by the backend. | XS (hours) |
| 2 | **Pass/fail → auto-create work order** (Feature 37) | `overall_pass` boolean stored on inspection completion | Add 5 lines to `PATCH /inspections/:id/complete`: if `overall_pass === false`, call `createWorkOrder()`. Schema is ready. | XS (1 day) |
| 3 | **Warranty expiration alerts** (Feature 6) | `warranty_expiry` date field in assets schema | Add a BullMQ delayed job at asset creation: enqueue a notification for 30 days before expiry. Email worker already functional. | S (1–2 days) |
| 4 | **CSV bulk import** (Feature 9) | JSON import route exists (`POST /assets/import`), accepts up to 500 assets | Add `multer`/`busboy` CSV parser, column-mapping step, and a simple web upload form. | S (2–3 days) |
| 5 | **Duplicate detection on import** (Feature 11) | `serial_number` field indexed in schema | Before inserting, query `WHERE serial_number IN (imported serials)` and return a warning array. | XS (hours) |
| 6 | **Signature capture on inspections** (Feature 38) | `signature_url` field in inspections schema | Add `react-native-signature-canvas` to mobile. On completion, upload to S3 and send URL. | S (1–2 days) |
| 7 | **Maintenance calendar view** (Feature 32) | Task list with `due_date` exists in backend and web | Swap the flat list for a calendar component (e.g., `react-big-calendar` on web). Data is already there. | S (2–3 days) |
| 8 | **CSV export for analytics/inventory** (Feature 68) | "Export CSV" button visible in web inventory UI | Add `fast-csv` or `papaparse` to API, add `GET /inventory/export?format=csv`. | S (1–2 days) |
| 9 | **Parts consumption linked to work orders** (Feature 60) | `POST /parts/:id/consume` decrements stock | Add `work_order_id` and `maintenance_task_id` optional fields to the consume endpoint and log the association. | XS (hours) |
| 10 | **Loss/shrinkage report** (Feature 66) | `asset_status` enum includes `lost`, `retired` | Add `GET /analytics/shrinkage` that queries assets by those statuses with cost totals. Add a card on the analytics dashboard. | S (1 day) |

---

## C. Push These to Later (with Reason)

These features are real, but their cost/benefit ratio is unfavorable at this stage.

| # | Feature | Why Defer | When to Revisit |
|---|---------|----------|----------------|
| 1 | **AI camera for unscanned removal detection** (Feature 90) | R&D-level effort requiring ML training data, edge hardware, and model deployment infrastructure. Zero ROI until the core product is stable and there are high-value installations to instrument. | Phase 4 or later; when a major customer specifically requests it |
| 2 | **OEM telematics integration (AEMP 2.0)** (Feature 91) | Requires bilateral API agreements with Caterpillar, Komatsu, Volvo, etc. Legal and partnership work, not just engineering. | Only when a specific OEM customer is signed |
| 3 | **Dedicated GPS / BLE / RFID hardware support** (Features 86–88) | Hardware-dependent features require vendor relationships, certified readers, and field testing. The platform's app-first approach (QR + phone GPS) covers 90% of use cases at zero hardware cost. | Phase 3, when Tier 1 customers require it |
| 4 | **Parent-child org hierarchy** (Feature 99) | Franchise/multi-branch model requires a full re-architecture of RBAC, reporting, and billing. Complex and currently no stated customer need. | Phase 4 (Enterprise tier) |
| 5 | **White-label / reseller model** (Feature 100) | Reseller channel requires separate onboarding, support, and pricing structures. Premature before the core product has proven product-market fit. | Phase 5 after stable v1.0 |
| 6 | **RTL layout support** (Feature 105) | Right-to-left language support (Arabic, Hebrew) requires systematic CSS and layout refactoring. No stated market need currently. | Only when entering MENA/Israeli markets |

---

## D. Features Never Mentioned — But Mandatory

These do not appear in `all_the_functions.md` but are essential for any production SaaS platform. They should be added to the spec.

| # | Feature | Why It's Mandatory | Effort |
|---|---------|-------------------|--------|
| 1 | **JWT token refresh flow** | Access tokens expire in 15 minutes. Without a refresh grant, every mobile user is broken after 15 minutes. Not mentioned anywhere in the spec, but foundational to auth. | S |
| 2 | **User invitation flow** | `invited_by` field exists in schema but there is no invite email, invite link, or invite acceptance screen. You cannot add users to an org without it. | S |
| 3 | **Onboarding wizard (guided setup)** | The onboarding page exists (`/onboarding`) but has no guided steps for connecting first assets, creating locations, or inviting team members. New orgs will get lost. | M |
| 4 | **Error monitoring / crash reporting** | `monitoring.md` specifies Highlight.io + SigNoz. **Zero integration exists in the actual code.** No error capturing on frontend or backend. A production system with no observability is blind when things go wrong. | S |
| 5 | **Full-text search across assets and documents** | Only basic `ILIKE` name matching exists. For an org with 10,000 assets, search by serial number, manufacturer, category, or document content is essential. PostgreSQL's `tsvector` or Meilisearch would work. | M |
| 6 | **QR label designer / print layout config** | QR generation works but there is no way to configure label size, layout, or include company logo before batch printing. Users need to print labels that fit their physical labels. | S |
| 7 | **Bulk status change / bulk operations** | No way to select 50 assets and mark them all as `in_maintenance` or `retired`. Required for realistic onboarding and lifecycle events (e.g., a site closes). | S |
| 8 | **API key management for third-party access** | `apiKeys` table and web UI exist at `/settings/api-keys`. **No route to create/revoke API keys in the backend.** The schema is there but the endpoints are missing. | S |
| 9 | **Mobile deep linking (QR → app or PWA)** | QR codes currently encode `orbit:asset:{id}` URLs. Scanning with the system camera should open the Orbit app if installed, or the PWA if not. Requires Universal Links (iOS) + App Links (Android) configuration. | M |
| 10 | **Password reset flow** | `forgot-password` and `reset-password` pages exist on web. Backend has `sendPasswordResetEmail()`. But the actual reset token route (`POST /auth/reset-password`) was not found in `routes/auth.ts`. | S |
| 11 | **Terms of Service & Privacy Policy pages** | Required for any SaaS product before launch. Cannot legally onboard users without these. | XS |
| 12 | **Pagination on all list endpoints** | Some routes accept `limit` params but no cursor or page-based pagination. With 10,000 assets, fetching `limit=100` is not enough and offset-based pagination degrades at scale. | M |
| 13 | **Admin panel for self-hosted deployments** | The spec mentions a self-hosted admin panel for backup/restore/config management. No such panel exists. Operators of self-hosted instances have no management UI. | L |

---

## Summary Scorecard

| Category | Count |
|---------|-------|
| Fix immediately (critical blockers) | 10 |
| Easy wins to finish | 10 |
| Defer to later | 6 |
| Missing from spec but mandatory | 13 |

**Overall verdict:** The architectural foundations are well-designed — schema, RBAC, multi-tenancy, and the API structure are solid. The gap is in execution depth: most features exist at the schema or route level but are not wired to real UIs, and multiple critical background systems are placeholder stubs. With focused engineering on the "Fix immediately" list, the core product loop (scan → check-out → return → work order → maintenance) can be fully functional within 4–6 weeks.
