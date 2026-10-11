# Local acceptance

All 375 supported cells passed exact-byte correctness across 20 scenarios and five engines. Nift parse-only/prepared-AST cells intentionally unavailable. Full certification took 55.3 seconds. Rejected initial attempts are retained in work/ for evidence publication.

Frozen timing plan: 50 persistent samples, 30–50 fresh samples, two separate warmup rounds, rotated engines each round, single CPU affinity. Locally selected batch counts target 10ms where feasible and bound retained output storage to approximately 16MB. Nominal official runtime 10–20 minutes plus installation/build.

The gated controller pilot passed literal, loop, include and repeated-render cells, including rotated sampling and whole-worker memory capture. Ten additional non-timed gates passed raw special characters/template-looking data and malformed-template rejection across all five engines. This is an intentionally unescaped text contract; no automatic HTML-safety claim is made.
