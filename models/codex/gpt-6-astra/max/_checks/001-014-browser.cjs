const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { pathToFileURL } = require('node:url');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const out = path.join(root, '_work', '001-014-evidence');
const temp = path.join(root, '_work', '001-014-temp');
fs.mkdirSync(out, { recursive: true });
fs.mkdirSync(temp, { recursive: true });
process.env.TEMP = temp;
process.env.TMP = temp;
const { chromium } = require('playwright');
const schemes = ['kiln-door','bloom-pass','velvet-rope','orbit-guide','letter-back','vault-six','seed-desk','window-light','harbor-shift','paper-lanes','tide-metrics','sunroom-days','ink-post','lost-folio'];
const only = new Set(process.argv.slice(2));
async function measureLongTitle(page) {
  const widths = {};
  for (const width of [1280,768]) {
    await page.setViewportSize({width,height:800});
    widths[width] = await page.evaluate(()=>document.documentElement.scrollWidth);
    assert(widths[width]<=width, 'A legal 60-character title must not expand the '+width+'px viewport');
  }
  return widths;
}
const regressionChecks = {
  '005': async p => {
    await p.reload(); await p.locator('#email').fill('return@example.com'); await p.locator('#to-login').click();
    await p.locator('#password').fill('123456'); await p.locator('#login-form .primary').click();
    assert.match(await p.locator('#login-status').textContent(),/成功/);
    await p.locator('#find-again').click(); await p.locator('#to-login').click();
    assert(await p.locator('#login-form').isVisible()); assert.equal(await p.locator('#password').inputValue(),''); assert.equal(await p.locator('#login-status').textContent(),'');
    await p.locator('#password').fill('654321'); await p.locator('#login-form .primary').click(); assert.match(await p.locator('#login-status').textContent(),/成功/);
    return {returnedFormVisible:true,repeatedLogin:true};
  },
  '007': async p => {
    await p.reload(); await p.locator('#create').click(); await p.locator('#title').fill('M'.repeat(60)); await p.locator('#body').fill('可保存的正文'); await p.locator('#note-form .primary').click();
    assert.equal(await p.locator('.note-card h3').textContent(),'M'.repeat(60));
    return {titleCharacters:60,scrollWidths:await measureLongTitle(p)};
  },
  '008': async p => {
    await p.reload(); await p.locator('#deny').click(); await p.locator('#city').selectOption('苏州');
    await p.locator('#preferences').click(); await p.locator('#allow').click();
    for(const selector of ['#sky-city','#result-text']) assert.match(await p.locator(selector).textContent(),/杭州/);
    await p.locator('#preferences').click(); await p.locator('#deny').click();
    for(const selector of ['#sky-city','#result-text']) assert.match(await p.locator(selector).textContent(),/苏州/);
    await p.locator('#preferences').click(); await p.locator('#once').click();
    for(const selector of ['#sky-city','#result-text']) assert.match(await p.locator(selector).textContent(),/杭州/);
    return {allowedCity:'杭州',retainedManualCity:'苏州',oneTimeCity:'杭州'};
  },
  '010': async p => {
    await p.reload(); await p.locator('#new').click(); await p.locator('#task-title').fill('M'.repeat(60)); await p.locator('#task-form .primary').click();
    const before=await measureLongTitle(p);
    await p.locator('#lane-0 .move').first().click();
    assert.match(await p.locator('#status').textContent(),/已移到正在做/);
    return {titleCharacters:60,createdScrollWidths:before,movedScrollWidths:await measureLongTitle(p)};
  },
  '014': async p => {
    await p.reload(); await p.locator('#query').fill('   '); await p.locator('#search-form button').click();
    assert(await p.locator('#query').evaluate(x=>x.validity.customError)); await p.locator('#suggest-moon').click();
    assert.equal(await p.locator('.book').count(),2); assert(await p.locator('#query').evaluate(x=>x.validity.valid));
    await p.locator('#search-form button').click(); assert.equal(await p.locator('.book').count(),2);
    return {blankRejected:true,suggestionClearsValidity:true,repeatedSearch:true};
  }
};
const checks = [
  async p => {
    await p.locator('#email').fill('test@example.com'); await p.locator('#password').fill('123456'); await p.locator('#login-form .primary').click(); assert(await p.locator('#inside').isVisible()); assert.match(await p.locator('#member').textContent(), /test@example.com/);
    await p.locator('#signout').click(); assert.equal(await p.locator('#password').inputValue(),''); await p.locator('#forgot').click(); await p.locator('#recover-email').fill('again@example.com'); await p.locator('#recover-form .primary').click(); assert.match(await p.locator('#recover-status').textContent(),/again@example.com/);
  },
  async p => {
    await p.locator('#nickname').fill('新邻居'); await p.locator('#email').fill('neighbor@example.com'); await p.locator('#password').fill('12345678'); await p.locator('#agree').check(); await p.locator('#signup-form .primary').click(); assert(await p.locator('#welcome').isVisible()); assert.match(await p.locator('#welcome-title').textContent(),/新邻居/);
    await p.locator('#restart').click(); await p.locator('#to-login').click(); await p.locator('#login-email').fill('neighbor@example.com'); await p.locator('#login-password').fill('12345678'); await p.locator('#login-form .primary').click(); assert.match(await p.locator('#welcome-title').textContent(),/欢迎回来/);
  },
  async p => {
    await p.locator('#code').fill('BAD-CODE'); await p.locator('#invite-form .primary').click(); assert.match(await p.locator('#status').textContent(),/未能匹配/); await p.locator('#code').fill('NUIT-0927'); await p.locator('#invite-form .primary').click(); assert(await p.locator('#admitted').isVisible()); assert.match(await p.locator('#admitted').textContent(),/NO. 027/); await p.locator('#return').click(); assert.equal(await p.locator('#code').inputValue(),'');
  },
  async p => {
    assert(await p.locator('#previous').isDisabled()); await p.locator('#next').click(); assert.match(await p.locator('#count').textContent(),/02/); await p.locator('#previous').click(); assert.match(await p.locator('#count').textContent(),/01/); await p.locator('#next').click(); await p.locator('#next').click(); assert.match(await p.locator('#next').textContent(),/开始使用/); await p.locator('#next').click(); assert(await p.locator('#dashboard').isVisible()); await p.locator('#start-lesson').click(); assert.match(await p.locator('#lesson-status').textContent(),/三种形状/); await p.locator('#replay').click(); await p.locator('#skip').click(); assert(await p.locator('#dashboard').isVisible());
  },
  async p => {
    await p.locator('#email').fill('reader@example.com'); await p.locator('#reset-form .primary').click(); assert(await p.locator('#sent').isVisible()); assert.equal(await p.locator('#recipient').textContent(),'reader@example.com'); assert(await p.locator('#resend').isDisabled()); await p.locator('#resend').click({timeout:8000}); assert.match(await p.locator('#status').textContent(),/再次寄出/); await p.locator('#change').click(); assert.equal(await p.locator('#email').inputValue(),'reader@example.com'); await p.locator('#to-login').click(); assert(await p.locator('#login').isVisible());
  },
  async p => {
    for(let i=0;i<3;i++){await p.locator('#otp').fill('111111');await p.locator('#verify').click()} assert(await p.locator('#verify').isDisabled()); assert.match(await p.locator('#status').textContent(),/锁定/); await p.locator('#resend').click(); assert(await p.locator('#otp').isEnabled()); await p.locator('#otp').fill('246810'); await p.locator('#verify').click(); assert(await p.locator('#verified').isVisible()); await p.locator('#again').click(); assert(await p.locator('#challenge').isVisible());
  },
  async p => {
    await p.locator('#create').click(); await p.locator('#title').fill('第一颗种子'); await p.locator('#body').fill('把今天的光留下。'); await p.locator('#note-form .primary').click(); assert.equal(await p.locator('#side-count').textContent(),'1'); assert.match(await p.locator('#notes').textContent(),/第一颗种子/); await p.reload(); await p.locator('#sample').click(); assert.match(await p.locator('#notes').textContent(),/在早晨留十分钟/);
  },
  async p => {
    await p.locator('#allow').click(); assert.match(await p.locator('#permission-state').textContent(),/已允许/); await p.locator('#preferences').click(); await p.locator('#once').click(); assert.match(await p.locator('#permission-state').textContent(),/仅本次/); await p.locator('#preferences').click(); await p.locator('#deny').click(); assert(await p.locator('#city-control').isVisible()); await p.locator('#city').selectOption('苏州'); assert.match(await p.locator('#sky-city').textContent(),/苏州/); assert.match(await p.locator('#permission-state').textContent(),/未允许/);
  },
  async p => {
    assert.equal(await p.locator('#rows tr').count(),8); await p.locator('[data-filter="pending"]').click(); assert.equal(await p.locator('#rows tr').count(),4); await p.locator('[data-filter="risk"]').click(); assert.equal(await p.locator('#rows tr').count(),2); await p.locator('[data-nav="warehouse"]').click(); assert.equal(await p.locator('#rows tr').count(),2); assert.match(await p.locator('#rows').textContent(),/已就绪/); await p.locator('[data-nav="overview"]').click(); assert.equal(await p.locator('#rows tr').count(),8);
  },
  async p => {
    assert.equal(await p.locator('#count-0').textContent(),'2'); await p.locator('#lane-0 .move').first().click(); assert.equal(await p.locator('#count-0').textContent(),'1'); assert.equal(await p.locator('#count-1').textContent(),'3'); await p.locator('#lane-1 .move').first().click(); assert.equal(await p.locator('#count-2').textContent(),'2'); await p.locator('#new').click(); await p.locator('#task-title').fill('准备样刊'); await p.locator('#task-description').fill('核对纸张和页码'); await p.locator('#task-form .primary').click(); assert.match(await p.locator('#lane-0').textContent(),/准备样刊/); assert.equal(await p.locator('#count-0').textContent(),'2');
  },
  async p => {
    const before=await p.locator('#curve').getAttribute('d'); await p.locator('#week').click(); assert.equal(await p.locator('#total').textContent(),'342.8'); assert.notEqual(await p.locator('#curve').getAttribute('d'),before); assert.match(await p.locator('#axis').textContent(),/周一/); assert.equal(await p.locator('#clean-label').textContent(),'当前 71%'); await p.locator('#day').click(); assert.equal(await p.locator('#total').textContent(),'48.6'); assert.match(await p.locator('#axis').textContent(),/00:00/);
  },
  async p => {
    assert.equal(await p.locator('.event').count(),7); await p.locator('[data-day="2"]').click(); assert.equal(await p.locator('#large-date').textContent(),'09'); assert.match(await p.locator('#state').textContent(),/2 项/); await p.locator('.event').filter({hasText:'香草换盆'}).click(); assert(await p.locator('#details').isVisible()); assert.match(await p.locator('#event-time').textContent(),/09 月 08 日/); assert.equal(await p.locator('#event-place').textContent(),'南侧操作台'); await p.keyboard.press('Escape'); assert(!(await p.locator('#details').isVisible()));
  },
  async p => {
    assert.equal(await p.locator('.message').count(),5); await p.locator('#star').click(); assert.equal(await p.locator('#star-count').textContent(),'2'); await p.locator('#archive').click(); assert.equal(await p.locator('#inbox-count').textContent(),'4'); await p.locator('[data-folder="archive"]').click(); assert.equal(await p.locator('.message').count(),1); await p.locator('#archive').click(); assert.equal(await p.locator('#inbox-count').textContent(),'5'); await p.locator('[data-folder="inbox"]').click(); await p.locator('#unread').check(); const n=await p.locator('.message').count(); assert(n>0); await p.locator('.message').first().click(); assert.equal(await p.locator('.message').count(),n-1); assert(await p.locator('#reading').isVisible());
  },
  async p => {
    assert.equal(await p.locator('#query').inputValue(),'月亮邮差的旅行'); await p.locator('#suggest-moon').click(); assert.equal(await p.locator('.book').count(),2); assert.match(await p.locator('#books').textContent(),/月亮与六便士/); await p.locator('#reset').click(); assert(await p.locator('#empty').isVisible()); await p.locator('#suggest-travel').click(); assert.equal(await p.locator('.book').count(),2); assert.match(await p.locator('#books').textContent(),/缓慢旅行指南/); await p.locator('#query').fill('不存在的书'); await p.locator('#search-form button').click(); assert(await p.locator('#empty').isVisible()); assert.match(await p.locator('#explanation').textContent(),/不存在的书/);
  }
];
(async()=>{
  const browser = await chromium.launch({channel:'msedge', headless:true});
  const results=[];
  try {
    for(let i=0;i<schemes.length;i++){
      const id=String(i+1).padStart(3,'0'), filename=`${id}-${schemes[i]}.html`;
      if(only.size && !only.has(id)) continue;
      const html=fs.readFileSync(path.join(root,filename),'utf8');
      for(const [,js] of html.matchAll(/<script>([\s\S]*?)<\/script>/g)) new vm.Script(js,{filename});
      const page=await browser.newPage({viewport:{width:1280,height:800},reducedMotion:'reduce'});
      const errors=[], remote=[];
      page.on('pageerror',e=>errors.push(e.message));
      page.on('request',r=>{if(/^https?:/.test(r.url()))remote.push(r.url())});
      try {
        await page.goto(pathToFileURL(path.join(root,filename)).href);
        assert.deepEqual(errors,[],filename+' JavaScript error');
        await page.screenshot({path:path.join(out,`${id}-1280.png`),fullPage:true});
        assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),filename+' desktop overflow');
        await page.setViewportSize({width:768,height:800});
        await page.screenshot({path:path.join(out,`${id}-768.png`),fullPage:true});
        assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),filename+' 768px overflow');
        await page.setViewportSize({width:1280,height:800});
        await checks[i](page);
        const regression=regressionChecks[id]?await regressionChecks[id](page):null;
        await page.screenshot({path:path.join(out,`${id}-result.png`),fullPage:true});
        assert.deepEqual(errors,[],filename+' JavaScript error after interaction');
        assert.deepEqual(remote,[],filename+' requested network resource');
        results.push({id,file:filename,status:'passed',checks:['JavaScript syntax','1280px no overflow','768px no overflow','required browser interactions','no remote requests'],regression,errors});
        console.log(id+' passed');
      } catch(e){results.push({id,file:filename,status:'failed',error:e.stack,errors}); console.error(id+' FAILED '+e.message)}
      await page.close();
    }
  } finally {await browser.close();fs.writeFileSync(path.join(out,only.size?'recheck-'+[...only].sort().join('-')+'.json':'results.json'),JSON.stringify({type:'implementation behavioral check; not independent QA',runtime:'gpt-6-astra/max',results},null,2))}
  assert.equal(results.filter(r=>r.status==='failed').length,0,'Some page checks failed; see _work/001-014-evidence/results.json');
})();
