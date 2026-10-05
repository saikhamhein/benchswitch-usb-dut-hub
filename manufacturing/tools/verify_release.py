#!/usr/bin/env python3
"""Verify shipped bytes, local CAD dependencies and exact fitted BOM identities.
This is a file-integrity check, not ERC/DRC or physical qualification.
Python 3.9+; standard library only.
"""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]


def verify():
    manifest = json.loads((ROOT / 'manufacturing/RELEASE_SHA256.json').read_text())
    for relative, expected in manifest['files'].items():
        path = ROOT / relative
        if not path.is_file():
            raise ValueError('Missing release file: ' + relative)
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Changed release file: ' + relative)
    pcb = ROOT / 'PCB'
    board = pcb / 'BenchSwitch_USB_DUT_Hub.kicad_pcb'
    references = 0
    for path in [board, *pcb.rglob('*.kicad_mod')]:
        for model in re.findall(r'\(model\s+"([^\"]+)"', path.read_text()):
            if model.startswith('${KIPRJMOD}/'):
                if not (pcb / model[len('${KIPRJMOD}/'):]).is_file():
                    raise ValueError('Missing local model: ' + model)
                references += 1
            else:
                raise ValueError('Unexpected model path: ' + model)
    for table in ('fp-lib-table', 'sym-lib-table'):
        for uri in re.findall(r'\(uri\s+"([^\"]+)"', (pcb / table).read_text()):
            if not uri.startswith('${KIPRJMOD}/') or not (pcb / uri[len('${KIPRJMOD}/'):]).exists():
                raise ValueError('Missing or nonlocal library: ' + uri)
    selection = json.loads((pcb / 'SELECTED_COMPONENTS.json').read_text())
    selected = {x['ref']: (x['mpn'], x['lcsc']) for x in selection['parts']}
    with (ROOT / 'manufacturing/R5_LCSC/assembly/BOM_exact_per_reference.csv').open(newline='') as stream:
        bom = {x['Reference']: (x['MPN'], x['LCSC']) for x in csv.DictReader(stream)}
    if selected != bom or len(selected) != 131:
        raise ValueError('Selected identities do not match the 131 fitted BOM references')
    package = ROOT / 'manufacturing/R5_LCSC'
    for relative, expected in json.loads((package / 'EXPORT_SHA256.json').read_text())['files'].items():
        if hashlib.sha256((package / relative).read_bytes()).hexdigest() != expected:
            raise ValueError('Manufacturing checksum differs: ' + relative)
    print(f"PASS: {len(manifest['files'])} release files, {references} local model bindings, local libraries and 131 fitted BOM identities.")
    print('No ERC/DRC, CAM approval or physical qualification is implied.')


if __name__ == '__main__':
    try:
        verify()
    except (OSError, ValueError, KeyError) as error:
        sys.exit('FAIL: ' + str(error))
