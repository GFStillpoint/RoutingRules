#!/usr/bin/env python3
"""Publish sing-box v2 source and binary rule sets from the Loon subscriptions."""
from collections import defaultdict
import ipaddress
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SUBS = ROOT / "subscriptions"
OUTPUT = SUBS / "sing-box"
NAMES = ("US", "Crypto", "Overseas", "Direct")
FIELDS = {
    "DOMAIN": "domain",
    "DOMAIN-SUFFIX": "domain_suffix",
    "DOMAIN-KEYWORD": "domain_keyword",
    "IP-CIDR": "ip_cidr",
    "IP-CIDR6": "ip_cidr",
}


def convert(path):
    fields = defaultdict(set)
    skipped = 0
    no_resolve = 0
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(",")
        kind = parts[0]
        if kind == "USER-AGENT" and len(parts) == 2:
            skipped += 1
            continue
        if kind not in FIELDS or len(parts) not in (2, 3) or not parts[1]:
            raise ValueError(f"{path.name}: unsupported rule {line}")
        if len(parts) == 3:
            if kind not in ("IP-CIDR", "IP-CIDR6") or parts[2].lower() != "no-resolve":
                raise ValueError(f"{path.name}: unexpected extra field {line}")
            no_resolve += 1
        value = parts[1].lower()
        if kind in ("IP-CIDR", "IP-CIDR6"):
            network = ipaddress.ip_network(value, strict=False)
            if network.version != (6 if kind == "IP-CIDR6" else 4):
                raise ValueError(f"{path.name}: address family mismatch {line}")
            value = str(network)
        fields[FIELDS[kind]].add(value)
    # Separate blocks are OR alternatives, preserving the individual Loon
    # matches instead of accidentally requiring domain AND destination IP.
    blocks = [{key: sorted(values)} for key, values in sorted(fields.items()) if values]
    if not blocks:
        raise ValueError(f"{path.name}: empty rule set")
    count = sum(len(values) for values in fields.values())
    print(f"{path.stem}: {count} unique matches; {skipped} Loon-only USER-AGENT; "
          f"{no_resolve} IP entries use client DNS behavior", flush=True)
    return {"version": 2, "rules": blocks}


def main():
    outputs = {name: convert(SUBS / f"{name}.list") for name in NAMES}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for name, data in outputs.items():
        source = OUTPUT / f"{name}.json"
        binary = OUTPUT / f"{name}.srs"
        source.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        subprocess.run(["sing-box", "rule-set", "compile", "--output", str(binary), str(source)], check=True)
        contents = binary.read_bytes()
        if len(contents) <= 4 or contents[:4] != b"SRS\x02":
            raise ValueError(f"{binary.name}: invalid SRS v2 header")
        # Validate binary loading using sing-box itself and a local route rule.
        config = {
            "outbounds": [{"type": "direct", "tag": "direct"}],
            "route": {
                "rules": [{"rule_set": ["check"], "outbound": "direct"}],
                "rule_set": [{"type": "local", "tag": "check", "format": "binary", "path": str(binary)}],
                "final": "direct"
            }
        }
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "config.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")
            subprocess.run(["sing-box", "check", "-c", str(config_path)], check=True)
        print(f"Verified {name}.json / {name}.srs ({len(contents)} bytes)", flush=True)


if __name__ == "__main__":
    main()
