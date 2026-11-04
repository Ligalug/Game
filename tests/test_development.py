"""Research, building gates, candidate training, crafting and use of real items."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
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
 p.evaluate('Game.fx.configure({enabled:false});Math.random=()=>.5;Game.newGame(801)')
 result=p.evaluate('''()=>{const f=Game.state.factions[0],p=f.town.plots;return{knowledge:f.knowledge,base:Game.cityEffects(f).knowledge,classes:f.candidates.map(h=>h.cls),tower:Game.buildPreview(f,p[0],'tower').ok,forge:Game.buildPreview(f,p[0],'smithy').ok}}''')
 assert result=={'knowledge':0,'base':2,'classes':['warrior','rogue','archer','acolyte'],'tower':False,'forge':True}
 ok('Knowledge is a separate resource; basic classes and smithy need no specialist buildings')
 p.evaluate('''()=>{const f=Game.state.factions[0];f.gold=1000;f.crystal=100;Game.ui.building='library';Game.ui.cityPlot=f.town.plots[0];Game.renderCity()}''')
 p.click('[data-a=construct]');assert p.evaluate('Game.state.factions[0].town.queue.id')=='library'
 p.evaluate('''()=>{const f=Game.state.factions[0];f.town.queue.progress=999;Game.tickFaction(f)}''')
 assert p.evaluate('Game.cityEffects(Game.state.factions[0]).knowledge')==6
 result=p.evaluate('''()=>{const f=Game.state.factions[0],p=f.town.plots;const without=Game.buildPreview(f,p[0],'enchanting').ok;f.town.buildings[p[1]]='tower';return{without,valid:Game.buildPreview(f,p[0],'enchanting').ok,wrong:Game.buildPreview(f,p[2],'enchanting').ok};}''')
 assert result=={'without':False,'valid':True,'wrong':False}
 p.evaluate('''()=>{const f=Game.state.factions[0];f.town.buildings[f.town.plots[0]]='enchanting'}''')
 assert p.evaluate('Game.hasBuilding(Game.state.factions[0],"library")')
 assert p.evaluate('''()=>{const f=Game.state.factions[0],saved={...f.town.buildings},p=f.town.plots;f.town.buildings={[p[0]]:'academy',[p[1]]:'tower'};const ok=Game.buildPreview(f,p[2],'magicacademy').ok;f.town.buildings=saved;return ok}''')
 ok('UI construction works; prerequisite and correct replacement hex are checked; replacement keeps the library')
 result=p.evaluate('''()=>{const f=Game.state.factions[0],plots=f.town.plots;f.town.buildings[plots[2]]='plaza';f.town.buildings[plots[3]]='plaza';f.town.buildings[plots[4]]='range';f.town.buildings[plots[5]]='magicacademy';Game.development.initialize();return{candidates:f.candidates.map(h=>h.level),live:f.armies[0].heroes.map(h=>h.level)}}''')
 assert result=={'candidates':[2,1,2,2],'live':[1,1]}
 p.evaluate('Game.renderHire()');p.locator('[data-a=recruit]').first.click()
 assert p.evaluate('Game.state.factions[0].armies[0].heroes.at(-1).level')==2
 ok('Training raises only matching candidates by one, never stacks, and the recruited hero keeps that level')
 result=p.evaluate('''()=>{const f=Game.state.factions[0],p=f.town.plots;f.town.buildings={};f.town.buildings[p[0]]='library';f.town.buildings[p[1]]='tower';f.town.buildings[p[2]]='kapish';const temple=Game.buildPreview(f,p[3],'temple').ok;f.town.buildings[p[2]]='cathedral08';const dark=Game.buildPreview(f,p[3],'kapish').ok;return{temple,dark,resurrection:Game.buildPreview(f,p[4],'shrine').ok}}''')
 assert result=={'temple':False,'dark':False,'resurrection':True}
 ok('Temple and occult branch exclude each other, including temple replacements; common resurrection remains accessible')
 p.evaluate('''()=>{Game.newGame(802);const f=Game.state.factions[0],p=f.town.plots;f.town.buildings[p[0]]='library';f.town.buildings[p[1]]='tower';f.knowledge=30;Game.renderCity()}''')
 p.click('[data-a=development]');p.click('[data-a=devResearch][data-id=barrier]')
 assert p.evaluate('Game.state.factions[0].knowledge')==20
 p.evaluate('''()=>{const f=Game.state.factions[0],a=f.armies[0];a.pos=35;Game.tickFaction(f)}''')
 assert p.evaluate('Game.state.factions[0].town.research.progress')==0
 p.evaluate('''()=>{const f=Game.state.factions[0];f.armies[0].pos=f.city;Game.tickFaction(f);Game.save();Game.load();Game.tickFaction(Game.state.factions[0]);Game.development.render()}''')
 assert p.evaluate('Game.state.factions[0].grimoire.includes("barrier")')
 assert not p.evaluate('Game.state.factions[0].armies[0].heroes.find(h=>h.cls==="acolyte").spells.includes("barrier")')
 p.click('[data-a=devTab][data-id=repertoire]');p.select_option('#replace-barrier','curse');p.click('[data-a=devLearn][data-id=barrier]')
 assert p.evaluate('Game.state.factions[0].armies[0].heroes.find(h=>h.cls==="acolyte").spells.includes("barrier")')
 assert not p.evaluate('Game.state.factions[0].armies[0].heroes.find(h=>h.cls==="acolyte").spells.includes("curse")')
 p.screenshot(path='/tmp/v08-research.png')
 ok('Research spends knowledge, pauses when the researcher leaves, survives reload and unlocks a shared spell requiring personal preparation')
 p.evaluate('''()=>{const a=Game.state.factions[0].armies[0];Game.startBattle(a,null,{kind:'ambush',family:'bandits',title:'Испытание нового заклинания',pos:a.pos});const b=Game.state.battle;b.field.cells.fill('ground');const u=b.units.find(u=>u.cls==='acolyte'),t=b.units.find(u=>u.cls==='warrior');u.pos=17;t.pos=9;u.ap=2;u.mana=12;Game.ui.battleSelected=u.id;Game.render()}''')
 assert p.locator('[data-a=bSpell][data-v=barrier]').count()==1
 assert p.locator('[data-a=bSpell][data-v=curse]').count()==0
 p.click('[data-a=bSpell][data-v=barrier]');point=p.evaluate('Game.painter.project(9,"battle")');p.mouse.click(point['x'],point['y'])
 assert p.evaluate('Game.state.battle.units.find(u=>u.cls==="warrior").greaterWard')==2
 assert p.evaluate('Game.state.battle.units.find(u=>u.cls==="acolyte").mana')==9
 p.screenshot(path='/tmp/v08-spell-battle.png')
 ok('The learned spell appears in battle, can be aimed and applies its real effect with the correct mana cost')
 result=p.evaluate('''()=>{Game.newGame(803);const f=Game.state.factions[0],p=f.town.plots;f.gold=1000;f.crystal=50;f.town.buildings[p[0]]='library';f.town.buildings[p[1]]='tower';f.knowledge=100;const blocked=Game.development.startResearch('fire');f.town.buildings[p[2]]='power';const started=Game.development.startResearch('fire');Game.tickFaction(f);Game.tickFaction(f);const h=f.armies[0].heroes.find(h=>h.cls==='acolyte');Game.development.learn('fire',h.id,'bolt');return{blocked,started,learned:h.spells.includes('fire')}}''')
 assert result=={'blocked':False,'started':True,'learned':True}
 result=p.evaluate('''()=>{const a=Game.state.factions[0].armies[0];Game.startBattle(a,null,{kind:'ambush',family:'bandits',title:'Пламя',pos:a.pos});const b=Game.state.battle;b.field.cells.fill('ground');const u=b.units.find(u=>u.cls==='acolyte'),t=b.units.find(u=>u.side===1);u.pos=18;t.pos=19;t.ac=-100;t.hp=t.max=100;u.ap=2;u.mana=12;const ok=Game.spellBattle(u,t,'fire');return{ok,damage:100-t.hp,mana:u.mana}}''')
 assert result=={'ok':True,'damage':12,'mana':8},result
 ok('Research school gates are enforced and elemental magic deals its configured damage')
 p.evaluate('''()=>{Game.newGame(804);const f=Game.state.factions[0],p=f.town.plots,forge=p[0],near=p.find(i=>i!==forge&&Game.nb(forge).includes(i)),remaining=p.filter(i=>i!==forge&&i!==near);f.gold=1000;f.crystal=20;f.town.buildings[forge]='magicforge';f.town.buildings[near]='power';f.town.buildings[remaining[0]]='library';f.town.buildings[remaining[1]]='tower';}''')
 assert p.evaluate('Game.development.craftInfo(Game.state.factions[0],"magicSword").crystals')==3
 assert p.evaluate('Game.development.startCraft("magicSword")')
 assert p.evaluate('Game.state.factions[0].crystal')==17
 p.evaluate('''()=>{const f=Game.state.factions[0];for(let i=0;i<3;i++)Game.tickFaction(f);const h=f.armies[0].heroes[0];Game.development.equip(f.bag.find(i=>i.name==='Зачарованный клинок').id,h.id);Game.development.render()}''')
 assert p.evaluate('Game.state.factions[0].armies[0].heroes[0].items.some(i=>i.enchantment==="bolt")')
 assert p.evaluate('Game.state.factions[0].bag.some(i=>i.name==="Походное оружие")')
 p.click('[data-a=devTab][data-id=production]');p.screenshot(path='/tmp/v08-workshop.png')
 p.evaluate('''()=>{const a=Game.state.factions[0].armies[0];Game.startBattle(a,null,{kind:'ambush',family:'bandits',title:'Клинок',pos:a.pos});}''')
 assert p.evaluate('Game.state.battle.units.find(u=>u.cls==="warrior").atk')==10
 ok('Production uses crystals with a genuine adjacent discount; gear is delivered, equipped and changes actual battle stats')
 p.evaluate('''()=>{Game.newGame(805);const f=Game.state.factions[0],p=f.town.plots;f.gold=1000;f.crystal=50;f.town.buildings[p[0]]='enchanting';f.town.buildings[p[1]]='tower';const item=f.armies[0].heroes[0].items[0];Game.development.startCraft('enchant','ward',item.id)}''')
 assert p.evaluate('Game.state.factions[0].armies[0].heroes[0].items.length')==0
 p.evaluate('''()=>{const f=Game.state.factions[0];Game.tickFaction(f);Game.tickFaction(f)}''')
 assert p.evaluate('Game.state.factions[0].bag.some(i=>i.enchantment==="ward")')
 assert not p.evaluate('''()=>{const f=Game.state.factions[0];return Game.development.startCraft('enchant','bolt',f.bag[0].id)}''')
 ok('Enchanting reserves an actual existing item, returns it to storage and prevents uncontrolled stacking of properties')
 p.evaluate('''()=>{Game.newGame(806);const f=Game.state.factions[0],p=f.town.plots;f.gold=1000;f.crystal=50;f.town.buildings[p[0]]='laboratory';f.town.buildings[p[1]]='library';Game.development.startCraft('potion');Game.tickFaction(f);Game.tickFaction(f);Game.development.equip(f.bag.find(i=>i.kind==='potion').id,f.armies[0].heroes[0].id);const a=f.armies[0];a.pos=35;Game.startBattle(a,null,{kind:'ambush',family:'bandits',title:'Зелье в походе',pos:a.pos});const u=Game.state.battle.units.find(u=>u.cls==='warrior');u.hp=5;u.ap=2;Game.ui.battleSelected=u.id;Game.render()}''')
 p.click('[data-a=bItem]')
 assert p.evaluate('Game.state.battle.units.find(u=>u.cls==="warrior").hp')==19
 assert p.evaluate('Game.state.battle.units.find(u=>u.cls==="warrior").ap')==1
 assert not p.evaluate('Game.state.factions[0].armies[0].heroes[0].items.some(i=>i.kind==="potion")')
 ok('A crafted potion must be carried by its hero; use in battle restores HP, spends AP and consumes the item')
 p.evaluate('''()=>{Game.newGame(807);const f=Game.state.factions[0],p=f.town.plots;f.gold=1000;f.crystal=50;f.town.buildings[p[0]]='enchanting';Game.development.startCraft('scroll','heal');Game.tickFaction(f);Game.tickFaction(f);Game.development.equip(f.bag.find(i=>i.kind==='scroll').id,f.armies[0].heroes[0].id);Game.startBattle(f.armies[0],null,{kind:'ambush',family:'bandits',title:'Свиток спасения',pos:f.city});const b=Game.state.battle;b.field.cells.fill('ground');const w=b.units.find(u=>u.cls==='warrior'),c=b.units.find(u=>u.cls==='acolyte');w.pos=9;c.pos=17;c.hp=0;w.ap=2;Game.ui.battleSelected=w.id;Game.render()}''')
 p.click('[data-a=bItem]');point=p.evaluate('Game.painter.project(17,"battle")');p.mouse.click(point['x'],point['y'])
 assert p.evaluate('Game.state.battle.units.find(u=>u.cls==="acolyte").hp')==14
 assert p.evaluate('Game.state.battle.units.find(u=>u.cls==="acolyte").ap')==1
 assert p.evaluate('Game.state.battle.units.find(u=>u.cls==="warrior").cls')=='warrior'
 assert p.evaluate('Game.state.battle.units.find(u=>u.cls==="warrior").mana')==2
 ok('A non-mage can use a prepared scroll without mana; healing a downed companion preserves revival rules')
 result=p.evaluate('''()=>{Game.newGame(808);const data=JSON.parse(JSON.stringify(Game.state));delete data.developmentVersion;for(const f of data.factions){delete f.knowledge;delete f.grimoire;for(const a of f.armies)for(const h of a.heroes)delete h.spells;for(const h of f.candidates){delete h.baseRecruitLevel;delete h.trainingBonus;}}const gold=data.factions[0].gold,loaded=Game.load(data);Game.save();const before=JSON.stringify(Game.state);Game.load();return{loaded,version:Game.state.version,gold:Game.state.factions[0].gold===gold,book:Game.state.factions[0].grimoire.length,exact:before===JSON.stringify(Game.state)}}''')
 assert result=={'loaded':True,'version':4,'gold':True,'book':4,'exact':True}
 ok('Old saves acquire development defaults without losing resources; new saves round-trip exactly')
 p.evaluate("""()=>{Game.newGame(809);const f=Game.state.factions[0],plots=f.town.plots;f.gold=1000;f.crystal=50;f.knowledge=100;f.town.buildings[plots[0]]='library';f.town.buildings[plots[1]]='tower';f.town.buildings[plots[2]]='enchanting';Game.development.startResearch('barrier');const item=f.armies[0].heroes[0].items[0];Game.development.startCraft('enchant','ward',item.id);Game.ui.devTab='production';Game.development.render()}""")
 p.click('[data-a=devCancelCraft]')
 assert not p.evaluate('Game.state.factions[0].town.craft')
 assert p.evaluate('Game.state.factions[0].bag.some(i=>i.name==="Походное оружие"&&!i.enchantment)')
 p.click('[data-a=devTab][data-id=research]');p.click('[data-a=devCancelResearch]')
 assert not p.evaluate('Game.state.factions[0].town.research')
 assert p.evaluate('Game.state.factions[0].knowledge')==90
 ok('Cancellation releases a reserved item and makes queues usable again with the advertised resource cost')
 p.evaluate("""()=>{const f=Game.state.factions[0];Game.development.startResearch('barrier');const newMage=Game.createHero('acolyte');f.armies[0].heroes.push(newMage);f.town.research.hero='missing-hero';Game.development.initialize();Game.ui.researchHero=newMage.id;Game.development.render()}""")
 p.click('[data-a=devAssignResearch]');p.evaluate('Game.tickFaction(Game.state.factions[0]);Game.tickFaction(Game.state.factions[0])')
 assert p.evaluate('Game.state.factions[0].grimoire.includes("barrier")')
 ok('Research can be reassigned when its original hero is gone')
 p.evaluate("""()=>{Game.newGame(810);const f=Game.state.factions[0],plots=f.town.plots;f.knowledge=30;f.town.buildings[plots[0]]='library';f.town.buildings[plots[1]]='tower';f.town.buildings[plots[2]]='smithy';Game.render()}""")
 assert p.evaluate('Game.turns.tasks().some(t=>t.key==="research")')
 assert p.evaluate('Game.turns.tasks().some(t=>t.key==="production")')
 p.evaluate('Game.turns.defer("research");Game.turns.defer("production")')
 assert not p.evaluate('Game.turns.tasks().some(t=>["research","production"].includes(t.key))')
 ok('New research and production decisions participate in the explicit end-turn deferral flow')
 from pathlib import Path
 with p.expect_download() as download:p.click('[data-a=downloadGame]')
 copy=Path('/tmp/tuman-08-browser-copy.html');download.value.save_as(copy)
 assert 'const ATLAS_URL=' in copy.read_text() and 'const Development=' in copy.read_text()
 snapshot=b.new_page();snapshot.route('**/local-copy.html',lambda r:r.fulfill(path=str(copy),content_type='text/html'))
 snapshot.goto(f'http://127.0.0.1:{server.server_port}/local-copy.html');snapshot.wait_for_function('Game.painter.ready')
 assert snapshot.locator('[data-a=start]').is_visible()
 snapshot.evaluate('Game.newGame(811);Game.fx.configure({enabled:false})')
 assert snapshot.evaluate('Game.state.developmentVersion')==8
 snapshot.close()
 ok('The in-game copy button downloads a standalone HTML that boots and runs the development module')
 assert not errors,errors
 b.close()
server.shutdown();print(f'{len(passed)} development scenarios passed.')
