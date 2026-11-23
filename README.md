# LoonRules

一个面向 **Loon** 的可复用分流规则项目。仓库统一维护规则来源、合并脚本和自动更新流程，最终发布四份可直接订阅的规则。**规则文件只定义匹配条件，不包含节点、代理服务器、账号、CA 证书或固定策略组。**

> Routing rules, not proxy configuration. All traffic policies are chosen in the client. A domain match does not certify that a website is trustworthy or that any product is available in a given region.

## 订阅 / Subscriptions

| 规则 | 内容 | 典型用途 |
| --- | --- | --- |
| [US.list](subscriptions/US.list) | 国际 AI 服务、辅助 API、全球财经与主流新闻媒体 | 可以绑定任意使用者选定的策略组；名称为历史分类，不强制美国节点 |
| [Crypto.list](subscriptions/Crypto.list) | 数字资产、钱包、交易平台、行情分析 | 独立分流；实际节点应符合当地法规及平台使用条款 |
| [Direct.list](subscriptions/Direct.list) | 中国大陆常用服务、银行与支付、Apple、国内 SDK 补充 | 通常绑定 **DIRECT** |
| [Overseas.list](subscriptions/Overseas.list) | 一般境外网站、Google/YouTube、GitHub、通用工具 | 可绑定任意代理或自动选择策略组 |

**GitHub Raw 订阅地址：**

```text
https://raw.githubusercontent.com/linjiayinchn/LoonRules/main/subscriptions/US.list
https://raw.githubusercontent.com/linjiayinchn/LoonRules/main/subscriptions/Crypto.list
https://raw.githubusercontent.com/linjiayinchn/LoonRules/main/subscriptions/Direct.list
https://raw.githubusercontent.com/linjiayinchn/LoonRules/main/subscriptions/Overseas.list
```

在 Loon 中为各远程规则分别选择策略即可。举例：AI/媒体、数字资产和普通境外网站可以使用三个不同策略组，也可以选择相同策略；**GitHub 不指定具体的节点、国家、测速组名称或者 FINAL 策略**。

### 分流逻辑 / Rule order

建议根据自身需要把更明确的类别排在较宽泛的类别前面。常见排列为：

```text
US       -> [自选策略]
Crypto   -> [自选策略]
Overseas -> [自选策略]
Direct   -> DIRECT
# 可选：GEOIP,CN,DIRECT,no-resolve
FINAL    -> [独立决定：DIRECT / 代理 / 其他]
```

- **Overseas 不是 FINAL。** 只处理命中其规则的流量；未命中请求由后续本地规则或 FINAL 决定。
- **Overseas 通常建议排在 Direct 前面。** China 来源含 `DOMAIN-SUFFIX,cn`，否则如 `google.cn`、`googleapis.cn` 这类明确列入 Overseas 的例外会先被直连。
- US 和 Crypto 等专项规则仍应排在 Overseas 前面。构建器还会从 Overseas 中移除与 Direct **完全相同**的规则，减少 Apple / 国内服务的直接冲突；其他父子域名或关键词重叠仍需在 Loon 中核查。
- `GEOIP,CN,DIRECT,no-resolve` 是可选的本地 IP 归属规则，不是本仓库必需的订阅。若 `FINAL=DIRECT`，其作用可能主要是提前匹配和记录，而非改变路由结果。
- `DOMAIN-SUFFIX` 覆盖域名及其子域名；尽量使用具体服务域名，不对所有第三方 CDN、验证码、云存储或支付网关进行一刀切分流。
- Loon 分流规则与 HTTPS MitM 是不同机制。**银行、支付、钱包等敏感服务不应默认加入不受信任的 MitM 解密范围**。

## 仓库结构 / Repository layout

