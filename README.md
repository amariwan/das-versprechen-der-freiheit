> **Aktuelle Forschungsrunde:** Siehe [README v3.2](README-v3.2.md). Die Webquellen und Chronologien sind Vorrecherche, **keine** geprüften Primärarchive.

# Das Versprechen der Freiheit — Forschungsmodell v3.0

**Historischer Untersuchungszeitraum: 1789–2026.** Quellengebundenes, ergebnisoffenes Sachbuchprojekt. **Dieses Paket enthält keine historischen Tatsachenbehauptungen, die bereits als geprüft gelten.**

## Was sich gegenüber v2 geändert hat

1. Kein freies `approved` in Fall-YAML. Freigabe ist eine separate GitHub-Attestation hinter geschütztem Review.
2. Bytebasierte Quellenaufnahme, extrahierte Passagen, gespeicherte SHA-256-Hashes und Abgleich mit archivierten Rohbytes.
3. Jede referenzierte Quelle muss abgerufen worden sein. A verlangt `primary/archive` und Raw Snapshot; B zwei unabhängige **menschlich kuratierte** akademische Herkunftsgruppen.
4. Unabhängige Zweitcodierung als Datei, automatischer Vergleich und dokumentierte Auflösung abweichender Codes.
5. Zehn M-Codes als Unterindikatoren von F1–F5, keine doppelte F-Richtung. Keine voreingenommenen Anker im Codebook.
6. Negativtests, CI, CODEOWNERS-Vorlage, `chapters/`, scriptgenerierter Quellenpaket-Hash.

## Verzeichnisübersicht

- `AGENTS.md`: kompakte bindende Agent-Anweisungen.
- `config/model.yaml`: zentrale Definitionen; `docs/CODEBOOK.md` ist generiert.
- `cases/_template.case.yaml`: Forschungsfall, `case_status: draft|under_review`.
- `sources/register.yaml`: bibliografisch verknüpfte Quellen mit Abruf-Metadaten.
- `sources/origins.yaml`: menschlich kuratierte Herkunftsgruppen (B-Indikator).
- `sources/raw/`, `sources/extracts/`, `sources/packs/`: archivierte Rohquellen (nur mit Rechten), Kurzbelege, gefrorene Quellenpakete.
- `reviews/second/`, `reviews/quotes/`, `reviews/resolutions/`: unabhängiger Zweitdurchlauf und Konfliktklärung.
- `.github/workflows/`, `.github/CODEOWNERS`: CI und menschliche Freigaben (GitHub-Einstellungen erforderlich).
- `docs/`: Methode, Redaktionsregeln, Fallauswahl, Begriffsklärung.
- `chapters/`: spätere, frei gestaltete Manuskripttexte.

## Installation und Tests

```bash
python -m pip install -r requirements.txt
python scripts/render_codebook.py --check
python scripts/validate.py
python -m unittest discover -s tests -v
```

## Durchgehender Forschungsablauf

1. Fall aus `cases/_template.case.yaml` kopieren; neue `case_id`, Forschungsfrage und Baseline definieren.
2. Herkunft einer wissenschaftlichen Quelle unter `sources/origins.yaml` **menschlich kuratieren**, ohne erwartete Kodierung.
3. Quelle abrufen, Treffer wortgleich aus Originaltext extrahieren und Hashes errechnen:

```bash
python scripts/ingest_source.py \
  --source-id SRC-001 --title 'Dokumenttitel' --source-type primary \
  --origin-id ORG-001 --file /path/to/licensed-text.txt \
  --needle 'tatsächlich im Text vorhandene Passage' \
  --locator 'S. 12, Absatz 3' --run-id RUN-001 \
  --archive-raw --rights-confirmed
```

**Nur** `--archive-raw --rights-confirmed`, wenn rechtmäßige Rohspeicherung vorliegt. `--url https://...` ist alternativ möglich. Akzeptiert aktuell Text/HTML, nicht PDF/OCR. Ohne archiviertes Raw nur vorläufige Evidenzklasse C, kein Direktzitat.

4. `cases/CASE-ID.case.yaml` mit echten Belegen füllen. Keine `not_retrieved`-Quellen referenzieren.
5. `python scripts/freeze_source_pack.py --case cases/CASE-ID.case.yaml` erstellt ein kanonisches Manifest und setzt den echten Paket-Hash. Danach `python scripts/make_blind_packet.py CASE-ID` und an **anderen** Coder geben, ohne Zugriff auf Erstcodierung und Pilot-Ergebnishypothesen.
6. Zweitcodierung nach `reviews/second/CASE-ID.coding.yaml`; Differenzen mit `python scripts/diff_codings.py CASE-ID` prüfen. Konflikte in `reviews/resolutions/CASE-ID.resolution.yaml` belegen. Direktzitate zusätzlich in `reviews/quotes/CASE-ID.quotes.yaml` prüfen.
7. `case_status: under_review`; sämtliche Validatoren und PR-Checks ausführen. Erst nach **GitHub Environment-Review** `workflow_dispatch` mit `case_id` zur Freigabe starten. Resultat ist eine Release-Attestation als Actions-Artefakt, nicht ein selbst eintragbares Flag.

## GitHub-Konfiguration: Pflicht, nicht im ZIP erzwingbar

- Repository mit Git initialisieren und pushen; `main` durch Ruleset/Branch Protection schützen.
- PR verpflichtend, Required CI-Check `validate`, mindestens ein **menschlicher** CODEOWNER-Review, eigene Reviews nicht zählen, keine Bypass-Administratoren; Änderungen an Workflows/Validatoren besonders prüfen.
- `@amariwan` in `.github/CODEOWNERS` an tatsächliche Verantwortliche anpassen; **zusätzliche unabhängige historische Fachprüfung** festlegen.
- Environment `historical-release` mit **Required Reviewers** und nur `main` als Deployment Branch einrichten. Dort `HUMAN_REVIEW_ENV_SECRET` setzen, **nicht** auf Repository-Ebene.
- Ohne diese externen GitHub-Einstellungen ist Release-Gating **nicht sicher aktiv**. Lokale Dateien/Häkchen können niemals die reale Identität eines Prüfers beweisen.

## Grenzen

Die Tests prüfen Verweise, Hashes, Wortlaut und Prozesskonsistenz. Ein Akteur mit Schreibrechten auf **alle** Rohdateien, Register und Workflows kann ein komplettes falsches Quellenpaket erzeugen. Schutz dagegen kommt **nur** durch unabhängige fachliche Quellenprüfung und geschützte GitHub-Reviews. Keine kryptografische Prüfung kann die historische Wahrheit einer manipulierten Primärquelle garantieren.
