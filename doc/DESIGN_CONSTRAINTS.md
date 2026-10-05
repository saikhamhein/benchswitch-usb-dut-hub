# BenchSwitch USB DUT Hub: design constraints

This summarizes the retained **R5-LCSC prototype** design basis. Preserve its circuit, placement, copper, drills and frozen manufacturing data. CAD integrity checks and component screens are not measured electrical/thermal qualification. The target remains **1 A per port, 2 A shared DUT current, regulated 12–24 V input**.

## Preserve the electrical layout

- Keep continuous inner ground planes and anchored outer ground fills; do not split digital and buck grounds.
- Preserve local input-bypass return to GND/exposed pad, six external regulator thermal vias, compact switch-node copper, short bootstrap return and quiet feedback return. The external-via arrangement does not inherit the vendor's under-exposed-pad reference-board thermal resistance.
- Preserve broad raw-output and protected-supply manifolds, the lower distribution bus, 2 mm right-edge feed and parallel layer transfers. Narrow sensing/bias/package escapes are not substitutes for the main high-current path.
- Keep the local 100 nF port-switch input bypasses and four nominal 10 µF input capacitors. Preserve the crystal's 1/3 resonator and 2/4 ground mapping and the selected 2.0 × 1.2 mm lands.
- Preserve USB data geometry and its eleven `USB_ESCAPE` rule areas. The reviewed outer-ground clearance was at least 0.500 mm to data tracks; the upstream through-hole data pads have approximately 0.450 mm minimum clearance. This is geometry evidence, not controlled-impedance or signal-integrity certification.
- Both 0.30/0.50 mm and 0.30/0.60 mm drill/land vias exist. The smaller lands have 0.10 mm nominal annular rings; do not represent all vias as 0.60 mm lands.

## Exact sourcing constraints

Use `PCB/SELECTED_COMPONENTS.json` and the frozen BOM for all references. The five R5-LCSC replacement groups cover 30 fitted references without changing their electrical connections or physical placement:

- Ordinary 10 kΩ group: **Yageo RC0603FR-0710KL / C98220**, 15 resistors, 1%, 0603, 0.1 W at 70 °C, ±100 ppm/°C. These do not replace tighter-tolerance feedback resistors; apply normal power/temperature derating.
- C20/C27: **Yageo CC0402KRX7R8BB104 / C105883**, 100 nF, 25 V, ±10%, X7R, 0402. C20 bypasses 3V3 and C27 HOST_VBUS; these parts are not the 24 V input capacitors or raw-output bank.
- Q11–Q14: **onsemi MMBT3904LT1G / C81464**, SOT-23 NPN, pin 1 base / 2 emitter / 3 collector, 40 V, 200 mA continuous. Emitters are grounded; 10 kΩ collector pullups to 5V_SYS and 10 kΩ base resistors/100 kΩ pulldowns are retained. Normal collector current is approximately 0.5 mA.
- C64–C69/C82–C83: **Samsung CL31B106KBHNFNE / C913957**, eight 10 µF/50 V/±10%/X7R/1206 ceramics. Keep the Samsung lands and the three Aishi 220 µF/50 V bulk capacitors. Nominally similar capacitance, voltage and package labels alone do not qualify alternatives.
- L6: **MetalLions MNR8065T100MT / C18222125**, 10 µH ±20%. The retained Sunlord-named footprint is a compatible land/envelope, not MetalLions-supplied CAD: two 2.2 × 7.5 mm pads with 3.8 mm inner gap; body maximum 8.3 × 8.3 × 6.5 mm.

J11–J14 remain XUNPU USB-231-ARY / C720525. A visual connector model must not become a BOM substitution.

## Output-capacitor screen

The selected Samsung part has the same 141-point typical DC-bias dataset as the prior CL31B106KBHNNNE. At 5.1 V, interpolated typical capacitance is 8.4357 µF per part. Eight parts multiplied by 0.90 tolerance, 0.85 temperature and 0.85 engineering reserve give **43.8826 µF**. The bias data are typical 25 °C, 1 kHz, 1 Vrms reference data; the reserve is an assumption. The result is voltage-dependent, not a universal minimum-capacitance or transient guarantee. The complete ceramic/polymer network still requires loop and load-release tests.

Do not automatically substitute TDK CGA5L1X7R1H106KT0Y0N or a generic 10 µF/50 V/X7R/1206. Exact ordering-code equivalence, bias behavior, lands and maximum body clearance require review.

## Inductor and fault screen

The selected MetalLions row specifies 44 mΩ maximum DCR and 13 MHz minimum SRF. Its published **8.00 A saturation / 3.20 A heat** entries appear under manufacturer **Max.** headings and must not be relabeled as guaranteed minima; 8.90/3.70 A are typical. Test data are at 20 °C: saturation is about 30% inductance drop and heat current about 40 °C rise. Operating range is −40 to +125 °C including self-heating. No guaranteed hot saturation or L(T,I) lower bound is established.

The SCT2433 high-side peak limit at 24 V is 4.25/5.00/5.75 A minimum/typical/maximum. A screening case uses 5.088 V output, 2.204 A total converter load and 479.4 kHz (510 kHz × 0.94). At assumed 4.48 µH, ideal CCM ripple gives approximately **3.137 A peak and 2.269 A RMS**. The 4.48 µH includes tolerance and assumed temperature/bias factors, not a guaranteed inductance bound. Current-limit delay, overshoot, core/AC loss and board thermal effects remain unbounded by that calculation; hot overload and normal-load testing are required.

Do not substitute the shorter SWPA8040S100MT or MNR8040T100MT merely because the pads fit: their published 3.6 A saturation rating is below the regulator fault-limit range. A different larger inductor requires its own primary-data, footprint and routing review. Component screens cannot certify hot fault immunity, loop stability or mounting-temperature limits.

## Verification boundary

Fresh KiCad 10.0.6 checks of the final sources on 5 October 2026 reported zero ERC findings, zero DRC violations, zero unconnected items and zero schematic-parity findings under inherited settings, including seven disabled DRC and four disabled ERC check types. Cleanup changed project naming, synchronized the embedded/source USB-A default-footprint metadata and removed optional 3D bindings; electrical connections, placed parts, copper and frozen manufacturing payloads were preserved. These checks do not establish actual connector fit, board temperatures, voltage transients, automatic-placement calibration or production qualification. Revalidate any hardware change and complete [prototype bring-up](BRINGUP.md).

### Configured checks excluded from the passing result

The [source-hash-bound verification summary](VERIFICATION.json) records the actual KiCad 10.0.6 result. The following check types were ignored; zero findings does not claim these checks passed:

- ERC: `single_global_label`, `four_way_junction`, `simulation_model_issue`, `footprint_filter`.
- DRC: `missing_courtyard`, `track_not_centered_on_via`, `tuning_profile_track_geometries`, `footprint_filters_mismatch`, `pth_inside_courtyard`, `npth_inside_courtyard`, `footprint_type_mismatch`.