```text
subscriptions/       发布给 Loon 的四份最终规则（自动生成，勿手工改）
sources/             可维护的分类源文件、补充域名
  US_AI.list         AI 主域名、登录、接口、静态资源等
  US_Finance.list    国际财经、宏观研究与主流媒体
  Crypto.list        数字资产服务
  Direct_Custom.list 大陆银行、支付、常用服务、特定 SDK 补充
  Overseas_Utility.list  通用境外工具和 Google 生态
  Overseas_Custom.list   GitHub 等补充
scripts/             合并、校验和生成规则的代码
  build_rules.py
.github/workflows/   GitHub Actions 定时与变更触发器
  update-rules.yml
plugins/             可选插件，与网站分流订阅独立
  Device_Loopback.plugin
rules/               迁移期的旧订阅地址（兼容层）
README.md
```

- 国内与 Apple 基础规则来自 [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) 的 China、China_Domain、Apple、Apple_Domain。
- 一般境外基础规则来自同项目的 Proxy、Proxy_Domain；补充的 AI、媒体和常用服务域名保存在本仓库的 `sources/`。
- `scripts/build_rules.py` 将上游 DOMAIN-SET 格式转换为 Loon classical 规则，合并、去除完全重复项并校验关键域名。
- 所有来源成功读取并通过校验后才写入成品；下载失败或异常缩减会终止生成，以降低生成空白或不完整规则的风险。
- `rules/` 只为**尚未迁移至新地址**的客户端保留。新配置不应继续订阅这些旧文件；新生成器仍维护旧 `China.list` 与 `Crypto.list`，旧 `AI.list`、`US_Media_Finance.list`、`Utility.list` 已冻结。

## 更新机制 / Automation

`update-rules.yml` 默认每天 **00:17 UTC（北京时间 08:17）**运行，并支持 GitHub Actions 手动触发。修改 `sources/` 或生成脚本也会触发重新构建。

`subscriptions/` 仅在内容变化时提交新版本。定时任务可能延迟；在 Loon 中刷新订阅仅下载 GitHub 已发布的文件，不会实时触发上游重建。

**维护步骤：** 找到 `sources/` 中匹配业务的分类文件 → 追加经核实的 `DOMAIN` 或 `DOMAIN-SUFFIX` 规则 → 提交 → 查看 Actions 运行结果 → 在 Loon 中更新对应订阅。无需直接修改 `subscriptions/`。

## 维护原则 / Scope and safety

1. 优先采用服务商官方文档、实际连接日志或可信的公开规则源。主域名不等于全部应用接口；必要时补充认证、上传、内容分发和 WebSocket 主机。
2. 不把大型共享基础设施域名（如整个 `cloudfront.net`、`amazonaws.com`、`googleapis.com`）强制归入某一服务。需要补充时优先使用 **DOMAIN 精确主机匹配**。
3. 不以广告域名、营销用途域名的存在推断其适用于所有用户；需要时通过请求记录校验。
4. 国内银行网址采用公开机构信息、官方公告与 [domain-list-community/category-bank-cn](https://github.com/v2fly/domain-list-community/blob/master/data/category-bank-cn) 等资料交叉核对。规则中的域名仅是路由匹配，不是防钓鱼白名单。
5. 保留原始规则来源标注，尊重上游许可证。分流规则不能突破网站所在地、账号或服务的法律与平台限制。

### 部分参考资料

- [OpenAI — ChatGPT 网络访问与第三方辅助域名](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)
- [Google — Gemini 应用防火墙设置](https://knowledge.workspace.google.com/admin/generative-ai/gemini-app/gemini-app-firewall-settings)
- [Cursor — Network Configuration](https://cursor.com/docs/enterprise/network-configuration)
- [blackmatrix7 — ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)
- [v2fly — category-bank-cn](https://github.com/v2fly/domain-list-community/blob/master/data/category-bank-cn)

## 可选插件 / Optional plugin

`plugins/Device_Loopback.plugin` 仅用于有相关需求的 iOS 本地开发回环场景（如 LocalDevVPN 兼容性实验）；**四份规则订阅不会自动启用它**。无需此功能的使用者不必安装。

本项目不提供或分发代理节点、账户凭证及证书私钥。
