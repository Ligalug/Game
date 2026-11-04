"""Turn guard, persisted reports, terrain rules, tooltips and idle map animation."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import os
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
passed=[]
def ok(s):passed.append(s);print('PASS:',s,flush=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox','--disable-webgl'])
 p=b.new_page(viewport={'width':1500,'height':1000});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto(f'http://127.0.0.1:{server.server_port}');p.wait_for_function('Game.painter.ready')
 p.evaluate('Game.fx.configure({enabled:false});Game.newGame(200)')
 p.click('#endTurn');assert p.evaluate('Game.state.turn')==1
 assert p.evaluate('Game.ui.modal')=='turnTasks'
 assert p.locator('[data-a=turnDefer]').count()==3
 p.locator('[data-a=turnDefer][data-id^="army:"]').click()
 assert p.evaluate('Game.state.factions[0].armies[0].mp')==5
 p.click('[data-a=turnGo][data-id=build]');p.click('[data-a=construct]')
 assert p.evaluate('Game.state.factions[0].town.queue!==null')
 p.click('[data-a=close]');p.click('#endTurn')
 assert p.locator('[data-a=turnDefer]').count()==1
 gold=p.evaluate('Game.state.factions[0].gold');p.click('[data-a=turnDefer][data-id=decree]')
 assert p.evaluate('Game.state.factions[0].gold')==gold
 assert p.locator('[data-a=end]').last.is_enabled()
 p.locator('[data-a=end]').last.click();p.wait_for_function('Game.state.turn===2&&Game.ui.modal==="turnReport"')
 assert p.locator('.turn-news[data-kind=income]').count()==1
 assert p.evaluate('Game.turns.tasks().some(t=>t.key.startsWith("army:"))')
 ok('End turn blocks until every important decision is performed or explicitly deferred; decisions reset next turn')
 p.evaluate('Game.endTurn()');assert p.evaluate('Game.state.turn')==2
 p.click('[data-a=turnReportDone]')
 p.evaluate('Game.turns.allDeferred();Game.save()')
 result=p.evaluate('''()=>{const before=JSON.stringify(Game.state);Game.load();return before===JSON.stringify(Game.state)}''')
 assert result
 p.evaluate('''()=>{const f=Game.state.factions[0];f.gold=0;f.crystal=0;f.town.queue=null;for(const a of f.armies)a.mp=0;Game.render()}''')
 assert not p.evaluate('Game.turns.tasks().some(t=>t.key==="build")')
 p.evaluate('Game.state.factions[0].gold=100;Game.render()')
 assert p.evaluate('Game.turns.tasks().some(t=>t.key==="build")')
 ok('Deferrals persist in saves; unavailable construction never blocks; newly available actions are rechecked')
 p.evaluate('''()=>{Game.newGame(201);const s=Game.state,f=s.factions[0];s.turn=2;s.decree.deadline=2;Game.relations.adjust(f.armies[0].heroes[0],f.armies[0].heroes[1],-2,'Спор из-за подарков деревне');f.gold=30;f.town.queue={plot:f.town.plots[0],id:'market',progress:999};f.town.wallQueue={type:'stone',left:1};f.town.growth=999;Game.makeConvoy(f,f.city,'bodies',[Game.createHero('archer',2)]);Game.turns.allDeferred();}''')
 p.evaluate('Game.endTurn()');p.wait_for_function('Game.state.turn===3&&Game.ui.modal==="turnReport"')
 kinds=p.evaluate('Game.state.turnFlow.report.items.map(v=>v.kind)')
 for kind in ['building','growth','king','event','convoy','income']:assert kind in kinds,kinds
 assert 'Новый королевский указ' in p.locator('#modal').inner_text()
 p.screenshot(path='/tmp/v06-report.png')
 result=p.evaluate('''()=>{Game.save();const before=JSON.stringify(Game.state.turnFlow.report);Game.load();return before===JSON.stringify(Game.state.turnFlow.report)}''')
 assert result
 p.wait_for_function('Game.ui.modal==="turnReport"')
 p.locator('.turn-news[data-kind=king] [data-a=turnNewsGo]').last.click()
 assert not p.evaluate('Game.state.turnFlow.report.pending')
 assert p.evaluate('Game.ui.modal')=='king'
 ok('Start-of-turn report covers completed buildings, walls, growth, decrees, new events and wagon arrivals; survives reload')
 p.evaluate('''()=>{Game.newGame(203);Game.fx.configure({enabled:true,speed:4});const f=Game.state.factions[0];f.town.queue={plot:f.town.plots[0],id:'market',progress:999};Game.turns.allDeferred()}''')
 p.evaluate('Game.endTurn()')
 assert p.evaluate('Game.state.turn')==2
 assert p.evaluate('Game.fx.busy')
 assert p.evaluate('Game.ui.modal')!='turnReport'
 p.wait_for_function('!Game.fx.busy&&Game.ui.modal==="turnReport"')
 p.click('[data-a=turnReportDone]');p.evaluate('Game.fx.configure({enabled:false})')
 ok('Start-of-turn news waits for animations and does not overwrite them')
 p.evaluate('Game.newGame(2026)');p.click('#endTurn');p.screenshot(path='/tmp/v06-decisions.png')
 # Every terrain has usable deployment cells and a connected lane between both sides.
 result=p.evaluate('''()=>{Game.newGame(2026);const t=Game.tactics;for(const terrain of Object.keys(t.profiles))for(let seed=1;seed<15;seed++){Game.state.seed=seed;const f=t.generate(terrain,34),k=f.cells.map(v=>t.tiles[v]);if(!k.some(v=>v.blocked)||!k.some(v=>v.cover)||!k.some(v=>v.cost>1))return false;for(const col of [1,6])for(let y=1;y<=4;y++)if(k[y*8+col].blocked)return false;const seen=new Set([9]),q=[9];while(q.length)for(const v of Game.nb(q.shift(),8,6))if(!seen.has(v)&&!k[v].blocked){seen.add(v);q.push(v)}if(!seen.has(14)||!seen.has(38))return false;}return true;}''')
 assert result
 ok('All six landscapes have obstacles, cover and difficult terrain; deployment and connecting paths remain open')
 p.evaluate('''()=>{Game.newGame(2026);const a=Game.state.factions[0].armies[0];Game.startBattle(a,null,{kind:'ambush',title:'Лесная засада',pos:a.pos});const b=Game.state.battle;b.field={terrain:'forest',cells:Array(48).fill('ground')};b.side=b.human;const u=b.units.find(u=>u.cls==='warrior');u.pos=9;u.speed=2;u.ap=2;b.field.cells[10]='marsh';}''')
 assert not p.evaluate('Game.battleReach(Game.state.battle.units.find(u=>u.cls==="warrior")).has(10)')
 p.evaluate('Game.state.battle.units.find(u=>u.cls==="warrior").speed=3')
 assert p.evaluate('Game.battleReach(Game.state.battle.units.find(u=>u.cls==="warrior")).get(10)')==3
 p.evaluate('Game.state.battle.field.cells[10]="rock"')
 assert not p.evaluate('Game.moveBattle(Game.state.battle.units.find(u=>u.cls==="warrior"),10)')
 ok('Movement uses terrain costs; rocks block movement and paths route around them')
 p.evaluate('''()=>{const b=Game.state.battle,u=b.units.find(u=>u.side===0&&u.cls==='acolyte'),t=b.units.find(u=>u.side===1);u.pos=9;u.ap=2;u.mana=12;t.pos=13;b.field.cells[10]='ground';b.field.cells[11]='tree';}''')
 result=p.evaluate('''()=>{const b=Game.state.battle,u=b.units.find(u=>u.cls==='acolyte'),t=b.units.find(u=>u.side===1),before=u.mana;return{cast:Game.spellBattle(u,t,'bolt'),same:u.mana===before,sight:Game.tactics.sight(u.pos,t.pos)}}''')
 assert result=={'cast':False,'same':True,'sight':False}
 result=p.evaluate('''()=>{const b=Game.state.battle,u=b.units.find(u=>u.cls==='warrior'),t=b.units.find(u=>u.side===1);b.field.cells.fill('ground');u.pos=9;u.range=4;u.atk=0;u.ap=2;t.pos=13;t.pierce=10;t.guard=false;t.wardUntil=0;u.curseUntil=0;t.hp=t.max=100;b.field.cells[13]='bush';Math.random=()=>.45;const protectedHP=t.hp;Game.attackBattle(u,t);const missed=t.hp===protectedHP;u.ap=2;b.field.cells[13]='ground';Game.attackBattle(u,t);return{missed,hit:t.hp<protectedHP};}''')
 assert result=={'missed':True,'hit':True}
 ok('Trees block projectiles and spells without spending mana; cover changes the actual hit result')
 p.evaluate('''()=>{const b=Game.state.battle;b.field=Game.tactics.generate('forest',34);const u=b.units.find(u=>u.cls==='acolyte');u.ap=2;u.mana=12;Game.ui.battleSelected=u.id;Game.render();}''')
 p.hover('[data-a=bSpell][data-v=heal]');p.wait_for_selector('#abilityTooltip:not([hidden])')
 assert '14 ХП' in p.locator('#abilityTooltip').inner_text()
 assert '3 маны' in p.locator('#abilityTooltip').inner_text()
 p.screenshot(path='/tmp/v06-forest-tooltip.png')
 p.mouse.move(10,10);p.wait_for_selector('#abilityTooltip[hidden]',state='attached')
 p.evaluate('''()=>{const b=Game.state.battle,u=b.units.find(u=>u.cls==='acolyte');u.mana=0;Game.render();}''')
 p.locator('.ability-tip').filter(has=p.locator('[data-a=bSpell][data-v=heal]')).focus()
 assert not p.locator('#abilityTooltip').is_hidden()
 assert 'Лечение' in p.locator('#abilityTooltip').inner_text()
 ok('Ability popups describe real effects and costs; disabled abilities remain readable with keyboard focus')
 p.evaluate('''()=>{const b=Game.state.battle;b.field=Game.tactics.generate('swamp',34);Game.render();}''')
 cell=p.evaluate('Game.state.battle.field.cells.findIndex(v=>v==="marsh")')
 point=p.evaluate('(p)=>Game.painter.project(p,"battle")',cell);p.mouse.move(point['x'],point['y'])
 assert 'Топь' in p.locator('#battleHexInfo').inner_text()
 p.screenshot(path='/tmp/v06-swamp.png')
 ok('Battlefield hover explains the actual tile and movement cost')
 p.evaluate('''()=>{Game.newGame(2026);Game.state.factions[0].seen.fill(true);Game.fx.configure({enabled:true,speed:1});Game.painter.focus(52)}''')
 before=p.evaluate('JSON.stringify(Game.state)');frames=p.evaluate('Game.painter.ambient.frames');shot=p.locator('#map').screenshot()
 p.wait_for_function('(n)=>Game.painter.ambient.frames>n+3',arg=frames)
 assert p.locator('#map').screenshot()!=shot
 assert p.evaluate('JSON.stringify(Game.state)')==before
 p.screenshot(path='/tmp/v06-living-map.png')
 p.evaluate('Game.fx.configure({enabled:false})');frames=p.evaluate('Game.painter.ambient.frames');shot=p.locator('#map').screenshot();p.wait_for_timeout(350)
 assert p.evaluate('Game.painter.ambient.frames')==frames
 assert p.locator('#map').screenshot()==shot
 ok('Idle wind and mill animation changes the picture without changing game state; animation off freezes it')
 assert not errors,errors
 b.close()
server.shutdown();print(f'{len(passed)} new scenarios passed.')
