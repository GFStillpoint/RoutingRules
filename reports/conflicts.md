# Rule conflicts / 规则冲突报告

Generated / 检测时间: `2026-11-25T08:26:08+00:00`

[JSON data / 结构化数据](conflicts.json)

Specialized rules (US, Crypto) take precedence over exact duplicates in general rules (Overseas, Direct). Within each tier, rule priority is chosen in the client. Structural overlaps are retained. / 专项规则优先于基础规则中的完全重复项；同层级优先级由客户端决定，匹配范围重叠仅报告。

## Rule counts / 规则数量

| Category / 分类 | Before / 处理前 | After / 处理后 |
| --- | ---: | ---: |
| US | 1106 | 1106 |
| Crypto | 375 | 375 |
| Overseas | 7017 | 6810 |
| Direct | 5390 | 5387 |

## Removed exact duplicates / 已去重 (210)

| Rule / 规则 | Kept in / 保留于 | Removed from / 移除于 |
| --- | --- | --- |
| DOMAIN-KEYWORD,1e100 | US | Overseas |
| DOMAIN-KEYWORD,blogspot | US | Overseas |
| DOMAIN-KEYWORD,gmail | US | Overseas |
| DOMAIN-KEYWORD,google | US | Overseas |
| DOMAIN-KEYWORD,youtube | US | Overseas |
| DOMAIN-SUFFIX,9news.com.au | US | Overseas |
| DOMAIN-SUFFIX,aave.com | Crypto | Overseas |
| DOMAIN-SUFFIX,abc.net.au | US | Overseas |
| DOMAIN-SUFFIX,abc.xyz | US | Overseas |
| DOMAIN-SUFFIX,admob.com | US | Overseas |
| DOMAIN-SUFFIX,adsense.com | US | Overseas |
| DOMAIN-SUFFIX,afr.com | US | Overseas |
| DOMAIN-SUFFIX,aljazeera.com | US | Overseas |
| DOMAIN-SUFFIX,aljazeera.net | US | Overseas |
| DOMAIN-SUFFIX,android.com | US | Overseas |
| DOMAIN-SUFFIX,androidify.com | US | Overseas |
| DOMAIN-SUFFIX,androidtv.com | US | Overseas |
| DOMAIN-SUFFIX,ap.org | US | Overseas |
| DOMAIN-SUFFIX,app-measurement.net | US | Overseas |
| DOMAIN-SUFFIX,appspot.com | US | Overseas |
| DOMAIN-SUFFIX,arstechnica.net | US | Overseas |
| DOMAIN-SUFFIX,asiaone.com | US | Overseas |
| DOMAIN-SUFFIX,axios.com | US | Overseas |
| DOMAIN-SUFFIX,bangkokpost.com | US | Overseas |
| DOMAIN-SUFFIX,bbc.co.uk | US | Overseas |
| DOMAIN-SUFFIX,bbc.com | US | Overseas |
| DOMAIN-SUFFIX,bbci.co.uk | US | Overseas |
| DOMAIN-SUFFIX,big.one | Crypto | Overseas |
| DOMAIN-SUFFIX,binance.com | Crypto | Overseas |
| DOMAIN-SUFFIX,binance.us | Crypto | Overseas |
| DOMAIN-SUFFIX,bitfinex.com | Crypto | Overseas |
| DOMAIN-SUFFIX,bitget.com | Crypto | Overseas |
| DOMAIN-SUFFIX,bithumb.com | Crypto | Overseas |
| DOMAIN-SUFFIX,blogblog.com | US | Overseas |
| DOMAIN-SUFFIX,blogger.com | US | Overseas |
| DOMAIN-SUFFIX,bloomberg.com | US | Overseas |
| DOMAIN-SUFFIX,brookings.edu | US | Overseas |
| DOMAIN-SUFFIX,businessinsider.com | US | Overseas |
| DOMAIN-SUFFIX,bwbx.io | US | Overseas |
| DOMAIN-SUFFIX,bybit.com | Crypto | Overseas |
| DOMAIN-SUFFIX,cbc.ca | US | Overseas |
| DOMAIN-SUFFIX,cbsnews.com | US | Overseas |
| DOMAIN-SUFFIX,cerebras.ai | US | Overseas |
| DOMAIN-SUFFIX,cex.io | Crypto | Overseas |
| DOMAIN-SUFFIX,channelnewsasia.com | US | Overseas |
| DOMAIN-SUFFIX,character.ai | US | Overseas |
| DOMAIN-SUFFIX,chat.com | US | Overseas |
| DOMAIN-SUFFIX,chosun.com | US | Overseas |
| DOMAIN-SUFFIX,chrome.com | US | Overseas |
| DOMAIN-SUFFIX,chromecast.com | US | Overseas |
| DOMAIN-SUFFIX,chromeexperiments.com | US | Overseas |
| DOMAIN-SUFFIX,chromestatus.com | US | Overseas |
| DOMAIN-SUFFIX,chromium.org | US | Overseas |
| DOMAIN-SUFFIX,civitai.com | US | Overseas |
| DOMAIN-SUFFIX,claude.com | US | Overseas |
| DOMAIN-SUFFIX,cloudfunctions.net | US | Overseas |
| DOMAIN-SUFFIX,cmegroup.com | US | Overseas |
| DOMAIN-SUFFIX,cnet.com | US | Overseas |
| DOMAIN-SUFFIX,cnn.com | US | Overseas |
| DOMAIN-SUFFIX,coinbase.com | Crypto | Overseas |
| DOMAIN-SUFFIX,coinex.com | Crypto | Overseas |
| DOMAIN-SUFFIX,coingecko.com | Crypto | Overseas |
| DOMAIN-SUFFIX,coinmarketcap.com | Crypto | Overseas |
| DOMAIN-SUFFIX,crbug.com | US | Overseas |
| DOMAIN-SUFFIX,crrev.com | US | Overseas |
| DOMAIN-SUFFIX,dailymail.co.uk | US | Overseas |
| DOMAIN-SUFFIX,deepmind.com | US | Overseas |
| DOMAIN-SUFFIX,docs.new | US | Overseas |
| DOMAIN-SUFFIX,dowjones.com | US | Overseas |
| DOMAIN-SUFFIX,dowjones.io | US | Overseas |
| DOMAIN-SUFFIX,dw.com | US | Overseas |
| DOMAIN-SUFFIX,dw.de | US | Overseas |
| DOMAIN-SUFFIX,economist.com | US | Overseas |
| DOMAIN-SUFFIX,elpais.com | US | Overseas |
| DOMAIN-SUFFIX,engadget.com | US | Overseas |
| DOMAIN-SUFFIX,etherscan.io | Crypto | Overseas |
| DOMAIN-SUFFIX,euronews.com | US | Overseas |
| DOMAIN-SUFFIX,faz.net | US | Overseas |
| DOMAIN-SUFFIX,fb.com | US | Overseas |
| DOMAIN-SUFFIX,fb.me | US | Overseas |
| DOMAIN-SUFFIX,fb.watch | US | Overseas |
| DOMAIN-SUFFIX,fbsbx.com | US | Overseas |
| DOMAIN-SUFFIX,feedburner.com | US | Overseas |
| DOMAIN-SUFFIX,firebaseio.com | US | Overseas |
| DOMAIN-SUFFIX,fish.audio | US | Overseas |
| DOMAIN-SUFFIX,focustaiwan.tw | US | Overseas |
| DOMAIN-SUFFIX,forbes.com | US | Overseas |
| DOMAIN-SUFFIX,foreignaffairs.com | US | Overseas |
| DOMAIN-SUFFIX,foreignpolicy.com | US | Overseas |
| DOMAIN-SUFFIX,ft.com | US | Overseas |
| DOMAIN-SUFFIX,g.co | US | Overseas |
| DOMAIN-SUFFIX,gate.com | Crypto | Overseas |
| DOMAIN-SUFFIX,gate.io | Crypto | Overseas |
| DOMAIN-SUFFIX,gcr.io | US | Overseas |
| DOMAIN-SUFFIX,ggpht.com | US | Overseas |
| DOMAIN-SUFFIX,gmgn.ai | Crypto | Overseas |
| DOMAIN-SUFFIX,golang.org | US | Overseas |
| DOMAIN-SUFFIX,goo.gl | US | Overseas |
| DOMAIN-SUFFIX,grok.com | US | Overseas |
| DOMAIN-SUFFIX,gstatic.com | US | Overseas |
| DOMAIN-SUFFIX,gvt0.com | US | Overseas |
| DOMAIN-SUFFIX,gvt1.com | US | Overseas |
| DOMAIN-SUFFIX,gvt3.com | US | Overseas |
| DOMAIN-SUFFIX,hitbtc.com | Crypto | Overseas |
| DOMAIN-SUFFIX,htx.com | Crypto | Overseas |
| DOMAIN-SUFFIX,huggingface.co | US | Overseas |
| DOMAIN-SUFFIX,imf.org | US | Direct |
| DOMAIN-SUFFIX,independent.co.uk | US | Overseas |
| DOMAIN-SUFFIX,infura.io | Crypto | Overseas |
| DOMAIN-SUFFIX,investing.com | US | Overseas |
| DOMAIN-SUFFIX,jan.ai | US | Overseas |
| DOMAIN-SUFFIX,japantimes.co.jp | US | Overseas |
| DOMAIN-SUFFIX,jiji.com | US | Overseas |
| DOMAIN-SUFFIX,keyhole.com | US | Overseas |
| DOMAIN-SUFFIX,kraken.com | Crypto | Overseas |
| DOMAIN-SUFFIX,kucoin.com | Crypto | Overseas |
| DOMAIN-SUFFIX,ledger.com | Crypto | Overseas |
| DOMAIN-SUFFIX,lemonde.fr | US | Overseas |
| DOMAIN-SUFFIX,leonardo.ai | US | Overseas |
| DOMAIN-SUFFIX,m.me | US | Overseas |
| DOMAIN-SUFFIX,manus.im | US | Overseas |
| DOMAIN-SUFFIX,marketwatch.com | US | Overseas |
| DOMAIN-SUFFIX,material.io | US | Overseas |
| DOMAIN-SUFFIX,messenger.com | US | Overseas |
| DOMAIN-SUFFIX,meta.ai | US | Overseas |
| DOMAIN-SUFFIX,meta.com | US | Overseas |
| DOMAIN-SUFFIX,metaaivm.com | US | Overseas |
| DOMAIN-SUFFIX,metamask.io | Crypto | Overseas |
| DOMAIN-SUFFIX,mistral.ai | US | Overseas |
| DOMAIN-SUFFIX,msn.com | US | Overseas |
| DOMAIN-SUFFIX,muse.ai | US | Overseas |
| DOMAIN-SUFFIX,nationthailand.com | US | Overseas |
| DOMAIN-SUFFIX,nature.com | US | Direct |
| DOMAIN-SUFFIX,nbcnews.com | US | Overseas |
| DOMAIN-SUFFIX,newsweek.com | US | Overseas |
| DOMAIN-SUFFIX,newyorker.com | US | Overseas |
| DOMAIN-SUFFIX,nikkei.com | US | Overseas |
| DOMAIN-SUFFIX,nyt.com | US | Overseas |
| DOMAIN-SUFFIX,nytco.com | US | Overseas |
| DOMAIN-SUFFIX,nytimes.com | US | Overseas |
| DOMAIN-SUFFIX,nytimg.com | US | Overseas |
| DOMAIN-SUFFIX,oculus.com | US | Overseas |
| DOMAIN-SUFFIX,oculuscdn.com | US | Overseas |
| DOMAIN-SUFFIX,oklink.com | Crypto | Overseas |
| DOMAIN-SUFFIX,okx.com | Crypto | Overseas |
| DOMAIN-SUFFIX,opensea.io | Crypto | Overseas |
| DOMAIN-SUFFIX,page.link | US | Overseas |
| DOMAIN-SUFFIX,pancakeswap.finance | Crypto | Overseas |
| DOMAIN-SUFFIX,pbs.org | US | Overseas |
| DOMAIN-SUFFIX,perplexity.ai | US | Overseas |
| DOMAIN-SUFFIX,plus.codes | US | Overseas |
| DOMAIN-SUFFIX,poe.com | US | Overseas |
| DOMAIN-SUFFIX,poloniex.com | Crypto | Overseas |
| DOMAIN-SUFFIX,polymarket.com | Crypto | Overseas |
| DOMAIN-SUFFIX,recaptcha.net | US | Overseas |
| DOMAIN-SUFFIX,restofworld.org | US | Overseas |
| DOMAIN-SUFFIX,reuters.com | US | Overseas |
| DOMAIN-SUFFIX,reutersmedia.net | US | Overseas |
| DOMAIN-SUFFIX,rfi.fr | US | Overseas |
| DOMAIN-SUFFIX,sbs.com.au | US | Overseas |
| DOMAIN-SUFFIX,scmp.com | US | Overseas |
| DOMAIN-SUFFIX,sheets.new | US | Overseas |
| DOMAIN-SUFFIX,slides.new | US | Overseas |
| DOMAIN-SUFFIX,smh.com.au | US | Overseas |
| DOMAIN-SUFFIX,snapseed.com | US | Overseas |
| DOMAIN-SUFFIX,solana.com | Crypto | Overseas |
| DOMAIN-SUFFIX,solscan.io | Crypto | Overseas |
| DOMAIN-SUFFIX,sourcegraph.com | US | Overseas |
| DOMAIN-SUFFIX,straitstimes.com | US | Overseas |
| DOMAIN-SUFFIX,suno.com | US | Overseas |
| DOMAIN-SUFFIX,swissinfo.ch | US | Overseas |
| DOMAIN-SUFFIX,taipeitimes.com | US | Overseas |
| DOMAIN-SUFFIX,techcrunch.com | US | Overseas |
| DOMAIN-SUFFIX,telegraph.co.uk | US | Overseas |
| DOMAIN-SUFFIX,tensorflow.org | US | Overseas |
| DOMAIN-SUFFIX,tfhub.dev | US | Overseas |
| DOMAIN-SUFFIX,theatlantic.com | US | Overseas |
| DOMAIN-SUFFIX,theaustralian.com.au | US | Overseas |
| DOMAIN-SUFFIX,theconversation.com | US | Overseas |
| DOMAIN-SUFFIX,theguardian.com | US | Overseas |
| DOMAIN-SUFFIX,theintercept.com | US | Overseas |
| DOMAIN-SUFFIX,theverge.com | US | Overseas |
| DOMAIN-SUFFIX,threads.com | US | Overseas |
| DOMAIN-SUFFIX,threads.net | US | Overseas |
| DOMAIN-SUFFIX,time.com | US | Overseas |
| DOMAIN-SUFFIX,tradingview.com | Crypto | Overseas |
| DOMAIN-SUFFIX,tronscan.org | Crypto | Overseas |
| DOMAIN-SUFFIX,trustwallet.com | Crypto | Overseas |
| DOMAIN-SUFFIX,uniswap.org | Crypto | Overseas |
| DOMAIN-SUFFIX,upbit.com | Crypto | Overseas |
| DOMAIN-SUFFIX,vox-cdn.com | US | Overseas |
| DOMAIN-SUFFIX,walletconnect.com | Crypto | Overseas |
| DOMAIN-SUFFIX,walletconnect.org | Crypto | Overseas |
| DOMAIN-SUFFIX,washingtonpost.com | US | Overseas |
| DOMAIN-SUFFIX,waymo.com | US | Overseas |
| DOMAIN-SUFFIX,web.dev | US | Overseas |
| DOMAIN-SUFFIX,worldbank.org | US | Direct |
| DOMAIN-SUFFIX,wsj.com | US | Overseas |
| DOMAIN-SUFFIX,wsj.net | US | Overseas |
| DOMAIN-SUFFIX,x.ai | US | Overseas |
| DOMAIN-SUFFIX,x.company | US | Overseas |
| DOMAIN-SUFFIX,xt.com | Crypto | Overseas |
| DOMAIN-SUFFIX,yahoo.com | US | Overseas |
| DOMAIN-SUFFIX,yimg.com | US | Overseas |
| DOMAIN-SUFFIX,yomiuri.co.jp | US | Overseas |
| DOMAIN-SUFFIX,you.com | US | Overseas |
| DOMAIN-SUFFIX,youtu.be | US | Overseas |
| DOMAIN-SUFFIX,yt.be | US | Overseas |
| DOMAIN-SUFFIX,ytimg.com | US | Overseas |
| DOMAIN-SUFFIX,zerohedge.com | US | Overseas |

