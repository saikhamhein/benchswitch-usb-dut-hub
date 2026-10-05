# BenchSwitch USB DUT Hub: build

R5-LCSC is a four-port USB 2.0 PCB for self assembly. Its characterization target is **1 A per port and 2 A shared DUT current**, using a regulated **12–24 V DC** bench supply. These are prototype targets, not qualified operating ratings. Read [bring-up](BRINGUP.md) before connecting DUTs.

## Fabrication and parts

Use the frozen R5-LCSC files, whose legacy filenames are retained:

- Bare PCB: `manufacturing/R5_LCSC/DIN_USB_Hub_A8_R5_LCSC_Gerber.zip`
- Fitted component BOM: `manufacturing/R5_LCSC/assembly/JLC_BOM_QUOTE_ONLY.csv`
- Per-board purchasing quantities: `manufacturing/R5_LCSC/LCSC_PROCUREMENT_PER_BOARD.csv`
- Exact selected identities: `PCB/SELECTED_COMPONENTS.json`

Fabrication parameters: **95 × 80 mm, four layers, 1.6 mm, green soldermask, lead-free HASL, standard/default JLC 7628 stackup, 1 oz outer copper and default inner copper**. Do not add paid impedance control, ENIG, Kelvin testing or a small-via option to this build. Minimum via drill is 0.30 mm; copper lands include both 0.50 and 0.60 mm diameters. The 0.50 mm lands have a nominal 0.10 mm annular ring; confirm CAM acceptance of the actual files. Existing USB geometry is unverified for this stackup; no 90-ohm production impedance claim is made.

There are **131 fitted PCB parts in 41 catalog groups**. Add one separate **Phoenix 1757019 / LCSC C90073** mating input plug per completed board. Derive quantities from per-board usage and the intended populated-board count, then round the totals once to current supplier MOQ/multiples. Saved stock and prices are historical; recheck all components before obtaining a new bare-PCB quote. Previous quotes are superseded. No PCBA service is requested; checkout is separate.

No assembly rails are required for self assembly. If a supplier adds rails, prefer left/right; top/bottom rails need a routed separation gap for overhanging USB shells.

## Self assembly and mounting

1. Compare received parts with the exact BOM. Keep DNP parts unpopulated, including optional C106/C206/C306/C406 timing capacitors. Use [design constraints](DESIGN_CONSTRAINTS.md) before considering any substitution.
2. Assemble from native PCB reference designators and pad markings. Check IC pin 1, diode and polarized-capacitor orientation, transistor pinouts, regulator exposed-pad soldering and actual resistor values. Use component-approved soldering processes; inspect for bridges, open joints and damaged pads before power.
3. Confirm connector fit using the purchased connectors and actual cables. J11–J14 are **XUNPU USB-231-ARY / C720525**; Optional Wurth and Phoenix vendor 3D visuals are omitted from this public package; this does not change the ordered parts or 2D pad geometry.
4. Secure the PCB on electrically insulated supports. Ensure screws, washers, inserts and other metal cannot contact or bridge copper on either face, including after cable insertion force or board flex. Verify clearances with the actual hardware before power. Do not operate the board on a conductive surface.
5. With input power removed, wire and mate the Phoenix terminal, checking polarity against the PCB/schematic. Use a current-limited supply for first power; keep valuable DUTs disconnected until the relevant tests pass.

The retained CPL/placement data have unresolved library-origin and rotation calibration issues. They are reference data, not automated-placement approval, and are not needed for bare-PCB ordering or manual assembly.

## Exporting a future revision

Open `PCB/BenchSwitch_USB_DUT_Hub.kicad_pro` in **KiCad 10.0.6** with the repository's local libraries. From the repository root, use `python manufacturing/tools/export_manufacturing.py --output <new-output-directory>` with initialized, writable KiCad configuration. Use a new, non-existing output directory each time; existing directories and symbolic-link output paths are refused to prevent stale files entering a fabrication ZIP. Keep the frozen `manufacturing/R5_LCSC` package unchanged until a separately reviewed revision is intended.

The exporter checks ERC, DRC, schematic parity and exact selected-part/BOM consistency, then creates quote files. Review CAM and every exported package; a newly generated CPL still needs origin/rotation calibration. The final renamed sources were checked with KiCad 10.0.6 on 5 October 2026: zero ERC findings and zero DRC, unconnected-item or schematic-parity findings. These checks retain seven disabled DRC and four disabled ERC check types. The frozen manufacturing payloads were preserved, not replaced by a new export. Export success does not establish physical qualification.

Every remaining board and footprint-library model reference is project-local. Optional vendor solids and inherited global-library 3D references were removed for a self-contained release; footprint pads and native PCB geometry are unchanged. Avoid bulk-updating footprints just to refresh a 3D view.
