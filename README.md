<p align="center">
  <img src="assets/banner.png" alt="AI Corner Store — a neon cyberpunk night storefront" width="100%">
</p>

<p align="center">
  <sub>Banner — an AI adaptation of <a href="https://jesse-zhou.medium.com/jesses-ramen-case-study-77bae77ab5f0">Jesse Zhou's ramen shop</a>.</sub>
</p>

# AI Corner Store

A small, curated shop of AI skills, plugins, and bundles — each a **self-contained release** you can install on its own. One repo, one folder per release.

## Releases

| Release | What it is | Install path |
|---|---|---|
| [`organisational-dysfunction`](./organisational-dysfunction) | Diagnose org & team dysfunction as a problem of structure, not people — 73 named dysfunctions read through open sociotechnical systems theory. | `organisational-dysfunction` |
| [`laws-of-ux`](./laws-of-ux) | Treat human limits — working memory, attention, tolerance for choice — as hard design constraints. 21 psychological laws, applied to interfaces *and* to configs, prompts, CLI output and the options a tool offers. | `laws-of-ux` |
| [`designsystemet`](./designsystemet) | **Experimental.** Build with Digdir's Designsystemet correctly on the first attempt — quote-verified component contracts (twins), a WCAG guard hook, MCP twins server, and the `/ds-check` audit. Interim home; moves to kihub. | `designsystemet` |
| _more coming_ | | |

## Installing

Add the store as a marketplace once, then install any release:

```
/plugin marketplace add sorensensig/ai-corner-store
```

Or install a single release by path:

```json
{ "source": { "source": "github", "repo": "sorensensig/ai-corner-store", "path": "organisational-dysfunction" } }
```

> **Moved from `sorensensig/organisational-dysfunction`** (marketplace `sorensen-skills`). If you installed it under the old name, re-add the marketplace once with the command above — the old repo URL still redirects here.
