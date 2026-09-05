const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const {pathToFileURL}=require('url');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..'),temp=path.join(root,'_work','028-040-temp');
fs.mkdirSync(temp,{recursive:true});process.env.TEMP=temp;process.env.TMP=temp;
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true,env:{...process.env,TEMP:temp,TMP:temp}}),results=[];
 try{
  for(const [id,stem,selector] of [['033','033-copper-wallet','#allTransactions'],['034','034-cassette-now','#seek'],['035','035-pocket-recipe','#save']]){
   const context=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'}),page=await context.newPage();
   try{
    await page.goto(pathToFileURL(path.join(root,stem+'.html')).href);
    const geometry=await page.locator(selector).evaluate(el=>({height:el.getBoundingClientRect().height,width:el.getBoundingClientRect().width,documentWidth:document.documentElement.scrollWidth,viewportWidth:innerWidth}));
    assert(geometry.documentWidth<=390,'Horizontal overflow');
    if(id==='033'){await page.locator(selector).click();assert.equal(await page.locator('#historyView').isVisible(),true);}
    if(id==='034'){await page.locator(selector).fill('60');assert.equal(await page.locator('#elapsed').textContent(),'01:00');}
    if(id==='035'){await page.locator(selector).click();assert.equal(await page.locator(selector).getAttribute('aria-pressed'),'true');}
    results.push({id,selector,...geometry,status:geometry.height>=44?'passed':'failed',behavior:'passed'});
    console.log(id+' height='+geometry.height+'px, document='+geometry.documentWidth+'px, behavior passed');
   }finally{await context.close();}
  }
 }finally{await browser.close();fs.writeFileSync(path.join(__dirname,'028-040-touch-'+(process.argv[2]||'results')+'.json'),JSON.stringify(results,null,2)+'\n');}
 assert(results.every(r=>r.status==='passed'),'Every touch target must be at least 44px tall');
})().catch(e=>{console.error(e.message);process.exitCode=1;});
