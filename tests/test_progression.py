"""Progression, criticals, creatures, extraction of heroes and carrying casualties."""
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
url=f'http://127.0.0.1:{server.server_port}/battle-lab.html';passed=[]
def ok(t):passed.append(t);print('PASS:',t,flush=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
 p=b.new_page(viewport={'width':1700,'height':1200});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto(url);p.uncheck('#motion')
 assert p.evaluate('Lab.state.units[3].max===18&&Lab.state.units[3].barrier===12&&Lab.state.critChance===.1')
 ok('Mage has eighteen HP at level one while keeping the twelve-point barrier; criticals default to ten percent')
 result=p.evaluate("()=>{const u=Lab.state.units[0],t=Lab.state.units[4],d={name:'Крит',lo:10,hi:10,damage:'magic',undodgeable:true};t.hp=100;Lab.state.critChance=1;const f=Lab.damageForecast(u,t,d),r=Lab.hit(u,t,d);return {critical:r.critical,damage:r.damage,hp:t.hp,forecast:f.critHi,stress:t.stress}}")
 assert result=={'critical':True,'damage':12,'hp':88,'forecast':12,'stress':10}
 p.fill('#critChance','0');p.dispatch_event('#critChance','change')
 result=p.evaluate("()=>{const u=Lab.state.units[0],t=Lab.state.units[4];return Lab.hit(u,t,{name:'Обычный',lo:10,hi:10,damage:'magic',undodgeable:true})}")
 assert result['critical'] is False and result['damage']==8
 ok('Critical multiplier is applied before defense, matches forecast and increases stress; zero percent disables it')
 p.select_option('#playerLevel','5');p.select_option('#enemyLevel','3')
 assert p.evaluate('Lab.state.units[0].max===48&&Lab.state.units[3].max===26&&Lab.state.units[3].barrier===20&&Lab.state.units[4].max===40')
 p.select_option('#warriorSub','bastion');assert p.evaluate('Lab.defense(Lab.state.units[0],"piercing")')==48
 p.select_option('#warriorSub','berserker');assert p.evaluate('Lab.spec(Lab.state.units[0],"attack").lo')==11
 p.select_option('#archerSub','sniper');assert p.evaluate('Lab.spec(Lab.state.units[1],"attack").range')==8
 p.select_option('#squad','classic');p.select_option('#rogueSub','thief');assert abs(p.evaluate('Lab.stats(Lab.state.units[2]).dodge')-.35)<1e-8
 assert p.evaluate('Lab.state.units[2].stride')==2
 p.select_option('#rogueSub','assassin');assert p.evaluate('Lab.damageForecast(Lab.state.units[2],Lab.state.units[4],Lab.spec(Lab.state.units[2],"attack")).critChance')==.1
 ok('Independent team levels scale HP, damage, defenses and barrier; subclass selectors alter real battle parameters')
 p.select_option('#mageSub','priest')
 result=p.evaluate("()=>{const u=Lab.state.units[3],t=Lab.state.units[0];t.hp=1;const amount=Lab.healing(u),ok=Lab.apply(u,t,'priestHeal');return {amount,ok,hp:t.hp,charges:u.heals}}")
 assert result=={'amount':24,'ok':True,'hp':25,'charges':2}
 ok('Priest subclass and level affect actual healing and available charges')
 p.select_option('#mageSub','cultist')
 assert p.evaluate("()=>{const u=Lab.state.units[3],t=Lab.state.units[4];u.hp=1;Object.assign(t,{q:4,r:6,hp:1});return Lab.apply(u,t,'attack')&&t.hp===0&&u.hp===2}")
 p.select_option('#squad','engineer');p.select_option('#enemyLevel','1')
 for pack in ['wolves','spiders','undead','goblins','kobolds','ogres','beasts']:
  p.select_option('#enemyType',pack)
  assert p.locator('#board .monster-figure').count()==4
  assert p.evaluate("Lab.state.units.filter(u=>u.side===1).every(u=>!['warrior','rogue','archer','acolyte','engineer'].includes(u.type))")
  p.evaluate('Lab.skipAll()');p.click('#end');p.wait_for_function('!Lab.busy')
  assert p.evaluate('Lab.state.units.every(u=>u.ap>=0&&u.hp>=0)')
 ok('Seven creature groups have their own figures and take legal turns instead of masquerading as hero enemies')
 p.select_option('#enemyType','wolves');p.select_option('#playerLevel','1');p.select_option('#mageSub','base')
 result=p.evaluate("()=>{const u=Lab.state.units[4],v=Lab.state.units[5],t=Lab.state.units[0];Object.assign(u,{q:3,r:3});Object.assign(v,{q:3,r:2});const pack=Lab.spec(u,'attack',t).lo;v.q=12;v.r=0;return {pack,alone:Lab.spec(u,'attack',t).lo}}")
 assert result['pack']-result['alone']==2
 p.select_option('#playerLevel','2');p.select_option('#enemyType','spiders')
 result=p.evaluate("()=>{const u=Lab.state.units[4],t=Lab.state.units[0];Object.assign(u,{q:4,r:3});Lab.state.side=1;const ok=Lab.apply(u,t,'web');return {ok,slow:t.slow}}")
 assert result=={'ok':True,'slow':1}
 p.select_option('#enemyType','undead');assert p.evaluate('Lab.defense(Lab.state.units[4],"piercing")>Lab.defense(Lab.state.units[4],"slashing")')
 p.evaluate("Lab.state.critChance=1;Lab.hit(Lab.state.units[0],Lab.state.units[4],{name:'Крит',lo:100,hi:100,damage:'magic',undodgeable:true})")
 assert p.evaluate('Lab.state.units[4].stress===0&&Lab.state.units[5].stress===0')
 ok('Creature mechanics work: wolf pack damage, slowing web and skeleton resistance to piercing')
 p.select_option('#scenario','convoy');assert p.evaluate('Lab.state.enemyType')=='heroes'
 assert p.locator('#enemyType').is_disabled()
 # Prisoner extraction is no longer an automatic win; both completion routes follow it.
 p.evaluate("const o=Lab.state.objective;Object.assign(o.prisoner,{status:'free',q:1,r:5,ap:2});o.wagon.stopped=true;Lab.render()")
 p.click('[data-objective="selectPrisoner"]');p.locator('[data-q="0"][data-r="5"]').click()
 assert p.evaluate('Lab.state.winner===null&&Lab.state.objective.prisoner.status==="evacuated"')
 assert p.locator('#result').is_hidden()
 # Each actual hero must leave, and cannot act or occupy a cell afterward.
 for i,r in enumerate([4,5,6,4]):
  p.evaluate(f"Object.assign(Lab.state.units[{i}],{{q:0,r:{r}}});Lab.render()")
  p.click(f'[data-select="p{i}"]');p.click('[data-objective="evacuateHero"]')
  assert p.evaluate(f'Lab.state.units[{i}].evacuated')
  assert p.locator(f'[data-unit="p{i}"]').count()==0, (i,p.evaluate("[...document.querySelectorAll('[data-unit]')].map(n=>[n.dataset.unit,n.parentNode.id])"),errors)
  if i<3:assert p.evaluate('Lab.state.winner===null')
 assert p.evaluate('Lab.state.winner===0&&Lab.state.objective.outcome==="rescued-withdrawal"')
 ok('Prisoner extraction keeps battle active; only evacuation of all four heroes wins by withdrawal')
 p.evaluate("Lab.reset('convoy');Lab.state.objective.prisoner.status='evacuated';for(const u of Lab.state.units.filter(u=>u.side===1)){u.hp=0;u.ap=0}Object.assign(Lab.state.units[4],{q:5,r:3,hp:1});Lab.apply(Lab.state.units[0],Lab.state.units[4],'attack');Lab.render()")
 assert p.evaluate('Lab.state.winner===0&&Lab.state.objective.outcome==="rescued-combat"')
 ok('Alternatively, after rescue the last defeated guard wins without requiring hero evacuation')
 # Carry and withdraw with a downed hero.
 p.evaluate("Lab.reset('convoy');Lab.state.objective.prisoner.status='evacuated';Object.assign(Lab.state.units[0],{q:1,r:5,hp:0,ap:0});Object.assign(Lab.state.units[1],{q:1,r:4});Lab.state.units[2].evacuated=true;Lab.state.units[3].evacuated=true;Lab.render()")
 p.click('[data-select="p1"]');p.click('[data-objective="carry:p0"]')
 assert p.evaluate('Lab.state.units[1].ap===2&&Lab.state.units[1].carrying==="p0"&&Lab.state.units[0].carriedBy==="p1"')
 assert p.evaluate("Lab.paths(Lab.state.units[1]).get('0,5').cost")==2
 p.locator('[data-q="0"][data-r="5"]').click();p.click('[data-objective="evacuateHero"]')
 assert p.evaluate('Lab.state.winner===0&&Lab.state.units[0].evacuated&&Lab.state.units[0].hp===0&&Lab.state.units[1].evacuated')
 ok('One AP picks up a downed ally, carrying slows movement and both can evacuate together without reviving the casualty')
 p.evaluate("Lab.reset('convoy');Lab.state.objective.prisoner.status='evacuated';Object.assign(Lab.state.units[0],{q:1,r:5,hp:0,ap:0});Object.assign(Lab.state.units[1],{q:1,r:4});Object.assign(Lab.state.units[2],{q:2,r:5,hp:0,ap:0});Lab.state.units[3].evacuated=true;Lab.render()")
 p.click('[data-select="p1"]');p.click('[data-objective="carry:p0"]');p.locator('[data-q="0"][data-r="5"]').click()
 assert p.locator('[data-objective="evacuateHero"]').is_disabled()
 p.click('[data-objective="deliverCargo"]')
 assert p.evaluate('Lab.state.units[0].evacuated&&!Lab.state.units[1].evacuated&&!Lab.state.units[1].carrying&&Lab.state.winner===null')
 ok('Carrier can deliver a casualty and return; final hero cannot silently abandon other downed allies')
 p.evaluate("Lab.reset('convoy');Object.assign(Lab.state.units[0],{q:4,r:5,hp:0,ap:0});Object.assign(Lab.state.units[1],{q:4,r:4});Lab.carryHero(Lab.state.units[1],'p0');Lab.hit(Lab.state.units[4],Lab.state.units[1],{name:'Удар',lo:1000,hi:1000,damage:'magic',undodgeable:true,noCrit:true});Lab.render()")
 assert p.evaluate('!Lab.state.units[0].carriedBy&&!Lab.state.units[0].evacuated&&!Lab.state.units[1].carrying&&Lab.state.units[0].hp===0')
 ok('Falling carrier drops the casualty back onto the battlefield instead of granting extraction')
 # Complete representative high-level creature battles using legal actions.
 p.select_option('#scenario','equal')
 results=p.evaluate("""async()=>{const out=[];for(const [level,pack] of [[5,'spiders'],[8,'undead'],[8,'ogres'],[8,'trolls'],[8,'eliteUndead'],[8,'ancientUndead']]){document.getElementById('playerLevel').value=level;document.getElementById('enemyLevel').value=level;document.getElementById('enemyType').value=pack;Lab.reset('equal');let n=0;while(Lab.state.winner===null&&n++<40){for(const u of Lab.state.units.filter(u=>u.side===0&&u.hp>0)){document.querySelector('[data-select="'+u.id+'"]').click();let moves=0;while((u.ap>0||u.stride>0)&&Lab.state.winner===null&&moves++<12){let acted=false;if(u.type==='acolyte'){const t=Lab.state.units.filter(t=>t.side===0&&t.hp<=t.max-10).find(t=>!Lab.check(u,t,'heal'));if(t)acted=Lab.apply(u,t,'heal')}if(!acted){const t=Lab.state.units.filter(t=>t.side===1&&t.hp>0).sort((a,b)=>a.hp-b.hp).find(t=>Lab.forecast(u,t,'attack').ok);if(t)acted=Lab.apply(u,t,'attack')}if(!acted){const dest=Lab.approach(u,Lab.state.units.filter(t=>t.side===1&&t.hp>0));if(dest){await Lab.chooseTile(dest.q,dest.r);acted=true}}if(!acted)break}}if(Lab.state.winner===null){Lab.skipAll();await Lab.endTurn()}}out.push({level,pack,winner:Lab.state.winner,round:Lab.state.round})}return out}""")
 assert all(v['winner'] is not None and v['round']<=40 for v in results),results
 print('High-level battles:',results,flush=True)
 ok('Representative level-five and level-eight creature battles reach a result without stalled AI')
 # Copied settings must survive a fresh offline browser context.
 p.select_option('#scenario','cover');p.select_option('#enemyType','ogres');p.select_option('#playerLevel','8');p.select_option('#enemyLevel','5');p.select_option('#warriorSub','bastion');p.fill('#critChance','20');p.dispatch_event('#critChance','change')
 p.screenshot(path='/tmp/battle-lab-085-levels.png',full_page=True)
 with p.expect_download() as dl:p.click('#download')
 raw=Path(dl.value.path()).read_text();fresh=b.new_context();copy=fresh.new_page();copy.route('**/*',lambda route:route.abort());copy.set_content(raw)
 assert copy.evaluate('Lab.state.playerLevel===8&&Lab.state.enemyLevel===5&&Lab.state.enemyType==="ogres"&&Lab.state.critChance===.2&&Lab.state.units[0].sub==="bastion"')
 fresh.close();p.set_viewport_size({'width':390,'height':844});assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert not errors,errors
 ok('Offline copy preserves levels, subclasses, creatures and critical settings; expanded controls fit narrow screens')
 b.close()
server.shutdown();print(len(passed),'progression and evacuation scenarios passed.')
