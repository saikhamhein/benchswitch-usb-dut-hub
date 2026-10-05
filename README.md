# BenchSwitch USB DUT Hub

A four-port USB 2.0 DUT hub for embedded firmware development and automated hardware testing.

BenchSwitch was born from a practical need in agentic firmware development: let the development workflow power-cycle a device instead of waiting for someone to unplug it. The design combines a USB2514B hub controller with individually switched downstream power, targeting host control through tools such as `uhubctl`.

**Prototype: hardware testing is pending.** See the [build guide](doc/BUILD.md), [design constraints](doc/DESIGN_CONSTRAINTS.md) and [bring-up checklist](doc/BRINGUP.md) before building or powering a board.

## Hardware

- Four USB-A DUT ports and one USB-B upstream connection
- Per-port CH217A power switching and overcurrent signalling
- Regulated 12–24 V DC input with buck conversion
- Design targets: 1 A per port, 2 A shared DUT current
- 95 × 80 mm, four-layer PCB
- KiCad 10.0.6 sources; 131 fitted components across 41 catalog groups

## Build

Open [BenchSwitch_USB_DUT_Hub.kicad_pro](PCB/BenchSwitch_USB_DUT_Hub.kicad_pro) in KiCad 10.0.6.

- [Schematic](doc/PCB_Schematic_R5_LCSC.pdf) and [assembly drawing](doc/PCB_Assembly_R5_LCSC.pdf)
- [Gerber ZIP](manufacturing/R5_LCSC/DIN_USB_Hub_A8_R5_LCSC_Gerber.zip)
- [Exact component BOM](manufacturing/R5_LCSC/assembly/BOM_exact_per_reference.csv) and [per-board procurement list](manufacturing/R5_LCSC/LCSC_PROCUREMENT_PER_BOARD.csv)

With Python 3.9+, verify the release files or export to a new directory:

```sh
python manufacturing/tools/verify_release.py
python manufacturing/tools/export_manufacturing.py --output build/manufacturing
```

## Files

- `PCB/`: native design, symbols, footprints and models
- `manufacturing/`: fabrication files, BOM and build tools
- `doc/`: drawings, assembly guidance and test procedures

[CAD verification](doc/VERIFICATION.json) · [Third-party notices and optional model downloads](doc/THIRD_PARTY.md)
