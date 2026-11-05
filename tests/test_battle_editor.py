"""Regression scenarios for ranged engagement, class defenses, barrier and custom terrain."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright
import json,os
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/battle-lab.html'
passed=[]
def ok(t):passed.append(t);print('PASS:',t,flush=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
 p=b.new_page(viewport={'width':1700,'height':1200});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto(url);p.uncheck('#motion')
 p.evaluate("Object.assign(Lab.state.units[4],{q:3,r:4});Object.assign(Lab.state.units[5],{q:6,r:4});Lab.render()")
 p.click('[data-select="p1"]')
 assert p.locator('[data-action="attack"]').is_disabled() and p.locator('[data-action="frost"]').is_disabled()
 assert 'Рядом враг' in p.locator('[data-action="attack"]').get_attribute('title')
 assert not p.evaluate("Lab.apply(Lab.state.units[1],Lab.state.units[5],'attack')")
 assert p.evaluate('Lab.state.units[1].ap')==3
 p.locator('[data-q="1"][data-r="4"]').click()
 assert p.locator('[data-action="attack"]').is_enabled()
 assert p.evaluate("Lab.forecast(Lab.state.units[1],Lab.state.units[5],'attack').ok")
 p.evaluate("Object.assign(Lab.state.units[6],{q:0,r:4});Lab.render()")
 assert p.locator('[data-action="attack"]').is_disabled()
 ok('Adjacent enemies prevent ranged shots and specials; moving away must clear all adjacent threats')
 result=p.evaluate("()=>{Lab.reset();const mage=Lab.state.units[3],enemy=Lab.state.units[4],ally=Lab.state.units[0];Object.assign(enemy,{q:3,r:6});ally.hp=10;return {shot:Lab.check(mage,enemy,'attack'),heal:Lab.check(mage,ally,'heal'),plan:Lab.approach(mage,[enemy])}}")
 assert 'Рядом враг' in result['shot'] and result['heal']=='' and result['plan'] is not None
 ok('Engagement also blocks offensive magic while healing remains legal; escape path exists')
 result=p.evaluate("()=>{Lab.reset();const u=Lab.state.units[0],t=Lab.state.units[3],d={lo:10,hi:10,damage:'piercing',name:'Тест',undodgeable:true};const a=Lab.hit(u,t,d),after1={hp:t.hp,barrier:t.barrier},c=Lab.hit(u,t,d),after2={hp:t.hp,barrier:t.barrier};Lab.startSide(1);const enemyTurn=t.barrier;Lab.startSide(0);const ownTurn=t.barrier;for(let i=0;i<5;i++)Lab.startSide(0);return {a,c,after1,after2,enemyTurn,ownTurn,cap:t.barrier}}")
 assert result['after1']=={'hp':24,'barrier':3} and result['after2']=={'hp':18,'barrier':0}
 assert result['enemyTurn']==0 and result['ownTurn']==4 and result['cap']==12
 ok('Mage barrier absorbs post-defense damage, regenerates only on own turns and caps at twelve')
 result=p.evaluate("()=>{Lab.reset();const u=Lab.state.units[0],t=Lab.state.units[3];Lab.hit(u,t,{lo:1000,hi:1000,damage:'piercing',name:'Тест',undodgeable:true});Lab.startSide(0);return {hp:t.hp,barrier:t.barrier,ap:t.ap}}")
 assert result=={'hp':0,'barrier':0,'ap':0}
 ok('Unconscious mage gains neither barrier nor actions')
 result=p.evaluate("()=>{let misses=0,hits=0;for(let i=0;i<40;i++){Lab.reset();const u=Lab.state.units[0],t=Lab.state.units[5];Object.assign(t,{q:3,r:3});Lab.state.seed=i*1000003;const before=t.hp;Lab.apply(u,t,'break');if(t.hp===before){misses++;if(t.exposed||u.ap!==1||u.cooldown!==3)throw Error('Miss caused a debuff or free action')}else hits++}return {misses,hits}}")
 assert 0<result['misses']<40 and result['hits']>0
 p.select_option('#squad','classic');p.click('[data-select="p2"]');assert 'уворот 25%' in p.inner_text('#stats')
 p.click('[data-select="p1"]');assert 'уворот 20%' in p.inner_text('#stats')
 ok('Dodge genuinely avoids attacks and debuffs but still spends attacker AP and cooldown; percentages are visible')
 p.evaluate('Lab.reset()');assert p.locator('.hero-figure').count()==8
 assert p.locator('.hero-figure[data-class="warrior"] path').count()>3
 assert p.locator('.hero-figure[data-class="acolyte"] path').count()>3
 assert p.locator('.barrier-aura').count()==2
 ok('Heroes render as distinct equipped figures, with a separate mage barrier aura')
 p.click('#editorToggle');assert p.evaluate('Lab.editing')
 assert p.locator('#end').is_disabled() and p.locator('[data-action="attack"]').is_disabled()
 p.select_option('#terrainBrush','rock');p.select_option('#heightBrush','1');p.locator('[data-q="6"][data-r="3"]').click()
 assert p.evaluate("Lab.state.tiles['6,3'].kind==='rock'&&Lab.state.tiles['6,3'].height===1&&Lab.state.actions===0")
 p.locator('[data-q="2"][data-r="3"]').click()
 assert p.evaluate("Lab.state.tiles['2,3'].kind==='plain'")
 assert 'защищен' in p.inner_text('#editorStatus')
 p.click('#saveLayout');p.click('#restart')
 assert p.evaluate("!Lab.editing&&Lab.state.tiles['6,3'].kind==='rock'")
 p.reload();p.uncheck('#motion')
 assert p.evaluate("Lab.state.tiles['6,3'].kind==='rock'&&Lab.state.tiles['6,3'].height===1")
 ok('Editor pauses combat, protects hero starts and preserves custom terrain across restart and reload')
 p.click('#editorToggle')
 with p.expect_download() as dl:p.click('#exportLayout')
 layout=json.loads(Path(dl.value.path()).read_text());assert len(layout['tiles'])==160
 before=p.evaluate('JSON.stringify(Lab.state.tiles)')
 p.locator('#layoutFile').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{"format":"bad"}'})
 p.wait_for_function("document.getElementById('editorStatus').textContent.includes('Неверный')")
 assert p.evaluate('JSON.stringify(Lab.state.tiles)')==before
 p.click('#restoreLayout');assert p.evaluate("Lab.state.tiles['6,3'].kind==='plain'")
 p.locator('#layoutFile').set_input_files({'name':'map.json','mimeType':'application/json','buffer':json.dumps(layout).encode()})
 p.wait_for_function("document.getElementById('editorStatus').textContent.includes('загружено')")
 assert p.evaluate("Lab.state.tiles['6,3'].kind==='rock'")
 ok('Map export/import round-trips; invalid input leaves the current map untouched')
 with p.expect_download() as dl:p.click('#download')
 raw=Path(dl.value.path()).read_text()
 fresh=b.new_context();copy=fresh.new_page();copy.route('**/*',lambda route:route.abort());copy.set_content(raw)
 assert copy.evaluate("Lab.state.tiles['6,3'].kind==='rock'&&Lab.state.tiles['6,3'].height===1&&!Lab.editing")
 fresh.close()
 ok('Standalone game copy includes the custom terrain without requiring browser storage or network')
 p.click('#restoreLayout');p.click('#editorToggle');p.evaluate("const u=Lab.state.units[0];Object.assign(u,{q:5,r:3});Lab.state.tiles['6,3'].height=1;Lab.render()")
 assert p.evaluate("Lab.paths(Lab.state.units[0]).get('6,3').cost")==2
 p.evaluate("Lab.state.tiles['6,3'].height=2;Lab.render()")
 assert not p.evaluate("Lab.paths(Lab.state.units[0]).has('6,3')")
 assert not p.evaluate('Lab.los({q:5,r:3},{q:8,r:3})')
 p.evaluate("Lab.state.tiles['6,3'].height=0;Lab.state.tiles['6,3'].kind='water';Lab.render()")
 assert not p.evaluate("Lab.paths(Lab.state.units[0]).has('6,3')")
 p.evaluate("Lab.state.tiles['6,3'].kind='forest'")
 assert not p.evaluate('Lab.los({q:5,r:3},{q:8,r:3})')
 ok('Elevation changes path cost and line of sight; steep cliffs, forests and water block movement')
 p.evaluate('Lab.reset()');p.locator('[data-q="3"][data-r="3"]').click();p.click('#editorToggle')
 assert not p.evaluate('Lab.editing') and 'до первого действия' in p.inner_text('#notice')
 ok('Editor cannot change the battlefield after combat actions have begun')
 p.evaluate("Lab.reset('cover')");p.click('#editorToggle');p.select_option('#terrainBrush','water');p.locator('[data-q="6"][data-r="6"]').click();p.screenshot(path='/tmp/battle-lab-083-editor.png',full_page=True)
 p.click('#editorToggle');p.click('[data-select="p3"]');p.click('[data-action="attack"]');p.screenshot(path='/tmp/battle-lab-083-figures.png',full_page=True)
 p.set_viewport_size({'width':390,'height':844});p.click('#editorToggle')
 assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert not errors,errors
 ok('Editor and figures work on desktop and narrow screens without script errors')
 b.close()
server.shutdown()
print(len(passed),'editor and combat scenarios passed.')
