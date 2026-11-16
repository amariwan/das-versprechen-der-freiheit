# Quellenregeln v3 – belegbare Provenienz statt Quellenhäkchen

## Grundsatz

Alle zitierten, paraphrasierten und zur Codierung oder Versprechensbewertung verwendeten Quellen müssen `retrieval.status: retrieved` haben; bloßer bibliografischer Eintrag (`not_retrieved`) reicht nicht. Direkte Zitate erfordern Wortlaut in einem unter derselben Run-ID archivierten Rohtext und einem automatisch aus ihm erzeugten Extract. Keine frei erfundenen oder aus Gedächtnis rekonstruierte Originalzitate.

## Aufnahme & Grenzen

- `scripts/ingest_source.py` lädt eine HTTPS-Quelle oder liest einen legitimen Textfile-Snapshot; `--needle` muss in den tatsächlich empfangenen Bytes enthalten sein. Es speichert einen kurzen kontextualisierten Auszug und berechnet Hashes aus **Inhalten**, nicht aus eingetippten Hash-Feldern. Für Rohtextarchivierung: explizit `--rights-confirmed`.
- `scripts/validate.py` rechnet den Extract-Hash nach; bei vorhandenem Raw ebenso Raw-Hash und Substring-Nachweis. `extract_only` ist ein **schwächerer Provenienzbeleg**: Ein Raw-Hash ohne Rohbytes ist nicht unabhängig nachprüfbar.
- Fachperson überprüft originalsprachliche Lesart, Übersetzung, Originalarchiv/Seite, Herkunft sowie seriöse Editionslage. Ein korrekt gehashter Fake-Text bleibt ein Fake-Text.
- PDF, Scans, OCR und nicht-UTF-8-Quellen werden derzeit **nicht automatisch** geparst. Für diese erst eine fachlich geprüfte, rechtmäßig nutzbare Transkription/Edition beschaffen. Seitenzahlen und Editionen müssen manuell geprüft werden.

## Evidenzklassen (für die jeweilige Behauptung, nicht pauschal pro Quelle)

| Klasse | Technisch erzwingbare Mindestbedingung | Fachliche Aussagegrenze |
|---|---|---|
| A | mindestens eine `primary`-/`archive`-Quelle mit verifiziertem Raw-Snapshot | Primärtext belegt Wortlaut/Vorgang, nicht automatisch Motiv, Wirkung oder Kausalität. |
| B | mindestens zwei `academic`-Quellen aus unterschiedlichen **in `sources/origins.yaml` menschlich geprüften** Herkünften und Raw-Snapshots | Unabhängigkeit muss von Menschen geprüft werden. Keine künstlich doppelt gezählte Sekundärzitation. |
| C | mindestens eine tatsächlich abgerufene Quelle | Vorläufig; auch reine Auszugssicherung möglich, jedoch nicht für unverifizierte Direktzitate. |
| D | offene Hypothese ohne tragfähigen Nachweis | Nicht als gesicherter historischer Fakt verwenden. |
| U | unbekannt / nicht recherchiert | Keine gesicherte Aussage. |

Klasse A verlangt **Art und Authentizität** des Originals. Eine zeitgenössische Polemik ist Primärquelle für die Polemik, nicht automatisch für ihre Anschuldigungen. Herkunftsgruppen dürfen nicht vom Erstrecherche-Agenten als unabhängige Tatsachen gesetzt und ungeprüft übernommen werden.

## Reviews

1. Frischer zweiter Coder bekommt `make_blind_packet.py` und Codebook ohne Pilot-Anker, aber **keine** Erstcodierung, deren Begründungen oder Schlussfolgerungen. Er schreibt ausschließlich `reviews/second/CASE-ID.coding.yaml`.
2. `validate.py` diffed die Richtungen automatisch; alle Abweichungen brauchen `reviews/resolutions/CASE-ID.resolution.yaml` mit fachlicher Begründung und abgerufenen Belegen.
3. Unabhängige Zitatprüfung gehört nach `reviews/quotes/CASE-ID.quotes.yaml`; Reviewer muss von beiden Codern verschieden sein. Bei direktem Zitat stimmen Rohbytes, Extract, Lauf-ID und Locator überein. **Menschliche Fachprüfung bleibt zwingend.**
4. Endfreigabe geschieht nicht durch selbst gesetzte YAML-Booleans, sondern ausschließlich als GitHub-Actions-Artefakt nach Required Reviewers im Environment `historical-release`.

## Zahlen & Neuzeit

Nenne für jede Zahl Nenner/Grundgesamtheit, Zeitraum, Gebiet, Messdefinition, Unsicherheit und die exakt verwendete Dataset-Releaseversion. Der Veröffentlichungs- oder Abrufkalendertag allein ersetzt keine Version. Für 2010–2026 fehlende Zweitliteratur nicht durch Schein-B-Evidenz überdecken: Primärquellen für konkrete Akte und ausdrücklich vorläufige C-Interpretationen trennen.

## Urheberrecht & Bewahrung

Keine vollständigen urheberrechtlich geschützten Bücher/Artikel in das Repository kopieren. `--archive-raw` nur mit Nutzungsrecht oder bei Gemeinfreiheit. Liegt nur ein kurzer rechtmäßiger Auszug vor, ist die automatische Verifikation begrenzt; ein externer menschlicher Originalabgleich ist erforderlich, bevor ein Direktzitat publiziert wird.

Herkunftskatalog (`sources/origins.yaml`) wird nur über menschlich geprüften Git-PR kuratiert. Neue Herkunftsvorschläge dürfen als Diskussion eingebracht, aber nicht ungeprüft als „unabhängig“ klassifiziert werden.
