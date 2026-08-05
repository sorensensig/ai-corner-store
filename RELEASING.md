# Adding a release

A release is a top-level folder containing `.claude-plugin/plugin.json`. Creating that
folder is the *start* of adding a release, not the end.

## The rule

**A release is not added until all four places know about it.** Three of them are
functional — get them wrong and the release does not install, or never gets a version
cut, while everything still looks fine in the diff.

| # | Place | What breaks without it |
|---|---|---|
| 1 | `<release>/.claude-plugin/plugin.json` — `name` matches the folder | every downstream reference is ambiguous |
| 2 | `.claude-plugin/marketplace.json` — an entry in `plugins[]` | **`/plugin install <release>` does nothing** |
| 3 | `.github/workflows/release.yml` — the `release:` matrix | **no GitHub Release is ever cut**; the version in `plugin.json` means nothing |
| 4 | `README.md` — a row in the Releases table | nobody can find it |

Run the check before opening the PR:

```bash
bash scripts/check-release-registration.sh
```

It discovers releases from the filesystem, so a new folder is picked up automatically —
the burden is on the registrations to catch up, never on you to add the release to a list
of things to check.

## Why this is a gate and not a paragraph

`laws-of-ux` merged as a complete, reviewed release folder — SKILL.md, 21 references,
attribution, an eval harness — and was still invisible. It was missing from
`marketplace.json` and from `release.yml`'s matrix, and its own README documented an
install command that could not work.

`release.yml` already carried the instruction, in its own header comment:

> Adding a future release = add its folder to the RELEASES list below.

That comment was read during the work and it still did not fire. An instruction that has
to be recalled at the moment someone is absorbed in shipping the actual content is not a
control. `scripts/check-release-registration.sh` runs in CI on every push and PR, so the
requirement is enforced at the point it is violated rather than remembered.

## When a release changes

Bumping an existing release does not touch registrations, but it does touch counts and
prose that are maintained by hand:

- `<release>/.claude-plugin/plugin.json` — `version`
- `<release>/README.md` — the metadata table, the changelog, and **every** count in the
  body prose, not just the first one
- `README.md` (store root) — the Releases table, if it quotes a count

Hand-maintained counts drift. `organisational-dysfunction/loop/research.md` sat at "59
reference files" for five additions before anyone noticed. If a number can be derived,
derive it; if it cannot, prefer prose that does not quote one.
