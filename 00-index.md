# Orbit — External Code Review
### Commissioned for Stakeholders | Based on v0.2.0 codebase

> **Reviewer note:** This review audits every feature in `docs/all_the_functions.md` against the actual source code at `apps/api`, `apps/web`, `apps/mobile`, and `apps/desktop`. No feature status was assumed — all findings are grounded in code that was read directly.

---

## Table of Contents

| File | Content |
|------|---------|
| [01-features-01-30.md](./01-features-01-30.md) | Asset Registry, Locations, Check-in/out, Work Orders |
| [02-features-31-65.md](./02-features-31-65.md) | Maintenance, Inspections, Audits, Scheduling, Documents, Forms, Inventory, Analytics |
| [03-features-66-110.md](./03-features-66-110.md) | Notifications, Users, Mobile, IoT, Integrations, Platform, Localization, Security |
| [04-recommendations.md](./04-recommendations.md) | Priority actions, quick wins, deferrals, missing-but-mandatory |

---

## Status Key

| Symbol | Meaning |
|--------|---------|
| ✅ | Implemented — backend route + frontend UI both functional with real data |
| 🟡 | Started — significant work done, not end-to-end functional |
| 🟠 | Planned — schema field or UI scaffold only, no working logic |
| ❌ | Not Found — nothing in codebase |
| 🔲 | Tested — has test coverage (applies to none currently) |

**Platform columns:** `W` = Web · `M` = Mobile · `D` = Desktop · `BE` = Backend API

---

## Executive Summary

### Codebase Health at a Glance

| Area | Assessment |
|------|-----------|
| Database schema | Solid. 24 tables, well-indexed, good use of JSONB and enums |
| API routes | Implemented for all major entities. Some stubs and TODOs remain |
| Web frontend | Pages exist for all sections. Most still use **mock data**, not wired to real API |
| Mobile | Expo structure complete. Scanner has critical stub. Home screen uses real API |
| Desktop | Shell only (`src/main.ts`). No functional code |
| Background workers | Email worker functional. Notification, Maintenance, Webhook workers are **empty TODOs** |
| Tests | **Zero test files exist** across the entire codebase |
| Auth security | JWT auth implemented. Token refresh **not implemented**. Web middleware validates cookie presence only — no actual token validation |

### Feature Implementation Scorecard

| Category | Total Features | ✅ Impl. | 🟡 Started | 🟠 Planned | ❌ Not Found |
|----------|---------------|---------|-----------|-----------|------------|
| Asset Registry | 8 | 4 | 2 | 1 | 1 |
| Onboarding | 3 | 0 | 1 | 0 | 2 |
| Lifecycle | 2 | 1 | 0 | 0 | 1 |
| Locations | 3 | 2 | 1 | 0 | 0 |
| Check-in/out | 4 | 3 | 1 | 0 | 0 |
| Work Orders | 7 | 3 | 1 | 0 | 3 |
| Maintenance | 7 | 2 | 1 | 2 | 2 |
| Inspections | 6 | 2 | 2 | 1 | 1 |
| Audits | 4 | 2 | 1 | 0 | 1 |
| Scheduling | 5 | 3 | 0 | 0 | 2 |
| Documents | 4 | 1 | 2 | 1 | 0 |
| Custom Forms | 4 | 1 | 1 | 0 | 2 |
| Inventory | 5 | 4 | 0 | 0 | 1 |
| Analytics | 6 | 2 | 2 | 0 | 2 |
| Notifications | 5 | 1 | 2 | 0 | 2 |
| Users & Auth | 6 | 2 | 1 | 0 | 3 |
| Mobile | 4 | 0 | 2 | 0 | 2 |
| IoT | 9 | 0 | 1 | 1 | 7 |
| Integrations | 5 | 0 | 2 | 0 | 3 |
| Platform | 6 | 1 | 2 | 0 | 3 |
| Localization | 2 | 0 | 0 | 0 | 2 |
| Accessibility | 1 | 0 | 1 | 0 | 0 |
| Security | 4 | 0 | 2 | 0 | 2 |
| **TOTAL** | **110** | **34** | **30** | **6** | **40** |

**Fully implemented: 31% · Partially started: 27% · Effectively missing: 42%**

---

## Most Critical Immediate Risks

1. **Scanner is broken** — QR code lookup uses a hardcoded string prefix check, not an API call. Core user flow is non-functional.
2. **3 of 4 background workers are empty TODOs** — maintenance scheduling, push notifications, and webhook dispatch never fire.
3. **Web session validation is a stub** — middleware only checks if a cookie *exists*, never validates the JWT.
4. **Token refresh not implemented** — access tokens expire with no recovery path on mobile.
5. **Zero tests** — no unit, integration, or E2E tests anywhere in the codebase.
