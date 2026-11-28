// Smart Selection 0.1.1 | RoutingRules | detection only
// Loon 3.5.1 (983)+. No policy writes, MitM, or credential collection.
function createSmartSelection(api) {
  "use strict";
  const VERSION="0.1.1", KEY="routingrules.smart-selection.v1", LOCK=KEY+".lease";
  const MB=1000000, H=3600000, BATCH=6, RUN_BYTES=16*MB, RUN_MS=155000;
  const now=api.now, own=(o,k)=>Object.prototype.hasOwnProperty.call(o,k);
  const unique=a=>Array.from(new Set(a));
  const validName=x=>typeof x==="string"&&x.trim().length>0&&x.length<=300;
  const builtIn=x=>/^(DIRECT|PROXY|REJECT(?:[-_].*)?|DROP|PASS)$/i.test(x.trim());
  const pseudo=x=>/剩余|到期|套餐|联系邮箱|导航网址|续费|流量重置|^Q群|^QQ群|官网地址/i.test(x);
  const day=t=>{const d=new Date(t);return [d.getFullYear(),String(d.getMonth()+1).padStart(2,"0"),String(d.getDate()).padStart(2,"0")].join("-");};
  const median=a=>{const b=a.slice().sort((x,y)=>x-y);return b.length?(b[Math.floor((b.length-1)/2)]+b[Math.ceil((b.length-1)/2)])/2:null;};
  const hash=s=>{let h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619);}return (h>>>0).toString(16);};
  const safeParse=x=>typeof x==="string"?JSON.parse(x):x;
  const format=x=>typeof x==="number"&&Number.isFinite(x)?x.toFixed(1):"—";
  const fresh=(s,t,age)=>s&&Number.isFinite(s.at)&&t>=s.at&&t-s.at<=age;
  function config() {
    const c=safeParse(api.config())||{};
    if(!Array.isArray(c.all_policy_groups)||!c.all_policy_groups.every(validName))throw Error("无法识别 all_policy_groups；请检查 Loon 版本");
    return c;
  }
  function options(args) {
    args=args&&typeof args==="object"?args:{};
    let budget=Number(args.dailyMB==null?200:args.dailyMB);
    if(![50,100,200,300].includes(budget))throw Error("不支持的每日预算");
    const groups=String(args.groups||"").split(/[;；\n]/).map(x=>x.trim()).filter(Boolean);
    return {budget:budget*MB,groups:unique(groups)};
  }
  function network(c){
    // Never persist SSID itself. An unidentified network is deliberately not trusted
    // as a stable network identity: history is short-lived and marked unverified.
    return typeof c.ssid==="string"&&c.ssid.trim()?{key:"wifi-"+hash(c.ssid),label:"Wi-Fi",known:true}:{key:"unknown",label:"网络未识别",known:false};
  }
  function newState(t) {return {v:1,day:day(t),charged:0,actual:0,records:{},last:null,cursor:0};}
  function load(){
    const raw=api.read(KEY);
    if(!raw)return newState(now());
    const s=safeParse(raw);
    if(!s||s.v!==1||typeof s.day!=="string"||!Number.isSafeInteger(s.charged)||s.charged<0||!Number.isSafeInteger(s.actual)||s.actual<0||!s.records||typeof s.records!=="object"||Array.isArray(s.records))throw Error("本地记录异常；为避免重复消耗预算，停止测速");
    // Do not reset after a backwards clock change.
    if(day(now())>s.day){s.day=day(now());s.charged=0;s.actual=0;}
    return s;
  }
  function save(s){if(api.write(KEY,JSON.stringify(s))!==true)throw Error("本地存储失败，停止测速");}
  function claim(){
    const old=api.read(LOCK);
    if(old){const x=safeParse(old);if(x&&x.until>now())return null;}
    const token=String(now())+"-"+String(api.random());
    if(api.write(LOCK,JSON.stringify({token,until:now()+240000}))!==true)throw Error("无法保存任务锁");
    const x=safeParse(api.read(LOCK));
    return x&&x.token===token?token:null;
  }
  function verifyLease(token){
    const x=safeParse(api.read(LOCK)||"null");
    if(!x||x.token!==token||x.until<=now())throw Error("任务锁已失效，停止测速");
  }
  function release(token){
    const x=safeParse(api.read(LOCK)||"null");
    if(x&&x.token===token)api.write(LOCK,JSON.stringify({token:"",until:0}));
  }
  function callbackCall(start,ms){
    return new Promise(resolve=>{
      let done=false;
      const timer=api.timer(()=>finish({watchdog:true}),ms);
      function finish(v){if(done)return;done=true;api.clear(timer);resolve(v);}
      try{start(finish);}catch(e){finish({error:"API 调用异常"});}
    });
  }
  async function discover(c,opts,context) {
    const all=unique(c.all_policy_groups), known=new Set(all);
    const requested=opts.groups.length?opts.groups:all;
    const scoped=context.group?requested.filter(x=>x===context.group):requested;
    if(context.group&&!scoped.length)throw Error("该策略组未纳入检测范围");
    const groups=[];
    const built=new Set(Array.isArray(c.all_buildin_nodes)?c.all_buildin_nodes:[]);
    // Flat leaf groups only in V0.1. Nested groups are not treated as individual nodes.
    for(const name of scoped){
      let g={name,nodes:[],selected:"",skipped:0,error:null};
      groups.push(g);
      if(!known.has(name)){g.error="策略组不存在";continue;}
      try{
        try{const selected=api.selected(name);g.selected=validName(selected)?selected:"";}catch(_){}
        const r=await callbackCall(cb=>api.members(name,x=>cb({value:x})),3500);
        if(r.watchdog||r.error)throw Error("候选节点读取超时或失败");
        const a=r.value===""||r.value==null?[]:safeParse(r.value);
        // Loon returns JSON arrays of {name,type} in actual clients.
        // Accept legacy name strings too; never probe typed non-node policies.
        if(!Array.isArray(a)){
          api.log(JSON.stringify({group:name,discovery:{array:false,kind:typeof a}}));
          throw Error("候选节点返回格式未识别");
        }
        const names=[], shape={strings:0,nodes:0,nonNodes:0,unknown:0};
        for(const item of a){
          if(validName(item)){shape.strings++;names.push(item);}
          else if(item&&typeof item==="object"&&validName(item.name)&&typeof item.type==="string"){
            if(item.type.toLowerCase()==="node"){shape.nodes++;names.push(item.name);}
            else shape.nonNodes++;
          }else shape.unknown++;
        }
        // Log only shape counts, not raw node descriptions or secrets.
        api.log(JSON.stringify({group:name,discovery:{total:a.length,...shape}}));
        if(a.length&&shape.strings+shape.nodes+shape.nonNodes===0)throw Error("候选节点条目格式未识别");
        g.nodes=unique(names.filter(x=>!known.has(x)&&!built.has(x)&&!builtIn(x)&&!pseudo(x)));
        g.skipped=a.length-g.nodes.length;
        if(context.node)g.nodes=g.nodes.filter(x=>x===context.node);
        if(!g.nodes.length)g.error="无可直接测速的叶子节点";
      }catch(e){g.error=e.message;}
    }
    return groups;
  }
  const recKey=(net,node)=>JSON.stringify([net.key,node]);
  function getRecord(s,net,node){
    const k=recKey(net,node);
    return own(s.records,k)?s.records[k]:null;
  }
  function record(s,net,node,result){
    const k=recKey(net,node), old=getRecord(s,net,node)||{samples:[],lastDownload:0,lastAttempt:0};
    const samples=(Array.isArray(old.samples)?old.samples:[]).filter(x=>fresh(x,now(),7*24*H)).slice(-7);
    samples.push(result);
    s.records[k]={samples,lastDownload:result.mbps!=null?result.at:old.lastDownload||0,lastAttempt:result.at};
  }
  function prune(s){
    for(const k of Object.keys(s.records)){const r=s.records[k];if(!r||!fresh({at:r.lastAttempt},now(),7*24*H))delete s.records[k];}
    const keys=Object.keys(s.records).sort((a,b)=>s.records[b].lastAttempt-s.records[a].lastAttempt);
    for(const k of keys.slice(0,Math.max(0,keys.length-600))){ // delete oldest only
      // no-op here; actual bound below
    }
    for(const k of keys.slice(600))delete s.records[k];
  }
  function quality(r,net,t){
    if(!r||!Array.isArray(r.samples))return {status:"待测",score:null};
    const age=net.known?24*H:2*H;
    const samples=r.samples.filter(x=>fresh(x,t,age));
    if(!samples.length)return {status:"过期",score:null};
    const latest=samples[samples.length-1];
    const lat=samples.flatMap(x=>Array.isArray(x.lat)?x.lat:[]);
    const down=samples.filter(x=>Number.isFinite(x.mbps));
    const success=100*samples.reduce((a,x)=>a+x.ok,0)/Math.max(1,samples.reduce((a,x)=>a+x.attempts,0));
    const delay=median(lat), deviation=delay==null?null:median(lat.map(x=>Math.abs(x-delay)));
    let speed=null;
    if(down.length){let num=0,den=0;down.forEach((x,i)=>{const w=Math.pow(.65,down.length-1-i);num+=x.mbps*w;den+=w;});speed=num/den;}
    const q={status:"样本不足",score:null,delay,speed,success,deviation,samples:samples.length,last:latest.at,lastError:latest.error||null};
    if(latest.ok===0){q.status="最近连接失败";return q;}
    if(!latest.mbps||speed==null||delay==null){q.status="待有效下载";return q;}
    const v=100*Math.min(1,Math.log(1+speed)/Math.log(51)), l=100*Math.exp(-Math.max(0,delay-50)/350), j=100*Math.exp(-deviation/100);
    q.score=Math.round((.4*v+.2*l+.3*success+.1*j)*10)/10;
    q.status=latest.ok<latest.attempts?"部分失败":(!net.known||down.length<2?"初步":"已复测");
    return q;
  }
  function queue(groups,s,net){
    const valid=groups.filter(g=>g.nodes.length);
    if(!valid.length)return [];
    const current=unique(valid.map(g=>g.selected).filter(x=>valid.some(g=>g.nodes.includes(x))));
    // Round-robin group ordering across batches; at least one oldest candidate per group.
    const offset=(s.cursor||0)%valid.length;
    const ordered=valid.slice(offset).concat(valid.slice(0,offset));
    const oldest=g=>g.nodes.slice().sort((a,b)=>(getRecord(s,net,a)?.lastAttempt||0)-(getRecord(s,net,b)?.lastAttempt||0)||a.localeCompare(b));
    const lists=ordered.map(oldest);
    const urgent=ordered.map(g=>g.selected).filter(x=>current.includes(x)&&(!getRecord(s,net,x)||now()-getRecord(s,net,x).lastAttempt>=H));
    const first=lists.map(a=>a[0]);
    const merged=unique(first.concat(urgent));
    for(let i=1;i<Math.max(...lists.map(a=>a.length));i++)for(const a of lists)if(a[i]!==undefined&&!merged.includes(a[i]))merged.push(a[i]);
    return merged;
  }
  function reserve(s,opts,run,bytes,token){
    verifyLease(token);
    if(day(now())!==s.day||s.charged+bytes>opts.budget||run.charged+bytes>RUN_BYTES)return false;
    s.charged+=bytes;run.charged+=bytes;save(s);return true;
  }
  async function request(node,url,method,bytes,s,opts,run,token) {
    // Reserve requested payload plus a conservative per-request allowance.
    // This is an estimate, not a physical transport-layer byte counter.
    const allowance=bytes+16000;
    if(!reserve(s,opts,run,allowance,token))return {skipped:true};
    const start=now();
    const options={url,node,timeout:12000,"binary-mode":true,"auto-redirect":false,"auto-cookie":false,insecure:false,headers:{"Cache-Control":"no-cache, no-store","Pragma":"no-cache","Accept-Encoding":"identity"}};
    const r=await callbackCall(cb=>api.request(method,options,(err,res,data)=>cb({err,res,data})),14500);
    const elapsed=Math.max(1,now()-start);
    let n=0;
    if(r.data&&typeof r.data.byteLength==="number")n=r.data.byteLength;
    else if(typeof r.data==="string")n=r.data.length;
    if(!Number.isSafeInteger(n)||n<0)n=0;
    // Unexpected oversized responses are charged retrospectively, then halt the run.
    if(n>bytes){const extra=Math.max(0,n-allowance);s.charged+=extra;run.charged+=extra;}
    s.actual+=n;run.actual+=n;verifyLease(token);save(s);
    if(r.watchdog){run.stop=true;return {ok:false,error:"回调超时，停止本批",elapsed,n};}
    if(n>allowance){run.stop=true;return {ok:false,error:"响应超过预期，停止本批",elapsed,n};}
    if(r.error||r.err||!r.res)return {ok:false,error:"连接失败或超时",elapsed,n};
    const status=Number(r.res.status??r.res.statusCode);
    const headers=r.res.headers||{};
    const header=name=>{const k=Object.keys(headers).find(x=>x.toLowerCase()===name);return k?String(headers[k]):"";};
    return {ok:true,status,elapsed,n,contentType:header("content-type"),encoding:header("content-encoding"),binary:r.data!=null&&typeof r.data!=="string"&&typeof r.data.byteLength==="number"};
  }
  async function probe(node,s,opts,run,token){
    const p={at:now(),lat:[],ok:0,attempts:0,mbps:null,bytes:0,error:null,targets:[]};
    const can=()=>!run.stop&&now()-run.start<RUN_MS-16000;
    for(const [url,status] of [["https://www.gstatic.com/generate_204",204],["https://www.apple.com/library/test/success.html",200]]){
      if(!can())break;
      const r=await request(node,url,"head",0,s,opts,run,token);
      if(r.skipped)break;
      p.attempts++;
      const pass=r.ok&&r.status===status;
      p.targets.push({target:status===204?"Google":"Apple",ok:pass,status:r.status||null,ms:r.elapsed});
      if(pass){p.ok++;p.lat.push(r.elapsed);}else p.error=r.error||"轻量目标状态异常";
    }
    // Even when both light targets fail, try the independent download target
    // to distinguish target-specific failures from a dead route.
    for(const bytes of [2*MB,5*MB]){
      if(!can())break;
      const r=await request(node,"https://speed.cloudflare.com/__down?bytes="+bytes+"&rr="+String(now()),"get",bytes,s,opts,run,token);
      if(r.skipped)break;
      p.attempts++;
      const pass=r.ok&&r.status===200&&r.binary&&r.n===bytes&&!/html|json|text\/plain/i.test(r.contentType)&&(!r.encoding||r.encoding==="identity");
      p.targets.push({target:"Cloudflare",ok:pass,status:r.status||null,ms:r.elapsed,bytes:r.n,expected:bytes});
      if(!pass){p.error=r.error||"下载响应校验失败";break;}
      p.ok++;p.bytes+=r.n;p.mbps=8*r.n/(r.elapsed*1000);
      if(r.elapsed>=300||bytes===5*MB)break;
    }
    p.at=now();
    return p;
  }
  function buildReport(groups,s,net,opts,run){
    return {version:VERSION,mode:"只检测，不切换",network:net.label,networkIdentified:net.known,
      day:s.day,budgetMB:opts.budget/MB,chargedMB:Math.round(s.charged/MB*100)/100,receivedMB:Math.round(s.actual/MB*100)/100,
      batch:run?{tested:run.tested,chargedMB:Math.round(run.charged/MB*100)/100,stop:run.stop}:null,
      groups:groups.map(g=>{const rows=g.nodes.map(node=>({node,current:node===g.selected,...quality(getRecord(s,net,node),net,now())})).sort((a,b)=>(b.score??-1)-(a.score??-1)||a.node.localeCompare(b.node));
        return {name:g.name,selected:g.selected,count:g.nodes.length,skipped:g.skipped,error:g.error,ranked:rows.filter(r=>r.score!=null).length,rows};})};
  }
  function summary(r){
    const lines=[`Smart Selection ${r.version} · 只检测`,`${r.network}｜今日预算 ${r.chargedMB}/${r.budgetMB} MB（预扣估算）`];
    if(r.batch)lines.push(`本轮检测 ${r.batch.tested.length} 个节点；${r.batch.chargedMB} MB${r.batch.stop?"；本批提前停止":""}`);
    for(const g of r.groups){
      lines.push(`\n${g.name} · ${g.ranked}/${g.count} 已评分${g.skipped?" · 排除 "+g.skipped:""}`);
      if(g.error){lines.push(g.error);continue;}
      lines.push("当前："+(g.selected||"未知"));
      for(const x of g.rows.slice(0,5))lines.push(`${x.current?"●":"○"} ${x.node}｜${x.score??"—"} 分｜${format(x.delay)} ms｜${format(x.speed)} Mbps｜${x.status}`);
      if(g.rows.length>5)lines.push("其余节点详见脚本日志");
    }
    if(!r.networkIdentified)lines.push("\n网络身份未识别，历史数据仅短期使用。");
    lines.push("\n完整 JSON 见脚本日志；未执行任何策略切换。");
    return lines.join("\n");
  }
  async function run(args,context={}){
    const opts=options(args),c=config(),net=network(c);
    const tag=String(context.tag||"");
    const isReport=tag.includes("质量报告");
    const token=claim();
    if(!token)return {title:"Smart Selection",content:"已有任务执行，稍后重试"};
    try{
      let s=load();
      const groups=await discover(c,opts,context);
      if(isReport){const report=buildReport(groups,s,net,opts,null);api.log(JSON.stringify(report));return {title:"线路质量报告",content:summary(report),report};}
      const run={start:now(),charged:0,actual:0,tested:[],stop:false};
      const candidates=queue(groups,s,net);
      for(const node of candidates){
        if(run.tested.length>=BATCH||run.stop||now()-run.start>RUN_MS-16000||s.charged+2*MB+48000>opts.budget||run.charged+2*MB+48000>RUN_BYTES)break;
        // Abort if identified Wi-Fi changes during a batch.
        if(network(config()).key!==net.key){run.stop=true;break;}
        const sample=await probe(node,s,opts,run,token);
        if(sample.attempts){record(s,net,node,sample);run.tested.push(node);api.log(JSON.stringify({node,sample}));save(s);}
      }
      s.cursor=(s.cursor||0)+1;prune(s);s.last=now();save(s);
      const report=buildReport(groups,s,net,opts,run);
      api.log(JSON.stringify(report));
      return {title:"线路检测完成",content:summary(report),report};
    }finally{release(token);}
  }
  return {run,quality,queue,options,network,newState,buildReport};
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = createSmartSelection;
} else {
  const api = {
    now: Date.now, random: Math.random,
    config: () => $config.getConfig(),
    members: (name, cb) => $config.getSubPolicies(name, cb),
    selected: name => $config.getSelectedPolicy(name),
    read: key => $persistentStore.read(key),
    write: (key, value) => $persistentStore.write(value, key),
    request: (method, opts, cb) => $httpClient[method](opts, cb),
    timer: (cb, ms) => setTimeout(cb, ms),
    clear: id => { if (typeof clearTimeout === "function") clearTimeout(id); },
    log: text => console.log(text)
  };
  const params = typeof $environment !== "undefined" && $environment ? ($environment.params || {}) : {};
  const args = typeof $argument !== "undefined" ? $argument : {};
  const tag = typeof $script !== "undefined" && $script ? $script.name : "";
  const node = typeof params.node === "string" ? params.node : (params.nodeInfo && typeof params.nodeInfo.name === "string" ? params.nodeInfo.name : "");
  createSmartSelection(api).run(args, { tag, group: typeof params.policyGroup === "string" ? params.policyGroup : "", node })
    .then(result => { $done({title:result.title, content:result.content}); })
    .catch(error => { console.log("Smart Selection: " + String(error.message || error)); $done({title:"Smart Selection 检测中止",content:String(error.message || error)}); });
}
