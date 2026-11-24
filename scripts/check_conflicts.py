#!/usr/bin/env python3
"""Resolve cross-tier duplicates and report detectable rule intersections."""
from datetime import datetime, timezone
from html import escape
from itertools import combinations
import ipaddress
import json

SPECIAL = ("US", "Crypto")
GENERAL = ("Overseas", "Direct")
CATEGORIES = SPECIAL + GENERAL


def intersections(left, right):
    """Find explicit host/suffix/keyword relationships and IP intersections.

    This is a conservative structural check, not a traffic simulation.
    Arbitrary wildcard USER-AGENT and speculative keyword matches are excluded.
    """
    def index(rules):
        domains, keywords, networks = {}, [], []
        for rule in rules:
            kind, value, *_ = rule.split(",")
            value = value.lower()
            if kind in ("DOMAIN", "DOMAIN-SUFFIX"):
                domains.setdefault(value, []).append((kind, rule))
            elif kind == "DOMAIN-KEYWORD":
                keywords.append((value, rule))
            elif kind in ("IP-CIDR", "IP-CIDR6"):
                networks.append((ipaddress.ip_network(value, strict=False), rule))
        return domains, keywords, networks

    ld, lk, li = index(left)
    rd, rk, ri = index(right)
    found = set()

    def add(kind, a, b):
        if a != b:
            found.add((kind, a, b))

    def host_suffix(hosts, suffixes, reverse=False):
        for host, entries in hosts.items():
            labels = host.split(".")
            for i in range(len(labels)):
                suffix = ".".join(labels[i:])
                for kind_b, rule_b in suffixes.get(suffix, ()):
                    if kind_b != "DOMAIN-SUFFIX":
                        continue
                    for kind_a, rule_a in entries:
                        a, b = (rule_b, rule_a) if reverse else (rule_a, rule_b)
                        add("domain_suffix", a, b)

    host_suffix(ld, rd)
    host_suffix(rd, ld, True)
    for host, entries in ld.items():
        for keyword, rule_b in rk:
            if keyword in host:
                for _, rule_a in entries:
                    add("domain_keyword", rule_a, rule_b)
    for host, entries in rd.items():
        for keyword, rule_a in lk:
            if keyword in host:
                for _, rule_b in entries:
                    add("domain_keyword", rule_a, rule_b)
    for ka, a in lk:
        for kb, b in rk:
            if ka in kb or kb in ka:
                add("keyword_containment", a, b)
    for na, a in li:
        for nb, b in ri:
            if na.version == nb.version and na.overlaps(nb):
                add("ip_network", a, b)

    return sorted(found)


def analyze(records):
    """Specialized rules supersede general duplicates; peers stay independent."""
    if set(records) != set(CATEGORIES):
        raise ValueError("Unexpected rule categories")
    before = {name: len(records[name]) for name in CATEGORIES}
    sets = {name: set(records[name]) for name in CATEGORIES}
    removed = []
    for rule in sorted(set.union(*(sets[n] for n in SPECIAL))):
        kept = [n for n in SPECIAL if rule in sets[n]]
        dropped = [n for n in GENERAL if rule in sets[n]]
        if dropped:
            removed.append({"rule": rule, "kept_in": kept, "removed_from": dropped})
    specialized = set.union(*(sets[n] for n in SPECIAL))
    final = {
        name: [r for r in records[name] if name in SPECIAL or r not in specialized]
        for name in CATEGORIES
    }
    retained = []
    for a, b in (SPECIAL, GENERAL):
        for rule in sorted(set(final[a]) & set(final[b])):
            retained.append({"rule": rule, "categories": [a, b]})

    overlaps = []
    for a, b in combinations(CATEGORIES, 2):
        for kind, ra, rb in intersections(final[a], final[b]):
            overlaps.append({"type": kind, "categories": [a, b], "rules": [ra, rb]})

    for n in GENERAL:
        if set(final[n]) & specialized:
            raise AssertionError(f"Unresolved cross-tier duplicate: {n}")
    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rule_counts": {
            n: {"before": before[n], "after": len(final[n])} for n in CATEGORIES
        },
        "removed_duplicates": removed,
        "retained_exact_duplicates": retained,
        "range_overlaps": overlaps,
    }
    print("Conflict check: "
          f"{sum(len(r['removed_from']) for r in removed)} cross-tier entries removed; "
          f"{len(retained)} peer duplicates retained; "
          f"{len(overlaps)} structural overlaps detected", flush=True)
    return final, report


def render_markdown(report):
    def cell(value):
        return escape(str(value)).replace("|", "&#124;").replace("\n", " ")

    lines = [
        "# Rule conflicts / 规则冲突报告", "",
        f"Generated / 检测时间: `{report['generated_at']}`", "",
        "[JSON data / 结构化数据](conflicts.json)", "",
        "Specialized rules (US, Crypto) take precedence over exact duplicates in "
        "general rules (Overseas, Direct). Within each tier, rule priority is chosen in the client. "
        "Structural overlaps are retained. / 专项规则优先于基础规则中的完全重复项；"
        "同层级优先级由客户端决定，匹配范围重叠仅报告。", "",
        "## Rule counts / 规则数量", "",
        "| Category / 分类 | Before / 处理前 | After / 处理后 |",
        "| --- | ---: | ---: |",
    ]
    for name, counts in report["rule_counts"].items():
        lines.append(f"| {name} | {counts['before']} | {counts['after']} |")
    removed = report["removed_duplicates"]
    retained = report["retained_exact_duplicates"]
    overlaps = report["range_overlaps"]
    lines += [
        "", f"## Removed exact duplicates / 已去重 ({len(removed)})", "",
        "| Rule / 规则 | Kept in / 保留于 | Removed from / 移除于 |",
        "| --- | --- | --- |",
    ]
    for row in removed:
        lines.append(f"| {cell(row['rule'])} | {', '.join(row['kept_in'])} | {', '.join(row['removed_from'])} |")
    lines += [
        "", f"## Retained peer duplicates / 同层重复 ({len(retained)})", "",
        "| Rule / 规则 | Categories / 分类 |",
        "| --- | --- |",
    ]
    for row in retained:
        lines.append(f"| {cell(row['rule'])} | {', '.join(row['categories'])} |")
    lines += [
        "", f"## Structural overlaps / 匹配范围重叠 ({len(overlaps)})", "",
        "Detected domain suffix relationships, explicit keyword containment and overlapping IP networks. "
        "These are structural checks, not exhaustive runtime matches. / 检测域名后缀、明确的关键词包含关系及 IP 网段重叠；"
        "不等同于实际流量匹配的穷尽检测。", "",
        "<details>", "<summary>View all overlaps / 查看全部重叠</summary>", "",
        "| Type / 类型 | Category A | Rule A | Category B | Rule B |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in overlaps:
        a, b = row["categories"]
        ra, rb = row["rules"]
        lines.append(f"| {row['type']} | {a} | {cell(ra)} | {b} | {cell(rb)} |")
    lines += ["", "</details>", ""]
    return "\n".join(lines)


def render_json(report):
    return json.dumps(report, ensure_ascii=False, indent=2) + "\n"
