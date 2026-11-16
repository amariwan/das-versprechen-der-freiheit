#!/usr/bin/env python3
"""Render the only public codebook from canonical model YAML; no expected outcomes."""
import argparse,sys,yaml
from provenance import ROOT

def render(model):
    lines=['# Codebook – das Versprechen der Freiheit','',f'Generiert aus `config/model.yaml`, Modell `{model["model_version"]}`. **Nicht von Hand editieren.**','','## Richtungen','']
    for key,value in model['direction_rule'].items():lines.append(f'- `{key}`: {value}')
    lines.extend(['','## F-Dimensionen mit jeweils eigenen M-Indikatoren','', 'F ist **keine zusätzliche Codierung**. Nur M-Indikatoren bekommen eine Richtung; kein aggregierter Freiheits-Score.',''])
    for f in model['freedom_definitions']:
        lines.extend([f'### {f["id"]} – {f["label"]}','',f'**Geltungsbereich:** {f["observable_indicators"]}',f'**Grenze:** {f["boundary_rule"]}',''])
        for m in f['indicators']:
            lines.extend([f'#### {m["id"]} – {m["label"]}','',f'**Entscheidungsregel:** {m["decision_rule"]}',f'**Indikatoren:** {m["observable_indicators"]}',f'**Abgrenzung:** {m["boundary_rule"]}',''])
    lines.extend(['## Einheitliche Prüfregeln','','- Vorher/Nachher, Zeitraum, betroffene Gruppen und alternative Deutungen benennen.','- `unknown` bei Evidenzlücken; `unchanged` nur mit positivem Nachweis.','- Primärquelle für Wortlaut beweist nicht automatisch die Wirksamkeit einer Maßnahme.','- Keine historischen Pilotfälle oder erwarteten Ergebnisse im Codierkontext.','- Machtweg und Versprechenerfüllung sind eigenständige Variablen, keine Indikatoren.',''])
    return '\n'.join(lines)

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    model=yaml.safe_load((ROOT/'config/model.yaml').read_text());path=ROOT/'docs/CODEBOOK.md';out=render(model)
    if args.check:
        if path.read_text()!=out:print('FAILED: codebook differs from YAML');return 1
        print('OK: Codebook is generated from YAML');return 0
    path.write_text(out);print('Codebook generated');return 0
if __name__=='__main__':sys.exit(main())
