const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const output=path.join(root,'_work','015-027-browser');
const temp=path.join(root,'_work','015-027-temp');
fs.mkdirSync(output,{recursive:true}); fs.mkdirSync(temp,{recursive:true});
process.env.TEMP=temp; process.env.TMP=temp;
const names=['015-signal-stack','016-guild-atlas','017-pebble-supply','018-brass-hour','019-daily-basket','020-stage-plans','021-field-notes','022-lunar-maker','023-cabinet-oddities','024-silk-counter','025-quiet-account','026-carbon-bill','027-lantern-roles'];
const checks={
  '015':async p=>{assert.equal(await p.locator('.notice').count(),6);assert.equal(await p.locator('.unread').count(),4);await p.locator('summary').first().click();await p.waitForFunction(()=>document.querySelector('#count').textContent==='03');await p.locator('#readall').click();assert.equal(await p.locator('#count').innerText(),'00');assert(await p.locator('#readall').isDisabled());await p.locator('[data-filter=unread]').click();assert(await p.locator('details[open]').isVisible());await p.locator('details[open] summary').click();await p.locator('#empty').waitFor();},
  '016':async p=>{await p.locator('[data-filter="工程"]').click();assert.equal(await p.locator('.person').count(),2);await p.locator('.person').first().click();assert.match(await p.locator('#profile').innerText(),/何牧/);await p.locator('#close').click();await p.locator('[data-filter="设计"]').click();assert.equal(await p.locator('.person').count(),3);},
  '017':async p=>{assert.equal(await p.locator('.product').count(),6);await p.locator('[data-heart="0"]').click();assert.equal(await p.locator('#saved-count').innerText(),'1');await p.locator('#saved').click();assert.equal(await p.locator('.product').count(),1);await p.locator('[data-heart="0"]').click();assert.equal(await p.locator('#saved-count').innerText(),'0');assert(await p.locator('#empty').isVisible());await p.locator('[data-category="家居"]').click();assert.equal(await p.locator('.product').count(),3);},
  '018':async p=>{await p.locator('[data-value="石墨黑"]').click();assert.equal(await p.locator('#clock-rim').getAttribute('fill'),'#4D554F');await p.locator('[data-size="40"]').click();assert.match(await p.locator('#price').innerText(),/880/);await p.locator('#buy').click();assert.match(await p.locator('#receipt').innerText(),/石墨黑.*40 cm.*880/);await p.locator('#again').click();assert(await p.locator('#buy').isVisible());},
  '019':async p=>{assert.equal(await p.locator('#total').innerText(),'¥71.00');await p.locator('[data-item="0"][data-delta="1"]').click();assert.equal(await p.locator('#total').innerText(),'¥83.00');assert.equal(await p.locator('#shipping').innerText(),'免配送费');await p.locator('[data-remove="1"]').click();assert.equal(await p.locator('#total').innerText(),'¥77.00');await p.locator('#checkout').click();assert.match(await p.locator('#checkout-list').innerText(),/番茄 × 3/);assert.match(await p.locator('#checkout-total').innerText(),/77.00/);await p.locator('#close-checkout').click();await p.locator('[data-remove="0"]').click();await p.locator('[data-remove="2"]').click();assert(await p.locator('#checkout').isDisabled());assert.equal(await p.locator('#total').innerText(),'¥0.00');},
  '020':async p=>{assert.equal(await p.locator('.plan').count(),3);await p.locator('[data-cycle=year]').click();assert.match(await p.locator('#creator-price').innerText(),/79.2/);await p.locator('[data-plan=creator]').click();assert.match(await p.locator('#choice').innerText(),/950.40/);await p.locator('#close').click();await p.locator('[data-plan=studio]').click();await p.locator('#contact-email').fill('studio@example.com');await p.locator('#team-size').fill('12');await p.locator('#contact button').click();assert.match(await p.locator('#contact-result').innerText(),/12 人团队/);},
  '021':async p=>{assert.equal(await p.locator('details').count(),5);await p.locator('summary').nth(1).click();assert(await p.locator('.excerpt').nth(1).isVisible());assert.match(await p.locator('.excerpt').nth(1).innerText(),/竹器铺/);await p.locator('summary').nth(3).click();assert(await p.locator('.excerpt').nth(1).isVisible());assert(await p.locator('.excerpt').nth(3).isVisible());},
  '022':async p=>{await p.locator('#follow').click();assert.match(await p.locator('#follow-status').innerText(),/129/);await p.locator('#follow').click();assert.match(await p.locator('#follow-status').innerText(),/128/);await p.locator('[data-work="1"]').click();assert.match(await p.locator('#dialog-content').innerText(),/无用之书/);await p.locator('#close').click();await p.locator('#contact').click();assert.match(await p.locator('#dialog-content').innerText(),/hello@lunar-maker.example/);},
  '023':async p=>{assert.equal(await p.locator('.specimen').count(),6);await p.locator('[data-remove="0"]').click();assert.equal(await p.locator('#count').innerText(),'05');await p.locator('[data-filter="器物"]').click();assert.equal(await p.locator('.specimen').count(),2);await p.locator('[data-filter="全部"]').click();assert.equal(await p.locator('.specimen').count(),5);await p.reload();assert.equal(await p.locator('.specimen').count(),5);await p.locator('[data-remove="1"]').click();await p.locator('#undo').click();assert.equal(await p.locator('.specimen').count(),5);},
  '024':async p=>{await p.locator('input[value=wallet]').check();assert(await p.locator('[data-method=wallet] .method-detail').isVisible());assert(!(await p.locator('[data-method=card] .method-detail').isVisible()));await p.locator('#confirm').click();assert.match(await p.locator('#paid-method').innerText(),/424.00/);assert.match(await p.locator('#receipt').innerText(),/456.00/);await p.locator('#reset').click();assert(await p.locator('input[value=wallet]').isChecked());},
  '025':async p=>{await p.locator('#name').fill('林间');await p.locator('#save').click();assert.equal(await p.locator('#identity-name').innerText(),'林间');await p.locator('[data-section=notifications]').click();await p.locator('#digest').uncheck();await p.locator('#save').click();assert.equal(await p.locator('#notifications-summary').innerText(),'仅重要提及');await p.locator('#email').fill('invalid');await p.locator('#save').click();assert.match(await p.locator('#save-status').innerText(),/有效/);assert.equal(await p.locator('#identity-email').innerText(),'lin.yi@example.com');},
  '026':async p=>{assert.equal(await p.locator('tbody tr').count(),4);const downloaded=p.waitForEvent('download');await p.locator('[data-download="0"]').click();const d=await downloaded;assert.equal(d.suggestedFilename(),'CL-202609-001.txt');const f=path.join(output,d.suggestedFilename());await d.saveAs(f);const contents=fs.readFileSync(f,'utf8');assert.match(contents,/CL-202609-001/);assert.match(contents,/129.00/);await p.locator('#change-method').click();await p.locator('input[value=bank]').check();await p.locator('#method-form button').first().click();assert.match(await p.locator('#current-method').innerText(),/8821/);await p.locator('#change-method').click();assert(await p.locator('input[value=bank]').isChecked());await p.locator('#cancel').click();},
  '027':async p=>{assert(await p.locator('#save').isDisabled());await p.locator('[data-role=viewer]').click();assert.match(await p.locator('#preview-body').innerText(),/查看项目/);await p.locator('[data-permission="3"]').check();assert.match(await p.locator('#preview-body').innerText(),/导出内容/);await p.locator('#save').click();assert(await p.locator('#save').isDisabled());await p.locator('[data-role=owner]').click();assert.equal(await p.locator('input:disabled').count(),5);await p.locator('[data-role=viewer]').click();assert(await p.locator('[data-permission="3"]').isChecked());await p.locator('[data-permission="1"]').check();await p.locator('#reset').click();assert(!(await p.locator('[data-permission="1"]').isChecked()));}
};
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const results=[];
 try{
  for(const name of names.filter(n=>process.argv.length<3||process.argv.slice(2).includes(n.slice(0,3)))){
   const context=await browser.newContext({viewport:{width:1280,height:800},reducedMotion:'reduce',acceptDownloads:true});
   const p=await context.newPage();const errors=[];p.on('pageerror',e=>errors.push(String(e)));
   await p.goto(pathToFileURL(path.join(root,name+'.html')).href);await p.evaluate(()=>document.fonts.ready);
   for(const width of [1280,768]){
    await p.setViewportSize({width,height:800});
    const overflow=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
    assert(!overflow,name+' overflows at '+width);
    await p.screenshot({path:path.join(output,name+'-'+width+'.png'),fullPage:true});
   }
   await p.setViewportSize({width:1280,height:800});
   await checks[name.slice(0,3)](p);
   assert.deepEqual(errors,[],name+' browser errors');
   results.push({page:name,widths:[1280,768],interaction:'passed',errors});
   console.log(name+' PASS');
   await context.close();
  }
 }finally{await browser.close();fs.writeFileSync(path.join(output,'results.json'),JSON.stringify(results,null,2));}
 assert.equal(results.length,process.argv.length<3?13:process.argv.length-2);console.log(results.length+' pages passed layout and interactive checks.');
})().catch(e=>{console.error(e);process.exitCode=1});
