# AGENT-ONBOARDING — Odoo-POS-Terminal

## Welcome, AGENT
This document defines the constraints and patterns for the Odoo-POS-Terminal project.

## Architecture & Conventions
- **Framework:** Python-based services on Raspberry Pi.
- **Hardware Integration:** Use dedicated Python libraries for LCD, RFID (MFRC522), and Thermal Printer (ESC/POS).
- **Communication:** XML-RPC for Odoo 17 connectivity.
- **Offline Mode:** Use local SQLite or JSON storage to queue offline transactions.
- **Enclosure:** Considerations for 3D printing and hardware assembly.

## Critical Workflows
- **Hardware Simulation:** Use mocks for hardware interfaces when developing on non-ARM systems.
- **Sync Logic:** Implement a robust background worker for syncing offline orders to Odoo.
- **Sync:** The project status is automatically synced to the Namka Mission Control dashboard via `PROJECT-SYNC.json` generated on every push to `main`.

## Verification Loop
1. Run local tests with mocked hardware.
2. Verify Odoo session management logic.
3. Validate and update `Master.md` and `AI_CHANGELOG.md` for each significant change.
