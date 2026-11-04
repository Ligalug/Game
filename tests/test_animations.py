"""Presentation checks: real gameplay hooks, deterministic results, settings and skip."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from pathlib import Path
from playwright.sync_api import sync_playwright
import os
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}'
passed=[]
def ok(s): passed.append(s);print('PASS:',s,flush=True)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox','--disable-webgl'])
    page=browser.new_page(viewport={'width':1500,'height':1000})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(url);page.wait_for_function('Game.painter.ready')
    page.evaluate('Game.newGame(2026);Game.fx.configure({enabled:true,speed:1})')
    page.evaluate('''()=>{const s=Game.state; s.map[35].searched=true;s.map[35].site=null;s.factions[0].seen[36]=false;Game.moveTo(s.factions[0].armies[0],35);}''')
    page.wait_for_function("Game.fx.active?.type==='move'")
    assert page.evaluate('Game.state.factions[0].armies[0].pos')==35
    assert page.evaluate('Game.fx.revealAlpha(36)')==0
    page.wait_for_function('Game.fx.active?.p>.15')
    point=page.evaluate("Game.fx.position('map',Game.state.factions[0].armies[0].id,35,p=>({x:p,y:0})).x")
    assert 34<point<35
    page.click('#fxSkip')
    assert not page.evaluate('Game.fx.busy')
    assert page.evaluate('Game.fx.revealAlpha(36)')==1
    ok('Map motion interpolates; new terrain waits its turn; skip keeps final gameplay state')
    page.evaluate('''()=>{Game.newGame(300);Game.fx.configure({speed:1});Game.fx.roll(17,20,{mode:'map',label:'Проверка харизмы',modifier:3,dc:15,success:true});}''')
    page.wait_for_function("document.querySelector('#dicePanel').dataset.result==='success'&&!document.querySelector('#dicePanel').hidden")
    assert page.locator('#diceValue').text_content()=='17'
    assert page.locator('#diceFormula').inner_text()=='17 + 3 = 20 · КС 15'
    page.screenshot(path='/tmp/v05-dice.png')
    page.keyboard.press('Space');assert not page.evaluate('Game.fx.busy')
    ok('Animated die lands on the actual value with modifier and difficulty; keyboard skip works')
    page.evaluate('''()=>{Game.newGame(301);const a=Game.state.factions[0].armies[0];Game.startBattle(a,null,{kind:'ambush',title:'Проверка анимаций',pos:a.pos});Game.fx.finish();const b=Game.state.battle,u=b.units.find(u=>u.side===0&&u.cls==='warrior'),t=b.units.find(u=>u.side===1);u.pos=18;t.pos=19;u.ap=2;u.range=1;t.hp=t.max=100;t.ac=-100;Math.random=()=>.5;Game.attackBattle(u,t);}''')
    page.wait_for_function("Game.fx.active?.type==='dice'")
    assert page.evaluate('Game.fx.queue.some(e=>e.label==="Отдельный бросок урона")')
    assert page.evaluate('Game.fx.queue.some(e=>e.type==="effect"&&e.kind==="slash")')
    page.evaluate('Game.fx.configure({speed:4})');page.wait_for_function('!Game.fx.busy')
    assert page.evaluate("Game.fx.history.filter(e=>e.type==='dice').map(e=>e.sides)")==[20,8]
    ok('Real attack queues separate hit and damage dice followed by the impact')
    page.evaluate('''()=>{const b=Game.state.battle,u=b.units.find(u=>u.side===0&&u.cls==='acolyte'),t=b.units.find(u=>u.side===0&&u.cls==='warrior');u.pos=17;u.ap=2;t.hp=1;Game.fx.configure({speed:1});Game.spellBattle(u,t,'heal');Game.render();}''')
    page.wait_for_function("Game.fx.active?.kind==='heal'")
    assert page.evaluate('Game.fx.hp(Game.state.battle.units.find(u=>u.side===0&&u.cls===\'warrior\'))')==1
    page.screenshot(path='/tmp/v05-heal.png')
    page.evaluate('Game.fx.finish()')
    assert page.evaluate('Game.fx.hp(Game.state.battle.units.find(u=>u.side===0&&u.cls===\'warrior\'))')>1
    ok('Healing displays pre-impact HP, then resolves to the saved healed value')
    page.evaluate('Game.newGame(302);Game.fx.configure({speed:1})')
    page.click('#nav [data-a=city]');page.click('[data-a=construct]')
    page.wait_for_function("Game.fx.active?.type==='city'")
    assert page.locator('.city-scaffold').count()>0
    page.wait_for_function('document.querySelectorAll(".fx-construction").length>0')
    page.screenshot(path='/tmp/v05-construction.png')
    page.evaluate('Game.fx.finish();Game.state.factions[0].town.queue.progress=999;Game.tickFaction(Game.state.factions[0]);Game.renderCity()')
    page.wait_for_function("Game.fx.active?.kind==='complete'")
    page.evaluate('Game.fx.finish()')
    ok('Construction has persistent scaffolding and distinct start and completion effects')
    page.evaluate("""()=>{Game.newGame(304);Game.fx.configure({enabled:true,speed:1});const f=Game.state.factions[0],c=Game.makeConvoy(f,35,'bodies',[Game.createHero('warrior',2)]);Game.fx.finish();Math.random=()=>.5;Game.tickConvoys();}""")
    assert page.evaluate('Game.state.convoys.length')==0
    assert page.evaluate('Game.fx.ghosts().length')==1
    assert page.evaluate("Game.fx.queue.some(e=>e.type==='move')")
    page.evaluate('Game.fx.configure({speed:4})');page.wait_for_function('!Game.fx.busy')
    assert page.evaluate('Game.fx.ghosts().length')==0
    assert page.evaluate('Game.state.factions[0].morgue.length')==1
    ok('Arriving wagon remains visible through its travel animation, then unloads')
    page.evaluate("""()=>{Game.newGame(305);Game.fx.configure({enabled:true,speed:1});const a=Game.state.factions[0].armies[0];Game.startBattle(a,null,{kind:'ambush',title:'Движение в бою',pos:a.pos});Game.fx.finish();const b=Game.state.battle,u=b.units.find(u=>u.side===0);b.side=b.human;u.ap=2;Game.ui.battleSelected=u.id;Game.ui.mode='attack';const target=[...Game.battleReach(u).keys()].find(p=>p!==u.pos);Game.clickBattle(target);}""")
    page.wait_for_function("Game.fx.active?.type==='move'")
    before=page.evaluate('Game.state.battle.units.map(u=>u.pos)')
    page.evaluate('Game.clickBattle(25)')
    assert page.evaluate('Game.state.battle.units.map(u=>u.pos)')==before
    page.evaluate('Game.fx.finish();Game.fx.configure({autoDetail:true,speed:4});Game.autoBattle()')
    assert page.evaluate("Game.fx.queue.some(e=>e.type==='dice')")
    page.wait_for_function('!Game.fx.busy',timeout=60000)
    ok('Tactical motion locks duplicate commands; detailed autobattle plays recorded actions')
    # Compare identical seeded gameplay with and without the presentation timeline.
    result=page.evaluate('''()=>{const run=enabled=>{Game.newGame(303);Game.fx.configure({enabled});let count=0;Math.random=()=>{count++;return .5};const a=Game.state.factions[0].armies[0];Game.startBattle(a,null,{kind:'ambush',title:'RNG',pos:a.pos});Game.fx.finish();const b=Game.state.battle,u=b.units.find(u=>u.side===0&&u.cls==='warrior'),t=b.units.find(u=>u.side===1);u.pos=18;t.pos=19;u.range=1;t.hp=t.max=100;t.ac=-100;Game.attackBattle(u,t);const state=JSON.stringify(Game.state);Game.fx.finish();return{state,count}};return[run(true),run(false)]}''')
    assert result[0]==result[1]
    ok('Enabled and disabled animations consume identical randomness and produce identical game state')
    page.evaluate('Game.fx.configure({enabled:true,speed:4,autoDetail:false});Game.autoBattle()')
    assert page.evaluate("Game.fx.queue.every(e=>e.kind==='summary')")
    page.wait_for_function('!Game.fx.busy')
    ok('Default autobattle stays brief instead of replaying every roll')
    page.evaluate("Game.fx.roll(9,20,{mode:'map'});Game.fx.configure({enabled:false,speed:2})")
    assert not page.evaluate('Game.fx.busy')
    page.reload();page.wait_for_function('Game.painter.ready')
    assert page.evaluate('Game.fx.settings')=={'enabled':False,'speed':2,'autoDetail':False}
    ok('Disabling immediately unlocks controls; speed and preferences persist after reload')
    reduced=browser.new_context(reduced_motion='reduce')
    rp=reduced.new_page();rp.goto(url)
    assert not rp.evaluate('Game.fx.settings.enabled')
    reduced.close()
    assert not errors,errors
    ok('Reduced-motion preference respected; no browser errors during animated gameplay')
    browser.close()
server.shutdown()
print(f'{len(passed)} animation scenarios passed.')
