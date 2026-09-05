const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const {pathToFileURL}=require('url');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..'),temp=path.join(root,'_work','028-040-temp');
fs.mkdirSync(temp,{recursive:true});process.env.TEMP=temp;process.env.TMP=temp;
const results=[];
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true,env:{...process.env,TEMP:temp,TMP:temp}});
 async function check(id,name,stem,run){
  const context=await browser.newContext({viewport:{width:id==='030'?1280:390,height:id==='030'?800:844},reducedMotion:'reduce'});
  const page=await context.newPage();page.setDefaultTimeout(5000);const errors=[];page.on('pageerror',e=>errors.push(e.message));
  try{await page.goto(pathToFileURL(path.join(root,stem+'.html')).href);const evidence=await run(page);assert.deepEqual(errors,[]);results.push({id,name,status:'passed',evidence});console.log(id+' '+name+' passed');}
  catch(error){results.push({id,name,status:'failed',message:error.message});console.log(id+' '+name+' FAILED: '+error.message);}
  finally{await page.screenshot({path:path.join(__dirname,'028-040-regression-'+id+'-'+name+'.png'),fullPage:false});await context.close();}
 }
 try{
  await check('030','all-options','030-specimen-find',async p=>{
   const options=await p.locator('#kind option').allTextContents();assert.deepEqual(options,['所有类别','草本','木本','蕨类']);
   assert.deepEqual(await p.locator('#habitat option').allTextContents(),['所有生境','林下','溪畔','山坡']);
   await p.locator('#kind').selectOption({label:'草本'});assert.equal(await p.locator('#resultCount').textContent(),'3');
   await p.locator('#habitat').selectOption({label:'溪畔'});await p.locator('#season').selectOption({label:'夏季'});await p.locator('#keyword').fill('石菖蒲');assert.equal(await p.locator('.sample').count(),1);
   await p.locator('#clear').click();await p.locator('#habitat').selectOption({label:'林下'});assert.equal(await p.locator('#resultCount').textContent(),'3');await p.locator('#clear').click();assert.equal(await p.locator('.sample').count(),8);
   return {allNativeOptionsPresent:true,grassAndForestSelectable:true,fourFilterIntersection:1,reset:8};
  });
  await check('033','blank-recipient','033-copper-wallet',async p=>{
   await p.locator('#transfer').click();await p.locator('#recipient').fill('   ');await p.locator('#amount').fill('1');await p.locator('#transferForm button[type=submit]').click();
   assert.equal(await p.locator('#balance').textContent(),'12,860.50','空白收款人不得扣款');assert.equal(await p.locator('#recent .transaction').count(),3);assert.equal(await p.locator('#transferDialog').isVisible(),true);assert.match(await p.locator('#transferMessage').textContent(),/收款人/);
   await p.locator('#recipient').fill('  唐梨  ');await p.locator('#transferForm button[type=submit]').click();assert.equal(await p.locator('#balance').textContent(),'12,859.50');assert.equal(await p.locator('#recent .desc b').first().textContent(),'转给 唐梨');
   return {whitespaceBlocked:true,unchangedOnFailure:true,trimmedRecipientAccepted:true};
  });
  await check('033','long-recipient','033-copper-wallet',async p=>{
   await p.locator('#transfer').click();await p.locator('#recipient').fill('M'.repeat(30));await p.locator('#amount').fill('1.23');await p.locator('#transferForm button[type=submit]').click();
   const geometry=await p.locator('#recent .transaction').first().evaluate(row=>{const amount=row.querySelector('.amount').getBoundingClientRect(),name=row.querySelector('.desc b'),range=document.createRange();range.selectNodeContents(name);return {textRight:Math.max(...Array.from(range.getClientRects(),r=>r.right)),amountLeft:amount.left,amountRight:amount.right,rowRight:row.getBoundingClientRect().right,nameHeight:name.getBoundingClientRect().height};});
   assert(geometry.textRight+8<=geometry.amountLeft,'名称不得侵入金额: '+JSON.stringify(geometry));assert(geometry.amountRight<=geometry.rowRight+1);assert(geometry.nameHeight>20,'长名称应换行');
   await p.locator('[data-view=history]').click();const gap=await p.locator('#history .transaction').first().evaluate(row=>row.querySelector('.amount').getBoundingClientRect().left-row.querySelector('.desc').getBoundingClientRect().right);assert(gap>=11);
   return geometry;
  });
  await check('036','storage-retry','036-blue-hour-note',async p=>{
   await p.evaluate(()=>{const original=Storage.prototype.setItem;window.restoreNoteStorage=()=>{Storage.prototype.setItem=original;};Storage.prototype.setItem=function(){throw new DOMException('Blocked for regression','QuotaExceededError');};});
   await p.locator('#title').fill('不能丢的手记');await p.locator('#body').fill('存储失败时保留我的文字。');await p.locator('#noteForm button[type=submit]').click();
   assert.equal(await p.locator('#compose').isVisible(),true,'拒写时必须留在编辑页');assert.equal(await p.locator('#published').isVisible(),false);assert.match(await p.locator('#message').textContent(),/发布未完成/);assert.match(await p.locator('#draftState').textContent(),/仅保留在本页/);assert.equal(await p.locator('#title').inputValue(),'不能丢的手记');assert.equal(await p.locator('#body').inputValue(),'存储失败时保留我的文字。');assert.equal(await p.evaluate(()=>localStorage.getItem('daedalus-036-note')),null);
   await p.evaluate(()=>window.restoreNoteStorage());await p.locator('#noteForm button[type=submit]').click();assert.equal(await p.locator('#published').isVisible(),true);assert.equal(await p.locator('#publishedBody').textContent(),'存储失败时保留我的文字。');const persisted=await p.evaluate(()=>JSON.parse(localStorage.getItem('daedalus-036-note')));assert.equal(persisted.title,'不能丢的手记');assert.equal(persisted.body,'存储失败时保留我的文字。');
   return {failureVisible:true,noFalsePublish:true,inputsRetained:true,retryPersisted:true};
  });
  await check('038','route-reset','038-detour-route',async p=>{
   await p.locator('#retry').click();await p.waitForSelector('#successView:visible');await p.locator('#startRoute').click();assert.equal(await p.locator('#startRoute').textContent(),'步行预览中');
   await p.locator('#successHome').click();await p.locator('#destination').fill('独立书店');await p.locator('#routeForm button').click();assert.match(await p.locator('#routeName').textContent(),/独立书店/);assert.equal(await p.locator('#startRoute').textContent(),'开始步行预览');assert.equal(await p.locator('#navigationStatus').textContent(),'');assert.equal(await p.locator('#startRoute').isEnabled(),true);
   await p.locator('#startRoute').click();assert.match(await p.locator('#navigationStatus').textContent(),/预览已开始/);await p.locator('#successHome').click();await p.locator('#routeForm button').click();assert.equal(await p.locator('#navigationStatus').textContent(),'');
   return {newDestinationClearsPreview:true,sameRouteReentryClearsPreview:true,restartWorks:true};
  });
 }finally{await browser.close();fs.writeFileSync(path.join(__dirname,'028-040-regressions-'+(process.argv[2]||'results')+'.json'),JSON.stringify(results,null,2)+'\n');}
 if(results.some(r=>r.status!=='passed'))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
