# TNI_PACK — Tests Négatifs Institutionnels (TSS-108) v1.0

But: démontrer que les tentatives de contournement sont neutralisées (BLOCK/HOLD), sans ajouter de capacité moteur.

## Exécution
- Exporter PYTHONPATH vers la racine du repo (et/ou src si layout src)
- Lancer: pytest -q

## Comportement
- Les tests "core" ciblent X108Gate (Obsidia) et gate2_x108_temporal (trading) si détectés.
- Les tests dépendant d’APIs non exposées (policy hot-reload, registry t0 write-once, audit trace engine) SKIP explicitement.
