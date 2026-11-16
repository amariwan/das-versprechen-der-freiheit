# Forschungsdesign v3.1 – Buch statt Fall-Lexikon

**Stand:** 16. November 2026. **Zeitraum des Buches:** 1789–2026. **Status:** Pilot- und Redaktionsdesign, noch keine akademische Freigabe.

## Tragende Buchfrage

**Unter welchen Bedingungen überleben Freiheitsversprechen die Phase des politischen Machtwechsels – und weshalb können dieselben Veränderungen Freiheit gleichzeitig stärken und schwächen?**

Drei Unterfragen: (1) Welche institutionellen Regeln halten politische Konkurrenz und Machtwechsel offen? (2) Wann wird „Freiheit“ auf bestimmte Gruppen oder Teilrechte begrenzt? (3) Welche Gegenkräfte – Gerichte, Zivilgesellschaft, internationale Bindungen, Eliten, Wahlteilnahme – verändern die Entwicklung?

Es geht um Mechanismen, **nicht** um eine von Anfang an feststehende Niedergangsgeschichte. Ein Fall kann institutionell positive und negative Phasen haben. Kausalität ist nicht mit Zeitfolge gleichzusetzen.

## Fallauswahl

- **Methodentestwelle**: Portugal 1974–1976, Iran 1978–1983, Ungarn 2010–2026.
- Danach maximal **8–15 Hauptfälle** anhand theoretischen Kontrasts; weitere 15–25 Kurzfälle nur als Perspektivvergleich und ausdrücklich ohne Gleichsetzung des Evidenzniveaus.
- Auswahlmatrix: Epoche, Weltregion, politischer/ideologischer Kontext, Übergangstyp (Wahl, Revolution, Putsch, Verhandlung), Verlauf der Freiheiten, Quellenlage, Vergleichsnutzen, alternative Erklärungen.
- Nicht nach dem Ergebnis allein auswählen. Fälle mit politischer Öffnung und tatsächlichem Machtwechsel müssen vertreten sein.
- **Spanien 1975–1978:** nur als ergänzende institutionelle Vergleichsfolie; kein automatisch gleichartiger Fall einer mobilisierten Freiheitsbewegung.

## Messung

- F1–F5 bleiben **Dimensionen**, M01–M10 sind **Unterindikatoren**; keine doppelten Scores und kein summarischer „Freiheitsindex“ aus dem Bauch heraus.
- Jeder Indikator: *Baseline (mit Datum) → Rechtslage → Vollzug / gesellschaftliche Wirkung → Betroffene Gruppen → Folgeperiode → Gegenbelege → Unsicherheit*.
- Wenn kein belastbarer Vergleich vorliegt: **unknown**, nicht „unverändert“. Für F4/F5 das formale Gesetz nie mit Wirkungen verwechseln.
- Differenzierte Zeitfenster: Portugal vor 25.4.1974 → Frühjahr 1975 → Ende 1976; Iran vor Februar 1979 → Dezember 1979 → Ende 1983; Ungarn 2010 → 2011/12 → vor April 2026 → nach Mai 2026.
- Zahlen erhalten Datensatz **und Version/Publikationsdatum**, Zähler, Nenner, Definition, Wahlart, Berichtszeitpunkt. Widersprüchliche Werte bleiben nebeneinander, bis die Grundgesamtheiten geklärt sind.

## Zwei Ebenen des Ergebnisses

1. **Forschungsakte:** voller, dokumentierter technischer Audit-Trail (Original, Retrieval, codierte Beobachtungen, Blindvergleich, Resolution, humanes Fachreview, Release).
2. **Buchtext:** Menschen, Ereignisse, überprüfbare Daten und Erklärung. Keine YAML-Erklärungen im erzählerischen Haupttext; Methodenkapitel und technische Forschungsbelege im Anhang/Repository.

## Review-Gates und ehrlicher Bearbeitungsstatus

`web angesehen` **≠** `lokal bytebasiert archiviert` **≠** `unabhängig codiert` **≠** `historisch verifiziert` **≠** `publikationsreif`.

Die drei neuen Fall-YAMLs sind absichtlich `draft` mit `unknown`: Webrecherche wurde betrieben, aber der isolierte Dateicontainer konnte die Originalbytes nicht direkt abrufen. Diese Fakten fließen zunächst in eigenständige Rechercheakten mit Links, **nicht als vorgetäuschte A-Belege in das validierende Register**. Die Rohquellen müssen später rechtmäßig mit `scripts/ingest_source.py` importiert werden; danach Erst-/unabhängige Zweitcodierung, Resolution und PR-Review. Eine KI darf ihre eigene zweite Antwort nicht als unabhängigen Reviewer ausgeben.

## Abnahmetest nach der Pilotwelle

- Prüfen wir bei allen drei Fällen dieselbe Frage, ohne eine erzwungene Dramaturgie zu produzieren?
- Ist für jede entscheidende Wertung eine Baseline und ein Gegenargument auffindbar?
- Sind Originalquellen/Übersetzungen sauber voneinander getrennt?
- Lässt sich ein 1.500–3.000-Wörter-Kapitel ohne methodisches Ballastwissen lesenswert schreiben?
- Bestehen gezielte Negativtests und unabhängiger menschlicher Review, **bevor** wir einen Fall freigeben?
