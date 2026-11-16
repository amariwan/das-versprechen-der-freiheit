# Recherchestand der Pilotwelle

Drei ausführliche, internetrecherchierte Dossiers und ein **unfreigegebener** Probekapiteltext.

**Quellenstatus:** Öffentliche amtliche und wissenschaftliche Quellen wurden über ein Web-Recherchewerkzeug gelesen; unmittelbarer Rohdatenimport in den isolierten Dateicontainer schlug fehl. Daher: echte URLs, konkrete Claim→Quelle-Zuordnung, bekannte Datenkonflikte – aber **keine** archivierten Quellbytes, kein täuschender SHA-256, keine Klasse A und kein `approved`.

- `dossiers/PORTUGAL_1974_1976.md`
- `dossiers/IRAN_1978_1983.md`
- `dossiers/UNGARN_2010_2026.md`
- `PILOT_VERGLEICH.md`
- `../chapters/PORTUGAL_PROBEKAPITEL.md`
- `../cases/` enthält prüfbare, bewusst unbewertete Draft-Stubs (keine bereits vollständig codierten Fälle).

## Nächste echte Schritte

1. Originaldokumente über `scripts/ingest_source.py` lokal abrufen; PDF vorher mit geeignetem PDF-Parser in Originaltext umwandeln, Original-Datei nach Rechteprüfung archivieren.
2. Claims und Versprechen im Case-YAML mit **realen** Register-IDs verknüpfen, Zeitfenster sauber begrenzen und Codierung durchführen.
3. Quellpaket einfrieren, Blindpaket an einen **anderen** Coder senden, maschinell diffen, Abweichungen dokumentieren.
4. Menschliches Sprach-/Quellenreview, Git-PR plus geschützte menschliche Freigabe. Ohne diese Arbeit bleibt alles `draft`.
