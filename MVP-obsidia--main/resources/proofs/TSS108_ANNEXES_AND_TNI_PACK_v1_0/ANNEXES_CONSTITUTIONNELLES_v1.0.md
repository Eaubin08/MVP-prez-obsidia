# ANNEXES CONSTITUTIONNELLES — Obsidia / TSS-108 (v1.0)
Statut: Normatif (non-exécutif) — Opposabilité, audit, gouvernance.

## AC-01 — Canon OS0–OS1
### Portée
- OS0: Invariants, IR Contract, intégrité racine, non-anticipation.
- OS1: Kernel d’exécution déterministe (lecture/évaluation), sans autorité d’action.

### Invariants (normatifs)
- I1. Non-anticipation irréversible: ACT MUST NOT avant τ.
- I2. Monotonie forte: HOLD MUST pour tout t<τ (irréversible).
- I3. Idempotence: mêmes entrées -> même décision.
- I4. Priority: BLOCK > HOLD > ACT (composition).
- I5. Clock skew: elapsed<0 -> HOLD.

### Interfaces minimales
- Intent: (intent_id, irreversible, t0, metadata)
- Decision: {BLOCK, HOLD, ACT} + (wait_s, reason)

## AC-02 — Violation Taxonomy (référence: VIOLATION_TAXONOMY.yaml)
- V-T: Temporel (non-anticipation, horloge)
- V-I: Intégrité (t0 write-once, hash)
- V-P: Policy / Sandbox (tooling, budgets)
- V-A: Audit / Trace / Replay (événements, divergences)

## AC-03 — Severity Matrix (référence: SEVERITY_MATRIX.yaml)
- S0 Info, S1 Minor, S2 Major, S3 Critical, S4 Systemic.
Chaque violation mappe vers un niveau minimal (MUST).

## AC-04 — Export Légal
### Exigences
- Pack: ZIP signé incluant manifeste, traces, replay, hashes, versions.
- Rapport: HTML/PDF canonique référant aux hashes et signatures.

## AC-05 — Portails Read-Only
- Lecture seule, zéro side-effect.
- Accès par rôle, journaux d’accès.
- Exposition d’artefacts signés uniquement.

## AC-06 — Certification Mapping
- Mapping contrôles -> preuves (tests, logs, packs).
- Cible: EU AI Act / ANSSI / ISO/IEC pertinents.
- Le mapping n’altère pas le moteur: il référence des preuves existantes.

## AC-07 — Policy Hot-Reload (Safe Mode)
- Toute mutation de policy en vol MUST déclencher HOLD global temporaire.
- Reprise ACT uniquement après validation de cohérence.

## AC-08 — Incident Protocol
1) Detect (taxonomy) 2) Contain (BLOCK/HOLD) 3) Replay 4) Report 5) Patch+Re-test.

## AC-09 — Human Veto (formel)
- Veto humain est un opérateur prioritaire non-bypassable.
- Toute tentative de bypass MUST produire BLOCK.
