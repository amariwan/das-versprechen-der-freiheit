# Das Versprechen der Freiheit – Pilottest v3.1 (16.11.2026)

**Bewahrt v3 unverändert als technischen Kern und ergänzt quellenorientierte Pilotdossiers, Buchfrage, Fallauswahlverfahren und ein Probekapitel.** Kein vorgetäuschter Vollzug von Primärarchivierung oder unabhängiger Zweitcodierung.

## Sofort lesen

1. [Forschungsdesign](docs/FORSCHUNGSDESIGN_v3_1.md)
2. [Pilotvergleich](research/PILOT_VERGLEICH.md)
3. [Portugal-Dossier](research/dossiers/PORTUGAL_1974_1976.md)
4. [Iran-Dossier](research/dossiers/IRAN_1978_1983.md)
5. [Ungarn-Dossier](research/dossiers/UNGARN_2010_2026.md)
6. [Portugal-Probekapitel](chapters/PORTUGAL_PROBEKAPITEL.md)

### Was wirklich erledigt ist

- Internetbasierte Erstquellenrecherche mit konkreten überprüfbaren Links.
- Drei inhaltliche Dossiers mit Baseline, Chronologie, Zahlen und offenen Gegenhypothesen.
- Drei valide `draft`-Stubs für Cases, absichtlich **ohne** bewertete F-Codes oder vorgetäuschte archivierte Quellen.
- Ein kapitelartiger erster Erzählversuch inklusive Quellenanker.
- Klare Methode für die Buchauswahl und Trennung von Erzählung und Forschungsapparat.

### Was explizit noch aussteht

- Bytegenauer legaler Rohquellenimport, Extract- und Hash-Registrierung.
- Erstcodierung auf Grundlage tatsächlich lokal verifizierter Dokumente.
- Unabhängige, blinde Zweitcodierung und dokumentierte Konfliktklärung.
- Menschlicher sprachkundiger Quellenreview und GitHub-Review-/Release-Gate.
- Erst danach Publikationsfreigabe einzelner Cases oder Kapitel.

### Prüfen

```bash
pip install -r requirements.txt
python scripts/validate.py
python scripts/render_codebook.py --check
python -m unittest discover -s tests -v
```
