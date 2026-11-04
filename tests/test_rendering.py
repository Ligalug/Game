"""Native pixel rendering and real map/battle input at multiple display scales."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/'
out=Path('/tmp/tik-rendering-checks');out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-webgl'])
 for dpr in [1,1.25,2]:
  c=b.new_context(device_scale_factor=dpr,viewport={'width':1500,'height':1000});pg=c.new_page();errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.goto(url);pg.wait_for_function('Game.painter.ready');pg.evaluate('Game.fx.configure({enabled:false});Game.newGame(2026)')
  result=pg.evaluate("""()=>{const cv=document.getElementById('map');return{width:cv.width,css:cv.clientWidth,height:cv.height,cssh:cv.clientHeight};}""")
  assert abs(result['width']-result['css']*dpr)<=1,result
  assert abs(result['height']-result['cssh']*dpr)<=1,result
  for zoom in ['home','in','out','all']:
   pg.evaluate('(mode)=>Game.painter.control(mode)',zoom)
   pg.evaluate('Game.ui.selected=34')
   point=pg.evaluate('Game.painter.project(35)');pg.mouse.click(point['x'],point['y'])
   assert pg.evaluate('Game.ui.selected')==35,(dpr,zoom,point)
  pg.evaluate("Game.painter.control('home')")
  if dpr==1:pg.screenshot(path=str(out/'tuman-i-kosti-051-crisp-map.png'))
  pg.evaluate("()=>{const a=Game.state.factions[0].armies[0];Game.startBattle(a,null,{kind:'ambush',title:'Проверка чёткости',pos:a.pos});const b=Game.state.battle;b.side=b.human;const u=b.units.find(u=>u.side===b.human);Game.ui.battleSelected=u.id;Game.ui.mode='attack';u.ap=2;}")
  u=pg.evaluate('Game.state.battle.units.find(u=>u.side===Game.state.battle.human&&u.id!==Game.ui.battleSelected)');point=pg.evaluate("(p)=>Game.painter.project(p,'battle')",u['pos']);pg.mouse.click(point['x'],point['y'])
  assert pg.evaluate('Game.ui.battleSelected')==u['id']
  target=pg.evaluate('(id)=>{const b=Game.state.battle,u=b.units.find(u=>u.id===id);return [...Game.battleReach(u).keys()].find(p=>p!==u.pos);}',u['id'])
  point=pg.evaluate("(p)=>Game.painter.project(p,'battle')",target);pg.mouse.click(point['x'],point['y'])
  assert pg.evaluate('(id)=>Game.state.battle.units.find(u=>u.id===id).pos',u['id'])==target
  result=pg.evaluate("""()=>{const cv=document.getElementById('battleCanvas');return{width:cv.width,css:cv.clientWidth};}""")
  assert abs(result['width']-result['css']*dpr)<=1,result
  if dpr==1:pg.screenshot(path=str(out/'tuman-i-kosti-051-crisp-battle.png'))
  assert not errors,errors
  print('PASS native rendering and map/battle picking, pixel ratio',dpr,flush=True)
  c.close()
 b.close()
server.shutdown()
print('3 display-scale scenarios passed.')
