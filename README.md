# LoonRules

A small, source-maintained Loon routing rule repository. Loon remains responsible
for choosing the policy groups; GitHub generates and publishes the matched rule sets.

## Subscribe in Loon

Use only the following files under **subscriptions/** after migration:

| File | Policy in Loon | Purpose |
| --- | --- | --- |
| [US.list](subscriptions/US.list) | Your fixed US group | AI and US-focused financial/media sources |
| [Crypto.list](subscriptions/Crypto.list) | Your crypto group | Wallets, exchanges and trading/analytics services |
| [Direct.list](subscriptions/Direct.list) | DIRECT | China, Apple and custom domestic exceptions |
| [Overseas.list](subscriptions/Overseas.list) | Available (auto-testing) | General overseas sites, Google/YouTube, GitHub and utilities |

`Overseas` is an **explicitly matched category**, not the Loon `FINAL` rule.
Keep the `GEOIP,CN,DIRECT,no-resolve` local rule and your separate `FINAL` policy
after these subscriptions. Prioritize specific US and Crypto subscriptions ahead
of the broad Direct and Overseas lists. Be aware of domain overlaps, and verify
actual matches using Loon request records.

Raw URLs:

- https://raw.githubusercontent.com/linjiayinchn/LoonRules/main/subscriptions/US.list
- https://raw.githubusercontent.com/linjiayinchn/LoonRules/main/subscriptions/Crypto.list
- https://raw.githubusercontent.com/linjiayinchn/LoonRules/main/subscriptions/Direct.list
- https://raw.githubusercontent.com/linjiayinchn/LoonRules/main/subscriptions/Overseas.list

## Repository layout

- **subscriptions/**: The four published Loon lists. **Generated**, do not edit.
- **sources/**: Files we edit to maintain US, Crypto, Direct and Overseas rules.
  - `US_AI.list`, `US_Finance.list`: inputs for the combined US subscription.
  - `Crypto.list`: crypto subscription input.
  - `Direct_Custom.list`: custom DIRECT domains; China and Apple rules are fetched from blackmatrix7.
  - `Overseas_Utility.list`, `Overseas_Custom.list`: general international services and GitHub overrides; proxy base is fetched from blackmatrix7.
- **scripts/build_rules.py**: Validated generator for all four lists.
- **.github/workflows/update-rules.yml**: Daily scheduled generator (08:17 China time) and source-change/manual triggers.
- **plugins/**: Separate optional Loon plugin(s), not merged into rule lists.

The generator converts upstream DOMAIN-SET entries to classical Loon
`DOMAIN-SUFFIX` / `DOMAIN` records and removes exact duplicate rules.
It rejects unexpectedly short/bad upstream inputs instead of overwriting
published subscriptions with incomplete data. The workflow commits only if
generated files changed. Scheduled GitHub Actions may run later than their
nominal time.

## Legacy rule URLs (temporary compatibility)

The original `rules/` folder is intentionally retained until existing Loon
subscriptions have been migrated. It contains previous `AI.list`,
`US_Media_Finance.list`, `Crypto.list`, `Utility.list`, and `China.list`
plus `China_Custom.list`. **Do not edit these legacy inputs.** The new
builder still refreshes the old `rules/China.list` and `rules/Crypto.list`
paths for compatibility; the other original files are frozen at their
previous versions. After confirming all clients use the four new subscription
URLs, the legacy folder can be removed in a separate cleanup.

This repository does not store account credentials or proxy subscriptions.
