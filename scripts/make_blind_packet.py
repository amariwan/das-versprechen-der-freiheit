#!/usr/bin/env python3
"""Prepare coding input that excludes first-coder decisions, results, and examples."""
import argparse,json,yaml,zipfile
from provenance import ROOT
p=argparse.ArgumentParser();p.add_argument('case_id');p.add_argument('--output');args=p.parse_args()
case=yaml.safe_load((ROOT/'cases'/f'{args.case_id}.case.yaml').read_text())
manifest=json.loads((ROOT/'sources/packs'/f'{args.case_id}.json').read_text())
model=yaml.safe_load((ROOT/'config/model.yaml').read_text())
out=ROOT/(args.output or f'reviews/{args.case_id}.blind.zip')
packet={'case_id':case['case_id'],'territory':case['territory'],'period':case['period'],
    'research_question':case['research_question'],'baseline':case['context']['baseline_description'],
    'pack_sha256':case['source_pack_sha256'],
    'indicator_rules':[{ 'id':ind['id'],'question':ind['decision_rule']} for f in model['freedom_definitions'] for ind in f['indicators']]}
with zipfile.ZipFile(out,'w') as z:
    z.writestr('instructions.json',json.dumps(packet,ensure_ascii=False,indent=2))
    z.writestr('manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))
    for item in manifest['items']:
        path=ROOT/item['extract_path'];z.write(path,f'extracts/{path.name}')
print(f'Blind bundle: {out} (source texts, case question, no first coding or outcome hypotheses)')
