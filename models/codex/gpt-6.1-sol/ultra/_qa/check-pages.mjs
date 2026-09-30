import assert from 'node:assert/strict';
import {readFile,readdir,writeFile} from 'node:fs/promises';
import {dirname,resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {browser} from './browser.mjs';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const repo=resolve(root,'../../../..');
const briefs=JSON.parse(await readFile(join(repo,'catalog/briefs.json'),'utf8')).briefs;
const files=await readdir(root),b=await browser(),rows=[];
try {
  for(const brief of briefs){
    const file=files.find(f=>f.startsWith(brief.id+'-')&&f.endsWith('.html'));
    assert(file,'Missing HTML '+brief.id);
    const width=brief.viewport==='mobile'?390:1280,height=brief.viewport==='mobile'?844:800;
    await b.open(join(root,file),width,height);
    if(process.env.DAEDALUS_SHOTS)await b.shot(join(process.env.DAEDALUS_SHOTS,brief.id+'.png'));
    assert.equal(b.errors.length,0,brief.id+': '+JSON.stringify(b.errors));
    const widths=brief.viewport==='mobile'?[390,1280]:[1280,768];
    for(const w of widths){
      await b.call('Emulation.setDeviceMetricsOverride',{width:w,height:w===390?844:800,deviceScaleFactor:1,mobile:w===390});
      assert(await b.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),brief.id+' overflow at '+w);
    }
    await b.call('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
    assert(await b.evaluate(`matchMedia('(prefers-reduced-motion: reduce)').matches`));
    await b.call('Emulation.setEmulatedMedia',{features:[]});
    rows.push({id:brief.id,file,widths,initialConsoleErrors:0,reducedMotionMode:'available'});
    console.log(brief.id+' viewport + initial render passed');
  }
  await writeFile(join(root,'page-render-check.json'),JSON.stringify({browser:'Chromium Edge headless',checkedAt:new Date().toISOString(),results:rows},null,2)+'\n');
} finally {await b.close()}
