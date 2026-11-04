"""Action-caused mutual relationships, player-controlled support and biome encounters."""
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
 p.evaluate('''()=>{Game.fx.configure({enabled:false});Math.random=()=>.5;Game.newGame(701);for(const f of Game.state.factions.slice(1)){f.armies=[];f.candidates=[]}}''')
 for _ in range(9):
  p.evaluate('''async()=>{if(Game.state.turnFlow?.report?.pending)Game.turns.dismiss();Game.turns.allDeferred();await Game.endTurn()}''')
 assert p.evaluate('Game.state.turn')==10
 assert p.evaluate('Game.state.factions[0].armies.every(a=>!a.conflict&&a.heroes.every(h=>Object.values(h.bonds).every(n=>n===0)))')
 ok('Nine idle turns, including former timer dates, create no dispute or relationship change')
 p.evaluate('''()=>{Game.newGame(702);const f=Game.state.factions[0],a=f.armies[0];a.pos=35;Game.relations.adjust(a.heroes[0],a.heroes[1],-2,'Подарки деревне вопреки возражениям товарища');for(let i=0;i<6;i++){Game.state.turn++;Game.tickFaction(f)}Game.render()}''')
 assert p.evaluate('Game.state.factions[0].armies[0].conflict.reason').startswith('Подарки деревне')
 assert p.evaluate('Game.state.factions[0].armies[0].heroes.every(h=>h.loyalty<65)')
 result=p.evaluate('''()=>{const a=Game.state.factions[0].armies[0],f=Game.state.factions[0],before=f.gold,mp=a.mp;Math.random=()=>{throw Error('Guaranteed settlement rolled dice')};const result=Game.relations.resolve(a,a.heroes[0],'compensate');Math.random=()=>.5;return{ok:result.ok,paid:before-f.gold,spent:mp-a.mp,conflict:!!a.conflict,mutual:a.heroes[0].bonds[a.heroes[1].id]===a.heroes[1].bonds[a.heroes[0].id]}}''')
 assert result=={'ok':True,'paid':20,'spent':1,'conflict':False,'mutual':True}
 ok('A real dispute keeps its cause, affects loyalty when neglected and can be settled without dice for a real cost')
 p.evaluate('''()=>{Game.newGame(703);const f=Game.state.factions[0],a=f.armies[0],other=Game.createArmy(f,35,[Game.createHero('warrior'),Game.createHero('rogue')]);Game.relations.adjust(a.heroes[0],a.heroes[1],-2,'Рискованное решение');Game.relations.adjust(other.heroes[0],other.heroes[1],-2,'Раздача премии');}''')
 assert p.evaluate('Game.state.factions[0].armies.filter(Game.relations.activeConflict).length')==1
 ok('Several armies share one active everyday dispute; no extra conversation queue is generated')
 p.evaluate('''()=>{Game.newGame(704);const a=Game.state.factions[0].armies[0];a.heroes.push(Game.createHero('archer'));a.heroes[0].traits=['sociable'];a.heroes[1].traits=['kind'];a.heroes[2].traits=['greedy'];a.pos=52;Game.ui.selected=52;Game.state.factions[0].seen[52]=true;Game.render();Game.openEvent('village',52);}''')
 p.hover('[data-a=eventChoice][data-v=gift]');p.wait_for_selector('#abilityTooltip:not([hidden])')
 assert '+1' in p.locator('#abilityTooltip').inner_text()
 assert '-1' in p.locator('#abilityTooltip').inner_text()
 p.click('[data-a=eventChoice][data-v=gift]')
 result=p.evaluate('''()=>{const a=Game.state.factions[0].armies[0],[x,y,z]=a.heroes;return[Game.relations.value(x,y),Game.relations.value(x,z),x.bonds[z.id]===z.bonds[x.id]]}''')
 assert result==[1,-1,True]
 p.click('[data-a=close]')
 p.evaluate('''()=>{Game.state.turn++;Game.state.factions[0].armies[0].mp=5;Game.openEvent('village',52)}''')
 p.click('[data-a=eventChoice][data-v=gift]')
 assert p.evaluate('Game.ui.modal')=='eventResult'
 assert 'подарки деревне' in p.evaluate('Game.state.factions[0].armies[0].conflict.reason')
 assert p.evaluate('Game.turns.tasks().some(t=>t.key.startsWith("conflict:"))')
 p.click('[data-a=close]');p.click('#armybar [data-a=conflict]');p.screenshot(path='/tmp/v07-conflict.png')
 ok('Traits can approve and disapprove of the same act; reactions are previewed and the actual act causes the dispute')
 p.evaluate('''()=>{const a=Game.state.factions[0].armies[0];Math.random=()=>0;const r=Game.relations.resolve(a,a.heroes[0],'mediate');Math.random=()=>.5;if(r.ok)throw Error('Expected a failed check')}''')
 assert p.evaluate('!!Game.state.factions[0].armies[0].conflict')
 assert p.evaluate('Game.relations.resolve(Game.state.factions[0].armies[0],Game.state.factions[0].armies[0].heroes[0],"mediate")') is None
 ok('Failed mediation leaves the cause unresolved; repeated checks cannot be spammed during one turn')
 p.evaluate('''()=>{Game.newGame(705);const a=Game.state.factions[0].armies[0];Game.startBattle(a,null,{kind:'ambush',family:'bandits',title:'Спасение товарища',pos:a.pos});const b=Game.state.battle;b.field.cells.fill('ground');b.side=b.human;const x=b.units.find(u=>u.cls==='acolyte'),y=b.units.find(u=>u.cls==='warrior');x.pos=17;y.pos=9;y.hp=0;x.ap=2;x.mana=12;Game.spellBattle(x,y,'heal')}''')
 assert p.evaluate('Game.relations.value(...Game.state.factions[0].armies[0].heroes)')==2
 assert not p.evaluate('Game.state.battle.units.some(u=>u.friendCover)')
 p.evaluate('''()=>{const b=Game.state.battle,x=b.units.find(u=>u.cls==='acolyte'),y=b.units.find(u=>u.cls==='warrior');y.hp=0;x.ap=2;x.mana=12;Game.spellBattle(x,y,'heal');Game.ui.battleSelected=y.id;Game.render()}''')
 assert p.evaluate('Game.relations.value(...Game.state.factions[0].armies[0].heroes)')==2
 p.click('[data-a=bSupport]')
 point=p.evaluate('Game.painter.project(Game.state.battle.units.find(u=>u.cls==="acolyte").pos,"battle")');p.mouse.click(point['x'],point['y'])
 assert p.evaluate('!!Game.state.battle.units.find(u=>u.cls==="acolyte").friendCover')
 assert p.evaluate('Game.state.battle.units.find(u=>u.cls==="warrior").ap')==0
 assert not p.evaluate('''()=>{const b=Game.state.battle,x=b.units.find(u=>u.cls==='acolyte'),y=b.units.find(u=>u.cls==='warrior');x.ap=2;return Game.relations.support(x,y)}''')
 p.screenshot(path='/tmp/v07-support.png')
 ok('Rescue unlocks mutual trust once per pair per battle; support needs a manual command, costs AP and cannot be spammed')
 p.evaluate('''()=>{Game.newGame(706);const a=Game.state.factions[0].armies[0];a.heroes.forEach(h=>h.traits=['brave']);Game.startBattle(a,null,{kind:'ambush',family:'bandits',title:'Общая победа',pos:a.pos});for(const u of Game.state.battle.units.filter(u=>u.side===0))u.didHit=true;Game.relations.victory(a,Game.state.battle)}''')
 assert p.evaluate('Game.state.factions[0].armies[0].heroes.every((h,i,a)=>h.rivals[a[1-i].id])')
 result=p.evaluate('''()=>{const b=Game.state.battle,u=b.units.find(u=>u.cls==='warrior'),r=b.units.find(u=>u.cls==='acolyte'),t=b.units.find(u=>u.side===1);b.field.cells.fill('ground');u.pos=18;t.pos=19;u.range=1;t.slash=-100;t.hp=t.max=100;u.ap=2;Game.attackBattle(u,t);const withRival=100-t.hp;r.hp=0;t.hp=100;u.ap=2;Game.attackBattle(u,t);return withRival-(100-t.hp)}''')
 assert result==1
 ok('Shared brave deeds create mutual rivalry; a living rival gives the promised damage benefit')
 result=p.evaluate('''()=>{Game.newGame(707);const a=Game.state.factions[0].armies[0],[x,y]=a.heroes;x.bonds[y.id]=2;y.bonds[x.id]=0;Game.relations.rivalry(x,y,'Общая победа');Game.save();const data=JSON.parse(JSON.stringify(Game.state));Game.load(data);return{mutual:x.bonds[y.id],v:Game.relations.value(...Game.state.factions[0].armies[0].heroes),rival:Game.state.factions[0].armies[0].heroes.every((h,i,a)=>h.rivals[a[1-i].id])}}''')
 assert result['v']==1 and result['rival']
 ok('Save migration restores mutual scores; rivalry and its reason survive reload')
 result=p.evaluate('''()=>{for(let seed=1;seed<=12;seed++){Game.newGame(seed);const s=Game.state,keys=new Set(s.map.filter(c=>c.site?.type==='camp').map(c=>c.site.family));if(keys.size<8)return{seed,keys:[...keys]};for(const c of s.map)if(c.site?.type==='camp'&&!Game.bestiary.families[c.site.family].habitats.includes(c.terrain))return false;}return true}''')
 assert result is True,result
 p.click('#nav [data-a=bestiary]');assert p.locator('canvas[data-monster]').count()==8
 p.screenshot(path='/tmp/v07-bestiary.png')
 ok('Every tested kingdom contains all eight encounter families in suitable habitats; the bestiary explains them')
 p.evaluate('''()=>{Game.newGame(708);const s=Game.state,a=s.factions[0].armies[0];a.pos=35;s.factions[0].seen[35]=true;s.map[35].site={type:'ruin',done:false,guarded:true,cleared:false,family:'undead'};Game.ui.selected=35;Game.render()}''')
 assert 'Нежить' in p.locator('#sidebar').inner_text()
 p.click('[data-a=site]')
 assert p.evaluate('Game.state.battle.meta.family')=='undead'
 assert set(p.evaluate('Game.state.battle.units.filter(u=>u.side===1).map(u=>u.monster)'))=={'skeleton','zombie'}
 p.screenshot(path='/tmp/v07-undead.png')
 p.evaluate('Game.state.battle.over=0;Game.finishBattle()')
 assert p.evaluate('Game.state.map[35].site.cleared&&!Game.state.map[35].site.done')
 p.evaluate('Game.state.factions[0].armies[0].mp=1;Game.render()');p.click('[data-a=site]')
 assert p.evaluate('Game.state.map[35].site.done&&Game.state.factions[0].bag.some(i=>i.kind==="artifact")')
 ok('Guarded ruins reveal their threat, require victory and then yield the artifact through exploration')
 p.evaluate('''()=>{Game.newGame(709);const a=Game.state.factions[0].armies[0];Game.startBattle(a,null,{kind:'ambush',family:'spiders',title:'Паучья засада',pos:a.pos});const b=Game.state.battle;b.field.cells.fill('ground');const spider=b.units.find(u=>u.monster==='spider'),hero=b.units.find(u=>u.cls==='warrior');spider.pos=18;hero.pos=19;hero.slash=-100;spider.ap=2;Game.attackBattle(spider,hero)}''')
 assert p.evaluate('Game.bestiary.speed(Game.state.battle.units.find(u=>u.cls==="warrior"))')==1
 p.screenshot(path='/tmp/v07-spiders.png')
 p.evaluate('Game.state.battle.round+=2')
 assert p.evaluate('Game.bestiary.speed(Game.state.battle.units.find(u=>u.cls==="warrior"))')==2
 p.evaluate('''()=>{Game.newGame(710);const a=Game.state.factions[0].armies[0];Game.startBattle(a,null,{kind:'ambush',family:'wolves',title:'Волчья стая',pos:a.pos});const b=Game.state.battle;b.field.cells.fill('ground');const w=b.units.filter(u=>u.monster==='wolf'),hero=b.units.find(u=>u.side===0);w[0].pos=18;w[1].pos=10;hero.pos=19;}''')
 assert p.evaluate('''()=>{const b=Game.state.battle;return Game.bestiary.attackBonus(b.units.find(u=>u.monster==='wolf'),b.units.find(u=>u.side===0))}''')==2
 ok('Spider hits actually slow movement and expire; wolves receive their pack attack bonus')
 result=p.evaluate("""()=>{Game.newGame(711);const a=Game.state.factions[0].armies[0];Game.relations.adjust(a.heroes[0],a.heroes[1],2,'Спасение в бою');Game.startBattle(a,null,{kind:'ambush',family:'bandits',title:'Проверка прикрытия',pos:a.pos});const b=Game.state.battle;b.field.cells.fill('ground');b.side=b.human;const w=b.units.find(u=>u.cls==='warrior'),c=b.units.find(u=>u.cls==='acolyte'),enemy=b.units.find(u=>u.side===1);w.pos=9;c.pos=17;enemy.pos=18;enemy.range=4;enemy.atk=0;c.pierce=12;c.hp=c.max=100;Math.random=()=>.55;enemy.ap=2;Game.attackBattle(enemy,c);const exposed=c.hp<100;c.hp=100;w.ap=2;const supported=Game.relations.support(w,c);enemy.ap=2;Game.attackBattle(enemy,c);const covered=c.hp===100;Game.moveBattle(w,0);enemy.ap=2;Game.attackBattle(enemy,c);Math.random=()=>.5;return{exposed,supported,covered,uncoveredAfterMove:c.hp<100};}""")
 assert result=={'exposed':True,'supported':True,'covered':True,'uncoveredAfterMove':True}
 ok('Manual support changes the actual hit result and stops protecting when the friend moves away')
 result=p.evaluate("""()=>{Game.newGame(712);const s=Game.state,a=s.factions[0].armies[0];a.pos=35;s.map[35].site={type:'camp',cleared:false};Game.startBattle(a,null,{kind:'camp',family:'bandits',title:'Старый бой',pos:35});const legacy=JSON.parse(JSON.stringify(s));for(const c of legacy.map)if(c.site)delete c.site.family;for(const v of legacy.villages)delete v.threatFamily;for(const u of legacy.battle.units)delete u.monster;delete legacy.battle.meta.family;legacy.factions[0].armies[0].conflict={first:a.heroes[0].id,second:a.heroes[1].id,created:1};const before=JSON.stringify(legacy.battle.units),loaded=Game.load(legacy);return{loaded,sameUnits:before===JSON.stringify(Game.state.battle.units),clearedTimer:!Game.state.factions[0].armies[0].conflict,family:Game.state.map[35].site.family};}""")
 assert result=={'loaded':True,'sameUnits':True,'clearedTimer':True,'family':'bandits'}
 ok('Legacy saves keep their current battle and remove only the old causeless calendar dispute')
 assert not errors,errors
 b.close()
server.shutdown();print(f'{len(passed)} relationship and creature scenarios passed.')
