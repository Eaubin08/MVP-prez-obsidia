# Obsidia Canonical Engine — v1.0.0

This repository is a **canonical, audit-oriented** implementation of a layered control engine.
It is designed to make **structural guarantees explicit**, testable, and reviewable.

## Scope

- Defines **layer boundaries** (OS0→OS4) and enforces them with tests.
- Implements **time-based safety gating** (X-108) and sandboxed execution.
- Adds a **structural equilibrium gate** (OS2) based on graph topology metrics.
- Provides a reproducible **freeze** (hash + version) for external review.

## Layer model (OS0 → OS4)

### OS0 — Axioms / Contract / IR / Sandbox (frozen base)
**Purpose:** define what is permitted structurally; execute in a constrained environment.
**Must not depend on:** OS1, OS2.
**Folder:** `src/obsidia_os0/`

### OS1 — Decision orchestration + X-108
**Purpose:** parse → validate → X-108 hold → sandbox → decision.
**May depend on:** OS0 and OS2 (one-direction only).
**Folder:** `src/obsidia_os1/`

### OS2 — Structural metrics (pure functions)
**Purpose:** compute structural equilibrium metrics on a Core subgraph
(triangles / hexagon score proxy / asymmetry / score S) with strict Core-vs-World invariance.
**Must not depend on:** OS0, OS1.
**Folder:** `src/obsidia_os2/`

### OS3 — Operators (dynamic pipelines)
**Purpose:** extend with dynamic operators (ACP, calibration loops, simulation).
**Status in this pack:** documented layer placeholder / extension point.

### OS4 — Meta / Civilisation layer
**Purpose:** vision, ontology, civilization constraints, narrative structures.
**Status in this pack:** documentation layer placeholder / extension point.

## Audit guarantees (what is tested)

- **Boundary integrity:** OS0 never imports OS1/OS2; OS2 never imports OS0/OS1.
- **Core invariance:** Core score is unchanged under World-only modifications.
- **End-to-end sanity:** minimal pipeline runs and returns a stable decision type.

## How to run tests

```bash
python -m pip install -U pip
pip install -e .
pip install pytest
pytest -q
```

## Canonical freeze markers

- `VERSION` : `1.0.0`
- `CANONICAL_HASH.sha256` : SHA-256 of the repository content (frozen snapshot)
- `CANONICAL_FREEZE.txt` : freeze metadata

## External audit pack

A separate audit bundle is provided alongside this release.
