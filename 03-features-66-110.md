# Feature Review — Part 3: Features 66–110
### Analytics · Notifications · Users & Auth · Mobile · IoT · Integrations · Platform · Localization · Security

> Legend: ✅ Implemented · 🟡 Started · 🟠 Planned · ❌ Not Found | W=Web · M=Mobile · D=Desktop · BE=Backend

---

## 14 cont. Analytics & Reporting (Features 66–68)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 66 | Loss/shrinkage reporting | ❌ | ❌ | ❌ | ❌ | 🟠 | P2 | Core | S | `asset_status` enum includes `lost`. No dedicated report, dashboard, or cost-of-loss calculation. Easy to add as a filtered analytics query. |
| 67 | Scheduled report auto-delivery via email | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | L | No scheduled job infrastructure. Would need maintenance worker + cron + email template. |
| 68 | CSV/Excel/PDF report export | ❌ | 🟠 | ❌ | ❌ | ❌ | P2 | Core | M | "Export CSV" button visible in web inventory UI. Backend analytics routes return JSON only. No export generation library. |

---

## 15. Notifications (Features 69–73)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 69 | Multi-channel notifications (email, push, WhatsApp, SMS) | 🟡 | 🟡 | 🟡 | ❌ | 🟡 | P1 | Core | L | Email: functional (`lib/email.ts`). Push: mobile adapter exists, not wired to events. SMS/WhatsApp: schema columns exist, **no sending logic**. Notification worker is `console.warn` only. |
| 70 | Per-user notification preferences | ✅ | 🟡 | 🟡 | ❌ | ✅ | P2 | Core | — | `notificationPreferences` table with channel toggles per event type. `GET/PATCH /notifications/preferences`. Web settings UI exists. Mobile profile has toggles. |
| 71 | Manager escalation rules | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | L | No escalation schema or logic. Would require a rules engine + BullMQ delayed jobs. |
| 72 | Digest/summary notification mode | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | M | No digest batching or summary generation. |
| 73 | Webhook notifications for external systems | 🟡 | 🟡 | ❌ | ❌ | 🟡 | P2 | Core | M | `webhooks` table with `url`, `events` JSONB, `secret_hash`. Create/delete routes in `organizations.ts`. **Webhook dispatch worker is an empty TODO** — events are never actually sent. |

**Section summary:** The notification infrastructure (schema, preferences, email plumbing) is well-designed. The critical gap is that the notification worker never runs — no push notifications, no webhook delivery, no in-app delivery reach users.

---

## 16. Users & Role Management (Features 74–79)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 74 | Role-based access control with custom roles | 🟡 | 🟡 | 🟡 | ❌ | ✅ | P0 | Core | — | 6 predefined roles (owner, admin, manager, worker, readonly, external). `requireRole()` middleware works. **No custom role builder** — only predefined roles. |
| 75 | Location-scoped permissions | ❌ | ❌ | ❌ | ❌ | ❌ | P2 | Core | L | All RBAC is org-level only. No location-based access scoping in schema or middleware. |
| 76 | Virtual users (trucks, subcontractors — no login) | ❌ | ❌ | ❌ | ❌ | ❌ | P2 | Core | M | No virtual/synthetic user flag in schema. `invited_by` field exists but no non-login account type. |
| 77 | Anonymous reporters (no account, QR-only) | ❌ | ❌ | ❌ | ❌ | ❌ | P1 | Core | M | Directly tied to Feature 21 (public form). No anonymous submission pathway. |
| 78 | SSO (SAML, OIDC) | 🟡 | 🟡 | ❌ | ❌ | ❌ | P2 | Core | L | Web settings page (`/settings/sso`) has full UI for SAML/OIDC/Google/Microsoft. **Zero backend implementation.** `lib/auth.ts` only handles JWT + password + TOTP. |
| 79 | Two-factor authentication (TOTP) | ✅ | 🟡 | ❌ | ❌ | ✅ | P1 | Core | — | Full TOTP implementation: `lib/totp.ts` with generate/verify/QR code. Routes: `/auth/2fa/enable`, `/auth/2fa/verify`, `/auth/2fa/disable`. Schema: `totp_secret`, `totp_enabled`. Web security settings page shows 2FA option (UI only). Mobile has no 2FA screen. |

