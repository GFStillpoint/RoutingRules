#!/usr/bin/env python3
"""Build four Loon subscriptions from curated local inputs and blackmatrix7.

Output:
    subscriptions/{US,Crypto,Direct,Overseas}.list
    rules/China.list and rules/Crypto.list (temporary legacy aliases)

If any upstream fetch or input validation fails, stop without writing any output.
Do not manually edit generated files.
"""
from __future__ import annotations

from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
OUTPUTS = ROOT / "subscriptions"
LEGACY = ROOT / "rules"
UPSTREAM = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Loon"
ALLOWED_TYPES = {
    "DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "USER-AGENT",
    "IP-CIDR", "IP-CIDR6",
}
VALID_DOMAIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")

REMOTE = {
    "China": ("China", "China", 50, 3000),
    "Apple": ("Apple", "Apple", 35, 1400),
    "Proxy": ("Proxy", "Proxy", 100, 6500),
}


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
    request = urllib.request.Request(url, headers={"User-Agent": "LoonRules-Builder/1.0"})
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


def fetch_pair(name: str) -> tuple[list[str], list[str], tuple[str, str]]:
    directory, basename, min_classical, min_domainset = REMOTE[name]
    base = f"{UPSTREAM}/{directory}/{basename}"
    url_classical, url_domainset = f"{base}.list", f"{base}_Domain.list"
    classical = validate_classical(download(url_classical), url_classical)
    domainset = read_domain_set(download(url_domainset), url_domainset)
    if len(classical) < min_classical or len(domainset) < min_domainset:
        raise ValueError(
            f"Incomplete {name} source: classical={len(classical)}, domains={len(domainset)}"
        )
    return classical, domainset, (url_classical, url_domainset)


def merged(*groups: list[str]) -> list[str]:
    return list(dict.fromkeys(item for group in groups for item in group))


def must_include(name: str, rules: list[str], required: tuple[str, ...]) -> None:
    found = set(rules)
    for rule in required:
        if rule not in found:
            raise ValueError(f"Missing required {name} rule: {rule}")


def format_rules(name: str, rules: list[str], sources: list[str], policy: str) -> str:
    header = [
        f"# NAME: {name}",
        "# FORMAT: Loon classical rules; one match per line without a policy",
        f"# SUGGESTED POLICY: {policy}; policy is assigned by the Loon client",
        "# AUTO-GENERATED: edit sources/*.list, not this file",
        *[f"# SOURCE: {source}" for source in sources],
        f"# RULES: {len(rules)}",
        "",
    ]
    return "\n".join([*header, *rules, ""])


def build() -> dict[Path, str]:
    china, china_domains, china_urls = fetch_pair("China")
    apple, apple_domains, apple_urls = fetch_pair("Apple")
    proxy, proxy_domains, proxy_urls = fetch_pair("Proxy")
    direct_custom = read_local("Direct_Custom.list", 100)
    overseas_custom = read_local("Overseas_Custom.list", 7)
    utility = read_local("Overseas_Utility.list", 12)
    us_ai = read_local("US_AI.list", 195)
    us_google = read_local("US_Google.list", 570)
    us_finance = read_local("US_Finance.list", 300)

    # The source text of Crypto is intentionally copied unmodified for old URLs.
    crypto_text = (SOURCES / "Crypto.list").read_text(encoding="utf-8-sig")
    crypto = validate_classical(crypto_text, "Crypto.list")
    if len(crypto) < 190:
        raise ValueError(f"Crypto source unexpectedly short: {len(crypto)}")

    us = merged(us_ai, us_google, us_finance)
    china_only = merged(direct_custom, china, china_domains)
    direct = merged(direct_custom, china, china_domains, apple, apple_domains)
    # Specific US/Crypto subscriptions should precede broader Overseas/Direct.
    # Remove exactly duplicated Direct and US entries from Overseas; more
    # general base rules continue to cover unrelated services.
    direct_keys = set(direct)
    us_keys = set(us)
    overseas = [rule for rule in merged(overseas_custom, utility, proxy, proxy_domains)
                if rule not in direct_keys and rule not in us_keys]

    must_include("US", us, (
        "DOMAIN-SUFFIX,openai.com", "DOMAIN-SUFFIX,bloomberg.com",
        "DOMAIN-SUFFIX,google.com", "DOMAIN-SUFFIX,google.cn",
        "DOMAIN-SUFFIX,youtube.com", "DOMAIN-SUFFIX,gmail.com",
        "DOMAIN-SUFFIX,googleapis.com", "DOMAIN-KEYWORD,google",
    ))
    must_include("Crypto", crypto, ("DOMAIN-SUFFIX,hyperliquid.xyz", "DOMAIN-SUFFIX,tradingview.com"))
    must_include("China", china_only, (
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

    outputs = {
        OUTPUTS / "US.list": format_rules(
            "US", us, ["sources/US_AI.list", "sources/US_Google.list", "sources/US_Finance.list"], "choose an appropriate client strategy"
        ),
        OUTPUTS / "Crypto.list": crypto_text,
        OUTPUTS / "Direct.list": format_rules(
            "Direct", direct, [
                "sources/Direct_Custom.list", *china_urls, *apple_urls,
            ], "DIRECT"
        ),
        OUTPUTS / "Overseas.list": format_rules(
            "Overseas", overseas, [
                "sources/Overseas_Custom.list", "sources/Overseas_Utility.list", *proxy_urls,
            ], "choose an appropriate client strategy"
        ),
        # Keep the old China and Crypto subscription URLs working during migration.
        LEGACY / "China.list": "\n".join([
            "# NAME: China (blackmatrix7 + custom)",
            "# FORMAT: Loon classical rule subscription",
            "# POLICY: DIRECT (set in Loon subscription, not in this file)",
            "# AUTO-GENERATED: deprecated alias; edit sources/Direct_Custom.list",
            f"# SOURCE: {china_urls[0]}",
            f"# SOURCE: {china_urls[1]}",
            f"# RULES: {len(china_only)}",
            "", *china_only, "",
        ]),
        LEGACY / "Crypto.list": crypto_text,
    }
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
