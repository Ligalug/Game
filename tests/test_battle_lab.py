"""Browser scenarios for movement packets, typed mitigation, engineers and explicit passes."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright
import os,json
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
passed=[]
def ok(text):passed.append(text);print('PASS:',text,flush=True)
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
 p=browser.new_page(viewport={'width':1600,'height':1100});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto(base+'/battle-lab.html');p.uncheck('#motion');p.fill('#critChance','0');p.dispatch_event('#critChance','change')
 assert p.locator('.tile').count()==160
 assert p.evaluate('Lab.state.units.length===8&&Lab.state.units.every(u=>u.ap===3)')
 assert p.evaluate('Lab.state.units.filter(u=>u.type==="engineer").length')==2
 ok('Expanded 16x10 map keeps four heroes per side, including engineers')
 p.locator('[data-q="3"][data-r="3"]').click()
 assert p.evaluate('Lab.state.units[0].ap===2&&Lab.state.units[0].stride===2')
 p.locator('[data-q="5"][data-r="3"]').click()
 assert p.evaluate('Lab.state.units[0].ap===2&&Lab.state.units[0].stride===0')
 p.locator('[data-q="6"][data-r="3"]').click()
 assert p.evaluate('Lab.state.units[0].ap===1&&Lab.state.units[0].stride===2')
 p.locator('[data-q="12"][data-r="3"]').click()
 assert p.evaluate('Lab.state.units[0].q===6&&Lab.state.units[0].ap===1')
 p.evaluate("Object.assign(Lab.state.units[4],{q:7,r:3});Lab.render()")
 p.click('[data-action="attack"]');p.locator('[data-q="7"][data-r="3"]').click()
 assert p.evaluate('Lab.state.units[0].ap===0&&Lab.state.units[0].stride===2')
 p.click('[data-action="move"]');p.locator('[data-q="6"][data-r="2"]').click()
 assert p.evaluate('Lab.state.units[0].ap===0&&Lab.state.units[0].stride===1&&Lab.pending().some(u=>u.id==="p0")')
 ok('Three cells cost one AP across separate clicks; exceeding the remaining movement budget is rejected')
 result=p.evaluate("()=>{Lab.reset('cover');const u=Lab.state.units[0];Object.assign(u,{q:5,r:3});const normal=Lab.paths(u).get('6,3');u.slow=1;const slow=Lab.paths(u).get('6,3');return {normal:normal.cost,slow:slow.cost,rock:Lab.paths(u).has('7,3')}}")
 assert result=={'normal':2,'slow':3,'rock':False}
 ok('Mud and slowing spend extra steps; rocks remain impassable')
 result=p.evaluate("()=>{Lab.reset();const vals=[0,25,50,100,200].map(Lab.reduction),u=Lab.state.units[0],t=Lab.state.units[4];const damage={};for(const type of ['piercing','slashing','magic'])damage[type]=Lab.damageForecast(u,t,{lo:10,hi:10,damage:type}).lo;return {vals,damage}}")
 assert result['damage']=={'piercing':7,'slashing':5,'magic':8}
 assert abs(result['vals'][1]-1/3)<1e-8 and result['vals'][2]==.5
 assert result['vals'][3]-result['vals'][2]>result['vals'][4]-result['vals'][3]>0
 ok('Three defenses mitigate their own damage type with diminishing percentage gains')
 result=p.evaluate('''()=>{const hits=[];for(let i=0;i<30;i++){Lab.reset();const u=Lab.state.units[i%4],t=Lab.state.units[4];Object.assign(t,{q:u.q+(Lab.spec(u,'attack').range>1?2:1),r:u.r});const f=Lab.forecast(u,t,'attack'),before=t.hp;Lab.state.seed=i*197;Lab.apply(u,t,'attack');hits.push(f.ok&&before-t.hp>=f.lo&&before-t.hp<=f.hi&&u.ap===2)}return hits.every(Boolean)}''')
 assert result
 p.evaluate("Lab.reset();Lab.guard(Lab.state.units[4]);Lab.state.units[0].q=12;Lab.render()")
 f=p.evaluate("Lab.forecast(Lab.state.units[0],Lab.state.units[4],'attack')")
 assert f['defense']==75 and not p.evaluate('Lab.guard(Lab.state.units[4])')
 ok('Real hits match typed forecasts; guarding adds twenty rating without stacking')
 p.evaluate("Lab.reset('cover')");p.click('[data-select="p1"]');p.click('[data-action="attack"]')
 assert p.locator('.range-clear').count()>0
 assert p.locator('[data-q="15"][data-r="9"]').get_attribute('data-range')==''
 p.evaluate("Lab.state.tiles['4,4'].kind='rock';Lab.render()")
 assert p.locator('[data-q="6"][data-r="4"]').get_attribute('data-range')=='blocked'
 p.click('[data-action="frost"]');assert p.locator('.range-clear').count()>0
 p.click('[data-select="p3"]');p.click('[data-action="heal"]');assert p.locator('.range-clear').count()>0
 ok('Ranged attacks, specials and healing highlight radius; blocked line of sight is distinguished')
 p.select_option('#scenario','rescue');p.click('[data-action="heal"]');p.locator('[data-q="7"][data-r="5"]').hover()
 assert 'Подъём с 1 ОД' in p.inner_text('#forecast')
 p.locator('[data-q="7"][data-r="5"]').click()
 assert p.evaluate('Lab.state.units[0].hp===10&&Lab.state.units[0].ap===1&&Lab.state.units[3].ap===1')
 p.click('[data-select="p0"]');p.locator('[data-q="8"][data-r="5"]').click()
 assert p.evaluate('Lab.state.units[0].ap===0&&Lab.state.units[0].stride===2')
 assert p.locator('[data-action="attack"]').is_disabled()
 ok('Revived hero has one AP, buying at most three steps and no extra attack')
 p.evaluate('Lab.reset()');p.click('#end')
 assert p.evaluate('Lab.state.round===1&&Lab.state.side===0')
 assert p.locator('[data-skip]').count()==4
 p.click('[data-skip="p0"]');assert p.evaluate('Lab.state.units[0].skipped&&Lab.state.units[0].ap===0')
 p.click('#skipAll');p.click('#end');p.wait_for_function('!Lab.busy')
 assert p.evaluate('Lab.state.round===2&&Lab.state.units.filter(u=>u.side===0).every(u=>!u.skipped&&u.stride===0)')
 ok('End turn blocks outstanding heroes; individual and explicit group passes allow progress')
 p.evaluate("Lab.reset();Object.assign(Lab.state.units[4],{q:3,r:3});Lab.render()")
 p.click('[data-action="break"]');p.locator('[data-q="3"][data-r="3"]').click()
 assert p.evaluate('Lab.state.units[0].ap===1&&Lab.state.units[0].cooldown===3&&Lab.state.units[4].exposed===1')
 p.evaluate('Lab.skipAll()');p.click('#end');p.wait_for_function('!Lab.busy')
 assert p.evaluate('Lab.state.round===2&&Lab.state.units[4].exposed===0&&Lab.state.units[0].cooldown===3')
 ok('Special costs and cooldowns remain valid; physical-defense debuff expires after target turn')
 p.select_option('#engineerSub','armorer');p.click('[data-select="p2"]');p.click('[data-action="powerarmor"]')
 assert p.evaluate('Lab.state.units[2].ap===1&&Lab.state.units[2].power===2&&Lab.defense(Lab.state.units[2],"piercing")===60&&Lab.spec(Lab.state.units[2],"attack").lo===7')
 assert not p.evaluate('Lab.activateArmor(Lab.state.units[2])')
 assert 'Бронник' in p.inner_text('#selected')
 ok('Armorer activates personal power armor, raises all defenses and damage, and cannot stack it')
 p.select_option('#engineerSub','demolitionist');p.click('[data-select="p2"]');p.click('[data-action="mine"]');p.locator('[data-q="4"][data-r="5"]').click()
 assert p.evaluate('Lab.state.mines.length===1&&Lab.state.units[2].ap===1')
 p.evaluate("Object.assign(Lab.state.units[0],{q:3,r:5});Object.assign(Lab.state.units[4],{q:5,r:5});for(const u of Lab.state.units.filter(u=>u.side===1&&u.id!=='e0')){u.hp=0;u.ap=0}Lab.skipAll()")
 p.click('#end');p.wait_for_function('!Lab.busy')
 assert p.evaluate('Lab.state.mines.length===0&&Lab.state.units[4].hp<Lab.state.units[4].max&&Lab.state.log.some(t=>t.includes("Мина"))')
 ok('Demolitionist lays a mine; an enemy walking onto it takes real typed damage and consumes the trap')
 p.select_option('#engineerSub','fortifier');p.click('[data-select="p2"]');p.click('[data-action="fortify"]');p.locator('[data-q="4"][data-r="5"]').click()
 assert p.evaluate("Lab.state.tiles['4,5'].fort&&Lab.state.tiles['4,5'].kind==='cover'")
 p.evaluate("Lab.state.tiles['3,5'].kind='mud';Lab.render()")
 p.click('[data-action="bridge"]');p.locator('[data-q="3"][data-r="5"]').click()
 assert p.evaluate("Lab.state.tiles['3,5'].kind==='bridge'&&Lab.state.units[2].ap===0")
 result=p.evaluate("()=>{const u=Lab.state.units[1],t=Lab.state.units[4];Object.assign(t,{q:4,r:5});return Lab.damageForecast(u,t,Lab.spec(u,'attack')).cover}")
 assert result==35
 ok('Fortifier builds an improved ranged cover and bridge; bridge remains available during fortification cooldown')
 p.select_option('#engineerSub','base');p.check('#motion');p.evaluate('Lab.skipAll()');p.click('#end');p.click('#restart');p.wait_for_timeout(700)
 assert p.evaluate('Lab.state.round===1&&Lab.state.side===0&&!Lab.busy&&Lab.state.actions===0')
 p.uncheck('#motion');p.fill('#critChance','0');p.dispatch_event('#critChance','change')
 ok('Restart cancels pending animated AI actions')
 p.evaluate("Lab.reset();for(const u of Lab.state.units.filter(u=>u.side===1)){u.hp=0;u.ap=0};Object.assign(Lab.state.units[4],{q:3,r:3,hp:1});Lab.state.units[3].hp=0;Lab.state.units[3].ap=0;Lab.render()")
 p.click('[data-action="attack"]');p.locator('[data-q="3"][data-r="3"]').click()
 assert p.evaluate('Lab.state.winner===0&&Lab.state.units[3].hp===1')
 assert p.locator('#result').is_visible() and p.locator('#end').is_disabled()
 ok('Battle ends when a squad falls; winners revive allies at one HP')
 p.select_option('#squad','classic')
 with p.expect_download() as dl:p.click('#download')
 dl.value.save_as('/tmp/battle-lab-copy.html')
 copy=browser.new_page();copy.route('**/*',lambda route:route.abort());copy.set_content(Path('/tmp/battle-lab-copy.html').read_text())
 assert copy.evaluate('Lab.state.round===1&&Object.keys(Lab.state.tiles).length===160')
 assert copy.evaluate("document.getElementById('squad').value!=='engineer'||!document.getElementById('engineerSub').disabled")
 copy.close();p.locator('summary').last.click()
 with p.expect_download() as dl:p.click('#report')
 result=json.loads(Path(dl.value.path()).read_text())
 assert result['version']=='0.8.5-lab'
 ok('Standalone backup boots offline; exported report identifies updated version')
 p.goto(base);p.wait_for_function('Game.painter.ready');p.get_by_role('button',name='Пробный бой 4 на 4',exact=True).click()
 frame=p.frame_locator('#battleLabOverlay iframe');frame.locator('#phase').wait_for();p.locator('#battleLabOverlay > button').click()
 p.evaluate('Game.newGame(813);Game.fx.configure({enabled:false})');before=p.evaluate('JSON.stringify(Game.state)')
 p.evaluate("document.getElementById('openBattleLab').click()")
 frame.locator('#engineerSub').select_option('armorer');frame.locator('#end').click();frame.locator('#skipAll').click();frame.locator('#end').click()
 p.wait_for_timeout(200);p.locator('#battleLabOverlay > button').click()
 assert p.evaluate('JSON.stringify(Game.state)')==before
 ok('Integrated experiment leaves campaign state unchanged')
 p.goto(base+'/battle-lab.html');p.uncheck('#motion');p.fill('#critChance','0');p.dispatch_event('#critChance','change')
 summaries=p.evaluate("""async()=>{const results=[];for(const sub of ['base','armorer','demolitionist','fortifier']){document.getElementById('engineerSub').value=sub;for(const scenario of ['equal','cover','rescue']){Lab.reset(scenario);let rounds=0;while(Lab.state.winner===null&&rounds++<30){for(const u of Lab.state.units.filter(u=>u.side===0&&u.hp>0)){document.querySelector('[data-select="'+u.id+'"]').click();let n=0;while((u.ap>0||u.stride>0)&&Lab.state.winner===null&&n++<10){let done=false;if(u.type==='acolyte'){const t=Lab.state.units.filter(t=>t.side===0&&t.hp<=t.max-10).sort((a,b)=>a.hp-b.hp).find(t=>!Lab.check(u,t,'heal'));if(t)done=Lab.apply(u,t,'heal')}if(!done){const options=[];for(const t of Lab.state.units.filter(t=>t.side===1&&t.hp>0)){const f=Lab.forecast(u,t,'attack');if(f.ok)options.push({t,f})}options.sort((a,b)=>a.t.hp-b.t.hp);if(options.length)done=Lab.apply(u,options[0].t,'attack')}if(!done){const dest=Lab.approach(u,Lab.state.units.filter(t=>t.side===1&&t.hp>0));if(dest){await Lab.chooseTile(dest.q,dest.r);done=true}}if(!done)break}}if(Lab.state.winner===null){Lab.skipAll();await Lab.endTurn()}}results.push({sub,scenario,winner:Lab.state.winner,round:Lab.state.round,actions:Lab.state.actions})}}return results}""")
 assert all(r['winner'] is not None and r['round']<=30 for r in summaries),summaries
 print('Completion metrics:',summaries,flush=True)
 ok('All scenarios reach a result with each engineer subclass; no AI or turn-lock deadlocks')
 p.goto(base+'/battle-lab.html');p.select_option('#scenario','cover');p.click('[data-select="p1"]');p.click('[data-action="attack"]');p.screenshot(path='/tmp/battle-lab-084-cover.png',full_page=True)
 p.set_viewport_size({'width':390,'height':844});p.screenshot(path='/tmp/battle-lab-084-mobile.png',full_page=True)
 assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert not errors,errors
 ok('Desktop and mobile preserve readable controls and contained map scrolling without browser errors')
 browser.close()
server.shutdown()
print(f'{len(passed)} battle lab scenarios passed.')
