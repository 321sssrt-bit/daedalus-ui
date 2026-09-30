import assert from 'node:assert/strict';
import {dirname,resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {readFile,writeFile} from 'node:fs/promises';
import {browser} from './browser.mjs';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..'),pieces=JSON.parse(await readFile(join(root,'model.json'),'utf8')).pieces,b=await browser(),results=[];
const run=s=>b.evaluate(s),click=id=>run(`document.getElementById(${JSON.stringify(id)}).click()`),set=(id,v)=>run(`document.getElementById(${JSON.stringify(id)}).value=${JSON.stringify(v)}`);
const open=async(id,w)=>{await b.open(join(root,pieces.find(p=>p.id===id).file),w,w===390?844:800)};
try{
  await open('002',1280);await click('login-link');assert(await run(`!document.getElementById('signin').hidden&&document.getElementById('register').hidden`));await click('returnRegister');assert(await run(`!document.getElementById('register').hidden`));results.push({id:'002',check:'真实登录视图与注册返回',status:'passed'});
  await open('005',1280);await click('back');assert(await run(`!document.getElementById('signin').hidden&&document.getElementById('reset').hidden`));await click('returnReset');assert(await run(`!document.getElementById('reset').hidden`));results.push({id:'005',check:'真实登录入口与找回返回',status:'passed'});
  await open('033',390);await click('transfer');await set('receiver','测试收款人');await set('money','0.001');await run(`document.getElementById('transfer-form').requestSubmit()`);assert(await run(`document.getElementById('transfer-modal').open&&document.getElementById('balance').textContent==='8,426.50'&&document.getElementById('transactions').children.length===3`));await set('money','0.29');await run(`document.getElementById('transfer-form').requestSubmit()`);assert(await run(`!document.getElementById('transfer-modal').open&&document.getElementById('balance').textContent==='8,426.21'&&document.getElementById('transactions').textContent.includes('−0.29')`));results.push({id:'033',check:'0.001阻断无扣款；0.29整数分扣减',status:'passed'});
  await open('041',1280);assert.deepEqual(await run(`Array.from(document.getElementById('variant').options,o=>o.value)`),['白','灰']);await click('shortage');await click('add');await click('order');assert(await run(`document.getElementById('feedback').textContent.includes('库存不足')`));await set('variant','灰');assert.equal(await run(`document.getElementById('variant').value`),'灰');await run(`document.getElementById('variant').dispatchEvent(new Event('change'))`);assert.equal(await run(`document.getElementById('stock').textContent`),'5');await click('add');await click('order');assert(await run(`!document.getElementById('receipt').hidden&&document.getElementById('receiptText').textContent.includes('/ 灰 × 1')`));results.push({id:'041',check:'原生颜色改选有货后成功，核对选项、选中值与订单颜色',status:'passed'});
  for(const [id,width,length] of [['007',768,40],['036',390,40],['037',390,30],['046',768,60]]){
    await open(id,width);
    if(id==='007'){await click('create');await set('project-name','W'.repeat(length));await run(`document.getElementById('new-form').requestSubmit()`)}
    if(id==='036'){await set('title','W'.repeat(length));await set('body','W'.repeat(80));await click('publish')}
    if(id==='037'){await click('create');await set('trip-name','W'.repeat(length));await run(`document.getElementById('create-form').requestSubmit()`)}
    if(id==='046'){await set('taskTitle','W'.repeat(length));await click('create')}
    assert(await run(`document.documentElement.scrollWidth<=innerWidth+1`),id+' page overflow');
    if(id==='036')assert(await run(`document.getElementById('published').scrollWidth<=document.getElementById('published').clientWidth+1`));
    if(id==='037')assert(await run(`document.querySelector('.trip').scrollWidth<=document.querySelector('.trip').clientWidth+1`));
    assert.equal(b.errors.length,0);
    if(process.env.DAEDALUS_SHOTS)await b.shot(join(process.env.DAEDALUS_SHOTS,id+'-long-fixed.png'));
    results.push({id,check:'允许长度的连续英文不溢出/裁切',width,status:'passed'});
  }
  await writeFile(join(root,'qa-fix-check.json'),JSON.stringify({browser:'Chromium Edge headless',checkedAt:new Date().toISOString(),results},null,2)+'\n');
  console.log('8 independent QA findings fixed and targeted browser checks passed');
} finally {await b.close()}
