# AGENTS.md — Das Versprechen der Freiheit (1789–2026)

**Auftrag:** Historisches Sachbuch über dokumentierte Freiheitsversprechen, tatsächliche institutionelle Änderungen und gegenläufige Entwicklungen. **Keine Niedergangsthese voraussetzen.**

## Verbindliche Regeln

1. **Nur tatsächliche Quellen.** Referenzen auf `not_retrieved` sind nie Evidenz, auch nicht bei Paraphrasen, Codes oder Interpretationen. Kein Agent darf Hashes oder Extracts aus freiem Text erfinden: `scripts/ingest_source.py` erzeugt sie aus gelesenen Bytes.
2. **Keine fingierten Zitate.** Direktzitat muss wortgleich im tatsächlich archivierten Rohtext **und** Kurzextract vorkommen; Retrieval-`run_id` entspricht Fall-`research_run_id`. Originalsprache, Übersetzung und Seiten-/Archivfundstelle benötigen eigenständige menschliche Prüfung.
3. **Evidenzklassen:** A nur Primär-/Archivquelle mit archiviertem Rohtext; B zwei nach unabhängigem menschlichem Herkunftscheck getrennte wissenschaftliche Ursprünge; C mindestens eine abgerufene Quelle, vorläufig; D Hypothese; U ungeklärt. Keine Sicherheit aus einer bloßen Quellen-ID ableiten.
4. **Single Source of Truth:** `config/model.yaml`; `docs/CODEBOOK.md` automatisch generieren. Zehn M-Unterindikatoren gehören zu F1–F5 und werden **nicht doppelt** als F-Scores codiert. `unknown` bei Evidenzlücken, `unchanged` nur mit Belegen.
5. **Keine ergebnisgelenkte Fallauswahl.** Positive, negative, gemischte und ungeklärte Fälle erfassen. Die Blindcodierer erhalten keine Pilot-Ergebnishypothesen, Erstcodierungen oder erwartete Richtungen.
6. **Fakten, Ursache, Interpretation trennen.** Zahl immer mit Grundgesamtheit, Zeitraum, Definition und Datensatz-Release; Kausalität nur mit Gegenhypothesen. Keine erfundenen historischen Dialoge.
7. **Keine Self-Approval.** Im Fall-YAML existiert kein `approved`. Zweitcodierung liegt separat unter `reviews/second/`, Zitatreview unter `reviews/quotes/`, Differenzen unter `reviews/resolutions/`. Publikationsfreigabe nur per `workflow_dispatch` auf geschütztem `main` und GitHub Environment `historical-release` mit menschlichen Required Reviewers.

## Workflow

`Fall abgrenzen → Quellen abrufen (`scripts/ingest_source.py`) → Provenienz prüfen → Erstcodierung (`cases/*.case.yaml`) → Quellenpaket einfrieren (`scripts/freeze_source_pack.py`) → Blindpaket erzeugen (`scripts/make_blind_packet.py`) → unabhängige Zweitcodierung → Differenzen klären → Zitate fachlich prüfen → menschlicher GitHub-Review → Release-Attestation → Kapitel schreiben.`

**Checks:** `python scripts/validate.py && python scripts/render_codebook.py --check && python -m unittest discover -s tests -v`.

## Dateien / Done

- `config/`, `schemas/`: normatives Modell und technische Datenformate.
- `cases/`: Forschungsfälle, kein Freigabe-Bool; `sources/register.yaml`, `sources/origins.yaml`, `sources/{raw,extracts,packs}/`: Provenienz.
- `reviews/{second,quotes,resolutions}/`: getrennte unabhängige Prüfartefakte.
- `.github/{CODEOWNERS,workflows/}`: PR-/Environment-Gates; GitHub-**Branch Protection muss separat eingerichtet** sein.
- `docs/`: Methodik, Quellendisziplin, Auswahl, Kapitelaufbau. `chapters/`: freie Erzählstruktur.

**Done =** valide Extract-/Rohtext-Hashes, alle Aussagen mit abgerufenen Belegen oder ausdrücklich ungeklärt, Quellenpaket eingefroren, getrennte Zweitcodierung + Differenzenabgleich, Originalsprachen-/Zahlenprüfung durch Fachperson, menschlich geschützter Merge/Release. **Technische Validierung allein beweist keine historische Wahrheit oder echte Unabhängigkeit.**
