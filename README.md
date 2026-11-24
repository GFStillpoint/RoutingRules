# RoutingRules

RoutingRules 是一个持续维护的网络分流规则集，按服务类型整理域名与 IP 规则，并提供适配不同客户端的订阅文件。

RoutingRules is a curated and continuously maintained collection of network routing rules. It organizes domain and IP rules by service category and publishes subscription files in formats for different clients.

## 规则分类 / Rule Categories

| 分类 / Category | 内容 / Coverage |
| --- | --- |
| US | AI 服务、Google 生态、全球财经与新闻媒体 / AI services, Google ecosystem, financial news and international media |
| Crypto | 加密资产、钱包、交易平台及行情工具 / Crypto assets, wallets, exchanges and market analytics |
| Overseas | GitHub、国际网站及网络工具 / GitHub, international websites and online utilities |
| Direct | 中国大陆常用服务、银行、支付及 Apple 服务 / Mainland Chinese services, banking, payments and Apple services |

## 订阅地址 / Subscriptions

选择客户端对应的格式，复制链接添加至远程规则或 Rule Set，为各分类配置所需的连接策略。

Choose the format for your client, copy its URL into a remote rule or rule set, and assign a connection policy to each category.

| 分类 / Category | Loon (LIST) | Karing / sing-box (SRS) | sing-box (JSON) |
| --- | --- | --- | --- |
| US | [US.list](https://raw.githubusercontent.com/linjiayinchn/RoutingRules/main/subscriptions/loon/US.list) | [US.srs](https://raw.githubusercontent.com/linjiayinchn/RoutingRules/main/subscriptions/sing-box/US.srs) | [US.json](https://raw.githubusercontent.com/linjiayinchn/RoutingRules/main/subscriptions/sing-box/US.json) |
| Crypto | [Crypto.list](https://raw.githubusercontent.com/linjiayinchn/RoutingRules/main/subscriptions/loon/Crypto.list) | [Crypto.srs](https://raw.githubusercontent.com/linjiayinchn/RoutingRules/main/subscriptions/sing-box/Crypto.srs) | [Crypto.json](https://raw.githubusercontent.com/linjiayinchn/RoutingRules/main/subscriptions/sing-box/Crypto.json) |
| Overseas | [Overseas.list](https://raw.githubusercontent.com/linjiayinchn/RoutingRules/main/subscriptions/loon/Overseas.list) | [Overseas.srs](https://raw.githubusercontent.com/linjiayinchn/RoutingRules/main/subscriptions/sing-box/Overseas.srs) | [Overseas.json](https://raw.githubusercontent.com/linjiayinchn/RoutingRules/main/subscriptions/sing-box/Overseas.json) |
| Direct | [Direct.list](https://raw.githubusercontent.com/linjiayinchn/RoutingRules/main/subscriptions/loon/Direct.list) | [Direct.srs](https://raw.githubusercontent.com/linjiayinchn/RoutingRules/main/subscriptions/sing-box/Direct.srs) | [Direct.json](https://raw.githubusercontent.com/linjiayinchn/RoutingRules/main/subscriptions/sing-box/Direct.json) |

### 快速开始 / Quick Start

**Loon:** 在规则设置中添加远程规则，填入 LIST 地址并选择策略。 / Add a remote rule using its LIST URL and select a policy.

**Karing:** 在分流规则中添加自定义规则组，填入 SRS 或 JSON 地址并选择策略。 / Create a custom diversion group, add the SRS or JSON rule-set URL, and select a policy.

建议从 US → Crypto → Overseas → Direct 的顺序开始配置，按实际需要调整优先级和默认策略。 / A suggested starting order is US → Crypto → Overseas → Direct. Adjust priority and the default policy to suit your setup.

## 插件 / Plugins

项目还提供独立的客户端辅助插件。 / Additional client utilities are available as optional plugins.

| 客户端 / Client | 插件 / Plugin | 功能 / Features |
| --- | --- | --- |
| Loon | [Device Loopback](https://raw.githubusercontent.com/linjiayinchn/RoutingRules/main/plugins/loon/Device_Loopback.plugin) | 支持本地开发服务的回环连接，适用于兼容的 iOS 开发工具。 / Enables local development loopback connections for compatible iOS development tools. |

在 Loon 的插件页面添加对应链接即可使用。 / Add the plugin URL in Loon's plugin settings.

## 自动更新 / Automatic Updates

项目每天同步上游规则，与自定义规则统一整理、去重及校验，并生成各客户端的订阅文件。 / Upstream and custom rules are merged, deduplicated and validated daily before being exported into client-specific subscription files.

更新计划 / Schedule: **00:17 UTC (08:17 UTC+8)**

## 项目结构 / Project Structure

| 目录 / Directory | 用途 / Purpose |
| --- | --- |
| [sources/upstream/](sources/upstream/) | 上游来源配置 / Upstream source registry |
| [sources/custom/](sources/custom/) | 自定义规则 / Curated custom rules |
| [subscriptions/](subscriptions/) | 按客户端格式发布的规则 / Client-specific subscriptions |
| [scripts/](scripts/) | 统一规则整理及各格式生成 / Shared rule processing and format-specific exporters |
| [plugins/](plugins/) | 客户端辅助插件 / Client-specific plugins |
| [.github/workflows/](.github/workflows/) | 自动更新与发布 / Automated updates and publishing |

基础规则来源包括 [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)，并结合本项目维护的服务域名。 / Base rules draw on [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script), supplemented by curated service domains.

欢迎通过 Issues 或 Pull Requests 提供建议与补充规则。 / Suggestions and contributions are welcome through Issues and Pull Requests.
