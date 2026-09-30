import {browser} from './browser.mjs';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {dirname,resolve,join} from 'node:path';
import assert from 'node:assert/strict';

const work=dirname(fileURLToPath(import.meta.url)), root=resolve(work,'..');
const pieces=JSON.parse(await readFile(join(root,'model.json'),'utf8')).pieces.filter(p=>p.id>='001'&&p.id<='013').filter(p=>!process.argv[2]||p.id===process.argv[2]);
const tests={
 '001':`$('#login').requestSubmit();if(!$('#status').textContent.includes('有效'))throw Error('empty email');$('#account').value='lin@demo.example';$('#password').value='123';$('#login').requestSubmit();if(!$('#status').textContent.includes('8'))throw Error('short password');$('#password').value='password123';$('#show').click();if($('#password').type!=='text')throw Error('show');$('#login').requestSubmit();if(!$('#status').textContent.includes('已登录'))throw Error('login');$('#forgot').click();if(!$('#status').textContent.includes('help@'))throw Error('forgot');`,
 '002':`$('#register').requestSubmit();if(!$('#status').textContent.includes('名字'))throw Error('name validation');$('#name').value='林沐';$('#journal').value='慢慢生长';$('#email').value='lin@demo.example';$('#password').value='password123';$('#register').requestSubmit();if(!$('#status').textContent.includes('同意'))throw Error('consent');$('#agree').checked=true;$('#register').requestSubmit();if(!$('#status').textContent.includes('创建成功'))throw Error('register');$('#login-link').click();if($('#signin').hidden||!$('#register').hidden||$('#loginEmail').value!=='lin@demo.example')throw Error('login route');$('#returnRegister').click();if($('#register').hidden||$('#name').value!=='林沐')throw Error('return signup');`,
 '003':`$('#code').value='BAD';$('#invite').requestSubmit();if(!$('#status').classList.contains('error'))throw Error('invalid invite');$('#code').value='night-2026';$('#invite').requestSubmit();if(!$('#status').textContent.includes('026'))throw Error('valid invite');`,
 '004':`if(!$('#back').disabled)throw Error('initial back');$('#next').click();if(!$('#title').textContent.includes('有序'))throw Error('step two');$('#next').click();if(!$('#next').textContent.includes('开始'))throw Error('step three');$('#back').click();if(!$('#title').textContent.includes('有序'))throw Error('back');$('#next').click();$('#next').click();if(!$('#status').textContent.includes('就绪'))throw Error('start');`,
 '005':`$('#reset').requestSubmit();if(!$('#status').classList.contains('error'))throw Error('email invalid');$('#email').value='reader@demo.example';$('#reset').requestSubmit();if($('#waiting').hidden||!$('#resend').disabled||!$('#sent-to').textContent.includes('reader@demo.example'))throw Error('waiting');$('#back').click();if($('#signin').hidden||!$('#reset').hidden||$('#loginEmail').value!=='reader@demo.example')throw Error('real login entry');$('#returnReset').click();if($('#reset').hidden||$('#email').value!=='reader@demo.example')throw Error('return reset retains');`,
 '006':`$('#otp').value='123';$('#verify').requestSubmit();if(!$('#status').textContent.includes('完整'))throw Error('format');for(let i=0;i<3;i++){$('#otp').value='111111';$('#verify').requestSubmit()}if(!$('#confirm').disabled||$('#resend').disabled||!$('#status').textContent.includes('锁定'))throw Error('lock');$('#resend').click();$('#otp').value='246810';$('#verify').requestSubmit();if(!$('#status').textContent.includes('成功'))throw Error('recovery');`,
 '007':`$('#create').click();if(!$('#new').open)throw Error('create dialog');$('#new-form').requestSubmit();if(!$('#dialog-error').textContent.includes('名称'))throw Error('empty project');$('#project-name').value='小花园';$('#new-form').requestSubmit();if(!$('#empty').hidden||!$('#projects').textContent.includes('小花园'))throw Error('project');`,
 '008':`$('#deny').click();if(!$('#badge').textContent.includes('关闭'))throw Error('deny');$('#once').click();if(!$('#status').textContent.includes('再次询问'))throw Error('once');$('#allow').click();if($('#allow').getAttribute('aria-pressed')!=='true'||!$('#badge').textContent.includes('授权'))throw Error('allow');`,
 '009':`document.querySelector('.task button').click();if($('#pending').textContent!=='2'||$('#completed').textContent!=='13')throw Error('counts');$('#filter').click();if(!document.querySelector('.task.done').hidden)throw Error('filter');document.querySelector('[data-view="tasks"]').click();if($('#heading').textContent!=='我的任务')throw Error('nav');`,
 '010':`const cards=document.querySelectorAll('.card');if(cards.length!==5)throw Error('initial cards');cards[0].click();if(document.querySelector('[data-col="0"] .counter').textContent!=='01'||document.querySelector('[data-col="1"] .counter').textContent!=='03')throw Error('move');$('#add').click();$('#new-form').requestSubmit();if(!$('#dialog-error').textContent.includes('标题'))throw Error('empty title');$('#title').value='新的小任务';$('#new-form').requestSubmit();if(document.querySelectorAll('.card').length!==6)throw Error('add');`,
 '011':`const path=$('#line').getAttribute('d');$('#month').click();if($('#visitors').textContent!=='31,608'||$('#line').getAttribute('d')===path||$('#month').getAttribute('aria-pressed')!=='true')throw Error('month');$('#week').click();if($('#visitors').textContent!=='8,426'||$('#line').getAttribute('d')!==path)throw Error('week');`,
 '012':`if(document.querySelectorAll('.day').length!==7||document.querySelectorAll('.event').length!==3)throw Error('initial agenda');document.querySelectorAll('.event')[1].click();if(!$('#detail').open||!$('#event-note').textContent.includes('样稿'))throw Error('details');$('#close').click();document.querySelectorAll('.day')[5].click();if(document.querySelectorAll('.event').length!==0||!$('#agenda').textContent.includes('周末'))throw Error('weekend');$('#next').click();if(!$('#status').classList.contains('error'))throw Error('boundary');`,
 '013':`document.querySelectorAll('.message')[1].click();if($('#unread-count').textContent!=='2'||!$('#subject').textContent.includes('到店'))throw Error('read');$('#star').click();if($('#star').getAttribute('aria-pressed')!=='true')throw Error('star');$('#archive').click();if(document.querySelectorAll('.message').length!==3)throw Error('archive');document.querySelector('[data-folder="archive"]').click();if(document.querySelectorAll('.message').length!==1)throw Error('folder');$('#archive').click();if(!$('#status').textContent.includes('移回'))throw Error('restore');`
};
const b=await browser(),results=[];
try{
 await mkdir(join(work,'screenshots/001-013'),{recursive:true});
 for(const p of pieces){
  const file=join(root,p.file),r={id:p.id,file:p.file,viewports:[]};
  for(const width of [1280,768,390]){
   await b.open(file,width,width===390?844:800);
   const layout=await b.evaluate(`({scroll:document.documentElement.scrollWidth,width:innerWidth,body:document.body.scrollWidth})`);
   assert(layout.scroll<=width+1&&layout.body<=width+1,`${p.id}: overflow at ${width}: ${JSON.stringify(layout)}`);
   assert.equal(b.errors.length,0,`${p.id}: runtime load exception`);
   r.viewports.push({width,overflow:false});
   if(width===1280||width===390)await b.shot(join(work,'screenshots/001-013',`${p.id}-${width}.png`));
  }
  await b.open(file,1280,800);
  await b.evaluate(`(()=>{${tests[p.id]}return true})()`);
  assert.equal(b.errors.length,0,`${p.id}: runtime interaction exception`);
  r.interactions='passed';results.push(r);console.log(p.id+' passed');
 }
 await writeFile(join(work,'runtime-001-013.json'),JSON.stringify({checkedAt:new Date().toISOString(),browser:'Edge headless via CDP',results},null,2));
}finally{await b.close()}