**Section summary:** Auth is the best-implemented section. RBAC works well. SSO is UI-only with no backend. Virtual users and anonymous reporters are absent — both tied to the missing public form feature.

---

## 17. Mobile Application (Features 80–83)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 80 | Native iOS + Android app | 🟡 | ❌ | 🟡 | ❌ | — | P0 | Core | M | Expo managed app with EAS Build config. App compiles. Home screen fetches real assets. Scanner, auth flow, work orders, inspections, maintenance screens all exist. Not fully wired. |
| 81 | Offline mode with sync-on-reconnect | ❌ | ❌ | ❌ | ❌ | ❌ | P0 | Core | XL | `expo-sqlite` available. Platform matrix declares `sqliteLocal: true`. **No sync engine implemented** despite being declared in `packages/core/src/sync/`. This is a major gap for field workers. |
| 82 | Tablet-optimized layout for kiosk use | ❌ | ❌ | ❌ | ❌ | — | P3 | Fancy | M | Platform matrix notes `multiWindow: partial` (iPad). No tablet-specific layout, no kiosk mode. |
| 83 | PWA fallback for web-only access | ❌ | ❌ | — | ❌ | — | P1 | Core | M | No `manifest.json`, no service worker, no `next-pwa` configuration found in actual code. Platform matrix says `installable: conditional` but nothing is wired. |

**Section summary:** The mobile app is a functional scaffold. Offline mode is the biggest miss — it's the primary selling point for field workers and completely absent. PWA is also missing, blocking users who won't install a native app.

---

## 18. IoT & Hardware (Features 84–92)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 84 | QR code auto-generation and batch printing | 🟡 | ❌ | ❌ | ❌ | 🟡 | P0 | Core | S | `qr_code` field in assets schema. QR library imported. **No dedicated generate/download route found.** Batch PDF printing absent. |
| 85 | Phone GPS capture on scan | 🟠 | ❌ | 🟠 | ❌ | 🟠 | P1 | Core | S | `gps_lat`/`gps_lng` fields on `assetEvents`. Platform matrix: `location.gps: conditional`. No GPS capture call in mobile scanner or check-in flow. Easy to wire: `expo-location` → send coords with checkout API call. |
| 86 | Dedicated GPS hardware tracker support | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | XL | No hardware integration routes, no telemetry ingestion API. Requires hardware partnerships. |
| 87 | BLE beacon support | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | XL | Platform matrix declares BLE capability. No application code. Requires hardware setup. |
| 88 | RFID gate support | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | XL | `nfc_tag_id` field covers NFC. RFID readers require separate hardware driver and integration API. |
| 89 | Runtime/battery/sensor IoT data ingestion | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | XL | No sensor telemetry schema or ingestion API. Required for usage-based maintenance (Feature 29). |
| 90 | AI camera for unscanned removal detection | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | XL | Platform matrix notes `camera.ocr: partial`. No ML model, no edge inference, no backend event handler. R&D project. |
| 91 | OEM telematics integration (AEMP 2.0) | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | XL | Nothing exists. Requires AEMP 2.0 standards compliance and manufacturer API agreements. |
| 92 | Geofencing with entry/exit alerts | ❌ | ❌ | ❌ | ❌ | ❌ | P2 | Fancy | L | Platform matrix: `location.geofencing: conditional`. No geofence boundary schema, no alert rules, no backend. |

**Section summary:** IoT is almost entirely absent. Only QR (partial) and GPS schema fields exist. Everything else is Tier 3 hardware requiring external vendors. These should remain on a long-term roadmap.

---

## 19. Integrations & API (Features 93–97)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 93 | REST API with OpenAPI documentation | 🟡 | — | — | — | 🟡 | P1 | Core | M | REST routes complete and clean. **No OpenAPI/Swagger spec.** No auto-generated docs. No API explorer. |
| 94 | Webhook subscriptions | 🟡 | 🟡 | ❌ | ❌ | 🟡 | P2 | Core | M | Schema + create/delete routes exist. Web API settings page shows webhooks UI. **Dispatch worker is an empty TODO** — no HTTP POST ever sent to webhook URLs. |
| 95 | Accounting export (DATEV, lexoffice, QuickBooks, Xero) | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | XL | Cost data exists in schema. No export format generation for any accounting system. |
| 96 | ERP connectors (SAP, Dynamics, Oracle) | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | XL | Nothing exists. Long-term enterprise feature. |
| 97 | Slack / Teams notification integration | ❌ | ❌ | ❌ | ❌ | ❌ | P2 | Fancy | M | No webhook-based channel integration. Would extend notification channels via BullMQ job. |

