# Template engine follow-up — no core changes made

## Prepared-template contract

The measured public API offers render_text/render_path but no standalone prepare-only or prepared-template handle. Source caching is not an AST reuse contract. Proposed separate-core work: explicit prepared-template lifetime/source identity, include invalidation, concurrent immutable renders, per-request Context and diagnostics. Preserve text/path distinction and exact output semantics. No benchmark fast path was introduced.

## Context binding copy investigation

Source inspection at the frozen revision shows Engine::render constructing a shared RuntimeValue copy for every Context binding; RuntimeValue copy recursively copies arrays/objects. This is a hypothesis for large-data overhead, not proof of the full loop bottleneck.

diagnostics/context-copy.cpp isolates a literal output with request-context arrays of 0/10/100/1000/10000 records against an engine-default binding. It uses only public APIs, validates every output, constructs input outside timing and retains two warmups plus ten 100-render samples. Run separately after official measurements. Engine defaults are static and not a substitute for request-scoped changing data.

Reproduce: compile with the pinned libnift_c.a and headers as in scripts/build.sh; run the diagnostic on the same CPU. Inspect context ownership/lifetime before considering shared immutable backing or a borrowed read-only render overlay. Public Value copy/independence semantics must remain intact.

## Loop and source evaluation

Use the frozen loop-10 through loop-10000 corpus with adapters/nift.cpp. Contrast literal with large Context, nested-field interpolation and actual record rendering. Profile parser/evaluator, lookup, allocation and output growth before attributing all overhead to reparsing. Do not infer an asymptotic explanation from four benchmark points alone.

The experiment workspace does not modify core. Diagnostic values are distinct from official observations and must not be pooled.

## Observed separate diagnostic

A 10,000-record request Context with literal output cost 3.641258 ms/render median; the equivalent engine-default binding cost 0.002193 ms. This isolates unconditional request-binding copying in this API path. The official 10,000-record loop cost 113.578 ms, so context copying alone explains only a small part; parser/lookup/loop execution remains to be profiled. Static defaults are not a substitute for request-specific values. Two warmups and ten 100-render samples are retained for each diagnostic cell.

## Separate software CPU profile

A 99 Hz cpu-clock/DWARF profile of 22 large-loop renders captured 254 samples with zero lost samples. It shows parser/expression paths, string comparison and allocation activity. This short sample profile is diagnostic, not a precise decomposition or a proof that one function causes the whole gap. Raw perf data, decoded report, render samples and binary SHA-256 identities are retained separately from official observations. Next core work should isolate loop-body parsing and value lookup before optimizing.
