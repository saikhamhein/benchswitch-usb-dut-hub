#!/usr/bin/env python3
"""Export quote-only fabrication files from the repository's current KiCad source.
Requires KiCad 10.0.6 command-line tools. This does not submit an order or approve CAM.
"""
import argparse, collections, csv, hashlib, json, pathlib, subprocess, xml.etree.ElementTree as ET, zipfile
repo = pathlib.Path(__file__).resolve().parents[2]
p = argparse.ArgumentParser()
p.add_argument('--project', type=pathlib.Path, default=repo/'PCB')
p.add_argument('--output', type=pathlib.Path, default=repo/'build/manufacturing')
a = p.parse_args(); project = a.project.resolve()
if a.output.is_symlink() or any(parent.is_symlink() for parent in a.output.absolute().parents):
    raise SystemExit('Output path must not traverse a symbolic link.')
out = a.output.resolve()
if out == (repo/'manufacturing/R5_LCSC').resolve() or out.is_relative_to((repo/'manufacturing/R5_LCSC').resolve()):
    raise SystemExit('Refusing to overwrite the frozen R5_LCSC package; use build/manufacturing or another new directory.')
if out.exists():
    raise SystemExit('Output directory already exists; choose a new directory to avoid mixing stale fabrication files.')
version = subprocess.check_output(['kicad-cli', 'version'], text=True).strip()
if version != '10.0.6':
    raise SystemExit('KiCad 10.0.6 is required; found ' + version + '. No exports were written.')
out.mkdir(parents=True, exist_ok=False)
for folder in ['gerbers', 'assembly', 'validation']:
    (out/folder).mkdir()
name = 'BenchSwitch_USB_DUT_Hub'
board, schematic = project/(name+'.kicad_pcb'), project/(name+'.kicad_sch')
def run(*args):
    subprocess.run(['kicad-cli', *map(str, args)], check=True)
run('sch','erc','--format','json','--severity-all','-o',out/'validation/ERC.json',schematic)
run('pcb','drc','--format','json','--severity-all','--all-track-errors','--schematic-parity','-o',out/'validation/DRC.json',board)
drc = json.loads((out/'validation/DRC.json').read_text())
if any(drc.get(k, []) for k in ['violations','unconnected_items','schematic_parity']):
    raise SystemExit('DRC findings remain; no quote package was created.')
erc = json.loads((out/'validation/ERC.json').read_text())
if any(s.get('violations', []) for s in erc.get('sheets', [])):
    raise SystemExit('ERC findings remain; no quote package was created.')
run('pcb','export','gerbers','-o',str(out/'gerbers')+'/', '--layers','F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts','--subtract-soldermask','--use-drill-file-origin',board)
run('pcb','export','drill','-o',str(out/'gerbers')+'/', '--drill-origin','plot','--excellon-separate-th',board)
run('pcb','export','pos','-o',out/'assembly/positions_all.csv','--format','csv','--units','mm','--use-drill-file-origin','--exclude-dnp',board)
run('sch','export','netlist','--format','kicadxml','-o',out/'assembly/netlist.xml',schematic)
selected = json.loads((project/'SELECTED_COMPONENTS.json').read_text())
selection = {x['ref']: x for x in selected['parts']}
ids = {x['mpn']: x['lcsc'] for x in selected['parts']}
rows = []
for c in ET.parse(out/'assembly/netlist.xml').getroot().findall('./components/comp'):
    fields = {x.get('name'): x.get('value','') for x in c.findall('property')}
    if 'exclude_from_bom' in fields:
        continue
    mpn = fields.get('MPN','')
    if not mpn:
        raise SystemExit('Missing MPN: '+c.get('ref'))
    rows.append((c.get('ref'),c.findtext('value'),c.findtext('footprint'),mpn))
if {r[0] for r in rows} != set(selection):
    raise SystemExit('Fitted schematic selection differs from the locked catalog list')
for ref,value,footprint,mpn in rows:
    if mpn != selection[ref]['mpn']:
        raise SystemExit('Exact MPN differs from selected part: '+ref+' '+mpn)
groups = collections.defaultdict(list)
for ref, value, footprint, mpn in rows:
    groups[(mpn, selection[ref]['lcsc'])].append((ref,value,footprint))
with (out/'assembly/JLC_BOM_QUOTE_ONLY.csv').open('w', newline='') as f:
    w = csv.writer(f); w.writerow(['Comment','Designator','Footprint','LCSC Part #','Manufacturer Part Number','Quantity'])
    for (mpn, lcsc), entries in groups.items():
        footprints = {x[2] for x in entries}
        footprint = entries[0][2] if len(footprints)==1 else '0603 compatible lands; see native per-reference geometry'
        w.writerow([entries[0][1],','.join(x[0] for x in entries),footprint,lcsc,mpn,len(entries)])
with (out/'assembly/BOM_exact_per_reference.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['Reference','Value','Footprint','MPN','LCSC'])
    for ref,value,fp,mpn in rows:w.writerow([ref,value,fp,mpn,selection[ref]['lcsc']])
refs = {r[0] for r in rows}
positions = [r for r in csv.DictReader((out/'assembly/positions_all.csv').open()) if r['Ref'] in refs]
if {r['Ref'] for r in positions} != refs:
    raise SystemExit('BOM/CPL reference mismatch')
with (out/'assembly/JLC_CPL_QUOTE_ONLY.csv').open('w', newline='') as f:
    w = csv.writer(f); w.writerow(['Designator','Mid X','Mid Y','Layer','Rotation'])
    for r in positions:
        w.writerow([r['Ref'],r['PosX']+'mm',r['PosY']+'mm',r['Side'],float(r['Rot']) % 360])
archive = out/'DIN_USB_Hub_A8_R5_LCSC_Gerber.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted((out/'gerbers').iterdir()):
        if f.is_file() and f.suffix != '.pdf': z.write(f,f.name)
manifest = {str(f.relative_to(out)): hashlib.sha256(f.read_bytes()).hexdigest() for f in out.rglob('*') if f.is_file() and f.name != 'EXPORT_SHA256.json'}
manifest['SOURCE_BOARD_SHA256'] = hashlib.sha256(board.read_bytes()).hexdigest()
manifest['SOURCE_SCHEMATIC_SHA256'] = hashlib.sha256(schematic.read_bytes()).hexdigest()
(out/'EXPORT_SHA256.json').write_text(json.dumps(manifest, indent=2))
print(f'Exported {len(rows)} PCB parts, {len(groups)} groups. Quote only: review live parts, rotations and CAM before ordering.')
