# Master — Odoo-POS-Terminal

## Project Vision
A custom hardware/software Point of Sale terminal integrated with Odoo. Features include offline transaction support, RFID card authentication, and thermal printer integration. Designed for resilience in low-connectivity environments.

## Metadata
- **Project ID:** Odoo-POS-Terminal
- **Status:** Active Development
- **Version:** 1.0.1
- **Last Sync:** 2026-03-31
- **Stack:** Python / Odoo / Raspberry Pi / Thermal Printer / RFID

## Roadmap & Progress
### Phase 1 — Hardware Interface
- [x] Raspberry Pi GPIO mapping
- [x] Thermal printer driver integration
- [x] RFID reader communication layer
- [x] Basic LCD/OLED display output

### Phase 2 — Odoo Integration
- [/] XML-RPC wrapper for POS orders
- [/] Local synchronization engine (offline-first)
- [ ] Inventory adjustment sync
- [ ] Session management (Open/Close)

### Phase 3 — Enclosure & Field Testing
- [ ] 3D-printable enclosure design
- [ ] Battery management system
- [ ] Pilot testing in actual sales environment

## Deployment Strategy
- **Target:** Raspberry Pi (Raspbian)
- **Environment:** Embedded Linux
- **Deployment:** Manual over SSH / Git Pull

## Related Documents
- [README.md](README.md): Project overview and setup.
