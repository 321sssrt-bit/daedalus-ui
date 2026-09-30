import {browser} from './browser.mjs';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {dirname,join} from 'node:path';
import assert from 'node:assert/strict';

const here=dirname(fileURLToPath(import.meta.url)),root=join(here,'..');
const pieces=JSON.parse(await readFile(join(root,'model.json'),'utf8')).pieces.filter(p=>p.id>='027'&&p.id<='040');
const selected=process.argv.slice(2),targets=selected.length?pieces.filter(p=>selected.includes(p.id)):pieces;
for(const p of pieces){const html=await readFile(join(root,p.file),'utf8');const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];new Function(script);const spec=await readFile(join(root,p.spec),'utf8');for(const color of spec.match(/#[0-9a-fA-F]{6,8}/g)||[])assert.ok(html.includes(color),p.id+' spec color absent in HTML: '+color);assert.ok(!/<(?:script|link|img)[^>]+(?:src|href)=["']https?:/i.test(html),p.id+' external resource');}
const shots=join(here,'screenshots/027-040');await mkdir(shots,{recursive:true});
const b=await browser();let results=[];
if(selected.length){try{results=JSON.parse(await readFile(join(here,'runtime-027-040.json'),'utf8')).results.filter(p=>!selected.includes(p.id));}catch{}}
const run=expression=>b.evaluate(expression);
const wait=ms=>new Promise(resolve=>setTimeout(resolve,ms));
const click=id=>run(`document.getElementById(${JSON.stringify(id)}).click()`);
const set=(id,value,event='input')=>run(`document.getElementById(${JSON.stringify(id)}).value=${JSON.stringify(value)};document.getElementById(${JSON.stringify(id)}).dispatchEvent(new Event(${JSON.stringify(event)},{bubbles:true}))`);
const value=id=>run(`document.getElementById(${JSON.stringify(id)}).textContent`);
const check=(ok,message)=>assert.ok(ok,message);
try{
  for(const p of targets){
    const mobile=Number(p.id)>=33;
    await b.open(join(root,p.file),mobile?390:1280,mobile?844:800);
    const initial=await run(`({overflow:document.documentElement.scrollWidth>innerWidth,lang:document.documentElement.lang,buttons:document.querySelectorAll('button').length,status:Boolean(document.querySelector('[role="status"]'))})`);
    check(!initial.overflow,p.id+' main viewport overflow');check(initial.lang==='zh-CN'&&initial.status,p.id+' accessibility structure');
    await b.shot(join(shots,p.id+'-main.png'));
    await run(`document.querySelector('button').focus()`);
    const focused=await run(`getComputedStyle(document.activeElement).outlineStyle`);check(focused!=='none',p.id+' focus visible');
    switch(p.id){
      case '027':
        check(await run(`document.querySelectorAll('tbody input').length===12`),'027 permission matrix');
        await run(`document.querySelector('[data-role="2"]').click()`);check((await value('preview-title')).includes('观察者'),'027 preview');
        await run(`document.querySelectorAll('tbody input').forEach((e,i)=>{if(i%3===2&&e.checked)e.click()})`);await click('save');check((await value('status')).includes('至少'),'027 empty-role guard');
        await run(`document.querySelectorAll('tbody input')[2].click()`);await click('save');check((await value('status')).includes('已保存'),'027 save');break;
      case '028':
        await run(`document.getElementById('application').requestSubmit()`);check((await value('status')).includes('必填'),'028 required');
        await run(`const f=document.getElementById('application');f.elements.name.value='测试申请人';f.elements.email.value='test@field.example';f.elements.project.value='山间植物观察';f.elements.description.value='沿山谷步行记录不同植物在秋季的颜色变化。';f.elements.consent.checked=true;`);
        await click('draft');check((await value('status')).includes('草稿已保存'),'028 draft');await run(`document.getElementById('application').requestSubmit()`);check((await value('status')).includes('FS-2026-0142'),'028 submit');
        await click('draft');await b.open(join(root,p.file),1280,800);check(await run(`document.getElementById('application').elements.name.value==='测试申请人'`),'028 restore');break;
      case '029':
        check(await run(`document.querySelectorAll('.file').length===2`),'029 preset queue');await click('start');await wait(1150);check((await value('percent'))==='100%','029 completion');check((await value('files')).includes('已完成'),'029 file state');
        await run(`while(document.querySelector('.remove'))document.querySelector('.remove').click()`);await click('start');check((await value('status')).includes('至少一份'),'029 empty guard');
        await run(`receive([new File(['hello'],'notes.txt',{type:'text/plain'})])`);check(await run(`document.querySelectorAll('.file').length===1`),'029 receive valid');
        await run(`receive([new File(['test'],'untrusted.exe')])`);check((await value('status')).includes('不符合'),'029 bad format');break;
      case '030':
        check(await run(`document.querySelectorAll('.entry').length===6`),'030 initial');await set('category','摄影','change');check((await value('count')).includes('2'),'030 category');await set('year','2026','change');check((await value('count')).includes('1'),'030 combined');
        await set('query','不可能存在的档案');check((await value('count')).includes('0'),'030 zero');await click('clear');check(await run(`document.querySelectorAll('.entry').length===6`),'030 clear');
        await run(`document.querySelectorAll('.entry')[1].click()`);check((await value('detail-title'))==='一座屋子的四季','030 select');break;
      case '031':
        check(await run(`document.getElementById('publish').disabled`),'031 disabled');await click('agree');check(await run(`!document.getElementById('publish').disabled`),'031 enable');await click('back');check(await run(`document.getElementById('publish').disabled && !document.getElementById('edit-view').hidden`),'031 return edit');await set('edit-title','');await click('continue');check((await value('status')).includes('不能为空'),'031 edit validation');await set('edit-title','山间来信 · 秋季刊');await click('continue');await click('agree');await click('publish');check(await run(`!document.getElementById('published').hidden`),'031 publish');break;
      case '032':
        check(await run(`document.getElementById('delete').disabled`),'032 initial guard');await set('phrase','删除');check(await run(`document.getElementById('delete').disabled`),'032 partial');await click('cancel');check((await value('result-title')).includes('保留'),'032 cancel');await click('again');await set('phrase','删除晴川档案');check(await run(`!document.getElementById('delete').disabled`),'032 exact');await click('delete');check((await value('result-title')).includes('已删除'),'032 delete');break;
      case '033':
        await click('transfer');await set('receiver','测试收款人');await set('money','9000');await run(`document.getElementById('transfer-form').requestSubmit()`);check((await value('transfer-error')).includes('超过'),'033 balance guard');check((await value('balance'))==='8,426.50','033 unchanged');
        await set('money','100');await run(`document.getElementById('transfer-form').requestSubmit()`);check((await value('balance'))==='8,326.50','033 deduction');check((await value('transactions')).includes('测试收款人'),'033 ledger');await click('toggle-balance');check((await value('balance')).includes('••'),'033 hide');await click('receive');check(await run(`document.getElementById('receive-modal').open`),'033 receive');await click('close-receive');break;
      case '034':
        await click('play');await wait(1100);check(await run(`document.getElementById('play').getAttribute('aria-label')==='暂停'`),'034 play');await click('play');check(await run(`document.getElementById('play').getAttribute('aria-label')==='播放'`),'034 pause');await click('next');check((await value('track-title'))==='雨落在石阶上','034 next');await set('progress','120');check((await value('elapsed'))==='02:00','034 progress');await click('favorite');check(await run(`document.getElementById('favorite').getAttribute('aria-pressed')==='true'`),'034 favorite');break;
      case '035':
        await click('larger');check(await run(`getComputedStyle(document.getElementById('article-body')).fontSize==='18px'`),'035 size');await click('save');check(await run(`document.getElementById('save').getAttribute('aria-pressed')==='true'`),'035 saved');await click('back');await click('read-again');check(await run(`getComputedStyle(document.getElementById('article-body')).fontSize==='18px'`),'035 preserve');break;
      case '036':
        await click('publish');check((await value('status')).includes('标题'),'036 required title');await set('title','一个慢下来的下午');await set('body','今天在窗边看见一只停留很久的鸟，它提醒我把生活的节奏放慢一点。');check((await value('count')).includes(' / 800'),'036 count');await click('draft');check((await value('status')).includes('已保存'),'036 draft');await click('publish');check(await run(`!document.getElementById('published').hidden`),'036 published');check((await value('published-title'))==='一个慢下来的下午','036 title');break;
      case '037':
        await click('create');await run(`document.getElementById('create-form').requestSubmit()`);check((await value('create-error')).includes('名称'),'037 empty');await set('trip-name','山中两日');await run(`document.getElementById('create-form').requestSubmit()`);check((await value('trips')).includes('山中两日'),'037 create');await run(`document.querySelectorAll('.checklist input').forEach(e=>e.click())`);check((await value('trips')).includes('3 / 3'),'037 ready');break;
      case '038':
        await click('retry');await wait(700);check((await value('status')).includes('仍未回应'),'038 failed retry');await click('retry');await wait(700);check((await value('home-title')).includes('恢复'),'038 recovery');break;
      case '039':
        await run(`document.getElementById('details').open=true`);check(await run(`document.getElementById('details').open`),'039 expand');await click('done');check(await run(`!document.getElementById('finished').hidden`),'039 done');await click('back');check(await run(`!document.getElementById('receipt-view').hidden`),'039 return');break;
      case '040':
        await click('aside');const before=await value('background-state');await wait(1200);check((await value('background-state'))!==before,'040 background continues');await click('resume');await click('cancel');await click('stop');check((await value('finish-title')).includes('取消'),'040 cancel');await click('again');await wait(10500);check(await run(`document.getElementById('step1').classList.contains('active')`),'040 color step');await wait(10500);check(await run(`document.getElementById('step2').classList.contains('active')`),'040 album step');await wait(9500);check((await value('finish-title')).includes('显影'),'040 finish');break;
    }
    check(b.errors.length===0,p.id+' runtime errors');
    await b.open(join(root,p.file),mobile?1280:768,mobile?900:800);
    check(await run(`document.documentElement.scrollWidth<=innerWidth`),p.id+' alternate viewport overflow');
    if(mobile)check(await run(`Math.round(document.querySelector('.phone').getBoundingClientRect().width)===390`),p.id+' wide phone');
    await b.shot(join(shots,p.id+'-'+(mobile?'wide':'768')+'.png'));
    await b.call('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
    check(await run(`getComputedStyle(document.documentElement).scrollBehavior==='auto'`),p.id+' reduced motion');
    await b.call('Emulation.setEmulatedMedia',{features:[]});
    results.push({id:p.id,mainViewport:mobile?'390x844':'1280x800',alternateViewport:mobile?'1280x900':'768x800',interaction:'passed',overflow:'passed',runtimeErrors:0,focus:'passed',reducedMotion:'passed'});
    console.log(p.id+' passed');
  }
  results.sort((a,c)=>a.id.localeCompare(c.id));
  await writeFile(join(here,'runtime-027-040.json'),JSON.stringify({checkedAt:new Date().toISOString(),browser:'Microsoft Edge headless CDP',results},null,2)+'\n');
  console.log(targets.length+' pages passed this run; '+results.length+' pages have saved runtime evidence.');
}finally{await b.close();}
