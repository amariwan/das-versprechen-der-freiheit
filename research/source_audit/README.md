# Quellenregister – Webrecherche (16.11.2026)

In `SOURCES_WEB_20261116.yaml` sind 18 einzeln geprüfte Quellenseiten dokumentiert. `web_read` bedeutet: Inhalt wurde über die Web-Recherche gelesen bzw. anhand der Fundstelle nachvollzogen. **Nicht** bedeutet es: Originaldatei bytegenau archiviert, Quellenechtheit wissenschaftlich begutachtet oder Zitat freigegeben.

Die Weblesefunktion liefert keine vertrauenswürdig rekonstruierbaren Originalbytes für `scripts/ingest_source.py`. Direkte Downloads in die Laufzeit schlugen fehl (DNS bzw. Downloadfehler). Deshalb bleiben `raw_archived: false`, `raw_sha256: null` und `independent_quote_review: false`. Bestehende `sources/register.yaml` und `cases/*.yaml` sind **bewusst unverändert**.

Nächster echter Archivierungsschritt: autorisierte Downloadkopie pro Originalquelle -> `python scripts/ingest_source.py` mit *Originaldatei* und belegbarem Needle -> Prüfung des Locator -> unabhängiger Originalsprachen-Review. Ein Hash einer selbst formulierten Zusammenfassung wäre **kein** Hash des Originals.

Für drittveröffentlichte akademische Werke nur kurze rechtmäßig nutzbare Auszüge archivieren. Von Verfassungen die maßgebliche historische Fassung vergleichen, nicht die heutige konsolidierte Fassung.
