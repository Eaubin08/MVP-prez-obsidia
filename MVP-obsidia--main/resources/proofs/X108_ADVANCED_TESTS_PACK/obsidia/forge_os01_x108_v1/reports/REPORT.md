# Obsidia OS0↔OS1 — Pytest Run Report

Date: $(date -Is)

## Résumé
- Tests: 2
- Failures: 0
- Errors: 0
- Skipped: 0

## Artefacts
- `reports/junit.xml` (Junit)
- `reports/pytest_stdout.txt` (console)

## Notes
- Ce run valide le chemin **OS1 → Contrat → OS0 Sandbox → décision (ACT/HOLD)** sur les tests internes du pack.
- Le pack fourni `X108_Ontology_Tests_v7_DROPIN_1770196354.zip` contient surtout des scripts/artefacts d'ontologie (pas un CSV/JSON de scénarios). Donc le mode **“1 scénario = 1 test”** attend toujours un vrai dataset scénarios (CSV/JSON) (tes packs v4/v5/v6 en contiennent).
