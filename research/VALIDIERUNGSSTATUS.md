# Stand der Evidenz – Pilotwelle 16.11.2026

**Technische Validität**: `scripts/validate.py` akzeptiert alle drei vorbereiteten *Entwurfsfälle*. Der generierte Codebook-Abgleich und 11 vorhandene Negativ-/Strukturtests bestehen.

**Wissenschaftlicher Evidenzstatus**: Quellen bisher über Web-Recherche gelesen und in den Dossiers verlinkt; sie wurden **nicht** bytegenau in `sources/register.yaml` aufgenommen. Deshalb enthält keine Fall-YAML erfundene Rohtext-Hashes, eingetragene Direktzitate, codierte Ergebnisse oder Selbstfreigaben. Das ist beabsichtigt.

`python scripts/pilot_readiness.py` zeigt je Fall den tatsächlichen Fortschritt. `python scripts/pilot_readiness.py --require-review-ready` muss für die gegenwärtige Pilotrecherche mit Exitcode 2 abbrechen.

| Phase | Portugal | Iran | Ungarn |
|---|---|---|---|
| Institutionelle Webquellen gesichtet | Ja | Ja | Ja |
| Chronologie + offene Konflikte dokumentiert | Ja | Ja | Ja |
| Erstes Kapitel zum Test der Erzählung | Ja | – | – |
| Originalbytes rechtmäßig archiviert und Hash geprüft | Nein | Nein | Nein |
| Alle F-Unterindikatoren quellengebunden erstcodiert | Nein | Nein | Nein |
| Unabhängige Blindcodierung + Resolution | Nein | Nein | Nein |
| Fachreview von Zitaten, Daten und Übersetzungen | Nein | Nein | Nein |
| Geschützte GitHub-Release-Attestation | Nein | Nein | Nein |

**Keine dieser Recherchen ist bereits ein freigegebener Fall.** Die nächsten Schritte müssen von einem Archivierungs-/Ingestlauf und einem unabhängigen Menschen/Review-Team durchgeführt werden.
