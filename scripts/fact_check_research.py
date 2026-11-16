#!/usr/bin/env python3
"""Deterministic arithmetic checks for published figures in research/source_audit/FAKTENCHECK.md.
Does NOT validate factual authenticity, original-source bytes, quotations or human review."""
from decimal import Decimal as D
from pathlib import Path
import sys, yaml
root=Path(__file__).resolve().parents[1]
inv=yaml.safe_load((root/'research/source_audit/SOURCES_WEB_20261116.yaml').read_text(encoding='utf-8'))
assert len(inv['sources']) == 18
assert len({s['id'] for s in inv['sources']}) == 18
assert all(s['verification_status']=='web_read' and s['raw_archived'] is False and s['raw_sha256'] is None and s['independent_quote_review'] is False for s in inv['sources'])
checks=[('Portugal Wahl 1975',5711829,6231372,D('91.66'),D('.01')),('Iran Staatsformreferendum 1979',20440108,20857391,D('98.00'),D('.01')),('Iran Verfassungsreferendum 1979',15690142,20857391,D('75.23'),D('.01')),('Iran Expertenwahl 1979',10784932,20857391,D('51.71'),D('.01')),('Ungarn Wahl 2026',5988778,7527742,D('79.56'),D('.01')),('TISZA Sitzanteil',141,199,D('70.85'),D('.01'))]
for label,num,den,expected,tol in checks:
    v=D(num)/D(den)*100
    if abs(v-expected) > tol:
        print('FAIL',label, v,'not',expected);sys.exit(1)
    print(f'OK  {label}: {v:.4f}% ≈ {expected}%')
print('NOTICE: Figures are arithmetic checks, NOT independent data verification.')
