# Would I actually use Nift as a template engine?

Qualitative practitioner assessment, not benchmark evidence. Written while implementing the five adapters; final numerical observations are separate.

## The language itself

Yes: Nift is an attractive general-purpose text-template language. `$[d.title]` is compact and recognizable, and `@for(item : d.records){...}` gives a named local rather than forcing authors into a positional/context stack. The same expression surface covers nested access, conditions and simple transformations. Includes are explicit source relationships. These are templating advantages in their own right; they do not depend on claiming tracked builds are faster.

Jinja/Nunjucks still have the most immediately familiar interpolation surface for an existing Python/JS template author. Their opening/closing block tags also make nested HTML easy to scan. I would not declare one spelling universally superior. Nift's braces are precise but punctuation becomes dense when large expressions, control flow and HTML are packed onto one line. An agent should format that structure, not minimize characters.

Handlebars is clean for deliberately logic-light views. Its context/`this` conventions required special attention in nested loops; named locals in Nift/Jinja/Nunjucks/Liquid were easier to inspect. Handlebars helpers intentionally keep more logic in application code. That separation is a feature when a team wants it, not a deficiency to defeat with a scripting benchmark. Liquid's constrained filters/blocks likewise encode a deliberate product boundary.

## What I actually encountered

Jinja interpreted a dictionary key named `items` as a host method under dot access. The independent output gate caught it; we renamed the shared field to `records` before freeze. That is a concrete implicit lookup convention an agent must know. Jinja also strips a final newline by default, so the adapter explicitly preserves it. Neither issue makes Jinja a poor engine, but exact-byte generation needs explicit environment policy.

Handlebars `compile()` is lazy. Prepared-render timing requires forcing the returned function before starting the timer; parse-only uses its separate precompile API. That is another convention an agent can easily misunderstand if it reasons only from API names.

Nift's source-vs-path API is clearer than guessing whether a string is a file. Its per-render Context and engine-owned loader also separate data, source policy and rendering. File source caching needed explicit treatment in the benchmark. The public result exposes controlled errors and discovered dependencies rather than silently persisting a project build record. This makes embedding useful without dragging in a website build.

The major standalone capability gap is a public prepared-template artifact. Keeping an Engine alive is not the same as parsing a template once. I would want an explicit prepare/render contract with source identity, include invalidation, lifetime and concurrency rules, not a benchmark-only hidden fast path. Existing source caching does not justify describing AST reuse as supported.

## Six-month maintenance and agents

An agent should be able to identify the data binding, local loop scope, include boundary and output contract independently. Nift's named scopes and explicit includes help. Jinja/Nunjucks also provide excellent structured template representations. Handlebars/Liquid can make agent modifications safer precisely because they restrict what the template is allowed to do.

Minimum character count is not the objective. Useful explicitness states semantic roles; redundant declarations merely create synchronization work. For every engine I would prefer formatted source, an explicit data schema, exact-output fixtures, escaping policy and an include tree over dense syntax with implicit defaults. Nift's richer expressions/functions can reduce awkward helper plumbing, but business decisions, network calls and persistence should remain outside presentation templates unless the project deliberately owns that policy there.

## Current preferences at equal performance

| Project requirement | My choice | Concrete reason |
|---|---|---|
| Small standalone native text generation with named data and explicit composition | Nift is a credible first choice | Direct embedded native API, expressive named loops, source/path distinction; no project required |
| Existing Python application | Jinja2 | Native Python values, established framework integration, macros and environment policy already in the application |
| Existing JavaScript application with expressive view composition | Nunjucks | Native JS data and template constructs without adding a native build/deployment dependency |
| Logic-light JS views reused heavily | Handlebars | Prepared functions and application-owned helpers match that presentation boundary |
| A product intentionally standardized on Liquid filters/blocks | LiquidJS | The constrained authoring contract is the actual requirement |
| Nift-owned website or mixed generation project | Nift | One expression/composition model plus tracked ownership is a real project advantage |
| Agent-maintained standalone templates | Nift or Jinja/Nunjucks according to host | Nift's explicit scopes/composition are compelling; existing host values and prepared reuse can decide the choice |
| Repeated server-side renders of a fixed complex template today | A prepared-template engine | Public prepare/reuse APIs provide a concrete capability Nift does not yet expose |

I would not retain another renderer underneath Nift merely on architectural principle. If Nift supplied a reliable prepared-template API, predictable include invalidation, equally strong escaping policy/diagnostics and comparable repeated-render performance, I would be comfortable choosing it for new standalone and agent-maintained native templating. Existing Python/JS applications may still prefer their native engine because of concrete data/framework/deployment integration, not because the Nift template language is inherently unsuitable.

## Scope of this judgement

This campaign exercises equivalent raw text output. It does not certify contextual HTML escaping, untrusted-template sandboxing, async application filters, localization, streaming output or every framework integration. Those are named requirements to evaluate when relevant; the benchmark cannot establish them from successful text rendering. Nift's tracked build model is compelling in a Nift project and irrelevant to an isolated renderer's throughput claim.
