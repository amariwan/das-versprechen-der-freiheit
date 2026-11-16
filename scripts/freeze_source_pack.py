#!/usr/bin/env python3
"""Freeze all actually referenced source snapshots in a canonical manifest."""
from __future__ import annotations
import argparse, pathlib, sys, yaml, json
from provenance import ROOT, canonical, sha256

def refs(case):
    ids=set()
    for actor in case['actors']:ids.update(actor['evidence_ids'])
    ids.update(case['power_transition']['evidence_ids'])
    for p in case['promises']:ids.add(p['source_id'])
    for p in case['promise_assessments']:ids.update(p['evidence_ids'])
    for c in case['claims']:ids.update(c['source_ids'])
    for d in case['freedom_dimensions']:
        for x in d['indicators']:
            ids.update(x['evidence_ids']);ids.update(x['counterevidence_ids'])
    ids.update(case['outcomes']['evidence_ids'])
    return sorted(ids)

def manifest(case,register):
    byid={s['source_id']:s for s in register['sources']}
    items=[]
    for id in refs(case):
        if id not in byid:raise ValueError(f'Unknown source {id}')
        r=byid[id]['retrieval']
        if r['status']!='retrieved':raise ValueError(f'Unretrieved source {id}')
        items.append({'source_id':id, 'origin_id':byid[id]['origin_id'], 'source_type':byid[id]['source_type'],
           'run_id':r['run_id'],'raw_sha256':r['raw_sha256'],'extract_sha256':r['extract_sha256'],
           'locator':r['locator'], 'extract_path':r['extract_path'], 'raw_path':r['raw_path']})
    return {'case_id':case['case_id'],'version':case['model_version'],'items':items}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--case',required=True)
    args=parser.parse_args();path=(ROOT/args.case).resolve()
    if not path.is_relative_to((ROOT/'cases').resolve()):parser.error('Case must be within cases/')
    case=yaml.safe_load(path.read_text());reg=yaml.safe_load((ROOT/'sources/register.yaml').read_text())
    data=manifest(case,reg)
    if not data['items']:parser.error('Cannot freeze empty source pack')
    digest=sha256(canonical(data))
    name=ROOT/'sources/packs'/f"{case['case_id']}.json"
    name.parent.mkdir(parents=True, exist_ok=True)
    name.write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    case['source_pack_version']=case['model_version'];case['source_pack_sha256']=digest
    path.write_text(yaml.safe_dump(case,allow_unicode=True,sort_keys=False,width=100))
    print(f'Frozen: {name.relative_to(ROOT)} SHA256={digest}')
if __name__=='__main__':sys.exit(main())
