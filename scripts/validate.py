#!/usr/bin/env python3
"""Fail-closed local checks for evidence integrity, case schema and two-coder workflow.
Cannot establish historical truth or GitHub human identity by itself.
"""
from __future__ import annotations
import argparse, json, pathlib, sys, yaml
from jsonschema import Draft202012Validator
from provenance import ROOT, sha256, canonical, confined, content_matches, normalized
from freeze_source_pack import refs as source_refs, manifest

def load_yaml(p):return yaml.safe_load(p.read_text(encoding='utf-8'))
def schema(name):return json.loads((ROOT/'schemas'/f'{name}.schema.json').read_text())
def check_schema(doc, name, label, errors):
    for e in Draft202012Validator(schema(name)).iter_errors(doc):
        errors.append(f'{label}: schema {list(e.path)} {e.message}')

def check_source_files(source,errors):
    id=source['source_id'];r=source['retrieval']
    if r['status']!='retrieved':return
    for key in ('raw_sha256','extract_sha256'):
        value=r[key]
        if not isinstance(value,str) or len(value)!=64 or any(x not in '0123456789abcdef' for x in value):
            errors.append(f'{id}: invalid {key}');return
    try:
        path=confined(r['extract_path'],'sources/extracts')
        if not path.is_file() or sha256(path.read_bytes())!=r['extract_sha256']:
            errors.append(f'{id}: extract missing or tampered');return
        if r['archival_scope']=='raw_and_extract':
            raw=confined(r['raw_path'],'sources/raw')
            if not raw.is_file() or sha256(raw.read_bytes()) != r['raw_sha256']:
                errors.append(f'{id}: raw snapshot missing or tampered');return
            if not content_matches(raw.read_bytes(),raw.suffix,path.read_text(encoding='utf-8')):
                errors.append(f'{id}: extract not found in raw source');return
        elif r['archival_scope'] != 'extract_only':
            errors.append(f'{id}: retrieved source has no verifiable archival scope')
        if not r['run_id'] or not r['locator'] or not r['retrieved_at']:
            errors.append(f'{id}: incomplete retrieval metadata')
    except (ValueError,TypeError,OSError,UnicodeDecodeError) as e:
        errors.append(f'{id}: source verification failed: {e}')

def check_evidence(ids,grade,byid,origins,label,errors,run_id=None):
    if grade in ('A','B','C') and not ids:
        errors.append(f'{label}: grade {grade} without sources')
    for id in ids:
        src=byid.get(id)
        if not src:
            errors.append(f'{label}: unknown source {id}');continue
        r=src['retrieval']
        if r['status']!='retrieved':errors.append(f'{label}: not_retrieved source {id} cannot support claims/codes/paraphrases')
        if grade in ('A','B') and r['archival_scope']!='raw_and_extract':
            errors.append(f'{label}: grade {grade} requires preserved raw snapshot: {id}')
        if run_id and r['run_id']!=run_id:errors.append(f'{label}: source {id} was not retrieved in research run {run_id}')
    if grade=='A' and not any(byid.get(id,{}).get('source_type') in ('primary','archive') for id in ids):
        errors.append(f'{label}: grade A requires primary/archive source')
    if grade=='B':
        qualifying={byid[id]['origin_id'] for id in ids if id in byid and byid[id]['source_type']=='academic' and byid[id]['origin_id'] in origins}
        if len(qualifying)<2:errors.append(f'{label}: grade B needs 2 distinct human-curated academic origins')

def ind_map(case):
    return {i['id']:i for f in case['freedom_dimensions'] for i in f['indicators']}

