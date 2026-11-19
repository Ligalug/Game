"""Browser acceptance checks for the current campaign rules."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

ROOT = Path(__file__).resolve().parents[1]

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=ROOT))
Thread(target=server.serve_forever, daemon=True).start()
origin = f'http://127.0.0.1:{server.server_port}'

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(
        executable_path=os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium'),
        headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    errors = []
    requests = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('request', lambda request: requests.append(request.url))
    page.goto(origin)
    page.evaluate('Game.fx.configure({enabled:false})')
    page.click('[data-a=start]')
    assert page.locator('[data-a=pickStart]').count() == 10
    page.locator('[data-a=pickStart]').nth(0).click()
    page.locator('[data-a=pickStart]').nth(4).click()
    page.click('[data-a=confirmStart]')
    page.click('[data-a=turnReportDone]')
    assert page.evaluate('player().armies[0].heroes.map(h=>h.cls)') == ['warrior', 'engineer']
    assert not [url for url in requests if url.startswith('http') and not url.startswith(origin + '/')]
    print('PASS offline campaign, five classes and initial party')

    page.click('#nav [data-a=city]')
    page.select_option('#buildSelect', 'market')
    page.click('[data-a=construct]')
    page.select_option('#buildSelect', 'workshop')
    second = page.evaluate('player().town.plots[1]')
    page.locator(f'[data-a=plot][data-pos="{second}"]').click()
    page.click('[data-a=construct]')
    assert page.locator('[data-a=capitalEdit][data-v=cancel]').count() == 2
    assert page.evaluate('player().gold') == 25
    page.click('[data-a=capitalEdit][data-v=first] >> nth=1')
    page.click('[data-a=capitalEdit][data-v=pause] >> nth=0')
    assert page.evaluate('''() => {
      const f=player(), t=f.town;
      Capital.tick(f, 4);
      const market=t.projects.find(q=>q.id==='market');
      if(market.progress!==4 || t.projects[0].progress!==0)return false;
      const gold=f.gold;
      Capital.edit(f,market.plot,'cancel');
      if(f.gold!==gold+26 || !Capital.edit(f,t.projects[0].plot,'pause'))return false;
      if(!Capital.enqueue(f,t.plots[0],'market'))return false;
      if(Capital.enqueue(f,t.plots[2],'market'))return false;
      Capital.tick(f,24);
      return t.buildings[t.plots[1]]==='workshop'&&t.projects[0].progress===8;
    }''')
    print('PASS prepayment, priority, pausing, linear refund, uniqueness and excess production')

    assert page.evaluate('''() => {
      const f=player(), t=f.town, h=f.armies[0].heroes[0], p=t.plots[2];
      f.gold=10000;
      if(!Capital.enqueue(f,p,'plaza'))return false;
      Capital.tick(f,100);
      if(!Capital.buy(f,'warrior','attack')||!Capital.buy(f,'warrior','recruit'))return false;
      if(f.candidates.find(h=>h.cls==='warrior').level!==2||h.level!==1)return false;
      if(!Capital.enqueue(f,f.city,'hall','hall'))return false;
      Capital.tick(f,100);
      if(!Capital.enqueue(f,p,'plaza','floor'))return false;
      Capital.tick(f,100);
      h.level=8;
      if(!Game.chooseSub(h.id,'captain')||Game.chooseSub(h.id,'bastion'))return false;
      if(!Talents.choose(h,2,'Защита')||Talents.choose(h,2,'Нападение')||Talents.choose(h,7))return false;
      if(!Talents.choose(h,6)||!Talents.choose(h,7)||!Talents.choose(h,8))return false;
      if(!Talents.reset(h,f,f.armies[0])||h.sub!=='captain'||Object.keys(h.talents.base).length)return false;
      if(!Capital.buy(f,'warrior','captain:2')||!Capital.buy(f,'warrior','captain:1'))return false;
      if(!Capital.enqueue(f,f.city,'hall','hall'))return false;
      Capital.tick(f,100);
      if(!Capital.enqueue(f,p,'plaza','floor'))return false;
      Capital.tick(f,100);
      if(!Capital.buy(f,'warrior','captain:3')||Capital.branchEffects(h,h.classRanks).support!==10)return false;
      if(!Capital.demolish(f,p)||h.classRanks.attack!==1||h.classRanks['captain:2']!==1||Capital.recruitLevel(f,'warrior')!==1)return false;
      if(!Capital.enqueue(f,p,'plaza'))return false;
      Capital.tick(f,100);
      return Capital.buy(f,'warrior','attack')&&h.classRanks.attack===1;
    }''')
    print('PASS class floors, talent rows, permanent subclass and non-stacking retained ranks')

    assert page.evaluate('''() => {
      const f=player(), t=f.town;
      t.buildings[t.plots[3]]='smithy';
      const before=f.bag.length;
      const key=Object.keys(Development.recipes).find(k=>Development.recipes[k].kind==='weapon'&&Development.recipes[k].building==='smithy');
      if(!Development.startCraft(key)||f.bag.length!==before+1||t.craft)return false;
      const item=f.bag.at(-1);
      if(!Development.modifyGear(f,item.id,false)||item.level!==2)return false;
      const gold=f.gold,refund=Math.floor(item.materials.gold/2);
      return Development.modifyGear(f,item.id,true)&&f.gold===gold+refund;
    }''')
    print('PASS instant smithing, gear level limits and material refund')

    assert page.evaluate('''() => {
      const r=Game.battleRules;
      return r.damage([{type:'physical',value:20},{type:'fire',value:15}],{physicalArmor:30,resists:{fire:20}})===26
        &&r.damage([{type:'astral',value:20}],{resists:{astral:100}},true)===3
        &&r.damage([{type:'physical',value:100,penetration:50}],{physicalArmor:50})===75
        &&r.damage([{type:'physical',value:21}],{physicalArmor:50},false,true)===5;
    }''')

    page.evaluate('''() => {
      Game.newGame(124);
      const a=player().armies[0], foe=S.factions[1].armies[0];
      Game.startBattle(a,foe,{kind:'duel',pos:a.pos,title:'Проверка блока'});
      const b=S.battle;
      b.field.cells.fill('ground');
      const [warrior,,enemy]=b.units;
      Object.assign(warrior,{pos:18,hp:100,physicalArmor:30,resists:{fire:0},ap:3});
      Object.assign(enemy,{pos:19,damage:20,atk:8,ap:3});
      Game.clickBattle(18);
    }''')
    page.click('[data-a=bGuard]')
    assert page.locator('[data-a=bGuard]').is_disabled()
    assert page.evaluate('''() => {
      const b=S.battle, [warrior,,enemy]=b.units, random=Math.random;
      if(warrior.ap!==2||!warrior.guardBlock)return false;
      b.side=1;
      Math.random=()=>.9;
      try {
        if(!Game.attackBattle(enemy,warrior,false,false,'fire')||warrior.hp!==80||!warrior.guardBlock)return false;
        if(!Game.attackBattle(enemy,warrior)||warrior.hp!==74||warrior.guardBlock)return false;
        if(!Game.attackBattle(enemy,warrior)||warrior.hp!==62||enemy.ap!==0)return false;
        warrior.damage=20;
        warrior.talents.counter=true;
        Object.assign(enemy,{cls:'engineer',ap:2,hp:100,physicalArmor:0});
        Math.random=()=>.12;
        return Game.attackBattle(enemy,warrior)&&Game.attackBattle(enemy,warrior)
          &&enemy.hp===85&&warrior.hp===50&&warrior.counterRound===b.round;
      } finally {Math.random=random;}
    }''')
    print('PASS one-AP guard, magic bypass, passive block and one counterattack per round')

    assert page.evaluate('''() => {
      Game.newGame(125,[Game.createHero('rogue'),Game.createHero('archer')]);
      const a=player().armies[0], random=Math.random;
      Game.startBattle(a,null,{kind:'camp',family:'spiders',pos:a.pos,title:'Проверка уклонения'});
      const b=S.battle, [rogue,archer,spider]=b.units;
      b.field.cells.fill('ground');
      Object.assign(rogue,{pos:18,hp:30,physicalArmor:0});
      Object.assign(archer,{pos:26,hp:30});
      Object.assign(spider,{pos:19,ap:3,damage:10});
      b.side=1;
      if(BattleRules.baseDodge(rogue)!==.25||BattleRules.baseDodge(archer)!==.20)return false;
      try {
        Math.random=()=>.10;
        if(!Game.attackBattle(spider,rogue)||rogue.hp!==30||rogue.snaredUntil||spider.ap!==2)return false;
        let checks=0;
        Math.random=()=>{checks++;return .9;};
        if(!Game.attackBattle(spider,rogue)||rogue.hp!==20||rogue.snaredUntil!==b.round+1||checks!==2)return false;
        const legacy=clone(S);
        Object.assign(legacy.battle.units[2],{damage:5.5,die:8});
        if(!Game.load(legacy)||S.battle.units[2].damage!==10||'die' in S.battle.units[2])return false;
        return Game.load(clone(S))&&S.battle.units[2].damage===10;
      } finally {Math.random=random;}
    }''')
    print('PASS dodge cancels damage and on-hit effects, attacks have fixed base damage, and old saves migrate once')

    assert page.evaluate('''() => {
      Game.newGame(123);
      const f=player(), e=S.factions[1], a=f.armies[0], v=e.armies[0];
      f.gold=100;
      Game.startBattle(a,v,{kind:'duel',pos:a.pos,title:'Проверка'});
      const b=S.battle;
      b.side=0;
      b.field.cells.fill('ground');
      b.units.forEach((u,i)=>{u.hp=28;u.pos=[9,17,12,20][i];u.ap=3;});
      const u=b.units[0];
      if(!moveBattle(u,10)||u.ap!==2||!moveBattle(u,11)||u.ap!==1)return false;
      if(!attackBattle(u,b.units[2])||u.ap!==0||moveBattle(u,3))return false;
      b.units[1].pos=16;
      b.units[1].hp=15;
      if(!BattleRules.flee(b.units[1]))return false;
      b.units[2].hp=0;b.units[3].hp=0;b.over=0;
      const first=v.heroes[0],second=v.heroes[1];
      first.items=[{id:'kept',name:'Меч',kind:'weapon'}];
      second.items=[{id:'loot',name:'Броня',kind:'armor'}];
      const gold=f.gold;
      Game.finishBattle();
      return S.aftermath.eligible.length===2&&first.xp===8&&a.heroes[0].xp===14
        &&f.gold===gold&&f.retreats[0].hero.hp===7;
    }''')
    page.click('[data-a=aftermathFate][data-v=hire] >> nth=0')
    page.click('[data-a=aftermathFate]:not([data-v])')
    assert page.evaluate('''() => {
      const m=S.aftermath, f=player(), hero=f.armies[0].heroes.find(h=>h.items.some(i=>i.id==='kept'));
      return hero?.hp===1&&m.loot[0].id==='loot'&&f.gold===80;
    }''')
    page.click('[data-a=aftermathDone]')
    assert page.evaluate('''() => {
      const f=player(), r=f.retreats[0];
      if(!f.bag.some(i=>i.id==='loot'))return false;
      S.turn=r.turn-1;BattleRules.returns(f);
      if(f.retreats.length!==1)return false;
      S.turn++;BattleRules.returns(f);
      return f.retreats.length===0&&f.armies.some(a=>a.pos===f.city&&a.heroes.includes(r.hero))&&r.hero.hp===7;
    }''')
    print('PASS tactical AP, mixed damage, individual retreat, recruit, execute and automatic loot delivery')

    assert page.evaluate('''() => {
      Game.newGame(42);
      const f=player();
      f.gold=0;
      f.town.buildings={0:'tower',1:'magicacademy',2:'hospital',3:'workshop',4:'shrine'};
      const e=Capital.economy(f);
      return e.paid===12&&e.due===16&&e.efficiency===0.75&&e.prod===6;
    }''')
    print('PASS deficit, partially paid buildings and half-up production')

    page.evaluate('''() => {
      Game.newGame(700);
      Game.fx.configure({enabled:false});
      const f=player();
      Capital.enqueue(f,f.town.plots[0],'market');
      Game.save();
    }''')
    page.reload()
    page.click('[data-a=continue]')
    assert page.evaluate('player().town.projects[0].id') == 'market'
    page.click('#endTurn')
    while page.locator('[data-a=turnDefer]').count():
        page.locator('[data-a=turnDefer]').first.click()
    page.locator('#modal [data-a=end]').click()
    page.wait_for_function('Game.state.turn === 2 || Game.state.battle !== null')
    assert page.evaluate("Game.state.turn===2 && player().town.projects[0].progress===4")
    page.click('[data-a=turnReportDone]')
    print('PASS real global turn, construction progress and turn report')

    assert page.evaluate('''() => {
      const f=player(), a=f.armies[0], enemy=S.factions[1].armies[0];
      Game.startBattle(a,enemy,{kind:'duel',pos:a.pos,title:'Проверка отсчёта'});
      const b=S.battle, u=b.units.find(v=>v.hero===a.heroes[0].id), mage=b.units.find(v=>v.cls==='acolyte'&&v.side===0);
      b.field.cells.fill('ground');b.over=null;b.side=1;u.hp=0;u.pos=9;mage.pos=10;mage.mana=12;
      switchSide();
      if(u.deathTurns!==1||!spellBattle(mage,u,'heal')||u.hp<=0||u.deathTurns!==0)return false;
      u.hp=0;b.side=1;
      for(let i=0;i<3;i++){b.side=1;switchSide();}
      if(!u.expired||spellBattle(mage,u,'heal'))return false;
      b.over=0;
      Game.finishBattle();
      return !a.heroes.some(h=>h.id===u.hero)&&S.remains.some(r=>r.hero.id===u.hero);
    }''')
    print('PASS personal death counter, revival in combat and permanent death')
    assert not errors, errors
    print('PASS save/reload and no uncaught browser errors')
