# LEGAL EXPORT SCHEMA (v1.0)

## Pack minimal (ZIP signé)
MUST contain:
- MANIFEST.json (version, build, hashes)
- SIGNATURES/ (root signature, key id)
- TRACES/ (event streams)
- REPLAY/ (expected vs observed, diff)
- REPORT/ (HTML et/ou PDF canon)
- LICENSE/NOTICE (si open)

## MANIFEST.json (exemple)
{
  "standard": "TSS-108",
  "version": "1.0.0",
  "generated_at": "<ISO8601>",
  "root_hash": "<sha256>",
  "artifacts": [
    {"path":"TRACES/trace.jsonl","sha256":"..."},
    {"path":"REPLAY/replay.json","sha256":"..."},
    {"path":"REPORT/report.html","sha256":"..."}
  ]
}

## Exigences de recevabilité
- Chaque artefact MUST être référencé par hash.
- Le rapport MUST citer root_hash et key_id.
- Toute divergence de replay MUST être associée à une violation (taxonomy).
