# Adapter audit

| Boundary | Nift | Jinja2 | Nunjucks | Handlebars | LiquidJS |
|---|---|---|---|---|---|
| Persistent host | C++ executable, embedded engine | Python | Node | Node | Node |
| Main prepare+render | render_text, parser/evaluator per call | from_string + render | eager Template + render | lazy compile + invoke | parse + renderSync |
| Prepare-only | unavailable | compile to code object | eager Template | precompile JavaScript source | parse token/AST |
| Prepared render | unavailable | Template.render | Template.render | compiled function, forced before timer | renderSync parsed tokens |
| Memory includes | custom source map | DictLoader, normal cache | custom loader, normal cache | registered compiled partials | custom filesystem source map, normal cache |
| Files | render_path + supported root reset per op | FileSystemLoader, cache disabled | custom file loader, noCache | host reads and compiles partial | native file loader, cache disabled |

No tracked builds, generated sites or application servers are measured. Inputs are immutable, preloaded context values are intentionally outside persistent timers, and engine-native lookup/stringification stays inside. Main templates are recreated in parse+render. Prepared artifacts differ intrinsically. Text-only raw output is intentional; this experiment does not compare context-sensitive HTML escaping.

Repeated-render scenarios alternate two datasets and check every output. Single-render cells use fixed preloaded data; their results do not measure fresh JSON decoding or a new HTTP request. Distinct-template scenarios cycle unique sources and output suffixes rather than claiming template-cache hits. Filesystem results include warm OS caches, but engine source/partial caches are invalidated/disabled per operation. Nift root reset cost is included explicitly.

Persistent rows are amortized per engine operation, not per batch. Fresh rows are complete invocation totals; many-render fresh calls contain all requested renders, while persistent many-render values divide by render count. Tables/charts preserve this distinction.

Persistent memory is one maximum-process RSS observation over the whole worker lifetime, including preload, preparation, batched outputs and validation. It is diagnostic and is not pooled with per-fresh-invocation child RSS distributions. CPU times for persistent workers also cover that lifetime; they are not claimed as engine-only CPU time.
