# Third-party and component-model notices

The native PCB and schematic are the design sources. 3D models are visual aids; they do not establish part interchangeability, physical fit, clearance or electrical qualification.

## KiCad libraries

The frozen symbols and footprints include KiCad-derived material. The KiCad community attribution and full CC-BY-SA 4.0 terms with the electronic-design exception are retained in:

- [Symbol notices](../PCB/frozen_libraries/kicad-symbols-COPYRIGHT.txt)
- [Footprint notices](../PCB/frozen_libraries/kicad-footprints-COPYRIGHT.txt)

These notices also apply to KiCad-derived portions of custom footprints, including the AOS TO-252 and Samsung 1206 adaptations. Custom library naming does not imply that every definition is entirely original. Preserve attribution and applicable share-alike obligations when redistributing library material. The electronic-design exception is stated in the included notices; it is not a blanket relicensing of a library collection.

## KiCad 3D assets

Keep the copyright and licensing headers embedded in each retained STEP file.

- `D_SMC.step` and `D_SOD-123F.step` carry **GPL-3.0-or-later** with an electronic-design exception. The [GPL-3.0 text](../PCB/3d_models/GPL-3.0.txt) accompanies them. Their embedded exception says that embedding the symbol or unaltered portions into a design does not by itself make the resulting design GPL-covered; it does not invalidate other reasons the design may be covered. Their exact exception text remains in each model.
- Other retained KiCad package STEP files carry their embedded **CC-BY-SA 4.0 with electronic-design exception** notices. The full CC-BY-SA terms are included in the library notices above.

The retained files are not relicensed by this project. Frozen footprint templates were modified only to remove inherited nonlocal 3D-model references; the Phoenix custom footprint also has its optional vendor-model bindings removed. Footprint pads and other 2D geometry are unchanged. The USB-A default footprint name was synchronized in the source library and embedded schematic symbol to the retained XUNPU footprint already used by all four placed USB-A connectors; symbol pin definitions and placed instance footprints are unchanged.

## Project-created models

Nominal and display models are simplified, drawing-derived package geometry rather than manufacturer-certified solids. Features such as internal contacts, draft, markings and finish may be omitted. Use component datasheets and physical measurements for engineering decisions.

## Omitted optional vendor CAD

The public release excludes the optional Wurth USB-A and Phoenix terminal/mating-plug vendor solids, their PCB/footprint model bindings and populated STEP aggregates. Redistribution rights for those recovered solids were not established for this public package. The native 2D footprint pads, copper, placement, component identities and frozen manufacturing payloads remain unchanged.

Consequently, those components may be absent from a 3D view. The purchased USB-A parts remain **XUNPU USB-231-ARY / C720525**, and the input terminal and mating plug remain the Phoenix parts specified in the exact BOM/accessory list. No replacement-part compatibility is claimed.

## Project license

No project-wide open-source license has been selected. Public availability does not replace third-party terms or grant a new blanket license to the original project material.

## Optional vendor-model downloads

The electrical project opens and the supplied fabrication package can be used without these optional 3D visuals. For a local visualization, obtain CAD directly from the manufacturer and follow the terms shown with the download:

- [Wurth WR-USB Standard](https://www.we-online.com/en/components/products/INPUT_OUTPUT_WR_USB_STANDARD): select **614004190021** and its STP download. This is a visualization surrogate, not the ordered XUNPU USB-A part.
- [Phoenix Contact MSTBA 2,5/2-G-5,08, 1757242](https://www.phoenixcontact.com/en-us/products/pcb-header-mstba-25-2-g-508-1757242): product CAD/downloads for the PCB header; [original model download](https://www.phoenixcontact.com/product/product/MTc1NzI0Mg/downloads/7966887?_realm=us&_locale=en-US).
- [Phoenix Contact MSTB 2,5/2-ST-5,08, 1757019](https://www.phoenixcontact.com/en-us/products/pcb-plug-mstb-25-2-st-508-1757019): product CAD/downloads for the mating plug; [original model download](https://www.phoenixcontact.com/product/product/MTc1NzAxOQ/downloads/8194525?_realm=us&_locale=en-US).

Add any locally downloaded file through KiCad's footprint 3D-model settings and check orientation, origin and alignment yourself. A newer vendor download may differ from the former private model; no alignment or interchangeability is assumed. Keep private downloads outside the published source tree unless redistribution permission is established. Do not modify pads, placement, copper or the frozen Gerbers just to improve a render.
