"""Adversarial tests: fake approvals, fake sources, fake hashes and invalid quote strings must fail.
All dummy content is TEST DATA and is not historical evidence.
"""
from __future__ import annotations
import copy,hashlib,json,os,shutil,subprocess,sys,tempfile,unittest,yaml
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]

def hashbytes(data):return hashlib.sha256(data).hexdigest()

class GuardrailTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'repo'
        self.root.mkdir()
        for folder in ('scripts','schemas','config','sources','cases','reviews'):
            shutil.copytree(BASE/folder,self.root/folder,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        self.casepath=self.root/'cases/_template.case.yaml'
        self.case=yaml.safe_load(self.casepath.read_text())
        self.case['case_id']='TEST-001';self.case['research_run_id']='RUN-TEST'
        self.case['first_coder_id']='coder_one'
    def tearDown(self):self.tmp.cleanup()
    def save(self):self.casepath.write_text(yaml.safe_dump(self.case,sort_keys=False,allow_unicode=True))
    def runval(self):
        self.save()
        proc=subprocess.run([sys.executable,str(self.root/'scripts/validate.py')],text=True,capture_output=True,cwd=self.root)
        return proc.returncode,proc.stdout+proc.stderr
    def add_source(self,source_type='primary',retrieved=True,raw=True,tamper=False):
        text='TEST DOCUMENT: the assembled committee adopted a change. Nothing here is historical.\n'
        rawbytes=text.encode();extract=rawbytes
        r={'status':'retrieved' if retrieved else 'not_retrieved',
           'run_id':'RUN-TEST' if retrieved else None,'retrieved_at':'2026-11-16T00:00:00Z' if retrieved else None,
           'locator':'Section TEST' if retrieved else None,
           'raw_sha256':hashbytes(rawbytes) if retrieved else None,
           'extract_sha256':hashbytes(extract) if retrieved else None,
           'raw_path':'sources/raw/SRC-TEST.txt' if retrieved and raw else None,
           'extract_path':'sources/extracts/SRC-TEST.txt' if retrieved else None,
           'archival_scope':'raw_and_extract' if retrieved and raw else 'extract_only' if retrieved else 'none',
           'method':'file' if retrieved else 'none'}
        if retrieved:
            (self.root/'sources/extracts/SRC-TEST.txt').write_bytes(b'MODIFIED\n' if tamper else extract)
            if raw:(self.root/'sources/raw/SRC-TEST.txt').write_bytes(rawbytes)
        reg=yaml.safe_load((self.root/'sources/register.yaml').read_text())
        reg['sources']=[{'source_id':'SRC-TEST','title':'TEST DATA (NOT REAL)','source_type':source_type,
                         'origin_id':'ORG-TEST','retrieval':r}]
        (self.root/'sources/register.yaml').write_text(yaml.safe_dump(reg))
        (self.root/'sources/origins.yaml').write_text(yaml.safe_dump({'origins':[{'origin_id':'ORG-TEST','publisher_or_archive':'TEST','independence_notes':'TEST ONLY'}]}))
    def claim(self,grade='A'):
        self.case['claims']=[{'claim_id':'CLAIM-1','text':'Sample claim','claim_type':'fact',
             'evidence_class':grade,'source_ids':['SRC-TEST'],'temporal_scope':'TEST'}]
    def test_baseline_draft_is_valid(self):
        rc,out=self.runval();self.assertEqual(rc,0,out)
    def test_cannot_self_declare_approved_even_with_fake_human_flags(self):
        self.case['case_status']='approved';self.case['reviews']={'human_final_approved':True,'fake_hash':'x'}
        rc,out=self.runval();self.assertNotEqual(rc,0);self.assertIn('schema',out)
    def test_unretrieved_source_cannot_back_claim_A(self):
        self.add_source(retrieved=False);self.claim()
        rc,out=self.runval();self.assertNotEqual(rc,0);self.assertIn('not_retrieved',out)
    def test_tampered_extract_is_detected(self):
        self.add_source(tamper=True);self.claim()
        rc,out=self.runval();self.assertNotEqual(rc,0);self.assertIn('tampered',out)
    def test_fake_raw_hash_is_detected(self):
        self.add_source();self.claim()
        regp=self.root/'sources/register.yaml';reg=yaml.safe_load(regp.read_text())
        reg['sources'][0]['retrieval']['raw_sha256']='0'*64
        regp.write_text(yaml.safe_dump(reg))
        rc,out=self.runval();self.assertNotEqual(rc,0);self.assertIn('raw snapshot missing or tampered',out)
    def test_fake_quote_string_is_detected(self):
        self.add_source()
        self.case['actors']=[{'actor_id':'ACT-1','name':'TEST','ideology_assessed':'','evidence_ids':[]}]
        self.case['promises']=[{'promise_id':'P-1','actor_id':'ACT-1','date':'2026-11-16','assertion_type':'direct_quote',
            'wording':'Something that never appeared in the document','original_language':'en',
            'source_id':'SRC-TEST','locator':'Section TEST'}]
        rc,out=self.runval();self.assertNotEqual(rc,0);self.assertIn('exact quote not found',out)
    def test_A_requires_primary_or_archive(self):
        self.add_source(source_type='news');self.claim('A')
        rc,out=self.runval();self.assertNotEqual(rc,0);self.assertIn('primary/archive',out)
    def test_early_approval_cannot_bypass_second_review(self):
        self.add_source();self.claim()
        self.case['case_status']='under_review'
        rc,out=self.runval();self.assertNotEqual(rc,0);self.assertIn('missing second coder',out)
    def test_canonical_ingestion_produces_verified_hashes(self):
        self.save()
        sample=self.root/'test_source.txt';sample.write_text('A verifiable test phrase belongs to test data only.',encoding='utf-8')
        cmd=[sys.executable,str(self.root/'scripts/ingest_source.py'),'--source-id','SRC-TEST',
             '--title','Demo source','--source-type','primary','--origin-id','ORG-TEST',
             '--file',str(sample),'--needle','verifiable test phrase','--locator','Section TEST',
             '--run-id','RUN-TEST','--archive-raw','--rights-confirmed']
        p=subprocess.run(cmd,text=True,capture_output=True,cwd=self.root)
        self.assertEqual(p.returncode,0,p.stderr)
        (self.root/'sources/origins.yaml').write_text(yaml.safe_dump({'origins':[{'origin_id':'ORG-TEST','publisher_or_archive':'TEST','independence_notes':'TEST ONLY'}]}))
        self.claim()
        rc,out=self.runval();self.assertEqual(rc,0,out)
    def test_frozen_pack_and_independent_second_coding_pass(self):
        self.casepath=self.root/'cases/TEST-001.case.yaml'
        self.add_source();self.claim('A')
        for d in self.case['freedom_dimensions']:
            for x in d['indicators']:
                x.update(status='assessed',direction='unknown',baseline='unknown starting conditions',
                         followup='unknown later conditions',rationale='No corroborated direction',
                         evidence_class='U')
        self.save()
        freeze=subprocess.run([sys.executable,str(self.root/'scripts/freeze_source_pack.py'),
                 '--case','cases/TEST-001.case.yaml'],capture_output=True,text=True,cwd=self.root)
        self.assertEqual(freeze.returncode,0,freeze.stderr)
        self.case=yaml.safe_load(self.casepath.read_text())
        blind=subprocess.run([sys.executable,str(self.root/'scripts/make_blind_packet.py'),
                 'TEST-001'],capture_output=True,text=True,cwd=self.root)
        self.assertEqual(blind.returncode,0,blind.stderr)
        with __import__('zipfile').ZipFile(self.root/'reviews/TEST-001.blind.zip') as archive:
            packet=json.loads(archive.read('instructions.json'))
            self.assertNotIn('outcomes',packet)
            self.assertNotIn('first_coder_id',packet)
        second={'case_id':'TEST-001','coder_id':'coder_two',
            'source_pack_sha256':self.case['source_pack_sha256'],
            'dimensions':[{'id':d['id'],'indicators':[{'id':x['id'],'direction':'unknown',
               'rationale':'No source supports a directional change', 'evidence_ids':[]} for x in d['indicators']]}
                for d in self.case['freedom_dimensions']]}
        (self.root/'reviews/second/TEST-001.coding.yaml').write_text(yaml.safe_dump(second))
        self.case['case_status']='under_review'
        rc,out=self.runval();self.assertEqual(rc,0,out)
        self.case['source_pack_sha256']='0'*64
        rc,out=self.runval();self.assertNotEqual(rc,0);self.assertIn('source pack hash mismatch',out)
    def test_fake_independence_group_cannot_make_B(self):
        self.add_source(source_type='academic');self.claim('B')
        rc,out=self.runval();self.assertNotEqual(rc,0);self.assertIn('2 distinct human-curated academic origins',out)

if __name__=='__main__':unittest.main()