## Retained peer duplicates / 同层重复 (8)

| Rule / 规则 | Categories / 分类 |
| --- | --- |
| DOMAIN-SUFFIX,apple-dns.net | Overseas, Direct |
| DOMAIN-SUFFIX,appsto.re | Overseas, Direct |
| DOMAIN-SUFFIX,crashlytics.com | Overseas, Direct |
| DOMAIN-SUFFIX,digicert.com | Overseas, Direct |
| DOMAIN-SUFFIX,itun.es | Overseas, Direct |
| DOMAIN-SUFFIX,shazam.com | Overseas, Direct |
| USER-AGENT,com.apple.trustd* | Overseas, Direct |
| USER-AGENT,hearthstone* | Overseas, Direct |

## Structural overlaps / 匹配范围重叠 (96)

Detected domain suffix relationships, explicit keyword containment and overlapping IP networks. These are structural checks, not exhaustive runtime matches. / 检测域名后缀、明确的关键词包含关系及 IP 网段重叠；不等同于实际流量匹配的穷尽检测。

<details>
<summary>View all overlaps / 查看全部重叠</summary>

| Type / 类型 | Category A | Rule A | Category B | Rule B |
| --- | --- | --- | --- | --- |
| domain_suffix | US | DOMAIN-SUFFIX,coindesk.com | Crypto | DOMAIN,data.coindesk.com |
| domain_keyword | US | DOMAIN-SUFFIX,cdninstagram.com | Overseas | DOMAIN-KEYWORD,instagram |
| domain_keyword | US | DOMAIN-SUFFIX,facebook.com | Overseas | DOMAIN-KEYWORD,facebook |
| domain_keyword | US | DOMAIN-SUFFIX,facebook.net | Overseas | DOMAIN-KEYWORD,facebook |
| domain_keyword | US | DOMAIN-SUFFIX,fbcdn.net | Overseas | DOMAIN-KEYWORD,fbcdn |
| domain_keyword | US | DOMAIN-SUFFIX,instagram.com | Overseas | DOMAIN-KEYWORD,instagram |
| domain_keyword | US | DOMAIN-SUFFIX,whatsapp.com | Overseas | DOMAIN-KEYWORD,whatsapp |
| domain_keyword | US | DOMAIN-SUFFIX,whatsapp.net | Overseas | DOMAIN-KEYWORD,whatsapp |
| domain_suffix | US | DOMAIN,agent-stores.s3.amazonaws.com | Overseas | DOMAIN-SUFFIX,amazonaws.com |
| domain_suffix | US | DOMAIN,agent-stores.s3.us-east-1.amazonaws.com | Overseas | DOMAIN-SUFFIX,amazonaws.com |
| domain_suffix | US | DOMAIN,anysphere-binaries.s3.us-east-1.amazonaws.com | Overseas | DOMAIN-SUFFIX,amazonaws.com |
| domain_suffix | US | DOMAIN,koreajoongangdaily.joins.com | Overseas | DOMAIN-SUFFIX,joins.com |
| domain_suffix | US | DOMAIN-SUFFIX,abcnews.go.com | Overseas | DOMAIN-SUFFIX,go.com |
| domain_suffix | US | DOMAIN-SUFFIX,copilot-proxy.githubusercontent.com | Overseas | DOMAIN-SUFFIX,githubusercontent.com |
| domain_suffix | US | DOMAIN-SUFFIX,copilot.microsoft.com | Overseas | DOMAIN-SUFFIX,microsoft.com |
| domain_suffix | US | DOMAIN-SUFFIX,designer.microsoft.com | Overseas | DOMAIN-SUFFIX,microsoft.com |
| domain_suffix | US | DOMAIN-SUFFIX,ecb.europa.eu | Overseas | DOMAIN-SUFFIX,europa.eu |
| domain_suffix | US | DOMAIN-SUFFIX,news.ycombinator.com | Overseas | DOMAIN-SUFFIX,ycombinator.com |
| domain_suffix | US | DOMAIN-SUFFIX,oaiusercontent.com | Overseas | DOMAIN-SUFFIX,files.oaiusercontent.com |
| domain_suffix | US | DOMAIN-SUFFIX,openai.com | Overseas | DOMAIN-SUFFIX,chat.openai.com |
| domain_suffix | US | DOMAIN-SUFFIX,openaiapi-site.azureedge.net | Overseas | DOMAIN-SUFFIX,azureedge.net |
| domain_suffix | US | DOMAIN-SUFFIX,production-openaicom-storage.azureedge.net | Overseas | DOMAIN-SUFFIX,azureedge.net |
| domain_keyword | US | DOMAIN,substrate.svc.cloud.microsoft | Direct | DOMAIN-KEYWORD,microsoft |
| domain_keyword | US | DOMAIN-SUFFIX,copilot.cloud.microsoft | Direct | DOMAIN-KEYWORD,microsoft |
| domain_keyword | US | DOMAIN-SUFFIX,copilot.microsoft.com | Direct | DOMAIN-KEYWORD,microsoft |
| domain_keyword | US | DOMAIN-SUFFIX,designer.microsoft.com | Direct | DOMAIN-KEYWORD,microsoft |
| domain_suffix | US | DOMAIN,cursor.blob.core.windows.net | Direct | DOMAIN-SUFFIX,windows.net |
| domain_suffix | US | DOMAIN,substrate.office.com | Direct | DOMAIN-SUFFIX,office.com |
| domain_suffix | US | DOMAIN-SUFFIX,ggpht.cn | Direct | DOMAIN-SUFFIX,cn |
| domain_suffix | US | DOMAIN-SUFFIX,google.cn | Direct | DOMAIN-SUFFIX,cn |
| domain_suffix | US | DOMAIN-SUFFIX,google.ms | Direct | DOMAIN-SUFFIX,ms |
| domain_suffix | US | DOMAIN-SUFFIX,googleapis.cn | Direct | DOMAIN-SUFFIX,cn |
| domain_suffix | US | DOMAIN-SUFFIX,googlecnapps.cn | Direct | DOMAIN-SUFFIX,cn |
| domain_suffix | US | DOMAIN-SUFFIX,gstatic.cn | Direct | DOMAIN-SUFFIX,cn |
| domain_suffix | US | DOMAIN-SUFFIX,lat.ms | Direct | DOMAIN-SUFFIX,ms |
| domain_suffix | US | DOMAIN-SUFFIX,openaiassets.z19.web.core.windows.net | Direct | DOMAIN-SUFFIX,windows.net |
| domain_suffix | US | DOMAIN-SUFFIX,openaicomproductionae4b.blob.core.windows.net | Direct | DOMAIN-SUFFIX,windows.net |
| domain_suffix | Crypto | DOMAIN,binance-docs.github.io | Overseas | DOMAIN-SUFFIX,github.io |
| domain_suffix | Crypto | DOMAIN,bingx-api.github.io | Overseas | DOMAIN-SUFFIX,github.io |
| domain_suffix | Crypto | DOMAIN,bybit-exchange.github.io | Overseas | DOMAIN-SUFFIX,github.io |
| domain_suffix | Crypto | DOMAIN,coins-docs.github.io | Overseas | DOMAIN-SUFFIX,github.io |
| domain_suffix | Crypto | DOMAIN,huobiapi.github.io | Overseas | DOMAIN-SUFFIX,github.io |
| domain_suffix | Crypto | DOMAIN,hyperliquid.gitbook.io | Overseas | DOMAIN-SUFFIX,gitbook.io |
| domain_suffix | Crypto | DOMAIN,phemex-docs.github.io | Overseas | DOMAIN-SUFFIX,github.io |
| domain_keyword | Overseas | DOMAIN,login.microsoftonline.com | Direct | DOMAIN-KEYWORD,microsoft |
| domain_keyword | Overseas | DOMAIN,testflight.apple.com | Direct | DOMAIN-KEYWORD,testflight |
| domain_keyword | Overseas | DOMAIN-KEYWORD,porn | Direct | DOMAIN-SUFFIX,empornium.me |
| domain_keyword | Overseas | DOMAIN-SUFFIX,baidu.jp | Direct | DOMAIN-KEYWORD,baidu |
| domain_keyword | Overseas | DOMAIN-SUFFIX,microsoft-falcon.io | Direct | DOMAIN-KEYWORD,microsoft |
| domain_keyword | Overseas | DOMAIN-SUFFIX,microsoft.com | Direct | DOMAIN-KEYWORD,microsoft |
| domain_keyword | Overseas | DOMAIN-SUFFIX,microsoftapp.net | Direct | DOMAIN-KEYWORD,microsoft |
| domain_keyword | Overseas | DOMAIN-SUFFIX,microsoftpersonalcontent.com | Direct | DOMAIN-KEYWORD,microsoft |
| domain_keyword | Overseas | DOMAIN-SUFFIX,microsofttranslator.com | Direct | DOMAIN-KEYWORD,microsoft |
| domain_suffix | Overseas | DOMAIN,cloud.oracle.com | Direct | DOMAIN-SUFFIX,oracle.com |
| domain_suffix | Overseas | DOMAIN,cvws.icloud-content.com | Direct | DOMAIN-SUFFIX,icloud-content.com |
| domain_suffix | Overseas | DOMAIN,developer.apple.com | Direct | DOMAIN-SUFFIX,apple.com |
| domain_suffix | Overseas | DOMAIN,login.microsoftonline.com | Direct | DOMAIN-SUFFIX,microsoftonline.com |
| domain_suffix | Overseas | DOMAIN,testflight.apple.com | Direct | DOMAIN-SUFFIX,apple.com |
| domain_suffix | Overseas | DOMAIN-SUFFIX,akamaihd.net | Direct | DOMAIN,blzddist1-a.akamaihd.net |
| domain_suffix | Overseas | DOMAIN-SUFFIX,akamaihd.net | Direct | DOMAIN,origin-a.akamaihd.net |
| domain_suffix | Overseas | DOMAIN-SUFFIX,akamaihd.net | Direct | DOMAIN,steamcommunity-a.akamaihd.net |
| domain_suffix | Overseas | DOMAIN-SUFFIX,blobstore.apple.com | Direct | DOMAIN-SUFFIX,apple.com |
| domain_suffix | Overseas | DOMAIN-SUFFIX,bx.in.th | Direct | DOMAIN-SUFFIX,in.th |
| domain_suffix | Overseas | DOMAIN-SUFFIX,c.mi.com | Direct | DOMAIN-SUFFIX,mi.com |
| domain_suffix | Overseas | DOMAIN-SUFFIX,cdn.angruo.com | Direct | DOMAIN,cdn.angruo.com |
| domain_suffix | Overseas | DOMAIN-SUFFIX,content.office.net | Direct | DOMAIN-SUFFIX,office.net |
| domain_suffix | Overseas | DOMAIN-SUFFIX,crisp.chat | Direct | DOMAIN-SUFFIX,api.crisp.chat |
| domain_suffix | Overseas | DOMAIN-SUFFIX,edgekey.net | Direct | DOMAIN,lookup-api.apple.com.edgekey.net |
| domain_suffix | Overseas | DOMAIN-SUFFIX,edgekey.net | Direct | DOMAIN-SUFFIX,gsp4-cn.ls.apple.com.edgekey.net |
| domain_suffix | Overseas | DOMAIN-SUFFIX,edgekey.net | Direct | DOMAIN-SUFFIX,itunes.com.edgekey.net |
| domain_suffix | Overseas | DOMAIN-SUFFIX,edgekey.net | Direct | DOMAIN-SUFFIX,store.apple.com.edgekey.net |
| domain_suffix | Overseas | DOMAIN-SUFFIX,edgekey.net | Direct | DOMAIN-SUFFIX,www.apple.com.edgekey.net |
| domain_suffix | Overseas | DOMAIN-SUFFIX,edgesuite.net | Direct | DOMAIN-SUFFIX,appldnld.apple.com.edgesuite.net |
| domain_suffix | Overseas | DOMAIN-SUFFIX,edgesuite.net | Direct | DOMAIN-SUFFIX,ls.apple.com.edgesuite.net |
| domain_suffix | Overseas | DOMAIN-SUFFIX,futu.cn | Direct | DOMAIN-SUFFIX,cn |
| domain_suffix | Overseas | DOMAIN-SUFFIX,futubull.cn | Direct | DOMAIN-SUFFIX,cn |
| domain_suffix | Overseas | DOMAIN-SUFFIX,gfx.ms | Direct | DOMAIN-SUFFIX,ms |
| domain_suffix | Overseas | DOMAIN-SUFFIX,go.sony.com | Direct | DOMAIN-SUFFIX,sony.com |
| domain_suffix | Overseas | DOMAIN-SUFFIX,longportapp.cn | Direct | DOMAIN-SUFFIX,cn |
| domain_suffix | Overseas | DOMAIN-SUFFIX,microsoft.com | Direct | DOMAIN,download.microsoft.com |
| domain_suffix | Overseas | DOMAIN-SUFFIX,microsoft.com | Direct | DOMAIN,ntservicepack.microsoft.com |
| domain_suffix | Overseas | DOMAIN-SUFFIX,microsoft.com | Direct | DOMAIN-SUFFIX,dl.delivery.mp.microsoft.com |
| domain_suffix | Overseas | DOMAIN-SUFFIX,microsoft.com | Direct | DOMAIN-SUFFIX,update.microsoft.com |
| domain_suffix | Overseas | DOMAIN-SUFFIX,microsoft.com | Direct | DOMAIN-SUFFIX,windowsupdate.microsoft.com |
| domain_suffix | Overseas | DOMAIN-SUFFIX,nyti.ms | Direct | DOMAIN-SUFFIX,ms |
| domain_suffix | Overseas | DOMAIN-SUFFIX,openapi-quote.longbridge.cn | Direct | DOMAIN-SUFFIX,cn |
| domain_suffix | Overseas | DOMAIN-SUFFIX,openapi-trade.longbridge.cn | Direct | DOMAIN-SUFFIX,cn |
| domain_suffix | Overseas | DOMAIN-SUFFIX,openapi.longbridge.cn | Direct | DOMAIN-SUFFIX,cn |
| domain_suffix | Overseas | DOMAIN-SUFFIX,schwab.com.cn | Direct | DOMAIN-SUFFIX,cn |
| domain_suffix | Overseas | DOMAIN-SUFFIX,sfx.ms | Direct | DOMAIN-SUFFIX,ms |
| domain_suffix | Overseas | DOMAIN-SUFFIX,shortconn.im.qcloud.com | Direct | DOMAIN-SUFFIX,qcloud.com |
| domain_suffix | Overseas | DOMAIN-SUFFIX,sina.com.hk | Direct | DOMAIN-SUFFIX,adimages.sina.com.hk |
| domain_suffix | Overseas | DOMAIN-SUFFIX,sina.com.hk | Direct | DOMAIN-SUFFIX,oascentral.sina.com.hk |
| domain_suffix | Overseas | DOMAIN-SUFFIX,tigerbbs.cn | Direct | DOMAIN-SUFFIX,cn |
| domain_suffix | Overseas | DOMAIN-SUFFIX,zhijianfengyi.cn | Direct | DOMAIN-SUFFIX,cn |
| ip_network | Overseas | IP-CIDR,17.252.156.0/23,no-resolve | Direct | IP-CIDR,17.0.0.0/8,no-resolve |

</details>
