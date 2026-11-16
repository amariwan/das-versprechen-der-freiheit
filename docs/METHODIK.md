# Methodik und Forschungsdesign (v3.0)

## Gegenstand und Grenzen

**Das Versprechen der Freiheit** untersucht zwischen 1789 und 2026 öffentliche Freiheits- und Gerechtigkeitsansprüche politischer Bewegungen und die spätere Entwicklung unter konkreten Akteuren. Es ist eine **vergleichende historische Untersuchung**, keine bereits bewiesene Theorie über den zwangsläufigen Übergang zur Diktatur.

**Analyseeinheit:** ein abgegrenzter *politischer Übergangsprozess* in einem Land oder Territorium, mit festem Beobachtungsfenster. Bündnisse, Parteiflügel und nachfolgende Regierungen werden getrennt erfasst. Ein Landesname ist keine einheitliche Akteursgruppe.

### Forschungsfragen

1. Welcher **spezifische Freiheitsbegriff** wurde wann, von wem, an wen adressiert und wie war er damals gemeint?
2. Welche institutionellen, rechtlichen und tatsächlichen Veränderungen traten danach ein – und **für welche Gruppen**?
3. Wie unterscheiden sich Fälle mit ähnlicher Ausgangslage, aber anderen Ergebnissen?
4. Wann sind Abweichungen von Versprechen nachgewiesen, und wann bleibt die Deutung offen?

## Trennung von Merkmalen, Mechanismen und Ergebnis

Das alte 20er-Modell vermischte Ursachen, Machtwege und Ergebnisse. Die überarbeitete Datenerfassung trennt:

| Typ | Speicherung | Beispiel ohne Vorbewertung |
|---|---|---|
| Kontext/Bedingung | `context` | Krieg, Wirtschaftslage, Wahlregeln, Kolonialordnung |
| Mobilisierung und Versprechen | `promises`, `actors` | konkrete, datierte öffentliche Äußerung |
| Machtweg (Kategorie, kein Muster) | `power_transition.kind` | `election`, `revolution`, `coup`, `negotiated`, `mixed` |
| Veränderungsindikatoren | `freedom_dimensions[].indicators[]` | M01–M10 innerhalb von F1–F5, jeweils mit Richtung und Belegen |
| Freiheitsdimension | `freedom_dimensions[].id` | F1–F5 als Gruppierung ohne eigenen Richtungsscore |
| Erfüllung des Versprechens | `promise_assessments[]` | `fulfilled`, `partly_fulfilled`, `contradicted`, `unresolved` |
| Historisches Resultat | `outcomes` | differenziert, nicht aus einem Code abgeleitet |

**Keine Einbahnstraße:** Für jede institutionelle Veränderung sind Verbesserungen, Rückschritte, Mischfälle und ausbleibende Veränderungen möglich. Bei fehlenden Daten lautet der Befund **unknown**, nicht „kein Effekt“.

## Zeitfenster und historische Vergleichbarkeit

- Baseline **vor** dem untersuchten Übergang festlegen. Folgezustand z. B. `0–2`, `3–10`, `>10` Jahre separat erfassen, wenn nachweisbar.
- Bei Prozessen über viele Jahrzehnte Periodenwechsel dokumentieren; Ergebnisse nicht nachträglich einer Gründerfigur zurechnen.
- Historische Begriffe zuerst zeitgenössisch erklären; den heutigen Demokratiebegriff nicht ungeprüft auf 1789 übertragen.
- Historische Massendaten sind ungleich vollständig. Keine stillschweigende Übertragung moderner Demokratie-Indizes auf die frühe Neuzeit.
- Stand des Buches: **16.11.2026**. Für laufende Datensätze zählt die angegebene **Release-/Snapshotversion**, nicht nur der Abrufkalendertag.

## Fallauswahl: Selektionsbias aktiv vermeiden

Nicht vom bekannten Ausgang (Diktatur) rückwärts auswählen. Sampling vor Analyse dokumentieren, inklusive Ausschlussgründen. Quoten sind Forschungsziele, keine mathematische Repräsentativität:

- Mindestens **drei nachvollziehbare Demokratisierungs-/Freiheitsgewinn-Fälle** in der ersten Pilotwelle.
- Mindestens **drei Fälle mit Rückschritten** und **zwei gemischte/umstrittene Fälle**.
- Variation nach Region, Jahrhundert, Ideologie und Machtweg.
- Ein **Gegenfall** pro größerer Erklärungshypothese; Kontextunterschiede dokumentieren.
- **Outcome nicht voraussetzen:** Vorabklassifikation in `docs/PILOTFAELLE.md` nur als *Sampling-Hypothese*, nicht als codiertes Ergebnis.

## Kausale Erklärung

Eine Fallanalyse trennt strikt:

- **Fakt:** ein belegter Akt oder beobachtbarer Zustand.
- **Interpretation:** fachlich diskutierte Bedeutung eines Faktums.
- **Kausalhypothese:** behaupteter Mechanismus mit zeitlicher Reihenfolge, Prozessbelegen, Alternativerklärungen und möglichem Gegenbeweis.

Mindestens prüfen: soziale Schichtung, Ökonomie, außenpolitische Intervention, Krieg/Besatzung, organisierte Opposition, institutionelle Vetospieler, Rollenwechsel von Akteuren. Wer nur ein ähnliches Muster erkennt, darf **keine Ursache** behaupten.

## Vergleichsverfahren

1. Chronologie und Primärdokumente pro Fall zusammentragen, **ohne** voreilige Musterkodierung.
2. Versprechen nach Sprecher, Wortlaut, Zielgruppe, Zeitpunkt, Übersetzung und Relevanz zuordnen.
3. Unabhängige Zweitkodierung mit demselben eingefrorenen Quellenpaket und ohne Erstcodierung.
4. Unterindikatoren M01–M10 innerhalb von F1–F5 nach `config/model.yaml` bewerten: Baseline, Folgezeitraum, Gruppen, Richtung, Evidenz und Gegenbelege.
5. Kein zweites F-Richtungsurteil abgeben; rechtliche Norm und tatsächliche Wirkung im Indikator unterscheiden.
6. Gegenprobe: vergleichbare andere Fälle, fehlende Daten, abweichende Forschung und Auswahlregeln offenlegen.
7. Erst nach Quellenreview und menschlichem Abnahmegate in ein Kapitel übertragen.

## Reproduzierbarkeit / Änderungen

`config/model.yaml` und `schemas/` sind versioniert. `case.model_version` muss zur Modellversion passen. Datensätze nennen Publikations-/Releaseversionen und konkrete Quellen-Snapshots. Änderungen an Codes erfordern Migrationsnotiz und Re-Codierungsentscheidung für bestehende Fälle. **Das YAML ist maßgeblich**, Prosa dient der Erklärung und wird daraus abgeleitet.

**Grenze des Projekts:** Weltweiter Vergleich bedeutet systematische Fallvielfalt, nicht vollständige Erfassung jedes Staates und jedes Machtwechsels seit 1789.

## Verblindung und Freigabe (v3)

Pilot-Hypothesen bleiben von den Codierpaketen getrennt. Schulungsanker mit erwarteter Richtung wurden aus dem produktiven Codebook entfernt. `scripts/make_blind_packet.py` exportiert nur Frage, Baseline, Code-Entscheidungsregeln und Quellenpaket. Outcome und Erstcodierung fehlen. Zwei Codierungen werden automatisch verglichen. **Keine agentenseitig gesetzten Freigabeflags**; Schutz benötigt menschlich konfigurierte GitHub-Regeln.
