#!/usr/bin/env python3
"""Collect, validate and publish shared routing rules in client-specific formats."""
from __future__ import annotations

from pathlib import Path
import json
import build_loon
import build_singbox
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources" / "custom"
OUTPUTS = ROOT / "subscriptions"
MANIFEST = ROOT / "sources" / "upstream" / "sources.json"
ALLOWED_TYPES = {
    "DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "USER-AGENT",
    "IP-CIDR", "IP-CIDR6",
}
VALID_DOMAIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")

def lines(text: str) -> list[str]:
    return [s.strip() for s in text.splitlines() if s.strip() and not s.lstrip().startswith("#")]


def validate_classical(text: str, label: str) -> list[str]:
    result = lines(text)
    for item in result:
        parts = item.split(",")
        kind = parts[0]
        if kind not in ALLOWED_TYPES or len(parts) < 2 or not parts[1]:
            raise ValueError(f"Invalid rule in {label}: {item!r}")
        if len(parts) != 2 and not (
            len(parts) == 3 and kind in {"IP-CIDR", "IP-CIDR6"}
            and parts[2].lower() == "no-resolve"
        ):
            raise ValueError(f"Unsupported rule fields or policy in {label}: {item!r}")
    return result


def read_local(file: str, minimum: int = 0) -> list[str]:
    path = SOURCES / file
    result = validate_classical(path.read_text(encoding="utf-8-sig"), file)
    if len(result) < minimum:
        raise ValueError(f"Local source {file} unexpectedly short: {len(result)}")
    return result


def download(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "RoutingRules-Builder/1.0"})
    with urllib.request.urlopen(request, timeout=45) as res:
        text = res.read().decode("utf-8-sig")
    if not text or "<html" in text[:300].lower():
        raise ValueError(f"Unexpected content returned for {url}")
    return text


def read_domain_set(text: str, label: str) -> list[str]:
    result = []
    for raw in lines(text):
        domain = raw[1:] if raw.startswith(".") else raw
        if not VALID_DOMAIN.fullmatch(domain):
            raise ValueError(f"Invalid domain-set entry in {label}: {raw!r}")
        kind = "DOMAIN-SUFFIX" if raw.startswith(".") else "DOMAIN"
        result.append(f"{kind},{domain.lower()}")
    return result


def fetch_upstream():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    groups = {"Direct": [], "Overseas": []}
    urls = {"Direct": [], "Overseas": []}
    for source in manifest["sources"]:
        category = source["category"]
        url = source["url"]
        content = download(url)
        if source["format"] == "classical":
            rules = validate_classical(content, url)
        elif source["format"] == "domain-set":
            rules = read_domain_set(content, url)
        else:
            raise ValueError(f"Unknown source format: {source['format']}")
        if len(rules) < source["minimum"]:
            raise ValueError(f"Incomplete upstream source: {url} ({len(rules)})")
        groups[category].extend(rules)
        urls[category].append(url)
    return groups, urls


def merged(*groups: list[str]) -> list[str]:
    return list(dict.fromkeys(item for group in groups for item in group))


def must_include(name: str, rules: list[str], required: tuple[str, ...]) -> None:
    found = set(rules)
    for rule in required:
        if rule not in found:
            raise ValueError(f"Missing required {name} rule: {rule}")


def build() -> dict[Path, str]:
    upstream, urls = fetch_upstream()
    local = {
        "US": ["US_AI.list", "US_Google.list", "US_Finance.list"],
        "Crypto": ["Crypto.list"],
        "Direct": ["Direct.list"],
        "Overseas": ["Overseas.list"],
    }
    minimums = {
        "US_AI.list": 195, "US_Google.list": 570, "US_Finance.list": 300,
        "Crypto.list": 190, "Direct.list": 100, "Overseas.list": 20,
    }
    records = {
        name: merged(*(read_local(file, minimums[file]) for file in files),
                     upstream.get(name, []))
        for name, files in local.items()
    }
    us = records["US"]
    crypto = records["Crypto"]
    direct = records["Direct"]
    # Preserve existing precedence and remove exact overlaps with US and Direct.
    excluded = set(us) | set(direct)
    records["Overseas"] = [rule for rule in records["Overseas"] if rule not in excluded]
    overseas = records["Overseas"]

    must_include("US", us, (
        "DOMAIN-SUFFIX,openai.com", "DOMAIN-SUFFIX,bloomberg.com",
        "DOMAIN-SUFFIX,google.com", "DOMAIN-SUFFIX,google.cn",
        "DOMAIN-SUFFIX,youtube.com", "DOMAIN-SUFFIX,gmail.com",
        "DOMAIN-SUFFIX,googleapis.com", "DOMAIN-KEYWORD,google",
    ))
    must_include("Crypto", crypto, ("DOMAIN-SUFFIX,hyperliquid.xyz", "DOMAIN-SUFFIX,tradingview.com"))
    must_include("Direct", direct, (
        "DOMAIN-SUFFIX,qcc.com", "DOMAIN-SUFFIX,qichacha.com",
        "DOMAIN,sysdk.cl2009.com", "DOMAIN,analytics.oceanengine.com",
    ))
    must_include("Direct", direct, ("DOMAIN-SUFFIX,apple.com", "DOMAIN-SUFFIX,icloud.com"))
    must_include("Overseas", overseas, ("DOMAIN-SUFFIX,github.com", "DOMAIN-SUFFIX,githubusercontent.com"))

    must_include("US", us, (
        "DOMAIN-SUFFIX,refuseless.com", "DOMAIN-SUFFIX,cursorapi.com",
        "DOMAIN-SUFFIX,institutionalinvestor.com", "DOMAIN-SUFFIX,afp.com",
    ))
    must_include("Direct", direct, (
        "DOMAIN-SUFFIX,psbc.com", "DOMAIN-SUFFIX,bankcomm.com",
        "DOMAIN-SUFFIX,unionpay.com", "DOMAIN,sysdk.cl2009.com",
        "DOMAIN,analytics.oceanengine.com",
    ))

    provenance = {
        name: [f"sources/custom/{file}" for file in files] + urls.get(name, [])
        for name, files in local.items()
    }
    outputs = build_loon.export(records, provenance, OUTPUTS / "loon")
    outputs.update(build_singbox.export(records, OUTPUTS / "sing-box"))
    return outputs


def main() -> None:
    # Validate all inputs before writing anything.
    outputs = build()
    for path, value in outputs.items():
        if path.exists() and path.read_text(encoding="utf-8") == value:
            print(f"Unchanged: {path.relative_to(ROOT)}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
        print(f"Updated: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
