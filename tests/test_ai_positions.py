"""Regression: enemies keep an attack position instead of spending AP/stride shuffling."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 p=b.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.set_content((ROOT/'battle-lab.html').read_text());p.uncheck('#motion')
 def setup(kind='warrior',q=5,r=3):
  p.evaluate('''({kind,q,r})=>{Lab.reset('equal');for(const t of Object.values(Lab.state.tiles)){t.kind='plain';t.height=0}for(const u of Lab.state.units){u.hp=0;u.ap=0;u.stride=0}const a=Lab.state.units[0],e=Lab.state.units[4];Object.assign(a,{q:2,r:3,hp:1000,max:1000});Object.assign(e,{type:kind,sub:'base',q,r,hp:1000,max:1000,heals:0,cooldown:100,skillCD:{},stress:0});Lab.state.critChance=0;Lab.render()}''',{'kind':kind,'q':q,'r':r})
 setup(q=3)
 assert p.evaluate('Lab.approach(Lab.state.units[4],[Lab.state.units[0]])===null')
 setup('archer',6)
 assert p.evaluate('Lab.approach(Lab.state.units[4],[Lab.state.units[0]])===null')
 print('PASS: Melee and ranged enemies keep a currently valid attack position',flush=True)
 setup(q=3)
 assert p.evaluate("()=>{const e=Lab.state.units[4],t=Lab.state.units[0];Lab.state.side=1;e.ap=3;e.cooldown=0;return Lab.apply(e,t,'break')&&e.cooldown>Lab.state.round&&Lab.apply(e,t,'attack')&&e.ap===0}")
 print('PASS: Special cooldown still permits a basic attack with the remaining AP',flush=True)
 setup()
 p.evaluate('Lab.skipAll();Lab.endTurn()');p.wait_for_function('!Lab.busy')
 assert p.evaluate('Lab.state.damage>0&&Lab.state.moves===1&&Lab.distance(Lab.state.units[4],Lab.state.units[0])===1'),p.evaluate('({moves:Lab.state.moves,damage:Lab.state.damage})')
 print('PASS: Enemy closes in once and spends remaining AP attacking without shuffling on leftover steps',flush=True)
 setup('archer',3)
 p.evaluate('Lab.skipAll();Lab.endTurn()');p.wait_for_function('!Lab.busy')
 assert p.evaluate('Lab.state.damage>0&&Lab.state.moves===1&&Lab.distance(Lab.state.units[4],Lab.state.units[0])>1')
 print('PASS: Engaged archer retreats once, then shoots rather than wandering',flush=True)
 setup(q=12)
 for _ in range(4):
  if p.evaluate('Lab.state.damage>0'):break
  p.evaluate('Lab.skipAll();Lab.endTurn()');p.wait_for_function('!Lab.busy')
 assert p.evaluate('Lab.state.damage>0')
 print('PASS: Distant melee enemy still approaches across several turns and attacks',flush=True)
 assert not errors,errors
 b.close()
