"""Objective-based combat: movement of the convoy, rescue, extraction and failures."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright
import os,json
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
 p.goto(url);p.uncheck('#motion');p.fill('#critChance','0');p.dispatch_event('#critChance','change');p.select_option('#scenario','convoy')
 assert p.locator('#objectivePanel').is_visible()
 assert p.evaluate('Lab.state.units.length===8&&Lab.state.objective.wagon.q===7&&Lab.state.objective.prisoner.status==="caged"')
 assert p.locator('[data-objective="stopWagon"]').is_disabled()
 assert not p.evaluate("Lab.objectiveAction('freePrisoner')")
 ok('Convoy scenario has four heroes per side, explicit mission stages and gated interactions')
 result=p.evaluate("()=>{Lab.reset('equal');const u=Lab.state.units[0],t=Lab.state.units[4];Object.assign(t,{q:3,r:3,hp:100});const first=Lab.apply(u,t,'attack'),second=Lab.apply(u,t,'attack');return {first,second,ap:u.ap}}")
 assert result=={'first':True,'second':True,'ap':1}
 p.evaluate("Lab.reset('convoy')")
 ok('Repeated normal attacks remain available; attacking does not end the hero turn')
 # A real first round, no state edits: two heroes cooperate to stop and unlock.
 p.click('[data-select="p1"]');p.locator('[data-q="6"][data-r="5"]').click()
 assert p.evaluate('Lab.state.units[1].ap===2')
 p.click('[data-objective="stopWagon"]')
 assert p.evaluate('Lab.state.objective.wagon.stopped&&Lab.state.units[1].ap===0')
 p.click('[data-select="p2"]');p.locator('[data-q="7"][data-r="4"]').click();p.click('[data-objective="freePrisoner"]')
 assert p.evaluate('Lab.state.objective.prisoner.status==="free"&&Lab.state.objective.prisoner.ap===1&&Lab.selected==="prisoner"')
 assert p.locator('[data-action="attack"]').count()==0
 assert p.locator('[data-action="move"]').count()==1
 assert p.evaluate('Lab.pending().some(u=>u.id==="prisoner")')
 ok('Through normal UI actions, one hero stops the wagon and another frees a separately controlled noncombatant')
 # Exit needs a second turn; enemies remain alive throughout the objective win.
 p.locator('[data-q="4"][data-r="6"]').click()
 assert p.evaluate('Lab.state.objective.prisoner.q===4&&Lab.state.objective.prisoner.ap===0&&Lab.state.winner===null')
 p.evaluate('Lab.skipAll()');p.click('#end');p.wait_for_function('!Lab.busy')
 assert p.evaluate('Lab.state.winner===null&&Lab.state.objective.prisoner.ap===2')
 p.click('[data-objective="selectPrisoner"]');p.locator('[data-q="0"][data-r="6"]').click()
 assert p.evaluate('Lab.state.winner===null&&Lab.state.objective.prisoner.status==="evacuated"&&Lab.state.units.filter(u=>u.side===1&&u.hp>0).length>0')
 assert p.locator('#result').is_hidden()
 assert 'Разбейте охрану' in p.inner_text('#objectivePanel')
 ok('Extracting the prisoner with living guards completes rescue but keeps the battle running')
 # Clear guards doesn't end the mission; extraction remains necessary.
 p.evaluate("Lab.reset('convoy');for(const u of Lab.state.units.filter(u=>u.side===1)){u.hp=0;u.ap=0};Lab.render()")
 # finish is triggered by a final actual hit rather than directly calling internal finish.
 p.evaluate("Object.assign(Lab.state.units[4],{q:5,r:3,hp:1});Lab.apply(Lab.state.units[0],Lab.state.units[4],'attack');Lab.render()")
 assert p.evaluate('Lab.state.winner===null&&Lab.state.objective.cleared&&Lab.state.objective.wagon.stopped')
 ok('Defeating every guard stops the wagon but does not substitute for freeing and extracting the prisoner')
 # Vehicle movement follows end-of-enemy-turn timing; no unconditional round victory.
 p.evaluate("Lab.reset('convoy');for(const u of Lab.state.units)if(u.side===0)u.hp=1000;const guards=Lab.state.units.filter(u=>u.side===1);guards.forEach((u,i)=>Object.assign(u,{q:12+i,r:0}));for(const u of guards)for(const [dq,dr] of [[1,0],[1,-1],[0,-1],[-1,0],[-1,1],[0,1]]){const t=Lab.state.tiles[(u.q+dq)+','+(u.r+dr)];if(t&&!Lab.state.units.some(v=>v.q===t.q&&v.r===t.r))t.kind='rock'}Lab.render()")
 for expected in [9,11,13,15]:
  p.evaluate('Lab.skipAll()');p.click('#end');p.wait_for_function('!Lab.busy')
  assert p.evaluate('Lab.state.objective.wagon.q')==expected
 assert p.evaluate('Lab.state.winner===1&&Lab.state.objective.outcome==="wagon-escaped"')
 ok('Unstopped wagon moves two real cells per enemy turn and escape causes mission failure')
 p.evaluate("Lab.reset('convoy');Object.assign(Lab.state.units[0],{q:8,r:5,hp:1000});Lab.render()")
 p.evaluate('Lab.skipAll()');p.click('#end');p.wait_for_function('!Lab.busy')
 assert p.evaluate('Lab.state.objective.wagon.q===7')
 ok('A hero physically blocking the road delays the convoy')
 # Lay a real mine through the engineer action UI.
 p.select_option('#engineerSub','demolitionist');p.click('[data-select="p2"]');p.locator('[data-q="5"][data-r="6"]').click()
 p.click('[data-action="mine"]');p.locator('[data-q="8"][data-r="5"]').click()
 p.evaluate('Lab.skipAll()');p.click('#end');p.wait_for_function('!Lab.busy')
 assert p.evaluate('Lab.state.objective.wagon.stopped&&Lab.state.objective.stoppedBy==="mine"&&Lab.state.objective.prisoner.hp===16&&Lab.state.mines.length===0')
 ok('A demolitionist mine can stop the moving wagon without harming the prisoner')
 # Recapture outcome, with exact action budget enforced.
 p.evaluate("Lab.reset('convoy');const o=Lab.state.objective;Object.assign(o.prisoner,{status:'free',q:6,r:5,ap:1});Object.assign(Lab.state.units[4],{q:6,r:4,ap:1});Lab.state.side=1;Lab.render()")
 assert not p.evaluate('Lab.capturePrisoner(Lab.state.units[4])')
 p.evaluate('Lab.state.units[4].ap=2')
 assert p.evaluate('Lab.capturePrisoner(Lab.state.units[4])')
 assert p.evaluate('Lab.state.winner===1&&Lab.state.objective.outcome==="recaptured"&&Lab.state.units[4].ap===0')
 ok('Adjacent guards need two AP to recapture; recapture is a distinct failed objective')
 # Empty space is required to release; failed attempt spends no AP.
 p.evaluate("Lab.reset('convoy');Lab.state.objective.wagon.stopped=true;Object.assign(Lab.state.units[0],{q:6,r:5});for(const [q,r] of [[8,5],[8,4],[7,4],[6,6],[7,6]])Lab.state.tiles[q+','+r].kind='rock';Lab.render()")
 assert 'свободный гекс' in p.evaluate("Lab.objectiveCheck(Lab.state.units[0],'freePrisoner')")
 assert not p.evaluate("Lab.objectiveAction('freePrisoner')")
 assert p.evaluate('Lab.state.units[0].ap===3')
 ok('Release rejects a blocked exit from the cage without consuming actions')
 p.evaluate("Lab.reset('convoy')");p.click('#editorToggle');p.select_option('#terrainBrush','water');p.locator('[data-q="8"][data-r="5"]').click()
 assert p.evaluate("Lab.state.tiles['8,5'].kind==='plain'")
 p.locator('[data-q="5"][data-r="2"]').click()
 with p.expect_download() as dl:p.click('#exportLayout')
 layout=json.loads(Path(dl.value.path()).read_text());assert layout['scenario']=='convoy'
 p.locator('#layoutFile').set_input_files({'name':'convoy.json','mimeType':'application/json','buffer':json.dumps(layout).encode()})
 p.wait_for_function("document.getElementById('editorStatus').textContent.includes('загружено')")
 assert p.evaluate("Lab.state.tiles['5,2'].kind==='water'")
 ok('Convoy editor protects route and extraction cells while custom layouts still export/import')
 p.click('#editorToggle');p.click('#restart')
 assert p.evaluate('Lab.state.objective.prisoner.status==="caged"&&Lab.state.objective.wagon.q===7&&Lab.state.round===1')
 assert p.locator('[data-unit="prisoner"]').count()==0
 p.select_option('#scenario','equal')
 assert p.locator('#objectivePanel').is_hidden() and p.locator('.hero-figure').count()==8
 ok('Restart and scenario changes remove objective actors and reset mission state')
 p.select_option('#scenario','convoy');p.check('#motion');p.evaluate('Lab.skipAll()');p.click('#end');p.click('#restart');p.wait_for_timeout(700)
 assert p.evaluate('Lab.state.round===1&&Lab.state.objective.wagon.q===7&&!Lab.busy')
 ok('Restart cancels pending animated guards and wagon movement')
 with p.expect_download() as dl:p.click('#download')
 raw=Path(dl.value.path()).read_text();copy=b.new_page();copy.route('**/*',lambda route:route.abort());copy.set_content(raw)
 copy.select_option('#scenario','convoy');assert copy.evaluate('Lab.state.objective.wagon.q===7')
 copy.close();p.locator('summary').last.click()
 with p.expect_download() as dl:p.click('#report')
 result=json.loads(Path(dl.value.path()).read_text());assert result['version']=='0.8.5-lab' and result['objective']['stage']=='caged' and result['objective']['stoppedBy'] is None
 p.screenshot(path='/tmp/battle-lab-084-convoy.png',full_page=True)
 p.set_viewport_size({'width':390,'height':844});assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert not errors,errors
 ok('Standalone copy, objective report and narrow-screen controls work without browser errors')
 b.close()
server.shutdown();print(len(passed),'convoy scenarios passed.')
