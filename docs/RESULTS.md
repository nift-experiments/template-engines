# Official results

Frozen measured suite: 0af69aead395d71e5b7294132d573e2049911b53. Nift source: 30d17733742132a1e474ce90ee4f5bee4a8bce06. All 375 cells passed; 17,950 measured samples + 750 warmups; 6,081,550 timed engine operations. No outlier removal. All 5,790 frozen corpus hashes verified.

| Case / boundary | Nift | Jinja2 | Nunjucks | Handlebars | LiquidJS |
|---|---:|---:|---:|---:|---:|
| literal / fresh | 3.392071 | 70.854355 | 43.783339 | 55.568667 | 56.462657 |
| article / fresh | 4.201437 | 74.108013 | 49.614075 | 63.346483 | 64.291877 |
| loop-10000 / fresh | 150.337608 | 102.409656 | 88.138939 | 87.876445 | 217.280073 |
| literal / render | 0.014052 | 0.213652 | 0.019350 | 0.035813 | 0.003224 |
| article / render | 0.434690 | 1.930968 | 0.276772 | 0.831594 | 0.356311 |
| loop-10000 / render | 113.578199 | 16.179046 | 11.329717 | 2.135186 | 82.300739 |
| article / reuse | Unavailable | 0.044122 | 0.019029 | 0.005153 | 0.184301 |

Fresh values are ms/invocation. Persistent values are amortized ms/render; Nift render means its supported source-reuse API, including reparsing. Prepared reuse is unavailable for Nift.

Nift has low fresh-process latency for the tiny/article cases. That is not a sustained-throughput ranking: prepared peers are much faster on repeated complex templates, and Nift loses the large record-loop throughput case. Native language/runtime, context copying, parser/lookup and reuse capabilities are distinct contributors.

Fresh literal child-RSS medians: Nift 17.750 MiB, Jinja2 20.250, Nunjucks 50.125, Handlebars 52.633, LiquidJS 54.621. Persistent memory is whole-worker lifetime high-water RSS and is not pooled with those per-invocation distributions.
