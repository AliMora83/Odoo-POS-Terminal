# 🧭 Odoo POS Terminal

> A decoupled, load-shedding-proof, Odoo-native customer-facing POS terminal built on ESP32 hardware — targeted at mid-to-high volume African retailers.

---

## 📌 Overview

**Odoo POS Terminal** is a hardware + software POS solution built for African retailers who are existing Odoo users. It handles offline-first transactions, integrates with the Odoo POS & Accounting modules via a FastAPI middleware layer (Antigravity), and is resilient to load shedding via built-in battery backup.

- **Owner:** Ali Mora
- **Location:** Johannesburg, ZA
- **Updated:** 2026-03-28
- **Status:** 🔴 Priority 1 — Ship Now (In Progress — 20%)
- **Stack:** ESP32 (FreeRTOS) / FastAPI (Antigravity) / Odoo JSON-RPC / Python / EasyEDA / PCBWay PCBA
- **Repo:** [https://github.com/AliMora83/Odoo-POS-Terminal](https://github.com/AliMora83/Odoo-POS-Terminal)
- **Live URL:** [https://namka.cloud](https://namka.cloud) _(middleware landing + API host)_

---

## 🎯 Mission

Build and ship a load-shedding-proof, Odoo-native POS terminal for African retailers — leveraging ESP32 hardware, FastAPI middleware, and SnapScan/M-Pesa QR payments — at a disruptive 1% transaction fee.

---

## 🏗 Infrastructure

| Service | Purpose |
|---------|---------|
| GitHub (AliMora83) | Source code |
| Odoo.sh | Odoo backend (POS + Accounting modules) |
| Hostinger VPS (namka.cloud) | Antigravity FastAPI middleware host |
| PCBWay | Sole approved PCBA vendor |
| EasyEDA | PCB design (Gerber + BOM + CPL export) |

---

## 🤖 AI Agents

This project uses a **Multi-Agent Context Protocol (MACP)** to coordinate AI assistants:

| Agent | Role |
|-------|------|
| **Gemini** | Internal orchestration only — not shipped in production |
| **Claude** | Full-stack agent — architecture & TypeScript |
| **Qwen** | Build agent — Python, autonomous implementation |
| **Comet (Perplexity)** | Cross-check, ratification, architecture review |

Review consensus states: `Unreviewed` → `Agent Reviewed` → `Cross-Checked` → `Ratified`

---

## 📋 Dev Mission Control

- **Master.md (this project):** [docs/Master.md](https://github.com/AliMora83/Odoo-POS-Terminal/blob/master/docs/Master.md)
- **Namka Mission Control:** [https://github.com/AliMora83/Namka-Mission-Control/blob/main/Master.md](https://github.com/AliMora83/Namka-Mission-Control/blob/main/Master.md)

---

## 🤖 Instructions for AI Agents

> **If you are an AI assistant (Claude, Gemini, Qwen, Perplexity, or any agent) reading this file:**

Before starting any work on this project, you **must** read the full `docs/Master.md` file. It is the single source of truth and contains:

- Current goal, next step, and blockers
- Full system architecture and key architectural rules
- Tech stack and hardware BOM
- Ratified architecture decisions from previous AI reviews
- MACP workflow and review protocol

### 📥 Master.md — Direct Link

```
https://github.com/AliMora83/Odoo-POS-Terminal/blob/master/docs/Master.md
```

Raw (for programmatic access):

```
https://raw.githubusercontent.com/AliMora83/Odoo-POS-Terminal/master/docs/Master.md
```

### ✅ Briefing Protocol

Use this prompt at the start of any session:

> *"Before starting [task], read `docs/Master.md` at the URL above and check the **AI Reviews & Artifacts** section for existing ratified decisions. Do not re-architect anything marked `Ratified` without explicit approval from Ali."*

### 🔁 After Your Work

Commit any decisions, architecture choices, or review notes back to `docs/Master.md` under the **AI Reviews & Artifacts** section, following the existing format. Set status to `Agent Reviewed` for your entry so the next agent knows to cross-check it.

---

## 📄 Using This README

This README is the public-facing entry point for the project. Keep it concise — `docs/Master.md` is the canonical source of truth for deep context, architecture decisions, and sprint tracking.

---

_Last updated by: Perplexity (Comet) on 2026-03-28_
