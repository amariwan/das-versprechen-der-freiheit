"""Shared deterministic content normalization and provenance helpers."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import re
import json

ROOT = Path(__file__).resolve().parents[1]

class _Text(HTMLParser):
    def __init__(self):
        super().__init__();self.out=[];self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'):self.skip += 1
        if not self.skip and tag in ('p','div','br','tr','li','h1','h2','h3'):self.out.append(' ')
    def handle_endtag(self, tag):
        if tag in ('script','style') and self.skip:self.skip-=1
        if not self.skip and tag in ('p','div','br','tr','li'):self.out.append(' ')
    def handle_data(self, data):
        if not self.skip:self.out.append(data)

def normalized(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()

def extract_text(raw: bytes, extension: str = '.txt') -> str:
    content=raw.decode('utf-8-sig')
    if extension.lower() in ('.html','.htm'):
        parser=_Text();parser.feed(content);return normalized(' '.join(parser.out))
    if extension.lower() not in ('.txt','.md','.csv','.json'):
        raise ValueError('Only text/html, text/plain, md, csv and json supported; no implicit OCR or PDF extraction')
    return normalized(content)

def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

def confined(path: str, parent: str) -> Path:
    resolved=(ROOT / path).resolve()
    if not resolved.is_relative_to((ROOT / parent).resolve()):
        raise ValueError(f'Unsafe path outside {parent}: {path}')
    return resolved

def content_matches(raw: bytes, extension: str, excerpt: str) -> bool:
    return normalized(excerpt) in extract_text(raw,extension)
