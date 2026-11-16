#!/usr/bin/env python3
"""Report evidential readiness distinctly from structural validation. No self approval."""
import argparse
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--require-review-ready', action='store_true', help='Fail if any pilot is below independent-review readiness.')
    ns = ap.parse_args()
    registry = yaml.safe_load((ROOT/'sources/register.yaml').read_text(encoding='utf-8'))
    sources = {s['source_id']:s for s in registry['sources']}
    all_ready = True
    print('Historische Evidenzreife (NICHT bloß YAML-Validität):')
    for file in sorted((ROOT/'cases').glob('*.case.yaml')):
        if file.name.startswith('_'): continue
        case = yaml.safe_load(file.read_text(encoding='utf-8'))
        found = len([r for r in sources.values() if r['retrieval']['status']=='retrieved'])
        coded=sum(i['status']=='assessed' for f in case['freedom_dimensions'] for i in f['indicators'])
        total=sum(len(f['indicators']) for f in case['freedom_dimensions'])
        review=(ROOT/'reviews/second'/f'{case["case_id"]}.coding.yaml').exists()
        frozen=bool(case['source_pack_sha256']) and (ROOT/'sources/packs'/f'{case["case_id"]}.json').exists()
        claims=len(case['claims']); promises=len(case['promises'])
        ready=(case['case_status']=='under_review' and found and coded == total and review and frozen and claims)
        all_ready &= bool(ready)
        print(f'- {case["case_id"]}: {case["case_status"]} | lokal importierte Quellen gesamt={found}, Claims={claims}, Versprechen={promises}, M bewertet={coded}/{total}, Pack={"ja" if frozen else "nein"}, Blindreview={"ja" if review else "nein"} | {"REVIEW-CANDIDATE" if ready else "NICHT FREIGABEREIF"}')
    if ns.require_review_ready and not all_ready: raise SystemExit(2)

if __name__=='__main__':main()
