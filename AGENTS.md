# BenchSwitch USB DUT Hub

This repository contains the R5-LCSC PCB, its frozen manufacturing packet, and essential build documentation. Start with README.md and doc/DESIGN_CONSTRAINTS.md.

## Layout

- PCB/: KiCad 10.0.6 native project, local symbols/footprints and required model assets.
- manufacturing/R5_LCSC/: frozen fabrication and procurement files. Preserve their original payload bytes unless a separately reviewed hardware revision is requested.
- manufacturing/tools/: release integrity and future export commands.
- doc/: PCB drawings, build, constraints and bring-up. Keep documentation concise; do not commit agent transcripts, private notes, scratch reviews, logs or editor backups.

## Working safely

- Use KiCad 10.0.6. Never downgrade file headers or save this board through an older KiCad version.
- Preserve circuit, copper, pads, placement, drills and exact fitted MPNs during housekeeping. Do not bulk-update libraries, refill or reroute as a side effect of documentation changes.
- Keep project-local library/model paths portable. Preserve third-party copyright, attribution and applicable license notices.
- A display model is not a qualified replacement part. BOM identity and conservative physical checks take priority over rendering appearance.
- Do not treat clean ERC/DRC or a passed file-integrity check as physical validation. Report disabled checks and all unrun/blocked tests.
- Use a current-limited supply and the bring-up checklist before real DUTs. Do not infer production ratings from prototype targets.

## Commands

From the repository root, with Python 3.9+:

```sh
python manufacturing/tools/verify_release.py
python manufacturing/tools/export_manufacturing.py --help
```

A future manufacturing export additionally requires KiCad 10.0.6:

```sh
python manufacturing/tools/export_manufacturing.py --output build/manufacturing
```

Never overwrite the frozen packet while checking a new revision. Review ERC, DRC, schematic parity, BOM identities, CAM outputs and placement calibration. Refresh the release manifest only after intentional changes are reviewed; do not rewrite historical validation as a new test result.
