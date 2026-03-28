# 6-Month Execution Strategy & Logistics

## Phase 1: The 90-Day MVP Sprint (Build & Break)

**Month 1: The "Frankenstein" Prototype**
* **Hardware:** Finalize EasyEDA schematic. Order 5 prototype boards from PCBWay (declare as "Engineering Samples" to mitigate early customs delays). Calibrate K1 Max CAD tolerances.
* **Software:** Stand up Hostinger VPS. Initialize FastAPI Antigravity endpoints (Heartbeat, Trigger QR, NFC Tap).
* **Ops:** File DA 185 and DA 185.4A1 forms with SARS for a permanent Importer's Code.

**Month 2: The Odoo Bridge & Firmware**
* **Hardware:** Assemble the first physical prototype upon PCBWay delivery.
* **Software:** Write ESP32 C++ firmware (Wi-Fi, LVGL graphics, NFC reading). Build custom Odoo module to intercept the "Pay" button and trigger the Antigravity API.

**Month 3: The Alpha Trial**
* **Deployment:** Install one polished prototype in a friendly local business (e.g., a coffee shop). 
* **Testing:** Monitor battery performance during load shedding and identify UI friction points. Free trial for the merchant in exchange for harsh feedback.

---

## Phase 2: The 90-Day Go-to-Market Sprint (Scale & Sell)

**Month 4: Iteration & Supply Chain**
* **Hardware:** Implement Alpha bug fixes. Order commercial batch 1 (25-50 boards) from PCBWay using the now-active SARS Importer Code. Batch print enclosures.
* **Software:** Harden API security. Finalize local payment gateway API access (SnapScan/Zapper).

**Month 5: Compliance & Commercial Prep**
* **Legal:** Draft Hardware-as-a-Service (HaaS) contracts.
* **Ops:** Set up automated Odoo billing to capture the $50/mo SaaS fee and 1% transaction fee.

**Month 6: Launch & Revenue**
* **Sales:** Deploy TCO calculator pitch deck. Close initial 5-10 merchants.
* **Fulfillment:** On-site installation and staff training. First MRR recognized.