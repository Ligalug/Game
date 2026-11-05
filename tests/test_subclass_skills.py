"""Subclass action replacement, real skill effects, tier gates and elite creatures."""
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
 p.goto(url);p.uncheck('#motion');p.fill('#critChance','0');p.dispatch_event('#critChance','change')
 assert p.evaluate("document.getElementById('engineerSub').closest('details').querySelector('summary').textContent.includes('Уровни')")
 p.select_option('#squad','classic');assert p.locator('#engineerSub').is_disabled()
 p.select_option('#squad','engineer');assert p.locator('#engineerSub').is_enabled()
 ok('Engineer subclasses are in the shared open settings panel and explain how to enable the engineer slot')
 p.select_option('#playerLevel','3');assert p.evaluate('Lab.state.enemyLevel')==3
 p.select_option('#enemyLevel','1');p.select_option('#playerLevel','2');assert p.evaluate('Lab.state.enemyLevel')==1
 p.select_option('#playerLevel','1');p.check('#autoEnemyLevel')
 cases=[('warriorSub','p0','bastion',['shieldBash','coverAlly']),('warriorSub','p0','berserker',['cleave','rage']),('archerSub','p1','sniper',['aimShot','pinShot']),('archerSub','p1','swift',['doubleShot','skirmishShot']),('rogueSub','p2','assassin',['backstab','smoke']),('rogueSub','p2','thief',['hamstring','sand']),('mageSub','p3','priest',['priestHeal','blessing']),('mageSub','p3','highpriest',['greaterHeal','sanctuary']),('mageSub','p3','elementalist',['fireball','iceLance']),('mageSub','p3','cultist',['drainLife','curse']),('mageSub','p3','paladin',['smite','layHands']),('engineerSub','p2','armorer',['powerarmor','armorPunch']),('engineerSub','p2','demolitionist',['mine','blastCharge']),('engineerSub','p2','fortifier',['fortify','bridge'])]
 for selector,hero,sub,expected in cases:
  p.select_option('#squad','engineer' if selector=='engineerSub' else 'classic')
  p.select_option('#'+selector,sub);p.click('[data-select="'+hero+'"]')
  actions=p.locator('#actions [data-action]').evaluate_all("els=>els.map(e=>e.dataset.action).filter(a=>!['attack','move','guard','skip'].includes(a))")
  assert actions==expected,(sub,actions)
 ok('All fourteen subclass selections replace parent abilities with their own visible action sets')
 equipment={'bastion':'tower-shield','berserker':'great-axe','sniper':'longbow','swift':'shortbow','assassin':'twin-daggers','thief':'purse-lockpicks','priest':'sun-staff','highpriest':'mitre-crozier','elementalist':'fire-ice','cultist':'skull-staff','paladin':'holy-shield-mace','armorer':'power-gauntlet','demolitionist':'bomb-bandolier','fortifier':'hammer-blueprint'}
 gallery=[]
 for selector,hero,sub,expected in cases:
  p.select_option('#squad','engineer' if selector=='engineerSub' else 'classic');p.select_option('#'+selector,sub)
  figure=p.locator('#board [data-unit="'+hero+'"] .hero-figure')
  assert figure.get_attribute('data-equipment')==equipment[sub]
  assert p.locator('[data-select="'+hero+'"] .roster-sprite .hero-figure').get_attribute('data-equipment')==equipment[sub]
  if sub=='sniper':longbow=figure.locator('[data-item="longbow"]').evaluate('(e)=>e.getBBox().height')
  if sub=='swift':shortbow=figure.locator('[data-item="shortbow"]').evaluate('(e)=>e.getBBox().height')
  gallery.append(p.evaluate("id=>{const u=Lab.state.units.find(u=>u.id===id);return {name:Lab.role(u),svg:Lab.figure(u)}}",hero))
 assert longbow>shortbow*1.7
 cells=[]
 for i,entry in enumerate(gallery):
  x=(i%4)*250;y=(i//4)*205
  cells.append(f'<g transform="translate({x},{y})"><rect x="5" y="5" width="238" height="193" rx="10" fill="#20392c" stroke="#8b9264"/><text x="125" y="30" text-anchor="middle" fill="#edd391" font-size="19" font-family="Georgia">{entry["name"]}</text><ellipse cx="125" cy="168" rx="45" ry="13" fill="#12271e"/><g transform="translate(125,120) scale(1.4)">{entry["svg"]}</g></g>')
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="820" viewBox="0 0 1000 820"><rect width="1000" height="820" fill="#14251f"/>'+''.join(cells)+'</svg>'
 Path('/tmp/subclass-looks-086.svg').write_text(svg)
 preview=b.new_page(viewport={'width':1000,'height':820});preview.set_content('<style>body{margin:0;background:#14251f}</style>'+svg);preview.screenshot(path='/tmp/subclass-looks-086.png');preview.close()
 ok('All subclasses have distinct equipment silhouettes in field and roster; longbow is visibly longer than shortbow')
 p.select_option('#squad','classic');p.select_option('#warriorSub','bastion');p.click('[data-select="p0"]')
 p.evaluate("Object.assign(Lab.state.units[4],{q:3,r:3,hp:100});Lab.render()")
 p.click('[data-action="shieldBash"]');p.locator('[data-q="3"][data-r="3"]').click()
 assert p.evaluate('Lab.state.units[4].slow===1&&Lab.state.units[0].ap===1')
 p.click('[data-action="coverAlly"]');p.locator('[data-q="2"][data-r="4"]').click()
 assert p.evaluate('Lab.state.units[1].protected===2&&Lab.state.units[0].ap===0&&Lab.state.units[0].skillCD.shieldBash===3&&Lab.state.units[0].skillCD.coverAlly===3')
 ok('Bastion bash slows an enemy and a separate one-AP ally protection still works during bash cooldown')
 p.select_option('#warriorSub','berserker');p.click('[data-select="p0"]')
 before=p.evaluate("({d:Lab.spec(Lab.state.units[0],'attack').lo,r:Lab.defense(Lab.state.units[0],'piercing')})")
 p.click('[data-action="rage"]')
 after=p.evaluate("({d:Lab.spec(Lab.state.units[0],'attack').lo,r:Lab.defense(Lab.state.units[0],'piercing')})")
 assert after['d']==before['d']+3 and after['r']==before['r']-10
 assert p.locator('[data-action="rage"]').is_disabled()
 ok('Berserker rage changes actual damage and defense and cannot stack')
 p.select_option('#archerSub','sniper');p.click('[data-select="p1"]');p.evaluate("Object.assign(Lab.state.units[4],{q:8,r:4,hp:100});Lab.render()")
 p.click('[data-action="aimShot"]');p.locator('[data-q="8"][data-r="4"]').click()
 assert p.evaluate('Lab.state.units[4].hp<100&&Lab.state.units[1].ap===1')
 p.click('[data-action="pinShot"]');p.locator('[data-q="8"][data-r="4"]').click()
 assert p.evaluate('Lab.state.units[4].slow===1&&Lab.state.units[1].ap===0')
 p.select_option('#archerSub','swift');p.click('[data-select="p1"]');p.evaluate("Object.assign(Lab.state.units[4],{q:4,r:4,hp:100});Lab.render()")
 f=p.evaluate("Lab.forecast(Lab.state.units[1],Lab.state.units[4],'doubleShot')")
 p.click('[data-action="doubleShot"]');p.locator('[data-q="4"][data-r="4"]').click()
 loss=p.evaluate('100-Lab.state.units[4].hp');assert f['lo']*2<=loss<=f['hi']*2
 p.click('[data-action="skirmishShot"]');p.locator('[data-q="4"][data-r="4"]').click()
 assert p.evaluate('Lab.state.units[1].ap===0&&Lab.state.units[1].stride===2')
 ok('Sniper shots have distinct reach and control; Swift performs two hits and earns movement from its other shot')
 p.select_option('#rogueSub','assassin');p.click('[data-select="p2"]');p.evaluate("Object.assign(Lab.state.units[4],{q:3,r:5,hp:100});Lab.render()")
 assert p.evaluate("Lab.forecast(Lab.state.units[2],Lab.state.units[4],'backstab').critChance")==.25
 p.click('[data-action="smoke"]');assert abs(p.evaluate('Lab.stats(Lab.state.units[2]).dodge')-.45)<1e-8
 p.select_option('#rogueSub','thief');p.click('[data-select="p2"]');p.evaluate("Object.assign(Lab.state.units[4],{q:3,r:5,hp:100});Lab.render()")
 p.click('[data-action="sand"]');p.locator('[data-q="3"][data-r="5"]').click()
 p.click('[data-action="hamstring"]');p.locator('[data-q="3"][data-r="5"]').click()
 assert p.evaluate('Lab.state.units[4].weaken===1&&Lab.state.units[4].slow===1')
 ok('Assassin gains critical opportunity and smoke evasion; Thief can weaken and slow a nearby enemy')
 p.select_option('#mageSub','priest');p.click('[data-select="p3"]');p.evaluate('Lab.state.units[0].hp=0;Lab.state.units[0].ap=0;Lab.render()')
 assert not p.evaluate("Lab.forecast(Lab.state.units[3],Lab.state.units[0],'heal').ok")
 p.click('[data-action="priestHeal"]');p.locator('[data-q="2"][data-r="3"]').click()
 assert p.evaluate('Lab.state.units[0].hp===16&&Lab.state.units[0].ap===1')
 p.click('[data-action="blessing"]');p.locator('[data-q="2"][data-r="3"]').click()
 assert p.evaluate('Lab.state.units[0].protected===2')
 p.select_option('#mageSub','highpriest');p.click('[data-select="p3"]');p.evaluate('Lab.state.units[0].hp=1;Lab.state.units[0].slow=1;Lab.state.units[0].weaken=1;Lab.render()')
 p.click('[data-action="greaterHeal"]');p.locator('[data-q="2"][data-r="3"]').click()
 assert p.evaluate('Lab.state.units[0].slow===0&&Lab.state.units[0].weaken===0&&Lab.state.units[0].hp>1')
 p.select_option('#mageSub','highpriest');p.click('[data-select="p3"]');p.click('[data-action="sanctuary"]');p.locator('[data-q="2"][data-r="4"]').click()
 assert p.evaluate('Lab.state.units.slice(0,3).every(u=>u.protected===2)')
 ok('Priest uses its own heal and blessing; High Priest cleanses conditions and protects several allies')
 p.select_option('#mageSub','elementalist');p.click('[data-select="p3"]');p.evaluate("Object.assign(Lab.state.units[4],{q:5,r:6,hp:100});Object.assign(Lab.state.units[5],{q:5,r:5,hp:100,type:'warrior'});Lab.render()")
 p.click('[data-action="fireball"]');p.locator('[data-q="5"][data-r="6"]').click()
 assert p.evaluate('Lab.state.units[4].hp<100&&Lab.state.units[5].hp<100&&Lab.state.units[4].burn===2')
 p.select_option('#mageSub','elementalist');p.click('[data-select="p3"]');p.evaluate("Object.assign(Lab.state.units[4],{q:6,r:6,hp:100});Lab.render()")
 p.click('[data-action="iceLance"]');p.locator('[data-q="6"][data-r="6"]').click();assert p.evaluate('Lab.state.units[4].slow===1')
 p.select_option('#mageSub','cultist');p.click('[data-select="p3"]');p.evaluate("Object.assign(Lab.state.units[4],{q:6,r:6,hp:100});Lab.state.units[3].hp=1;Lab.render()")
 p.click('[data-action="curse"]');p.locator('[data-q="6"][data-r="6"]').click()
 assert p.evaluate('Lab.state.units[4].weaken===1&&Lab.state.units[4].exposed===1')
 before=p.evaluate('Lab.state.units[3].hp');p.click('[data-action="drainLife"]');p.locator('[data-q="6"][data-r="6"]').click()
 assert p.evaluate('Lab.state.units[3].hp')>before
 ok('Elementalist has area fire and slowing ice; Cultist curses and actually drains health')
 p.select_option('#mageSub','paladin');p.click('[data-select="p3"]');p.evaluate("Object.assign(Lab.state.units[4],{q:3,r:6,hp:100,type:'skeleton'});Lab.state.units[2].hp=1;Lab.render()")
 normal=p.evaluate("Lab.spec(Lab.state.units[3],'smite').lo");undead=p.evaluate("Lab.spec(Lab.state.units[3],'smite',Lab.state.units[4]).lo");assert undead==normal+4
 p.click('[data-action="layHands"]');p.locator('[data-q="2"][data-r="5"]').click();assert p.evaluate('Lab.state.units[2].hp>1')
 ok('Paladin has adjacent healing and a melee magical strike with a real undead damage bonus')
 p.select_option('#playerLevel','1');p.select_option('#enemyType','wolves')
 assert p.locator('#enemyType option[value="undead"]').get_attribute('disabled') is None
 assert p.locator('#enemyType option[value="ogres"]').get_attribute('disabled') is not None and p.locator('#enemyType option[value="trolls"]').get_attribute('disabled') is not None, p.evaluate("({level:document.getElementById('playerLevel').value,options:document.getElementById('enemyType').innerHTML})")
 p.select_option('#playerLevel','2');assert p.locator('#enemyType option[value="spiders"]').get_attribute('disabled') is None
 p.select_option('#playerLevel','5');assert p.locator('#enemyType option[value="ogres"]').get_attribute('disabled') is None and p.locator('#enemyType option[value="trolls"]').get_attribute('disabled') is None
 assert p.locator('#enemyType option[value="eliteUndead"]').get_attribute('disabled') is not None
 p.select_option('#playerLevel','6');assert p.locator('#enemyType option[value="eliteUndead"]').get_attribute('disabled') is None
 assert p.locator('#enemyType option[value="ancientUndead"]').get_attribute('disabled') is not None
 p.select_option('#playerLevel','8');p.select_option('#enemyType','ancientUndead');assert p.evaluate('Lab.state.units[4].type')=='wightlord'
 p.select_option('#playerLevel','1');assert p.evaluate('Lab.state.enemyType')=='wolves'
 ok('Enemy pack gates follow player level from wolves and skeletons to ogres, trolls, elite and ancient undead')
 p.select_option('#playerLevel','5');p.select_option('#enemyLevel','1');p.select_option('#mageSub','elementalist');p.select_option('#enemyType','trolls')
 p.evaluate('Lab.state.units[4].hp=10;Lab.startSide(1)');assert p.evaluate('Lab.state.units[4].hp')==18
 p.evaluate("Lab.startSide(0);Object.assign(Lab.state.units[4],{q:6,r:6,hp:40});Lab.render()")
 p.click('[data-select="p3"]');p.click('[data-action="fireball"]');p.locator('[data-q="6"][data-r="6"]').click()
 hp=p.evaluate('Lab.state.units[4].hp');p.evaluate('Lab.startSide(1)');assert p.evaluate('Lab.state.units[4].hp')==hp
 p.evaluate('Lab.state.units[4].burn=0;Lab.startSide(1)');assert p.evaluate('Lab.state.units[4].hp')>hp
 p.evaluate('Lab.state.units[4].hp=0;Lab.startSide(1)');assert p.evaluate('Lab.state.units[4].hp')==0
 ok('Living trolls regenerate; fire suppresses regeneration and dead trolls never revive')
 p.select_option('#playerLevel','8')
 for pack in ['eliteUndead','ancientUndead','mountainTrolls']:
  p.select_option('#enemyType',pack);assert p.locator('#board .monster-figure').count()==4
  p.evaluate('Lab.skipAll()');p.click('#end');p.wait_for_function('!Lab.busy')
  assert p.evaluate('Lab.state.units.every(u=>u.ap>=0&&u.hp>=0)')
 ok('Late-game packs use distinct creature types and can complete AI turns')
 p.select_option('#scenario','cover');p.select_option('#squad','engineer');p.select_option('#engineerSub','demolitionist');p.click('[data-select="p2"]')
 p.screenshot(path='/tmp/battle-lab-086-subclasses.png',full_page=True)
 with p.expect_download() as dl:p.click('#download')
 copy=b.new_page();copy.route('**/*',lambda route:route.abort());copy.set_content(Path(dl.value.path()).read_text())
 assert copy.evaluate('Lab.state.playerLevel===8&&Lab.state.units[2].sub==="demolitionist"&&Lab.abilities(Lab.state.units[2]).includes("blastCharge")')
 copy.close();p.set_viewport_size({'width':390,'height':844});assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert not errors,errors
 ok('Offline copy retains subclass skills and pack selection; settings remain usable on narrow screens')
 b.close()
server.shutdown();print(len(passed),'subclass and tier scenarios passed.')
