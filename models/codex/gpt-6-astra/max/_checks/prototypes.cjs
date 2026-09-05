const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const root=path.resolve(__dirname,'..');
const artifacts=path.join(__dirname,'artifacts');
fs.mkdirSync(artifacts,{recursive:true});
const temp=path.join(root,'_work','prototype-temp');
fs.mkdirSync(temp,{recursive:true});
process.env.TEMP=temp;process.env.TMP=temp;
const tests={
 '041':async p=>{
  await p.locator('#quantity').fill('2');await p.locator('#add').click();await p.locator('#bag').click();assert.equal(await p.locator('#total').textContent(),'¥256');
  await p.locator('#order').click();assert.equal(await p.locator('#orderTotal').textContent(),'¥256');assert.match(await p.locator('#orderItems').textContent(),/苔绿 × 2/);
  await p.locator('#again').click();await p.locator('#stockDemo').click();assert.equal(await p.locator('#stockError').isVisible(),true);assert.equal(await p.locator('#bagCount').textContent(),'0');
  await p.locator('#quantity').fill('1');await p.locator('#add').click();await p.locator('#bag').click();await p.locator('#cartLines input').fill('2');await p.locator('#cartLines input').blur();await p.locator('#order').click();assert.equal(await p.locator('#cartError').isVisible(),true);assert.equal(await p.locator('#success').isVisible(),false);
  await p.locator('#cartLines input').fill('1');await p.locator('#cartLines input').blur();await p.locator('#order').click();assert.equal(await p.locator('#orderTotal').textContent(),'¥128');assert.match(await p.locator('#orderItems').textContent(),/砂白 × 1/);
 },
 '042':async p=>{
  await p.locator('[data-person="0"]').click();await p.locator('#value').fill('88');await p.locator('#next').click();await p.locator('#confirm').click();assert.equal(await p.locator('#receiptBalance').textContent(),'¥1,180.50');assert.equal(await p.locator('#receiptPerson').textContent(),'林小满');
  await p.locator('#done').click();await p.locator('[data-person="1"]').click();await p.locator('#tooMuch').click();await p.locator('#next').click();await p.locator('#confirm').click();assert.match(await p.locator('#fundsError').textContent(),/1,180.50/);assert.equal(await p.locator('#receipt').isVisible(),false);
  await p.locator('#edit').click();assert.equal(await p.locator('#value').inputValue(),'1500.00');await p.locator('#value').fill('68.50');await p.locator('#next').click();await p.locator('#confirm').click();assert.equal(await p.locator('#receiptBalance').textContent(),'¥1,112.00');assert.equal(await p.locator('#receiptPerson').textContent(),'陈一舟');
 },
 '043':async p=>{
  await p.locator('[data-convo="0"]').click();await p.locator('#message').fill('我带热茶');await p.locator('#send').click();await p.waitForFunction(()=>document.querySelector('.message:last-child .delivery')?.textContent==='已送达');
  await p.locator('#failNext').click();await p.locator('#message').fill('九点见');await p.locator('#send').click();await p.locator('.retry').waitFor();const count=await p.locator('.message').count();assert.equal(await p.locator('.message:last-child .bubble').textContent(),'九点见');
  await p.locator('#back').click();await p.locator('[data-convo="0"]').click();assert.equal(await p.locator('.message:last-child .bubble').textContent(),'九点见');await p.locator('.retry').click();await p.waitForFunction(()=>document.querySelector('.message:last-child .delivery')?.textContent==='已送达');assert.equal(await p.locator('.message').count(),count);
  await p.locator('#failNext').click();await p.locator('#message').fill('切换前发送');await p.locator('#send').click();await p.locator('#back').click();await p.locator('[data-convo="1"]').click();await p.waitForTimeout(750);assert.equal(await p.locator('#composeStatus').textContent(),'');assert.equal(await p.locator('.retry').count(),0);
  await p.locator('#back').click();await p.locator('[data-convo="0"]').click();await p.locator('.retry').click();await p.locator('#back').click();await p.locator('[data-convo="2"]').click();await p.waitForTimeout(550);assert.equal(await p.locator('#composeStatus').textContent(),'');await p.locator('#back').click();await p.locator('[data-convo="0"]').click();assert.equal(await p.locator('.message:last-child .delivery').textContent(),'已送达');
 },
 '044':async p=>{
  const initial=await p.locator('.post').count();await p.locator('#write').click();await p.locator('#draft').fill('窗台的花开了');await p.locator('#audience').selectOption('朋友可见');await p.locator('#publish').click();assert.equal(await p.locator('.post').count(),initial+1);assert.match(await p.locator('.post').first().textContent(),/朋友可见/);
  await p.locator('#write').click();await p.locator('#draft').fill('第一行\n第二行');await p.locator('#audience').selectOption('仅自己');await p.locator('#failPublish').click();await p.locator('#publish').click();assert.equal(await p.locator('#publishError').isVisible(),true);assert.equal(await p.locator('#draft').inputValue(),'第一行\n第二行');assert.equal(await p.locator('#audience').inputValue(),'仅自己');assert.equal(await p.locator('.post').count(),initial+1);
  await p.locator('#publish').click();assert.equal(await p.locator('.post').count(),initial+2);assert.equal(await p.locator('.post').first().locator('p').textContent(),'第一行\n第二行');assert.match(await p.locator('.post').first().textContent(),/仅自己/);
 },
 '045':async p=>{
  await p.locator('[data-track="1"]').click();await p.locator('#play').click();await p.waitForFunction(()=>document.getElementById('playState').textContent==='正在播放');assert.equal(await p.evaluate(()=>ctx.state),'running');
  await p.locator('#play').click();await p.locator('#progress').evaluate(e=>{e.value='42';e.dispatchEvent(new Event('input',{bubbles:true}))});await p.locator('#save').click();assert.match(await p.locator('#saved').textContent(),/0:42/);await p.reload();assert.equal(await p.locator('#trackName').textContent(),'玻璃雨');assert.equal(await p.locator('#elapsed').textContent(),'0:42');
  await p.locator('#play').click();await p.waitForFunction(()=>document.getElementById('playState').textContent==='正在播放');await p.locator('#disconnect').click();const stopped=await p.locator('#elapsed').textContent();await p.waitForTimeout(600);assert.equal(await p.locator('#elapsed').textContent(),stopped);assert.equal(await p.locator('#interruption').isVisible(),true);await p.locator('#reconnect').click();await p.waitForFunction(()=>document.getElementById('playState').textContent==='正在播放');assert.ok(Number(await p.locator('#progress').inputValue())>=42);
 },
 '046':async p=>{
  await p.locator('#taskName').fill('整理首页反馈');await p.locator('#newTask button').click();const row=p.locator('[data-task="4"]');await row.locator('select').selectOption('林简');await row.locator('button').click();assert.equal(await row.locator('.state').textContent(),'进行中');await row.locator('button').click();assert.equal(await row.locator('.state').textContent(),'已完成');assert.match(await p.locator('#activities').textContent(),/整理首页反馈/);
  const locked=p.locator('[data-task="3"]');await locked.locator('button').click();assert.equal(await p.locator('#permission').isVisible(),true);assert.equal(await locked.locator('.state').textContent(),'待开始');await p.locator('#request').click();assert.equal(await locked.locator('.state').textContent(),'待开始');await p.locator('#safeReturn').click();assert.equal(await locked.count(),0);await p.locator('[data-task="1"] button').click();assert.equal(await p.locator('[data-task="1"] .state').textContent(),'已完成');
 },
 '047':async p=>{
  await p.locator('#headline').fill('今天就出发');await p.locator('[data-color="#86d9dc"]').click();assert.equal(await p.locator('#posterTitle1').textContent(),'今天就出发');await p.locator('#exportButton').click();await p.locator('#exportResult').waitFor();let event=p.waitForEvent('download');await p.locator('#download').click();let d=await event;await d.saveAs(path.join(artifacts,'047-poster.svg'));assert.match(fs.readFileSync(path.join(artifacts,'047-poster.svg'),'utf8'),/今天就出发/);const old=await p.locator('#download').getAttribute('href');
  await p.locator('#unsupported').click();await p.locator('#exportButton').click();assert.equal(await p.locator('#exportError').isVisible(),true);assert.equal(await p.locator('#download').getAttribute('href'),old);assert.equal(await p.locator('#headline').inputValue(),'今天就出发');await p.locator('#format').selectOption('png');await p.locator('#exportButton').click();await p.waitForFunction(()=>document.getElementById('exportDescription').textContent.startsWith('PNG'));event=p.waitForEvent('download');await p.locator('#download').click();d=await event;await d.saveAs(path.join(artifacts,'047-poster.png'));const png=fs.readFileSync(path.join(artifacts,'047-poster.png'));assert.equal(png.readUInt32BE(16),600);assert.equal(png.readUInt32BE(20),760);
 },
 '048':async p=>{
  await p.locator('#searchForm button').click();await p.locator('[data-train="0"]').click();await p.locator('[data-seat="08A"]').click();await p.locator('#reviewButton').click();await p.locator('#confirm').click();assert.equal(await p.locator('#ticketSeat').textContent(),'06车厢 08A');assert.equal(await p.locator('#ticketFare').textContent(),'¥156');
  await p.locator('#another').click();await p.locator('#searchForm button').click();const route=await p.locator('#routeSummary').textContent();await p.locator('[data-train="0"]').click();await p.locator('[data-seat="09B"]').click();await p.locator('#reviewButton').click();await p.locator('#confirm').click();assert.equal(await p.locator('#soldOut').isVisible(),true);assert.equal(await p.locator('#receipt').isVisible(),false);assert.equal(await p.locator('#routeSummary').textContent(),route);await p.locator('#changeSeat').click();await p.locator('[data-seat="08B"]').click();await p.locator('#reviewButton').click();await p.locator('#confirm').click();assert.equal(await p.locator('#ticketSeat').textContent(),'06车厢 08B');assert.match(await p.locator('#ticketId').textContent(),/002$/);
  const search=async(date,destination='黄山北',train='0')=>{await p.locator('#home').click();await p.locator('#date').fill(date);await p.locator('#destination').selectOption(destination);await p.locator('#searchForm button').click();await p.locator('[data-train="'+train+'"]').click()};
  await search('2026-09-06');assert.equal(await p.locator('[data-seat="08A"]').isDisabled(),true);assert.equal(await p.locator('[data-seat="09B"]').isDisabled(),true);
  await search('2026-09-07');assert.equal(await p.locator('[data-seat="08A"]').isEnabled(),true);assert.equal(await p.locator('[data-seat="09B"]').isEnabled(),true);
  await search('2026-09-06','千岛湖');assert.equal(await p.locator('[data-seat="08A"]').isEnabled(),true);
  await search('2026-09-06','黄山北','1');assert.equal(await p.locator('[data-seat="08A"]').isEnabled(),true);
  await search('2026-09-06');assert.equal(await p.locator('[data-seat="08A"]').isDisabled(),true);
 },
 '049':async p=>{
  await p.locator('#minutes').fill('30');await p.locator('#recordForm .primary').click();assert.equal(await p.locator('#total').textContent(),'125');assert.equal(await p.locator('.day').last().getAttribute('data-minutes'),'30');assert.equal(await p.locator('.record').count(),1);
  await p.locator('#invalid').click();await p.locator('#recordForm .primary').click();assert.equal(await p.locator('#dataError').isVisible(),true);assert.equal(await p.locator('#total').textContent(),'125');assert.equal(await p.locator('.record').count(),1);await p.locator('#minutes').fill('20');await p.locator('#recordForm .primary').click();assert.equal(await p.locator('#total').textContent(),'145');assert.equal(await p.locator('.day').last().getAttribute('data-minutes'),'50');assert.equal(await p.locator('.record').count(),2);
 },
 '050':async p=>{
  await p.locator('#start').click();await p.locator('[value="side"]').check();await p.locator('#submitAnswer').click();assert.match(await p.locator('#resultTitle').textContent(),/练习完成/);assert.equal(await p.locator('#courseCount').textContent(),'1 / 3');
  await p.locator('#practice').click();await p.locator('[value="front"]').check();await p.locator('#submitAnswer').click();assert.equal(await p.locator('#feedback').isVisible(),true);assert.equal(await p.locator('#result').isVisible(),false);assert.match(await p.locator('#explainWrong').textContent(),/侧面/);await p.locator('#retry').click();await p.locator('[value="side"]').check();await p.locator('#submitAnswer').click();assert.match(await p.locator('#resultTitle').textContent(),/订正成功/);assert.equal(await p.locator('#courseCount').textContent(),'1 / 3');
 }
};
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});const results=[];
 try{for(const [id,test] of Object.entries(tests)){
  if(process.argv[2]&&!process.argv[2].split(',').includes(id))continue;
  const file=fs.readdirSync(root).find(n=>n.startsWith(id+'-')&&n.endsWith('.html'));assert.ok(file,id+' exists');
  const mobile=['042','043','044','048','049'].includes(id);const p=await browser.newPage({viewport:{width:mobile?390:1280,height:mobile?844:800}});const errors=[],external=[];p.on('pageerror',e=>errors.push(e.message));p.on('request',r=>{if(/^https?:/.test(r.url()))external.push(r.url())});
  await p.goto(pathToFileURL(path.join(root,file)).href);await p.screenshot({path:path.join(artifacts,id+'-initial.png'),fullPage:true});
  assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,id+' primary width');
  await test(p);assert.deepEqual(errors,[],id+' no page errors');assert.deepEqual(external,[],id+' offline');
  await p.screenshot({path:path.join(artifacts,id+'-result.png'),fullPage:true});
  await p.setViewportSize({width:mobile?1280:768,height:800});await p.reload();assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,id+' secondary width');
  await p.emulateMedia({reducedMotion:'reduce'});await p.screenshot({path:path.join(artifacts,id+'-responsive.png'),fullPage:true});
  results.push({id,normal:'pass',exceptionRecovery:'pass',pageErrors:errors.length,externalRequests:external.length,primaryWidth:mobile?390:1280,secondaryWidth:mobile?1280:768});await p.close();
 }}finally{await browser.close()}
 const report=path.join(artifacts,'prototype-results.json');const previous=fs.existsSync(report)?JSON.parse(fs.readFileSync(report,'utf8')):[];const merged=[...previous.filter(r=>!results.some(n=>n.id===r.id)),...results].sort((a,b)=>a.id.localeCompare(b.id));fs.writeFileSync(report,JSON.stringify(merged,null,2));console.log(JSON.stringify(results));
})().catch(e=>{console.error(e);process.exitCode=1});
