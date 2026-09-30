import {browser} from './browser.mjs';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {dirname,resolve,join} from 'node:path';
import vm from 'node:vm';

const work=dirname(fileURLToPath(import.meta.url)),root=resolve(work,'..');
const allPieces=JSON.parse(await readFile(join(root,'model.json'),'utf8')).pieces.filter(p=>p.id>='014'&&p.id<='026');
const pieces=process.argv[2]?allPieces.filter(p=>p.id===process.argv[2]):allPieces;
const tests={
 '014':`click('[data-query="星图"]');ok($('#count').textContent==='1','改搜返回1条');ok(!$('#results').hidden&&$('#empty').hidden,'结果替换空态');$('#query').value=' ';$('#searchForm').requestSubmit();ok($('#error').textContent.includes('请输入'),'空词校验');ok(document.activeElement===$('#query'),'错误聚焦');`,
 '015':`ok($$('.notice').length===6,'6条不同通知');click('.expand');ok(!$('#detail-0').hidden,'展开详情');ok($('#unreadCount').textContent==='2 未读','展开标读');click('#markAll');ok($('#unreadCount').textContent==='0 未读'&&$('#markAll').disabled,'全部标读');click('[data-filter="unread"]');ok(!$('#emptyfeed').hidden&&$$('.notice').every(x=>x.hidden),'未读空态');`,
 '016':`click('[data-filter="设计"]');ok($$('.person').filter(x=>!x.hidden).length===2,'团队筛选');$('#memberSearch').value='不存在';$('#memberSearch').dispatchEvent(new Event('input'));ok(!$('#noresults').hidden,'姓名无结果');$('#memberSearch').value='';$('#memberSearch').dispatchEvent(new Event('input'));click('.person');ok($('#profile').open&&$('#profileName').textContent==='林屿','成员简介');click('#closeProfile');ok(!$('#profile').open,'关闭简介');`,
 '017':`const bs=$$('[data-save]');bs[0].click();bs[1].click();ok($('#saveCount').textContent==='2','收藏计数');ok(bs[0].getAttribute('aria-pressed')==='true','收藏选中');bs[0].click();ok($('#saveCount').textContent==='1'&&bs[0].textContent==='♡','取消收藏');`,
 '018':`click('#buy');ok($('#buyError').textContent.includes('请先')&&!$('#order').open,'未选套装拦截');click('[data-kit="旅行套装"]');click('[data-color="苔绿"]');click('#buy');ok($('#order').open&&$('#orderSummary').textContent.includes('苔绿')&&$('#orderSummary').textContent.includes('1,399'),'规格购买摘要');click('#closeOrder');ok(!$('#order').open&&$('#colorName').textContent==='苔绿','返回保留规格');`,
 '019':`click('.plus');ok($('#total').textContent==='¥234'&&$('#shipping').textContent==='免运费','数量同步合计与运费');click('.minus');ok($('#total').textContent==='¥188','减少恢复合计');$$('.remove')[1].click();ok($('#total').textContent==='¥152'&&$('#bagCount').textContent==='3','删除同步');click('#checkout');ok($('#checkoutDialog').open&&$('#checkoutSummary').textContent.includes('152'),'结算当前金额');click('#closeCheckout');$$('.remove').forEach(x=>x.click());ok(!$('#emptyCart').hidden&&$('#checkout').disabled&&$('#total').textContent==='¥0','空车禁止结算');`,
 '020':`click('[data-cycle="year"]');ok($$('[data-price]')[1].textContent==='38.4','年付折扣');click('[data-plan="合奏"]');ok($('#planDialog').open&&$('#planSummary').textContent.includes('460.8'),'方案摘要');$('#planForm').requestSubmit();ok($('#mailError').textContent.includes('有效'),'邮箱空值校验');$('#workmail').value='team@studio.example';$('#planForm').requestSubmit();ok(!$('#planDialog').open&&$('#feedback').textContent.includes('已确认'),'有效确认');`,
 '021':`click('#bookmark');ok($('#bookmark').getAttribute('aria-pressed')==='true','保存首篇');click('[data-index="1"]');ok($('#featureTitle').textContent==='一盏灯的来处'&&$('#featureSource').textContent.includes('阿芦'),'摘要切换');ok($('#bookmark').getAttribute('aria-pressed')==='false','第二篇独立保存状态');click('[data-index="0"]');ok($('#bookmark').getAttribute('aria-pressed')==='true','首篇保存保留');click('#bookmark');ok($('#bookmark').getAttribute('aria-pressed')==='false','取消保存');`,
 '022':`click('#follow');ok($('#followers').textContent==='1,249'&&$('#follow').getAttribute('aria-pressed')==='true','关注同步人数');click('#follow');ok($('#followers').textContent==='1,248','取消恢复人数');click('#contact');ok($('#contactDialog').open&&$('#contactDialog').textContent.includes('hello@xiaya.example'),'合作弹窗');click('#closeContact');ok(!$('#contactDialog').open,'关闭合作');`,
 '023':`click('[data-category-filter="读物"]');ok($$('.saved-item').filter(x=>!x.hidden).length===2,'分类2条');click('.remove-save');ok($('#collectionCount').textContent.startsWith('1 ')&&!$('#undo').disabled,'删除减数');click('#undo');ok($('#collectionCount').textContent.startsWith('2 ')&&$('#undo').disabled,'撤销恢复');$$('.saved-item').filter(x=>!x.hidden).forEach(x=>x.querySelector('.remove-save').click());ok(!$('#emptyCollection').hidden,'当前分类空态');click('#undo');ok($('#emptyCollection').hidden&&$('#collectionCount').textContent.startsWith('1 '),'空态恢复');`,
 '024':`$('#cardTail').value='20';$('#paymentForm').requestSubmit();ok($('#paymentError').textContent.includes('4 位'),'尾号校验');$('#cardTail').value='2048';$('#paymentForm').requestSubmit();ok($('#paymentError').textContent.includes('同意'),'条款校验');click('[value="电子钱包"]');ok($('#cardinfo').hidden&&!$('#walletNote').hidden,'支付切换');$('#agree').checked=true;$('#paymentForm').requestSubmit();ok(!$('#success').hidden&&$('#success').textContent.includes('QS-1026')&&$('#pay').disabled,'确认完成防重复');`,
 '025':`$$('details')[0].open=true;$('#nameInput').value='';$('#profileForm').requestSubmit();ok($('#profileError').textContent.includes('不能为空'),'姓名校验');$('#nameInput').value='林杉';$('#emailInput').value='wrong';$('#profileForm').requestSubmit();ok($('#profileError').textContent.includes('有效'),'邮箱校验');$('#emailInput').value='linshan@dock.example';$('#profileForm').requestSubmit();ok($('#displayName').textContent==='林杉'&&$('#displayEmail').textContent==='linshan@dock.example','资料同步');$$('details')[1].open=true;$('#newPassword').value='123';$('#passwordForm').requestSubmit();ok($('#passwordError').textContent.includes('8 位'),'密码长度校验');$('#newPassword').value='test1234';$('#confirmPassword').value='test4321';$('#passwordForm').requestSubmit();ok($('#passwordError').textContent.includes('不一致'),'重复确认校验');$('#confirmPassword').value='test1234';$('#passwordForm').requestSubmit();ok($('#newPassword').value===''&&$('#confirmPassword').value==='','完成清空密码');$$('details')[2].open=true;$$('.switch')[2].click();ok($('#notifyState').textContent==='3 项已开启','通知数量同步');`,
 '026':`ok($$('tbody tr').length===4,'4笔记录');click('#changeCard');$('#newTail').value='66';$('#cardForm').requestSubmit();ok($('#cardError').textContent.includes('4 位'),'尾号错误');$('#newTail').value='6688';$('#cardForm').requestSubmit();ok(!$('#cardDialog').open&&$('#cardDisplay').textContent.includes('6688'),'付款卡更新');window.__blobPromise=null;const create=URL.createObjectURL;URL.createObjectURL=b=>{window.__blobPromise=b.text();return create(b)};click('[data-invoice]');ok($('#feedback').textContent.includes('CP-202609-0042'),'下载反馈');`
};
const result={model:'gpt-6.1-sol',reasoningEffort:'ultra',harness:'codex',checkedAt:new Date().toISOString(),pages:[]};
const b=await browser();
try{
 for(const p of pieces){
  const html=await readFile(join(root,p.file),'utf8');
  const script=html.match(/<script>([\s\S]*?)<\/script>/)?.[1];new vm.Script(script,{filename:p.file});
  if(/<(?:script|link|img)[^>]+(?:src|href)=["']https?:/i.test(html))throw new Error('External asset: '+p.file);
  const colors=await readFile(join(root,p.spec),'utf8');
  for(const c of new Set(colors.match(/#[0-9a-fA-F]{6,8}/g)||[]))if(!html.includes(c))throw new Error('Spec color absent: '+p.id+' '+c);
  const row={id:p.id,file:p.file,checks:[],viewports:[]};
  for(const width of [1280,768,390]){
   await b.open(join(root,p.file),width,800);
   const layout=await b.evaluate(`({width:innerWidth,scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth,external:performance.getEntriesByType('resource').filter(x=>/^https?:/.test(x.name)).length})`);
   if(layout.scroll>layout.client+1)throw new Error(p.id+' overflow '+JSON.stringify(layout));
   if(layout.external)throw new Error(p.id+' external requests');
   const shot=join(work,'screenshots/014-026',p.id+'-'+width+'.png');await b.shot(shot);
   row.viewports.push({width,noHorizontalOverflow:true,screenshot:shot});
   if(width===1280){
    row.checks=await b.evaluate(`(()=>{const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)],click=s=>$(s).click(),out=[],ok=(x,m)=>{if(!x)throw new Error(m);out.push(m)};${tests[p.id]}return out})()`);
    if(p.id==='026'){
      const invoice=await b.evaluate('window.__blobPromise');
      if(!invoice.includes('CP-202609-0042')||!invoice.includes('CNY 68.00'))throw new Error('026 invoice content');
      row.checks.push('下载Blob真实内容含编号、日期、金额');
    }
    if(b.errors.length)throw new Error(p.id+' browser errors '+JSON.stringify(b.errors));
   }
   await b.call('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
   const reduced=await b.evaluate(`(()=>{const x=document.querySelector('button');return x?getComputedStyle(x).transitionDuration:'0s'})()`);
   if(reduced!=='0s')throw new Error(p.id+' reduced motion transition '+reduced);
   await b.call('Emulation.setEmulatedMedia',{features:[]});
  }
  result.pages.push(row);console.log(p.id+' PASS '+row.checks.length+' interactions / 3 viewports');
 }
 result.status='passed';
}catch(error){result.status='failed';result.error=String(error.stack);console.error(result.error);process.exitCode=1}
finally{await mkdir(work,{recursive:true});await writeFile(join(work,'runtime-014-026'+(process.argv[2]?'-'+process.argv[2]:'')+'.json'),JSON.stringify(result,null,2)+'\n');await b.close()}
