# Motubrain · 具身数据开放计划

This repository contains the deployable static website: HTML, built JavaScript/CSS,
registration snapshot, data standard, annotation guide and demonstration media.
The editable application source remains in a separate private repository.

Open the interface directly on GitHub Pages:
[Motubrain Open Embodied Data](https://mrluckyfive.github.io/motubrain-open-data-pages/#/data-strength).

The data standard is V2.11 (consultation draft, revised 2026-11-25).
Dataset totals are a registration snapshot; the verified, deduplicated effective scale
has not yet been validated.

## Licensing

| Content | License |
| --- | --- |
| Site code and quality inspection operators | Apache License 2.0; see `open-source/APACHE-2.0.txt` |
| Dataset, registration snapshot, videos, posters and data documents under `open-data/` | CC BY-NC-SA 4.0 |

Third-party notices: `open-source/THIRD_PARTY_NOTICES.txt`.

The website uses hash routing and relative asset paths. Serve this directory directly;
no application server or database is required. `.nojekyll` preserves the static tree.
