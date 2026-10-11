# Template-engine campaign closeout — 2026-10-11

The campaign is complete and frozen. [Live report](https://lab.nift.dev/benchmarks/template-engines/). [Experiment repository](https://github.com/nift-experiments/template-engines), local `/home/nick/Repositories/nift/nift-experiments/template-engines`.

## Storage cleanup preceded measurement

The apparent Labs ballooning was primarily an ignored plotting environment (approximately 329 MiB) and `public.zip` (12,145,221 bytes). They were preserved under `/home/nick/Repositories/nift/.lab-tools`, outside Labs. Working-tree byte totals count filesystem stat sizes, including symlink targets; they are not physical disk allocations. Fifteen JSON audit receipts (163,038 bytes) and 382 raw memory samples in eight existing chart inputs were moved to canonical evidence; compact statistics and all published chart bytes were preserved.

| Scope | Before cleanup | After cleanup | After new report |
|---|---:|---:|---:|
| Working files excluding both Git directories | 382,014,825 | 9,299,464 | 10,534,837 |
| Tracked source + publication | 9,028,139 | 8,861,342 | 10,061,397 |
| Source `.git` bytes | 7,780,822 | 7,823,738* | 8,575,604 |
| Publication `.git` bytes | 7,816,141 | 7,816,141 | 8,507,057 |

*Post-cleanup audit checkpoint, before the final guard follow-up. Final Git totals include fetched publication objects as well as source objects; separate Git directories may contain overlapping history and should not be interpreted as unique remote bytes. Final working-file ZIP, excluding Git: 6,194,554 bytes.

Remote main/stage and all reachable refs were inspected. Unique uncompressed historical blobs were 21,772,147 bytes; the largest was legitimate hero artwork at 1,196,950 bytes. Raw pushed history was not a material clone-size cause. No history rewrite or force push. Separate cleanup source commits: `12eb402` and `6f4a2ff720497b8554aa0f14f39e7a1bf06689e8`.

The guard rejects canonical evidence namespaces, raw formats/archives, JSON audit receipts, embedded raw sample arrays and oversized payloads. It checks every pointer entry and has positive/negative self-tests. Legitimate publication datasets/figures remain allowed within the total cap. Receipt-generating scripts now write outside Labs.

## Frozen implementation and matrix

Measured suite: `0af69aead395d71e5b7294132d573e2049911b53`. Nift source: `30d17733742132a1e474ce90ee4f5bee4a8bce06`, embedded C++ library 4.11.0. Other participants: Jinja2 3.1.6 / MarkupSafe 3.0.4 / Python 3.12.3; Nunjucks 3.2.4, Handlebars 4.7.10, LiquidJS 10.30.0 / Node 22.22.1. Five participants cover native source interpretation, Python code generation, expressive JS templates, compiled logic-light templates and constrained templates; Go was omitted to keep scope bounded.

Twenty timed scenarios: literal, scalar interpolation, condition, nested object, loops 10/100/1,000/10,000, nested loops, partial depths 1/4/8, article, 2,000-record collection, 100/1,000 repeated renders alternating data, 10/100/1,000 distinct templates and case conversion. Fresh invocation, persistent prepare-and-render/source reuse, supported preparation-only, supported prepared reuse and three file-backed composition cells have separate boundaries. Nift has 43 cells; each other engine 83: 375 total. Nift's public API has no preparation-only/prepared-AST handle, so those cells are unavailable.

One fresh g6-standard-4 shared Linode: us-east, Ubuntu 24.04, AMD EPYC 7542, 4 shared vCPUs / 8 GiB, Linux 6.8.0-134-generic, $0.072/hour listed price. Same CPU affinity and rotating participant order. Frozen locally selected batches, 30–50 fresh samples, 50 persistent samples and two separate warmup rounds. Local full correctness/feasibility preceded cloud creation.

## Correctness and results

All 375 measured cells passed. Retained: 17,950 measured observations + 750 warmups = 18,700; 6,081,550 timed engine operations. No outlier removal. Independent audits verified all 5,790 corpus hashes and sample/round/batch/output/resource consistency. Cloud certification covered 393 supported corpus/mode gates; ten additional special-value/error gates and twenty second-variant/true-branch gates passed. Supplemental gates are untimed and do not change the frozen matrix. Initial local rejected development attempts are retained separately.

| Median milliseconds / boundary | Nift | Jinja2 | Nunjucks | Handlebars | LiquidJS |
|---|---:|---:|---:|---:|---:|
| Literal / fresh invocation | 3.392 | 70.854 | 43.783 | 55.569 | 56.463 |
| Article / fresh invocation | 4.201 | 74.108 | 49.614 | 63.346 | 64.292 |
| Article / prepare+render* | 0.435 | 1.931 | 0.277 | 0.832 | 0.356 |
| Article / prepared reuse | unavailable | 0.044 | 0.019 | 0.005 | 0.184 |
| 10,000 records / prepare+render* | 113.578 | 16.179 | 11.330 | 2.135 | 82.301 |

*Nift uses persistent source reuse, including reparsing. Fresh values are per entire invocation; persistent values are amortized per render. Every fresh adapter preloads both frozen datasets and all scenario sources, so this is the reproducible harness boundary, not a minimally tuned HTTP request. Prepared results are not an apples-to-apples public capability for Nift. Preparation artifacts differ across peers, and cache/reset boundaries are explicit in [ADAPTER-BOUNDARIES.md](ADAPTER-BOUNDARIES.md).

Fresh literal direct-child RSS medians: Nift 17.750 MiB, Jinja2 20.250, Nunjucks 50.125, Handlebars 52.633, LiquidJS 54.621. Persistent memory is whole-worker lifetime high water, including preload/retention/validation; it is not per-render RSS and is not pooled with fresh memory.

Nift is compelling for owned native/Nift composition and short standalone invocations. Existing Python projects often favor Jinja; expressive JS projects Nunjucks; logic-light precompiled presentation Handlebars; constrained/user-facing template requirements Liquid. Equal performance does not erase host integration or template-language policy requirements. Conversely, reliable prepared templates and comparable repeat performance would remove any inherent architectural requirement to retain another renderer inside Nift. The full candid assessment is [NIFT-TEMPLATE-ENGINE-DX-REVIEW.md](NIFT-TEMPLATE-ENGINE-DX-REVIEW.md).

No Nift core code was changed. Follow-up: an explicit prepared-template lifetime/source/include/concurrency contract; request-context copy investigation; parser/expression/lookup/allocation profiling and loop throughput. The isolated 10,000-record literal-context diagnostic measured 3.641 ms versus 0.002 ms with a static engine binding; this explains only a small part of the 113.578 ms loop. A separate 99 Hz software CPU profile captured 254 samples, zero lost; it is diagnostic, not precise causal attribution. Reproducer and [NIFT-CORE-HANDOVER.md](NIFT-CORE-HANDOVER.md) are provided. HTML-context escaping, sandboxing, async, localization and streaming were not certified.

## Publication identities and verification

- Measurement evidence: `a538d1e00440aa5ff7c51d9c35cbb24adab38617` ([frozen directory](https://github.com/nift-experiments/lab-evidence/tree/a538d1e00440aa5ff7c51d9c35cbb24adab38617/benchmarks/template-engines/20261011-v4110)).
- Experiment assessment/adapters before closeout: `4c7fc315cc25c5989e36294cb047902102eaccb8`; report assessment link pins `74114ca420152e621228e9342dc7553c650c263e`.
- Labs source: `efdc6550f6a43a4c08521d1b64e518b3cc6b4f0d`.
- Public main: `714cfe9ca16080e1a6651f500a866751df92e7d1`.
- Append-only lifecycle evidence: `ec310a81aca22122bff8fc868702ecdba5a0c738` ([receipts](https://github.com/nift-experiments/lab-evidence/tree/ec310a81aca22122bff8fc868702ecdba5a0c738/benchmarks/template-engines/20261011-v4110/lifecycle)).

Labs source was pushed first, then public main. Both storage-policy CI and Pages deployment passed. All 157 live HTML/SVG/PNG/CSS/JS files match local publication bytes. Report/homepage/collection were checked at 1440/390/320px with all images loaded, no page overflow and ten equal-width plot/table container pairs. Narrow data regions scroll independently and support keyboard navigation. The 375-row distribution detail opens without overflow. Shared green test-tube favicon is unchanged; existing report styles/graph designs are byte-preserved. All 137 prior public files besides home/collection remain unchanged.

Exactly **1,200,055 net tracked bytes** were added after cleanup. New public route/assets total **992,978 bytes**; compact publication input **99,515 bytes**. There are no raw samples/traces/corpora in the Labs addition. Twenty-one displayed assets regenerate deterministically from the compact input, with identical hashes. Website total remains below 10 MiB. All 5,844 original canonical manifest hashes remain unchanged after lifecycle append. The final private-material scan passed across 11,971 files.

## Teardown

Linode **107883449** was created 2026-10-11T06:12:35Z and deleted **2026-10-11T07:00:25Z**, only after successful live verification. CLI listing confirms absence; authenticated API returns 404. Temporary SSH key, known-host entry, CLI directory, private state and helper were removed. Existing account credentials were neither changed nor published. No campaign VM remains. Measurements/evidence are frozen; no rerun is required.
