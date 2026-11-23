#!/usr/bin/env python3
"""Refresh merged Loon classical rules from blackmatrix7's rule + domain-set pairs.

Outputs China.list, Apple.list and Global.list, preserving source rule types.
Optional rules/<name>_Custom.list entries are merged ahead of upstream rules.
No source is published when any fetch/validation fails. Outputs are stable so
no commit occurs when upstream contents have not changed.
"""

from __future__ import annotations

from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "rules"
UPSTREAM = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Loon"
ALLOWED = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "USER-AGENT", "IP-CIDR", "IP-CIDR6"}
DOMAIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")

# Loon display name -> (upstream directory, upstream basename, minimum classical, minimum domain-set)
SETS = {
    "China": ("China", "China", 50, 3000),
    "Apple": ("Apple", "Apple", 35, 1400),
    "Global": ("Proxy", "Proxy", 100, 6500),
}


def content_lines(text: str) -> list[str]:
    return [s.strip() for s in text.splitlines() if s.strip() and not s.lstrip().startswith("#")]


def read_upstream(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "LoonRules-Merger/1.0"})
    with urllib.request.urlopen(req, timeout=45) as res:
        data = res.read().decode("utf-8-sig")
    if not data or "<html" in data[:250].lower():
        raise ValueError(f"Invalid upstream content: {url}")
    return data


def read_classical(text: str, label: str) -> list[str]:
    result = content_lines(text)
    for item in result:
        parts = item.split(",")
        kind = parts[0]
        if kind not in ALLOWED or len(parts) < 2 or not parts[1]:
            raise ValueError(f"Invalid classical rule in {label}: {item!r}")
        if len(parts) != 2 and not (
            len(parts) == 3
            and kind in ("IP-CIDR", "IP-CIDR6")
            and parts[2].lower() == "no-resolve"
        ):
            raise ValueError(f"Unexpected policy/fields in {label}: {item!r}")
    return result


def read_domain_set(text: str, label: str) -> list[str]:
    result = []
    for item in content_lines(text):
        domain = item[1:] if item.startswith(".") else item
        if not DOMAIN.fullmatch(domain):
            raise ValueError(f"Invalid DOMAIN-SET entry in {label}: {item!r}")
        kind = "DOMAIN-SUFFIX" if item.startswith(".") else "DOMAIN"
        result.append(f"{kind},{domain.lower()}")
    return result


def build_one(name: str, upstream_dir: str, upstream_name: str, min_classical: int, min_domains: int) -> str:
    base = f"{UPSTREAM}/{upstream_dir}/{upstream_name}"
    classical_url, domains_url = f"{base}.list", f"{base}_Domain.list"
    classical = read_classical(read_upstream(classical_url), f"{name} classical")
    domains = read_domain_set(read_upstream(domains_url), f"{name} domain-set")
    if len(classical) < min_classical or len(domains) < min_domains:
        raise ValueError(f"{name} upstream unexpectedly short: {len(classical)} + {len(domains)}")

    additions_path = RULES / f"{name}_Custom.list"
    additions = read_classical(additions_path.read_text(encoding="utf-8-sig"), f"{name} custom") if additions_path.exists() else []

    merged = list(dict.fromkeys([*additions, *classical, *domains]))
    expected = {
        "China": ("DOMAIN-SUFFIX,qcc.com", "DOMAIN-SUFFIX,qichacha.com"),
        "Apple": ("DOMAIN-SUFFIX,apple.com", "DOMAIN-SUFFIX,icloud.com"),
        "Global": ("DOMAIN-SUFFIX,google.com", "DOMAIN-SUFFIX,youtube.com"),
    }[name]
    for item in expected:
        if item not in merged:
            raise ValueError(f"Critical {name} rule missing: {item}")

    comment = [
        f"# NAME: {name} (blackmatrix7 + custom)",
        "# FORMAT: Loon classical rule subscription",
        "# AUTO-GENERATED: do not edit; optional additions go in rules/<name>_Custom.list",
        "# POLICY: Assign DIRECT/Proxy strategy in Loon, not in this file.",
        f"# SOURCE: {classical_url}",
        f"# SOURCE: {domains_url}",
        f"# RULES: {len(merged)} (custom {len(additions)}, upstream {len(classical)} + {len(domains)})",
        "",
    ]
    return "\n".join([*comment, *merged, ""])


def main() -> None:
    outputs = {}
    for name, args in SETS.items():
        outputs[RULES / f"{name}.list"] = build_one(name, *args)

    # All source reads and validations must succeed before changing ANY file.
    for path, new_text in outputs.items():
        old_text = path.read_text(encoding="utf-8") if path.exists() else None
        if new_text != old_text:
            path.write_text(new_text, encoding="utf-8")
            print(f"Updated {path.relative_to(ROOT)}")
        else:
            print(f"Unchanged {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
