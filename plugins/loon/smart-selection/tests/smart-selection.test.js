"use strict";
const createSmartSelection = require("../Smart_Selection.js");
function mockTests(factory){
  return (async()=>{
    let passed=0;const check=(v,label)=>{if(!v)throw Error("FAIL: "+label);passed++;};
    function mock(custom={}){
      let time=Date.UTC(2026,10,28,8),store=new Map(),calls=[],logs=[],writes=0;
      const groups=custom.groups||{"所有可用线路":["JP-fast","JP-slow","US","HK","DIRECT","剩余流量: 100 GB"],"美国线路":["US"],"香港线路":["HK"],"日本线路":["JP-fast","JP-slow"]};
      const selected=custom.selected||{"所有可用线路":"JP-slow","美国线路":"US","香港线路":"HK","日本线路":"JP-slow"};
      const api={now:()=>time,random:()=>.123,config:()=>JSON.stringify({all_policy_groups:Object.keys(groups),all_buildin_nodes:["DIRECT","REJECT"],ssid:"mock-wifi"}),members:(n,cb)=>cb(JSON.stringify(groups[n])),selected:n=>selected[n]||"",read:k=>store.get(k)||"",write:(k,v)=>{writes++;if(custom.writeFail)return false;store.set(k,v);return true;},timer:()=>0,clear:()=>{},log:s=>logs.push(s),request:(method,o,cb)=>{
        calls.push({method,node:o.node,url:o.url,secure:o.insecure===false});
        let fail=(custom.fail||[]).includes(o.node);
        if(fail){time+=1000;cb("timeout",null,null);return;}
        const m=/bytes=(\d+)/.exec(o.url),n=m?Number(m[1]):0;
        if(method==="head"){time+=o.node==="JP-slow"?70:130;cb(null,{status:o.url.includes("gstatic")?204:200,headers:{}},new Uint8Array(0));return;}
        time+=o.node==="JP-slow"?4000:400;
        cb(null,{status:200,headers:{"content-type":"application/octet-stream"}},new Uint8Array(custom.badLength?n-1:n));
      }};
      return {api,store,calls,logs,advance:ms=>time+=ms};
    }
    const m=mock(),core=factory(m.api);
    const r=(await core.run({dailyMB:200},{})).report;
    check(r.groups.length===4,"four independent groups");
    check(r.groups[0].count===4&&r.groups[0].skipped===2,"built-in and pseudo-node excluded");
    check(new Set(r.batch.tested).size===r.batch.tested.length,"shared probe dedupe");
    check(m.calls.filter(x=>x.node==="JP-fast"&&x.method==="get").length===1,"overlapping group download once");
    check(r.groups[3].rows[0].node==="JP-fast","faster throughput outranks lower delay");
    check(r.groups[1].rows.every(x=>x.node==="US"),"regional isolation");
    check(m.calls.every(x=>x.secure),"TLS validation");
    check(r.chargedMB>=r.receivedMB&&r.chargedMB<=16,"budget reserve");
    const count=m.calls.length;
    const rr=(await core.run({dailyMB:200},{tag:"质量报告"})).report;
    check(m.calls.length===count&&rr.batch===null,"read-only report");
    const a=mock({fail:["US"]}),fa=(await factory(a.api).run({},{})).report;
    check(fa.groups[1].rows[0].score===null&&fa.groups[3].ranked>0,"failed group isolated");
    const b=mock({badLength:true}),br=(await factory(b.api).run({},{})).report;
    check(br.groups.every(g=>g.ranked===0),"truncated body not scored");
    const c=mock(),cc=factory(c.api);
    for(let i=0;i<8;i++)await cc.run({dailyMB:50},{});
    const cr=(await cc.run({dailyMB:50},{tag:"质量报告"})).report;
    check(cr.chargedMB<=50&&cr.chargedMB>45,"daily budget shared");
    c.advance(24*3600000);
    check((await cc.run({dailyMB:50},{tag:"质量报告"})).report.chargedMB===0,"day rollover");
    const d=mock({groups:{A:["B","JP-fast"],B:["JP-fast","REJECT"]},selected:{A:"B",B:"JP-fast"}});
    const dr=(await factory(d.api).run({},{})).report;
    check(dr.groups[0].count===1&&dr.groups[0].skipped===1,"nested group safely excluded");
    const e=mock({writeFail:true});let threw=false;try{await factory(e.api).run({},{});}catch(_){threw=true;}
    check(threw&&e.calls.length===0,"fail closed on storage error");
    const f=mock();f.store.set("routingrules.smart-selection.v1.lease",JSON.stringify({token:"other",until:f.api.now()+50000}));
    check((await factory(f.api).run({},{})).report===undefined&&f.calls.length===0,"active lease");
    const g=mock(),gr=(await factory(g.api).run({groups:"日本线路"},{group:"日本线路"})).report;
    check(gr.groups.length===1&&g.calls.every(x=>x.node.startsWith("JP")),"manual group scope");
    const z=mock();z.store.set("routingrules.smart-selection.v1","not-json");let err=false;try{await factory(z.api).run({},{});}catch(_){err=true;}
    check(err&&z.calls.length===0,"corrupt state fail closed");
    return {passed};
  })();
}
mockTests(createSmartSelection).then(r=>console.log("Passed "+r.passed+" assertions")).catch(e=>{console.error(e);process.exitCode=1;});
