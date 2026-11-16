# Migration v2 → v3

**Breaking Change:** `schema_version: 2.0.0`, `model_version: 3.0.0`.

1. `patterns[]` aus v2 wird in `freedom_dimensions[].indicators[]` verschoben. Zuordnung: F1 = M01,M02,M03,M10; F2 = M05,M06; F3 = M04,M07; F4 = M09; F5 = M08. Die alten separaten F-Richtungen entfallen.
2. `case_status: approved` wird **entfernt**. Zulässig sind nur `draft` und `under_review`. Externe Freigabe via `.github/workflows/research-ci.yml`, geschütztem Environment und Attestation-JSON.
3. `reviews`-Boolean-Felder entfallen. Neue unabhängige Dokumente liegen unter `reviews/second`, `reviews/quotes`, `reviews/resolutions`.
4. Quellenregister wurde v3-kompatibel um Provenienz-Raw/Extract-Hash, konkrete Pfade und Archivumfang erweitert. Alle mit v2 handgesetzten `retrieval.sha256` sind **ungültig** und müssen durch nachweisbare Abrufe neu erfasst werden.
5. `sources/origins.yaml` ist kuratierter Herkunftskatalog, der nur nach menschlichem Git-Review erweitert werden darf. Keine selbst eingetragene `independence_group` in Einzelquellen.
6. Erstelle Fallakten aus der neuen Vorlage und übertrage nur bereits **nachweislich** belegte Inhalte. Ungeklärte Aussagen auf `unknown`/`U` zurücksetzen. Danach Quellen neu einfrieren.

**Nicht automatisch migrieren:** Andernfalls würden alte Schein-Reviews und ungeprüfte Hashes unbemerkt legitimiert.
