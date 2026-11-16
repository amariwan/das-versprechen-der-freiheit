#!/usr/bin/env python3
"""Produce approval attestations only from a human-gated GitHub Environment job.
Approval is NOT encoded in editable case YAML. GitHub repo protections are a deployment prerequisite.
"""
import json,os,subprocess,sys,datetime,yaml
from pathlib import Path
from provenance import ROOT,canonical,sha256
from validate import main as validate_main
if len(sys.argv)!=2:sys.exit('Usage: python scripts/release.py CASE-ID')
id=sys.argv[1]
allowed={'GITHUB_ACTIONS':'true','GITHUB_REF':'refs/heads/main','GITHUB_EVENT_NAME':'workflow_dispatch'}
for key,value in allowed.items():
    if os.getenv(key)!=value:sys.exit(f'FAILED: {key} must be {value}')
if not os.environ.get('HUMAN_REVIEW_ENV_SECRET'):
    sys.exit('FAILED: protected historical-release environment secret absent')
case_path=ROOT/'cases'/f'{id}.case.yaml'
if not case_path.is_file():sys.exit('FAILED: no such case')
case=yaml.safe_load(case_path.read_text())
if case['case_status']!='under_review':sys.exit('FAILED: must complete review')
# Validator checks entire repository including reviews and byte-level evidence snapshots.
sys.argv=['validate.py','--case',str(case_path)]
if validate_main()!=0:sys.exit('FAILED: case did not pass verification')
sha=os.environ.get('GITHUB_SHA')
if not sha or len(sha)!=40 or any(c not in '0123456789abcdef' for c in sha):sys.exit('FAILED: missing Git commit SHA')
manifest={'case_id':id,'source_pack_sha256':case['source_pack_sha256'],'model_version':case['model_version'],
    'commit_sha':sha,'reviewed_by_github_actor':os.getenv('GITHUB_ACTOR'),
    'approved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'gate':'GitHub Environment historical-release required reviewers; CODEOWNERS and protected main must be enabled'}
(ROOT/'releases').mkdir(exist_ok=True)
path=ROOT/'releases'/f'{id}.approved.json';path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(f'RELEASE ATTESTATION: {path}; note GitHub settings must actually enforce reviewers')
