# Externe Freigabe – Einrichtung vor jedem Publikations-Release

**Nicht durch Dateien allein erzwingbar.** Diese Einstellungen muss ein Repository-Admin in GitHub aktivieren und ihre Wirksamkeit mit einem negativen PR-Test beweisen.

1. **Ruleset für `main`:** ausschließlich PR-Merges, keine Direct Pushes/Bypasses, Required Status Check `validate`, mindestens ein Review, **CODEOWNER-Review erforderlich**, Review bei neuem Commit verwerfen, Self-Approval verhindern; Schutz auch für Admins.
2. **CODEOWNERS:** `@amariwan` ist nur eine Vorbelegung. Zweite unabhängige fachliche Person benennen; Zugriffsrechte und tatsächliche Verfügbarkeit prüfen. Änderungen an `AGENTS.md`, `scripts/`, `schemas/`, `config/`, `.github/`, `sources/origins.yaml` nur mit CODEOWNER-Review.
3. **Environment `historical-release`:** Required Reviewers aktivieren; Reviews durch Auslöser selbst deaktivieren (Prevent self-reviews); nur Branch `main` zulassen. Environment-Secret `HUMAN_REVIEW_ENV_SECRET` dort hinterlegen, nicht im Repo oder Repository-Secrets.
4. **Release:** `workflow_dispatch` mit Case-ID läuft erst nach Validierung und menschlichem Environment-Gate. Das erzeugte `*.approved.json` wird als Actions-Artefakt mit Commit-SHA exportiert. YAML-Fallstatus wird **nie** zu `approved` editiert.
5. **Red-Team-Abnahme:** PR nur mit manipuliertem `approved`-YAML, Fake-Hashes, nicht abgerufenem Beleg, fremder Codebookänderung und Fake-Reviewer einreichen. CI und Branch Protection müssen den Merge bzw. die Freigabe stoppen.

**Wichtig:** Eine GitHub-Actions-Umgebung, die keine Required Reviewers unterstützt oder falsch konfiguriert ist, darf keine „menschlich freigegebene“ Publikation ausgeben. Der Validator schützt nur interne Konsistenz, nicht Wahrhaftigkeit einer komplett gefälschten und erneut gehashten Quelle. Historische Originalprüfung bleibt ein eigener menschlicher Arbeitsschritt.
