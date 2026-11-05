"""Original pixel assets, real subclass silhouettes, zoom and offline rendering."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright
import base64,json,os
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
 p=b.new_page(viewport={'width':1700,'height':1200});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto(f'http://127.0.0.1:{server.server_port}/battle-lab.html');p.uncheck('#motion')
 # Inspect decoded assets, not just a CSS pixelation flag. Body edges are hard,
 # silhouettes fit their frames and every subclass has genuinely different art.
 result=p.evaluate('''async()=>{const designs=PixelSprites.designs,signatures=new Set(),counts=[];for(const u of designs){const sp=PixelSprites.sprite({...u,side:0}),im=new Image();im.src=sp.body;await im.decode();if(im.naturalWidth!==40||im.naturalHeight!==48)throw Error('Wrong source resolution');const cv=document.createElement('canvas');cv.width=40;cv.height=48;const c=cv.getContext('2d');c.drawImage(im,0,0);const a=c.getImageData(0,0,40,48).data;const colors=new Set();let solid=0;for(let n=0;n<a.length;n+=4){if(a[n+3]!==0&&a[n+3]!==255)throw Error('Antialiased body edge');if(a[n+3]){solid++;colors.add([a[n],a[n+1],a[n+2]].join(','))}}if(solid<60||colors.size>48)throw Error('Empty or unbounded palette');counts.push(colors.size);signatures.add(sp.body+sp.gear)}return {designs:designs.length,unique:signatures.size,maxColors:Math.max(...counts)}}''')
 assert result['designs']==36 and result['unique']==36,result
 assert p.locator('#board .hero-figure path').count()==0
 assert p.locator('#board .pixel-body').count()==8
 assert p.locator('#board .pixel-terrain').count()==160
 print('PASS: 36 original 40×48 designs have distinct artwork, hard alpha edges and limited palettes',flush=True)
 for name in ['wolves','spiders','undead','goblins','kobolds','ogres','beasts']:
  p.select_option('#enemyType',name);assert p.locator('#board .monster-figure image.pixel-body').count()==4
 p.select_option('#scenario','convoy');assert p.locator('#board image.pixel-wagon').count()==1
 p.select_option('#scenario','cover');p.select_option('#playerLevel','5');p.select_option('#warriorSub','berserker');p.select_option('#archerSub','sniper');p.select_option('#mageSub','elementalist');p.select_option('#engineerSub','armorer')
 assert p.locator('#board .hero-figure[data-subclass="berserker"]').count()==2
 for _ in range(3):p.click('#zoomIn')
 assert p.locator('#board .pixel-body').first.evaluate("e=>getComputedStyle(e).imageRendering")=='pixelated'
 p.screenshot(path='/tmp/battle-lab-087-pixels.png',full_page=True)
 p.set_viewport_size({'width':390,'height':844});p.click('#zoomFit')
 assert p.locator('.roster-sprite image').first.evaluate("e=>getComputedStyle(e).imageRendering")=='pixelated'
 p.screenshot(path='/tmp/battle-lab-087-mobile.png',full_page=True)
 print('PASS: Creature packs, wagon, portraits and enlarged battlefield use pixel assets on desktop and mobile',flush=True)
 atlas=p.evaluate('PixelSprites.atlas()');Path('/tmp/pixel-sprites-087.png').write_bytes(base64.b64decode(atlas['png'].split(',',1)[1]));Path('/tmp/pixel-sprites-087.json').write_text(json.dumps(atlas['meta'],ensure_ascii=False,indent=2)+'\n')
 names={'bastion':'Бастион','berserker':'Берсерк','sniper':'Снайпер','swift':'Стриж','assassin':'Ассасин','thief':'Вор','priest':'Жрец','highpriest':'Верховный жрец','elementalist':'Стихийник','cultist':'Культист','paladin':'Паладин','armorer':'Бронник','demolitionist':'Подрывник','fortifier':'Фортификатор'}
 items=p.evaluate("PixelSprites.designs.filter(u=>u.sub!=='base').map(u=>({...u,...PixelSprites.sprite(u),bodyPixels:null,gearPixels:null}))")
 cards=[]
 for u in items:
  bound=u['gearBounds'];gear=f'<img src="{u["gear"]}" style="left:{bound["x"]*3}px;top:{bound["y"]*3}px;width:{bound["w"]*3}px;height:{bound["h"]*3}px">' if bound else ''
  cards.append(f'<article><h2>{names[u["sub"]]}</h2><div class="sprite"><img src="{u["body"]}" width="120" height="144">{gear}</div></article>')
 gallery=b.new_page(viewport={'width':1000,'height':920});gallery.set_content('<meta charset="utf-8"><style>body{margin:0;padding:20px;background:#14251f;color:#edcc86;font:16px system-ui}h1{font-size:24px;margin:0 0 15px}main{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}article{text-align:center;background:#243c2f;border:1px solid #68775b;padding:12px}h2{font-size:16px;margin:0 0 5px}.sprite{position:relative;width:120px;height:144px;margin:auto}.sprite img{position:absolute;left:0;top:0;image-rendering:pixelated}</style><h1>Туман и кости · Пиксельные подклассы · 40 × 48, масштаб ×3</h1><main>'+''.join(cards)+'</main>');gallery.screenshot(path='/tmp/pixel-subclasses-087.png',full_page=True);gallery.close()
 with p.expect_download() as dl:p.click('#download')
 copy=b.new_page();copy.route('**/*',lambda route:route.abort());copy.set_content(Path(dl.value.path()).read_text());assert copy.locator('#board .pixel-body').count()==8
 assert copy.locator('#board .hero-figure[data-subclass="armorer"]').count()==2
 print('PASS: Offline combat copy preserves pixel sprites and subclass settings without network access',flush=True)
 assert not errors,errors
 b.close()
server.shutdown()
