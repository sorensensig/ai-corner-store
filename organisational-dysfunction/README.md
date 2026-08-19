# Organisational Dysfunction

|  |  |
|---|---|
| **Creator** | Sigurd Sæther Sørensen |
| **Based on** | Trond Hjorteland — *Organisational Dysfunction of the Day* ([full list](https://www.linkedin.com/pulse/organisational-dysfunction-day-full-list-trond-hjorteland-gxrze/)) |
| **Framework** | Open sociotechnical systems theory (DP1 / DP2) |
| **Contents** | 1 skill · 75 dysfunctions |
| **Version** | 0.15.0 |

A Claude Code plugin of org-design knowledge for diagnosing the recurring ways organisations and teams get stuck — and what to actually do about them.

It packages **75 named dysfunctions** from Trond Hjorteland's *"Organisational Dysfunction of the Day"* series, all read through the same lens: **open sociotechnical systems theory (OST)** and its DP1 (top-down bureaucracy) vs DP2 (self-managing teams) distinction.

## What's inside

One sharp, cleanly-triggering skill — `organisational-dysfunction` — built on Anthropic's progressive-disclosure pattern:

- **`SKILL.md`** — the always-loaded router. Holds the shared DP1/DP2 lens once, plus an index of all 75 dysfunctions grouped by theme.
- **`references/NN-*.md`** — one lean file per dysfunction: how it shows up, the sociotechnical diagnosis (the *why*), and concrete remedies. Claude reads only the one(s) that match.

## When it triggers

Whenever someone describes a workplace or team problem that smells structural rather than personal: stuck or slow decisions, hollow agile ceremonies (standups, retros, OKRs, DORA, Team Topologies), disengagement or "quiet quitting", a "frozen middle", stalled change initiatives, AI dropped into a broken process, or blame aimed at people instead of the system.

## Installation

How you install depends on which Claude you use. Pick your surface below. In every case the skill then activates **automatically** when you describe an org/team dysfunction — you never call it by name.

> **Two words worth knowing:** a **skill** is the unit of knowledge (a `SKILL.md` folder). A **plugin** is a bundle you install from a **marketplace** — which is just a Git repo that lists plugins. This release is one plugin in the **`ai-corner-store`** marketplace (repo [`sorensensig/ai-corner-store`](https://github.com/sorensensig/ai-corner-store)); it lives in that repo's `organisational-dysfunction/` folder.
>
> **Moved:** this was previously `sorensensig/organisational-dysfunction` (marketplace `sorensen-skills`). If you installed it under the old name, re-add the marketplace once with the command below — the old repo URL still redirects here.

### Claude Code (terminal, VS Code, JetBrains)

Run these inside Claude Code:

1. **Add the store as a marketplace** (once):
   ```
   /plugin marketplace add sorensensig/ai-corner-store
   ```
2. **Install the plugin:**
   ```
   /plugin install organisational-dysfunction@ai-corner-store
   ```
   (Format is `plugin-name@marketplace-name`.)
3. If it's not active immediately, **restart Claude Code** (or run `/reload-plugins`).

Prefer clicking? Run **`/plugin`** → **Marketplaces** tab → add `sorensensig/ai-corner-store` → **Discover** tab → pick **organisational-dysfunction** → Enter.
Uninstall: `/plugin uninstall organisational-dysfunction@ai-corner-store` · remove marketplace: `/plugin marketplace remove ai-corner-store`.

**No-marketplace alternative** (also works for the local Claude Desktop app, which reads the same folder):
```bash
git clone https://github.com/sorensensig/ai-corner-store
cp -r ai-corner-store/organisational-dysfunction/skills/organisational-dysfunction ~/.claude/skills/
```

> **A copied folder won't update itself.** Click **Watch → Releases** on this repo to be notified when a new version ships, then re-run the copy.

### Claude Cowork

1. Open the **Cowork** tab → **Customize** → **Plugins**.
2. Under **Personal plugins**, click **+** → **Add marketplace** → **Add from a repository**, and enter:
   `https://github.com/sorensensig/ai-corner-store`
3. Back on the **Plugins** tab, **Browse plugins**, find **organisational-dysfunction**, and click **Install**.

> Cowork won't notify you when a new version ships. Click **Watch → Releases** on this repo to be alerted, then update the plugin from **Customize → Plugins**.

### Claude.ai (web) & Claude Desktop app

These use the **Skills** feature — you upload the packaged skill.

1. **Enable code execution first** (Skills require it):
   - **Free / Pro / Max:** Settings → **Capabilities** → turn on **"Code execution and file creation"**.
   - **Team / Enterprise:** an admin enables it under **Organization settings → Skills**.
2. **Download the packaged skill:** [**organisational-dysfunction-skill.zip**](https://github.com/sorensensig/ai-corner-store/releases/latest) (from the latest release — its tag is `organisational-dysfunction-v<version>`).
3. Go to **Customize → Skills**, click **+** → **Create skill** → **Upload a skill**, and select the ZIP.

Skills uploaded this way are per-user and don't sync to other surfaces.
*(To build the ZIP yourself, from this release folder: `cd skills && zip -r organisational-dysfunction-skill.zip organisational-dysfunction` — the skill folder must sit at the ZIP's root.)*

> Uploaded skills **don't auto-update**. Click **Watch → Releases** on this repo to know when a new version ships, then re-download the ZIP and re-upload.

### Team / scripted setup (Claude Code)

To have a team pick it up automatically, add this to the project's `.claude/settings.json` (members are prompted to trust and install it):

```json
{
  "extraKnownMarketplaces": {
    "ai-corner-store": {
      "source": { "source": "github", "repo": "sorensensig/ai-corner-store" }
    }
  },
  "enabledPlugins": {
    "organisational-dysfunction@ai-corner-store": true
  }
}
```

## Attribution

The references **synthesise and paraphrase** [Trond Hjorteland](https://www.linkedin.com/in/trondhjort/)'s publicly posted series through the OST framing he uses — they are not verbatim copies. For his own words, see his article [**"Organisational Dysfunction of the Day — full list"**](https://www.linkedin.com/pulse/organisational-dysfunction-day-full-list-trond-hjorteland-gxrze/) on LinkedIn (which links every individual post) and his forthcoming (2026) book.

Each reference file also notes its source dysfunction number; the corresponding original post can be found via the full-list article above.

## Changelog

New entries are appended automatically by the update pipeline (`loop/pipeline.md`) as Trond publishes them, and each version is cut as a [GitHub Release](https://github.com/sorensensig/ai-corner-store/releases) (tagged `organisational-dysfunction-v<version>`). **Installed copies do not auto-update** — click **Watch → Releases** on this repo to be notified of new versions, then re-pull (see [Installation](#installation)). Newest first.

### 0.15.0 — 2026-08-19
- Added `#75` **Divided for efficiency** (74 → 75 dysfunctions). Generated via the update pipeline; passed the targeted routing/triggering test.

### 0.14.0 — 2026-08-18
- Added `#74` **Matrices** (73 → 74 dysfunctions). Generated via the update pipeline; passed the targeted routing/triggering test.

### 0.13.0 — 2026-08-17
- Added `#73` **What the war room proves** (72 → 73 dysfunctions). Generated via the update pipeline; passed the targeted routing/triggering test.

### 0.12.0 — 2026-08-14
- Added `#71` **The values on the wall** and `#72` **Hired from above** (70 → 72 dysfunctions). Generated via the update pipeline; both passed the targeted routing/triggering test.

### 0.11.0 — 2026-08-12
- Added `#70` **The blind decision** (69 → 70 dysfunctions). Generated via the update pipeline; passed the targeted routing/triggering test.

### 0.10.0 — 2026-08-11
- Added `#69` **Playing politics** (68 → 69 dysfunctions). Generated via the update pipeline; passed the targeted routing/triggering test.

### 0.9.0 — 2026-08-10
- Added `#68` **The bureaucracy that became the work** (67 → 68 dysfunctions). Generated via the update pipeline; passed the targeted routing/triggering test.

### 0.8.0 — 2026-08-07
- Added `#67` **The IT-business divide** (66 → 67 dysfunctions). Generated via the update pipeline; passed the targeted routing/triggering test.

### 0.7.0 — 2026-08-06
- Added `#66` **Everything is fine** (65 → 66 dysfunctions). Generated via the update pipeline; passed the targeted routing/triggering test.

### 0.6.0 — 2026-08-05
- Added `#65` **The facilitator's toolkit** (64 → 65 dysfunctions). Generated via the update pipeline; passed the targeted routing/triggering test.

### 0.5.0 — 2026-08-04
- Added `#64` **The code review that became personal** (63 → 64 dysfunctions). Generated via the update pipeline; passed the targeted routing/triggering test.

### 0.4.0 — 2026-08-03
- Added `#63` **The leadership team that isn't** (62 → 63 dysfunctions). Generated via the update pipeline; passed the targeted routing/triggering test.

### 0.3.0 — 2026-07-03
- Added `#62` **The agenda that sabotaged itself** (61 → 62 dysfunctions). Generated via the update pipeline; passed the targeted routing/triggering test.

### 0.2.0 — 2026-07-02
- Added `#60` **The output nobody owned** and `#61` **Rearranging the furniture** (59 → 61 dysfunctions). Generated via the auto-update pipeline; both passed the targeted routing/triggering test.

### 0.1.0 — 2026-06-30
- Initial release: 59 dysfunctions as one umbrella skill (router `SKILL.md` + `references/`), plus the eval/loop harness and the autoresearch-style tuning loop.
