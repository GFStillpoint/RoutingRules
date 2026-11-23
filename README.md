# LoonRules

**简洁、自动更新的 Loon 分流规则合集。** 按服务类型整理常用网站和应用，让不同网络流量使用合适的连接策略。

**A clean, automatically updated collection of routing rules for Loon.** Organize websites and apps into practical categories and choose how each category connects.

## 规则订阅 / Rule Subscriptions

| 规则 / List | 内容 / Coverage |
| --- | --- |
| **[US](subscriptions/US.list)** | AI 服务、Google 生态、全球财经与新闻媒体 / AI services, Google ecosystem, financial news and international media |
| **[Crypto](subscriptions/Crypto.list)** | 加密货币、钱包、交易所及行情工具 / Crypto, wallets, exchanges and market analytics |
| **[Overseas](subscriptions/Overseas.list)** | GitHub、国际网站及常用网络工具 / GitHub, international sites and online utilities |
| **[Direct](subscriptions/Direct.list)** | 中国大陆常用网站、银行、支付及 Apple 服务 / Mainland Chinese websites, banking, payments and Apple services |

**订阅地址 / Subscription URLs**

~~~text
https://raw.githubusercontent.com/linjiayinchn/LoonRules/main/subscriptions/US.list
https://raw.githubusercontent.com/linjiayinchn/LoonRules/main/subscriptions/Crypto.list
https://raw.githubusercontent.com/linjiayinchn/LoonRules/main/subscriptions/Overseas.list
https://raw.githubusercontent.com/linjiayinchn/LoonRules/main/subscriptions/Direct.list
~~~

## 快速开始 / Quick Start

1. **添加订阅 / Add a subscription** — 在 Loon 的规则设置中新增远程规则，粘贴上方对应的 URL。 / Add a remote rule in Loon and paste its URL.
2. **选择策略 / Choose a policy** — 根据网络环境，为各类规则选择直连或合适的代理策略。Direct 通常选择 **DIRECT**。 / Assign a direct or proxy policy to each list. **DIRECT** is commonly used for the Direct category.
3. **排列顺序 / Set the order** — 建议按照 **US → Crypto → Overseas → Direct → FINAL** 排列，再按实际需求微调。 / A useful starting order is **US → Crypto → Overseas → Direct → FINAL**; customize it as needed.
4. **更新规则 / Refresh** — 在 Loon 中更新远程规则，即可获取仓库发布的最新内容。 / Refresh remote rules in Loon to load the latest published lists.

## 自动更新 / Automatic Updates

项目每天自动同步上游规则，并合并社区维护的扩充内容。新规则经过整理和去重后发布到四份订阅。

The repository syncs upstream rules daily, merges curated additions, and publishes refreshed lists after validation and deduplication.

**更新频率 / Schedule:** 00:17 UTC 每日一次 / Once daily at 00:17 UTC. 源规则修改后也会触发构建 / Source changes also trigger a build.

## 项目结构 / Project Structure

| 目录 / Directory | 用途 / Purpose |
| --- | --- |
| [subscriptions/](subscriptions/) | 可以直接导入 Loon 的四份规则 / Ready-to-use Loon subscriptions |
| [sources/](sources/) | 按类别整理的规则素材 / Curated source lists by category |
| [scripts/](scripts/) | 规则转换、合并与校验 / Rule conversion, merging and validation |
| [.github/workflows/](.github/workflows/) | 自动更新任务 / Scheduled updates |
| [plugins/](plugins/) | 可选的辅助插件 / Optional utilities and plugins |

### 规则来源 / Rule Sources

中国大陆、Apple 和常见境外网站的基础规则基于 [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)。AI、Google、财经媒体、加密资产和常用服务域名由本项目持续整理扩充。

Base coverage for mainland China, Apple, and international websites comes from [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script). This project maintains additional rules for AI, Google, finance, media, crypto and everyday services.

欢迎通过 Issues 或 Pull Requests 分享建议及新域名。

Suggestions and contributions are welcome through Issues and Pull Requests.
