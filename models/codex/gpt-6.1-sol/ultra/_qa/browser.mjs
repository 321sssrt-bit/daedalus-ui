import {spawn} from 'node:child_process';
import {mkdtemp,writeFile,mkdir,readFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {pathToFileURL} from 'node:url';

export async function browser() {
  let child=null,endpoint=process.env.DAEDALUS_ENDPOINT;
  if(!endpoint){
    const profile=await mkdtemp(join(process.env.DAEDALUS_RUNTIME || tmpdir(),'daedalus-sol-ultra-'));
    const binary=process.env.DAEDALUS_BROWSER || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
    child=spawn(binary,['--headless','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-port=0',`--user-data-dir=${profile}`,'about:blank'],{windowsHide:true,stdio:['ignore','ignore','ignore']});
    const until=Date.now()+20000;
    while(Date.now()<until){try{const [port,path]= (await readFile(join(profile,'DevToolsActivePort'),'utf8')).trim().split(/\r?\n/);endpoint=`ws://127.0.0.1:${port}${path}`;break}catch{await new Promise(r=>setTimeout(r,100))}}
    if(!endpoint){child.kill();throw new Error('Browser endpoint timeout')}
  }
  const ws=new WebSocket(endpoint);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});
  let seq=0;const pending=new Map(),errors=[];
  ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);if(p)m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result)}else if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails)};
  const send=(method,params={},sessionId)=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params,...(sessionId?{sessionId}:{})}))});
  const {targetId}=await send('Target.createTarget',{url:'about:blank'});
  const {sessionId}=await send('Target.attachToTarget',{targetId,flatten:true});
  const call=(m,p={})=>send(m,p,sessionId);
  await call('Page.enable');await call('Runtime.enable');
  const evaluate=async expression=>{const r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true,userGesture:true});if(r.exceptionDetails)throw new Error(r.exceptionDetails.text+': '+JSON.stringify(r.exceptionDetails.exception));return r.result.value};
  const open=async(path,width=1280,height=800)=>{errors.length=0;await call('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:width<600});const url=pathToFileURL(path).href;await call('Page.navigate',{url});const until=Date.now()+15000;while(Date.now()<until){if(await evaluate(`location.href===${JSON.stringify(url)} && document.readyState==='complete'`))return;await new Promise(r=>setTimeout(r,50))}throw new Error('Page load timeout: '+path)};
  const shot=async path=>{const {data}=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await mkdir(join(path,'..'),{recursive:true});await writeFile(path,Buffer.from(data,'base64'))};
  const close=async()=>{try{await send('Browser.close')}catch{}ws.close();if(child&&child.exitCode===null)child.kill()};
  return {call,evaluate,open,shot,close,errors};
}
