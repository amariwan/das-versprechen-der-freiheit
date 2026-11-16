#!/usr/bin/env python3
"""Create verifiable retrieval metadata by obtaining source content and extracting text programmatically.

Example: python scripts/ingest_source.py --source-id SRC-001 --title 'Public domain decree' \
 --source-type primary --origin-id ORG-001 --file evidence.txt --needle 'some exact passage' \
 --locator 'paragraph 7' --run-id RUN-001 --archive-raw --rights-confirmed

No manual --hash or --excerpt flags: hashes and excerpts are computed from retrieved bytes.
"""
from __future__ import annotations
import argparse, datetime, pathlib, re, sys, urllib.request, urllib.parse, yaml
from provenance import ROOT, sha256, normalized, extract_text

p=argparse.ArgumentParser()
p.add_argument('--source-id',required=True);p.add_argument('--title',required=True)
p.add_argument('--source-type',choices=['primary','archive','academic','dataset','news','other'],required=True)
p.add_argument('--origin-id',required=True)
p.add_argument('--file',type=pathlib.Path);p.add_argument('--url')
p.add_argument('--needle',required=True,help='Exact segment in retrieved source, not a free-form extract')
p.add_argument('--locator',required=True);p.add_argument('--run-id',required=True)
p.add_argument('--context-chars',type=int,default=160)
p.add_argument('--archive-raw',action='store_true');p.add_argument('--rights-confirmed',action='store_true')
args=p.parse_args()
if not re.fullmatch(r'[A-Z][A-Z0-9-]+',args.source_id):p.error('Bad source ID')
if bool(args.file) == bool(args.url):p.error('Supply exactly one of --file or --url')
if args.archive_raw and not args.rights_confirmed:p.error('Archiving full original requires --rights-confirmed')
if args.context_chars < 0 or args.context_chars > 1000:p.error('--context-chars must be 0..1000')
try:
    if args.url:
        u=urllib.parse.urlparse(args.url)
        if u.scheme != 'https' or not u.hostname:p.error('Only HTTPS source URLs are accepted')
        with urllib.request.urlopen(urllib.request.Request(args.url, headers={'User-Agent':'ResearchProvenance/3.0'}),timeout=20) as response:
            if urllib.parse.urlparse(response.url).scheme != 'https':raise ValueError('Redirected off HTTPS')
            raw=response.read(2_000_001)
            if len(raw)>2_000_000:raise ValueError('Source too large; ingest a licensed local text copy')
            mime=response.headers.get_content_type()
            ext='.html' if mime=='text/html' else '.txt'
    else:
        raw=args.file.read_bytes()
        if len(raw)>2_000_000:raise ValueError('Source too large; preprocess into a licensed text excerpt')
        ext=args.file.suffix.lower()
    full=extract_text(raw,ext)
    needle=normalized(args.needle)
    pos=full.find(needle)
    if not needle or pos<0:raise ValueError('Needle not found verbatim in retrieved text after whitespace normalization')
    start=max(0,pos-args.context_chars);end=min(len(full),pos+len(needle)+args.context_chars)
    excerpt=full[start:end];extract_bytes=(excerpt+'\n').encode('utf-8')
    regpath=ROOT/'sources/register.yaml'
    reg=yaml.safe_load(regpath.read_text())
    if any(x['source_id']==args.source_id for x in reg['sources']):raise ValueError('Source ID already exists; immutable IDs, create new ID for a fresh snapshot')
    extract_path=f'sources/extracts/{args.source_id}.txt'
    (ROOT/extract_path).write_bytes(extract_bytes)
    raw_path=None
    if args.archive_raw:
        raw_path=f'sources/raw/{args.source_id}{ext}'
        (ROOT/raw_path).write_bytes(raw)
    reg['sources'].append({
        'source_id':args.source_id,'title':args.title,'source_type':args.source_type,'origin_id':args.origin_id,
        'url':args.url or '', 'archive_id':'','license_notes':'full local snapshot only when rights confirmed' if args.archive_raw else 'excerpt-only; cannot prove raw checksum offline',
        'retrieval':{'status':'retrieved','run_id':args.run_id,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'locator':args.locator, 'raw_sha256':sha256(raw),'extract_sha256':sha256(extract_bytes),
         'raw_path':raw_path,'extract_path':extract_path,
         'archival_scope':'raw_and_extract' if args.archive_raw else 'extract_only',
         'method':'https' if args.url else 'file'}
    })
    reg['sources'].sort(key=lambda x:x['source_id'])
    reg['updated_at']=datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    regpath.write_text(yaml.safe_dump(reg,allow_unicode=True,sort_keys=False,width=96))
    print(f'INGESTED {args.source_id}: {extract_path}, snapshot={"yes" if raw_path else "no"}; hash derived from bytes')
except (ValueError,UnicodeDecodeError,OSError) as err:
    print(f'FAILED: {err}',file=sys.stderr);sys.exit(1)
