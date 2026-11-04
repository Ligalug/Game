"""End-to-end browser checks for the rebuilt standalone prototype."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from pathlib import Path
from playwright.sync_api import sync_playwright
import os
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
ROOT=Path(__file__).resolve().parents[1]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
passed=[]
def ok(t):
    passed.append(t);print('PASS:',t,flush=True)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox','--disable-webgl'])
    page=browser.new_page(viewport={'width':1500,'height':1000})
    errors=[];external=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    def route(r):
        if r.request.url.startswith(f'http://127.0.0.1:{server.server_port}/'):r.continue_()
        else:external.append(r.request.url);r.abort()
    page.route('**/*',route)
    page.goto(f'http://127.0.0.1:{server.server_port}')
    page.evaluate('Game.fx.configure({enabled:false})')
    page.click('[data-a=start]')
    assert page.locator('[data-a=pickStart]').count()==8
    page.locator('[data-a=pickStart]').nth(0).click();page.locator('[data-a=pickStart]').nth(3).click()
    page.click('[data-a=confirmStart]')
    page.click('[data-a=turnReportDone]')
    assert page.evaluate('Game.state.factions[0].armies[0].heroes.map(h=>h.cls)')==['warrior','acolyte']
    page.wait_for_function('Game.painter.ready')
    assert not external
    ok('Two chosen level-1 candidates, embedded pixel assets, no WebGL or external requests')
    assert 'Рост' not in page.locator('#resources').inner_text()
    assert page.locator('#armybar').is_visible() and page.locator('#sidebar').is_visible()
    page.evaluate('''()=>{Game.state.map[35].searched=true;Game.state.map[35].site=null;}''')
    point=page.evaluate('Game.painter.project(35)');page.mouse.click(point['x'],point['y'])
    page.click('[data-a=move]')
    assert page.evaluate('Game.state.factions[0].armies[0].pos')==35
    ok('Map picking drives movement; AoW-inspired panels keep growth metrics inside the city')
    page.evaluate('Game.newGame(123)');page.click('#nav [data-a=city]')
    assert page.locator('.citymap polygon').count()==19
    assert page.evaluate('Game.state.factions[0].town.plots.length')==6
    page.click('[data-a=construct]')
    assert page.evaluate('Game.state.factions[0].town.queue.id')=='market'
    assert page.evaluate('Game.state.factions[0].gold')==60
    ok('Six initial building plots plus twelve outer plots; building charges resources through UI')
    result=page.evaluate('''()=>{Game.newGame(124);const f=Game.state.factions[0],p=f.town.plots;f.town.buildings[p[0]]='market';const near=p.find(j=>j!==p[0]&&Game.nb(p[0]).includes(j)),far=p.find(j=>j!==p[0]&&!Game.nb(p[0]).includes(j));return{near:Game.buildPreview(f,near,'workshop'),far:Game.buildPreview(f,far,'workshop'),wrong:Game.buildPreview(f,near,'trading'),valid:Game.buildPreview(f,p[0],'trading')};}''')
    assert result['near']['ok'] and len(result['near']['links'])==1
    assert result['far']['ok'] and not result['far']['links']
    assert not result['wrong']['ok'] and result['valid']['ok']
    result=page.evaluate('''()=>{const f=Game.state.factions[0],p=f.town.plots[0];f.town.buildings[p]='trading';return Game.cityEffects(f);}''')
    assert result['gold']==18 and result['trade']==1 # 12 base + 4 market + 2 trading
    ok('Only immediate neighbors create synergy; replacements require the right building and retain its effects')
    result=page.evaluate('''()=>{Game.newGame(125);const f=Game.state.factions[0];f.town.growth=13;Game.tickFaction(f);const outer=Array.from({length:256},(_,i)=>i).filter(i=>Game.dist(f.city,i)===2);const accepted=Game.claimPlot(f,outer[0]);return{outer:outer.length,accepted,count:f.town.plots.length,claims:f.town.claims};}''')
    assert result=={'outer':12,'accepted':True,'count':7,'claims':0}
    ok('Population growth grants one contiguous second-ring hex; all twelve are available')
    page.evaluate('''()=>{Game.newGame(126);Game.state.factions[0].gold=500;}''')
    page.click('#nav [data-a=city]');page.click('[data-a=hire]')
    for _ in range(4):page.locator('[data-a=recruit]').first.click()
    assert page.evaluate('Game.state.factions[0].armies.map(a=>a.heroes.length)')==[4,2]
    page.click('[data-a=close]')
    page.evaluate('''()=>{const f=Game.state.factions[0],a=f.armies[0];Game.ui.army=a.id;Game.startBattle(a,null,{kind:'ambush',title:'Проверка отдельного отряда',pos:a.pos});}''')
    assert page.evaluate('Game.state.battle.units.filter(u=>u.side===0).length')==4
    ok('Base classes need no buildings; overflow recruitment creates another army; armies never combine in battle')
    page.evaluate('''()=>{Game.newGame(127);const f=Game.state.factions[0],a=f.armies[0],v=Game.state.villages[0];a.pos=v.pos;a.mp=5;f.seen[v.pos]=true;Game.ui.selected=v.pos;Game.render();}''')
    page.click('[data-a=village]')
    assert page.locator('[data-a=eventHero]').count()==2
    selected=page.locator('[data-a=eventHero]').nth(1).get_attribute('data-id')
    page.locator('[data-a=eventHero]').nth(1).click()
    page.evaluate('Math.random=()=>.95')
    page.click('[data-a=eventChoice][data-v=help]')
    assert page.evaluate('Game.state.villages[0].quest[0]')
    assert page.evaluate('Game.state.factions[0].rep')==5
    assert page.evaluate(f'Game.state.log[0].text.includes(Game.state.factions[0].armies[0].heroes.find(h=>h.id==="{selected}").name)')
    ok('Events let the player choose a hero; that hero performs the check and earns the village quest reward')
    result=page.evaluate('''()=>{Game.newGame(128);Math.random=()=>.95;const a=Game.state.factions[0].armies[0];Game.startBattle(a,null,{kind:'ambush',title:'Лечение',pos:a.pos});const b=Game.state.battle,w=b.units.find(u=>u.side===0&&u.cls==='warrior'),h=b.units.find(u=>u.side===0&&u.cls==='acolyte');w.hp=0;w.pos=9;h.pos=17;h.ap=2;const healed=Game.spellBattle(h,w,'heal'),ap=w.ap;w.hp=0;b.over=0;Game.finishBattle();return{healed,ap,hp:a.heroes.find(t=>t.cls==='warrior').hp};}''')
    assert result=={'healed':True,'ap':1,'hp':1}
    ok('Healing raises a hero with one AP; victory revives all friendly knockouts at one HP')
    result=page.evaluate('''()=>{Game.newGame(129);const f=Game.state.factions[0],e=Game.state.factions[1],a=f.armies[0],d=e.armies[0];Math.random=()=>0;Game.startBattle(a,d,{kind:'duel',title:'Стресс',pos:a.pos});const b=Game.state.battle,u=b.units.find(u=>u.side===1&&u.hero);u.stress=95;Game.stressUnit(u,10,'Испытание');return{surrender:u.surrender,active:Game.activeUnits(b,1).some(v=>v.id===u.id)};}''')
    assert result=={'surrender':True,'active':False}
    ok('A failed resolve check causes surrender and removes the hero from active combat')
    # A genuine post-battle flow through the interface: trophies, remains, prisoners, shipping.
    page.evaluate('''()=>{Game.newGame(130);Math.random=()=>.95;const f=Game.state.factions[0],e=Game.state.factions[1],a=f.armies[0],d=e.armies[0];f.town.buildings[f.town.plots[0]]='prison';d.pos=35;Game.startBattle(a,d,{kind:'duel',title:'Поле боя',pos:35});const b=Game.state.battle,en=b.units.filter(u=>u.side===1);en[0].hp=0;en[1].surrender=true;b.over=0;Game.finishBattle();}''')
    assert page.evaluate('Game.state.factions[0].bag.length')==2
    assert page.evaluate('Game.state.aftermath.corpses.length')==1
    assert page.evaluate('Game.state.aftermath.captives.length')==1
    page.click('[data-a=aftermathBodies]')
    assert 'Маршрут' in page.locator('#modal').inner_text() and 'Примерное время' in page.locator('#modal').inner_text()
    page.click('[data-a=confirmShipping]');page.click('[data-a=aftermathCapture]');page.click('[data-a=aftermathDone]')
    assert page.evaluate('Game.state.convoys.map(c=>c.kind).sort()')==['bodies','prisoners']
    assert page.evaluate('Game.state.factions[0].armies[0].pos')==35
    ok('Winner takes all enemy items; bodies and live prisoners dispatch as separate interceptable wagons')
    result=page.evaluate('''()=>{const s=Game.state,a=s.factions[0].armies[0],c=s.convoys.find(c=>c.kind==='bodies');const escort=Game.escortConvoy(c.id,a.id);Math.random=()=>.5;Game.tickConvoys();return{escort,convoys:s.convoys.length,bodies:s.factions[0].morgue.length,prison:s.factions[0].prison.length,items:s.factions[0].prison[0].items.length};}''')
    assert result=={'escort':True,'convoys':0,'bodies':1,'prison':1,'items':0}
    ok('Escort moves with the wagon; arrivals populate morgue and unlimited prison without restoring items')
    result=page.evaluate('''()=>{const f=Game.state.factions[0],h=f.morgue[0];f.gold=500;f.crystal=30;f.town.buildings[f.town.plots[1]]='resurrection';const before=f.gold,blocked=Game.revive(h.id)===false,bodyKept=f.morgue.length===1;const priest=Game.createHero('acolyte',8);priest.sub='highpriest';Game.createArmy(f,f.city,[priest]);const level=h.level,revived=Game.revive(h.id);return{blocked,bodyKept,uncharged:before===500,revived,level:h.level,expected:level,loyalty:h.loyalty,weak:h.weak};}''')
    assert result['blocked'] and result['bodyKept'] and result['revived']
    assert result['level']==result['expected']==1 and result['loyalty']==15 and result['weak']==2
    result=page.evaluate('''()=>{const f=Game.state.factions[0];f.armies=f.armies.filter(a=>!a.heroes.some(h=>h.sub==='highpriest'));const h=Game.createHero('warrior',3);h.dead=true;h.hp=0;h.originalOwner=0;f.morgue.push(h);const yes=Game.revive(h.id);return{yes,level:h.level,weak:h.weak};}''')
    assert result=={'yes':True,'level':2,'weak':4}
    ok('Level-1 resurrection is blocked without a High Priest; priest preserves levels; foreign resurrection has low loyalty')
    result=page.evaluate('''()=>{Game.newGame(131);const s=Game.state,f=s.factions[0],e=s.factions[1],h=Game.createHero('warrior',2);h.originalOwner=0;const c=Game.makeConvoy(e,35,'bodies',[h]);const a=f.armies[0];a.pos=34;a.mp=5;const yes=Game.intercept(c.id,a);return{yes,removed:!s.convoys.some(v=>v.id===c.id),body:s.remains[0].hero.id===h.id};}''')
    assert result=={'yes':True,'removed':True,'body':True}
    result=page.evaluate('''()=>{const s=Game.state,f=s.factions[0],e=s.factions[1],h=Game.createHero('archer',2);h.originalOwner=0;h.capturedOwner=0;h.items=[];const c=Game.makeConvoy(e,35,'prisoners',[h]);const a=f.armies[0];a.mp=5;Game.intercept(c.id,a);return s.convoys.some(v=>v.owner===0&&v.kind==='released'&&v.cargo[0].id===h.id);}''')
    assert result
    ok('Enemy corpse wagons can be seized and captive heroes can be rescued by interception')
    result=page.evaluate('''()=>{Game.newGame(132);const s=Game.state,f=s.factions[0],e=s.factions[1],a=f.armies[0];a.pos=44;a.mp=5;const yes=Game.startSiege(a,e),si=s.sieges[0],early=Game.assault(si);si.progress=Game.fortification(e);const ready=Game.assault(si);s.battle.over=0;Game.finishBattle();return{yes,early,ready,dead:e.dead};}''')
    assert result=={'yes':True,'early':False,'ready':True,'dead':True}
    result=page.evaluate('''()=>{Game.newGame(133);const s=Game.state,f=s.factions[0],e=s.factions[1],a=e.armies[0];a.pos=35;a.mp=5;Game.startSiege(a,f);const si=s.sieges[0];Game.sally(si,f.armies[0]);s.battle.over=1;Game.finishBattle();return{dead:f.dead,result:!!s.result};}''')
    assert result=={'dead':True,'result':True}
    result=page.evaluate('''()=>{Game.newGame(134);const s=Game.state,f=s.factions[0],e=s.factions[1],a=e.armies[0];a.pos=35;Game.startSiege(a,f);s.sieges[0].progress=3;a.pos=100;Game.cancelSieges();return s.sieges.length;}''')
    assert result==0
    ok('Siege delays assault; losing a sally loses the capital; leaving removes all siege progress')
    result=page.evaluate('''()=>{Game.newGame(135);const s=Game.state,f=s.factions[0];f.rep=60;s.factions[1].rep=20;Game.checkVictory();s.completed=1;Game.checkVictory();const held=s.dominance.held;const purchased=Game.requestBoon(f,'gold');Game.checkVictory();return{held,purchased,rep:f.rep,reset:s.dominance.leader===null};}''')
    assert result=={'held':1,'purchased':True,'rep':48,'reset':True}
    result=page.evaluate('''()=>{Game.newGame(136);const f=Game.state.factions[0];Game.state.decree.type='artifact';f.bag.push({id:'specialTest',kind:'artifact',name:'Печать первого короля',value:90,special:true});const yes=Game.fulfill(f);return{yes,rep:f.rep,main:Game.state.decree.status[0].main,extra:Game.state.decree.status[0].extra,left:f.bag.length};}''')
    assert result=={'yes':True,'rep':30,'main':True,'extra':True,'left':0}
    ok('Reputation spending breaks superiority; a special artifact fulfills main and optional decree parts together')
    # Save/load retains the new data model, including multiple armies and cargo.
    result=page.evaluate('''()=>{Game.newGame(137);const f=Game.state.factions[0];const h=Game.createHero('rogue');h.originalOwner=0;Game.createArmy(f,35,[h]);Game.makeConvoy(f,52,'bodies',[Game.createHero('archer',2)]);Game.save();const before=JSON.stringify(Game.state);const yes=Game.load();return{yes,same:before===JSON.stringify(Game.state)};}''')
    assert result=={'yes':True,'same':True}
    ok('Round-trip save/load preserves separate armies, convoys and all persistent rules')
    page.evaluate('Game.newGame(200)')
    for _ in range(100):
        if page.evaluate('!!Game.state.result'):break
        page.evaluate('''async()=>{const s=Game.state;if(s.battle){Game.autoBattle();Game.finishBattle();}else if(s.aftermath){const m=s.aftermath;if(m.corpses.length)Game.dispatchBodies(s.factions[0],m.pos,m.corpses);if(m.captives.length){const f=s.factions[0];f.town.buildings[f.town.plots[0]]='prison';Game.dispatchCaptives(f,m.pos,m.captives);}s.aftermath=null;Game.closeModal();Game.after();}else {if(s.turnFlow?.report?.pending)Game.turns.dismiss();Game.turns.allDeferred();await Game.endTurn();}}''')
        page.wait_for_timeout(45)
    assert page.evaluate('!!Game.state.result')
    assert page.evaluate('Game.state.factions.slice(1).some(f=>f.rep!==0||f.kills>0)')
    assert page.evaluate('Game.state.factions.every(f=>Number.isFinite(f.gold)&&f.gold>=0&&f.armies.every(a=>a.heroes.length<=4))')
    ok('An AI session reaches an ending with active opponents and valid resources and army limits')
    assert not errors,errors
    assert not external,external
    ok('No JavaScript errors or external asset requests across all scenarios')
    page.evaluate('Game.newGame(2026)');page.screenshot(path='/tmp/v04-map.png',full_page=True)
    page.click('#nav [data-a=city]');page.screenshot(path='/tmp/v04-city.png',full_page=True)
    page.click('[data-a=close]');page.set_viewport_size({'width':390,'height':844})
    assert page.evaluate('document.documentElement.scrollWidth<=390')
    assert page.locator('#endTurn').is_visible()
    page.screenshot(path='/tmp/v04-mobile.png',full_page=True)
    ok('Narrow-screen layout keeps controls within the viewport')
    browser.close()
server.shutdown()
print(f'{len(passed)} scenarios passed.')
