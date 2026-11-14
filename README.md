# LoonRules

Routing rule lists for Loon, with a small configuration extension for FlClash.

## Files

| Path | Contents |
| --- | --- |
| `rules/AI.list` | AI services and related tools |
| `rules/Crypto.list` | Crypto and Web3 services |
| `rules/US_Media_Finance.list` | Financial and international news sources |
| `rules/Utility.list` | Utility, documentation and external resource domains |
| `flclash/LoonRules.js` | FlClash configuration extension |
| `plugins/Device_Loopback.plugin` | Optional local developer service loopback for Loon 3.5.3 (1007)+ |

## Rule format

Each `.list` file contains plain-text rules, one per line. For example:

```text
DOMAIN-SUFFIX,example.com
```

Lines starting with `#` are comments. The lists contain matching rules only; proxy policies are assigned in the client. Use each file's raw URL as a subscription endpoint. Renamed files require the subscription URL to be updated.

## FlClash

`flclash/LoonRules.js` is an extension for a compatible Mihomo subscription, not a standalone proxy configuration. It converts the main node selector into a latency-based `url-test` group using its underlying nodes, then adds remote rule providers for the AI, Crypto/Web3 and Finance lists. Other subscription rules and groups are retained. The Utility list is optional and is not loaded by this extension.

The rule providers refresh independently. If the extension script itself changes, a client that stores an imported copy may need the script re-imported.

## Karing

Karing uses sing-box JSON source rule sets rather than Loon `.list` subscriptions:

| Karing rule set | Source list |
| --- | --- |
| `karing/AI.json` | `rules/AI.list` |
| `karing/Crypto.json` | `rules/Crypto.list` |
| `karing/US_Media_Finance.json` | `rules/US_Media_Finance.list` |
| `karing/Utility.json` | `rules/Utility.list` |

Each JSON rule set contains the same domain suffixes as its source list. In Karing, add a remote `Rule Set` in a custom diversion group and set the outbound action separately.

**Keep the JSON files in sync when editing a `.list` file.** Only the source `.list` should be edited for domain changes; then regenerate the matching JSON from its domain suffix entries. No credentials or client settings are stored in either format.

## Maintenance

1. Update the most specific existing list for the domain or service.
2. Check official domains, duplicate entries and overlap with other lists before adding a rule. Avoid broad matches on shared infrastructure unless necessary.
3. Keep rule syntax, file names and subscription paths unchanged unless a migration is intentional.
4. When editing the FlClash script, test nested groups, selector name variations, repeated application and preservation of existing rules.

Commit changes to `main`; raw file URLs then continue to serve the same paths.