def check_review(case,byid,origins,errors):
    id=case['case_id'];label=f'case {id}'
    if case['case_status']!='under_review':return
    second_path=ROOT/'reviews/second'/f'{id}.coding.yaml'
    if not second_path.exists():errors.append(f'{label}: missing second coder file');return
    second=load_yaml(second_path);check_schema(second,'second',str(second_path.relative_to(ROOT)),errors)
    if second.get('case_id')!=id:errors.append(f'{label}: second coding case ID mismatch')
    if second.get('coder_id') in (case['first_coder_id'],None,'UNASSIGNED'):
        errors.append(f'{label}: second coder ID not independent')
    if second.get('source_pack_sha256')!=case['source_pack_sha256']:
        errors.append(f'{label}: second coder used different source pack')
    a=ind_map(case);b={x['id']:x for f in second.get('dimensions',[]) for x in f.get('indicators',[])}
    if set(a)!=set(b):errors.append(f'{label}: second coder indicator set differs')
    diffs={code for code in a.keys() & b.keys() if a[code]['direction']!=b[code]['direction']}
    if diffs:
        rp=ROOT/'reviews/resolutions'/f'{id}.resolution.yaml'
        if not rp.exists():errors.append(f'{label}: unresolved coding differences: {sorted(diffs)}')
        else:
            data=load_yaml(rp);check_schema(data,'resolutions',str(rp.relative_to(ROOT)),errors)
            if data.get('case_id')!=id:errors.append(f'{label}: resolution case ID mismatch')
            given={r['code_id'] for r in data.get('differences',[])}
            if given!=diffs:errors.append(f'{label}: resolution codes must equal actual differences {sorted(diffs)}')
            for record in data.get('differences',[]):
                check_evidence(record.get('supporting_ids',[]),'C',byid,origins,label+' resolution',errors)
    for item in b.values():
        if item['direction'] not in ('unknown','not_applicable'):
            check_evidence(item['evidence_ids'],'C',byid,origins,label+' second '+item['id'],errors)
    direct={p['promise_id']:p for p in case['promises'] if p['assertion_type']=='direct_quote'}
    if direct:
        qp=ROOT/'reviews/quotes'/f'{id}.quotes.yaml'
        if not qp.exists():errors.append(f'{label}: missing independent quote-review file')
        else:
            data=load_yaml(qp);check_schema(data,'quotes',str(qp.relative_to(ROOT)),errors)
            if data.get('case_id')!=id:errors.append(f'{label}: quote review case mismatch')
            if data.get('reviewer_id') in (case['first_coder_id'],second.get('coder_id')):
                errors.append(f'{label}: quote reviewer must be distinct from both coders')
            verified={q['promise_id'] for q in data['quotes'] if q['verdict']=='match'}
            if verified!=set(direct):errors.append(f'{label}: not all direct quotes independently reviewed as matching')

