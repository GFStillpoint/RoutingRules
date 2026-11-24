#!/usr/bin/env python3
"""Export unified rule records as Loon LIST subscriptions."""
from pathlib import Path


def format_rules(name: str, rules: list[str], sources: list[str], policy: str) -> str:
    header = [
        f"# NAME: {name}",
        "# FORMAT: Loon classical rules; one match per line without a policy",
        f"# SUGGESTED POLICY: {policy}; policy is assigned by the Loon client",
        "# AUTO-GENERATED: edit sources/custom/*.list, not this file",
        *[f"# SOURCE: {source}" for source in sources],
        f"# RULES: {len(rules)}",
        "",
    ]
    return "\n".join([*header, *rules, ""])



def export(records, provenance, output_dir: Path) -> dict[Path, str]:
    """Render Loon subscriptions without fetching or classifying sources."""
    return {
        output_dir / f"{name}.list": format_rules(
            name, rules, provenance[name],
            "DIRECT" if name == "Direct" else "client-selected strategy",
        )
        for name, rules in records.items()
    }
