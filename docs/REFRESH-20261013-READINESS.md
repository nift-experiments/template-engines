# Candidate refresh readiness — 2026-10-13

Candidate: committed `main` SHA `7f7e487c47a87e871dfef53345e2b71288008bff`. Use a fresh independent core clone, exact detached checkout and empty pre-build porcelain status. Untracked local core material is excluded. Historical measurements and docs remain frozen. These are preparation instructions, not a certification claim; freeze the new suite SHA only after correctness/capability gates pass.

Build with the Makefile's normal `-O2` configuration, record compiler/version/flags, source SHA, CLI SHA-256 and embedded library/adapter hashes where applicable. No sanitizer/instrumentation flags in official timing. Installers accept `NIFT_SOURCE_SHA` (full lowercase 40-digit SHA); absent override preserves historical behavior. Capture `make -n`/build log and effective flags in the shared campaign receipt. Do not reuse a local old `work/nift-source` clone for this campaign.

Comparator policy: retain historical exact versions for direct contract comparison, verify download checksums/lockfiles, and disclose these are pinned versions rather than an unsupported claim of latest. Any comparator update requires its own recorded pin and historical-comparability caveat. New series metadata may be provided with `NIFT_BENCH_VERSIONS_JSON` to filesystem/template runners; historical `docs/VERSIONS.json` stays unchanged.

Baseline suite: `9370f7128bc13743949b108feaf548d42f460ab8`. Historical embedded source was `30d17733742132a1e474ce90ee4f5bee4a8bce06`. Exact pins: Jinja2 3.1.6, MarkupSafe 3.0.4; npm-lock Nunjucks 3.2.4, Handlebars 4.7.10, LiquidJS 10.30.0; cloud Node 22.22.1 (different from runtime suites, disclose). `requirements.txt` exact versions but no wheel hashes; preserve resolved wheel hashes in new environment receipt.

Embedded build: `NIFT_SOURCE_SHA=<candidate> sh scripts/build.sh` (normal `make -j4 embed`, adapter `g++ -std=c++17 -O2 -pthread ... libnift_c.a -ldl`). Fresh cloud bootstrap calls this with inherited override. Record archive and adapter SHA-256 as well as core source; CLI-only artifact identity cannot stand in for embedded measurement.

Full small correctness certification:

```sh
python3 scripts/certify.py
python3 scripts/semantics.py
python3 scripts/variant_gates.py
```

All existing corpus shapes and supported boundaries checked; fresh bytes exact, persistent adapter checks every sample, malformed template must reject, both single-render data variants retained. Historical corpus generated files are immutable; no regeneration necessary. Gate 10k-record loops, partials/root/loaders and alternating contexts explicitly. `corpus.py` is only needed to validate regeneration in a scratch clone.

Candidate public `include/nift/engine.h` exposes source rendering and internal cache semantics but no public `Prepared`/`prepare` method found. Confirm via pinned public API and compiled probe before retaining prepared-parse/reuse unavailable cells. Keep Nift source-reuse separate from peers' parsed/prepared reuse; if public prepared capability exists, add independently labelled supplement with matching compile/render/reuse oracles and audit extension.

Official: `python3 scripts/run.py work/refresh-official`; `python3 scripts/audit.py work/refresh-official`. TIMING-PLAN.json retains historical samples/batches, 2 warmups and rotation. Runner output metadata now records actual core checkout and library/adapter hashes plus optional new versions manifest. No silent old-source identity from docs.
