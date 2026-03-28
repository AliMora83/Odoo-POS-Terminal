# Master Document: Rugged Odoo POS Terminal

**Project Name:** Odoo POS Customer Terminal (Africa Edition)
**Target Market:** Mid-to-High Volume African Retailers (Coffee shops, pharmacies, franchises) & Current Odoo Users.
**Core Value Proposition:** A decoupled, load-shedding-proof, Odoo-native hardware solution with a disruptive hybrid pricing model.

## 1. The Technology Stack
* **Hardware Brain:** ESP32-WROOM-32E Microcontroller
* **Customer Interface:** 2.8" SPI TFT LCD (ILI9341) & PN532 NFC Module
* **Power System:** TP4056 IC with 18650 Li-Ion Battery Backup (Load-shedding resilient)
* **Fabrication (Local):** Creality K1 Max (PETG/ABS Enclosures) printed in Pretoria.
* **Fabrication (Outsourced):** PCBWay (Turnkey PCBA Carrier Boards)
* **Middleware API:** Antigravity Framework (FastAPI) hosted on Hostinger VPS (namka.cloud)
* **ERP/Backend:** Odoo (Inventory, UI, Accounting)

## 2. Unit Economics & Pricing Model
* **Total Hardware BOM:** ~$34.00 USD
* **Upfront Hardware Price:** $150.00 USD (Generates immediate cash flow for manufacturing)
* **Monthly SaaS Fee:** $50.00 USD / Terminal (Covers server and API maintenance)
* **Transaction Fee:** 1.0% Flat (Highly competitive vs. traditional 2.75% models like Square)

## 3. Business Model Canvas

### Value Propositions
* **Zero-Downtime:** Built-in battery handles Stage 6 grid failures; offline-first memory prevents data loss.
* **Radical Cost Savings:** 1% transaction fee saves high-volume merchants thousands annually.
* **Native Odoo Integration:** No messy third-party syncing; hardware talks directly to their ERP.
* **Mobile Money Ready:** Instantly renders dynamic QR codes for SnapScan, M-Pesa, etc.

### Customer Segments
* Local retail franchises moving >$10k/month.
* Existing Odoo enterprise clients needing a modern customer-facing terminal.

### Channels & Sales
* Direct B2B Outbound Sales using our TCO Savings Calculator.
* Strategic partnerships with local Odoo integration agencies.
* High-conversion landing page on namka.cloud.

### Key Resources & Activities
* Odoo Developer Certification logic.
* Supply Chain Management (PCBWay bulk orders + SARS Importer clearance).
* Local Hardware Assembly & QA testing.

## 4. Long-Term Vision (Embedded Finance)
Once the hardware footprint is established and API data is flowing, Phase 2 involves integrating Banking-as-a-Service (BaaS) APIs to offer Merchant Cash Advances (MCA) and next-day wallet settlements directly inside the client's Odoo dashboard.