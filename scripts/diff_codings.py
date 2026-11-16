#!/usr/bin/env python3
import argparse,yaml
from pathlib import Path
from provenance import ROOT
p=argparse.ArgumentParser();p.add_argument('case_id');args=p.parse_args()
case=yaml.safe_load((ROOT/'cases'/f'{args.case_id}.case.yaml').read_text())
second=yaml.safe_load((ROOT/'reviews/second'/f'{args.case_id}.coding.yaml').read_text())
a={i['id']:i['direction'] for d in case['freedom_dimensions'] for i in d['indicators']}
b={i['id']:i['direction'] for d in second['dimensions'] for i in d['indicators']}
for id in sorted(set(a)|set(b)):
    if a.get(id)!=b.get(id):print(f'{id}: first={a.get(id)} second={b.get(id)}')
if a==b:print('No disagreements')
