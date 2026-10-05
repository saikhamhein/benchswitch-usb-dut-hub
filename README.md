# BenchSwitch USB DUT Hub

**A four-port USB 2.0 DUT hub for embedded firmware development and automated hardware testing.**

BenchSwitch grew out of a practical need in **agentic firmware development**: software can build, flash and test firmware, but a device that needs a power cycle can still bring an unattended workflow to a stop. The project puts individually switched USB power on the bench so that device recovery can become part of the development loop.

The hardware is designed around a USB2514B hub controller, four downstream USB-A ports and per-port VBUS switches. It targets host-driven power control with tools such as `uhubctl`, while keeping the electrical design, exact component identities and PCB fabrication files together in a small, buildable repository.

> **Prototype status:** R5-LCSC targets 1 A per port and 2 A shared DUT current from a regulated 12–24 V supply. These are characterization targets, not qualified ratings. Physical bring-up, power-cycle behavior, USB compatibility, protection response and thermal performance still need measurement.

## At a glance

- Four USB 2.0 downstream DUT ports and one USB-B upstream connection
- USB2514B hub controller with individual downstream power-control signals
- Per-port CH217A load switching and overcurrent signalling
- 12–24 V regulated bench input, buck conversion and basic overvoltage disconnect
- 95 × 80 mm, four-layer PCB; KiCad 10.0.6 native sources
- 131 fitted components across 41 catalog groups; bare-PCB fabrication and self assembly

The repository covers **embedded systems hardware, PCB design, power electronics, USB integration and hardware test automation**. It contains the PCB and build information only; enclosure designs and development-review working files are excluded.

## Start here

1. Read the [build guide](doc/BUILD.md) and [design constraints](doc/DESIGN_CONSTRAINTS.md).
2. Open [BenchSwitch_USB_DUT_Hub.kicad_pro](PCB/BenchSwitch_USB_DUT_Hub.kicad_pro) in **KiCad 10.0.6**. Keep the project-local libraries with it.
3. Review the [schematic](doc/PCB_Schematic_R5_LCSC.pdf), [PCB assembly drawing](doc/PCB_Assembly_R5_LCSC.pdf), and [exact fitted BOM](manufacturing/R5_LCSC/assembly/BOM_exact_per_reference.csv).
4. Use the frozen [Gerber ZIP](manufacturing/R5_LCSC/DIN_USB_Hub_A8_R5_LCSC_Gerber.zip) for the R5-LCSC board and [per-board procurement CSV](manufacturing/R5_LCSC/LCSC_PROCUREMENT_PER_BOARD.csv) for purchasing quantities. Recheck stock, supplier multiples and CAM acceptance before ordering.
5. Follow the [bring-up checklist](doc/BRINGUP.md) with a current-limited supply and dummy loads before attaching valuable DUTs.

## Repository layout

```text
README.md
AGENTS.md
PCB/              Native KiCad project and required local libraries/models
manufacturing/    Frozen fabrication/BOM package and export/verification tools
doc/              PCB drawings, build guide, design constraints and bring-up
```

The project name is BenchSwitch USB DUT Hub. **R5-LCSC** remains the hardware revision; legacy filenames inside the frozen manufacturing package and drawing titles identify that same design. The cleanup does not change the ordered circuit, placement, copper, drills or component identities. Optional vendor 3D visuals and their bindings are omitted; see the third-party notes.

## Checks and future exports

Check the packaged files and source dependencies with Python 3.9+:

```sh
python manufacturing/tools/verify_release.py
```

For a future reviewed revision, use Python 3.9+ and KiCad 10.0.6:

```sh
python manufacturing/tools/export_manufacturing.py --output build/manufacturing
```

The exporter refuses to overwrite the frozen package. A successful export is still a quote package: inspect CAM and any component-placement data. The retained CPL has unresolved library-origin/rotation calibration and is **not automated-assembly approval**.

The final sources were checked with **KiCad 10.0.6 on 5 October 2026**: ERC reported zero findings; DRC reported zero violations, zero unconnected items and zero schematic-parity findings. See the [source-hash-bound verification summary](doc/VERIFICATION.json). These results use the inherited rule settings, including **seven disabled DRC check types and four disabled ERC check types**. The supplied stackup has no verified controlled-impedance claim. Hash checks and clean CAD reports do not establish measured electrical, thermal or mechanical qualification.

## Source and third-party notices

The native KiCad design is authoritative. Component models are visual aids, not proof of part interchangeability or mechanical fit. See [third-party and model notes](doc/THIRD_PARTY.md) for provenance, optional manufacturer download links and limits. Individual third-party library notices remain alongside their files. No project-wide open-source license is assigned by this repository cleanup.
