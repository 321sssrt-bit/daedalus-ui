const fs=require('fs');
const path=require('path');
const assert=require('assert/strict');
const {pathToFileURL}=require('url');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
const temp=path.join(root,'_work','028-040-temp');
fs.mkdirSync(temp,{recursive:true});
process.env.TEMP=temp;process.env.TMP=temp;
const from=process.argv[2]||'028';
const files=fs.readdirSync(root).filter(n=>/^(02[89]|03\d|040)-.*\.html$/.test(n)&&n.slice(0,3)>=from).sort();
const resultFile=path.join(__dirname,'028-040-results.json');
const results=from==='028'?[]:JSON.parse(fs.readFileSync(resultFile,'utf8')).filter(r=>r.id<from);
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true,env:{...process.env,TEMP:temp,TMP:temp}});
 try{
  for(const file of files){
   const id=file.slice(0,3),mobile=Number(id)>=33;
   const context=await browser.newContext({viewport:{width:mobile?390:1280,height:mobile?844:800},reducedMotion:'reduce'});
   const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(pathToFileURL(path.join(root,file)).href);
   await page.screenshot({path:path.join(__dirname,'028-040-'+id+'-initial.png'),fullPage:false});
   const overflow=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
   assert(overflow.scroll<=overflow.width+1,id+' initial horizontal overflow '+JSON.stringify(overflow));
   if(!mobile){await page.setViewportSize({width:768,height:800});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),id+' 768px overflow');await page.screenshot({path:path.join(__dirname,'028-040-'+id+'-768.png'),fullPage:false});await page.setViewportSize({width:1280,height:800});}
   if(id==='028'){
    assert.equal(await page.locator('#application').evaluate(e=>e.checkValidity()),false);
    await page.locator('[name=name]').fill('林间');await page.locator('[name=email]').fill('lin@example.com');await page.locator('[name=practice]').selectOption({label:'写作与研究'});await page.locator('[name=project]').fill('山地声音笔记');await page.locator('[name=idea]').fill('记录驻地周围的山谷回声与日常声音。');await page.locator('[name=agree]').check();
    await page.locator('#saveDraft').click();await page.reload();assert.equal(await page.locator('[name=project]').inputValue(),'山地声音笔记');assert.equal(await page.locator('[name=agree]').isChecked(),true);await page.locator('#submitApplication').click();assert.equal(await page.locator('#receipt').isVisible(),true);assert.equal(await page.locator('#submitApplication').isDisabled(),true);assert.match(await page.locator('#receipt').textContent(),/林间/);
   }else if(id==='029'){
    assert.equal(await page.locator('.file').count(),2);await page.locator('.remove').first().click();assert.equal(await page.locator('#count').textContent(),'01');await page.locator('#files').setInputFiles({name:'test.png',mimeType:'image/png',buffer:Buffer.from([137,80,78,71])});assert.equal(await page.locator('.file').count(),2);await page.locator('#process').click();await page.waitForFunction(()=>document.querySelectorAll('.state.done').length===2);await page.locator('#files').setInputFiles({name:'notes.txt',mimeType:'text/plain',buffer:Buffer.from('abc')});assert.match(await page.locator('.state.bad').textContent(),/不支持/);
   }else if(id==='030'){
    assert.equal(await page.locator('.sample').count(),8);await page.locator('#kind').selectOption({label:'木本'});assert.equal(await page.locator('#resultCount').textContent(),'3');await page.locator('#season').selectOption({label:'秋季'});assert.equal(await page.locator('.sample').count(),2);await page.locator('#keyword').fill('不存在');assert.equal(await page.locator('#resultCount').textContent(),'0');assert.equal(await page.locator('.zero').isVisible(),true);await page.locator('#clear').click();assert.equal(await page.locator('.sample').count(),8);await page.locator('.sample').first().click();assert.match(await page.locator('#detailName').textContent(),/银杏.*H-201/);await page.locator('#closeDetail').click();
   }else if(id==='031'){
    assert.equal(await page.locator('#publish').isDisabled(),true);await page.locator('#ack').check();assert.equal(await page.locator('#publish').isEnabled(),true);await page.locator('#backEdit').click();await page.locator('#editTitle').fill('街巷里的回声');await page.locator('#returnReview').click();assert.equal(await page.locator('#ack').isChecked(),false);assert.match(await page.locator('#coverTitle').textContent(),/街巷里的回声/);await page.locator('#ack').check();await page.locator('#publish').click();assert.equal(await page.locator('#published').isVisible(),true);await page.locator('#readIssue').click();assert.equal(await page.locator('#readArticle').isVisible(),true);
   }else if(id==='032'){
    assert.equal(await page.locator('#delete').isDisabled(),true);await page.locator('#confirmWord').fill('删除冰川 ');assert.equal(await page.locator('#delete').isDisabled(),true);await page.locator('#cancel').click();assert.match(await page.locator('#outcomeTitle').textContent(),/已取消/);await page.locator('#backDanger').click();await page.locator('#confirmWord').fill('删除冰川');assert.equal(await page.locator('#delete').isEnabled(),true);await page.locator('#delete').click();assert.match(await page.locator('#outcomeTitle').textContent(),/已删除/);assert.equal(await page.locator('#archiveList').isVisible(),false);
   }else if(id==='033'){
    await page.locator('#transfer').click();await page.locator('#recipient').fill('唐梨');await page.locator('#amount').fill('99999');await page.locator('#transferForm button[type=submit]').click();assert.match(await page.locator('#transferMessage').textContent(),/不超过/);assert.equal(await page.locator('#balance').textContent(),'12,860.50');await page.locator('#amount').fill('10.50');await page.locator('#transferForm button[type=submit]').click();assert.equal(await page.locator('#balance').textContent(),'12,850.00');assert.match(await page.locator('#recent').textContent(),/唐梨/);await page.locator('#receive').click();assert.match(await page.locator('#receiveDialog').textContent(),/TB 8802/);await page.locator('#closeReceive').click();await page.locator('[data-view=history]').click();assert.equal(await page.locator('#historyView').isVisible(),true);await page.locator('[data-view=mine]').click();assert.equal(await page.locator('#mineView').isVisible(),true);
   }else if(id==='034'){
    await page.locator('#play').click();await page.waitForFunction(()=>document.querySelector('#elapsed').textContent!=='00:42');await page.locator('#play').click();const time=await page.locator('#elapsed').textContent();await page.waitForTimeout(1100);assert.equal(await page.locator('#elapsed').textContent(),time);await page.locator('#next').click();assert.equal(await page.locator('#title').textContent(),'末班电车的窗');assert.equal(await page.locator('#elapsed').textContent(),'00:00');assert.equal(await page.locator('#duration').textContent(),'03:16');await page.locator('#seek').fill('60');assert.equal(await page.locator('#elapsed').textContent(),'01:00');await page.locator('#showQueue').click();await page.locator('#queue button').last().click();assert.equal(await page.locator('#title').textContent(),'十点钟的唱片店');
   }else if(id==='035'){
    await page.locator('#more').click();assert.equal(await page.locator('[data-amount="200"]').textContent(),'600 克');await page.locator('#less').click();await page.locator('#less').click();assert.equal(await page.locator('#less').isDisabled(),true);await page.locator('#save').click();assert.equal(await page.locator('#save').getAttribute('aria-pressed'),'true');await page.locator('#start').click();await page.locator('#nextStep').click();await page.locator('#nextStep').click();await page.locator('#nextStep').click();assert.equal(await page.locator('#cookTitle').textContent(),'开饭啦。');assert.match(await page.locator('#cookText').textContent(),/1 个人/);
   }else if(id==='036'){
    await page.locator('#title').fill('窗边的蓝');await page.locator('#body').fill('今天看见蓝天');assert.equal(await page.locator('#count').textContent(),'6 / 3000 字');await page.locator('#saveDraft').click();await page.reload();assert.equal(await page.locator('#body').inputValue(),'今天看见蓝天');await page.locator('#openDraft').click();assert.equal(await page.locator('#draftTitle').textContent(),'窗边的蓝');await page.locator('#continueWriting').click();await page.locator('#noteForm button[type=submit]').click();assert.equal(await page.locator('#publishedBody').textContent(),'今天看见蓝天');await page.locator('#editAgain').click();assert.equal(await page.locator('#body').inputValue(),'今天看见蓝天');
   }else if(id==='037'){
    assert.equal(await page.locator('#empty').isVisible(),true);await page.locator('#add').click();await page.locator('#taskName').fill('散步');await page.locator('#addForm button[type=submit]').click();assert.equal(await page.locator('#empty').isVisible(),false);await page.locator('#items input').check();assert.match(await page.locator('#summary').textContent(),/0 件待完成 · 1 件已放飞/);await page.locator('#completedTab').click();assert.match(await page.locator('#completed').textContent(),/散步/);await page.locator('#completed input').click();assert.equal(await page.locator('.archive-empty').isVisible(),true);await page.locator('#activeTab').click();await page.locator('#items button').click();assert.equal(await page.locator('#empty').isVisible(),true);
   }else if(id==='038'){
    await page.locator('#retry').click();await page.locator('#home').click();await page.waitForTimeout(1400);assert.equal(await page.locator('#homeView').isVisible(),true);assert.equal(await page.locator('#destination').inputValue(),'西岸美术馆');await page.locator('#destination').fill('江边书店');await page.locator('#routeForm button').click();assert.match(await page.locator('#routeName').textContent(),/江边书店/);await page.locator('#startRoute').click();assert.match(await page.locator('#navigationStatus').textContent(),/200 米/);await page.reload();await page.locator('#retry').click();await page.waitForSelector('#successView:visible');
   }else if(id==='039'){
    await page.locator('summary').click();assert.match(await page.locator('details').textContent(),/12 分钟/);await page.locator('#done').click();assert.equal(await page.locator('#walletView').isVisible(),true);await page.locator('#openTicket').click();assert.equal(await page.locator('#receiptView').isVisible(),true);assert.match(await page.locator('.stub').textContent(),/FR-20260905-039/);
   }else if(id==='040'){
    await page.locator('#aside').click();await page.waitForTimeout(2100);assert(Number((await page.locator('#backgroundStatus').textContent()).match(/(\d+)%/)[1])>12);await page.locator('#cancelBackground').click();await page.waitForTimeout(1100);assert.equal(await page.locator('#cancelledView').isVisible(),true);await page.locator('#restart').click();assert.equal(await page.locator('#percent').textContent(),'12%');await page.waitForFunction(()=>document.querySelector('#percent').textContent==='100%',null,{timeout:22000});assert.equal(await page.locator('#cancel').isVisible(),false);await page.locator('#aside').click();assert.equal(await page.locator('#result').isVisible(),true);assert.match(await page.locator('#result').textContent(),/6 页/);
   }
   assert.deepEqual(errors,[],id+' page errors');
   results.push({id,file,status:'passed',viewport:mobile?'390x844':'1280x800 + 768x800',pageErrors:errors});console.log(id+' passed');await context.close();
  }
 }finally{await browser.close();fs.writeFileSync(path.join(__dirname,'028-040-results.json'),JSON.stringify(results,null,2)+'\n');}
 assert.equal(results.length,13);console.log('13 pieces passed behavior + viewport checks.');
})().catch(e=>{console.error(e);process.exitCode=1});
