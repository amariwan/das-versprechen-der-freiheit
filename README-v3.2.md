# Das Versprechen der Freiheit – Quellenrecherche v3.2 (16.11.2026)

**Neue Arbeit:** überprüfbarer Web-Quellenkatalog, vergleichende Ereignis-Chronologien für Portugal, Iran und Ungarn, arithmetische Datenchecks und offene Prüfaufträge. Vorhandene v3.1-Dossiers, AGENTS.md, Schemata, Skripte, Cases und Tests bleiben erhalten.

## Einstieg

1. `research/VERGLEICH_VERSPRECHEN_WIRKLICHKEIT.md` – die gemeinsame Forschungsfrage.
2. `research/chronologies/` – Portugal / Iran / Ungarn: konkrete Zeitachsen Versprechen → Maßnahme → Effekt.
3. `research/source_audit/SOURCES_WEB_20261116.yaml` – Quellen, Fundstellen, Limits und Status (18 Einträge).
4. `research/source_audit/FAKTENCHECK.md` – Zahlenchecks, Trennung von Bericht und Beweis, offene sprachliche Review-Schritte.
5. Bestehende `research/dossiers/`, `chapters/` und `docs/` – tiefere Vorgeschichte.

## Stand

Die Quellen wurden online recherchiert und inhaltlich überprüft. **Es liegen noch keine rechtskonform bytegenau archivierten Originaldateien vor.** `sources/register.yaml` wird nicht durch fingierte Retrieval-Einträge angereichert. Es wurden keine Freigabehäkchen gesetzt. Kein Case ist `approved`. Daher **kein** wissenschaftlich endgültiger Pilotfall.

## Lokal prüfen

```bash
python scripts/fact_check_research.py
python scripts/validate.py
python scripts/render_codebook.py --check
python -m unittest discover -s tests -v
```

## Reelle nächsten Schritte

Originale mit erlaubten Archivkopien beschaffen, mit `scripts/ingest_source.py` importieren, die spezifischen Claims evidenzbasiert codieren und unkenntlich für den zweiten Coder machen. Erst nach echter Doppelcodierung, Konfliktlösung und Fachreview auf Veröffentlichung gehen.
