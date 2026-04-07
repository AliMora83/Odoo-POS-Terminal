# Master-Update.md — Odoo POS Terminal

> **Status:** 📋 READY FOR REVIEW
> **Authored by:** Claude (UX & Product Owner)
> **Date:** 2026-04-07
> **Session:** Namka Control Alignment
> **Based on:** docs/Master.md v1.0.2 + Active-Projects.md from Namka Control

---

## 🎯 Objective

Align Odoo POS Terminal project governance with the Namka Control multi-agent coordination protocol (MACP) and establish the "Hello Odoo" Sprint as the next approved phase.

---

## 📋 Review Status

| Component | Status | Notes |
|---|---|---|
| **PROJECT-SYNC.json** | ✅ Updated | Now feeds into Namka Control dashboard + future Supabase aggregation |
| **GitHub Actions Workflow** | ✅ Created | Auto-syncs PROJECT-SYNC.json on push to main |
| **Governance Alignment** | 📋 Ready | Links to Namka Control, MACP workflow confirmed |
| **Hello Odoo Sprint** | 🔄 Proposed | See sprint scope below |

---

## 🏗 Proposed: "Hello Odoo" Sprint

**Goal:** Prove the full data path end-to-end before touching hardware.

**Deliverables:**
1. Antigravity FastAPI scaffold at `/api/health` (simple return `{"status": "ok"}`)
2. Antigravity endpoint `POST /terminal/order` accepts simulated ESP32 payload
3. Python/Postman script simulates ESP32 sending a transaction to Antigravity
4. Antigravity calls Odoo JSON-RPC to create a POS order
5. Verify POS order appears in Odoo back-office under the configured session

**Effort Estimate:** M (Medium — 1 week)

**Success Criteria:**
- [ ] `POST /terminal/order` endpoint returns `200 OK`
- [ ] Simulated transaction payload accepted without errors
- [ ] POS order created in Odoo visible in back-office
- [ ] No direct ESP32 ↔ Odoo communication (Antigravity is sole intermediary)
- [ ] Offline-first queue design documented (for Phase 2 implementation)

**Blockers:**
- Payment acquiring entity / PSP licence — **Not required for this sprint**, defer to Phase 1 shipping gate

---

## 🔄 MACP Integration

This project now follows the same multi-agent coordination protocol as Namka Control:

- **Master.md** → Approved operating truth (updated)
- **Master-Update.md** → Review and proposed changes (this file)
- **AG-Update-*.md** → Execution work orders (to be authored by Claude post-approval)
- **AI_CHANGELOG.md** → Auto-maintained context log (created)
- **PROJECT-SYNC.json** → Aggregated into Namka Control dashboard (auto-synced)

### Review Gate

| Agent | Vote | Status |
|---|---|---|
| **Gemini** | ⏳ Open | Architect — confirm FastAPI scaffold approach |
| **Comet** | ⏳ Open | Auditor — verify Odoo JSON-RPC integration strategy |
| **Claude** | ✅ Ready | UX/Product — Hello Odoo Sprint approved pending cross-checks |

---

## 🔗 Namka Control Integration

**Central Dashboard:** https://github.com/AliMora83/namka-control

**This project's data:**
- Feeds into Namka Control via auto-updated `PROJECT-SYNC.json`
- Visible on dashboard at `https://control.namka.cloud` (when Supabase realtime ships in Phase 3 Sprint 2)
- Part of Priority 1 portfolio alongside Namka Control Dashboard and SmartPress

**Supabase Aggregation (Future):**
- When Namka Control Phase 3 Sprint 2 completes, GitHub Action will upsert this project's data to Supabase
- Dashboard will show live updates without polling

---

## ⚠️ Pre-conditions for Hello Odoo Sprint Approval

Before Claude authors the AG-Update work order, confirm:

- [ ] **Gemini approves FastAPI approach** — No architectural conflicts with existing Antigravity design
- [ ] **Comet verifies Odoo JSON-RPC flow** — Credentials management, versioning strategy confirmed
- [ ] **Ali confirms timeline** — "Hello Odoo" can start immediately post-approval

---

## 📝 Next Steps

1. **Gemini:** Review FastAPI scaffold approach, confirm compatible with Odoo JSON-RPC
2. **Comet:** Verify Odoo credentials handling, review offline-queue design doc
3. **Claude:** Once both votes in → author `AG-Update-HelloOdoo.md` work order
4. **AG:** Execute work order and report outcomes to `AI_CHANGELOG.md`

---

*Authored by Claude (UX & Product Owner) — Namka Control Alignment Session*