def validate_case(path,case,model,register,origins,errors):
    label=str(path.relative_to(ROOT));check_schema(case,'case',label,errors)
    if not isinstance(case,dict) or not isinstance(case.get('freedom_dimensions'),list):return
    if case.get('model_version')!=model['model_version']:errors.append(f'{label}: old model version')
    if case['period']['start_year']>case['period']['end_year']:errors.append(f'{label}: inverted period')
    expected={d['id']:[i['id'] for i in d['indicators']] for d in model['freedom_definitions']}
    received={d['id']:[i['id'] for i in d['indicators']] for d in case['freedom_dimensions']}
    if len(received)!=len(case['freedom_dimensions']) or expected!=received:
        errors.append(f'{label}: dimensions or nested indicator IDs differ from canonical model')
    byid={s['source_id']:s for s in register['sources']}
    # Every reference, even in a placeholder/paraphrase or blank field, must resolve to retrieved bytes.
    for ref in source_refs(case):
        if ref not in byid:
            errors.append(f'{label}: unknown referenced source {ref}')
        elif byid[ref]['retrieval']['status'] != 'retrieved':
            errors.append(f'{label}: not_retrieved reference {ref} is never evidence')
    run=case['research_run_id']
    for actor in case['actors']:
        if actor['ideology_assessed']:
            check_evidence(actor['evidence_ids'],'C',byid,origins,label+' actor '+actor['actor_id'],errors)
    if case['power_transition']['description']:
        check_evidence(case['power_transition']['evidence_ids'],'C',byid,origins,label+' power_transition',errors)
    for f in case['freedom_dimensions']:
        for i in f['indicators']:
            id=i['id']; direction=i['direction']; status=i['status']
            if status=='not_assessed' and direction!='unknown':errors.append(f'{label}: {id}: not_assessed must be unknown')
            if status=='not_applicable' and direction!='not_applicable':errors.append(f'{label}: {id}: nonapplicable mismatch')
            if status=='assessed' and (not i['rationale'] or not i['baseline'] or not i['followup']):
                errors.append(f'{label}: {id}: assessed needs rationale, baseline and followup')
            decisive=direction in ('strengthened','weakened','mixed','unchanged')
            if decisive and (not i['evidence_ids'] or i['evidence_class'] in ('D','U')):
                errors.append(f'{label}: {id}: decisive direction requires evidence of A/B/C grade')
            if i['evidence_ids'] or i['counterevidence_ids']:
                check_evidence(i['evidence_ids']+i['counterevidence_ids'],i['evidence_class'],byid,origins,label+' '+id,errors)
    for claim in case['claims']:
        if case['case_status']=='under_review' and claim['claim_type']=='fact' and claim['evidence_class'] in ('D','U'):
            errors.append(f'{label}: unsupported factual claim must not enter review: {claim["claim_id"]}')
        check_evidence(claim['source_ids'],claim['evidence_class'],byid,origins,label+' claim '+claim['claim_id'],errors)
    for promise in case['promises']:
        id=promise['source_id']; assert_type=promise['assertion_type']
        check_evidence([id],'C',byid,origins,label+' promise '+promise['promise_id'],errors)
        if assert_type=='direct_quote' and id in byid:
            src=byid[id];r=src['retrieval']
            if r['run_id']!=run:errors.append(f'{label}: quote source not retrieved in same run')
            if r['archival_scope']!='raw_and_extract':errors.append(f'{label}: direct quote requires raw snapshot')
            try:
                extract=confined(r['extract_path'],'sources/extracts').read_text(encoding='utf-8')
                if normalized(promise['wording']) not in normalized(extract):
                    errors.append(f'{label}: exact quote not found in source extract: {promise["promise_id"]}')
                if promise['locator']!=r['locator']:
                    errors.append(f'{label}: quote locator differs from captured source metadata')
            except (ValueError,TypeError,OSError) as e:errors.append(f'{label}: quote missing extract: {e}')
    for assessment in case['promise_assessments']:
        if assessment['assessment']!='unresolved' or assessment['evidence_ids']:
            check_evidence(assessment['evidence_ids'],assessment['evidence_class'],byid,origins,label+' promise assessment '+assessment['promise_id'],errors)
    promiseids={p['promise_id'] for p in case['promises']}
    if len(promiseids)!=len(case['promises']):errors.append(f'{label}: duplicate promise IDs')
    actorids={a['actor_id'] for a in case['actors']}
    if len(actorids)!=len(case['actors']):errors.append(f'{label}: duplicate actor IDs')
    for p in case['promises']:
        if p['actor_id'] not in actorids:errors.append(f'{label}: promise unknown actor')
    for a in case['promise_assessments']:
        if a['promise_id'] not in promiseids:errors.append(f'{label}: assessment missing promise')
    if case['outcomes']['summary']:
        check_evidence(case['outcomes']['evidence_ids'],'C',byid,origins,label+' outcomes',errors)
    try:
        ids=source_refs(case)
        if ids and (case['case_status']=='under_review' or case['source_pack_sha256']):
            p=ROOT/'sources/packs'/f'{case["case_id"]}.json'
            if not p.exists():errors.append(f'{label}: missing source pack manifest')
            else:
                stored=json.loads(p.read_text());expected=manifest(case,register)
                if stored!=expected:errors.append(f'{label}: source pack does not match current references or registry')
                digest=sha256(canonical(expected))
                if case['source_pack_sha256']!=digest:errors.append(f'{label}: source pack hash mismatch')
        if case['case_status']=='under_review':
            if not ids:errors.append(f'{label}: cannot review case without sources')
            if case['source_pack_version']!=model['model_version']:errors.append(f'{label}: source pack version mismatch')
            if any(x['status']=='not_assessed' for f in case['freedom_dimensions'] for x in f['indicators']):
                errors.append(f'{label}: review requires all indicators assessed or marked not_applicable')
    except (ValueError,KeyError,TypeError) as e:errors.append(f'{label}: source pack invalid: {e}')
    check_review(case,byid,origins,errors)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--case')
    args=parser.parse_args();errors=[]
    model=load_yaml(ROOT/'config/model.yaml');register=load_yaml(ROOT/'sources/register.yaml');orig_doc=load_yaml(ROOT/'sources/origins.yaml')
    for doc,name in ((model,'model'),(register,'register'),(orig_doc,'origins')):check_schema(doc,name,name,errors)
    dims=model['freedom_definitions'];ids=[p['id'] for d in dims for p in d['indicators']]
    if set(ids)!={f'M{x:02d}' for x in range(1,11)} or len(ids)!=10:errors.append('model: M01-M10 once each')
    if [d['id'] for d in dims]!=[f'F{x}' for x in range(1,6)]:errors.append('model: F1-F5 in order')
    sources=register['sources'];origins={x['origin_id']:x for x in orig_doc['origins']}
    if len({s['source_id'] for s in sources})!=len(sources):errors.append('register: duplicate source IDs')
    if len(origins)!=len(orig_doc['origins']):errors.append('origins: duplicate IDs')
    for source in sources:
        if source['origin_id'] not in origins:errors.append(f'{source["source_id"]}: unreviewed or unknown origin ID')
        check_source_files(source,errors)
    paths=[(ROOT/args.case).resolve()] if args.case else sorted((ROOT/'cases').glob('*.case.yaml'))
    for p in paths:
        if not p.is_relative_to(ROOT/'cases'):errors.append(f'Invalid case path {p}');continue
        validate_case(p,load_yaml(p),model,register,origins,errors)
    if errors:
        print(f'FAILED: {len(errors)} issue(s)');[print(' - '+e) for e in errors];return 1
    print(f'OK: {len(paths)} case(s); source integrity, references, nesting and required independent reviews passed. No claim of historical truth.')
    return 0
if __name__=='__main__':sys.exit(main())