**Section summary:** The REST API is a solid foundation. OpenAPI docs are a quick win with Hono's built-in support. Webhook dispatch is the key missing piece — the infrastructure is built but never fires.

---

## 20. Multi-Tenancy & Organization Management (Features 98–103)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 98 | Multi-tenant organization management | ✅ | ✅ | ✅ | ❌ | ✅ | P0 | Core | — | All tables have `org_id` FK. `tenant.ts` middleware validates org scope on every request. JWT includes `orgId`. Properly isolated. |
| 99 | Parent-child org hierarchy (franchise model) | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | L | `locations.parent_id` exists but `organizations` has no parent reference. No cross-org reporting. |
| 100 | White-label / custom branding | ❌ | ❌ | ❌ | ❌ | 🟠 | P3 | Fancy | M | `organizations.logo_url` in schema. No theme/color customization. Brand hardcoded. |
| 101 | Cloud-hosted SaaS deployment | 🟡 | 🟡 | — | — | 🟡 | P1 | Core | M | `org_plan` enum (free, starter, pro, enterprise) in schema. **No plan enforcement, no feature gating, no billing integration.** Onboarding wizard page exists. |
| 102 | Self-hosted Docker deployment | 🟡 | — | — | — | — | P1 | Core | M | Docker Compose files exist (per docs). Architecture is containerizable. **No Dockerfile found in orbit/ subfolder.** Deployment docs exist but ops config incomplete. |
| 103 | Air-gapped / offline server deployment | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | XL | Requires full offline server stack. No relevant configuration. |

**Section summary:** Multi-tenancy is excellent — one of the architectural strengths. SaaS plan enforcement and self-hosted Docker config are the production-readiness gaps.

---

## 21. Localization & Accessibility (Features 104–106)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 104 | Multi-language UI (10+ languages) | ❌ | ❌ | ❌ | ❌ | 🟠 | P2 | Core | L | `users.language`, `organizations.locale` schema fields exist. No i18n library wired up. All strings hardcoded in English. |
| 105 | RTL layout support | ❌ | ❌ | ❌ | ❌ | ❌ | P3 | Fancy | L | Nothing. Would require RTL CSS + Expo RTL mode. |
| 106 | WCAG 2.1 AA accessibility | 🟡 | 🟡 | 🟡 | ❌ | — | P2 | Core | L | Basic: `aria-label`, `role=list`, semantic HTML on web. Mobile has `accessibilityRole`, `accessibilityLabel` on some screens. **No comprehensive audit or systematic coverage.** |

---

## 22. Security & Data Protection (Features 107–110)

| # | Feature | Status | W | M | D | BE | Priority | Core/Fancy | Effort | Notes |
|---|---------|--------|---|---|---|----|----------|-----------|--------|-------|
| 107 | GDPR compliance (export, deletion, consent) | ❌ | ❌ | ❌ | ❌ | ❌ | P1 | Core | L | No data export route (Art. 20), no data deletion route (Art. 17), no consent management. **Legally required for EU deployment.** |
| 108 | Encryption at rest + in transit | 🟡 | — | — | — | 🟡 | P0 | Core | M | In transit: HTTPS/TLS at proxy layer (assumed). Passwords: Argon2id (correct). Tokens: SHA-256. **No DB-level column encryption.** No encryption for file metadata. |
| 109 | Full audit log of all data access and modifications | 🟡 | ❌ | ❌ | ❌ | 🟡 | P1 | Core | M | `assetEvents` table covers asset mutations. **No audit of auth events (login, logout, failed attempts), user management changes, or settings modifications.** |
| 110 | Configurable data retention policies | ❌ | ❌ | ❌ | ❌ | 🟠 | P2 | Core | M | `archived_at` soft-delete on assets. No retention policy schema, no purge jobs, no per-org configuration. |

**Section summary:** Security fundamentals (Argon2id passwords, JWT, RBAC, multi-tenant isolation) are solid. The critical gap is GDPR — required by law for EU operations and completely absent. Audit logging covers assets but not auth or admin actions.
