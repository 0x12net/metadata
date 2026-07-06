# metadata
Service data for company applications

## Files

| File | Consumed by | Purpose |
|---|---|---|
| `correction_cpl_jlc.csv` | `kicadRelease.sh` (`-c`) in [kici](https://github.com/0x12net/kici) | Global placement (CPL) rotation/offset corrections |
| `risk_classification.csv` | `kicadRiskCheck.sh` in [kici](https://github.com/0x12net/kici) | Part risk classification used by the KiCad Risk Check pipeline |
| `userAgent.txt` | `bomVerifier.py` (`USERAGENTURL`) in [kici](https://github.com/0x12net/kici) | User-Agent string for distributor API/scrape requests, kept current by `scripts/update_useragent.py` |

## risk_classification.csv

Consumed by `kicadRiskCheck.sh`/`riskChecker.py` in [kici](https://github.com/0x12net/kici), referenced from a hardware repository's pipeline via a raw-file URL (`RISKCLASSIFICATIONURL`), the same way `kicad-release.yml` references `correction_cpl_jlc.csv` via `CORRECTIONCPLURL`.

Columns:

| Column | Description |
|---|---|
| `risk_level` | `1` (low) / `2` (medium) / `3` (critical) |
| `part` | Chip name or MPN/SKU. Glob pattern: `*`/`?` wildcards, case-insensitive |
| `description` | Free text, why this part is classified this way (shown in the pipeline log) |

`description` is free text and often contains commas -- standard CSV quoting applies: wrap the field in `"..."` if it contains a comma, a `"` (doubled: `""`), or a newline. An unquoted comma splits the row into an extra column and silently truncates the description.

Each entry is matched against a BOM part's chip name (`Value`/`Comment` field) and its `mpn`/`*_sku` fields. A pipeline run fails only when the highest risk level found across the BOM reaches `RISK_FAIL_LEVEL` (default `3`, critical); lower levels are reported but don't fail the build.
