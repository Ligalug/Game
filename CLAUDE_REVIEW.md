# «Туман и кости» — прототип кампании для ревью Claude

Проверь соответствие реализации принятым решениям, переходы состояния и случаи, которые могут сломать партию. В бою обрати внимание на порядок уклонения, брони, блока и критического множителя, сохранение подготовленного блока при магическом ударе и ограничения контратаки. В кампании проверь предоплату и возврат очереди, сохранение выданных рангов при сносе, ход поднятого героя и выдачу добычи при повторном действии.

## Бой без кубиков · 19 ноября 2026

В кампании и пробном бою у оружия и способностей фиксированный базовый урон. Значения взяты из середины прежних диапазонов. Отдельная проверка общего попадания убрана. Уклонение отменяет удар и побочные эффекты, расход ОД и перезарядка учитываются при применении атаки. Новый раздел добавлен в локальный диздок. [Правила боя](docs/DESIGN_GLOBAL_MAP.md)

- Пробные базовые шансы уклонения — 20% у Лучника и 25% у Плута. В кампании на уклонение также влияют укрытие, высота, окружение, точность и бонусы подкласса. Боевой полигон использует свой рейтинг укрытий.
- Блок у Воина срабатывает с шансом 15% и уменьшает физический урон вдвое после брони. Стойка за 1 ОД готовит один гарантированный блок следующего физического попадания. Уклонение и магия оставляют подготовленный блок доступным. Талант кампании даёт контратаку в ближнем бою до одного раза за раунд.
- Критический удар имеет базовый шанс 10% и множитель ×1,5 до защиты. Ходы начинают нападающие. При предельном стрессе шанс воодушевления определяется по решимости героя.
- При загрузке боя старый вклад кубика преобразуется в фиксированный базовый урон один раз. Боевые анимации показывают сам удар, блок или уклонение. Анимация броска с карты пропускается, если по результату события уже открыто поле боя.

## Исходная версия

- При исходной сверке `git ls-remote origin refs/heads/main` и локальная ветка `work` указывали на `d257e0e8aac4a45989a7aa180de561ac1cca7cfe`. В этой ревизии последние решения уточняют общую добычу, опыт участников, переманивание и размещение героев. [Базовый диздок](https://github.com/Ligalug/Game/blob/d257e0e8aac4a45989a7aa180de561ac1cca7cfe/docs/DESIGN_GLOBAL_MAP.md)
- Локальную сборку 0.9.2 искали по именам файлов, оглавлениям ZIP и доступной истории Git. Для `b050ac6` GitHub API вернул 422 `No commit found for SHA: b050ac6`. Основой стала 0.8.8 из локального репозитория. [Архивная сборка](archive/tuman-i-kosti-088.html)

## Запуск

Откройте `index.html` и выберите двух героев для кампании. Для быстрого теста атаки откройте «Пробный бой» или отдельный `battle-lab.html`. Оба файла автономны. Если браузер блокирует локальные HTML-файлы, их можно открыть через локальный HTTP-сервер. Его автоматически запускают браузерные тесты.

| Механика | Реализация |
| --- | --- |
| Столица | Пятиуровневая ратуша, расширение от населения, уникальность построек, отражение, снос, предоплата и резерв участков, пауза, приоритет, линейный возврат и перенос ОП. Стены используют общую очередь. |
| Экономика | Доход до содержания, пропорциональное снижение выпуска платных зданий, округление половины вверх и разбивка потерь. |
| Классы | Воин, Плут, Лучник, Послушник и Инженер. Ранги найма, атаки и защиты, два узла второго этажа и один узел третьего для каждого подкласса. Герой хранит свой максимум выданных рангов. |
| Таланты | По одному выбору в каждой базовой строке 2–5, постоянный подкласс и последовательные узлы 6–8. Платный сброс в столице позволяет заново распределить очки. |
| Кузня и башня | Мгновенное изготовление оружия и брони, постоянный рецепт из руин, предел уровня предмета, разборка и зачарования. Улучшенная башня открывает вторую ячейку зачарования. |
| Тактика | 3 ОД, атака за 1 ОД, отдельные перемещения до 3 шагов до первой атаки, линия огня, укрытие, высота и окружение. Защита и автоматические исходы атаки описаны выше. |
| Судьба героев | Три личных очереди до смерти, лечение с 0 HP, отход с края и возвращение через три хода. После победы доступны казнь или наём противника с 0 HP, общая добыча и городской склад. |
| Кампания | Четыре вассала, глобальная карта, деревни, указы, отношения, стресс, осады, перевозка останков и воскрешение. Досрочная победа по репутации требует пяти полных ходов лидерства. |

## Границы прототипа

Цены, порог репутации 60, предел 60 раундов, условия этажей и численные эффекты талантов используются для прогона. В кампании ходят стороны. Личная очередь недееспособного героя наступает в ход его стороны. Смешанный урон покрыт проверкой формулы.

Подземелья, изометрическая планировка с дорогами, режимы длительности партии и полный каталог талантов, рецептов и заклинаний требуют отдельной реализации. Баланс кампании от старта до победы пока не проверен.

## Проверки

Chromium и Playwright проверяют игровой интерфейс, сохранения, анимации и сценарии полигона. Сборка и проверка синтаксиса JavaScript прошли.

```sh
python tools/build.py
python tests/test_current_prototype.py
python tests/test_animations.py
python tests/test_battle_lab.py
git diff --check
```


Ключевые проверки актуального боя прошли.

### `test_current_prototype.py`

```text
PASS offline campaign, five classes and initial party
PASS prepayment, priority, pausing, linear refund, uniqueness and excess production
PASS class floors, talent rows, permanent subclass and non-stacking retained ranks
PASS instant smithing, gear level limits and material refund
PASS one-AP guard, magic bypass, passive block and one counterattack per round
PASS dodge cancels damage and on-hit effects, attacks have fixed base damage, and old saves migrate once
PASS tactical AP, mixed damage, individual retreat, recruit, execute and automatic loot delivery
PASS deficit, partially paid buildings and half-up production
PASS real global turn, construction progress and turn report
PASS personal death counter, revival in combat and permanent death
PASS save/reload and no uncaught browser errors
```

### `test_animations.py`

```text
PASS: Map motion interpolates; new terrain waits its turn; skip keeps final gameplay state
PASS: Animated die lands on the actual value with modifier and difficulty; keyboard skip works
PASS: Battle starts without initiative dice and a real attack plays only the impact
PASS: Healing displays pre-impact HP, then resolves to the saved healed value
PASS: An ambush starts from map movement and the dice animation stays out of the battle window
PASS: Construction has persistent scaffolding and distinct start and completion effects
PASS: Arriving wagon remains visible through its travel animation, then unloads
PASS: Tactical motion locks duplicate commands; detailed autobattle plays recorded actions
PASS: Enabled and disabled animations consume identical randomness and produce identical game state
PASS: Default autobattle stays brief instead of replaying every action
PASS: Disabling immediately unlocks controls; speed and preferences persist after reload
PASS: Reduced-motion preference respected; no browser errors during animated gameplay
12 animation scenarios passed.
```

### `test_battle_lab.py`

```text
PASS: Expanded 16x10 map keeps four heroes per side, including engineers
PASS: Three cells cost one AP across separate clicks; exceeding the remaining movement budget is rejected
PASS: Mud and slowing spend extra steps; rocks remain impassable
PASS: Three defenses mitigate their own damage type with diminishing percentage gains
PASS: Real hits match fixed forecasts, and defense prepares a single block on top of the armor
PASS: Dodge avoids all damage and the attack debuff while the attacker spends the AP
PASS: Ranged attacks, specials and healing highlight radius; blocked line of sight is distinguished
PASS: Revived hero has one AP, buying at most three steps and no extra attack
PASS: End turn blocks outstanding heroes; individual and explicit group passes allow progress
PASS: Special costs and cooldowns remain valid; physical-defense debuff expires after target turn
PASS: Armorer activates personal power armor, raises all defenses and damage, and cannot stack it
PASS: Demolitionist lays a mine; an enemy walking onto it takes real typed damage and consumes the trap
PASS: Fortifier builds an improved ranged cover and bridge; bridge remains available during fortification cooldown
PASS: Restart cancels pending animated AI actions
PASS: Battle ends when a squad falls; winners revive allies at one HP
PASS: Standalone backup boots offline; exported report identifies updated version
PASS: Integrated experiment leaves campaign state unchanged
PASS: All scenarios reach a result with each engineer subclass; no AI or turn-lock deadlocks
PASS: Desktop and mobile preserve readable controls and contained map scrolling without browser errors
19 battle lab scenarios passed.
```

Также прошли `test_ai_positions`, `test_battle_editor`, `test_convoy`, `test_pixel_art`, `test_progression`, `test_relations_and_bestiary`, `test_rendering` и `test_subclass_skills`. Итого 11 из 14 наборов.

Три прежних набора остановились на ожиданиях старой версии. `test_development.py:21` ожидает четыре класса. `test_game.py:28` ожидает восемь стартовых кандидатов. `test_turns_and_tactics.py:26` ожидает одиночный объект `town.queue`. Последующие утверждения этих наборов в этом прогоне не выполнялись.

## Исходники

Ниже полный текст затронутых исходников, шаблона, сборщика и обновлённых проверок. Остальные компоненты и бинарные ассеты доступны в базовой ревизии. `index.html` и `battle-lab.html` генерируются сборщиком.

### `src/strike.js`

```js
// Shared automatic defenses for the campaign and the battle lab.
const Strike = (() => {
  const heroDodge = {archer:.20, rogue:.25};
  const criticalMultiplier = 1.5;

  function chance(probability, random = Math.random) {
    return probability >= 1 || probability > 0 && random() < probability;
  }

  function blockChance(cls, physical, prepared) {
    return cls === 'warrior' && physical ? (prepared ? 1 : .15) : 0;
  }

  function resolve({dodge, block, critical}, random = Math.random) {
    if (chance(dodge, random)) return {dodged:true, blocked:false, critical:false};
    return {dodged:false, blocked:chance(block, random), critical:chance(critical, random)};
  }

  function roundDamage(value, blocked = false) {
    return Math.max(1, Math.round(value * (blocked ? .5 : 1)));
  }

  return {heroDodge, criticalMultiplier, chance, blockChance, resolve, roundDamage};
})();

```

### `src/battle_rules.js`

```js
// Combat rules from the November 11–12 decisions.
const BattleRules = (() => {
  const schools=['fire','water','air','earth','light','dark','astral'];

  function damage(components,target,critical=false,blocked=false) {
    const total=components.reduce((sum,{type,value,penetration=0})=>{
      const rate=type==='physical'?target.physicalArmor:target.resists?.[type];
      const defense=clamp(rate||0,0,90)*(1-clamp(penetration,0,100)/100);
      return sum+value*(critical?Strike.criticalMultiplier:1)*(1-defense/100);
    },0);
    return Strike.roundDamage(total,blocked);
  }

  function baseDodge(u) {
    const innate = Strike.heroDodge[u.cls] ?? Bestiary.species[u.monster]?.dodge ?? 0;
    return clamp(innate+(u.branch?.evasion||0)/100,0,.75);
  }

  function dodgeChance(u,t,ranged) {
    const b=S.battle;
    const baseAttack=C[u.cls]?.atk ?? Bestiary.species[u.monster]?.atk ?? 8;
    const accuracy=(u.atk-baseAttack+Bestiary.attackBonus(u,t)-(u.curseUntil>=b.round?3:0))*5+(u.branch?.accuracy||0);
    const flanked=!ranged&&dist(u.pos,t.pos,8)===1&&activeUnits(b,u.side).some(
      v=>v!==u&&dist(v.pos,t.pos,8)===1&&dist(v.pos,u.pos,8)>1);
    const position=ranged?5*Tactics.cover(u,t)-10*Tactics.elevation(u,t):flanked?-15:0;
    return clamp(baseDodge(t)+(position-accuracy)/100,0,.75);
  }

  function normalizeSave(b) {
    for(const u of b?.units||[]) {
      if(!Number.isFinite(u.die)) continue;
      u.damage+=(u.die+1)/2;
      delete u.die;
    }
  }

  function attack(u,t,special=false,free=false,magic=false) {
    const b=S.battle;
    if(!b||b.over!==null||!u||!t||u.surrender||t.surrender||u.retreated||t.retreated||u.hp<=0||t.hp<=0||u.side===t.side||!free&&(u.ap<1||u.side!==b.side)||!Tactics.canAttack(u,t)) return false;
    if(u.cls==='acolyte'&&!magic&&!free) return spellBattle(u,t,Development.defaultAttackSpell(u));
    if(special&&u.cls==='warrior'&&(!u.talents?.power||u.powerRound===b.round)) return false;
    if(special&&u.cls!=='warrior'&&u.used) return false;
    const school=schools.includes(magic)?magic:'astral';
    const ranged=u.range>1, type=magic?'magic':ranged?'arrow':'slash';
    const {dodged,blocked,critical}=Strike.resolve({
      dodge:dodgeChance(u,t,ranged),
      block:Strike.blockChance(t.cls,!magic,t.guardBlock),
      critical:.10,
    });
    if(!free) u.ap--;
    u.attackedRound=b.round;
    if(special) {
      if(u.cls==='warrior')u.powerRound=b.round;
      else u.used=true;
    }
    if(dodged) {
      FX.impact(u,t,0,type,{defense:'dodge'});
      b.log.unshift(`${u.name} → ${t.name}: уклонение.`);
      return true;
    }
    u.didHit=true;
    const raw=Math.max(1,u.damage+Relations.rivalBonus(u)+Bestiary.damageBonus(u)+(special&&u.cls!=='warrior'?5:0));
    const protection=activeUnits(b,t.side).filter(v=>v!==t&&dist(v.pos,t.pos,8)===1).reduce((n,v)=>n+(v.talents?.support||0)+(v.sub==='captain'?3:v.sub==='fortifier'?4:0),0);
    const target={...t,physicalArmor:(t.physicalArmor??Math.max(0,(t.slash||10)-10)*3)+protection+(t.guard?10:0)+(t.friendCover&&activeUnits(b,t.side).some(u=>u.id===t.friendCover&&dist(u.pos,t.pos,8)===1)?5:0)+(t.wardUntil>=b.round?10:0)+(t.greaterWard>=b.round?15:0)};
    const dealt=damage([{type:magic?school:'physical',penetration:magic?(u.branch?.magicPen||0):(u.branch?.penetration||0),value:raw*(special&&u.cls==='warrior'?1.5:1)*(free?.75:1)}],target,critical,blocked);
    if(blocked) t.guardBlock=false;
    const before=t.hp, effect=FX.impact(u,t,dealt,type,{critical,defense:blocked?'block':null});
    damageUnit(t,dealt,critical,u);
    if(effect){effect.hpAfter=t.hp;effect.amount=before-t.hp;}
    b.log.unshift(`${u.name} → ${t.name}: ${before-t.hp} урона${critical?' · крит':''}${blocked?' · блок':''}.`);
    Bestiary.onHit(u,t);
    if(!free&&blocked&&t.hp>0&&t.talents?.counter&&t.counterRound!==b.round&&dist(t.pos,u.pos,8)===1) {
      t.counterRound=b.round;
      const attacked=t.attackedRound;
      attack(t,u,false,true);
      t.attackedRound=attacked;
    }
    return true;
  }

  const makeLegacyUnit=makeUnit;
  makeUnit=function(h,a,side,i){
    const u=makeLegacyUnit(h,a,side,i), ranks=Capital.bonuses(owner(a),h), talents=Talents.effects(h), branch=Capital.branchEffects(h,ranks);
    u.talents={...talents,support:talents.support+(branch.support||0)};
    u.branch=branch;
    u.range+=branch.range||0;
    u.mana+=branch.mana||0;
    u.maxMana+=branch.mana||0;
    u.damage+=(h.sub==='demolitionist'?3:0)+(ranks.attack||0)+talents.attack+(branch.damage||0);
    u.physicalArmor=clamp((u.slash-10)*3+(cityEffects(owner(a)).armyArmor||0)+(h.sub==='armorer'?8:0)+4*(ranks.defense||0)+talents.defense+(branch.armor||0),0,90);
    u.resists=Object.fromEntries(schools.map(k=>[k,Math.max(0,(u.ac-10)*2)]));
    return u;
  };

  function arrival(f,h,position) {
    let a=f.armies.find(a=>a.pos===position&&a.heroes.length<4&&!a.escort);
    if(!a) a=createArmy(f,position);
    a.heroes.push(h);
    Capital.bonuses(f,h);
    return a;
  }

  function flee(u) {
    const b=S.battle;
    if(!b||!u?.hero||u.hp<=0||u.surrender||u.retreated||u.side!==b.side||b.meta.kind==='dungeon') return false;
    if(u.pos>=8&&u.pos<40&&u.pos%8!==0&&u.pos%8!==7) return false;
    u.retreated=true;
    u.ap=0;
    checkBattle();
    return true;
  }

  function returns(f) {
    const list=f.retreats??=[];
    for(const r of [...list]) if(r.turn<=S.turn) {
      arrival(f,r.hero,f.city);
      list.splice(list.indexOf(r),1);
      log(r.hero.name+' возвращается в столицу после отступления.');
    }
  }

  function price(h) { return Math.ceil((h.recruitCost??40)/2); }
  function fate(m,h,recruit) {
    const i=m.eligible.indexOf(h);
    if(i<0) return false;
    const f=S.factions[m.winner];
    if(recruit) {
      if(!pay(f,price(h))) return false;
      const a=findArmy(m.army);
      const neighbor=nb(m.pos).filter(p=>!allArmies().some(a=>a.pos===p)&&!S.factions.some(g=>!g.dead&&g.city===p)&&!['river','mountain'].includes(cell(p).terrain)).sort((a,b)=>dist(a,f.city)-dist(b,f.city)||a-b)[0];
      h.hp=1;
      h.dead=false;
      if(a&&a.heroes.length<4&&!a.escort) {
        a.heroes.push(h);
        Capital.bonuses(f,h);
      } else arrival(f,h,neighbor??f.city);
      log(h.name+' нанят за '+price(h)+' золота.');
    } else bury(m,h);
    m.eligible.splice(i,1);
    return true;
  }

  function bury(m,h) {
    m.loot.push(...h.items);
    h.items=[];
    h.dead=true;
    const r={id:id('body'),pos:m.pos,hero:h,holder:m.winner??null};
    S.remains.push(r);
    m.corpses.push(r.id);
  }

  function stash(m) {
    const f=S.factions[m.winner];
    if(f) f.bag.push(...m.loot.splice(0));
  }

  return {schools,damage,attack,baseDodge,normalizeSave,flee,returns,price,fate,bury,stash};
})();
Game.battleRules=BattleRules;

```

### `src/animations.js`

```js
// Transient presentation timeline. Never changes game state or consumes game RNG.
const FX=(()=>{
 const $=id=>document.getElementById(id);
 const KEY='tik-motion-v1',reduced=window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
 let settings={enabled:!reduced,speed:1,autoDetail:false};
 try{Object.assign(settings,JSON.parse(localStorage.getItem(KEY)||'{}'));}catch{}
 settings.speed=[1,2,4].includes(settings.speed)?settings.speed:1;
 const queue=[],positions=new Map(),reveals=new Map(),health=new Map(),history=[];
 let current=null,raf=0,muted=0,autoDepth=0,autoCount=0,lastDraw=0,waiters=[],session=0;
 const now=()=>performance.now(),ease=t=>t*t*(3-2*t),key=(mode,id)=>mode+':'+id;
 function keep(){try{localStorage.setItem(KEY,JSON.stringify(settings));}catch{}}
 function usable(mode='map'){return settings.enabled&&!muted&&(mode!=='battle'||S?.battle?.human!==null);}
 function start(){if(!raf)raf=requestAnimationFrame(frame);document.body.classList.add('fxbusy');const el=$('fxProgress');if(el)el.hidden=false;}
 function add(e){if(!usable(e.mode))return null;if(autoDepth&&!settings.autoDetail)return null;if(autoDepth&&autoCount++>=120)return null;
   e.duration=(e.duration||450)/(autoDepth?2.3:1);e.session=session;e.auto=!!autoDepth;queue.push(e);start();return e;
 }
 function release(){positions.clear();reveals.clear();health.clear();$('dicePanel').hidden=true;$('fxProgress').hidden=true;document.body.classList.remove('fxbusy');const callbacks=waiters;waiters=[];for(const fn of callbacks)queueMicrotask(fn);}
 function record(e){history.push({type:e.type,kind:e.kind,label:e.label,value:e.value,sides:e.sides,mode:e.mode,from:e.from,to:e.to});if(history.length>160)history.shift();}
 function complete(e){if(e.type==='move'){positions.set(key(e.mode,e.id),{pos:e.to});if(!queue.some(t=>t.type==='move'&&t.id===e.id&&t.mode===e.mode))positions.delete(key(e.mode,e.id));}if(e.type==='reveal')for(const p of e.cells)reveals.delete(p);if(e.target&&e.hpAfter!=null){health.set(key(e.battleId,e.target),e.hpAfter);if(!queue.some(t=>t.target===e.target&&t.battleId===e.battleId))health.delete(key(e.battleId,e.target));}}
 function paint(){if(typeof Painter==='undefined')return;if(current?.mode==='battle')Painter.battle();else Painter.draw();paintCity();}
 function frame(time){
   raf=0;
   if(!settings.enabled){finish();return;}
   // A map check can open combat before its result animation reaches the front of the queue.
   if(UI.modal==='battle'){
     if(current?.type==='dice'){current=null;$('dicePanel').hidden=true;}
     while(queue[0]?.type==='dice')queue.shift();
   }
   if(!current&&queue.length){current=queue.shift();current.start=time;record(current);}
   if(!current){release();paint();return;}
   current.p=Math.min(1,(time-current.start)/(current.duration/settings.speed));
   if(current.type==='dice')paintDie(current);
   const text=$('fxLabel');if(text)text.textContent=current.label||({move:'Перемещение',reveal:'Открываем местность',effect:'Действие',city:'Городское строительство'}[current.type]||'Анимация');
   if(time-lastDraw>=24||current.p>=1){paint();lastDraw=time;}
   if(current.p>=1){complete(current);if(current.type==='dice')$('dicePanel').hidden=true;current=null;}
   if(current||queue.length)raf=requestAnimationFrame(frame);else{release();paint();}
 }
 function finish(){if(raf)cancelAnimationFrame(raf);raf=0;queue.length=0;current=null;release();if(typeof Painter!=='undefined'){Painter.draw();if(S?.battle)Painter.battle();paintCity();}}
 function reset(){session++;muted=0;finish();history.length=0;}
 function roll(value,sides,options={}){return add({type:'dice',value,sides,...options,mode:'map',duration:options.duration||1050});}
 function move(mode,id,from,to,options={}){if(from===to||!usable(mode))return null;if(mode==='map'&&options.owner!==0&&(!visible(player(),from)||!visible(player(),to)))return null;
   const e=add({type:'move',mode,id,from,to,...options,duration:options.duration||620});if(e&&!positions.has(key(mode,id)))positions.set(key(mode,id),{pos:from,ghost:options.ghost});return e;
 }
 function reveal(cells){if(!cells.length||!usable('map'))return;const e=add({type:'reveal',mode:'map',cells:[...cells],label:'Туман отступает',duration:600});if(e)for(const p of cells)reveals.set(p,e);}
 function effect(kind,from,to,options={}){const mode=options.mode||'battle',b=mode==='battle'?S?.battle:null;const e=add({type:'effect',kind,mode,from,to,battleId:b?.id,...options,duration:options.duration||650});if(e&&e.target&&e.hpBefore!=null&&!health.has(key(e.battleId,e.target)))health.set(key(e.battleId,e.target),e.hpBefore);return e;}
 function impact(u,t,amount,type,{critical=false,defense=null}={}){
   const label=defense==='dodge'?'Уклонение':defense==='block'?'Блок':critical?'Критическое попадание':type==='magic'?'Магический болт':'Атака';
   return effect(type,u.pos,t.pos,{actor:u.id,target:t.id,hpBefore:t.hp,hpAfter:t.hp,amount,critical,defense,label});
 }
 function city(plot,kind,label){return add({type:'city',mode:'map',plot,kind,label,duration:850});}
 function position(mode,id,pos,coord){const hold=positions.get(key(mode,id)),e=current?.type==='move'&&current.id===id&&current.mode===mode?current:null;if(e){const a=coord(e.from),b=coord(e.to),t=ease(e.p||0);return{x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t,moving:true,walk:Math.sin((e.p||0)*Math.PI*4)*1.7,flip:b.x<a.x};}return{...coord(hold?.pos??pos),moving:false,walk:0};}
 function revealAlpha(p){const e=reveals.get(p);if(!e)return 1;return current===e?ease(e.p||0):0;}
 function hp(u){return health.get(key(S?.battle?.id,u.id))??u.hp;}
 function ghosts(){const out=[];for(const [k,v]of positions)if(k.startsWith('map:')&&v.ghost){const id=k.slice(4);if(!S?.convoys.some(c=>c.id===id))out.push({...v.ghost,id,pos:v.pos});}return out;}
 function auto(fn){autoDepth++;autoCount=0;try{return fn();}finally{autoDepth--;if(settings.enabled&&S?.battle&&S.battle.human!==null&&!settings.autoDetail){const e={type:'effect',kind:'summary',mode:'battle',from:0,to:0,label:'Автобой завершён',text:'Результат готов. Подробности — в журнале боя.',duration:700};queue.push(e);start();}}}
 function whenIdle(fn){if(current||queue.length)waiters.push(fn);else queueMicrotask(fn);}
 function paintDie(e){const panel=$('dicePanel');panel.hidden=false;const p=e.p||0,rolling=p<.7,n=rolling?1+Math.floor(p*145)%e.sides:e.value,die=$('fxDie');die.style.transform=rolling?`translateY(${Math.sin(p*45)*8}px) rotate(${Math.sin(p*24)*27}deg) scale(${1+Math.sin(p*32)*.06})`:'none';$('diceValue').textContent=n;$('diceSides').textContent='d'+e.sides;$('diceTitle').textContent=e.label||'Бросок';
   const mod=e.modifier==null?'':` ${e.modifier>=0?'+':'−'} ${Math.abs(e.modifier)}`;
   $('diceFormula').textContent=rolling?'Бросок…':`${e.alternatives?'['+e.alternatives.join(', ')+'] → ':''}${e.value}${mod}${e.modifier!=null?' = '+(e.value+e.modifier):''}${e.dc!=null?' · КС '+e.dc:''}${e.opposed!=null?' · соперник '+e.opposed:''}`;
   $('diceOutcome').textContent=rolling?'':e.outcome||(e.success===true?'Успех':e.success===false?'Провал':'');
   panel.dataset.result=rolling?'rolling':e.value===e.sides&&e.sides===20?'critical':e.value===1&&e.sides===20?'failure':e.success===false?'failure':'success';
 }
 function overlay(ctx,mode,coord){const e=current;if(!e||e.mode!==mode)return;if(e.type==='city'&&mode==='map'){const p=coord(e.plot),t=e.p||0;ctx.save();ctx.strokeStyle='#f0d58b';ctx.globalAlpha=1-t;ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(p.x,p.y,28+t*32,14+t*12,0,0,Math.PI*2);ctx.stroke();ctx.fillStyle='#fae6a8';ctx.font='bold 13px Georgia';ctx.textAlign='center';ctx.fillText(e.label,p.x,p.y-24-t*20);ctx.restore();return;}if(e.type!=='effect'||e.kind==='summary')return;const p=e.p||0,from=coord(e.from),to=coord(e.to),x=to.x,y=to.y,alpha=1-p;ctx.save();ctx.lineWidth=2;ctx.textAlign='center';ctx.font='bold 14px Georgia';
   if(['arrow','magic','slash'].includes(e.kind)){
     const t=Math.min(1,p/.55),px=from.x+(to.x-from.x)*t,py=from.y+(to.y-from.y)*t-25;
     if(e.kind==='arrow'||e.kind==='magic'){
       ctx.strokeStyle=e.kind==='magic'?'#94d7ed':'#e9dbaf';ctx.fillStyle=e.kind==='magic'?'#bdebf9':'#e8dcae';ctx.beginPath();ctx.moveTo(px-(to.x-from.x)*.14,py-(to.y-from.y)*.14);ctx.lineTo(px,py);ctx.stroke();ctx.fillRect(px-2,py-2,4,4);
     }else{const u=Math.sin(Math.min(1,p/.65)*Math.PI);ctx.translate(from.x+(to.x-from.x)*u*.16,from.y+(to.y-from.y)*u*.16);ctx.strokeStyle='#e8dcbb';ctx.beginPath();ctx.moveTo(5-14*u,-45);ctx.lineTo(18,-15+12*u);ctx.stroke();ctx.translate(-(from.x+(to.x-from.x)*u*.16),-(from.y+(to.y-from.y)*u*.16));}
     if(p>.45){
       ctx.globalAlpha=Math.max(0,1-(p-.45)/.55);
       ctx.fillStyle=e.defense?'#bdebf9':e.critical?'#ffe195':'#f3b293';
       const text=e.defense==='dodge'?'Уклонение':e.defense==='block'?`Блок · −${e.amount}`:`−${e.amount}`;
       ctx.fillText(text,x,y-48-(p-.45)*30);
       for(let k=0;k<8;k++){const a=k*Math.PI/4,r=6+(p-.45)*34;ctx.fillRect(x+Math.cos(a)*r,y-22+Math.sin(a)*r*.7,3,2);}
     }
   }else{
     const colors={heal:'#b7e7a2',ward:'#a8daf0',curse:'#c5a0e3',guard:'#e8d58f',revive:'#ffe9a3',meditate:'#a9c8ef',surrender:'#efdeba',inspired:'#f7db7b',protect:'#c8dcb4',arrival:'#e4d194'};ctx.strokeStyle=colors[e.kind]||'#e7d6a4';ctx.fillStyle=ctx.strokeStyle;ctx.globalAlpha=.95*(1-p*.6);
     if(e.kind==='heal'||e.kind==='revive'||e.kind==='inspired')for(let k=0;k<5;k++){const yy=y-8-p*45+(k%3)*7,xx=x+(k-2)*8;ctx.fillRect(xx-1,yy-4,2,8);ctx.fillRect(xx-4,yy-1,8,2);}
     ctx.beginPath();ctx.ellipse(x,y-23,17+p*21,26+p*8,0,0,Math.PI*2);ctx.stroke();
     const text=e.text||(e.kind==='heal'?`+${e.amount}`:e.kind==='ward'?'+3 КБ':e.kind==='curse'?'Проклятье':e.kind==='guard'?'Оборона':e.kind==='meditate'?'+4 маны':e.kind==='surrender'?'Сдаюсь':e.kind==='inspired'?'Воодушевление':'');if(text)ctx.fillText(text,x,y-50-p*18);
   }ctx.restore();
 }
 function paintCity(){for(const el of document.querySelectorAll('.fx-construction'))el.remove();const e=current;if(e?.type!=='city')return;const target=document.querySelector(`.plot[data-pos="${e.plot}"]`);if(!target)return;const p=target.querySelector('polygon'),bbox=p?.getBBox();if(!bbox)return;const ns='http://www.w3.org/2000/svg',g=document.createElementNS(ns,'g');g.classList.add('fx-construction');g.setAttribute('pointer-events','none');const ring=document.createElementNS(ns,'polygon');ring.setAttribute('points',p.getAttribute('points'));ring.setAttribute('fill',e.kind==='complete'?'#f5d886':'#8fae71');ring.setAttribute('fill-opacity',String((1-(e.p||0))*.55));ring.setAttribute('stroke','#f5d58b');ring.setAttribute('stroke-width','3');ring.setAttribute('stroke-dasharray','6 4');ring.setAttribute('stroke-dashoffset',String(-40*(e.p||0)));g.append(ring);const txt=document.createElementNS(ns,'text');txt.setAttribute('x',bbox.x+bbox.width/2);txt.setAttribute('y',bbox.y+13-(e.p||0)*5);txt.setAttribute('text-anchor','middle');txt.setAttribute('fill','#fff1b4');txt.setAttribute('font-size','8');txt.textContent=e.kind==='complete'?'Готово':e.kind==='grow'?'Новая территория':'Строительство';g.append(txt);target.parentElement.append(g);}
 function configure(changes){Object.assign(settings,changes);settings.speed=[1,2,4].includes(+settings.speed)?+settings.speed:1;keep();document.body.classList.toggle('fx-disabled',!settings.enabled);if(!settings.enabled)finish();drawSettings();}
 function drawSettings(){const el=$('fxSettings');if(!el||el.hidden)return;el.innerHTML=`<div class="fxSettingsBox"><h3>Анимации</h3><label><input id="fxEnabled" type="checkbox" ${settings.enabled?'checked':''}> Показывать анимации</label><p>Скорость: <select id="fxSpeed">${[1,2,4].map(v=>`<option value="${v}" ${settings.speed===v?'selected':''}>${v}×</option>`).join('')}</select></p><label><input id="fxAutoDetail" type="checkbox" ${settings.autoDetail?'checked':''}> Подробный автобой ускоренно</label><p class="muted">Пробел или «Пропустить» завершает показ. Результаты бросков и сохранённая партия не меняются. ${reduced?'Учтена системная настройка уменьшения движения.':''}</p><button id="fxCloseSettings">Готово</button></div>`;$('fxEnabled').onchange=e=>configure({enabled:e.target.checked});$('fxSpeed').onchange=e=>configure({speed:+e.target.value});$('fxAutoDetail').onchange=e=>configure({autoDetail:e.target.checked});$('fxCloseSettings').onclick=()=>el.hidden=true;}
 function openSettings(){$('fxSettings').hidden=false;drawSettings();}
 document.addEventListener('keydown',e=>{if((current||queue.length)&&(e.code==='Space'||e.key==='Escape')&&e.target.tagName!=='SELECT'&&e.target.tagName!=='INPUT'){e.preventDefault();e.stopImmediatePropagation();finish();}},true);
 document.addEventListener('visibilitychange',()=>{if(document.hidden)finish();});
 document.body.classList.toggle('fx-disabled',!settings.enabled);
 $('fxSkip').onclick=finish;
 return{roll,move,reveal,effect,impact,city,position,revealAlpha,hp,ghosts,overlay,paintCity,auto,whenIdle,finish,reset,configure,openSettings,mute(v){muted+=v?1:-1;muted=Math.max(0,muted);},get busy(){return !!current||queue.length>0;},get active(){return current?{...current}:null;},get queue(){return queue.map(e=>({...e}));},get history(){return history.slice();},get settings(){return{...settings};}};
})();

```

### `src/game.js`

```js
'use strict';
const N=16,MAX_PARTY=4,VERSION=4,SAVE='tik-restored-v04',LIMIT=60;
const $=id=>document.getElementById(id),esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])),rnd=n=>1+Math.floor(Math.random()*n),clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const C={warrior:{name:'Воин',icon:'⚔',hp:44,pierce:13,slash:19,ac:16,atk:8,damage:8.5,range:1,speed:2,mana:2,str:3,wis:0,cha:1,sprite:8},rogue:{name:'Плут',icon:'◆',hp:30,pierce:17,slash:12,ac:13,atk:9,damage:9.5,range:1,speed:4,mana:2,str:1,wis:1,cha:3,sprite:9},archer:{name:'Лучник',icon:'➶',hp:30,pierce:13,slash:13,ac:13,atk:8,damage:7.5,range:4,speed:3,mana:2,str:1,wis:3,cha:0,sprite:10},acolyte:{name:'Послушник',icon:'✦',hp:26,pierce:12,slash:12,ac:12,atk:7,damage:7.5,range:4,speed:2,mana:12,str:0,wis:3,cha:2,sprite:11}};
C.engineer={name:'Инженер',icon:'⚒',hp:28,pierce:20,slash:18,ac:16,atk:8,damage:6.5,range:5,speed:3,mana:2,str:2,wis:2,cha:1,sprite:13};
const TRAITS={brave:{name:'Храбрый',text:'+2 к решимости.'},kind:{name:'Сострадательный',text:'+3 к помощи и примирению.'},sociable:{name:'Общительный',text:'+2 к переговорам.'},greedy:{name:'Алчный',text:'Премия даёт больше верности.'},stubborn:{name:'Упрямый',text:'Сложность примирения +2.'},cautious:{name:'Осторожный',text:'+1 к защите.'}};
const COLORS=['#e9c77c','#dc9581','#a4b7df','#a6c58b'],HOUSES=['Дом Янтаря','Багряный Шип','Синий Сокол','Белый Ясень'],CITIES=['Янтарный двор','Терновая крепость','Соколиный утёс','Ясеневый оплот'];
const NAMES=['Альрик','Мира','Берен','Эльса','Торен','Рада','Кассий','Илона','Дарий','Веста','Ролан','Нэя','Северин','Лисса','Гарт','Эйра','Лиора','Оскар','Яромир','Селена'];
const TERRAIN={plain:{name:'Равнина',cost:1,color:'#67744a'},forest:{name:'Лес',cost:2,color:'#465f3d'},hill:{name:'Холмы',cost:2,color:'#7e7952'},river:{name:'Река',cost:2,color:'#537b7b'},swamp:{name:'Болото',cost:3,color:'#535f40'},mountain:{name:'Горы',cost:3,color:'#737469'}};
// Each replacement names its actual predecessor and inherits that predecessor's effects.
const BUILD={housing:{name:'Жилой квартал',cost:25,work:12,icon:'⌂',effects:{food:1,gold:1},text:'Поддерживает рост города.'},farm:{name:'Амбар',cost:30,work:14,icon:'♧',effects:{food:3},text:'Ускоряет прирост населения.'},workshop:{name:'Мастерская',cost:35,work:16,icon:'⚒',effects:{prod:3},text:'Ускоряет строительство.'},market:{name:'Рынок',cost:35,work:16,icon:'⚖',effects:{gold:4},text:'Приносит золото.'},shrine:{name:'Святилище',cost:35,crystal:2,work:16,icon:'✧',effects:{crystal:1},text:'Источник мана-кристаллов.'},tavern:{name:'Таверна',cost:30,work:14,icon:'☷',effects:{gold:1},text:'Больше кандидатов для найма.'},prison:{name:'Тюрьма',cost:45,work:20,icon:'▥',effects:{},text:'Открывает плен. Число мест не ограничено.'},hospital:{name:'Лечебница',cost:40,work:18,icon:'✚',effects:{heal:3},text:'Ускоряет лечение и сокращает слабость.'},siegeworks:{name:'Осадный двор',cost:50,work:22,icon:'⚑',effects:{siege:1},text:'Повышает силу осады.'},trading:{name:'Торговое подворье',from:'market',cost:45,work:20,icon:'⚖',effects:{gold:2,trade:1},text:'Сохраняет Рынок; улучшает доход торговли.'},forge:{name:'Кузница',from:'workshop',cost:45,work:20,icon:'⚒',effects:{attack:1},text:'Сохраняет производство Мастерской; +1 к атаке.'},resurrection:{name:'Храм восстановления',from:'shrine',cost:65,crystal:4,work:26,icon:'✥',effects:{resurrect:1},text:'Сохраняет кристаллы Святилища; позволяет воскрешать.'},chapel:{name:'Часовня',cost:40,crystal:2,work:18,icon:'✝',effects:{heal:1},text:'Поддержка героев. Базовые классы доступны без неё.'},light:{name:'Храм света',from:'chapel',cost:55,crystal:4,work:22,icon:'✝',effects:{priest:1},text:'Сохраняет Часовню; открывает Жреца.'},cathedral:{name:'Собор света',from:'light',cost:80,crystal:6,work:30,icon:'♜',effects:{highpriest:1,paladin:1},text:'Сохраняет Храм света; открывает дальнейшее обучение.'},shield:{name:'Школа щита',from:'forge',cost:50,work:22,icon:'▣',effects:{bastion:1},text:'Сохраняет Кузницу; открывает Бастиона.'},fury:{name:'Зал ярости',from:'forge',cost:50,work:22,icon:'⚔',effects:{berserker:1},text:'Сохраняет Кузницу; открывает Берсерка.'},range:{name:'Охотничий двор',cost:40,work:18,icon:'➶',effects:{},text:'Основа специализированного обучения.'},sniper:{name:'Башня стрелка',from:'range',cost:50,work:22,icon:'➶',effects:{sniper:1},text:'Открывает Снайпера.'},swift:{name:'Двор быстрых стрел',from:'range',cost:50,work:22,icon:'➶',effects:{swift:1},text:'Открывает Стрижа.'},den:{name:'Тайное убежище',cost:40,work:18,icon:'◆',effects:{},text:'Основа обучения Плутов.'},assassin:{name:'Дом скрытого клинка',from:'den',cost:50,work:22,icon:'◆',effects:{assassin:1},text:'Открывает Ассасина.'},thief:{name:'Воровская гильдия',from:'den',cost:50,work:22,icon:'◆',effects:{thief:1},text:'Открывает Вора: ускоряет осаду и повышает трофеи.'},cult:{name:'Тайное святилище',from:'chapel',cost:55,crystal:4,work:22,icon:'✦',effects:{cultist:1},text:'Открывает Культиста.'},elemental:{name:'Школа стихий',from:'chapel',cost:55,crystal:4,work:22,icon:'✦',effects:{elementalist:1},text:'Открывает Стихийника.'}};
const SYN=[{a:'housing',b:'farm',key:'food',n:2,text:'Снабжение квартала'},{a:'housing',b:'market',key:'gold',n:2,text:'Покупатели рядом'},{a:'workshop',b:'market',key:'gold',n:2,text:'Продажа изделий'},{a:'workshop',b:'forge',key:'prod',n:2,text:'Совместные мастерские'},{a:'shrine',b:'chapel',key:'crystal',n:1,text:'Священный источник'},{a:'hospital',b:'resurrection',key:'recovery',n:1,text:'Уход за воскрешёнными'},{a:'workshop',b:'siegeworks',key:'siege',n:1,text:'Осадные механизмы'},{a:'tavern',b:'housing',key:'gold',n:1,text:'Постояльцы'}];
const SUBS={bastion:{name:'Бастион',cls:'warrior',text:'Больше защиты; принимает часть урона соседнего союзника.'},berserker:{name:'Берсерк',cls:'warrior',text:'Больше урона; подхватывает атаки союзников.'},assassin:{name:'Ассасин',cls:'rogue',text:'+5 урона.'},thief:{name:'Вор',cls:'rogue',text:'+1 к силе осады; больше золота за победу.'},sniper:{name:'Снайпер',cls:'archer',text:'+2 дальности, +3 урона.'},swift:{name:'Стриж',cls:'archer',text:'Две атаки за ход при наличии действий.'},priest:{name:'Жрец',cls:'acolyte',text:'Усиленное лечение.'},cultist:{name:'Культист',cls:'acolyte',text:'Проклятья вызывают дополнительный стресс.'},elementalist:{name:'Стихийник',cls:'acolyte',text:'Усиленный Болт.'},highpriest:{name:'Верховный жрец',cls:'acolyte',level:8,parent:'priest',text:'В городе позволяет воскрешать без потери уровня.'},paladin:{name:'Паладин',cls:'acolyte',level:8,parent:'priest',text:'Боец поддержки с аурой защиты.'}};
let S=null,serial=0,processing=false,toastTimer;
const UI={selected:17,army:null,modal:null,cityPlot:null,building:'market',candidate:null,chosen:[],startPool:[],tab:'',battleSelected:null,mode:'attack',spell:null};
const id=p=>p+(++serial),clone=o=>JSON.parse(JSON.stringify(o)),player=()=>S.factions[0],army=()=>player().armies.find(a=>a.id===UI.army)||player().armies[0]||null;
const allArmies=()=>S.factions.flatMap(f=>f.dead?[]:f.armies),findArmy=i=>allArmies().find(a=>a.id===i),owner=a=>S.factions[a.owner],living=a=>a.heroes.filter(h=>h.hp>0&&!h.dead),maxHP=h=>C[h.cls].hp+(h.level-1)*6,hasTrait=(h,t)=>h.traits.includes(t);
function nb(i,w=N,h=N){const x=i%w,y=Math.floor(i/w);return[[x+1,y],[x-1,y],[x+(y%2?1:0),y-1],[x+(y%2?0:-1),y-1],[x+(y%2?1:0),y+1],[x+(y%2?0:-1),y+1]].filter(([a,b])=>a>=0&&a<w&&b>=0&&b<h).map(([a,b])=>b*w+a);}
function dist(a,b,w=N){let x=a%w,y=Math.floor(a/w),u=b%w,v=Math.floor(b/w);x-=(y-(y&1))/2;u-=(v-(v&1))/2;return(Math.abs(x-u)+Math.abs(y-v)+Math.abs(x+y-u-v))/2;}
const cell=i=>S.map[i],button=(a,t,extra='',disabled=false,klass='')=>`<button class="${klass}" data-a="${a}" ${extra} ${disabled?'disabled':''}>${t}</button>`,bar=(v,m=100,color='var(--gold)')=>`<div class="bar"><i style="width:${clamp(v/m*100,0,100)}%;background:${color}"></i></div>`;
function say(t){$('toast').textContent=t;$('toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').hidden=true,4500);}
function log(t){S.log.unshift({turn:S.turn,text:t});S.log=S.log.slice(0,160);}
function show(type,html,wide=false){UI.modal=type;$('modal').innerHTML=`<section class="window ${wide?'wide':''}">${html}${type==='battle'||type==='aftermath'||type==='start'?'':`<div class="stack">${button('close','Закрыть')}</div>`}</section>`;$('modal').hidden=false;}
function closeModal(){UI.modal=null;$('modal').hidden=true;$('modal').innerHTML='';}
function stats(h,k){return C[h.cls][k]+Math.floor((h.level-1)/3);}
function createHero(cls,level=1){const n=++serial;return{id:'h'+n,name:NAMES[(n-1)%NAMES.length],cls,level,xp:0,hp:C[cls].hp+(level-1)*6,mana:C[cls].mana,traits:[['brave','kind','sociable'][n%3],['greedy','stubborn','cautious'][n%3]],loyalty:65,stress:0,bonds:{},sub:null,talent:false,weak:0,warning:null,originalOwner:null,items:[{id:id('i'),name:cls==='archer'?'Походный лук':cls==='acolyte'?'Посох ученика':'Походное оружие',value:10,kind:'weapon'}]};}
function createArmy(f,pos,heroes=[]){const a={id:id('a'),owner:f.id,pos,heroes,mp:5,escort:null};f.armies.push(a);return a;}
function reveal(f,pos,r=1){const opened=[];for(let i=0;i<N*N;i++)if(dist(i,pos)<=r&&!f.seen[i]){f.seen[i]=true;f.explored++;opened.push(i);}if(f.id===0)FX.reveal(opened);}
function visible(f,pos){return dist(f.city,pos)<=1||f.armies.some(a=>living(a).length&&dist(a.pos,pos)<=1);}
function path(from,to,allowEnemy=false){const costs=new Map([[from,0]]),prev=new Map(),queue=[from];while(queue.length){queue.sort((a,b)=>costs.get(a)-costs.get(b));const u=queue.shift();if(u===to)break;for(const v of nb(u)){const n=costs.get(u)+TERRAIN[cell(v).terrain].cost;if(!costs.has(v)||n<costs.get(v)){costs.set(v,n);prev.set(v,u);queue.push(v);}}}const out=[];let v=to;while(v!==from){if(!prev.has(v))return[];out.unshift(v);v=prev.get(v);}return out;}
function lineage(b){const out=[];while(b){out.push(b);b=BUILD[b]?.from;}return out;}
function hasBuilding(f,b){return Object.values(f.town.buildings).some(v=>lineage(v).includes(b));}
function cityEffects(f,override=null){const buildings=override||f.town.buildings,e={gold:12,food:2,prod:4,crystal:0,heal:0,siege:1,recovery:0},links=[];for(const b of Object.values(buildings))for(const t of lineage(b))for(const [k,v]of Object.entries(BUILD[t].effects))e[k]=(e[k]||0)+v;const seen=new Set();for(const [p,b]of Object.entries(buildings))for(const j of nb(+p))if(buildings[j]){const k=[+p,j].sort((a,b)=>a-b).join(':');if(seen.has(k))continue;seen.add(k);for(const s of SYN){const a=lineage(b),c=lineage(buildings[j]);if(a.includes(s.a)&&c.includes(s.b)||a.includes(s.b)&&c.includes(s.a)){e[s.key]=(e[s.key]||0)+s.n;links.push({p:+p,j,key:s.key,n:s.n,text:s.text});}}}return{...e,links};}
function buildPreview(f,p,b){if(!BUILD[b])return{ok:false,why:'Выберите здание'};const old=f.town.buildings[p],def=BUILD[b];if(!Capital.project(f,+p,b,'build'))return{ok:false,why:'Участок зарезервирован, здание уже есть или не выполнены условия.'};if(!f.town.plots.includes(+p))return{ok:false,why:'Клетка не входит в территорию города'};if(def.from?old!==def.from:!!old)return{ok:false,why:def.from?`Требуется ${BUILD[def.from].name} на этой клетке`:'Клетка занята'};const before=cityEffects(f),after=cityEffects(f,{...f.town.buildings,[p]:b}),changes=Object.keys(after).filter(k=>k!=='links'&&typeof after[k]==='number'&&after[k]!==before[k]).map(k=>({key:k,n:after[k]-(before[k]||0)}));return{ok:true,changes,links:after.links.filter(l=>l.p===+p||l.j===+p),old};}
const METRIC={gold:'золото',food:'рост',prod:'производство',crystal:'кристаллы',heal:'лечение',attack:'атака',siege:'осада',recovery:'восстановление',trade:'торговля',resurrect:'воскрешение',priest:'обучение Жреца',highpriest:'обучение Верховного жреца',paladin:'обучение Паладина',bastion:'обучение Бастиона',berserker:'обучение Берсерка',assassin:'обучение Ассасина',thief:'обучение Вора',sniper:'обучение Снайпера',swift:'обучение Стрижа',cultist:'обучение Культиста',elementalist:'обучение Стихийника'};
function pay(f,g=0,c=0){if(f.gold<g||f.crystal<c)return false;f.gold-=g;f.crystal-=c;return true;}
function queueBuilding(f,p,b){return Capital.enqueue(f,p,b);}
function refreshCandidates(f){f.candidates=Array.from({length:hasBuilding(f,'tavern2')?15:hasBuilding(f,'tavern')?10:5},(_,i)=>createHero(Object.keys(C)[i%Object.keys(C).length],Math.min(4,1+Math.floor(S.turn/18))));}
function beginStart(){UI.startPool=Array.from({length:10},(_,i)=>createHero(Object.keys(C)[i%Object.keys(C).length]));UI.chosen=[];renderStart();}
function renderStart(){show('start',`<div class="eyebrow">Первый отряд · два героя первого уровня</div><h2>Кому вы доверите первое поручение?</h2><p>Выберите двух кандидатов. Их черты будут влиять на события и отношения.</p><div class="three">${UI.startPool.map(h=>`<div class="card candidate ${UI.chosen.includes(h.id)?'active':''}" data-a="pickStart" data-id="${h.id}"><canvas class="heroThumb" data-hero="${h.cls}"></canvas><h3>${h.name}</h3><b>${C[h.cls].name}</b><p class="muted">${h.traits.map(t=>TRAITS[t].name).join(' · ')}</p><small>♥ ${maxHP(h)} · Сила ${stats(h,'str')} · Мудрость ${stats(h,'wis')} · Харизма ${stats(h,'cha')}</small></div>`).join('')}</div><div class="stack">${button('confirmStart',`Начать · выбрано ${UI.chosen.length}/2`,'',UI.chosen.length!==2,'gold')}</div>`,true);Painter.thumbnails();}
function newGame(seed=Date.now(),selected=null){FX.reset();FX.mute(true);serial=0;let z=seed>>>0;const random=()=>{z=(Math.imul(z,1664525)+1013904223)>>>0;return z/4294967296;};S={version:VERSION,seed:seed>>>0,turn:1,completed:0,map:[],factions:[],villages:[],remains:[],convoys:[],sieges:[],log:[],battle:null,aftermath:null,result:null,phase:null,decree:null,dominance:{leader:null,held:0,checked:0},serial:0};for(let i=0;i<N*N;i++){const r=random();S.map.push({terrain:r<.53?'plain':r<.76?'forest':r<.88?'hill':r<.94?'river':r<.98?'swamp':'mountain',searched:false,site:null});}const homes=[34,45,221,210];for(let n=0;n<4;n++){const f={id:n,name:HOUSES[n],city:homes[n],dead:false,gold:95,crystal:8,rep:0,seen:Array(256).fill(false),explored:0,kills:0,armies:[],bag:[],morgue:[],prison:[],candidates:[],town:{plots:nb(homes[n]),buildings:{},population:1,growth:0,claims:0,queue:null,walls:'palisade',wallQueue:null}};S.factions.push(f);cell(f.city).terrain='plain';cell(f.city).searched=true;cell(f.city).site={type:'city',owner:n};for(const i of nb(f.city))cell(i).terrain='plain';createArmy(f,f.city,[createHero('warrior'),createHero(n===2?'archer':'acolyte')]);reveal(f,f.city,2);refreshCandidates(f);}if(selected){player().armies[0].heroes=selected.map(h=>({...clone(h),id:id('h'),originalOwner:0}));}for(const f of S.factions)for(const a of f.armies)for(const h of a.heroes)if(h.originalOwner===null)h.originalOwner=f.id;
 const places=[[4,3],[11,3],[12,11],[3,12],[7,5],[10,8],[7,12],[4,7]];places.forEach(([x,y],i)=>{const v={id:i,pos:y*N+x,name:['Липовка','Рудный Бор','Тихие Ключи','Медвежий Брод','Верески','Старые Сосны','Ольховка','Мельничный Луг'][i],good:i%3===0?'crystal':'gold',affinity:[0,0,0,0],favorite:null,last:[-1,-1,-1,-1],quest:[false,false,false,false],trades:[0,0,0,0],threat:true};S.villages.push(v);cell(v.pos).terrain='plain';cell(v.pos).searched=true;cell(v.pos).site={type:'village',id:i};});for(const p of [37,42,125,219,213,114,119,169]){cell(p).site={type:'camp',cleared:false};cell(p).searched=true;}for(let i=0;i<256;i++)if(!cell(i).site&&random()<.055)cell(i).site={type:'ruin',done:false,special:i%3===0};cell(136).site={type:'court'};cell(136).terrain='plain';cell(136).searched=true;Bestiary.populate();newDecree();UI.army=player().armies[0].id;UI.selected=player().city;UI.cityPlot=null;closeModal();processing=false;TurnFlow.initialize();log('Король объявил поиск преемника. Два героя готовы к первому походу.');after();Painter.home();FX.mute(false);if(selected)TurnFlow.welcome();}
function save(){if(!S)return;S.serial=serial;try{localStorage.setItem(SAVE,JSON.stringify(S));}catch{say('Автосохранение недоступно. Используйте экспорт.');}}
function validate(s){if(!s||s.version!==4||s.map?.length!==256||s.factions?.length!==4||!Array.isArray(s.villages)||!Array.isArray(s.convoys)||!Array.isArray(s.remains)||!Number.isInteger(s.turn)||s.turn<1||s.turn>61)throw Error('Неверная версия сохранения');for(const c of s.map)if(!TERRAIN[c.terrain])throw Error('Повреждён рельеф');for(const f of s.factions){if(typeof f.name!=='string'||/[<>&]/.test(f.name))throw Error('Неверное имя дома');if(!Number.isFinite(f.gold)||f.gold<0||!Array.isArray(f.armies)||!f.town||!Array.isArray(f.town.plots))throw Error('Повреждён город');for(const a of f.armies){if(a.heroes?.length>4||!Number.isInteger(a.pos)||a.pos<0||a.pos>=256)throw Error('Повреждён отряд');for(const h of a.heroes)if(typeof h.name!=='string'||/[<>&]/.test(h.name)||!C[h.cls]||!Number.isFinite(h.hp)||h.level<1||h.level>8)throw Error('Повреждён герой');}}}
function load(data=null){try{const s=data||JSON.parse(localStorage.getItem(SAVE));validate(s);FX.reset();S=s;BattleRules.normalizeSave(S.battle);Relations.normalize();Bestiary.upgrade();serial=S.serial||100;UI.army=player().armies[0]?.id;UI.selected=army()?.pos??player().city;closeModal();processing=false;after();Painter.home();if(S.battle)renderBattle();else if(S.aftermath)renderAftermath();else if(S.phase)setTimeout(endTurn,30);else if(S.turnFlow?.report?.pending)FX.whenIdle(TurnFlow.openReport);return true;}catch(e){say(e.message||'Не удалось прочитать сохранение');return false;}}
function exportSave(){if(!S)return;const u=URL.createObjectURL(new Blob([JSON.stringify(S,null,2)],{type:'application/json'})),a=document.createElement('a');a.href=u;a.download=`tuman-kosti-v04-turn-${S.turn}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(u),500);}
function victory(){if(S.result)return;const fs=S.factions.filter(f=>!f.dead);if(player().dead){S.result={winner:null,text:'Ваша столица захвачена. Дом Янтаря выбыл.'};return;}if(fs.length===1){S.result={winner:fs[0].id,text:'Все остальные столицы захвачены.'};return;}fs.sort((a,b)=>b.rep-a.rep);const d=S.dominance,f=fs[0];if(f.rep>=60&&f.rep>fs[1].rep){if(d.leader!==f.id){d.leader=f.id;d.held=0;d.checked=S.completed;}else if(S.completed>d.checked){d.held+=S.completed-d.checked;d.checked=S.completed;}if(d.held>=5)S.result={winner:f.id,text:'Превосходство удержано пять полных ходов.'};}else{d.leader=null;d.held=0;d.checked=S.completed;}if(!S.result&&S.completed>=60){const tied=fs.filter(v=>v.rep===f.rep);S.result={winner:tied.length===1?f.id:null,text:tied.length===1?'Королевский совет выбрал лидера по репутации.':'Совет завершился ничьей.'};}}
function after(){if(!S)return;Relations.cleanup();victory();save();render();}
function awardXP(h,n,restore=true){h.xp+=n;while(h.level<8&&h.xp>=h.level*18){h.xp-=h.level*18;h.level++;if(restore&&h.hp>0)h.hp+=6;log(`${h.name}: ${h.level}-й уровень.`);}}
function gainXP(a,n){for(const h of living(a))awardXP(h,n);}
function newDecree(){const types=['tribute','patrol','relations','artifact'];const type=types[(S.turn===1?0:Math.floor(S.turn/8))%4];S.decree={id:id('d'),type,start:S.turn,deadline:S.turn+8,status:S.factions.map(f=>({main:false,extra:false,kills:f.kills,aff:S.villages.reduce((n,v)=>n+v.affinity[f.id],0)}))};if(S.turn>1){log('Король издал новый обязательный указ.');TurnFlow.notice('king','Новый королевский указ',decreeInfo(player()).title+'. '+decreeInfo(player()).text,'king');}}
function decreeInfo(f){const d=S.decree,s=d.status[f.id];if(d.type==='tribute')return{title:'Обеспечить королевский двор',text:'Основное: отправить 35 золота из своей столицы. Дополнительно: 3 кристалла.',ready:f.gold>=35&&f.armies.some(a=>a.pos===f.city),extra:f.crystal>=3};if(d.type==='patrol')return{title:'Очистить королевские дороги',text:'Основное: одна победа над существами или разбойниками после объявления. Дополнительно: ещё две победы.',ready:f.kills-s.kills>=1,extra:f.kills-s.kills>=3};if(d.type==='relations')return{title:'Заслужить доверие деревень',text:'Основное: увеличить суммарные отношения с деревнями на 20. Дополнительно: выполнить деревенскую просьбу и добиться особой дружбы.',ready:S.villages.reduce((n,v)=>n+v.affinity[f.id],0)-s.aff>=20,extra:S.villages.some(v=>v.favorite===f.id)};return{title:'Сокровище для короны',text:'Основное: подарить артефакт стоимостью не менее 40. Дополнительно: найти и передать Печать первого короля.',ready:f.bag.some(i=>i.kind==='artifact'&&i.value>=40),extra:f.bag.some(i=>i.special)};}
function fulfill(f,extra=false){const d=S.decree,s=d.status[f.id],v=decreeInfo(f);if(extra){if(!s.main||s.extra||!v.extra)return false;if(d.type==='tribute')f.crystal-=3;if(d.type==='artifact'){const i=f.bag.findIndex(i=>i.special);if(i<0)return false;f.bag.splice(i,1);}s.extra=true;f.rep+=18;f.gold+=15;log(`${f.name}: дополнительные условия указа исполнены, +18 репутации.`);}else{if(s.main||!v.ready)return false;if(d.type==='tribute')f.gold-=35;if(d.type==='artifact'){const i=f.bag.findIndex(i=>i.kind==='artifact'&&i.value>=40&&!i.special);const j=i>=0?i:f.bag.findIndex(i=>i.kind==='artifact'&&i.value>=40);const [gift]=f.bag.splice(j,1);if(gift.special&&!s.extra){s.extra=true;f.rep+=18;f.gold+=15;} }s.main=true;f.rep+=12;log(`${f.name}: основная часть указа исполнена, +12 репутации.`);}return true;}
function requestBoon(f,k){const b={gold:{cost:12,act:()=>f.gold+=60},crystal:{cost:10,act:()=>f.crystal+=5},support:{cost:8,act:()=>{for(const a of f.armies)for(const h of a.heroes){h.loyalty=clamp(h.loyalty+10,0,100);h.stress=Math.max(0,h.stress-10);}}}}[k];if(!b||f.rep<b.cost||f.boonTurn===S.turn)return false;f.rep-=b.cost;f.boonTurn=S.turn;b.act();log(`${f.name}: королевское благо, −${b.cost} репутации.`);return true;}
function giftKing(kind,target){const f=player();if(f.giftTurn===S.turn)return false;if(kind==='gold'){if(!pay(f,30))return false;f.rep+=4;}else if(kind==='artifact'){const i=f.bag.findIndex(i=>i.id===target&&i.kind==='artifact');if(i<0)return false;const [it]=f.bag.splice(i,1);f.rep+=Math.max(3,Math.round(it.value/8));}else if(kind==='hero'){const a=f.armies.find(a=>a.heroes.some(h=>h.id===target)),h=a?.heroes.find(h=>h.id===target);if(!a||a.pos!==f.city||h.level!==8||h.hp<=0)return false;a.heroes=a.heroes.filter(v=>v!==h);f.rep+=22;log(`${h.name} переходит на службу королю.`);}else return false;f.giftTurn=S.turn;return true;}
function openEvent(kind,pos,data={}){const a=army();if(!a||!living(a).length||a.pos!==pos||a.mp<1)return;UI.event={kind,pos,...data};UI.eventHero=living(a)[0].id;renderEvent();}
function renderEvent(){const e=UI.event,a=army();if(!e||!a)return;const h=a.heroes.find(h=>h.id===UI.eventHero)||living(a)[0];if(!h)return;UI.eventHero=h.id;const v=e.kind==='village'?S.villages[cell(e.pos).site.id]:null,first=a.heroes.find(h=>h.id===e.first),second=a.heroes.find(h=>h.id===e.second),dc=12+2*[first,second].filter(h=>h&&hasTrait(h,'stubborn')).length;
 const option=(k,text,disabled=false)=>`<span class="ability-tip" data-tip="${esc(Relations.preview(a,h,k))}" tabindex="${disabled?0:-1}">${button('eventChoice',text,`data-v="${k}"`,disabled)}</span>`;let options='';
 if(v)options=`${option('negotiate',`Договориться · Харизма +${stats(h,'cha')+(hasTrait(h,'sociable')?2:0)} · КС 12`)}${option('help',`Помочь жителям · Мудрость +${stats(h,'wis')+(hasTrait(h,'kind')?3:0)} · КС 12`)}${option('gift','Подарки · 15 золота · +16 отношений',player().gold<15)}${v.threat?option('protect','Защитить от разбойников'):''}`;
 else if(e.kind==='conflict')options=`${button('eventChoice',`Примирить · Мудрость +${stats(h,'wis')+(hasTrait(h,'kind')?3:0)} · КС ${dc}`,'data-v="mediate"',a.conflict?.tried===S.turn)}${button('eventChoice',`Компенсация · ${Relations.COMPENSATION} золота · без проверки`,'data-v="compensate"',player().gold<Relations.COMPENSATION)}${button('eventChoice',`Поддержать ${esc(first?.name||'первого спорящего')}`,'data-v="side"')}`;
 else options=`${option('help',`Помочь путнику · Мудрость +${stats(h,'wis')+(hasTrait(h,'kind')?3:0)} · КС 12`)}${option('persuade',`Убедить поделиться сведениями · Харизма +${stats(h,'cha')} · КС 13`)}`;
 show('event',`<div class="eyebrow">Выбор участника влияет на исход</div><h2>${v?v.name:e.kind==='conflict'?'Спор внутри отряда':'Путник у дороги'}</h2><p>${v?'Староста хочет понять, можно ли доверять вашему дому.':e.kind==='conflict'?esc(e.reason||a.conflict?.reason||'Товарищи вспоминают прошлые поступки.'):'У дороги сидит раненый путешественник. Он знает окрестности и нуждается в помощи.'}</p>${e.kind==='conflict'?`<div class="hint">${esc(first?.name)} и ${esc(second?.name)}. Каждый вариант расходует 1 очко перемещения отряда. Компенсация гарантирует урегулирование; проверку примирения можно пройти один раз за ход.</div>`:''}<div class="stack">${living(a).map(t=>button('eventHero',`${esc(t.name)} · ${C[t.cls].name}`,`data-id="${t.id}"`,false,t.id===h.id?'gold':'')).join('')}</div><div class="card"><b>${h.name}</b><p class="muted">${h.traits.map(t=>`${TRAITS[t].name}: ${TRAITS[t].text}`).join(' · ')}</p></div><div class="stack">${options}</div><p class="muted">${e.kind==='conflict'?'Успешное примирение или компенсация: отношения +2 и верность +3 обоим. Поддержка одного закрывает спор, но оставляет обиду у другого.':`Проверка d20 + характеристика ≥ КС. 20 — успех, 1 — провал. Наведите на вариант: видны реакции товарищей на поступок. Помощь деревне при успехе: +18 отношений с деревней, +5 репутации; провал: +3 отношения. Переговоры: +14 / +2 отношений. Один раз за ход.`}</p>`);}
function eventChoice(k){const e=UI.event,a=army(),h=a?.heroes.find(h=>h.id===UI.eventHero);if(!e||!a||!h||a.mp<1)return;const f=owner(a),v=e.kind==='village'?S.villages[cell(e.pos).site.id]:null;
 if(e.kind==='conflict'){const result=Relations.resolve(a,h,k);if(!result)return;UI.event=null;show('eventResult',`<h2>Результат</h2><div class="rule">${esc(result.message)}</div>${!result.ok?button('conflict','Вернуться к спору'):''}`);after();return;}
 if(v&&v.last[f.id]===S.turn||k==='gift'&&f.gold<15)return;
 if(k==='protect'&&v){v.last[f.id]=S.turn;a.mp--;Relations.observe(a,h,k);closeModal();startBattle(a,null,{kind:'protect',village:v.id,title:`Защита ${v.name}`,pos:a.pos});return;}
 a.mp--;let message='',success=true;
 if(k==='gift'&&v){f.gold-=15;v.affinity[f.id]=clamp(v.affinity[f.id]+16,0,100);message='Подарки приняты: отношения с деревней +16.';}
 else{const stat=k==='help'?'wis':'cha',bonus=stats(h,stat)+(stat==='wis'&&hasTrait(h,'kind')?3:stat==='cha'&&hasTrait(h,'sociable')?2:0),dc=k==='persuade'?13:12,n=rnd(20),ok=n===20||n!==1&&n+bonus>=dc;success=ok;FX.roll(n,20,{mode:'map',label:`${h.name}: ${stat==='wis'?'Мудрость':'Харизма'}`,modifier:bonus,dc,success:ok});message=`${h.name}: d20 ${n} + ${bonus} против КС ${dc}. ${ok?'Успех':'Провал'}. `;
  if(v){const gain=k==='help'?(ok?18:3):(ok?14:2);v.affinity[f.id]=clamp(v.affinity[f.id]+gain,0,100);if(k==='help'&&ok&&!v.quest[f.id]){v.quest[f.id]=true;f.rep+=5;message+='Просьба выполнена: +5 репутации. ';}message+=`Отношения с деревней +${gain}.`;}
  else if(ok){f.gold+=12;f.rep+=2;reveal(f,a.pos,2);message+='+12 золота, +2 репутации, сведения об окрестностях.';}else{h.stress=clamp(h.stress+5,0,100);message+='Герой расстроен: +5 стресса.';}gainXP(a,ok?5:1);}
 if(v)v.last[f.id]=S.turn;Relations.observe(a,h,k,success);log(message);UI.event=null;show('eventResult',`<h2>Результат</h2><div class="rule">${esc(message)}</div><p class="muted">Реакции товарищей записаны в истории отношений.</p>`);after();}

function bond(a,b,n,reason){return Relations.adjust(a,b,n,reason);}
function allyVillage(v,f){const others=Math.max(...v.affinity.filter((_,i)=>i!==f.id));return v.quest[f.id]&&v.affinity[f.id]>=60&&v.affinity[f.id]>=others+15&&v.favorite!==f.id;}
function search(a){const c=cell(a.pos),f=owner(a);if(c.searched)return;c.searched=true;gainXP(a,2);const n=rnd(20);if(f.id===0)FX.roll(n,20,{mode:'map',label:'Поиск на новом гексе',outcome:n<=3?'Засада':n<=9?'Тихая местность':n<=14?'Золото':n<=17?'Встреча':'Руины'});if(f.id===0)log(`Поиск на гексе: d20 = ${n}.`);if(n<=3){startBattle(a,null,{kind:'ambush',title:'Засада',pos:a.pos});return;}if(n<=9)return;if(n<=14){const lootRoll=rnd(8);if(f.id===0)FX.roll(lootRoll,8,{mode:'map',label:'Находка: золото',modifier:4,outcome:'В казну'});f.gold+=lootRoll+4;return;}if(n<=17){c.site={type:'event'};if(f.id===0)openEvent('road',a.pos);else{f.gold+=12;gainXP(a,4);}return;}c.site={type:'ruin',done:false,special:!S.specialFound&&n===20};}
function moveTo(a,to){if(!a||!living(a).length||a.mp<1||a.escort)return false;for(const p of path(a.pos,to)){const enemy=S.factions.find(f=>!f.dead&&f.id!==a.owner&&f.city===p)||allArmies().find(t=>t.owner!==a.owner&&living(t).length&&t.pos===p);if(enemy)break;const cost=TERRAIN[cell(p).terrain].cost;if(a.mp<cost)break;const from=a.pos;a.mp-=cost;a.pos=p;FX.move('map',a.id,from,p,{owner:a.owner,label:a.owner===0?'Отряд в пути':HOUSES[a.owner]+' перемещает отряд'});reveal(owner(a),p);search(a);if(S.battle||S.aftermath||UI.modal==='event'||cell(p).site)break;}if(a.owner===0){UI.selected=a.pos;after();}return true;}
function exploreSite(){const a=army(),c=cell(a.pos);if(!a||a.mp<1||!living(a).length)return;if(c.site?.type==='camp'&&!c.site.cleared){a.mp--;startBattle(a,null,{kind:'camp',title:Bestiary.families[Bestiary.family(a.pos)].lair,pos:a.pos});return;}if(c.site?.type==='event'){openEvent('road',a.pos);return;}if(c.site?.type==='ruin'&&!c.site.done){if(c.site.guarded&&!c.site.cleared){a.mp--;startBattle(a,null,{kind:'ruin',title:'Стражи руин',family:c.site.family,pos:a.pos});return;}a.mp--;c.site.done=true;const special=c.site.special&&!S.specialFound;const it={id:id('i'),kind:'artifact',name:special?'Печать первого короля':'Перстень советника',value:special?90:45,special};owner(a).bag.push(it);Development.discover(owner(a));if(special)S.specialFound=true;owner(a).gold+=15;gainXP(a,10);log(`${owner(a).name} исследовал руины и нашёл ${it.name}.`);after();}}
function splitHero(hid){const a=army(),h=a?.heroes.find(h=>h.id===hid);if(!a||!h||a.heroes.length<=1||a.escort)return;const b=createArmy(player(),a.pos,[h]);b.mp=a.mp;a.heroes=a.heroes.filter(t=>t!==h);UI.army=b.id;after();}
function transferHero(hid,target){const a=army(),b=findArmy(target),h=a?.heroes.find(h=>h.id===hid);if(!h||!b||a===b||b.owner!==0||dist(a.pos,b.pos)>1||b.heroes.length>=4||a.escort||b.escort)return false;a.heroes=a.heroes.filter(t=>t!==h);b.heroes.push(h);cleanupArmies();return true;}
function cleanupArmies(){for(const f of S.factions)f.armies=f.armies.filter(a=>a.heroes.length);if(!findArmy(UI.army))UI.army=player().armies[0]?.id;}
function hire(hid){const f=player(),i=f.candidates.findIndex(h=>h.id===hid);if(i<0||f.gold<40||S.sieges.some(s=>s.defender===0))return false;let a=f.armies.find(a=>a.pos===f.city&&a.heroes.length<4&&!a.escort);if(!a)a=createArmy(f,f.city);const h=f.candidates.splice(i,1)[0];h.originalOwner=0;Capital.bonuses(f,h);f.gold-=40;a.heroes.push(h);UI.army=a.id;log(`${h.name} поступает на службу. В отряде ${a.heroes.length}/4 героев.`);return true;}
function availableSub(h,f){
  return h.level>=6&&!h.sub&&hasBuilding(f,Capital.classes[h.cls])&&Capital.level(f,h.cls)>=2 ? Capital.branches(h.cls) : [];
}
function chooseSub(hid,sub){
  const a=army(),h=a?.heroes.find(h=>h.id===hid),f=player();
  if(!h||!availableSub(h,f).some(([k])=>k===sub)) return false;
  h.sub=sub;
  Capital.bonuses(f,h);
  return true;
}
function armor(u,type){const b=S.battle;return(type==='pierce'?u.pierce:type==='slash'?u.slash:u.ac)+(u.guard?2:0)+(u.wardUntil>=b.round?3:0)+(u.friendCover&&activeUnits(b,u.side).some(t=>t.id===u.friendCover&&dist(t.pos,u.pos,8)<=1)?2:0)+(b.units.some(t=>t.hp>0&&!t.surrender&&t.side===u.side&&t.sub==='paladin'&&dist(t.pos,u.pos,8)<=1)?1:0);}
const activeUnits=(b,s)=>b.units.filter(u=>u.side===s&&u.hp>0&&!u.surrender&&!u.retreated);
function makeUnit(h,a,side,i){const c=C[h.cls],f=owner(a),lev=h.level-1,care=hasTrait(h,'cautious')?1:0,bonded=a.heroes.some(t=>t!==h&&(h.bonds[t.id]||0)>=2),conflict=a.heroes.some(t=>t!==h&&(h.bonds[t.id]||0)<=-2);return{id:h.id,hero:h.id,name:h.name,owner:f.id,side,cls:h.cls,sub:h.sub,pos:(i+1)*8+(side===0?1:6),hp:h.hp,max:Math.floor(maxHP(h)*(h.weak?.75:1)),mana:h.mana,maxMana:c.mana,stress:h.stress,pierce:c.pierce+care+Math.floor(lev/3)+(h.sub==='bastion'?3:0),slash:c.slash+care+Math.floor(lev/3)+(h.sub==='bastion'?3:0),ac:c.ac+care,atk:c.atk+lev+(cityEffects(f).attack||0)+(bonded?1:0)-(conflict?1:0)-(h.weak?2:0)-(!h.items.some(i=>i.kind==='weapon')?3:0),damage:c.damage+Math.floor(lev/2)+(h.sub==='assassin'?5:h.sub==='sniper'?3:h.sub==='berserker'?3:0),range:c.range+(h.sub==='sniper'?2:0),speed:c.speed,ap:3,used:false,surrender:false,resolveChecked:false,level:h.level,brave:hasTrait(h,'brave'),wis:stats(h,'wis'),originalOwner:h.originalOwner};}
function strength(a){return living(a).reduce((n,h)=>n+h.hp*(1+(h.level-1)*.2),0);}
function startBattle(a,d,meta){if(S.battle||!living(a).length)return false;const f=owner(a),of=d?owner(d):meta.defender!=null?S.factions[meta.defender]:null,units=living(a).map((h,i)=>makeUnit(h,a,0,i));if(d)units.push(...living(d).map((h,i)=>makeUnit(h,d,1,i)));else units.push(...Bestiary.create(a,meta,of));
 S.battle={id:id('b'),attacker:a.id,defender:d?.id??null,attackOwner:f.id,defendOwner:of?.id??null,meta,units,round:1,side:0,human:f.id===0?0:of?.id===0?1:null,log:['Первыми ходят нападающие.'],over:null,retreat:false,healed:[],combos:[],power:[units.filter(u=>u.side===0).reduce((n,u)=>n+u.max*(1+(u.level-1)*.2),0),units.filter(u=>u.side===1).reduce((n,u)=>n+u.max*(1+(u.level-1)*.2),0)]};
 for(const u of units)u.ap=3;
 Tactics.field();
 // Former companions recognise each other; both sides feel the encounter.
 for(const u of units)if(u.hero&&units.some(t=>t.hero&&t.side!==u.side&&(u.originalOwner!==u.owner&&t.owner===u.originalOwner||t.originalOwner!==t.owner&&u.owner===t.originalOwner)))stressUnit(u,18,'Бывшие товарищи по другую сторону');
 UI.battleSelected=null;UI.mode='attack';if(S.battle.human===null){autoBattle();finishBattle();}else{if(S.battle.side!==S.battle.human)advanceBattle();renderBattle();save();render();}return true;}
function checkBattle(){const b=S.battle;if(!b||b.over!==null)return;if(!activeUnits(b,0).length)b.over=1;else if(!activeUnits(b,1).length)b.over=0;}
function stressUnit(u,n,why){
 const b=S.battle;
 if(!u.hero||u.surrender)return;
 u.stress=clamp(u.stress+n,0,100);
 if(u.hp<=0||u.stress<100||u.resolveChecked)return;
 u.resolveChecked=true;
 const resolve=(u.wis||0)+(u.brave?2:0);
 const inspired=Strike.chance(Math.max(1,resolve-1)/20);
 FX.effect(inspired?'inspired':'surrender',u.pos,u.pos,{label:inspired?'Воодушевление':'Герой сдаётся'});
 if(inspired){
   u.stress=55;u.inspired=true;u.atk+=2;
   b.log.unshift(u.name+': воодушевление!');
 }else{
   u.surrender=true;u.ap=0;
   b.log.unshift(`${u.name}: ${why}. Герой бросает оружие и сдаётся.`);
 }
 checkBattle();
}
function occupiedBattle(pos){return S.battle.units.some(u=>u.pos===pos&&u.hp>0&&!u.retreated);}
function battleReach(u){return Tactics.paths(u).costs;}
function moveBattle(u,p){if(!u||u.surrender||u.retreated||u.hp<=0||u.attackedRound===S.battle.round||p===u.pos)return false;const route=Tactics.route(u,p);if(!route.length)return false;let from=u.pos;u.pos=p;u.ap--;u.movedRound=S.battle.round;for(const to of route){FX.move('battle',u.id,from,to,{battleId:S.battle.id,label:u.name+' перемещается',duration:route.length>1?400:620});from=to;}return true;}

function damageUnit(t,dmg,critical=false,source=null){const b=S.battle,bastion=activeUnits(b,t.side).find(u=>u!==t&&u.sub==='bastion'&&dist(u.pos,t.pos,8)<=1);if(bastion&&dmg>1){const part=Math.floor(dmg*.3);const prior=bastion.hp;bastion.hp=Math.max(0,bastion.hp-part);FX.effect('protect',t.pos,bastion.pos,{target:bastion.id,hpBefore:prior,hpAfter:bastion.hp,amount:part,label:'Бастион прикрывает товарища',text:'Прикрытие'});dmg-=part;b.log.unshift(`${bastion.name} принимает ${part} урона за ${t.name}.`);}t.hp=Math.max(0,t.hp-dmg);if(critical)stressUnit(t,20,'Критическое попадание');if(t.hp<=0)b.log.unshift(`${t.name} без сознания. Его можно поднять лечением.`);checkBattle();}
function attackBattle(u,t,special=false,free=false,magic=false){return BattleRules.attack(u,t,special,free,magic);}
const SPELLS={bolt:{name:'Болт',cost:2,target:'enemy'},heal:{name:'Лечение',cost:3,target:'ally'},ward:{name:'Оберег',cost:2,target:'ally'},curse:{name:'Проклятье',cost:2,target:'enemy'}};
function spellBattle(u,t,k){const b=S.battle,s=SPELLS[k];if(!s||!u||!t||u.cls!=='acolyte'||u.hp<=0||u.surrender||u.ap<1||u.mana<s.cost||dist(u.pos,t.pos,8)>4||!Tactics.sight(u.pos,t.pos))return false;if(s.target==='enemy'&&(u.side===t.side||t.hp<=0||t.surrender))return false;if(s.target==='ally'&&u.side!==t.side)return false;if(k==='heal'){if(t.hp>=t.max||t.surrender||t.expired||t.retreated||t.hp<=0&&occupiedBattle(t.pos))return false;const down=t.hp<=0,previousHP=t.hp;t.hp=Math.min(t.max,t.hp+14+(u.branch?.heal||0)+(u.sub==='priest'||u.sub==='highpriest'?8:0));FX.effect('heal',u.pos,t.pos,{target:t.id,hpBefore:previousHP,hpAfter:t.hp,amount:t.hp-previousHP,label:down?'Поднимаем товарища':'Лечение'});if(down){t.ap=1;t.raisedRound=b.round;t.deathTurns=0;}if(down)Relations.rescue(u,t);}else if(k==='ward'){if(t.hp<=0||t.surrender)return false;t.wardUntil=b.round+1;FX.effect('ward',u.pos,t.pos,{label:'Оберег'});}else if(k==='curse'){t.curseUntil=b.round+1;FX.effect('curse',u.pos,t.pos,{label:'Проклятье'});stressUnit(t,u.sub==='cultist'?22:10,'Проклятье');}if(k==='bolt'&&!Tactics.canAttack(u,t))return false;u.mana-=s.cost;if(k==='bolt'){const old=u.damage;u.damage+=u.sub==='elementalist'?6:0;attackBattle(u,t,false,false,true);u.damage=old;}else u.ap--;b.log.unshift(`${u.name}: ${s.name} → ${t.name}, −${s.cost} маны.`);checkBattle();return true;}
function skillBattle(u){if(!u||u.hp<=0||u.surrender||u.ap<1)return;if(u.cls==='acolyte'){u.mana=Math.min(u.maxMana,u.mana+4);u.ap--;FX.effect('meditate',u.pos,u.pos,{label:'Медитация'});S.battle.log.unshift(`${u.name}: медитация, +4 маны.`);}else if(u.cls==='warrior'){if(u.talents?.power&&u.powerRound!==S.battle.round)UI.mode='special';}else if(!u.used){UI.mode='special';return;}}
function aiBattle(side){const b=S.battle;for(const u of activeUnits(b,side)){if(b.over!==null)break;if(u.ap<1)continue;if(u.cls==='acolyte'){const hurt=b.units.filter(t=>t.side===side&&!t.surrender&&t.hp<t.max-10&&dist(u.pos,t.pos,8)<=4&&Tactics.sight(u.pos,t.pos)&&(t.hp>0||!occupiedBattle(t.pos))).sort((a,b)=>a.hp/a.max-b.hp/b.max)[0];if(hurt&&spellBattle(u,hurt,'heal'))continue;if(u.mana<2)skillBattle(u);}const enemies=activeUnits(b,1-side);if(!enemies.length)break;let t=enemies.filter(t=>Tactics.canAttack(u,t)).sort((a,b)=>a.hp-b.hp)[0];if(!t&&u.ap){const reach=[...battleReach(u).keys()].filter(i=>i!==u.pos).sort((a,b)=>Math.min(...enemies.map(t=>dist(a,t.pos,8)))-Math.min(...enemies.map(t=>dist(b,t.pos,8))));if(reach.length)moveBattle(u,reach[0]);t=enemies.filter(t=>Tactics.canAttack(u,t)).sort((a,b)=>a.hp-b.hp)[0];}while(t&&u.ap&&b.over===null){
 const special=u.cls==='warrior'?u.talents?.power&&u.powerRound!==b.round:!u.used&&['rogue','archer'].includes(u.cls);
 if(!attackBattle(u,t,special))break;
 t=activeUnits(b,1-side).filter(v=>Tactics.canAttack(u,v)).sort((a,b)=>a.hp-b.hp)[0];
 }
 if(u.ap&&b.over===null){u.guard=true;u.guardBlock=u.cls==='warrior';u.ap=0;}}checkBattle();}
function switchSide(){const b=S.battle;if(b.side===1)b.round++;b.side=1-b.side;
 for(const u of b.units.filter(u=>u.side===b.side&&u.hero&&u.hp===0&&!u.expired&&!u.retreated)){
   u.deathTurns=(u.deathTurns||0)+1;
   if(u.deathTurns>=3){u.expired=true;b.log.unshift(u.name+' погибает.');}
 }
 for(const u of activeUnits(b,b.side)){u.ap=u.raisedRound===b.round?1:3;u.steps=0;u.guard=false;u.guardBlock=false;u.friendCover=null;}
 UI.battleSelected=null;UI.mode='attack';if(b.round>70){b.over=1;b.log.unshift('Нападающие не добились победы за 70 раундов.');}}
function advanceBattle(){const b=S.battle;if(!b||b.over!==null)return;aiBattle(b.side);if(b.over===null)switchSide();}
function endBattleTurn(){if(FX.busy)return;const b=S.battle;if(!b||b.over!==null||b.side!==b.human)return;for(const u of activeUnits(b,b.side))u.ap=0;switchSide();if(b.over===null)advanceBattle();renderBattle();after();}
function autoBattle(){return FX.auto(()=>{const b=S.battle;let k=0;while(b&&b.over===null&&k++<150)advanceBattle();if(b?.over===null)b.over=1;});}
function clickBattle(p){if(FX.busy)return;const b=S.battle;if(!b||b.over!==null||b.side!==b.human)return;let u=b.units.find(u=>u.id===UI.battleSelected),t=b.units.find(t=>t.pos===p&&t.hp>0&&!t.retreated);if(UI.mode==='support'&&u){if(Relations.support(u,t))UI.mode='attack';else say('Нужен соседний друг в строю; пара может применить прикрытие один раз за бой.');}else if(UI.mode==='spell'&&u){t=t||b.units.find(t=>t.pos===p&&!t.retreated&&!t.expired);if(!spellBattle(u,t,UI.spell))say('Недоступная цель, дальность или недостаток маны.');else UI.mode='attack';}else if(t?.side===b.human&&!t.surrender){UI.battleSelected=t.id;UI.mode='attack';}else if(u&&t){if(!attackBattle(u,t,UI.mode==='special'))say('Цель вне дальности, закрыта препятствием или не хватает маны.');UI.mode='attack';}else if(u&&!moveBattle(u,p))say('Клетка занята, непроходима или путь требует слишком много движения.');renderBattle();after();}
function finishBattle(){
 const b=S.battle;
 if(!b||b.over===null)return;
 const aa=findArmy(b.attacker),dd=findArmy(b.defender),win=b.over,wa=win===0?aa:dd;
 const wf=S.factions[win===0?b.attackOwner:b.defendOwner],lf=S.factions[win===0?b.defendOwner:b.attackOwner];
 const place=b.meta.pos??aa?.pos??0,m={winner:wf?.id,pos:place,army:wa?.id,corpses:[],eligible:[],loot:[]};
 for(const [a,side] of [[aa,0],[dd,1]]) {
   if(!a)continue;
   const f=owner(a),keep=[];
   for(const h of a.heroes) {
     const u=b.units.find(u=>u.hero===h.id);
     if(!u){keep.push(h);continue;}
     h.hp=u.hp;h.mana=u.mana;h.stress=u.stress;
     awardXP(h,side===win?14:8,false);
     if(u.retreated){
       h.hp=Math.max(1,Math.floor(u.hp/2));
       (f.retreats??=[]).push({hero:h,turn:S.turn+3});
     } else if(u.expired||side!==win&&u.hp===0&&!wf) BattleRules.bury(m,h);
     else if(side!==win&&u.hp===0) m.eligible.push(h);
     else {
       h.hp=u.hp===0?1:u.hp;
       h.loyalty=clamp(h.loyalty+(side===win?3:-8),0,100);
       keep.push(h);
     }
   }
   a.heroes=keep;a.mp=0;
   if(side!==win&&a.heroes.length)a.pos=f.city;
 }
 if(wf){
   const ratio=b.power[1-win]/Math.max(1,b.power[win]),rep=clamp(Math.round(5*ratio),1,12);
   wf.rep+=rep;
   if(lf)lf.rep-=clamp(Math.round(5/Math.max(.3,ratio)),1,10);
   log(`${wf.name}: победа, +${rep} репутации.`);
 } else if(lf)lf.rep-=4;
 if(wa&&wa.heroes.length){
   wa.pos=place;Relations.victory(wa,b);
   if(!lf){
     wf.gold+=20+(wa.heroes.some(h=>h.sub==='thief')?10:0);wf.kills++;
     if(['camp','ruin'].includes(b.meta.kind)&&cell(place).site)cell(place).site.cleared=true;
     if(b.meta.kind==='protect'){
       const v=S.villages[b.meta.village];
       v.threat=false;v.quest[wf.id]=true;v.affinity[wf.id]=clamp(v.affinity[wf.id]+30,0,100);wf.rep+=5;
     }
   }
 }
 if(['siege','sally'].includes(b.meta.kind)){
   const def=S.factions[b.meta.defender];
   if(b.meta.kind==='siege'?win===0:win===1){def.dead=true;log(CITIES[def.id]+' захвачен.');}
   S.sieges=S.sieges.filter(s=>s.id!==b.meta.siegeId);
 }
 if(b.human!==null)TurnFlow.notice('battle',win===b.human?'Победа в бою':'Поражение в бою',b.meta.title);
 if(b.meta.kind==='convoy'&&win===0&&wa){
   const wagon=S.convoys.find(c=>c.id===b.meta.convoy);
   if(wagon)takeConvoy(wagon,wa);
 }
 S.battle=null;UI.battleSelected=null;cleanupArmies();UI.selected=army()?.pos??player().city;
 if(wf?.id===0&&(m.eligible.length||m.loot.length||m.corpses.length)){
   S.aftermath=m;UI.lootHero=null;renderAftermath();
 } else {
   for(const h of [...m.eligible])BattleRules.fate(m,h,false);
   BattleRules.stash(m);
   if(wf&&m.corpses.length&&hasBuilding(wf,'resurrection'))dispatchBodies(wf,place,m.corpses);
   closeModal();
 }
 after();
 if(S.phase&&!S.aftermath&&!S.result)FX.whenIdle(()=>setTimeout(endTurn,35));
}
function releaseHeroes(heroes){for(const h of heroes){const f=S.factions[h.capturedOwner??h.originalOwner];if(!f||f.dead)continue;h.hp=Math.max(1,h.hp);let a=f.armies.find(a=>a.pos===f.city&&a.heroes.length<4);if(!a)a=createArmy(f,f.city);a.heroes.push(h);}}
function renderAftermath(){
 const m=S.aftermath;if(!m)return;
 m.eligible??=[];m.loot=Array.isArray(m.loot)?m.loot:[];
 show('aftermath',`<h2>После боя</h2>
   ${m.eligible.map(h=>`<div class="card"><b>${esc(h.name)} · ${h.level} ур. · 0 HP</b><div class="stack">
     ${button('aftermathFate','Нанять · '+BattleRules.price(h)+' зол.',`data-id="${h.id}" data-v="hire"`,player().gold<BattleRules.price(h))}
     ${button('aftermathFate','Казнить',`data-id="${h.id}"`)}</div></div>`).join('')}
   <h3>Общая добыча</h3>
   <div class="stack">${(findArmy(m.army)?.heroes||[]).map(h=>button('aftermathRecipient',esc(h.name),`data-id="${h.id}"`,false,UI.lootHero===h.id?'gold':'')).join('')}</div>
   ${m.loot.map(item=>`<p>${esc(item.name)} ${button('aftermathLoot','Выдать выбранному герою',`data-id="${item.id}" data-v="equip"`,!lootRecipient(m,item))}</p>`).join('')||'<p>Добычи нет.</p>'}
   <p>Оставшиеся предметы отправятся на склад столицы.</p>
   ${m.corpses.length?button('aftermathBodies','Отправить останки повозкой')+button('aftermathLeave','Оставить останки на гексе'):''}
   ${button('aftermathDone','Завершить','',!!m.eligible.length,'gold')}`);
}
function lootRecipient(m,item){
 const h=findArmy(m.army)?.heroes.find(h=>h.id===UI.lootHero)||findArmy(m.army)?.heroes[0];
 if(!h)return null;
 const gear=['weapon','armor'].includes(item.kind);
 return gear?h.items.some(i=>i.kind===item.kind)?null:h:['potion','scroll'].includes(item.kind)&&h.items.filter(i=>['potion','scroll'].includes(i.kind)).length<2?h:null;
}
function convoyRoute(pos,dest){return path(pos,dest);}
function makeConvoy(f,pos,kind,cargo,dest=f.city){const route=convoyRoute(pos,dest),c={id:id('wagon'),owner:f.id,pos,dest,kind,cargo,route,escort:null,created:S.turn};S.convoys.push(c);if(f.id===0)FX.effect('arrival',pos,pos,{mode:'map',label:'Повозка подготовлена',text:'Повозка готова'});log(`${f.name}: отправлена повозка (${kind==='bodies'?'останки':kind==='prisoners'?'пленники':'освобождённые герои'}), путь ${route.length} гексов.`);return c;}
function dispatchBodies(f,pos,ids){const bodies=S.remains.filter(r=>ids.includes(r.id)&&r.pos===pos);if(!bodies.length)return null;S.remains=S.remains.filter(r=>!bodies.includes(r));return makeConvoy(f,pos,'bodies',bodies.map(r=>r.hero));}
function dispatchCaptives(f,pos,heroes){if(!hasBuilding(f,'prison'))return null;return makeConvoy(f,pos,'prisoners',clone(heroes));}
function bodyShipping(pos,ids,fromAftermath=false){const route=convoyRoute(pos,player().city);UI.shipping={pos,ids,fromAftermath};show('shipping',`<h2>Отправить останки в город</h2><p>Груз: ${ids.map(i=>S.remains.find(r=>r.id===i)?.hero.name).filter(Boolean).join(', ')}.</p><div class="rule">Маршрут: ${route.map(i=>`${i%N+1}:${Math.floor(i/N)+1}`).join(' → ')||'Груз уже в столице'}<br>Примерное время: ${Math.max(1,Math.ceil(route.length/2))} ход.</div><p class="muted">Повозку можно перехватить. В пути бывают мировые события. Отряд на этом гексе можно назначить сопровождением.</p>${button('confirmShipping','Отправить повозку','','', 'gold')}`);}
function escortConvoy(cid,aid){const c=S.convoys.find(c=>c.id===cid),a=findArmy(aid);if(!c||!a||a.owner!==c.owner||a.pos!==c.pos||a.escort||c.escort||!living(a).length)return false;c.escort=a.id;a.escort=c.id;a.mp=0;return true;}
function stopEscort(a){if(a?.escort){const c=S.convoys.find(c=>c.id===a.escort);if(c)c.escort=null;a.escort=null;}}
function convoyArrival(c){if(c.owner===0)FX.effect('arrival',c.dest,c.dest,{mode:'map',label:'Повозка прибыла',text:'Груз доставлен'});const f=S.factions[c.owner];if(c.owner===0)TurnFlow.notice('convoy','Повозка прибыла в город',`${c.cargo.map(h=>h.name).join(', ')}: ${c.kind==='bodies'?'останки доставлены':c.kind==='prisoners'?'пленники доставлены':'герои вернулись'}.`,'cargo',c.id);if(c.kind==='bodies'){f.morgue.push(...c.cargo);log(`${f.name}: останки доставлены в город.`);}else if(c.kind==='prisoners'){f.prison.push(...c.cargo);log(`${f.name}: пленники доставлены в Тюрьму.`);}else{for(const h of c.cargo){h.hp=Math.max(1,h.hp);let a=f.armies.find(a=>a.pos===f.city&&a.heroes.length<4);if(!a)a=createArmy(f,f.city);a.heroes.push(h);}log(`${f.name}: освобождённые герои вернулись без вещей.`);}const a=findArmy(c.escort);if(a)a.escort=null;S.convoys=S.convoys.filter(v=>v!==c);}
function tickConvoys(){for(const c of [...S.convoys]){if(S.factions[c.owner].dead)continue;const a=findArmy(c.escort);if(c.escort&&(!a||a.pos!==c.pos||!living(a).length)){if(a)a.escort=null;c.escort=null;}if(c.pos===c.dest){convoyArrival(c);continue;}const n=rnd(20);if(c.owner===0)FX.roll(n,20,{mode:'map',label:'Дорога повозки',outcome:n<=2?'Размытая дорога':n===3&&!c.escort?'Нападение разбойников':'Путь свободен'});if(n<=2){if(c.owner===0)TurnFlow.notice('convoy','Событие на дороге: задержка повозки','Размытая дорога задержала повозку на ход.','cargo',c.id);log(`${S.factions[c.owner].name}: размытая дорога задержала повозку на ход.`);continue;}if(n===3&&!c.escort){if(c.owner===0)TurnFlow.notice('convoy','Событие на дороге: нападение разбойников','Неохраняемая повозка потеряна. Останки оставлены на гексе; пленные освобождены.','cargo',c.id);if(c.kind==='bodies')for(const hero of c.cargo)S.remains.push({id:id('body'),pos:c.pos,hero,holder:null});else releaseHeroes(c.cargo);S.convoys=S.convoys.filter(v=>v!==c);log(`${S.factions[c.owner].name}: разбойники остановили неохраняемую повозку; груз оставлен на гексе.`);continue;}for(let k=0;k<2;k++){const next=convoyRoute(c.pos,c.dest)[0];if(next==null)break;if(allArmies().some(z=>z.owner!==c.owner&&living(z).length&&z.pos===next)){log('Повозка остановилась перед вражеским отрядом.');break;}const from=c.pos;c.pos=next;FX.move('map',c.id,from,next,{owner:c.owner,label:'Повозка в пути',ghost:{owner:c.owner,kind:c.kind,cargo:c.cargo}});if(a){a.pos=c.pos;a.mp=0;FX.move('map',a.id,from,next,{owner:a.owner,label:'Сопровождение повозки'});}reveal(S.factions[c.owner],c.pos);if(c.pos===c.dest){convoyArrival(c);break;}}}}
function intercept(cid,a){const c=S.convoys.find(c=>c.id===cid);if(!c||!a||c.owner===a.owner||dist(c.pos,a.pos)>1||a.mp<1||!living(a).length)return false;if(c.escort&&findArmy(c.escort)){a.mp--;startBattle(a,findArmy(c.escort),{kind:'convoy',convoy:c.id,pos:c.pos,title:'Перехват охраняемой повозки'});return true;}takeConvoy(c,a);return true;}
function takeConvoy(c,a){const f=owner(a);if(c.kind==='bodies'){for(const h of c.cargo)S.remains.push({id:id('body'),pos:c.pos,hero:h,holder:f.id});}else{const rescued=c.cargo.filter(h=>(h.capturedOwner??h.originalOwner)===f.id),others=c.cargo.filter(h=>!rescued.includes(h));if(rescued.length)makeConvoy(f,c.pos,'released',rescued);if(others.length&&hasBuilding(f,'prison'))makeConvoy(f,c.pos,'prisoners',others);else releaseHeroes(others);}const guard=findArmy(c.escort);if(guard)guard.escort=null;a.mp=0;S.convoys=S.convoys.filter(v=>v!==c);log(`${f.name} перехватил повозку на гексе ${c.pos%N+1}:${Math.floor(c.pos/N)+1}.`);}
function highPriest(f){return f.armies.some(a=>a.pos===f.city&&a.heroes.some(h=>h.hp>0&&(h.sub==='highpriest'||h.sub==='priest'&&h.classRanks?.['priest:3'])));}
function reviveInfo(f,h){const priest=highPriest(f);return{ok:hasBuilding(f,'resurrection')&&(h.level>1||priest)&&f.gold>=25&&f.crystal>=5,priest,why:!hasBuilding(f,'resurrection')?'Нужен Храм восстановления':h.level===1&&!priest?'Герой 1-го уровня не выдержит: нужен Верховный жрец':f.gold<25||f.crystal<5?'Нужно 25 золота и 5 кристаллов':priest?'Уровень сохраняется; слабость 2 хода':'Потеря уровня; слабость 4 хода'};}
function revive(hid,f=player()){const i=f.morgue.findIndex(h=>h.id===hid);if(i<0)return false;const h=f.morgue[i],r=reviveInfo(f,h);if(!r.ok)return false;pay(f,25,5);f.morgue.splice(i,1);if(!r.priest)h.level--;h.dead=false;h.xp=0;h.hp=Math.max(1,Math.floor(maxHP(h)*(r.priest?.8:.6)));h.mana=Math.floor(C[h.cls].mana/2);h.weak=Math.max(1,(r.priest?2:4)-(cityEffects(f).recovery||0));h.loyalty=h.originalOwner===f.id?50:15;h.stress=35;h.warning=null;h.items=[];let a=f.armies.find(a=>a.pos===f.city&&a.heroes.length<4);if(!a)a=createArmy(f,f.city);a.heroes.push(h);if(f.id===0)FX.effect('revive',f.city,f.city,{mode:'map',label:'Воскрешение героя',text:h.name+' возвращается'});log(`${h.name} воскрешён: уровень ${h.level}, слабость ${h.weak} ход., верность ${h.loyalty}.`);return true;}
function offerRansom(hid){const jailer=S.factions.find(f=>f.prison.some(h=>h.id===hid)),h=jailer?.prison.find(h=>h.id===hid);if(!h)return false;const buyer=S.factions[h.capturedOwner??h.originalOwner],price=30+h.level*15;if(!buyer||buyer.dead||buyer.gold<price){say('У владельца пленника недостаточно средств.');return false;}if(jailer.id!==0&&rnd(20)<=5){say('Владелец пленника отказался от сделки.');log('Предложение выкупа отклонено.');return false;}buyer.gold-=price;jailer.gold+=price;jailer.prison=jailer.prison.filter(t=>t!==h);makeConvoy(buyer,jailer.city,'released',[h],buyer.city);log(`Выкуп за ${h.name}: ${price} золота. Герой отправлен домой без вещей.`);return true;}
function siegePower(a){return cityEffects(owner(a)).siege+a.heroes.filter(h=>h.hp>0&&h.sub==='thief').length;}
function fortification(f){return f.town.walls==='stone'?7:f.town.walls==='rampart'?10:4;}
function startSiege(a,def){if(a.owner===def.id||def.dead||dist(a.pos,def.city)>1||a.mp<1||S.sieges.some(s=>s.attacker===a.id||s.defender===def.id))return false;a.mp=0;S.sieges.push({id:id('siege'),attacker:a.id,defender:def.id,progress:0,created:S.turn});if(def.id===0)TurnFlow.notice('siege','Началась осада вашей столицы',`${owner(a).name} осаждает ${CITIES[0]}. Торговля остановлена; укрепления дают время на защиту.`,'city');log(`${owner(a).name} начал осаду ${CITIES[def.id]}. До прорыва примерно ${Math.ceil(fortification(def)/siegePower(a))} ход.`);return true;}
function siegeDefenders(f){return f.armies.filter(a=>a.pos===f.city&&living(a).length).sort((a,b)=>strength(b)-strength(a))[0]||null;}
function assault(s){const a=findArmy(s.attacker),f=S.factions[s.defender];if(!a||s.progress<fortification(f))return false;return startBattle(a,siegeDefenders(f),{kind:'siege',title:`Штурм ${CITIES[f.id]}`,pos:f.city,defender:f.id,siegeId:s.id});}
function sally(s,a){const enemy=findArmy(s.attacker);if(!enemy||!a||a.owner!==s.defender||a.pos!==owner(a).city||!living(a).length)return false;return startBattle(a,enemy,{kind:'sally',title:'Вылазка из осаждённой столицы',pos:owner(a).city,defender:a.owner,siegeId:s.id});}
function cancelSieges(){for(const s of [...S.sieges]){const a=findArmy(s.attacker);if(!a||!living(a).length||dist(a.pos,S.factions[s.defender].city)>1){S.sieges=S.sieges.filter(v=>v!==s);log('Осада снята. Ущерб укреплениям не сохраняется.');}}}
function tickFaction(f){if(f.dead)return;const treasury={gold:f.gold,crystal:f.crystal},e=Capital.economy(f);f.gold+=e.gold-e.paid;f.crystal+=e.crystal;let bill=0;for(const a of f.armies)for(const h of a.heroes)bill+=Math.ceil((2+Math.floor(h.level/2))*(h.loyalty<30?1.5:h.loyalty>=75?.8:1));const paid=f.gold>=bill;f.gold=Math.max(0,f.gold-bill);if(!paid){log(`${f.name}: не хватает жалованья, верность падает.`);if(f.id===0)TurnFlow.notice('loyalty','Не хватает денег на жалованье','Верность героев снижается. Проверьте казну и расходы.','roster');}
 for(const a of [...f.armies]){a.mp=a.escort?0:5;for(const h of [...a.heroes]){h.weak=Math.max(0,h.weak-1);if(a.pos===f.city){if(h.hp>0)h.hp=Math.min(Math.floor(maxHP(h)*(h.weak?.75:1)), h.hp+8+e.heal);h.mana=C[h.cls].mana;h.stress=Math.max(0,h.stress-18);h.loyalty=clamp(h.loyalty+(paid?2:-8),0,100);}else{h.hp=Math.min(Math.floor(maxHP(h)*(h.weak?.75:1)),h.hp+3+e.heal);h.mana=Math.min(C[h.cls].mana,h.mana+2);if(!paid)h.loyalty=clamp(h.loyalty-10,0,100);}if(Relations.neglected(a,h))h.loyalty=clamp(h.loyalty-2,0,100);if(h.loyalty>=30)h.warning=null;else if(h.warning===null){h.warning=S.turn;if(f.id===0)TurnFlow.notice('loyalty',`${h.name}: угроза ухода`,'Низкая верность. Герой предупреждает об уходе через 3 хода.','roster');log(`${h.name}: низкая верность, герой предупреждает об уходе через 3 хода.`);}else if(S.turn-h.warning>=3){a.heroes=a.heroes.filter(t=>t!==h);const dest=S.factions.filter(t=>!t.dead&&t.id!==f.id).sort((a,b)=>b.rep-a.rep)[0];if(dest){let p=dest.armies.find(p=>p.pos===dest.city&&p.heroes.length<4);if(!p)p=createArmy(dest,dest.city);h.loyalty=45;h.warning=null;p.heroes.push(h);}if(f.id===0||dest?.id===0)TurnFlow.notice('loyalty',f.id===0?'Герой покинул ваш дом':'Герой присоединился к вашему дому',`${h.name}${dest?` перешёл в ${dest.name}`:' ушёл'}.`,'roster');log(`${h.name} покинул ${f.name}${dest?` и перешёл в ${dest.name}`:''}.`);}}}
 Capital.tick(f,e.prod);
 BattleRules.returns(f);


 f.town.growth+=e.food;if(f.town.population<13&&f.town.growth>=10+f.town.population*4){f.town.growth-=10+f.town.population*4;f.town.population++;if(f.town.plots.length+f.town.claims<18)f.town.claims++;if(f.id===0){log('Население столицы выросло. В городе можно присоединить клетку второго кольца.');TurnFlow.notice('growth','Население столицы выросло','В городе можно присоединить клетку второго кольца.','growth',Array.from({length:256},(_,i)=>i).find(i=>dist(f.city,i)===2&&!f.town.plots.includes(i)&&nb(i).some(j=>f.town.plots.includes(j))));}}
 if(!S.sieges.some(s=>s.defender===f.id))for(const v of S.villages)if(v.affinity[f.id]>=30&&f.gold>=3){f.gold-=3;if(v.good==='gold')f.gold+=5+(e.trade||0)+(v.favorite===f.id?2:0);else f.crystal+=v.favorite===f.id?2:1;v.trades[f.id]++;v.affinity[f.id]=Math.min(100,v.affinity[f.id]+1);if(v.trades[f.id]%3===0)f.rep++;}
 if(S.turn%5===0){refreshCandidates(f);if(f.id===0)TurnFlow.notice('heroes','Новые кандидаты на службу','В городе обновился список героев для найма.','city');}if(f.id===0)TurnFlow.notice('income','Казна в начале хода',`Золото: ${f.gold} (${f.gold-treasury.gold>=0?'+':''}${f.gold-treasury.gold}); кристаллы: ${f.crystal} (${f.crystal-treasury.crystal>=0?'+':''}${f.crystal-treasury.crystal}). Учтены доход, жалованье и торговля.`);
}
function claimPlot(f,p){if(!f.town.claims||f.town.plots.includes(p)||dist(f.city,p)!==2||!nb(p).some(i=>f.town.plots.includes(i)))return false;f.town.plots.push(p);f.town.claims--;if(f.id===0)FX.city(p,'grow','Новая городская территория');return true;}
function aiArmy(a){const f=owner(a);if(f.dead||!living(a).length||a.escort)return;const si=S.sieges.find(s=>s.attacker===a.id);if(si){if(si.progress>=fortification(S.factions[si.defender]))assault(si);return;}if(f.armies.some(t=>t!==a&&t.pos===a.pos&&living(t).length)&&a.pos!==f.city)return;
 for(const s of S.sieges.filter(s=>s.defender===f.id))if(a.pos===f.city&&strength(a)>strength(findArmy(s.attacker))*1.2){sally(s,a);return;}
 const hurt=living(a).some(h=>h.hp<maxHP(h)*.4);let target=hurt?f.city:null;
 const enemy=allArmies().filter(t=>t.owner!==f.id&&visible(f,t.pos)&&dist(a.pos,t.pos)<=3&&strength(a)>strength(t)*1.4).sort((x,y)=>dist(a.pos,x.pos)-dist(a.pos,y.pos))[0];if(!target&&enemy)target=enemy.pos;
 if(!target&&S.turn>12&&a.heroes.length===4&&living(a).every(h=>h.level>=3)){const city=S.factions.filter(t=>!t.dead&&t.id!==f.id).sort((x,y)=>dist(a.pos,x.city)-dist(a.pos,y.city))[0];if(city)target=city.city;}
 if(target===null){const jobs=[];for(const v of S.villages)if(f.seen[v.pos]&&v.affinity[f.id]<80)jobs.push({p:v.pos,n:dist(a.pos,v.pos)+2});for(let p=0;p<256;p++)if(f.seen[p]){if(cell(p).site?.type==='camp'&&!cell(p).site.cleared&&!hurt)jobs.push({p,n:dist(a.pos,p)+1});if(nb(p).some(i=>!f.seen[i])&&!cell(p).site)jobs.push({p,n:dist(a.pos,p)+4});}jobs.sort((x,y)=>x.n-y.n);target=jobs[0]?.p??f.city;}
 const foe=allArmies().find(t=>t.owner!==f.id&&living(t).length&&t.pos===target);const city=S.factions.find(t=>!t.dead&&t.id!==f.id&&t.city===target);
 if(foe&&dist(a.pos,target)<=1&&a.mp){a.mp--;startBattle(a,foe,{kind:'duel',title:'Стычка вассалов',pos:target});return;}if(city&&dist(a.pos,target)<=1){startSiege(a,city);return;}
 moveTo(a,target);if(S.battle||S.aftermath)return;const c=cell(a.pos),v=c.site?.type==='village'?S.villages[c.site.id]:null;if(v&&a.mp&&v.last[f.id]!==S.turn){v.last[f.id]=S.turn;a.mp--;if(v.threat&&strength(a)>80)startBattle(a,null,{kind:'protect',village:v.id,title:`Защита ${v.name}`,pos:a.pos});else{v.affinity[f.id]=clamp(v.affinity[f.id]+12,0,100);if(v.affinity[f.id]>=30&&!v.quest[f.id]){v.quest[f.id]=true;f.rep+=5;}if(allyVillage(v,f))v.favorite=f.id;}}else if(c.site?.type==='camp'&&!c.site.cleared&&a.mp){a.mp--;startBattle(a,null,{kind:'camp',title:'Разбойники',pos:a.pos});}else if(c.site?.type==='ruin'&&!c.site.done&&a.mp){if(c.site.guarded&&!c.site.cleared){a.mp--;startBattle(a,null,{kind:'ruin',family:c.site.family,title:'Стражи руин',pos:a.pos});return;}c.site.done=true;f.bag.push({id:id('i'),name:'Перстень советника',kind:'artifact',value:45});}}
function aiCity(f){if(f.dead)return;fulfill(f);fulfill(f,true);if(f.gold<20&&f.rep>=12&&S.dominance.leader!==f.id)requestBoon(f,'gold');if(!f.town.projects?.length){const wants=['market','workshop','farm','shrine','resurrection','forge','barracks','engineering'];for(const b of wants){if(hasBuilding(f,b))continue;const d=BUILD[b],p=d.from?Object.keys(f.town.buildings).find(p=>f.town.buildings[p]===d.from):f.town.plots.find(p=>!f.town.buildings[p]);if(p!=null&&f.gold>d.cost+35&&f.crystal>=(d.crystal||0)){queueBuilding(f,+p,b);break;}}}if(f.town.claims){const p=Array.from({length:256},(_,i)=>i).find(p=>dist(f.city,p)===2&&!f.town.plots.includes(p)&&nb(p).some(i=>f.town.plots.includes(i)));if(p!=null)claimPlot(f,p);}let a=f.armies.find(a=>a.pos===f.city&&a.heroes.length<4);if(!a&&f.gold>=55&&(!f.armies.length||f.gold>=170&&f.armies.length<2&&S.turn>10))a=createArmy(f,f.city);if(a&&f.gold>=55){const h=f.candidates.shift();if(h){f.gold-=40;h.originalOwner=f.id;a.heroes.push(h);}}for(const a of f.armies)for(const h of a.heroes){if(h.loyalty<35&&f.gold>=12){f.gold-=12;h.loyalty+=15;}const sub=availableSub(h,f)[0];if(sub&&a.pos===f.city){h.sub=sub[0];h.talent=false;h.pathPoint=true;}}if(f.morgue.length)revive(f.morgue[0].id,f);}
async function endTurn(){if(FX.busy){FX.whenIdle(endTurn);return;}if(!S||S.result||S.battle||S.aftermath||processing)return;if(!S.phase){if(!TurnFlow.check())return;TurnFlow.begin();closeModal();S.phase={tasks:S.factions.slice(1).flatMap(f=>f.armies.map(a=>a.id)),next:0};}let advanced=false;processing=true;render();await new Promise(r=>setTimeout(r,20));try{while(S.phase.next<S.phase.tasks.length&&!S.result){const a=findArmy(S.phase.tasks[S.phase.next++]);if(a)aiArmy(a);if(S.battle||S.aftermath)break;}if(!S.battle&&!S.aftermath){S.phase=null;for(const f of S.factions.slice(1))aiCity(f);S.completed++;victory();if(!S.result){S.turn++;advanced=true;cancelSieges();for(const s of S.sieges)if(S.turn>s.created)s.progress+=siegePower(findArmy(s.attacker));for(const f of S.factions)tickFaction(f);tickConvoys();cleanupArmies();const d=S.decree;if(S.turn>d.deadline){for(const f of S.factions)if(!f.dead&&!d.status[f.id].main){f.rep-=8;if(f.id===0)TurnFlow.notice('king','Указ не исполнен','Основная часть прошлого указа не сдана: −8 репутации.','king');log(`${f.name}: основная часть указа не выполнена, −8 репутации.`);}newDecree();}Relations.cleanup();}}}finally{processing=false;if(advanced)TurnFlow.finish();after();}}
function tileDetails(){const p=UI.selected,a=army(),f=player(),c=cell(p),town=S.factions.find(t=>t.city===p),seen=f.seen[p];let html=`<div class="eyebrow">Гекс ${p%N+1} : ${Math.floor(p/N)+1}</div><h3>${town?CITIES[town.id]:seen?TERRAIN[c.terrain].name:'Неизведанная земля'}</h3>`;if(town){html+=`<p class="muted">${town.dead?'Дом выбыл из борьбы за престол.':town.name}</p>`;if(town.id===0)html+=button('city','Открыть город','','','gold');else if(!town.dead&&a){const s=S.sieges.find(s=>s.defender===town.id);html+=`<p class="muted">Укрепления задержат штурм на ${fortification(town)} очков осады.</p>${s?`<div class="rule">Осада: ${s.progress}/${fortification(town)}</div>${button('assault','Штурмовать',`data-id="${s.id}"`,s.progress<fortification(town)||findArmy(s.attacker)?.owner!==0)}`:button('siege','Начать осаду',`data-id="${town.id}"`,dist(a.pos,town.city)>1||a.mp<1)}`;}}
 if(seen&&c.site?.type==='village'){const v=S.villages[c.site.id];html+=`<h3>${v.name}</h3><p class="muted">${v.good==='crystal'?'Торгует мана-кристаллами':'Торговля даёт золото'}. От 30 отношений — обычная торговля; особая дружба только с одним домом.</p>${S.factions.map(t=>`<div class="row"><small style="color:${COLORS[t.id]}">${t.name}</small><b>${v.affinity[t.id]}${v.favorite===t.id?' ★':''}</b></div>`).join('')}<p class="muted">${v.threat?'Жителям угрожают: '+(Bestiary.families[v.threatFamily||'bandits'].name)+'.':v.quest[0]?'Ваша просьба выполнена.':'Можно помочь жителям.'}</p>${button('village','Выбрать героя для разговора','',!a||a.pos!==p||a.mp<1||v.last[0]===S.turn)}${button('villageAlly','Заключить особый союз',`data-id="${v.id}"`,!a||a.pos!==p||!allyVillage(v,f))}<small>Особая дружба: просьба выполнена, отношения ≥60, преимущество ≥15.</small>`;}
 else if(seen&&c.site?.type==='camp')html+=`<h3>${Bestiary.families[Bestiary.family(p)].lair}</h3><p class="muted">${c.site.cleared?'Угроза устранена.':esc(Bestiary.describe(Bestiary.family(p)))}</p>${button('site','Атаковать логово','',!a||a.pos!==p||a.mp<1||c.site.cleared)}`;
 else if(seen&&c.site?.type==='ruin')html+=`<p class="muted">${c.site.done?'Руины исследованы.':c.site.guarded&&!c.site.cleared?'Руины охраняются. '+Bestiary.describe(c.site.family):'Здесь может быть дорогой артефакт.'}</p>${button('site','Исследовать руины','',!a||a.pos!==p||a.mp<1||c.site.done)}`;
 else if(seen&&c.site?.type==='event')html+=button('site','Исследовать событие','',!a||a.pos!==p||a.mp<1);
 const enemies=allArmies().filter(t=>t.owner!==0&&t.pos===p&&living(t).length&&visible(f,p));for(const t of enemies)html+=`<div class="card"><b style="color:${COLORS[t.owner]}">${HOUSES[t.owner]}</b><p class="muted">Героев ${t.heroes.length}, уровни: ${t.heroes.map(h=>h.level).join(', ')}.</p>${button('attack','Атаковать этот отряд',`data-id="${t.id}"`,!a||dist(a.pos,p)>1||a.mp<1)}</div>`;
 for(const q of S.convoys.filter(q=>q.pos===p&&(q.owner===0||visible(f,p))))html+=`<div class="card"><b>Повозка · ${HOUSES[q.owner]}</b><p class="muted">${q.kind==='bodies'?'Останки':q.kind==='prisoners'?'Пленники':'Освобождённые герои'}: ${q.cargo.map(h=>h.name).join(', ')}<br>${q.escort?'Есть сопровождение':'Без сопровождения'} · осталось примерно ${Math.ceil(path(q.pos,q.dest).length/2)} ход.</p>${q.owner===0?button('escort',q.escort?'Снять сопровождение':'Назначить сопровождение',`data-id="${q.id}"`,!a||!q.escort&&a.pos!==p):button('intercept','Перехватить',`data-id="${q.id}"`,!a||dist(a.pos,p)>1||a.mp<1)}</div>`;
 const bodies=S.remains.filter(r=>r.pos===p);if(bodies.length&&(seen||a?.pos===p))html+=`<div class="card"><b>Останки на поле</b><p class="muted">${bodies.map(r=>r.hero.name).join(', ')}</p>${button('sendBodies','Отправить останки в город',`data-pos="${p}"`,!a||a.pos!==p)}</div>`;
 if(a&&a.pos!==p&&!town&&!enemies.length)html+=`<div class="stack">${button('move','Идти сюда',`data-pos="${p}"`,a.mp<1||!living(a).length||!!a.escort,'gold')}</div><small>Отряд остановится у находки или встречи.</small>`;
 const own=player().armies.filter(t=>t.pos===p);if(own.length>1)html+=`<p class="muted">На гексе несколько ваших отрядов. В сражение вступает только выбранный отряд.</p>`;
 return html;}
function render(){if(!S)return;const f=player(),a=army();$('resources').innerHTML=`<div><small>Золото</small><b>${f.gold}</b></div><div><small>Мана-кристаллы</small><b>${f.crystal}</b></div><div><small>Репутация</small><b>${f.rep}</b></div><div><small>Ход</small><b>${S.turn}/${LIMIT}</b></div>`;$('nav').innerHTML=[['city','♜ Город'],['king','♛ Король'],['roster','⚔ Герои'],['villages','⌂ Деревни'],['cargo','▣ Перевозки'],['bestiary','♧ Бестиарий'],['journal','☷ Летопись']].map(([k,t])=>button(k,t,'',processing)).join('');$('sidebar').innerHTML=tileDetails();$('armies').innerHTML=f.armies.map((p,i)=>button('selectArmy',`Отряд ${i+1} · ${p.heroes.length}/4 · ${p.mp} ОХ`,`data-id="${p.id}"`,false,UI.army===p.id?'active small':'small')).join('');$('armybar').innerHTML=a?`<div class="row"><b>Отряд ${f.armies.indexOf(a)+1}</b><small>${a.escort?'Сопровождает повозку':`${a.mp} очков перемещения`} · бои отдельных отрядов</small>${a.conflict?button('conflict','Спор в отряде','','','small warn'):''}</div><div id="portraits">${a.heroes.map(h=>`<div class="portrait" data-a="hero" data-id="${h.id}"><canvas width="36" height="45" data-hero="${h.cls}"></canvas><b>${h.name}</b><small>${C[h.cls].name} · ${h.level} ур.</small><small>♥ ${h.hp} · В ${h.loyalty} · С ${h.stress}</small>${bar(h.hp,maxHP(h),'#9ec589')}</div>`).join('')}${a.heroes.length<4?'<small>Свободное место<br>Найм в городе</small>':''}</div>`:'<h3>Нет действующих отрядов</h3><p class="muted">Наймите кандидатов или дождитесь возвращения отступивших.</p>';$('phase').innerHTML=S.result?`<b>${S.result.winner===0?'Ваша победа':S.result.winner===null?'Партия завершена':HOUSES[S.result.winner]+' победил'}</b><br>${S.result.text}`:processing?'Соперники выполняют свои ходы…':`Указ действует до хода ${S.decree.deadline}.<br>${S.dominance.leader!==null?`${HOUSES[S.dominance.leader]}: превосходство ${S.dominance.held}/5`:'Путь к короне — поручения, торговля и война.'}`;const pending=TurnFlow.tasks().length;$('endTurn').textContent=pending?`Остались действия · ${pending}`:'Завершить ход →';$('endTurn').disabled=processing||!!S.result||!!S.battle||!!S.aftermath;if(!processing&&!S.result&&!S.phase)$('phase').innerHTML+=`<div class="stack">${button('turnTasks','Приказы и решения','','','small')}${S.turnFlow?.report?button('turnReport',`Сводка · ход ${S.turnFlow.report.turn}`,'','','small'):''}</div>`;Painter.draw();Painter.thumbnails();if(S.battle)renderBattle();else if(S.aftermath&&UI.modal!=='shipping')renderAftermath();else if(UI.modal==='city')renderCity();else if(UI.modal==='king')renderKing();else if(UI.modal==='roster')renderRoster();else if(UI.modal==='cargo')renderCargo();else if(UI.modal==='turnTasks')TurnFlow.openTasks();}
function cityHexes(){const f=player(),centre=f.city,ids=Array.from({length:256},(_,i)=>i).filter(i=>dist(i,centre)<=2),[cx,cy]=[centre%N,Math.floor(centre/N)],points=i=>{const x=i%N,y=Math.floor(i/N);return{x:300+(x-cx+(y%2-cy%2)/2)*86,y:260+(y-cy)*74};};let html='';const prev=UI.cityPlot!=null?buildPreview(f,UI.cityPlot,UI.building):null,links=prev?.links||[];for(const p of ids){const v=points(p),base=p===centre,own=f.town.plots.includes(p),b=f.town.buildings[p],claimable=!base&&!own&&f.town.claims>0&&nb(p).some(j=>f.town.plots.includes(j)),selected=UI.cityPlot===p,poly=Array.from({length:6},(_,j)=>`${v.x+Math.cos((j*60-30)*Math.PI/180)*48},${v.y+Math.sin((j*60-30)*Math.PI/180)*48}`).join(' ');html+=`<g class="plot" data-a="plot" data-pos="${p}"><polygon points="${poly}" fill="${base?'#716747':own?'#4c6545':claimable?'#394d39':'#25392d'}" stroke="${selected?'#f7d48a':claimable?'#abc68e':'#70805a'}" stroke-width="${selected?3:1}" ${!own&&!base?'stroke-dasharray="5 4"':''}/><text x="${v.x}" y="${v.y-3}" text-anchor="middle" fill="#ead8aa" font-size="${base?30:24}" transform="${f.town.facings?.[p]?`translate(${2*v.x} 0) scale(-1 1)`: ''}">${base?'♜':b?BUILD[b].icon:claimable?'+':own?'·':'🔒'}</text><text x="${v.x}" y="${v.y+16}" text-anchor="middle" fill="#e7dfc7" font-size="9">${base?'Ратуша '+(f.town.hall||1):b?BUILD[b].name:f.town.projects?.some(q=>q.plot===p)?BUILD[f.town.projects.find(q=>q.plot===p).id].name:claimable?'Присоединить':own?'Свободно':''}</text></g>`;}
 for(const q of f.town.projects||[]){const v=points(q.plot),percent=Math.min(100,Math.round(q.progress/q.work*100));html+=`<g class="city-scaffold" pointer-events="none"><path d="M${v.x-25} ${v.y+8}V${v.y-28}H${v.x+25}V${v.y+8} M${v.x-25} ${v.y-10}H${v.x+25}" stroke="#c6ab73" stroke-width="4" fill="none"/><rect class="scaffold-glow" x="${v.x-24}" y="${v.y-26}" width="48" height="33" fill="#d1ba8055"/><text x="${v.x}" y="${v.y+30}" text-anchor="middle" fill="#f0dcaa" font-size="10">${q.paused?"Пауза":percent+"% · работы"}</text></g>`;}
 const owned=[f.city,...f.town.plots];for(const p of owned){const v=points(p);for(let e=0;e<6;e++){const angle=e*Math.PI/3,target={x:v.x+Math.cos(angle)*86,y:v.y+Math.sin(angle)*86};const neighbor=nb(p).find(j=>{const q=points(j);return Math.hypot(q.x-target.x,q.y-target.y)<6;});if(neighbor!=null&&owned.includes(neighbor))continue;const a=angle-Math.PI/6,b=angle+Math.PI/6;html+=`<line x1="${v.x+Math.cos(a)*48}" y1="${v.y+Math.sin(a)*48}" x2="${v.x+Math.cos(b)*48}" y2="${v.y+Math.sin(b)*48}" stroke="#d5bd82" stroke-width="${f.town.walls==='palisade'?3:5}" pointer-events="none"/>`;}}
 for(const l of links){const a=points(l.p),b=points(l.j);html+=`<line x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" stroke="#e8cd78" stroke-width="3" stroke-dasharray="5 3" pointer-events="none"/><text x="${(a.x+b.x)/2}" y="${(a.y+b.y)/2-7}" fill="#ffffbe" stroke="#263426" paint-order="stroke" stroke-width="3" text-anchor="middle" font-size="11" pointer-events="none">+${l.n} ${METRIC[l.key]}</text>`;}
 return `<svg viewBox="50 55 500 410" aria-label="Карта строительства: шесть начальных клеток и второе кольцо">${html}</svg>`;}
function renderCity(){const f=player(),t=f.town,e=cityEffects(f),p=UI.cityPlot,b=BUILD[UI.building],pr=p!=null?buildPreview(f,p,UI.building):null,claimable=p!=null&&!t.plots.includes(p)&&dist(f.city,p)===2&&t.claims>0&&nb(p).some(j=>t.plots.includes(j));const siege=S.sieges.find(s=>s.defender===0);show('city',`<div class="eyebrow">Управление столицей</div><div class="row"><h2>${CITIES[0]}</h2><div>${button('hire','Найм')}${button('morgue','Воскрешение')}</div></div><div class="citylayout"><section><div class="three"><div class="card"><b>Население ${t.population}</b><small>${bar(t.growth,10+t.population*4)}Рост ${t.growth}/${10+t.population*4} · +${e.food}/ход</small></div><div class="card"><b>Производство ${e.prod}</b><br><small>Золото +${e.gold}, кристаллы +${e.crystal}/ход</small></div><div class="card"><b>${t.plots.length}/18 клеток</b><br><small>Доступно присоединений: ${t.claims}</small></div></div><div class="citymap">${cityHexes()}</div><div class="hint">Синергия действует только между непосредственными соседями. Новое население открывает одну клетку второго кольца. Показатели роста видны только здесь.</div><div class="card"><div class="row"><b>Стены: ${t.walls==='palisade'?'частокол':t.walls==='stone'?'каменные':'крепостной вал'}</b><span>${fortification(f)} укреплений</span></div><p class="muted">Стены идут по границе города и не занимают гекс. ${t.wallQueue?`Идёт восстановление: ${t.wallQueue.left} ход.`:''}</p>${button('walls',t.walls==='palisade'?'Заменить каменными · 80 золота':'Возвести крепостной вал · 120 золота','',!Capital.afford(f,Capital.project(f,f.city,'walls','walls')))}</div>${siege?`<div class="rule">Город осаждён. Торговля остановлена. Прогресс ${siege.progress}/${fortification(f)}. Поражение в вылазке означает потерю столицы.<div class="stack">${button('sally','Вылазка выбранным отрядом',`data-id="${siege.id}"`,!army()||army().pos!==f.city)}</div></div>`:''}</section><section><h3>Размещение здания</h3><select id="buildSelect" style="width:100%;padding:9px">${Object.entries(BUILD).filter(([k])=>!['hall','walls'].includes(k)&&!Capital.legacy.includes(k)).map(([k,v])=>`<option value="${k}" ${UI.building===k?'selected':''}>${v.name}${v.from?' ← '+BUILD[v.from].name:''}</option>`).join('')}</select><div class="card"><h3>${b.name}</h3><p>${b.text}</p><p class="muted">${b.from?`Можно разместить только поверх «${BUILD[b.from].name}». Все его эффекты сохраняются.`:'Строится на свободном городском гексе.'}</p><p>Цена: ${b.cost} золота${b.crystal?`, ${b.crystal} крист.`:''}. Работы: ${b.work}.</p></div>${Capital.cityPanel(f,p)}${claimable?button('claimPlot','Присоединить выбранную клетку',`data-pos="${p}"`,false,'gold'):''}<div class="card"><b>Предварительный результат</b>${p==null?'<p class="muted">Выберите клетку на карте города.</p>':!pr.ok?`<p class="danger">${pr.why}</p>`:`<p>${pr.changes.map(v=>`${v.n>0?'+':''}${v.n} ${METRIC[v.key]||v.key}`).join('<br>')}</p><h3>Соседские связи</h3>${pr.links.map(v=>`<p class="synergy">${v.text}: +${v.n} ${METRIC[v.key]}</p>`).join('')||'<p class="muted">На выбранной клетке новых синергий нет.</p>'}`}</div>${button('construct',b.from?'Заменить здание':'Начать строительство','',p==null||!pr?.ok||f.gold<b.cost||f.crystal<(b.crystal||0), 'gold')}${p!=null&&t.buildings[p]?`<div class="stack">${button('demolish','Снести выбранное здание',`data-pos="${p}"`,t.projects.some(q=>q.plot===p),'small warn')}</div><small>Герои сохраняют выданные ранги. Восстановленное здание развивается заново.</small>`:''}</section></div>`,true);}
function renderHire(){const f=player();show('hire',`<div class="eyebrow">Базовые классы не требуют построек</div><h2>Кандидаты на службу</h2><p class="muted">Цена найма: 40 золота. Герой присоединится к свободному отряду в городе или создаст новый. До четырёх героев в каждом.</p><div class="three">${f.candidates.map(h=>`<div class="card"><canvas class="heroThumb" data-hero="${h.cls}"></canvas><h3>${h.name}</h3><b>${C[h.cls].name}, ${h.level} ур.${h.sub?' · '+SUBS[h.sub].name:''}</b><p class="muted">${h.traits.map(t=>TRAITS[t].name).join(' · ')}</p>${button('recruit','Нанять',`data-id="${h.id}"`,f.gold<40||S.sieges.some(s=>s.defender===0))}</div>`).join('')}</div>`);Painter.thumbnails();}
function heroCard(h,a){const subs=availableSub(h,player()),bonds=a.heroes.filter(t=>t!==h);return `<div class="card"><canvas class="heroThumb" data-hero="${h.cls}"></canvas><h3>${h.name} · ${h.level} ур.</h3><b>${h.sub?SUBS[h.sub].name:C[h.cls].name}</b>${Talents.render(h,a)}<p>♥ ${h.hp}/${maxHP(h)} · Мана ${h.mana}/${C[h.cls].mana}<br>Верность ${h.loyalty} · Стресс ${h.stress}</p>${bar(h.loyalty)}${bar(h.stress,100,'#bf8875')}<p class="muted">Опыт ${h.xp}/${h.level*18}. ${h.weak?`Слабость ${h.weak} ход.: −2 атаки и сниженное здоровье.`:''}</p><p class="muted">${h.traits.map(t=>`${TRAITS[t].name}: ${TRAITS[t].text}`).join(' ')}</p><p class="muted">Отношения: ${bonds.map(t=>`${t.name}: ${Relations.label(h,t)}`).join(' · ')||'Других героев в отряде нет'}</p>${h.memories?.length?`<details class="relation-history"><summary>Почему изменились отношения</summary>${h.memories.slice(0,5).map(m=>`<p><small>Ход ${m.turn} · ${esc(m.name)}${m.change?' · '+(m.change>0?'+':'')+m.change:''}</small><br>${esc(m.reason)}</p>`).join('')}</details>`:''}${h.warning!==null?`<div class="hint">Угроза ухода: осталось ${Math.max(0,3-(S.turn-h.warning))} ход.</div>`:''}<p class="muted">Снаряжение: ${h.items.map(i=>i.name).join(', ')||'Нет оружия (−3 к атаке)'}</p><div class="stack">${button('bonus','Премия · 12 зол.',`data-id="${h.id}"`,player().gold<12||h.bonusTurn===S.turn)}${button('split','Отделить в новый отряд',`data-id="${h.id}"`,a.heroes.length<2||!!a.escort)}${button('equip','Выдать оружие · 10 зол.',`data-id="${h.id}"`,a.pos!==player().city||h.items.some(i=>i.kind==='weapon')||player().gold<10)}</div>${bonds.some(t=>(h.bonds[t.id]||0)<0)?button('reconcile','Разобрать конфликт',`data-id="${h.id}"`,a.mp<1):''}${h.level>=6&&!h.sub?`<div class="rule">Выбор подкласса<div class="stack">${subs.map(([k,v])=>button('subclass',v.name,`data-id="${h.id}" data-v="${k}"`,false)).join('')||'<small>Нужен второй этаж классового здания.</small>'}</div></div>`:''}${allArmies().filter(t=>t.owner===0&&t!==a&&t.heroes.length<4&&dist(a.pos,t.pos)<=1).map(t=>button('transfer',`Передать в отряд ${player().armies.indexOf(t)+1}`,`data-id="${h.id}" data-v="${t.id}"`)).join('')}</div>`;}
function renderRoster(hid=null){const a=army();if(!a){say('Наймите героев в городе.');return;}show('roster',`<div class="eyebrow">Верность, черты и отношения</div><h2>Герои выбранного отряда</h2><div class="hint">В бою отряд действует отдельно. На 5-м уровне выбирается подкласс; первое очко таланта вкладывается сразу. Верховный жрец в этой пробе доступен Жрецу с 8-го уровня при Соборе света.</div><div class="two">${a.heroes.filter(h=>!hid||h.id===hid).map(h=>heroCard(h,a)).join('')}</div>`,true);Painter.thumbnails();}
function renderKing(){const f=player(),d=S.decree,v=decreeInfo(f),st=d.status[0];show('king',`<div class="eyebrow">Один действующий указ · обязательная основа для всех</div><h2>Королевский совет</h2><div class="three">${S.factions.map(t=>`<div class="card" style="border-color:${COLORS[t.id]}"><b>${t.name}</b><h3>${t.rep} репутации</h3><small>${t.dead?'Выбыл':S.dominance.leader===t.id?`Превосходство ${S.dominance.held}/3`:'Претендент на престол'}</small></div>`).join('')}</div><div class="card"><h3>${v.title}</h3><p>${v.text}</p><p class="muted">Срок: ход ${d.deadline}. Основное +12 репутации; дополнительное +18 и 15 золота. Невыполнение основы −8; за невыполнение дополнительной части штрафа нет.</p><div class="stack">${button('decree',st.main?'Основа выполнена':'Выполнить основную часть','data-v="main"',st.main||!v.ready,'gold')}${button('decree',st.extra?'Дополнение выполнено':'Выполнить дополнение','data-v="extra"',!st.main||st.extra||!v.extra)}</div></div><h3>Блага за репутацию</h3><p class="muted">Одна просьба за ход. Расход может прервать превосходство.</p><div class="stack">${button('boon','60 золота · 12 реп.','data-v="gold"',f.rep<12||f.boonTurn===S.turn)}${button('boon','5 кристаллов · 10 реп.','data-v="crystal"',f.rep<10||f.boonTurn===S.turn)}${button('boon','Поддержка героев · 8 реп.','data-v="support"',f.rep<8||f.boonTurn===S.turn)}</div><h3>Подарки правителю</h3><div class="stack">${button('gift','30 золота · +4 реп.','data-v="gold"',f.gold<30||f.giftTurn===S.turn)}${f.bag.filter(i=>i.kind==='artifact').map(i=>button('gift',`${i.name} · +${Math.max(3,Math.round(i.value/8))} реп.`,`data-v="artifact" data-id="${i.id}"`,f.giftTurn===S.turn)).join('')}${f.armies.filter(a=>a.pos===f.city).flatMap(a=>a.heroes.filter(h=>h.level===8&&h.hp>0).map(h=>button('gift',`Передать ${h.name} королю · +22 реп.`,`data-v="hero" data-id="${h.id}"`,f.giftTurn===S.turn))).join('')}</div><p class="muted">Победа: репутация ≥60 и отрыв ≥40 на протяжении 3 полных ходов; лидерство после 60 ходов; либо захват всех чужих столиц. Числа предварительные.</p>`,true);}
function renderVillages(){show('villages',`<h2>Деревни королевства</h2><p class="muted">Обычная торговля возможна с несколькими вассалами; особая дружба — только с одним. Для смены любимого дома нужны выполненная просьба, отношения от 60 и перевес минимум 15.</p><div class="two">${S.villages.filter(v=>player().seen[v.pos]).map(v=>`<div class="card"><h3>${v.name}</h3><p>Отношения ${v.affinity[0]}/100 ${v.favorite===0?'★ Особый союз':''}</p>${bar(v.affinity[0])}<p class="muted">Сделок ${v.trades[0]}. Каждые 3 сделки дают 1 репутацию. При осаде столицы торговля прекращается.</p>${button('showHex','Показать на карте',`data-pos="${v.pos}"`)}</div>`).join('')||'<p>Исследуйте карту, чтобы найти деревни.</p>'}</div>`);}
function renderMorgue(){const f=player();show('morgue',`<div class="eyebrow">Останки и возвращение героев</div><h2>Храм восстановления</h2><p>${hasBuilding(f,'resurrection')?'Постройка готова.':'Сначала замените Святилище Храмом восстановления.'} ${highPriest(f)?'В городе есть Верховный жрец.':'Верховного жреца в городе нет.'}</p><p class="muted">Без Верховного жреца герой теряет уровень и временно слабеет; героя 1-го уровня воскресить нельзя. С Верховным жрецом уровень сохраняется и слабость меньше. Чужой герой возвращается с верностью 15.</p>${f.morgue.map(h=>{const r=reviveInfo(f,h);return `<div class="card"><h3>${h.name} · ${h.level} ур.</h3><p class="muted">${r.why}. Цена: 25 золота и 5 кристаллов.</p>${button('revive','Воскресить',`data-id="${h.id}"`,!r.ok)}</div>`;}).join('')||'<p>Доставленных останков нет. Их можно привезти с поля боя повозкой.</p>'}`);}
function renderPrison(){const f=player();show('prison',`<h2>Тюрьма</h2><p>${hasBuilding(f,'prison')?'Тюрьма построена. Число мест не ограничено.':'Для содержания пленных постройте Тюрьму.'}</p>${f.prison.map(h=>`<div class="card"><h3>${h.name}, ${h.level} ур.</h3><p class="muted">Пленник без вещей. Цена выкупа в пробе: ${30+h.level*15} золота.</p><div class="stack">${button('ransom','Предложить выкуп',`data-id="${h.id}"`)}${button('refuse','Отказать / оставить в тюрьме')}${button('releasePrisoner','Освободить без выкупа',`data-id="${h.id}"`)}</div></div>`).join('')||'<p class="muted">Пленных в городе нет.</p>'}<h3>Ваши герои в чужом плену</h3>${S.factions.slice(1).flatMap(t=>t.prison.filter(h=>(h.capturedOwner??h.originalOwner)===0).map(h=>`<div class="card"><b>${h.name} у ${t.name}</b><div class="stack">${button('ransom',`Предложить ${30+h.level*15} золота`,`data-id="${h.id}"`,f.gold<30+h.level*15)}</div></div>`)).join('')||'<p class="muted">Нет сведений о пленных.</p>'}`);}
function renderCargo(){show('cargo',`<h2>Перевозки и останки</h2><p class="muted">Повозка проходит примерно два гекса за ход. Возможны задержки и нападения разбойников. При сопровождении груз защищает только назначенный отряд.</p>${S.convoys.filter(c=>c.owner===0).map(c=>`<div class="card"><h3>${c.kind==='bodies'?'Останки':c.kind==='prisoners'?'Пленники':'Освобождённые герои'}</h3><p>${c.cargo.map(h=>h.name).join(', ')}</p><p class="muted">Осталось ${path(c.pos,c.dest).length} гексов. ${c.escort?'Сопровождается отрядом':'Без сопровождения'}</p>${button('showHex','Показать повозку',`data-pos="${c.pos}"`)}</div>`).join('')||'<p>Ваших повозок сейчас нет.</p>'}<h3>Останки на разведанной территории</h3>${S.remains.filter(r=>player().seen[r.pos]).map(r=>`<div class="card"><b>${r.hero.name}, ${r.hero.level} ур.</b><div class="stack">${button('showHex','Показать',`data-pos="${r.pos}"`)}</div></div>`).join('')||'<p class="muted">Нет обнаруженных останков.</p>'}`);}
function renderBattle(){const b=S.battle;if(!b)return;const u=b.units.find(u=>u.id===UI.battleSelected);show('battle',`<div class="eyebrow">Один отряд против одного · подкрепления не присоединяются</div><div class="row"><h2>${b.meta.title}</h2><span class="badge">${TERRAIN[Tactics.field().terrain].name} · Раунд ${b.round}</span></div><div class="battlelayout"><section><canvas id="battleCanvas" aria-label="Тактическое поле боя" tabindex="0"></canvas>${b.meta.family?`<div class="hint">${esc(Bestiary.describe(b.meta.family))}</div>`:''}<div id="battleHexInfo" class="hint" aria-live="polite">Наведите на клетку: укрытия снижают точность дальних атак; трудная местность расходует больше движения. Деревья и скалы закрывают обзор.</div><div class="card log">${b.log.slice(0,10).map(t=>`<p>${esc(t)}</p>`).join('')}</div></section><section><h3>${u?u.name:'Выберите героя'}</h3>${u?`<p>♥ ${u.hp}/${u.max} · Мана ${u.mana}<br>Стресс ${u.stress} · Действий ${u.ap}<br>Броня: ${u.physicalArmor??Math.max(0,(u.slash||10)-10)*3}%<br>Урон ${u.damage.toLocaleString('ru-RU')} · Дальность ${u.range}<br>Уклонение ${Math.round(BattleRules.baseDodge(u)*100)}%${u.cls==='warrior'?` · Блок ${Math.round(Strike.blockChance(u.cls,true,u.guardBlock)*100)}%`:''}</p><p class="muted">${u.surrender?'Герой сдался и не действует.':`Движение: 3 шага за ОД. После атаки движение недоступно.`}</p><div class="stack">${Tips.button('bSkill',u.cls==='acolyte'?'Медитация':u.cls==='warrior'?'Мощный удар':'Особая атака','',b.over!==null||u.ap<1||u.surrender||(u.cls==='warrior'?(!u.talents?.power||u.powerRound===b.round):u.used&&u.cls!=='acolyte'),u,'skill')}${Tips.button('bGuard','Оборона · 1 ОД','',b.over!==null||u.ap<1||u.hp<=0||u.surrender||u.guard,u,'guard')}${Relations.friends(u).length?Tips.button('bSupport','Прикрыть друга · 1 ОД','',b.over!==null||u.ap<1||u.surrender||!Relations.friends(u).some(t=>dist(u.pos,t.pos,8)<=1&&!t.friendCover&&!(b.supported||[]).includes([u.id,t.id].sort().join(':'))),u,'support'):''}</div>${u.cls==='acolyte'?`<div class="stack">${Object.entries(SPELLS).map(([k,s])=>Tips.button('bSpell',`${s.name} · ${s.cost}`,`data-v="${k}"`,b.over!==null||u.ap<1||u.mana<s.cost||u.surrender,u,k)).join('')}</div>`:''}`:'<p class="muted">Союзники отмечены зелёным, противники красным. Выберите героя, затем цель или клетку движения.</p>'}${UI.mode==='spell'?`<p class="synergy">${SPELLS[UI.spell].name}: выберите цель.</p>`:UI.mode==='support'?'<p class="synergy">Выберите друга на соседней клетке для прикрытия.</p>':''}${u&&Relations.rivalBonus(u)?'<p class="synergy">Соперничество: +1 к урону, пока соперник в строю.</p>':''}<div class="stack">${b.over!==null?button('bFinish',b.over===b.human?'Принять победу':'Принять поражение','','','gold'):`${button('bEnd','Завершить раунд','','','gold')}${button('bAuto','Завершить автобоем')}${button('bRetreat','Отступить выбранным героем','',!u||b.meta.kind==='dungeon')}`}</div><p class="muted">Уклонение отменяет удар. Блок вдвое снижает физический урон после брони. Крит: 10% при попадании, ×1,5 до защиты. Лечение поднимает упавшего с одним действием. При победе все свои упавшие возвращаются с 1 ХП.</p></section></div>`,true);Painter.battle();}
function renderBestiary(){show('bestiary',`<div class="eyebrow">Существа королевства</div><h2>Бестиарий</h2><p>Повадки и места обитания помогают подготовить отряд к встрече.</p><div class="three">${Object.entries(Bestiary.families).map(([key,f])=>`<div class="card"><canvas class="heroThumb" data-monster="${f.pack[0]}"></canvas><h3>${f.name}</h3><p class="muted">${f.habitats.map(k=>TERRAIN[k].name).join(' · ')}<br>Угроза: ${f.danger}</p>${f.pack.map(k=>`<p><b>${Bestiary.species[k].name}</b><br><small>${Bestiary.species[k].text}</small></p>`).join('')}</div>`).join('')}</div>`,true);Painter.monsterThumbnails();}
function help(){show('help',`<h2>Как играть</h2><p class="muted">Анимации показывают уже определённые результаты. Скорость 1×, 2× и 4×, отключение и подробность автобоя — в меню «Анимации». Пробел пропускает показ.</p><div class="rule"><b>Начало и конец хода</b><p>В начале хода появляется общая сводка изменений: указы, постройки, события и повозки. Перед завершением хода примите оставшиеся решения или явно пропустите их на этот ход. Без денег или допустимого места строительство не блокирует ход.</p></div><div class="rule"><b>Ландшафт боя</b><p>Деревья и скалы непроходимы и закрывают обзор; глубокая вода непроходима, но не закрывает обзор. Укрытие повышает шанс уклонения от дальних атак. Грязь, осыпи и мелководье требуют 2 очка движения, топь — 3. Возвышенность даёт +1 к дальним атакам по целям ниже. Наведите на клетку или способность для объяснения.</p></div><ol><li>Выберите двух кандидатов. Каждый отряд вмещает до четырёх героев. Отряды можно разделять и передавать героев между соседними отрядами; совместных боёв нет.</li><li>Нажмите гекс, затем «Идти сюда». Перетаскивайте карту и меняйте масштаб колесом. Выбранный отряд показан внизу, действия — справа, ресурсы — сверху.</li><li>Откройте город. Разместите здание на одном из шести соседних гексов. До подтверждения видны бонусы непосредственного соседства. Замены разрешены только поверх указанного здания; прежние эффекты сохраняются.</li><li>Население открывает клетки второго кольца, всего до 18 мест. Стены идут по границе города, не занимая гекс. Рост и производство отображаются только внутри города.</li><li>В событиях выбирайте героя: черты влияют на проверки и отношение товарищей к поступку. Отношения взаимные; причина изменений доступна в карточке героя. Споры возникают из поступков. Примиряйте проверкой навыка или компенсацией 20 золота; каждый вариант стоит 1 очко перемещения. Игнорирование уже возникшего спора снижает верность после трёх ходов.</li><li>Спасение товарища без сознания даёт +2 доверия один раз на пару за бой. При доверии от +2 доступно ручное прикрытие друга: 1 ОД, +2 КБ соседнему другу, одна активация на пару за бой. Общее храброе выступление может создать соперничество: +1 к урону, пока соперник в строю.</li><li>В мире есть волки, пауки, гоблины, кобольды, нежить, огры, вепри и разбойники. Перед нападением на разведанное логово прочитайте угрозу справа. Некоторые руины охраняются: победите стражей, затем исследуйте руины. Бестиарий слева описывает повадки.</li><li>Сдавайте основную часть королевского указа до срока. Дополнительная часть даёт награду без штрафа за отказ. Репутацию можно тратить на блага.</li><li>От 30 отношений деревни торгуют с вами. Особый союз доступен одному дому: просьба выполнена, отношения от 60 и перевес 15.</li><li>Для захвата столицы нужна осада на карте. Стены дают время защитнику. При проигранной вылазке столица захвачена. Уход нападающих полностью прекращает осаду.</li><li>Герою с 0 ХП можно помочь лечением в течение трёх его собственных ходов. Победитель нанимает или казнит недееспособных противников. Экипировка погибших попадает в общую добычу.</li><li>Повозки с останками можно сопровождать и перехватывать. Отступивший в бою герой возвращается в столицу через три глобальных хода.</li><li>Храм восстановления воскрешает доставленное тело с потерей уровня и временной слабостью. Героя 1-го уровня без Верховного жреца воскресить нельзя. С Верховным жрецом в городе уровень сохраняется, слабость меньше.</li></ol><div class="hint">Пробные параметры: уровни 1–8, выбор подкласса с 6-го уровня при наличии второго этажа классового здания. Список зданий, стоимость, сроки, формулы стресса и репутации временные. Вещи представлены простым списком: полная система слотов пока не восстановлена.</div><p class="muted">Победа: репутация ≥60 и единоличное лидерство пять полных ходов; лидерство после 60 ходов; или захват всех столиц. Потеря своей столицы — немедленное поражение. Экспортируйте сохранения и исходники: публикация среды не выполняется автоматически.</p>`,true);}
function handle(el){const a=el.dataset.a;if(a==='animationSettings'){FX.openSettings();return;}if(FX.busy&&!['export','zoom','grid'].includes(a))return;const k=el.dataset.v,i=el.dataset.id,p=+el.dataset.pos;if(a==='close'){if(UI.modal==='turnReport'){TurnFlow.dismiss();return;}if(S?.aftermath)renderAftermath();else closeModal();return;}if(a==='help'){help();return;}if(a==='new'){show('new',`<h2>Начать новую партию?</h2><p>Перед новой партией экспортируйте текущее сохранение, если хотите его оставить.</p>${button('start','Выбрать двух кандидатов','','','gold')}`);return;}if(a==='start'){beginStart();return;}if(a==='continue'){load();return;}if(a==='pickStart'){if(UI.chosen.includes(i))UI.chosen=UI.chosen.filter(v=>v!==i);else if(UI.chosen.length<2)UI.chosen.push(i);renderStart();return;}if(a==='confirmStart'){if(UI.chosen.length===2)newGame(Date.now(),UI.startPool.filter(h=>UI.chosen.includes(h.id)));return;}if(a==='import'){$('file').click();return;}if(!S)return;if(a==='export'){save();exportSave();return;}if(a==='zoom'){Painter.control(k);return;}if(a==='grid'){Painter.grid();return;}if(a==='showHex'){closeModal();UI.selected=p;Painter.focus(p);render();return;}if(a==='selectArmy'){UI.army=i;UI.selected=army().pos;Painter.home();render();return;}
 if(S.battle){const b=S.battle,u=b.units.find(v=>v.id===UI.battleSelected);if(a==='bFinish'){finishBattle();return;}if(b.over!==null)return;if(a==='bAuto'){autoBattle();renderBattle();after();return;}if(a==='bRetreat'){if(!BattleRules.flee(u))say('Выберите героя на краю поля. Из подземелья отступить нельзя.');renderBattle();after();return;}if(a==='bEnd'){endBattleTurn();return;}if(a==='bSupport'&&u){UI.mode='support';renderBattle();return;}if(a==='bSpell'&&u){UI.mode='spell';UI.spell=k;renderBattle();return;}if(a==='bSkill'&&u){skillBattle(u);renderBattle();after();return;}if(a==='bGuard'&&u?.side===b.human&&b.side===b.human&&u.hp>0&&u.ap>0&&!u.guard&&!u.surrender&&!u.retreated){
   u.guard=true;u.guardBlock=u.cls==='warrior';u.ap--;
   FX.effect('guard',u.pos,u.pos,{label:'Оборона'});renderBattle();after();
 }return;}
 if(processing&&!S.aftermath||S.result&&!S.aftermath)return;if(!S.aftermath&&TurnFlow.dispatch(a,i,p))return;
 if(a.startsWith('aftermath')){
  const m=S.aftermath;if(!m)return;
  if(a==='aftermathBodies'){if(m.corpses.length)bodyShipping(m.pos,m.corpses,true);return;}
  if(a==='aftermathLeave')m.corpses=[];
  if(a==='aftermathFate'){const h=m.eligible.find(h=>h.id===i);if(h)BattleRules.fate(m,h,k==='hire');}
  if(a==='aftermathRecipient')UI.lootHero=i;
  if(a==='aftermathLoot'){const index=m.loot.findIndex(item=>item.id===i);if(index>=0){const h=lootRecipient(m,m.loot[index]);if(h)h.items.push(m.loot.splice(index,1)[0]);}}
  if(a==='aftermathDone'&&!m.eligible.length){
    BattleRules.stash(m);S.aftermath=null;closeModal();after();
    if(S.phase)FX.whenIdle(()=>setTimeout(endTurn,30));
    return;
  }
  renderAftermath();after();return;
 }
 if(a==='confirmShipping'){const q=UI.shipping;if(q&&dispatchBodies(player(),q.pos,q.ids)){if(q.fromAftermath&&S.aftermath)S.aftermath.corpses=[];UI.shipping=null;if(S.aftermath)renderAftermath();else closeModal();after();}return;}
 if(S.aftermath)return;
 if(a==='end'){endTurn();return;}if(a==='city'){UI.cityPlot=UI.cityPlot??player().town.plots[0];renderCity();return;}if(a==='plot'){UI.cityPlot=p;renderCity();return;}if(a==='construct'){queueBuilding(player(),UI.cityPlot,UI.building);save();renderCity();return;}if(a.startsWith('capital')||a==='classBuy'){if(processing||S.result)return;const f=player();if(a==='capitalEdit')Capital.edit(f,p,k);if(a==='capitalMirror')UI.cityMirror=!UI.cityMirror;if(a==='capitalHall')Capital.enqueue(f,f.city,'hall','hall');if(a==='capitalFloor')Capital.enqueue(f,p,f.town.buildings[p],'floor');if(a==='classBuy')Capital.buy(f,i,k);save();renderCity();return;}if(a==='claimPlot'){claimPlot(player(),p);after();return;}if(a==='demolish'){Capital.demolish(player(),p);save();renderCity();return;}if(a==='walls'){const f=player();Capital.enqueue(f,f.city,'walls','walls');save();renderCity();return;}
 if(a.startsWith('talent')){const z=army(),h=z?.heroes.find(h=>h.id===i);if(!h)return;if(a==='talentChoose')Talents.choose(h,p,k);if(a==='talentReset')Talents.reset(h,player(),z);if(a==='talentPower'&&h.cls==='warrior'&&z.pos===player().city){const t=Talents.data(h);t.active=t.active.includes('power')?[]:['power'];}save();renderRoster(i);$('modal').querySelector('details')?.setAttribute('open','');return;}if(a==='hire'){renderHire();return;}if(a==='recruit'){hire(i);renderHire();after();return;}if(a==='roster'){renderRoster();return;}if(a==='hero'){renderRoster(i);return;}if(a==='split'){splitHero(i);return;}if(a==='transfer'){transferHero(i,k);renderRoster();after();return;}if(a==='subclass'){chooseSub(i,k);save();renderRoster(i);return;}if(a==='bonus'){const h=army()?.heroes.find(h=>h.id===i);if(h&&h.bonusTurn!==S.turn&&pay(player(),12)){h.bonusTurn=S.turn;h.loyalty=clamp(h.loyalty+14+(hasTrait(h,'greedy')?5:0),0,100);if(h.loyalty>=30)h.warning=null;Relations.observe(army(),h,'bonus');}after();return;}if(a==='equip'){const h=army()?.heroes.find(h=>h.id===i);if(h&&army().pos===player().city&&!h.items.some(i=>i.kind==='weapon')&&pay(player(),10))h.items.push({id:id('i'),kind:'weapon',name:'Походное оружие',value:10});after();return;}
 if(a==='village'){openEvent('village',army().pos);return;}if(a==='eventHero'){UI.eventHero=i;renderEvent();return;}if(a==='eventChoice'){eventChoice(k);return;}if(a==='conflict'||a==='reconcile'){const z=army();if(z&&Relations.request(z,i))openEvent('conflict',z.pos,{...z.conflict});return;}if(a==='villageAlly'){const v=S.villages[+i];if(allyVillage(v,player())){v.favorite=0;log(`${v.name} выбрала Дом Янтаря особым союзником.`);}after();return;}if(a==='site'){exploreSite();return;}if(a==='move'){moveTo(army(),p);cancelSieges();return;}if(a==='attack'){const z=army(),t=findArmy(i);if(z&&t&&t.owner!==0&&dist(z.pos,t.pos)<=1&&z.mp>0){z.mp--;startBattle(z,t,{kind:'duel',title:`Стычка с ${HOUSES[t.owner]}`,pos:t.pos});}after();return;}
 if(a==='king'){renderKing();return;}if(a==='decree'){fulfill(player(),k==='extra');after();return;}if(a==='boon'){requestBoon(player(),k);after();return;}if(a==='gift'){giftKing(k,i);after();return;}if(a==='bestiary'){renderBestiary();return;}if(a==='villages'){renderVillages();return;}if(a==='cargo'){renderCargo();return;}if(a==='morgue'){renderMorgue();return;}if(a==='revive'){revive(i);renderMorgue();after();return;}if(a==='releasePrisoner'){const f=player(),h=f.prison.find(h=>h.id===i);if(h){f.prison=f.prison.filter(v=>v!==h);const o=S.factions[h.capturedOwner??h.originalOwner];makeConvoy(o,f.city,'released',[h],o.city);}renderPrison();after();return;}if(a==='sendBodies'){bodyShipping(p,S.remains.filter(r=>r.pos===p).map(r=>r.id));return;}if(a==='escort'){const c=S.convoys.find(c=>c.id===i);if(c?.escort)stopEscort(findArmy(c.escort));else escortConvoy(i,UI.army);after();return;}if(a==='intercept'){intercept(i,army());after();return;}if(a==='siege'){startSiege(army(),S.factions[+i]);after();return;}if(a==='assault'){const s=S.sieges.find(s=>s.id===i);if(s)assault(s);after();return;}if(a==='sally'){const s=S.sieges.find(s=>s.id===i);if(s)sally(s,army());after();return;}if(a==='journal'){show('journal',`<h2>Летопись</h2>${S.log.map(v=>`<div class="card"><small>Ход ${v.turn}</small><p>${esc(v.text)}</p></div>`).join('')}`);return;}}
document.addEventListener('click',e=>{const el=e.target.closest('[data-a]');if(el&&!el.disabled)handle(el);});
document.addEventListener('change',e=>{if(e.target.id==='buildSelect'){UI.building=e.target.value;renderCity();}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&UI.modal&&!['battle','aftermath','start'].includes(UI.modal)){if(UI.modal==='turnReport')TurnFlow.dismiss();else closeModal();}});
$('file').addEventListener('change',async e=>{const f=e.target.files[0];if(!f)return;try{if(f.size>3e6)throw Error('Файл слишком большой');const d=JSON.parse(await f.text());load(d);}catch(err){say(err.message);}e.target.value='';});
function boot(){let saved=false;try{saved=!!localStorage.getItem(SAVE);}catch{}show('intro',`<div class="eyebrow">Туман и кости · пересборка по согласованным правилам</div><h2 class="introtitle">Чью клятву<br>запомнит король?</h2><p>Четыре вассала соперничают за престол. У каждого одна столица и несколько небольших отрядов. Выберите двух героев, исполняйте указы, стройте город и берегите своих людей.</p><div class="three"><div class="rule"><b>Город из гексов</b><p class="muted">Соседские синергии и осмысленные замены зданий. Стены по границе города.</p></div><div class="rule"><b>Отряды по четыре</b><p class="muted">Кандидаты с чертами, события, отношения, верность и стресс.</p></div><div class="rule"><b>Судьба героев</b><p class="muted">Осады, трофеи, останки и повозки с сопровождением.</p></div></div><div class="stack">${button('start','Выбрать первых героев','','','gold')}${button('continue','Продолжить','',!saved)}${button('help','Правила')}<button onclick="document.getElementById('openBattleLab').click()">Пробный бой 4 на 4</button></div><p class="screenOnly">Автономная пробная сборка 0.8.8. Анимации можно ускорить или отключить. Публикация среды не выполняется. Сохранения 0.3 имеют другой формат. Кнопка «Копия игры» сохраняет автономный HTML. «Экспорт» сохраняет партию отдельно.</p>`,true);}
window.Game={get state(){return S;},get ui(){return UI;},newGame,createHero,createArmy,cityEffects,buildPreview,queueBuilding,claimPlot,hasBuilding,newDecree,fulfill,requestBoon,moveTo,startBattle,autoBattle,finishBattle,spellBattle,attackBattle,stressUnit,clickBattle,endBattleTurn,activeUnits,dispatchBodies,dispatchCaptives,escortConvoy,intercept,tickConvoys,revive,reviveInfo,highPriest,startSiege,assault,sally,cancelSieges,tickFaction,endTurn,save,load,render,renderCity,renderKing,renderMorgue,renderPrison,renderRoster,openEvent,splitHero,transferHero,chooseSub,after,closeModal,bodyShipping,makeConvoy,createHero,nb,dist,fortification,checkVictory:victory,get painter(){return Painter;},get fx(){return FX;},get turns(){return TurnFlow;},get tactics(){return Tactics;},get relations(){return Relations;},get bestiary(){return Bestiary;},battleReach,moveBattle};
queueMicrotask(boot);

```

### `src/bestiary.js`

```js
// Familiar fantasy creatures, with original prototype statistics for this game.
const Bestiary=(()=>{
 const species={
  bandit:{name:'Разбойник',hp:24,ac:12,pierce:13,slash:13,atk:6,damage:6.5,range:1,speed:3,look:'bandit',text:'Боец ближнего боя.'},
  banditArcher:{name:'Разбойник-стрелок',hp:22,ac:12,pierce:13,slash:12,atk:6,damage:6.5,range:4,speed:3,look:'bandit',text:'Стреляет с четырёх гексов.'},
  wolf:{dodge:.10,name:'Волк',hp:22,ac:12,pierce:12,slash:12,atk:6,damage:6.5,range:1,speed:4,look:'wolf',text:'Стая: цели сложнее уклониться, если ещё один волк стоит рядом.'},
  spider:{dodge:.10,name:'Гигантский паук',hp:27,ac:13,pierce:13,slash:12,atk:6,damage:6.5,range:1,speed:3,look:'spider',text:'Попадание опутывает: −1 к движению до конца следующего раунда.'},
  spinner:{name:'Паук-плетельщик',hp:20,ac:12,pierce:12,slash:11,atk:6,damage:4.5,range:3,speed:3,look:'spider',text:'Стреляет липкой паутиной с трёх гексов; попадание замедляет.'},
  goblin:{dodge:.15,name:'Гоблин',hp:20,ac:13,pierce:13,slash:12,atk:6,damage:5.5,range:1,speed:4,look:'goblin',text:'Маленькая цель: дополнительно уклоняется от дальних атак в укрытии.'},
  goblinArcher:{dodge:.15,name:'Гоблин-лучник',hp:18,ac:13,pierce:13,slash:12,atk:6,damage:5.5,range:4,speed:4,look:'goblin',text:'Подвижный стрелок; лучше уклоняется от дальних атак в укрытии.'},
  kobold:{name:'Кобольд-копейщик',hp:23,ac:12,pierce:14,slash:12,atk:6,damage:6.5,range:1,speed:3,look:'kobold',text:'Защищён от колющих атак.'},
  slinger:{name:'Кобольд-пращник',hp:20,ac:12,pierce:13,slash:11,atk:6,damage:5.5,range:3,speed:4,look:'kobold',text:'Быстрый стрелок с пращой.'},
  skeleton:{name:'Скелет',hp:25,ac:12,pierce:16,slash:11,atk:6,damage:6.5,range:1,speed:3,look:'skeleton',text:'Кости трудно пробить стрелами: высокая защита от колющего урона.'},
  zombie:{name:'Зомби',hp:40,ac:10,pierce:10,slash:10,atk:5,damage:7.5,range:1,speed:1,look:'zombie',text:'Медленный, но живучий. Нежить не проходит проверки стресса.'},
  ogre:{name:'Огр',hp:72,ac:11,pierce:12,slash:11,atk:7,damage:10.5,range:1,speed:2,look:'ogre',level:2,text:'Опасный противник с большим запасом здоровья и тяжёлой дубиной.'},
  boar:{name:'Дикий вепрь',hp:35,ac:12,pierce:12,slash:12,atk:6,damage:7.5,range:1,speed:3,look:'boar',text:'Наскок: +2 урона, если перед атакой двигался в этом раунде.'}
 };
 const families={
  bandits:{name:'Разбойники',lair:'Разбойничий лагерь',habitats:['plain','hill','river'],pack:['bandit','banditArcher'],danger:'Умеренная',color:'#bc9572'},
  wolves:{name:'Волчья стая',lair:'Волчье логово',habitats:['forest','plain'],pack:['wolf'],danger:'Умеренная',color:'#b4bcb3'},
  spiders:{name:'Гигантские пауки',lair:'Паучье гнездо',habitats:['forest','swamp'],pack:['spider','spinner'],danger:'Умеренная',color:'#b9a08a'},
  goblins:{name:'Гоблины',lair:'Гоблинский стан',habitats:['forest','hill'],pack:['goblin','goblinArcher'],danger:'Умеренная',color:'#b5c27d'},
  kobolds:{name:'Кобольды',lair:'Кобольдовы норы',habitats:['hill','mountain'],pack:['kobold','slinger'],danger:'Умеренная',color:'#d0a47a'},
  undead:{name:'Нежить',lair:'Заброшенный склеп',habitats:['swamp','hill','mountain'],pack:['skeleton','zombie'],danger:'Повышенная',color:'#d2cdb1'},
  ogres:{name:'Огры',lair:'Стоянка огров',habitats:['hill','mountain'],pack:['ogre'],danger:'Высокая',color:'#bdac83'},
  boars:{name:'Дикие вепри',lair:'Лежбище вепрей',habitats:['forest','river','swamp'],pack:['boar'],danger:'Повышенная',color:'#c0aa93'}
 };
 function hash(n){let z=Math.imul(n+31,374761393)^(S.seed||1);z=Math.imul(z^(z>>>13),1274126177);return(z^(z>>>16))>>>0;}
 function choose(pos,ambush=false){const biome=cell(pos).terrain,keys=Object.keys(families).filter(k=>families[k].habitats.includes(biome)&&(!ambush||!['ogres','boars'].includes(k)));return keys[hash(pos)%keys.length]||'bandits';}
 function family(pos){const site=cell(pos).site;return families[site?.family]?site.family:'bandits';}
 function populate(){for(let p=0;p<256;p++){const s=cell(p).site;if(s?.type==='camp')s.family=choose(p);if(s?.type==='ruin'&&hash(p)%3===0){s.family=hash(p)%2?'undead':'spiders';s.guarded=true;s.cleared=false;}}
  for(const [key,f]of Object.entries(families)){if(S.map.some(c=>c.site?.type==='camp'&&c.site.family===key))continue;const positions=Array.from({length:256},(_,i)=>i).filter(p=>!cell(p).site&&f.habitats.includes(cell(p).terrain)&&S.factions.every(t=>dist(t.city,p)>=3)).sort((a,b)=>hash(a)-hash(b));const p=positions[0];if(p!=null){cell(p).site={type:'camp',family:key,cleared:false};cell(p).searched=true;}}
  for(const v of S.villages){const near=nb(v.pos)[hash(v.pos)%nb(v.pos).length];v.threatFamily=choose(near,true);}
 }
 function upgrade(){for(let p=0;p<256;p++){const s=cell(p).site;if(s?.type==='camp'&&!s.family)s.family=S.battle?.meta.pos===p&&!S.battle.units.some(u=>u.monster)?'bandits':choose(p);}for(const v of S.villages)if(!v.threatFamily){const near=nb(v.pos)[hash(v.pos)%nb(v.pos).length];v.threatFamily=choose(near,true);}}
 function create(a,meta,of){const count=of?4:Math.min(4,Math.max(2,a.heroes.length));if(of)return Array.from({length:count},(_,i)=>({id:id('u'),name:'Страж крепости',side:1,pos:(i+1)*8+6,hp:34,max:34,pierce:16,slash:17,ac:15,atk:8,damage:6.5,range:i===count-1?4:1,speed:3,ap:2,mana:0,stress:0,level:1,surrender:false,resolveChecked:false}));
  const key=families[meta.family]?meta.family:meta.kind==='protect'?S.villages[meta.village].threatFamily||'bandits':meta.kind==='ambush'?choose(meta.pos??a.pos,true):family(meta.pos??a.pos),f=families[key];meta.family=key;if(['Засада','Разбойники','Лагерь разбойников'].includes(meta.title))meta.title=f.name+(meta.kind==='ambush'?' — засада':'');const n=key==='ogres'?(count<=2?1:2):key==='boars'?2:count;
  return Array.from({length:n},(_,i)=>{const k=f.pack[i%f.pack.length],d=species[k];return{id:id('u'),name:d.name,monster:k,side:1,pos:(i+1)*8+6,hp:d.hp,max:d.hp,pierce:d.pierce,slash:d.slash,ac:d.ac,atk:d.atk,damage:d.damage,range:d.range,speed:d.speed,ap:2,mana:0,stress:0,level:d.level||1,surrender:false,resolveChecked:false};});
 }
 function attackBonus(u,t){return u.monster==='wolf'&&activeUnits(S.battle,u.side).some(z=>z!==u&&z.monster==='wolf'&&dist(z.pos,t.pos,8)<=1)?2:0;}
 function damageBonus(u){return u.monster==='boar'&&u.movedRound===S.battle.round?2:0;}
 function onHit(u,t){if(['spider','spinner'].includes(u.monster)&&t.hp>0){t.snaredUntil=S.battle.round+1;S.battle.log.unshift(`${t.name} опутан паутиной: движение −1 до конца следующего раунда.`);FX.effect('curse',u.pos,t.pos,{label:'Липкая паутина',text:'Движение −1'});}}
 function speed(u){return Math.max(1,u.speed-(u.snaredUntil>=S.battle.round?1:0));}
 function describe(key){const f=families[key]||families.bandits;return `${f.name}. Угроза: ${f.danger.toLowerCase()}. ${f.pack.map(k=>species[k].name+': '+species[k].text).join(' ')}`;}
 return{species,families,hash,choose,family,populate,upgrade,create,attackBonus,damageBonus,onHit,speed,describe};
})();

```

### `src/development.js`

```js
// City research and production. Values are prototype tuning parameters.
const Development=(()=>{
 const baseSpells=['bolt','heal','ward','curse'];
 const definitions={
 smithy:{name:'Кузня',cost:35,work:14,icon:'⚒',effects:{craft:1},text:'Создаёт оружие и снаряжение. Базовые классы доступны без неё.'},
 library:{name:'Библиотека',cost:35,work:14,icon:'▤',effects:{knowledge:4},text:'Знания для изучения заклинаний.'},
 plaza:{name:'Плац',cost:35,work:14,icon:'⚔',effects:{trainWarrior:1},text:'Кандидаты-воины на один уровень выше. Повторы бонус не суммируют.'},
 academy:{name:'Академия',requires:['library'],cost:45,work:18,icon:'▥',effects:{knowledge:3},text:'Дополнительный приток знаний. Необязательная постройка.'},
 laboratory:{name:'Лаборатория',requires:['library'],cost:40,work:16,icon:'⚗',effects:{knowledge:2,potions:1},text:'Знания и простые зелья.'},
 tower:{name:'Башня мага',requires:['library'],cost:50,crystal:2,work:18,icon:'♜',effects:{research:1},text:'Послушник в городе исследует заклинания для общего репертуара.'},
 magicforge:{name:'Магическая кузница',from:'smithy',requires:['tower'],cost:55,crystal:3,work:20,icon:'⚒',effects:{magicCraft:1},text:'Сохраняет Кузню. Магическое свойство добавляется при изготовлении.'},
 enchanting:{name:'Библиотека зачарований',from:'library',requires:['tower'],cost:55,crystal:3,work:20,icon:'✧',effects:{enchant:1},text:'Сохраняет Библиотеку. Зачаровывает готовые вещи и создаёт свитки известных заклинаний.'},
 magicacademy:{name:'Магическая академия',requires:['tower'],requiresAny:['library','academy'],cost:45,work:18,icon:'✦',effects:{trainAcolyte:1},text:'Кандидаты-послушники на один уровень выше.'},
 alchemy:{name:'Алхимическая лаборатория',from:'laboratory',requires:['tower'],cost:55,crystal:3,work:20,icon:'⚗',effects:{advancedPotions:1},text:'Сохраняет Лабораторию. Продвинутые зелья и алхимические свойства предметов.'},
 power:{name:'Место силы',requires:['tower'],cost:50,crystal:3,work:18,icon:'✦',effects:{elementalist:1},text:'Открывает стихийника и стихийные исследования. Соседние магические производства тратят на 1 кристалл меньше.'},
 temple:{name:'Храм',requires:['tower'],excludes:['kapish','cult'],cost:50,crystal:2,work:18,icon:'✝',effects:{priest:1},text:'Жречество и святая магия. Несовместим с Капищем. Обычное воскрешение остаётся отдельной постройкой.'},
 kapish:{name:'Капище',requires:['tower'],excludes:['temple','light'],cost:50,crystal:2,work:18,icon:'✦',effects:{cultist:1},text:'Оккультизм и тёмная магия. Несовместимо с Храмом.'},
 cathedral08:{name:'Верховный храм',from:'temple',requires:['tower'],excludes:['kapish','cult'],cost:75,crystal:5,work:26,icon:'♜',effects:{highpriest:1,paladin:1},text:'Сохраняет Храм; открывает обучение Верховного жреца и Паладина по прежним требованиям уровня.'}
 };
 Object.assign(BUILD,definitions);BUILD.forge.name='Военная кузница';BUILD.range.name='Стрельбище';BUILD.range.effects.trainArcher=1;BUILD.range.text+=' Кандидаты-лучники на один уровень выше.';BUILD.den.name='Слесарная мастерская';BUILD.den.effects.trainRogue=1;BUILD.den.text+=' Кандидаты-плуты на один уровень выше.';
 Object.assign(METRIC,{knowledge:'знания',craft:'изготовление снаряжения',research:'исследования',potions:'простые зелья',advancedPotions:'продвинутые зелья',magicCraft:'магическое производство',enchant:'зачарование',magicSaving:'скидка соседям',trainWarrior:'уровень найма воина',trainArcher:'уровень найма лучника',trainRogue:'уровень найма плута',trainAcolyte:'уровень найма послушника'});
 for(const b of ['tower','magicforge','enchanting','laboratory','alchemy'])SYN.push({a:'power',b,key:'magicSaving',n:1,text:'Место силы: скидка соседнему производству'});
 const studies={barrier:{name:'Крепкий оберег',knowledge:10,turns:2,school:'research',cost:3,target:'ally',text:'+4 КБ союзнику до конца следующего раунда.'},fire:{name:'Пламя',knowledge:16,turns:2,school:'elementalist',cost:4,target:'enemy',text:'Магическая атака с дополнительными 4 урона.'},frost:{name:'Ледяной болт',knowledge:18,turns:2,school:'elementalist',cost:4,target:'enemy',text:'Магическая атака и замедление на 1 до конца следующего раунда.'},renewal:{name:'Исцеление духа',knowledge:16,turns:2,school:'priest',cost:4,target:'ally',text:'Восстанавливает 18 ХП и снимает 15 стресса.'},drain:{name:'Похищение жизни',knowledge:18,turns:3,school:'cultist',cost:4,target:'enemy',text:'Магическая атака, половина нанесённого урона возвращается здоровьем.'}};
 for(const [k,d]of Object.entries(studies))SPELLS[k]={name:d.name,cost:d.cost,target:d.target};
 const recipes={sword:{name:'Стальное оружие',building:'smithy',gold:20,crystal:0,work:8,kind:'weapon',attack:1,value:25},armor:{name:'Походная броня',building:'smithy',gold:20,crystal:0,work:8,kind:'armor',armor:1,value:25},magicSword:{name:'Зачарованный клинок',building:'magicforge',gold:30,crystal:4,work:12,kind:'weapon',attack:1,enchantment:'bolt',value:55},potion:{name:'Зелье лечения',building:'laboratory',gold:12,crystal:0,work:6,kind:'potion',heal:14,value:15},greaterPotion:{name:'Сильное зелье лечения',building:'alchemy',gold:20,crystal:2,work:8,kind:'potion',heal:26,value:30},scroll:{name:'Свиток заклинания',building:'enchanting',gold:15,crystal:2,work:8,kind:'scroll',value:25},enchant:{name:'Зачаровать готовый предмет',building:'enchanting',gold:20,crystal:3,work:8,kind:'enchant'},alchemize:{name:'Алхимическая обработка',building:'alchemy',gold:20,crystal:2,work:8,kind:'enchant'}};
 recipes.expeditionBlade={name:'Клинок экспедиции',building:'smithy',gold:38,crystal:1,work:0,kind:'weapon',attack:3,value:48,discovery:true};
 const enchantments=item=>item.enchantments??(item.enchantment?[item.enchantment]:[]);
 const slots=(f,item)=>Math.min(item.enchantSlots??2,hasBuilding(f,'tower2')?2:hasBuilding(f,'tower')?1:0);
 const enchantable=(f,item,spell)=>['weapon','armor','accessory'].includes(item.kind)&&enchantments(item).length<slots(f,item)&&!enchantments(item).includes(spell);
 function discover(f){
   const found=f.foundRecipes??=[];
   if(!found.includes('expeditionBlade')){
     found.push('expeditionBlade');
     log('В руинах найден постоянный рецепт «Клинок экспедиции».');
   }
 }
 function enchantmentText(k){return SPELLS[k]?.target==='ally'?'+1 ко всем КБ':k==='fire'?'+2 к урону':'+1 к атаке';}
 function itemText(v){return[v.attack?'+'+v.attack+' к атаке':'',v.armor?'+'+v.armor+' ко всем КБ':'',v.heal?'Лечение '+v.heal+' ХП':'',v.spell?'Заклинание: '+SPELLS[v.spell].name:'',enchantments(v).map(k=>SPELLS[k].name+': '+enchantmentText(k)).join(', ')].filter(Boolean).join(' · ');}
 function initialize(){if(!S)return;for(const f of S.factions){f.knowledge=Number.isFinite(f.knowledge)?f.knowledge:0;f.grimoire=Array.isArray(f.grimoire)?f.grimoire:[...baseSpells];for(const a of f.armies)for(const h of a.heroes)if(h.cls==='acolyte'&&!Array.isArray(h.spells))h.spells=[...baseSpells];updateCandidates(f);}S.developmentVersion=8;}
 function training(f,cls){return Capital.recruitLevel(f,cls)-1;}
 function updateCandidates(f){
   Capital.init(f);
   f.candidates.forEach((h,i)=>{
     h.level=Capital.recruitLevel(f,h.cls);
     h.hp=maxHP(h);
     h.sub=Capital.offeredSub(f,h,Math.floor(i/Object.keys(C).length));
     if(h.cls==='acolyte'&&!h.spells)h.spells=[...baseSpells];
   });
 }
 function mages(f){return f.armies.filter(a=>a.pos===f.city).flatMap(a=>living(a)).filter(h=>h.cls==='acolyte');}
 function heroes(f){return f.armies.filter(a=>a.pos===f.city).flatMap(a=>living(a));}
 function researcher(f){return mages(f).find(h=>h.id===UI.researchHero)||mages(f)[0];}
 function holder(f,itemId){for(const h of heroes(f)){const i=h.items.findIndex(i=>i.id===itemId);if(i>=0)return{list:h.items,index:i,item:h.items[i]};}const index=f.bag.findIndex(i=>i.id===itemId);return index>=0?{list:f.bag,index,item:f.bag[index]}:null;}
 function source(f,b){return Object.keys(f.town.buildings).map(Number).filter(p=>lineage(f.town.buildings[p]).includes(b)).sort((a,b)=>discount(f,b)-discount(f,a)||a-b)[0];}
 function discount(f,p){return p!=null?nb(p).filter(j=>lineage(f.town.buildings[j]).includes('power')).length:0;}
 function craftInfo(f,key){const d=recipes[key];if(!d||d.discovery&&!f.foundRecipes?.includes(key))return null;const plot=source(f,d.building);return{...d,plot,crystals:d.crystal?Math.max(1,d.crystal-discount(f,plot)):0};}
 function startResearch(key,heroId){const f=player(),d=studies[key],h=mages(f).find(h=>h.id===heroId)||researcher(f);if(!d||!h||f.town.research||f.grimoire.includes(key)||!hasBuilding(f,'tower')||!cityEffects(f)[d.school]||f.knowledge<d.knowledge)return false;f.knowledge-=d.knowledge;f.town.research={key,hero:h.id,progress:0};log(`${h.name} начал исследование «${d.name}».`);return true;}
 function learn(key,heroId,replace){const f=player(),h=mages(f).find(h=>h.id===heroId);if(!h||!f.grimoire.includes(key)||h.spells.includes(key))return false;if(h.spells.length>=4){const i=h.spells.indexOf(replace);if(i<0)return false;h.spells.splice(i,1,key);}else h.spells.push(key);log(`${h.name}: подготовлено заклинание «${SPELLS[key].name}».`);return true;}
 function startCraft(key,spell,itemId){const f=player(),d=craftInfo(f,key);if(!d||d.plot==null||f.town.craft||f.gold<d.gold||f.crystal<d.crystals)return false;if(['scroll','enchant'].includes(d.kind)&&!f.grimoire.includes(spell))return false;let reserved=null;if(d.kind==='enchant'){const entry=holder(f,itemId);if(!entry||!enchantable(f,entry.item,spell)||!f.grimoire.includes(spell))return false;reserved=entry.list.splice(entry.index,1)[0];}f.gold-=d.gold;f.crystal-=d.crystals;f.town.craft={key,spell,plot:d.plot,progress:0,reserved,crystals:d.crystals};if(['weapon','armor'].includes(d.kind))finishCraft(f);log(`Начато производство: ${d.name}${spell?' · '+SPELLS[spell].name:''}.`);return true;}
 function tick(f){const e=cityEffects(f);f.knowledge+=e.knowledge;const q=f.town.research;if(q){const d=studies[q.key];if(d&&hasBuilding(f,'tower')&&mages(f).some(h=>h.id===q.hero)&&e[d.school]){q.paused=false;q.progress++;if(q.progress>=d.turns){if(!f.grimoire.includes(q.key))f.grimoire.push(q.key);f.town.research=null;log(`${f.name}: изучено «${d.name}».`);if(f.id===0)TurnFlow.notice('research','Изучено новое заклинание',`${d.name}. Послушники в городе могут подготовить его в своём наборе.`,'development','repertoire');}}else if(d&&!q.paused){q.paused=true;if(f.id===0)TurnFlow.notice('research','Исследование приостановлено','Проверьте Башню, направление магии и присутствие исследователя в городе. Можно назначить другого послушника.','development','research');}}
 const c=f.town.craft;
 if(c){
   const d=recipes[c.key];
   if(d&&lineage(f.town.buildings[c.plot]).includes(d.building)&&(d.kind!=='enchant'||enchantable(f,c.reserved,c.spell))){
     c.paused=false;
     c.progress+=Capital.economy(f).prod;
     if(c.progress>=d.work)finishCraft(f);
   }else if(!c.paused){
     c.paused=true;
     if(f.id===0)TurnFlow.notice('production','Производство приостановлено','Нужный цех недоступен.','development','production');
   }
 }
 updateCandidates(f);
 }
 function finishCraft(f){
 const c=f.town.craft,d=recipes[c.key];
 let item=c.reserved;if(d.kind==='enchant')item.enchantments=[...enchantments(item),c.spell];else{item={id:id('i'),name:d.name,kind:d.kind,value:d.value,attack:d.attack||0,armor:d.armor||0,heal:d.heal||0,level:1,materials:{gold:d.gold,crystal:c.crystals??d.crystal}};if(d.enchantment)item.enchantment=d.enchantment;if(d.kind==='scroll'){item.spell=c.spell;item.name='Свиток: '+SPELLS[c.spell].name;}}f.bag.push(item);f.town.craft=null;log(`${f.name}: готово «${item.name}».`);if(f.id===0)TurnFlow.notice('production','Предмет готов',`${item.name}: находится на городском складе.`,'development','storage');
 }
 function modifyGear(f,itemId,scrap){
   const entry=holder(f,itemId), item=entry?.item;
   if(!hasBuilding(f,'smithy')||!item||!['weapon','armor'].includes(item.kind))return false;
   const materials=item.materials??={gold:0,crystal:0};
   if(scrap){
     entry.list.splice(entry.index,1);
     f.gold+=Math.floor(materials.gold/2);
     f.crystal+=Math.floor(materials.crystal/2);
   }else{
     const next=(item.level||1)+1;
     const limit=Math.min(item.maxLevel||3,hasBuilding(f,'magicforge')?3:2);
     if(next>limit||!pay(f,next*10))return false;
     item.level=next;
     materials.gold+=next*10;
     if(item.kind==='weapon')item.attack=(item.attack||0)+1;
     else item.armor=(item.armor||0)+1;
   }
   return true;
 }
 function equip(itemId,heroId){const f=player(),h=heroes(f).find(h=>h.id===heroId),i=f.bag.findIndex(i=>i.id===itemId);if(!h||i<0)return false;const item=f.bag[i];if(['potion','scroll'].includes(item.kind)&&h.items.filter(i=>['potion','scroll'].includes(i.kind)).length>=2)return false;if(['weapon','armor'].includes(item.kind)){const old=h.items.findIndex(i=>i.kind===item.kind);if(old>=0)f.bag.push(h.items.splice(old,1)[0]);}h.items.push(f.bag.splice(i,1)[0]);return true;}
 function enchantStats(h){const e={attack:0,armor:0,damage:0};for(const item of h.items){e.attack+=item.attack||0;e.armor+=item.armor||0;for(const spell of enchantments(item)){if(SPELLS[spell]?.target==='ally')e.armor++;else if(spell==='fire')e.damage+=2;else e.attack++;}}return e;}
 function unitHero(u){return allArmies().flatMap(a=>a.heroes).find(h=>h.id===u?.hero);}
 function known(u){return unitHero(u)?.spells||baseSpells;}
 function defaultAttackSpell(u){return known(u).find(k=>['bolt','fire','frost','drain'].includes(k))||'bolt';}
 function cast(u,t,key,scroll=false){const b=S.battle,d=SPELLS[key];if(!b||!d||!u||!t||u.hp<=0||u.surrender||u.ap<1||!scroll&&(u.cls!=='acolyte'||!known(u).includes(key)||u.mana<d.cost)||dist(u.pos,t.pos,8)>4||!Tactics.sight(u.pos,t.pos)||d.target==='enemy'&&(t.side===u.side||t.hp<=0||t.surrender)||d.target==='ally'&&(t.side!==u.side||t.surrender||t.expired||t.retreated))return false;
 if(baseSpells.includes(key))return original.spell(u,t,key);
 if(d.target==='enemy'&&!Tactics.canAttack({...u,range:4},t))return false;
 if(key==='renewal'&&(t.hp>=t.max&&t.stress<=0||t.hp<=0&&occupiedBattle(t.pos)))return false;
 u.mana-=d.cost;
 if(['fire','frost','drain'].includes(key)){const hp=t.hp,damage=u.damage;u.damage+=key==='fire'?4:0;attackBattle(u,t,false,false,{fire:'fire',frost:'water',drain:'dark'}[key]);u.damage=damage;if(t.hp<hp&&key==='frost')t.snaredUntil=b.round+1;if(key==='drain'&&t.hp<hp){const before=u.hp;u.hp=Math.min(u.max,u.hp+Math.ceil((hp-t.hp)/2));FX.effect('heal',u.pos,u.pos,{target:u.id,hpBefore:before,hpAfter:u.hp,amount:u.hp-before,label:'Похищение жизни'});}}
 else if(key==='barrier'){t.greaterWard=b.round+1;u.ap=0;FX.effect('ward',u.pos,t.pos,{label:'Крепкий оберег',text:'+4 КБ'});}
 else if(key==='renewal'){const before=t.hp;t.hp=Math.min(t.max,t.hp+18);t.stress=Math.max(0,t.stress-15);if(before<=0){t.ap=1;t.raisedRound=b.round;t.deathTurns=0;Relations.rescue(u,t);}u.ap=0;FX.effect('heal',u.pos,t.pos,{target:t.id,hpBefore:before,hpAfter:t.hp,amount:t.hp-before,label:'Исцеление духа'});}
 b.log.unshift(`${u.name}: ${d.name} → ${t.name}, −${d.cost} маны.`);checkBattle();return true;}
 function consume(u,itemId,target=null){const b=S.battle,h=unitHero(u),i=h?.items.findIndex(i=>i.id===itemId),item=i>=0?h.items[i]:null;if(!b||!item||b.side!==u.side||u.ap<1||u.hp<=0||u.surrender)return false;if(item.kind==='potion'){if(u.hp>=u.max)return false;const before=u.hp;u.hp=Math.min(u.max,u.hp+item.heal);u.ap--;h.items.splice(i,1);FX.effect('heal',u.pos,u.pos,{target:u.id,hpBefore:before,hpAfter:u.hp,amount:u.hp-before,label:item.name});return true;}
 if(item.kind==='scroll'){const saved={cls:u.cls,mana:u.mana,range:u.range,atk:u.atk,damage:u.damage};Object.assign(u,{cls:'acolyte',mana:20,range:4,atk:7,damage:7.5});let ok=false;try{ok=cast(u,target,item.spell,true);}finally{Object.assign(u,saved);}if(ok)h.items.splice(i,1);return ok;}return false;}
 function renderPanel(){initialize();const f=player(),e=cityEffects(f),h=researcher(f),q=f.town.research,c=f.town.craft,cityHeroes=heroes(f),recipient=cityHeroes.find(h=>h.id===UI.workshopHero)||cityHeroes[0],chosenSpell=f.grimoire.includes(UI.craftSpell)?UI.craftSpell:f.grimoire[0],goods=[...f.bag,...cityHeroes.flatMap(h=>h.items)].filter(i=>enchantable(f,i,chosenSpell));
 show('development',`<div class="eyebrow">Знания · ремесло · репертуар</div><h2>Развитие города</h2><p>Знания: <b>${f.knowledge}</b> (+${e.knowledge}/ход) · Золото ${f.gold} · Кристаллы ${f.crystal}</p><div class="two dev-panels"><section data-dev-section="research"><h3>Исследование заклинаний</h3><p class="muted">Нужны Башня мага и живой послушник в городе. Знания платятся при начале исследования. Уход исследователя или утрата нужного здания приостанавливает работу.</p><select id="researchHero">${mages(f).map(v=>`<option value="${v.id}" ${h===v?'selected':''}>${esc(v.name)}</option>`).join('')||'<option>В городе нет послушника</option>'}</select>${q?`<div class="rule">${studies[q.key].name}: ${q.progress}/${studies[q.key].turns} ход. ${mages(f).some(h=>h.id===q.hero)&&hasBuilding(f,'tower')&&e[studies[q.key].school]?'Идёт исследование.':'Работа приостановлена.'}<div class="stack">${button('devAssignResearch','Передать выбранному послушнику','',!h||h.id===q.hero)}${button('devCancelResearch','Отменить: знания не возвращаются')}</div></div>`:''}${Object.entries(studies).map(([k,d])=>`<div class="card"><b>${d.name}</b><p>${d.text}</p><small>${d.knowledge} знаний · ${d.turns} хода · ${d.cost} маны в бою. ${e[d.school]?'Направление доступно.':'Нужно направление: '+(d.school==='research'?'Башня мага':d.school==='priest'?'Храм':d.school==='cultist'?'Капище':'Место силы')}</small><div class="stack">${button('devResearch',f.grimoire.includes(k)?'Уже изучено':'Исследовать',`data-id="${k}"`,!!q||f.grimoire.includes(k)||!h||!hasBuilding(f,'tower')||!e[d.school]||f.knowledge<d.knowledge)}</div></div>`).join('')}</section><section data-dev-section="repertoire"><h3>Общий репертуар</h3>${h?`<p>${esc(h.name)}: до четырёх подготовленных заклинаний. При замене выберите, что убрать.</p>${f.grimoire.map(k=>`<div class="card"><b>${SPELLS[k].name}</b><select id="replace-${k}">${h.spells.map(v=>`<option value="${v}">${SPELLS[v].name}</option>`).join('')}</select>${button('devLearn',h.spells.includes(k)?'Подготовлено':'Подготовить',`data-id="${k}"`,h.spells.includes(k))}</div>`).join('')}`:'<p>Послушник должен находиться в городе для подготовки заклинаний.</p>'}</section><section data-dev-section="production"><h3>Производство и склад</h3><p class="muted">Изготовление расходует городское производство. Каждое соседнее Место силы даёт цеху скидку 1 кристалл (минимум 1). Очередь ставится на паузу при утрате цеха.</p><label>Известное заклинание для свитка или свойства: <select id="craftSpell">${f.grimoire.map(k=>`<option value="${k}" ${k===chosenSpell?'selected':''}>${SPELLS[k].name}</option>`).join('')}</select></label><label>Готовый предмет: <select id="craftItem">${goods.map(v=>`<option value="${v.id}">${esc(v.name)} · ${esc(cityHeroes.find(h=>h.items.includes(v))?.name||'склад')}</option>`).join('')||'<option>Нет подходящих предметов</option>'}</select></label><p class="muted">Свойство ${SPELLS[chosenSpell].name}: ${enchantmentText(chosenSpell)}. Ячейки зависят от предмета и башни. Установленные свойства постоянны.</p>${c?`<div class="rule">${recipes[c.key].name}: ${c.progress}/${recipes[c.key].work} работ. ${lineage(f.town.buildings[c.plot]).includes(recipes[c.key].building)?'Идёт изготовление.':'Цех недоступен — пауза.'}${c.reserved?'<br>Предмет передан мастеру и вернётся на склад.':''}<div class="stack">${button('devCancelCraft','Отменить: затраченные ресурсы не возвращаются')}</div></div>`:''}${Object.entries(recipes).map(([k,r])=>{const d=craftInfo(f,k);if(!d)return '';return`<div class="card"><b>${d.name}</b><p>${itemText(d)}</p><p class="muted">${d.gold} золота${d.crystals?', '+d.crystals+' крист.':''} · ${['weapon','armor'].includes(r.kind)?'Мгновенно':d.work+' работ'}. Нужна ${BUILD[d.building].name}.${d.plot!=null&&discount(f,d.plot)&&d.crystal?' Скидка за соседство учтена.':''}</p>${button('devCraft','Заказать',`data-id="${k}"`,!!c||d.plot==null||f.gold<d.gold||f.crystal<d.crystals||d.kind==='enchant'&&!goods.length)}</div>`}).join('')}</section><section data-dev-section="storage"><h3>Выдать герою в городе</h3><select id="workshopHero">${cityHeroes.map(v=>`<option value="${v.id}" ${recipient===v?'selected':''}>${esc(v.name)}</option>`).join('')||'<option>Героев в городе нет</option>'}</select>${recipient?`<div class="card"><b>Снаряжение ${esc(recipient.name)}</b>${recipient.items.map(v=>`<p>${esc(v.name)}<br><small>${itemText(v)}</small> ${button('devUnequip','На склад',`data-id="${v.id}"`,false,'small')}</p>`).join('')||'<p>Нет снаряжения.</p>'}</div>`:''}<p class="muted">Одно оружие и одна броня; прежняя вещь возвращается на склад. До двух зелий/свитков. В походе доступны только взятые с собой расходники.</p>${f.bag.map(v=>`<div class="card"><b>${esc(v.name)}</b><p class="muted">${itemText(v)}</p>${['weapon','armor','potion','scroll'].includes(v.kind)?button('devEquip','Выдать',`data-id="${v.id}"`,!recipient):''}</div>`).join('')||'<p>Склад пуст.</p>'}</section></div>`,true);
 const win=$('modal').querySelector('.window'),tabs={research:'Исследования',repertoire:'Репертуар',production:'Производство',storage:'Склад и снаряжение'},active=tabs[UI.devTab]?UI.devTab:'research';
 const storage=win.querySelector('[data-dev-section="storage"]');
 if(hasBuilding(f,'smithy'))storage.insertAdjacentHTML('beforeend',`<h3>Кузня</h3>${[...f.bag,...cityHeroes.flatMap(h=>h.items)].filter(i=>['armor','weapon'].includes(i.kind)).map(i=>`<p>${esc(i.name)} · ур. ${i.level||1} ${button('devUpgrade','Улучшить · '+((i.level||1)+1)*10+' зол.',`data-id="${i.id}"`,(i.level||1)>=Math.min(i.maxLevel||3,hasBuilding(f,'magicforge')?3:2)||f.gold<((i.level||1)+1)*10)} ${button('devScrap','Разобрать · вернуть '+Math.floor((i.materials?.gold||0)/2)+' зол.',`data-id="${i.id}"`)}</p>`).join('')}`);
 const row=document.createElement('div');row.className='stack';row.innerHTML=Object.entries(tabs).map(([key,name])=>button('devTab',name,`data-id="${key}"`,false,key===active?'gold':'')).join('');win.querySelector('.dev-panels').before(row);
 const mage=$('researchHero'),label=document.createElement('label');label.textContent='Послушник для исследования и подготовки: ';label.append(mage);row.before(label);
 for(const panel of win.querySelectorAll('[data-dev-section]'))panel.hidden=panel.dataset.devSection!==active;
 }
 function decisions(){if(!S)return[];const f=player(),e=cityEffects(f),list=[];if(!f.town.research&&hasBuilding(f,'tower')&&mages(f).length&&Object.entries(studies).some(([k,d])=>!f.grimoire.includes(k)&&e[d.school]&&f.knowledge>=d.knowledge))list.push({key:'research',title:'Башня ждёт выбора исследования',text:'Есть послушник в городе и знания для нового заклинания. Можно начать исследование или сохранить знания.',data:'research',sig:[f.knowledge,f.grimoire,mages(f).map(h=>h.id)]});
 if(!f.town.craft&&Object.entries(recipes).some(([k,d])=>{const c=craftInfo(f,k);return c&&c.plot!=null&&f.gold>=c.gold&&f.crystal>=c.crystals&&(d.kind!=='enchant'||[...f.bag,...heroes(f).flatMap(h=>h.items)].some(i=>['weapon','armor'].includes(i.kind)&&!i.enchantment));}))list.push({key:'production',title:'Мастерские ждут заказа',text:'Можно изготовить предмет или сохранить ресурсы на следующие ходы.',data:'production',sig:[f.gold,f.crystal,f.town.buildings,f.bag.map(i=>i.id)]});return list;}
 function saveHTML(){const doc=document.documentElement.cloneNode(true);doc.querySelector('body').classList.remove('fxbusy');for(const key of ['modal','toast','dicePanel','fxProgress','fxSettings']){const el=doc.querySelector('#'+key);if(el)el.hidden=true;}doc.querySelector('#modal').innerHTML='';for(const el of doc.querySelectorAll('#abilityTooltip'))el.remove();for(const key of ['resources','nav','sidebar','armybar','armies','phase'])doc.querySelector('#'+key).innerHTML='';for(const script of doc.querySelectorAll('script'))if(!script.textContent.includes('const ATLAS_URL='))script.remove();const end=doc.querySelector('#endTurn');end.disabled=false;end.textContent='Завершить ход →';const blob=new Blob(['<!doctype html>\n'+doc.outerHTML],{type:'text/html;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='tuman-i-kosti-086-local-copy.html';a.click();setTimeout(()=>URL.revokeObjectURL(url),30000);}
 const original={effects:cityEffects,preview:buildPreview,refresh:refreshCandidates,tick:tickFaction,unit:makeUnit,spell:spellBattle,armor,render:render,city:renderCity,hire:renderHire,handle,click:clickBattle,load,newGame,ai:aiCity};
 cityEffects=function(f,override=null){const e=original.effects(f,override);e.knowledge=(e.knowledge||0)+2;for(const key of ['trainWarrior','trainArcher','trainRogue','trainAcolyte'])e[key]=Math.min(1,e[key]||0);return e;};
 buildPreview=function(f,p,b){const d=BUILD[b];if(d){if(d.requiresAny&&!d.requiresAny.some(k=>hasBuilding(f,k)))return{ok:false,why:'Нужно одно из зданий: '+d.requiresAny.map(k=>BUILD[k].name).join(', ')};const missing=(d.requires||[]).filter(k=>!hasBuilding(f,k));if(missing.length)return{ok:false,why:'Нужно в городе: '+missing.map(k=>BUILD[k].name).join(', ')};const excludes=[...(d.excludes||[])];if(b==='light')excludes.push('kapish');if(b==='cult')excludes.push('temple');if(excludes.some(k=>hasBuilding(f,k)))return{ok:false,why:'Несовместимо с другой религиозной веткой'};}return original.preview(f,p,b);};
 refreshCandidates=function(f){original.refresh(f);updateCandidates(f);};
 tickFaction=function(f){original.tick(f);if(!f.dead)tick(f);};
 makeUnit=function(h,a,side,i){const u=original.unit(h,a,side,i),e=enchantStats(h);u.atk+=e.attack;u.damage+=e.damage;u.pierce+=e.armor;u.slash+=e.armor;u.ac+=e.armor;return u;};
 armor=function(u,type){return original.armor(u,type)+(u.greaterWard>=S.battle.round?4:0);};
 spellBattle=function(u,t,k){return cast(u,t,k);};
 renderCity=function(){original.city();const f=player(),section=$('modal').querySelector('.window');section.insertAdjacentHTML('afterbegin',`<div class="stack">${button('development','Исследования, производство и склад','','','gold')}</div>`);const select=$('buildSelect');for(const key of ['chapel','light','cult','elemental','cathedral'])if(!hasBuilding(f,key)&&UI.building!==key)select.querySelector(`option[value="${key}"]`)?.remove();const d=BUILD[UI.building];if(d?.requires)section.insertAdjacentHTML('beforeend',`<p class="hint">Условия в городе: ${d.requires.map(k=>BUILD[k].name).join(', ')}${d.requiresAny?'; одно из: '+d.requiresAny.map(k=>BUILD[k].name).join(' / '):''}. Условие не требует соседства. ${d.from?'Замена требует предшественника на выбранном гексе.':''}</p>`);};
 renderHire=function(){updateCandidates(player());original.hire();$('modal').querySelector('.window').insertAdjacentHTML('afterbegin','<p class="hint">Стартовый уровень кандидатов определяется купленными рангами действующего классового здания.</p>');};
 render=function(){initialize();original.render();if(S){$('resources').insertAdjacentHTML('beforeend',`<div><small>Знания</small><b>${player().knowledge}</b></div>`);if(UI.modal==='development')Development.render();}};
 newGame=function(...args){UI.devTab='research';original.newGame(...args);initialize();save();render();};
 load=function(...args){const ok=original.load(...args);if(ok){initialize();save();}return ok;};
 aiCity=function(f){original.ai(f);if(f.dead)return;if(!f.town.projects?.length)for(const key of ['plaza','library','tower','magicacademy','power']){if(hasBuilding(f,key))continue;const p=f.town.plots.find(p=>!f.town.buildings[p]);if(p!=null&&f.gold>BUILD[key].cost+40&&buildPreview(f,p,key).ok){queueBuilding(f,p,key);break;}}};
 clickBattle=function(p){if(UI.mode==='scroll'&&!FX.busy){const u=S.battle?.units.find(u=>u.id===UI.battleSelected),t=S.battle?.units.find(t=>t.pos===p);if(consume(u,UI.scrollItem,t)){UI.mode='attack';after();}else say('Недоступная цель свитка.');return;}original.click(p);};
 handle=function(el){const a=el.dataset.a,k=el.dataset.id;if(a==='downloadGame'){saveHTML();return;}if(a==='development'){if(!FX.busy&&!S.battle&&!processing)Development.render();return;}if(a.startsWith('dev')){if(FX.busy||S.battle||processing||S.result)return;const f=player();if(a==='devUnequip'){const h=heroes(f).find(h=>h.id===$('workshopHero')?.value),i=h?.items.findIndex(v=>v.id===k);if(i>=0)f.bag.push(h.items.splice(i,1)[0]);}if(a==='devTab')UI.devTab=k;if(a==='devAssignResearch'&&f.town.research&&researcher(f))f.town.research.hero=researcher(f).id;if(a==='devCancelResearch')f.town.research=null;if(a==='devCancelCraft'&&f.town.craft){if(f.town.craft.reserved)f.bag.push(f.town.craft.reserved);f.town.craft=null;}if(a==='devResearch')startResearch(k,researcher(f)?.id);if(a==='devLearn')learn(k,researcher(f)?.id,$('replace-'+k)?.value);if(a==='devUpgrade'||a==='devScrap')modifyGear(f,k,a==='devScrap');if(a==='devCraft')startCraft(k,$('craftSpell')?.value,$('craftItem')?.value);if(a==='devEquip')equip(k,$('workshopHero')?.value);save();Development.render();return;}if(a==='bItem'){if(FX.busy)return;const u=S.battle?.units.find(u=>u.id===UI.battleSelected),item=unitHero(u)?.items.find(i=>i.id===k);if(item?.kind==='scroll'){UI.mode='scroll';UI.scrollItem=k;renderBattle();}else if(consume(u,k))after();return;}original.handle(el);};
 const baseBattle=renderBattle;renderBattle=function(){baseBattle();const b=S.battle,u=b?.units.find(u=>u.id===UI.battleSelected);if(!u)return;for(const btn of $('modal').querySelectorAll('[data-a="bSpell"]'))if(!known(u).includes(btn.dataset.v))btn.closest('.ability-tip').remove();const panel=$('modal').querySelector('.battlelayout>section:last-child');for(const item of unitHero(u)?.items||[])if(['potion','scroll'].includes(item.kind))panel.insertAdjacentHTML('beforeend',button('bItem',esc(item.name),`data-id="${item.id}" data-tip="${esc(item.kind==='potion'?itemText(item)+'. Цена: 1 ОД, на себя; предмет расходуется.':itemText(item)+'. Мана не расходуется. Выберите цель в пределах 4 гексов; завершает действия героя.') }"`,b.over!==null||u.ap<1||u.hp<=0||u.surrender||item.kind==='potion'&&u.hp>=u.max));if(UI.mode==='scroll')panel.insertAdjacentHTML('beforeend','<p class="synergy">Выберите цель свитка. Мана не расходуется.</p>');};
 document.addEventListener('change',e=>{if(e.target.id==='researchHero')UI.researchHero=e.target.value;else if(e.target.id==='workshopHero')UI.workshopHero=e.target.value;else if(e.target.id==='craftSpell')UI.craftSpell=e.target.value;else return;Development.render();});
 const baseTip=Tips.ability;Tips.ability=(u,k)=>studies[k]?`${studies[k].name}\n${studies[k].text}\nДальность: 4, нужна линия видимости. Цена: ${studies[k].cost} маны. Завершает действия героя.`:baseTip(u,k);
 Object.assign(Game,{newGame,load,cityEffects,buildPreview,refreshCandidates,tickFaction,spellBattle,clickBattle,render,renderCity,renderHire,renderBattle});
 return{studies,recipes,definitions,discover,modifyGear,initialize,training,updateCandidates,craftInfo,startResearch,learn,startCraft,equip,tick,render:renderPanel,decisions,saveHTML,consume,defaultAttackSpell,known};
})();
Game.development=Development;

```

### `src/battle-lab.html`

```html
<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Туман и кости · Пробный бой</title><style>
:root{color-scheme:dark;font:15px/1.5 system-ui,sans-serif;color:#eee6cf;background:#14251f}*{box-sizing:border-box}body{margin:0}button,select{font:inherit;color:inherit;background:#2c4032;border:1px solid #68795c;border-radius:6px;padding:9px 12px;cursor:pointer}button:hover:enabled,button.active{border-color:#edcc86;background:#435437}button:disabled{opacity:.4;cursor:default}button.primary{background:#e5c27c;color:#213124;font-weight:700}button:focus-visible,select:focus-visible{outline:3px solid #ffe6aa}h1,h2{font-family:Georgia,serif;font-weight:400;margin:0;color:#edcc86}h1{font-size:29px}h2{font-size:22px}p{margin:7px 0}small,.muted{color:#b7c5b1;font-size:12px}.eyebrow{font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#c3b27b}.toolbar{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:18px 24px;border-bottom:1px solid #647156;background:#1c3026}.buttons{display:flex;flex-wrap:wrap;gap:7px}main{max-width:1500px;margin:auto;padding:16px 24px}.layout>section,.layout>aside{min-width:0}.layout{display:grid;grid-template-columns:minmax(0,1fr) 310px;gap:18px}.panel{background:#203529;border:1px solid #596e50;border-radius:10px;padding:16px;margin-bottom:12px}.boardbox{border:1px solid #6c7858;border-radius:10px;background:radial-gradient(ellipse at center,#344c32,#1c3027);overflow:hidden;position:relative}svg{display:block;width:100%;height:auto;touch-action:manipulation}.tile{cursor:pointer;outline:none}.tile:focus polygon,.tile:hover polygon{stroke:#ffe1a0;stroke-width:3}.unit{pointer-events:none;transition:transform .22s ease}.selected-ring{fill:none;stroke:#ffe1a0;stroke-width:3;stroke-dasharray:5 4}.tile-label{pointer-events:none;fill:#b6c59b;font-size:11px}.sectionline{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:10px}.roster{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-top:10px}.hero{font-size:12px;text-align:left;padding:9px;min-width:0}.hero b{display:block;font-size:14px}.hp{height:5px;background:#14241c;margin:7px 0}.hp i{display:block;height:100%;background:#b2ce8f}button.hero.enemy:disabled{opacity:1}.roster-sprite{width:40px;height:48px;float:left;margin:0 7px 5px 0;overflow:visible}.hero .hp{clear:both}.hero.enemy .hp i{background:#d99e83}.actions{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0}.actions button{text-align:left;font-size:13px}.actions small{display:block}.forecast{min-height:100px;border-left:3px solid #e5c27c;background:#2d412d;padding:12px;margin:10px 0}.log{max-height:160px;overflow:auto;font-size:12px}.log p{border-bottom:1px solid #3a5140;padding-bottom:5px}.legend{font-size:12px;color:#c6cfba;padding:10px 14px}.result{border:1px solid #edcc86;background:#38482d;padding:12px;border-radius:7px;margin-bottom:10px}.pending-row{display:flex;gap:5px;margin:6px 0}.pending-row button{font-size:12px}#pending{font-size:12px}#stats{white-space:pre-line}#pending button{margin:3px 0}.boardbox{overflow:auto}#board{min-width:950px}.notice{min-height:24px;color:#edcc86;font-size:13px;margin:8px 0}.rules{font-size:13px}details summary{cursor:pointer;color:#edcc86}label{font-size:13px}textarea{display:block;width:100%;min-height:70px;background:#15291f;color:#eee6cf;border:1px solid #66785a;border-radius:5px;padding:8px;font:inherit}.flash{animation:flash .35s ease}.hit-fx{animation:hitfade .65s ease forwards;pointer-events:none}@keyframes hitfade{to{opacity:0;transform:translateY(-16px)}}@keyframes flash{50%{filter:brightness(1.7)}}@media(prefers-reduced-motion:reduce){.unit{transition:none}.flash{animation:none}}@media(max-width:950px){.layout{grid-template-columns:1fr}aside{display:grid;grid-template-columns:1fr 1fr;gap:10px}main{padding:12px}.toolbar{padding:12px}h1{font-size:24px}}@media(max-width:620px){aside{display:block}.roster{grid-template-columns:repeat(2,1fr)}.toolbar select{max-width:100%}}
.pixel-sprite image,.pixel-terrain,.roster-sprite image{image-rendering:pixelated}</style></head><body><header class="toolbar"><div><div class="eyebrow">Туман и кости · Пробный бой</div><h1>Четыре против четырёх</h1></div><div class="buttons"><select id="scenario" aria-label="Сценарий"><option value="equal">1. Равные силы</option><option value="cover">2. Укрытия и обход</option><option value="rescue">3. Спасти товарища</option><option value="convoy">4. Перехват пленника</option></select><select id="squad" aria-label="Состав отряда"><option value="classic">Классический отряд</option><option value="engineer" selected>Отряд с инженером</option></select><button id="restart">Начать заново</button><button id="download">Копия боя</button></div></header><main><section class="panel"><details open><summary>Уровни, подклассы и противники</summary><div class="buttons" style="margin-top:10px"><label>Ваш уровень <select id="playerLevel"><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option></select></label><label><input id="autoEnemyLevel" type="checkbox" checked> Уровень врагов как у отряда</label><label>Уровень врагов <select id="enemyLevel"><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option></select></label><label>Противники <select id="enemyType"><option value="heroes">Васcалы / герои</option><option value="wolves">Волчья стая</option><option value="spiders">Пауки и плетельщики</option><option value="undead">Скелеты и зомби</option><option value="goblins">Гоблины</option><option value="kobolds">Кобольды</option><option value="ogres">Огры и гоблины</option><option value="beasts">Вепри и волки</option></select></label><label>Базовый крит, % <input id="critChance" type="number" min="0" max="50" step="5" value="10" style="width:75px"></label></div><div class="buttons" style="margin-top:10px"><label>Воин <select id="warriorSub"><option value="base">Воин</option><option value="bastion">Бастион</option><option value="berserker">Берсерк</option></select></label><label>Следопыт <select id="archerSub"><option value="base">Следопыт</option><option value="sniper">Снайпер</option><option value="swift">Стриж</option></select></label><label>Плут <select id="rogueSub"><option value="base">Плут</option><option value="assassin">Ассасин</option><option value="thief">Вор</option></select></label><label>Маг <select id="mageSub"><option value="base">Послушник</option><option value="priest">Жрец</option><option value="elementalist">Стихийник</option><option value="cultist">Культист</option><option value="highpriest">Верховный жрец</option><option value="paladin">Паладин</option></select></label><label id="engineerSubLabel">Инженер <select id="engineerSub" aria-label="Подкласс инженера"><option value="base">Инженер</option><option value="armorer">Бронник</option><option value="demolitionist">Подрывник</option><option value="fortifier">Фортификатор</option></select></label></div><p class="muted">Изменение настроек начинает бой заново. В лаборатории подклассы доступны на любом уровне для сравнения; выбор подкласса заменяет набор боевых способностей. Это тестовые наборы, не полные деревья талантов. Чтобы выбрать Бронника, Подрывника или Фортификатора, включите «Отряд с инженером» вверху. В перехвате повозки охраной остаются герои.</p><p id="packInfo" class="muted"></p></details></section><div class="sectionline"><div><b id="phase"></b><p class="muted" id="goal"></p></div><label><input id="motion" type="checkbox" checked> Анимации</label></div><section id="objectivePanel" class="panel" hidden aria-label="Задача боя"></section><div id="result" hidden class="result" role="status"></div><div class="layout"><section><div class="buttons" style="margin-bottom:8px"><button id="editorToggle">Редактор поля</button><button id="zoomOut" title="Уменьшить карту">−</button><button id="zoomFit">Вся карта</button><button id="zoomIn" title="Увеличить карту">+</button><small>На узком экране карту можно прокручивать в стороны.</small></div><section id="editorPanel" class="panel" hidden><h2>Редактор поля</h2><p class="muted">Редактирование до первого действия. Нажимайте гексы кистью; занятые героями клетки защищены. Перепад высоты больше 1 непроходим, подъём стоит дополнительный шаг.</p><div class="buttons"><label>Поверхность <select id="terrainBrush"><option value="plain">Трава</option><option value="rock">Скалы</option><option value="forest">Деревья</option><option value="cover">Кусты / укрытие</option><option value="mud">Топь</option><option value="water">Вода</option><option value="rubble">Осыпь</option><option value="bridge">Мостки</option></select></label><label>Высота <select id="heightBrush"><option value="keep">Не менять</option><option value="0">0 — низина</option><option value="1">1 — холм</option><option value="2">2 — возвышенность</option></select></label><button id="saveLayout">Сохранить в браузере</button><button id="exportLayout">Скачать поле JSON</button><button id="importLayout">Загрузить поле</button><button id="restoreLayout">Вернуть исходное поле</button></div><input id="layoutFile" type="file" accept=".json,application/json" hidden><p id="editorStatus" class="muted" role="status"></p></section><div class="boardbox"><svg id="board" viewBox="-10 -20 1520 810" role="group" aria-label="Гексовое поле боя"></svg><div class="legend">Синие — ваш отряд · Красные — противник · Камни — преграда · Кусты — +20 защиты от дальнего урона · Топь — 2 шага · Цветные гексы — дальность выбранного действия</div></div><div id="roster" class="roster"></div><p class="muted">Выберите героя → действие → гекс. Светлые гексы доступны для перемещения за оставшиеся ОД. Наведите на цель, чтобы увидеть расчёт.</p></section><aside><section class="panel"><h2 id="selected">Выберите героя</h2><p id="stats" class="muted"></p><div id="actions" class="actions"></div><div id="forecast" class="forecast" aria-live="polite">Выберите действие и наведите на цель.</div><div id="notice" class="notice" role="status"></div><button id="end" class="primary" style="width:100%">Завершить ход отряда</button><div id="pending"></div><p class="muted">Оставшиеся действия нужно выполнить или явно пропустить у героя.</p></section><section class="panel"><h2>Ход боя</h2><div id="log" class="log" aria-live="polite"></div></section><section class="panel rules"><details><summary>Правила этой пробы</summary><p>В сценарии «Перехват пленника» повозка проходит 2 клетки в конце хода охраны к выходу справа. Остановить колёса — 2 ОД соседнего героя; затем освободить пленника — ещё 2 ОД. Мина на дороге также останавливает повозку. Освобождённый получает 1 ОД сразу, затем 2 ОД за ход; он безоружен. Выведите его на любой синий выход слева. Соседний охранник может захватить его повторно за 2 ОД — это провал. Вывод пленника не завершает бой. После него нужно разбить оставшуюся охрану либо эвакуировать всех своих героев. Герой на синем выходе уходит отдельной кнопкой без дополнительной платы ОД. Можно нести одного товарища без сознания: взять за 1 ОД, движение дороже на 1 шаг за клетку; на выходе можно передать раненого в безопасность и вернуться за остальными.</p><p>У каждого героя 3 ОД. За 1 ОД можно пройти до 3 обычных клеток. Остаток оплаченного движения сохраняется до конца хода, даже между атаками. Топь стоит 2 шага, замедление добавляет 1 шаг на клетку. Новый ход обнуляет остаток.</p><p>Обычная атака — 1 ОД, особый приём — 2 ОД, защита — 1 ОД. Все доступные действия нужно выполнить или явно пропустить. Можно пропустить остаток действий выбранного героя или всех перечисленных героев.</p><p>Защита разделена на колющую, режущую и магическую. Снижение = рейтинг / (рейтинг + 50). Рейтинг 25 даёт 33%, 50 — 50%, 100 — 67%. Итоговый урон округляется, минимум 1. Защитная стойка добавляет 20 ко всем рейтингам до следующего своего хода; укрытие — ещё 20 против дальнего урона.</p><p>Цветная область показывает дальность выбранного действия с учётом скал. Пунктирные гексы — в радиусе, но без линии огня. Скалы, деревья и вода непроходимы. Скалы, деревья и высокая земля перекрывают огонь; герои — нет.</p><p>Пробитие уменьшает обе физические защиты на 20 до конца следующего хода цели. Ледяная стрела замедляет на следующий ход. Перезарядка приёмов — два раунда.</p><p>Послушник лечит 10 ХП за 2 ОД с дальности 4, всего два раза за бой. Поднятый герой имеет только 1 ОД. При поражении всего отряда бой завершается; победители поднимают своих с 1 ХП.</p><p>Инженер занимает одно из четырёх мест вместо разведчика. Базовый приём — пробивающий выстрел. Бронник использует личную силовую броню, Подрывник ставит мины, Фортификатор создаёт укреплённые укрытия и мостки через топь. Подклассы выбираются перед боем. Ремесло Бронника и работы Фортификатора на глобальной карте ещё не реализованы. Оба отряда получают одинаковый выбор.</p><p>Соседний живой враг блокирует дальние атаки, включая атакующую магию. Сначала нужно отойти так, чтобы рядом не осталось врагов. Лечение и размещение объектов не блокируются. У следопыта 20% уклонениеа, у плута 25%. Мины не проверяют уклонение. Послушник начинает с барьером 12: он поглощает урон после защиты; +4 барьера в начале собственного хода, максимум 12. Без сознания барьер не восстанавливается.</p><p>Стресс +15 при падении товарища, при 60+ — на 1 ОД меньше в начале хода. Полной системы плена героев, срывов и развития отношений в этой пробе нет. Критические попадания наносят ×1,5 урона до защиты; базовый шанс задаётся выше. Правила кампании сохранены.</p></details></section></aside></div><section class="panel"><details><summary>Записать впечатления и результат</summary><p class="muted">После каждого сценария полезно сравнить: были ли понятны последствия, хватало ли выбора, сколько занял бой. Запись скачивается текстовым файлом и никуда не отправляется.</p><label>Ваши впечатления<textarea id="feedback" placeholder="Что понравилось? Где было непонятно или скучно?"></textarea></label><button id="report" style="margin-top:8px">Сохранить результат пробы</button></details></section></main><script id="labMapData" type="application/json">{}</script><script>
'use strict';
/*__PIXEL_SPRITES__*/
/*__STRIKE__*/
const Lab=(()=>{
const $=id=>document.getElementById(id), W=16,H=10,dirs=[[1,0],[1,-1],[0,-1],[-1,0],[-1,1],[0,1]];
const DAMAGE={piercing:'колющий',slashing:'режущий',magic:'магический'};
const TYPES={
 warrior:{name:'Страж',mark:'Щ',hp:32,def:{piercing:20,slashing:55,magic:15},baseDamage:8,range:1,damage:'slashing'},
 archer:{name:'Следопыт',mark:'Л',hp:24,def:{piercing:5,slashing:10,magic:20},baseDamage:6,range:6,damage:'piercing',dodge:Strike.heroDodge.archer},
 rogue:{name:'Разведчик',mark:'К',hp:26,def:{piercing:10,slashing:15,magic:15},baseDamage:7,range:1,damage:'piercing',dodge:Strike.heroDodge.rogue},
 acolyte:{name:'Послушник',mark:'М',hp:18,def:{piercing:5,slashing:5,magic:40},baseDamage:6,range:5,damage:'magic',barrier:12,regen:4},
 prisoner:{name:'Освобождённый пленник',hp:16,def:{piercing:5,slashing:5,magic:5},baseDamage:0,range:0,damage:'piercing'},
 engineer:{name:'Инженер',mark:'И',hp:28,def:{piercing:30,slashing:25,magic:20},baseDamage:6,range:5,damage:'piercing'}
};
const SUBS={base:'Инженер',armorer:'Бронник',demolitionist:'Подрывник',fortifier:'Фортификатор'};
const ACTIONS={
 move:{name:'Перемещение',cost:0,tip:'За 1 ОД — 3 шага. Остаток сохраняется до конца хода. Топь — 2 шага, замедление — ещё +1 на клетку.'},
 attack:{name:'Атака',cost:1,tip:'Урон указан для удара, от которого цель не уклонилась. Цветная область показывает дальность и линию огня. Прогноз учитывает соответствующий тип защиты.'},
 guard:{name:'Защита',cost:1,tip:'+20 ко всем трём рейтингам защиты до следующего своего хода. Не складывается.'},
 skip:{name:'Пропустить остаток',cost:0,tip:'Явно отказаться от оставшихся ОД и оплаченных шагов до следующего хода.'},
 break:{name:'Пробитие',cost:2,range:1,baseDamage:7,damage:'slashing',tip:'6–8 режущего урона; обе физические защиты цели −20 до конца следующего хода. Перезарядка 2 раунда.'},
 frost:{name:'Ледяная стрела',cost:2,range:6,baseDamage:6,damage:'magic',tip:'5–7 магического урона. Движение цели дороже на 1 шаг за клетку в следующий ход. Перезарядка 2 раунда.'},
 lunge:{name:'Точный удар',cost:2,range:1,baseDamage:9,damage:'piercing',pierce:25,tip:'8–10 колющего урона. Игнорирует 25 колющей защиты. Перезарядка 2 раунда.'},
 blast:{name:'Пламя',cost:2,range:5,baseDamage:9,damage:'magic',tip:'8–10 магического урона по одной цели. Перезарядка 2 раунда.'},
 heal:{name:'Лечение',cost:2,range:4,ally:true,tip:'10 ХП союзнику, подъём с 1 ОД. Дальность 4; два применения за бой.'},
 pierceshot:{name:'Пробивающий выстрел',cost:2,range:5,baseDamage:8,damage:'piercing',pierce:15,tip:'7–9 колющего урона; игнорирует 15 защиты. Перезарядка 2 раунда.'},
 mine:{name:'Поставить мину',cost:2,range:3,baseDamage:9,damage:'piercing',tile:true,tip:'Мина на свободном гексе в радиусе 3. Первый враг при входе получает 8–10 колющего урона. Перезарядка 2 раунда.'},
 powerarmor:{name:'Силовая броня',cost:2,self:true,tip:'Личная силовая броня: +30 к трём защитам и +2 к базовому урону до конца следующего своего хода. Перезарядка 2 раунда.'},
 fortify:{name:'Укрепить гекс',cost:2,range:3,tile:true,tip:'Укреплённое укрытие на свободной обычной клетке: +35 защиты от дальнего урона тому, кто её занимает. Перезарядка 2 раунда.'},
 bridge:{name:'Мостки через топь',cost:1,range:3,tile:true,tip:'Превращает свободную клетку топи в мостки: проход стоит 1 шаг вместо 2. Глобальные мосты и ремесло будут отдельным этапом.'}

};
const PROFILES={base:{name:'Базовый'},bastion:{name:'Бастион',armor:20},berserker:{name:'Берсерк',damage:2,armor:-10},sniper:{name:'Снайпер',damage:2,range:2},swift:{name:'Стриж'},assassin:{name:'Ассасин',damage:3,crit:.1},thief:{name:'Вор',dodge:.1},priest:{name:'Жрец',healing:6,heals:3},highpriest:{name:'Верховный жрец',healing:10,heals:4},elementalist:{name:'Стихийник',magic:10},cultist:{name:'Культист'},paladin:{name:'Паладин',hp:10,armor:15}};
Object.assign(TYPES,{
 wolf:{name:'Волк',hp:22,def:{piercing:10,slashing:15,magic:5},baseDamage:6,range:1,damage:'piercing',dodge:.1,special:'lunge'},
 spider:{name:'Гигантский паук',hp:25,def:{piercing:15,slashing:10,magic:10},baseDamage:6,range:1,damage:'piercing',dodge:.1,special:'web'},
 spinner:{name:'Паук-плетельщик',hp:20,def:{piercing:10,slashing:5,magic:10},baseDamage:4,range:4,damage:'piercing',special:'web'},
 skeleton:{fearless:true,name:'Скелет',hp:24,def:{piercing:55,slashing:10,magic:5},baseDamage:7,range:1,damage:'slashing',special:'break'},
 zombie:{fearless:true,name:'Зомби',hp:40,def:{piercing:15,slashing:10,magic:5},baseDamage:8,range:1,damage:'slashing',special:'lunge'},
 goblin:{name:'Гоблин',hp:20,def:{piercing:10,slashing:10,magic:5},baseDamage:6,range:1,damage:'piercing',dodge:.15,special:'lunge'},
 goblinArcher:{name:'Гоблин-лучник',hp:18,def:{piercing:5,slashing:5,magic:5},baseDamage:5,range:5,damage:'piercing',dodge:.15,special:'pierceshot'},
 kobold:{name:'Кобольд-копейщик',hp:23,def:{piercing:40,slashing:15,magic:5},baseDamage:6,range:1,damage:'piercing',special:'lunge'},
 slinger:{name:'Кобольд-пращник',hp:20,def:{piercing:15,slashing:10,magic:5},baseDamage:5,range:4,damage:'piercing',special:'pierceshot'},
 ogre:{name:'Огр',hp:52,def:{piercing:35,slashing:35,magic:5},baseDamage:11.5,range:1,damage:'slashing',special:'smash'},
 boar:{name:'Дикий вепрь',hp:32,def:{piercing:25,slashing:25,magic:5},baseDamage:7.5,range:1,damage:'piercing',special:'lunge'}
});
const PACKS={wolves:['wolf','wolf','wolf','wolf'],spiders:['spider','spinner','spider','spinner'],undead:['skeleton','zombie','skeleton','zombie'],goblins:['goblin','goblinArcher','goblin','goblinArcher'],kobolds:['kobold','slinger','kobold','slinger'],ogres:['ogre','goblin','ogre','goblinArcher'],beasts:['boar','wolf','boar','wolf']};
ACTIONS.web={name:'Липкая паутина',cost:2,range:4,baseDamage:4,damage:'piercing',tip:'Паутина: 3–5 колющего урона и замедление на следующий ход при попадании.'};
ACTIONS.smash={name:'Удар дубиной',cost:2,range:1,baseDamage:12.5,damage:'slashing',area:1,tip:'11–14 режущего урона врагам в радиусе 1 от цели.'};
function stats(u){const t=TYPES[u.type],p=PROFILES[u.sub]||{},n=Math.max(0,(u.level||1)-1),growth=u.type==='acolyte'?2:u.type==='warrior'||u.type==='engineer'?4:3,def=Object.fromEntries(Object.entries(t.def).map(([k,v])=>[k,Math.max(0,v+n*2+(k==='magic'?(p.magic||0):(p.armor||0)))]));return {...t,hp:t.hp+growth*n+(p.hp||0),baseDamage:t.baseDamage+Math.floor(n/2)+(p.damage||0),range:u.sub==='paladin'?1:t.range+(p.range||0),damage:u.sub==='paladin'?'slashing':t.damage,def,dodge:Math.min(.75,(t.dodge||0)+(p.dodge||0)+(u.smoke?.2:0)),barrier:t.barrier?t.barrier+n*2:0,regen:t.regen?t.regen+Math.floor(n/2):0}}
const healing=u=>10+Math.max(0,(u.level||1)-1)*2+(PROFILES[u.sub]?.healing||0);
Object.assign(ACTIONS,{
 shieldBash:{name:'Удар щитом',cost:2,range:1,baseDamage:5,damage:'slashing',slow:true,tip:'4–6 режущего урона, замедляет цель на следующий ход.'},
 coverAlly:{name:'Прикрыть союзника',cost:1,range:2,ally:true,kind:'ward',tip:'+20 ко всем защитам союзника до конца его следующего хода.'},
 cleave:{name:'Размашистый удар',cost:2,range:1,baseDamage:10.5,damage:'slashing',area:1,tip:'9–12 режущего урона цели и врагам в радиусе 1 от неё.'},
 rage:{name:'Боевая ярость',cost:1,self:true,buff:'rage',tip:'+3 урона и −10 физических защит до конца следующего своего хода.'},
 aimShot:{name:'Прицельный выстрел',cost:2,range:8,baseDamage:9.5,damage:'piercing',pierce:25,tip:'8–11 колющего урона с игнорированием 25 защиты, дальность 8.'},
 pinShot:{name:'Сковывающий выстрел',cost:1,range:7,baseDamage:5,damage:'piercing',slow:true,tip:'4–6 колющего урона, замедляет цель на следующий ход.'},
 doubleShot:{name:'Двойной выстрел',cost:2,range:6,baseDamage:5,damage:'piercing',hits:2,tip:'Два отдельных удара по 4–6 колющего урона. Уклонение, блок и крит определяются для каждого удара.'},
 skirmishShot:{name:'Выстрел на отходе',cost:1,range:4,baseDamage:4,damage:'piercing',grantStride:2,tip:'3–5 колющего урона и 2 оплаченных шага для смены позиции.'},
 backstab:{name:'Удар в уязвимость',cost:2,range:1,baseDamage:10.5,damage:'piercing',pierce:30,critBonus:.15,tip:'9–12 колющего урона; игнорирует 30 защиты, +15 п.п. шанса крита.'},
 smoke:{name:'Дымовая завеса',cost:1,self:true,buff:'smoke',tip:'+20 п.п. уклонениеа до конца следующего своего хода, максимум 75%.'},
 hamstring:{name:'Подрезать сухожилия',cost:1,range:1,baseDamage:5,damage:'slashing',slow:true,tip:'4–6 режущего урона и замедление цели.'},
 sand:{name:'Песок в глаза',cost:1,range:2,baseDamage:1.5,damage:'piercing',weaken:true,meleeTool:true,tip:'1–2 колющего урона; цель наносит на 2 меньше урона следующий ход. Можно использовать рядом с врагом.'},
 priestHeal:{name:'Жреческое исцеление',cost:2,range:4,ally:true,kind:'heal',cooldown:1,stressRelief:10,tip:'Усиленное лечение, −10 стресса, поднимает бессознательного с 1 ОД.'},
 blessing:{name:'Благословение защиты',cost:1,range:3,ally:true,kind:'ward',tip:'+20 ко всем защитам союзника до конца следующего его хода.'},
 greaterHeal:{name:'Высшее исцеление',cost:2,range:5,ally:true,kind:'heal',cooldown:1,healBonus:4,cleanse:true,stressRelief:20,tip:'Усиленное лечение, снимает замедление и ослабление, −20 стресса.'},
 sanctuary:{name:'Священный покров',cost:2,range:3,ally:true,kind:'ward',area:1,tip:'+20 защиты союзнику и товарищам в радиусе 1 от него до конца их следующего хода.'},
 fireball:{name:'Огненный шар',cost:2,range:5,baseDamage:9.5,damage:'magic',area:1,fire:true,tip:'8–11 магического урона цели и врагам в радиусе 1. Огонь подавляет регенерацию тролля.'},
 iceLance:{name:'Ледяное копьё',cost:2,range:6,baseDamage:8,damage:'magic',pierce:15,slow:true,tip:'7–9 магического урона; игнорирует 15 сопротивления и замедляет.'},
 drainLife:{name:'Похищение жизни',cost:2,range:4,baseDamage:8.5,damage:'magic',drain:.5,tip:'7–10 магического урона; восстанавливает половину реально снятых ХП.'},
 curse:{name:'Проклятье немощи',cost:1,range:4,baseDamage:3,damage:'magic',weaken:true,expose:true,tip:'2–4 магического урона; −2 урона и −20 физических защит цели на следующий ход.'},
 smite:{name:'Карающий удар',cost:2,range:1,baseDamage:9.5,damage:'magic',bonusUndead:4,tip:'8–11 магического урона вблизи; против нежити ещё +4.'},
 layHands:{name:'Возложение рук',cost:2,range:1,ally:true,kind:'heal',healBonus:4,cooldown:2,tip:'Лечение соседнего союзника и подъём с 1 ОД.'},
 armorPunch:{name:'Удар силовой перчаткой',cost:2,range:1,baseDamage:9.5,damage:'piercing',pierce:20,tip:'8–11 колющего урона; игнорирует 20 защиты, работает в ближнем бою.'},
 blastCharge:{name:'Подрывной заряд',cost:2,range:3,baseDamage:8.5,damage:'piercing',area:1,tip:'7–10 колющего урона цели и врагам в радиусе 1.'}
});
const SUB_ABILITIES={bastion:['shieldBash','coverAlly'],berserker:['cleave','rage'],sniper:['aimShot','pinShot'],swift:['doubleShot','skirmishShot'],assassin:['backstab','smoke'],thief:['hamstring','sand'],priest:['priestHeal','blessing'],highpriest:['greaterHeal','sanctuary'],elementalist:['fireball','iceLance'],cultist:['drainLife','curse'],paladin:['smite','layHands'],armorer:['powerarmor','armorPunch'],demolitionist:['mine','blastCharge'],fortifier:['fortify','bridge']};
for(const ids of Object.values(SUB_ABILITIES))for(const id of ids)if(!['powerarmor','mine','fortify','bridge'].includes(id))ACTIONS[id].profile=true;
ACTIONS.heal.kind='heal';ACTIONS.blast.fire=true;
Object.assign(TYPES,{
 troll:{name:'Тролль',hp:50,def:{piercing:25,slashing:30,magic:10},baseDamage:10.5,range:1,damage:'slashing',special:'smash',regenHP:8},
 deathguard:{name:'Костяной гвардеец',hp:40,def:{piercing:65,slashing:35,magic:15},baseDamage:9.5,range:1,damage:'slashing',special:'break',fearless:true},
 revenant:{name:'Умертвие',hp:42,def:{piercing:35,slashing:25,magic:25},baseDamage:9.5,range:1,damage:'magic',special:'graveStrike',fearless:true},
 necromancer:{name:'Некромант',hp:32,def:{piercing:15,slashing:15,magic:40},baseDamage:7.5,range:5,damage:'magic',special:'deathBolt',fearless:true},
 wightlord:{name:'Древнее умертвие',hp:60,def:{piercing:55,slashing:45,magic:35},baseDamage:11.5,range:1,damage:'magic',special:'graveWave',fearless:true}
});
Object.assign(ACTIONS,{
 graveStrike:{name:'Могильный удар',cost:2,range:1,baseDamage:10.5,damage:'magic',drain:.3,tip:'Магический удар, восстанавливает часть снятого здоровья.'},
 deathBolt:{name:'Стрела смерти',cost:2,range:5,baseDamage:9.5,damage:'magic',drain:.3,tip:'Магический снаряд с похищением части здоровья.'},
 graveWave:{name:'Могильная волна',cost:2,range:1,baseDamage:11.5,damage:'magic',area:1,drain:.3,tip:'Магический урон по площади и похищение части здоровья.'}
});
PACKS.undead=['skeleton','skeleton','skeleton','skeleton'];
PACKS.zombies=['skeleton','zombie','skeleton','zombie'];PACKS.trolls=['troll','goblin','troll','goblinArcher'];PACKS.eliteUndead=['deathguard','revenant','necromancer','deathguard'];PACKS.ancientUndead=['wightlord','revenant','necromancer','deathguard'];PACKS.mountainTrolls=['troll','ogre','troll','ogre'];
const PACK_INFO={heroes:{min:1,name:'Вассалы / герои'},wolves:{min:1,name:'Волчья стая'},undead:{min:1,name:'Скелеты'},goblins:{min:1,name:'Гоблины'},spiders:{min:2,name:'Пауки и плетельщики'},kobolds:{min:2,name:'Кобольды'},beasts:{min:3,name:'Вепри и волки'},zombies:{min:3,name:'Скелеты и зомби'},ogres:{min:5,name:'Огры и гоблины'},trolls:{min:5,name:'Тролли и гоблины'},eliteUndead:{min:6,name:'Усиленная нежить'},ancientUndead:{min:8,name:'Древняя нежить'},mountainTrolls:{min:8,name:'Тролли и огры'}};
function syncPacks(){const select=$('enemyType'),level=Number($('playerLevel').value),old=select.value;select.innerHTML=Object.entries(PACK_INFO).map(([id,p])=>`<option value="${id}" ${level<p.min?'disabled':''}>${p.name} · с ${p.min} ур.</option>`).join('');select.value=PACK_INFO[old]&&level>=PACK_INFO[old].min?old:'wolves';$('packInfo').textContent='Доступ определяется уровнем вашего отряда. По умолчанию уровень врагов равен вашему; ручной выбор отключает автоматическую подстройку. Тролли восстанавливают здоровье: огненные атаки подавляют регенерацию.'}
function abilities(u){if(!u||u.type==='prisoner')return [];if(TYPES[u.type].special)return [TYPES[u.type].special];if(SUB_ABILITIES[u.sub])return SUB_ABILITIES[u.sub];return [({warrior:'break',archer:'frost',rogue:'lunge',acolyte:'blast',engineer:'pierceshot'}[u.type]),...(u.type==='acolyte'?['heal']:[])].filter(Boolean)}
const cooldownUntil=(u,a)=>ACTIONS[a]?.profile?(u.skillCD?.[a]||0):(a==='attack'||a==='bridge'||a==='heal'?0:u.cooldown||0);
function setCooldown(u,a){if(a==='attack'||a==='heal'||a==='bridge')return;if(ACTIONS[a].profile){u.skillCD??={};u.skillCD[a]=s.round+(ACTIONS[a].cooldown||2)}else u.cooldown=s.round+2}
function activateSelf(u,a){const d=spec(u,a);if(!abilities(u).includes(a)||!d.self||!available(u,a)||u[d.buff])return false;u.ap-=d.cost;u[d.buff]=2;setCooldown(u,a);s.actions++;log(`${u.name}: ${d.name}.`);return true}

let customMaps={},editorActive=false;
let s=null,mode='move',selected='p0',busy=false,serial=0,notice='',hover=null,pendingOpen=false;
const actors=()=>{const units=s.units.filter(u=>!u.evacuated&&!u.carriedBy);return s?.objective&&['free','recaptured'].includes(s.objective.prisoner.status)?[...units,s.objective.prisoner]:units};
const key=(q,r)=>q+','+r,cell=(q,r)=>s.tiles[key(q,r)],unit=id=>actors().find(u=>u.id===id),at=(q,r)=>actors().find(u=>u.q===q&&u.r===r),distance=(a,b)=>(Math.abs(a.q-b.q)+Math.abs(a.r-b.r)+Math.abs(a.q+a.r-b.q-b.r))/2;
const point=(q,r)=>({x:52+q*70+r*35,y:70+r*70-(cell(q,r)?.height||0)*12});
const alive=u=>u.hp>0&&!u.evacuated;
function log(t){s.log.unshift(t);s.log=s.log.slice(0,80)}
function rng(){s.seed=(Math.imul(s.seed,1664525)+1013904223)>>>0;return s.seed/4294967296}
function reset(scenario='equal'){
 if($('autoEnemyLevel').checked)$('enemyLevel').value=$('playerLevel').value;syncPacks();
 serial++;$('lab-effects')?.replaceChildren();busy=false;mode='move';selected='p0';hover=null;notice='';pendingOpen=false;editorActive=false;
 s={scenario,round:1,side:0,seed:8127,units:[],tiles:{},log:[],winner:null,started:Date.now(),actions:0,moves:0,damage:0,absorbed:0,dodges:0,blocks:0,crits:0,critChance:Math.max(0,Math.min(50,Number($('critChance').value)||0))/100,playerLevel:Number($('playerLevel').value),enemyLevel:Number($('enemyLevel').value),enemyType:scenario==='convoy'?'heroes':$('enemyType').value,heals:0,revives:0,mines:[],loadout:$('squad').value,sub:$('engineerSub').value};
 for(let r=0;r<H;r++)for(let q=0;q<W;q++)s.tiles[key(q,r)]={q,r,kind:'plain',height:0};
 const kinds=['warrior','archer',s.loadout==='engineer'?'engineer':'rogue','acolyte'],names=['Борис','Эльга',s.loadout==='engineer'?'Тихон':'Радан','Мира'];
 for(let side=0;side<2;side++)for(let i=0;i<4;i++){const type=kinds[i],t=TYPES[type];s.units.push({id:(side?'e':'p')+i,name:side?['Железный страж','Вражеский лучник',s.loadout==='engineer'?'Вражеский инженер':'Налётчик','Чародей'][i]:names[i],side,type,sub:type==='engineer'?s.sub:null,q:side?13:2,r:i+3,hp:t.hp,max:t.hp,ap:3,stress:0,guard:false,exposed:0,slow:0,cooldown:0,barrier:t.barrier||0,heals:2,wake:false,stride:0,power:0,skipped:false,evacuated:false,carrying:null,carriedBy:null});}
 $('enemyType').disabled=scenario==='convoy';if(scenario==='convoy')$('enemyType').value='heroes';
 const pack=PACKS[s.enemyType];if(pack)s.units.filter(u=>u.side===1).forEach((u,i)=>{u.type=pack[i];u.name=TYPES[u.type].name+' '+(i+1);u.sub=null});
 for(const u of s.units){u.level=u.side?s.enemyLevel:s.playerLevel;if(!pack||u.side===0){if(u.type!=='engineer')u.sub=$({warrior:'warriorSub',archer:'archerSub',rogue:'rogueSub',acolyte:'mageSub'}[u.type]).value}const t=stats(u);u.hp=u.max=t.hp;u.barrier=t.barrier;u.heals=PROFILES[u.sub]?.heals||2;u.skillCD={};u.protected=0;u.rage=0;u.smoke=0;u.weaken=0;u.burn=0;u.stride=u.sub==='thief'?2:0;}
 for(const [q,r,h] of [[5,1,1],[6,1,1],[7,1,2],[8,1,1],[9,8,1],[10,8,1]])cell(q,r).height=h;
 if(scenario==='cover'){
  for(const [q,r] of [[7,2],[7,3],[7,4],[8,5],[8,6],[8,7]])cell(q,r).kind='rock';
  for(const [q,r] of [[5,2],[6,4],[5,6],[9,3],[10,5],[10,7]])cell(q,r).kind='cover';
  for(const [q,r] of [[8,0],[7,9]])cell(q,r).kind='forest';
  for(const [q,r] of [[6,3],[6,5],[7,5],[8,4],[9,4],[9,6]])cell(q,r).kind='mud';
 }
 if(scenario==='rescue'){
  Object.assign(unit('p0'),{q:7,r:5,hp:0,ap:0});Object.assign(unit('p3'),{q:5,r:5});Object.assign(unit('p1'),{q:4,r:3});Object.assign(unit('p2'),{q:4,r:7});
  Object.assign(unit('e0'),{q:9,r:5});Object.assign(unit('e1'),{q:11,r:3});Object.assign(unit('e2'),{q:11,r:7});Object.assign(unit('e3'),{q:12,r:5});
  cell(6,4).kind='cover';cell(8,6).kind='mud';selected='p3';
  log('Борис без сознания. Мира может поднять его лечением; после подъёма у него будет 1 ОД.');
 }
 if(scenario==='convoy')setupConvoy();
 if(customMaps[scenario]){const m=customMaps[scenario];if(!s.units.some(u=>['rock','forest','water'].includes(m.tiles.find(t=>t.q===u.q&&t.r===u.r)?.kind)))s.tiles=Object.fromEntries(m.tiles.map(t=>[key(t.q,t.r),{...t}]))}
 $('scenario').value=scenario;$('engineerSub').disabled=s.loadout!=='engineer';$('engineerSubLabel').title=s.loadout==='engineer'?'Бронник, Подрывник, Фортификатор':'Выберите «Отряд с инженером» вверху';$('feedback').value='';log('Начало боя. Ваш отряд действует первым.');render();
}
function cubeRound(x,z){let y=-x-z,rx=Math.round(x),ry=Math.round(y),rz=Math.round(z);const dx=Math.abs(rx-x),dy=Math.abs(ry-y),dz=Math.abs(rz-z);if(dx>dy&&dx>dz)rx=-ry-rz;else if(dy>dz)ry=-rx-rz;else rz=-rx-ry;return {q:rx,r:rz}}
function los(a,b){const n=distance(a,b),from=(cell(a.q,a.r)?.height||0)+1,to=(cell(b.q,b.r)?.height||0)+1;for(let i=1;i<n;i++){const t=i/n,p=cubeRound(a.q+(b.q-a.q)*t+.000001,a.r+(b.r-a.r)*t+.000001),tile=cell(p.q,p.r);if(!tile||['rock','forest'].includes(tile.kind)||tile.height>from+(to-from)*t)return false}return true}
function engaged(u,pos=u){return s.units.some(t=>t.side!==u.side&&alive(t)&&distance(pos,t)===1)}
function blockedShot(u,d,pos=u){return !!(d?.baseDamage&&d.range>1&&!d.tile&&!d.meleeTool&&engaged(u,pos))}
const movementBudget=u=>u.ap*3+(u.stride||0);
const stepCost=(u,t,from=u)=>(['mud','rubble'].includes(t.kind)?2:1)+(u.slow?1:0)+(u.carrying?1:0)+(u.type==='zombie'?1:0)+Math.max(0,(t.height||0)-(cell(from.q,from.r)?.height||0));
const movementAP=(u,steps)=>Math.ceil(Math.max(0,steps-(u.stride||0))/3);
function paths(u,budget=movementBudget(u)){
 const result=new Map([[key(u.q,u.r),{q:u.q,r:u.r,cost:0,path:[]}]]),queue=[{q:u.q,r:u.r,cost:0,path:[]}];
 while(queue.length){queue.sort((a,b)=>a.cost-b.cost);const p=queue.shift();if(p.cost!==result.get(key(p.q,p.r)).cost)continue;
 for(const [dq,dr] of dirs){const q=p.q+dq,r=p.r+dr,t=cell(q,r);if(!t||['rock','forest','water'].includes(t.kind)||occupied(q,r)||Math.abs(t.height-(cell(p.q,p.r).height||0))>1)continue;const cost=p.cost+stepCost(u,t,p);if(cost>budget)continue;const k=key(q,r);if(!result.has(k)||cost<result.get(k).cost){const v={q,r,cost,apCost:movementAP(u,cost),path:[...p.path,{q,r}]};result.set(k,v);queue.push(v)}}}
 return result;
}
const special=u=>abilities(u)[0];
const role=u=>u.type==='engineer'?SUBS[u.sub]||SUBS.base:PROFILES[u.sub]?.name&&u.sub!=='base'?PROFILES[u.sub].name:TYPES[u.type].name;
const reduction=rating=>Math.max(0,rating)/(50+Math.max(0,rating));
function defense(u,damage){return Math.max(0,stats(u).def[damage]-(u.exposed&&damage!=='magic'?20:0))+(u.guard?20:0)+(u.power?30:0)+(u.protected?20:0)-(u.rage&&damage!=='magic'?10:0)}
const pending=()=>actors().filter(u=>u.side===0&&alive(u)&&(u.ap>0||u.stride>0));
function skip(u){if(!u||u.side!==0||s.side!==0||busy||!alive(u)||s.winner!==null)return;u.ap=0;u.stride=0;u.skipped=true;log(`${u.name}: остаток действий явно пропущен.`);notice='';render()}
function skipAll(){for(const u of [...pending()])skip(u);pendingOpen=false;render()}
function available(u,a){const d=spec(u,a);return !!u&&!!d&&alive(u)&&u.side===s.side&&!u.skipped&&u.ap>=d.cost&&cooldownUntil(u,a)<=s.round}
function spec(u,a,t=null){
 const action=ACTIONS[a];
 if(!action||!u)return action;
 const d=a==='attack'?{...action,...stats(u),name:'Атака'}:{...action};
 if(d.profile)d.tip+=' Перезарядка: '+(d.cooldown||2)+((d.cooldown||2)===1?' раунд.':' раунда.');
 if(d.kind==='heal'){
   d.amount=healing(u)+(d.healBonus||0);
   d.tip+=' Лечение: '+d.amount+' ХП.';
 }
 if(a==='heal')d.tip=healing(u)+' ХП союзнику, подъём с 1 ОД. Дальность 4, осталось '+u.heals+' применений.';
 if(a==='guard'&&u.type==='warrior')d.tip+=' Страж готовит гарантированный блок следующего физического удара.';
 if(!d.baseDamage)return d;
 if(a!=='attack')d.baseDamage+=Math.floor(((u.level||1)-1)/2);
 if(u.power)d.baseDamage+=2;
 if(u.rage)d.baseDamage+=3;
 if(u.weaken)d.baseDamage=Math.max(1,d.baseDamage-2);
 if(d.bonusUndead&&t&&TYPES[t.type].fearless)d.baseDamage+=d.bonusUndead;
 if(u.sub==='swift'&&a==='frost')d.cost=1;
 if(u.sub==='elementalist'&&a==='blast')d.baseDamage+=3;
 if(u.type==='wolf'&&a==='attack'&&t&&s.units.some(v=>v.id!==u.id&&v.side===u.side&&v.type==='wolf'&&alive(v)&&distance(v,t)===1))d.baseDamage+=2;
 if(u.type==='boar'&&a==='attack'&&u.movedRound===s.round)d.baseDamage+=2;
 d.tip=d.tip.replace(/\d+–\d+/,d.baseDamage.toLocaleString('ru-RU'));
 return d;
}
function check(u,t,a){
 if(!u||!alive(u))return 'Герой без сознания';if(s.winner!==null)return 'Бой завершён';if(u.side!==s.side)return 'Сейчас ход другого отряда';if(u.skipped)return 'Остаток действий уже пропущен';
 if(u.type==='prisoner')return 'Пленник может только двигаться или пропускать действия';
 if(!['attack',...abilities(u)].includes(a))return 'Это действие недоступно герою';const d=spec(u,a,t);if(d.self)return 'Нажмите кнопку способности для применения к себе';if(u.ap<d.cost)return 'Недостаточно ОД';if(!t)return 'Выберите героя на поле';
 if(ACTIONS[a].tile)return 'Выберите свободный гекс';
 if(cooldownUntil(u,a)>s.round)return 'Приём перезаряжается';
 if(d.ally){if(t.side!==u.side)return 'Нужен союзник';if(t.evacuated||t.carriedBy)return 'Цель не находится на поле';if(d.kind==='heal'){if(!u.heals)return 'Лечение исчерпано';if(t.hp>=t.max&&!(d.cleanse&&(t.slow||t.weaken||t.exposed)))return 'Здоровье уже полное'}else{if(!alive(t))return 'Нужен союзник в сознании';if(t.protected)return 'Защита уже действует'}}
 else{if(t.side===u.side)return 'Нужен противник';if(!alive(t))return 'Цель уже без сознания'}
 if(blockedShot(u,d))return 'Рядом враг: отойдите хотя бы на клетку, чтобы стрелять';
 if(distance(u,t)>d.range)return 'Цель вне дальности';if(!los(u,t))return 'Скала перекрывает линию огня';return '';
}
function forecast(u,t,a){
 const err=check(u,t,a);if(err)return {ok:false,text:err};const d=spec(u,a,t);
 if(d.kind==='heal'){
   const amount=Math.min(d.amount,t.max-t.hp);
   return {ok:true,amount,text:`${t.name}: +${amount} ХП.${!alive(t)?' Подъём с 1 ОД.':''} ${d.cleanse?'Снимает замедление и ослабление.':''} Цена: ${d.cost} ОД.`};
 }
 if(d.kind==='ward')return {ok:true,text:`${t.name}: +20 ко всем защитам до конца следующего своего хода.${d.area?' Действует и на союзников рядом.':''} Цена: ${d.cost} ОД.`};
 const f=damageForecast(u,t,d), hits=d.hits||1;
 const result=hits>1?`${hits} удара по ${f.normalDamage}`:`${f.normalDamage} урона`;
 const block=f.block?` · блок ${Math.round(f.block*100)}% → ${f.blockedDamage} урона`:'';
 const critical=f.critChance?` · крит ${Math.round(f.critChance*100)}% → ${f.criticalDamage} урона`:'';
 const barrier=t.barrier?`Барьер ${t.barrier} поглощает урон до потери ХП. `:'';
 return {...f,ok:true,text:`${t.name}: ${result}. Уклонение ${Math.round(f.dodge*100)}%${block}${critical}.\nТип: ${DAMAGE[d.damage]}. Защита ${f.defense}${f.cover?' (укрытие +'+f.cover+')':''} → −${Math.round(f.reduction*100)}%.\n${barrier}Цена: ${d.cost} ОД.${a==='break'?' После удара: −20 физических защит.':a==='frost'?' После удара: замедление.':d.area?' Площадь: цель и враги в радиусе 1.':''}`};
}
function damageForecast(u,t,d){
 const critChance=d.noCrit?0:Math.min(1,s.critChance+(PROFILES[u.sub]?.crit||0)+(d.critBonus||0));
 const cover=distance(u,t)>1&&cell(t.q,t.r).kind==='cover'?(cell(t.q,t.r).fort?35:20):0;
 const rating=Math.max(0,defense(t,d.damage)+cover-(d.pierce||0)), res=reduction(rating);
 const afterArmor=d.baseDamage*(1-res);
 const criticalAfterArmor=afterArmor*Strike.criticalMultiplier;
 return {
   normalDamage:Strike.roundDamage(afterArmor), blockedDamage:Strike.roundDamage(afterArmor,true),
   criticalDamage:Strike.roundDamage(criticalAfterArmor), blockedCriticalDamage:Strike.roundDamage(criticalAfterArmor,true),
   defense:rating, cover, reduction:res, critChance,
   dodge:d.undodgeable?0:stats(t).dodge,
   block:Strike.blockChance(t.type,d.damage!=='magic',t.guardBlock),
 };
}
function hit(u,t,d){
 const f=damageForecast(u,t,d), {dodged,blocked,critical}=Strike.resolve({dodge:f.dodge,block:f.block,critical:f.critChance},rng);
 if(dodged){
   s.dodges++;
   effect(u,t,'Уклонение');
   log(`${t.name} уклоняется от «${d.name}».`);
   return {connected:false,damage:0,absorbed:0};
 }
 if(blocked){
   s.blocks++;
   t.guardBlock=false;
 }
 if(critical){
   s.crits++;
   if(!TYPES[t.type].fearless)t.stress=Math.min(100,(t.stress||0)+10);
 }
 const dmg=critical?(blocked?f.blockedCriticalDamage:f.criticalDamage):(blocked?f.blockedDamage:f.normalDamage);
 const absorbed=Math.min(t.barrier||0,dmg), hpLoss=Math.min(t.hp,dmg-absorbed);
 t.barrier=(t.barrier||0)-absorbed;
 t.hp-=hpLoss;
 s.damage+=hpLoss;
 s.absorbed+=absorbed;
 effect(u,t,(blocked?'Блок · ':'')+(critical?'Крит · ':'')+(absorbed?`Щит −${absorbed} / ХП −${hpLoss}`:'−'+hpLoss));
 log(`${u.name} → ${t.name}${critical?' · крит':''}${blocked?' · блок':''}: ${hpLoss} ХП${absorbed?', барьер поглотил '+absorbed:''} (${DAMAGE[d.damage]}, ${d.name}).`);
 if(!alive(t)){dropCargo(t);t.ap=0;t.stride=0;t.barrier=0;for(const h of s.units.filter(h=>h.side===t.side&&h.id!==t.id&&alive(h)&&!TYPES[h.type].fearless))h.stress=Math.min(100,h.stress+15);log(`${t.name} без сознания. Стресс товарищей +15.`)}
 return {connected:true,damage:hpLoss,absorbed,critical,blocked};
}
function finish(){
 if(s.winner!==null)return true;if(s.objective){const o=s.objective;if(o.prisoner.status==='evacuated'){const left=s.units.filter(u=>u.side===0&&!u.evacuated),guards=s.units.some(u=>u.side===1&&alive(u));if(!guards)return endObjective(0,'rescued-combat','Пленник спасён, охрана разбита. Победа!');if(!left.length)return endObjective(0,'rescued-withdrawal','Пленник и все герои эвакуированы. Успешный отход!')}if(o.prisoner.status==='free'&&!alive(o.prisoner))return endObjective(1,'prisoner-down','Пленник выведен из строя. Эвакуация сорвана.');if(o.prisoner.status==='recaptured')return endObjective(1,'recaptured','Охрана снова захватила пленника. Задача провалена.');if(o.escaped)return endObjective(1,'wagon-escaped','Повозка покинула поле с пленником. Перехват провален.');if(!s.units.some(u=>u.side===0&&alive(u)))return endObjective(1,'squad-defeated',o.prisoner.status==='evacuated'?'Пленник спасён, но оставшийся отряд выведен из строя.':'Отряд выведен из строя. Спасение не удалось.');if(!s.units.some(u=>u.side===1&&alive(u))&&!o.cleared){o.cleared=true;o.wagon.stopped=true;log('Сопровождение разбито, повозка остановилась. Освободите и выведите пленника.')}return false}
 for(const side of [0,1])if(!s.units.some(u=>u.side===side&&alive(u))){s.winner=1-side;s.ended=Date.now();for(const u of s.units.filter(u=>u.side===s.winner&&!alive(u))){u.hp=1;u.ap=0}log(s.winner===0?'Победа! Своих павших привели в чувство с 1 ХП.':'Поражение. Ваш отряд выведен из строя.');return true}return false;
}
function effect(u,t,label,heal=false){if(!$('motion').checked)return;const from=point(u.q,u.r),to=point(t.q,t.r),g=document.createElementNS('http://www.w3.org/2000/svg','g');g.setAttribute('class','hit-fx');g.innerHTML=`<line x1="${from.x}" y1="${from.y}" x2="${to.x}" y2="${to.y}" stroke="${heal?'#bce796':'#efc27f'}" stroke-width="4"/><text x="${to.x}" y="${to.y-38}" text-anchor="middle" fill="${heal?'#d0f5a8':'#ffe7a9'}" stroke="#15291f" stroke-width=".6" font-size="24" font-weight="bold">${label}</text>`;$('lab-effects')?.appendChild(g);setTimeout(()=>g.remove(),700)}
function apply(u,t,a){const f=forecast(u,t,a);if(!f.ok)return false;const d=spec(u,a,t);u.ap-=d.cost;s.actions++;
 if(d.kind==='heal'){const down=!alive(t);t.hp=Math.min(t.max,t.hp+d.amount);u.heals--;s.heals++;t.stress=Math.max(0,t.stress-(d.stressRelief||0));if(d.cleanse){t.slow=0;t.weaken=0;t.exposed=0}if(down){t.ap=t.side===s.side?1:0;t.wake=t.side!==s.side;s.revives++}effect(u,t,'+'+f.amount,true);log(`${u.name}: ${d.name}, ${t.name} +${f.amount} ХП.`);setCooldown(u,a)}
 else if(d.kind==='ward'){const targets=d.area?actors().filter(v=>v.side===u.side&&alive(v)&&distance(v,t)<=d.area):[t];for(const v of targets){v.protected=2;effect(u,v,'Защита',true)}setCooldown(u,a);log(`${u.name}: ${d.name}.`)}
 else{const targets=d.area?actors().filter(v=>v.side!==u.side&&alive(v)&&distance(v,t)<=d.area):[t];for(const v of targets)for(let i=0;i<(d.hits||1)&&alive(v);i++){const result=hit(u,v,d);if(result.connected){if(alive(v)){if(a==='break'||d.expose)v.exposed=1;if(a==='frost'||a==='web'||d.slow||['spider','spinner'].includes(u.type))v.slow=1;if(d.weaken)v.weaken=1;if(d.fire)v.burn=2}const drain=Math.max(d.drain||0,u.sub==='cultist'?1/3:0);if(drain)u.hp=Math.min(u.max,u.hp+Math.ceil(result.damage*drain))}}if(d.grantStride)u.stride+=d.grantStride;setCooldown(u,a)}
 finish();return true;
}
async function pause(ms){if($('motion').checked)await new Promise(resolve=>setTimeout(resolve,ms))}
async function move(u,dest,token){const p=paths(u).get(key(dest.q,dest.r));if(!p||!p.path.length||u.skipped)return false;const cost=movementAP(u,p.cost);u.ap-=cost;u.stride=(u.stride||0)+cost*3-p.cost;s.moves++;s.actions++;u.movedRound=s.round;
 for(const step of p.path){if(token!==serial)return false;u.q=step.q;u.r=step.r;if(u.carrying){const cargo=s.units.find(t=>t.id===u.carrying);cargo.q=u.q;cargo.r=u.r}const mine=s.mines.find(m=>m.q===u.q&&m.r===u.r&&m.side!==u.side);if(mine){s.mines=s.mines.filter(m=>m!==mine);hit(unit(mine.owner),u,{...ACTIONS.mine,name:'Мина',undodgeable:true});finish()}if(u.type==='prisoner'&&alive(u)&&s.winner===null&&s.objective.exits.some(t=>t.q===u.q&&t.r===u.r)){u.status='evacuated';u.ap=0;u.stride=0;selected=s.units.find(t=>t.side===0&&alive(t))?.id||'p0';log('Пленник в безопасности. Теперь разбейте охрану или выведите всех своих героев.');finish()}render();await pause(90);if(!alive(u)||s.winner!==null)break}log(`${u.name}: перемещение за ${cost} ОД; осталось ${u.stride} оплаченных шагов.`);return true;
}
function guard(u){if(u.ap<1||u.guard||!alive(u)||u.skipped)return false;u.ap--;u.guard=true;u.guardBlock=u.type==='warrior';s.actions++;log(`${u.name} занимает защитную стойку.`);return true}
async function chooseTile(q,r){if(editorActive){paintTile(q,r);return}if(busy||s.side!==0||s.winner!==null)return;const t=at(q,r),u=unit(selected);
 if(s.objective&&q===s.objective.wagon.q&&r===s.objective.wagon.r){notice='Повозка с пленником: подойдите соседним героем и используйте кнопки задачи.';render();return}
 if(t?.side===0&&!spec(u,mode)?.ally){selected=t.id;mode='move';notice='';hover=null;render();return}
 if(!u||!alive(u)){notice='Выберите героя в сознании.';render();return}
 if(spec(u,mode)?.tile){notice=deploy(u,{q,r},mode)?'':tileCheck(u,{q,r},mode);render();return}
 if(mode==='move'&&!t){const token=serial;busy=true;const ok=await move(u,{q,r},token);if(token!==serial)return;busy=false;notice=ok?'':'Гекс недоступен за оставшиеся ОД.';render();return}
 const a=mode==='move'&&t?.side===1?'attack':mode;
 const f=forecast(u,t,a);notice=f.ok?'':f.text;if(f.ok)apply(u,t,a);hover=null;render();
}
function setMode(a){if(editorActive||busy||s.side!==0||s.winner!==null)return;const u=unit(selected);if(!u||!alive(u))return;if(a==='powerarmor'){activateArmor(u);mode='move'}else if(ACTIONS[a]?.self){activateSelf(u,a);mode='move'}else if(a==='skip'){skip(u);mode='move'}else if(a==='guard'){guard(u);mode='move'}else mode=a;notice='';hover=null;render()}
function startSide(side){s.side=side;for(const u of actors().filter(u=>u.side===side)){u.guard=false;u.guardBlock=false;u.stride=u.sub==='thief'?2:0;u.skipped=false;u.ap=alive(u)?u.wake?1:u.type==='prisoner'?2:u.stress>=60&&!TYPES[u.type].fearless?2:3:0;u.wake=false;if(alive(u)&&TYPES[u.type].regenHP&&!u.burn){const amount=Math.min(u.max-u.hp,TYPES[u.type].regenHP);u.hp+=amount;if(amount)log(`${u.name}: регенерация +${amount} ХП.`)}if(alive(u)&&stats(u).barrier){const before=u.barrier;u.barrier=Math.min(stats(u).barrier,u.barrier+stats(u).regen);if(u.barrier>before)log(`${u.name}: барьер +${u.barrier-before} (${u.barrier}/${stats(u).barrier}).`)}}}
function endSide(side){for(const u of s.units.filter(u=>u.side===side)){u.exposed=Math.max(0,u.exposed-1);u.slow=Math.max(0,u.slow-1);u.power=Math.max(0,u.power-1);for(const k of ['protected','rage','smoke','weaken','burn'])u[k]=Math.max(0,(u[k]||0)-1)}}
function approach(u,enemies){
 // Plan beyond this turn: a useful route may initially increase distance.
 const all=paths(u,W*H*3),range=stats(u).range;let best=null;
 for(const v of all.values()){if(range>1&&engaged(u,v))continue;if(!enemies.some(t=>distance(v,t)<=range&&los(v,t)))continue;const score=v.cost-(cell(v.q,v.r).kind==='cover'?.2:0);if(!best||score<best.score)best={...v,score}}
 // Staying in an existing firing position wins over any paid side step.
 if(!best||!best.path.length)return null;let spent=0,dest=null;let from=u;for(const p of best.path){spent+=stepCost(u,cell(p.q,p.r),from);from=p;if(spent>movementBudget(u))break;dest=p}return dest;
}
async function enemyTurn(token){
 for(const u of s.units.filter(u=>u.side===1&&alive(u))){let count=0;
 while((u.ap>0||u.stride>0)&&s.winner===null&&count++<12){if(token!==serial)return;let acted=false;
 if(s.objective?.prisoner.status==='free'){if(capturePrisoner(u)){acted=true}else if(u.type==='warrior'||u.type==='rogue'){const dest=captureApproach(u);if(dest){acted=await move(u,dest,token)}}}
 const healAction=abilities(u).find(a=>ACTIONS[a].kind==='heal');if(!acted&&healAction&&u.heals){const allies=s.units.filter(t=>t.side===1&&t.hp<=t.max-10).sort((a,b)=>a.hp-b.hp);const t=allies.find(t=>!check(u,t,healAction));if(t){apply(u,t,healAction);acted=true}}
 if(!acted&&special(u)==='powerarmor'&&!u.power&&available(u,'powerarmor'))acted=activateArmor(u);
 if(!acted){const a=abilities(u).find(a=>ACTIONS[a].self&&ACTIONS[a].buff&&!u[ACTIONS[a].buff]&&available(u,a));if(a)acted=activateSelf(u,a)}
 if(!acted){const a=abilities(u).find(a=>ACTIONS[a].kind==='ward'&&available(u,a));if(a){const t=actors().find(t=>t.side===u.side&&alive(t)&&!check(u,t,a));if(t)acted=apply(u,t,a)}}
 if(!acted){const options=[];for(const a of ['attack',...abilities(u).filter(a=>ACTIONS[a].baseDamage)])for(const t of s.units.filter(t=>t.side===0&&alive(t))){const f=forecast(u,t,a);if(f.ok)options.push({a,t,score:f.normalDamage*(ACTIONS[a].hits||1)+(t.hp+(t.barrier||0)<=f.normalDamage*(ACTIONS[a].hits||1)?12:0)+(a==='frost'?2:0)})}options.sort((a,b)=>b.score-a.score);if(options[0]){apply(u,options[0].t,options[0].a);acted=true}}
 if(!acted&&special(u)==='mine'&&available(u,'mine')){const tile=Object.values(s.tiles).find(t=>!tileCheck(u,t)&&s.units.some(v=>v.side===0&&alive(v)&&distance(v,t)===1));if(tile)acted=deploy(u,tile)}
 if(!acted&&special(u)==='fortify'&&available(u,'fortify')){const tile=Object.values(s.tiles).find(t=>!tileCheck(u,t,'fortify')&&s.units.some(v=>v.side===0&&alive(v)&&distance(v,t)<=3));if(tile)acted=deploy(u,tile,'fortify')}
 if(!acted){const dest=approach(u,s.units.filter(t=>t.side===0&&alive(t)));if(dest){acted=await move(u,dest,token)}else acted=guard(u)}
 if(!acted)break;render();await pause(220);
 }}
 if(token!==serial)return;await advanceWagon(token);if(token!==serial)return;endSide(1);if(s.winner===null){s.round++;startSide(0);log(`Раунд ${s.round}. Ваш ход.`)}busy=false;mode='move';hover=null;render();
}
async function endTurn(){if(editorActive){notice='Закройте редактор кнопкой «Готово — к бою».';render();return}if(busy||s.side!==0||s.winner!==null)return;if(pending().length){pendingOpen=true;notice='Выполните оставшиеся действия или явно пропустите их.';render();return false}pendingOpen=false;busy=true;notice='';endSide(0);startSide(1);log('Противник выполняет действия.');render();await enemyTurn(serial)}
function activateArmor(u){if(!available(u,'powerarmor')||special(u)!=='powerarmor'||u.power)return false;u.ap-=2;u.power=2;setCooldown(u,'powerarmor');s.actions++;effect(u,u,'Броня',true);log(`${u.name}: силовая броня, +30 защиты и +2 базового урона.`);return true}
function tileCheck(u,t,a='mine'){if(!u||!alive(u)||u.side!==s.side||u.skipped)return 'Герой недоступен';const allowed=abilities(u).includes(a);if(!allowed||!ACTIONS[a]?.tile)return 'Это действие недоступно';if(!available(u,a))return 'Не хватает ОД или приём перезаряжается';const tile=cell(t.q,t.r);if(!tile||['rock','forest'].includes(tile.kind)||(tile.kind==='water'&&a!=='bridge')||occupied(t.q,t.r)||s.mines.some(m=>m.q===t.q&&m.r===t.r))return 'Нужен свободный проходимый гекс';if(a==='fortify'&&tile.kind!=='plain')return 'Укрепление ставится на обычный гекс';if(a==='bridge'&&!['mud','water'].includes(tile.kind))return 'Мостки ставятся на топь или воду';if(distance(u,t)>ACTIONS[a].range)return 'Гекс вне дальности';if(!los(u,t))return 'Скала перекрывает обзор';return ''}
function deploy(u,t,a='mine'){if(tileCheck(u,t,a))return false;u.ap-=ACTIONS[a].cost;setCooldown(u,a);s.actions++;if(a==='mine')s.mines.push({q:t.q,r:t.r,side:u.side,owner:u.id});if(a==='fortify'){cell(t.q,t.r).kind='cover';cell(t.q,t.r).fort=true}if(a==='bridge')cell(t.q,t.r).kind='bridge';log(`${u.name}: ${ACTIONS[a].name}.`);return true}
function rangeInfo(u,t){const d=spec(u,mode);if(editorActive||!u||!alive(u)||s.side!==0||busy||s.winner!==null||!d?.range)return null;if(distance(u,t)>d.range)return null;return blockedShot(u,d)?'engaged':['rock','forest'].includes(t.kind)||!los(u,t)?'blocked':'clear'}
function tileMarkup(t,reachable){const p=point(t.q,t.r),poly=Array.from({length:6},(_,i)=>{const a=(i*60-30)*Math.PI/180;return `${p.x+Math.cos(a)*39},${p.y+Math.sin(a)*39}`}).join(' '),u=at(t.q,t.r),path=reachable.get(key(t.q,t.r));let fill={plain:'#3a533a',rock:'#46504a',cover:'#496542',mud:'#55513b',bridge:'#6b5c3f',forest:'#314e3b',water:'#315b64',rubble:'#6a6150'}[t.kind];if(!editorActive&&path?.path.length&&mode==='move')fill='#526d45';const reach=rangeInfo(unit(selected),t);if(reach==='clear')fill=spec(unit(selected),mode).ally?'#356356':'#635639';if(reach==='blocked'||reach==='engaged')fill='#4a4141';const art=PixelSprites.tile(t,fill),mine=s.mines.find(m=>m.q===t.q&&m.r===t.r),bomb=mine?PixelSprites.object('mine'):null;
return `<g class="tile ${reach?'range-'+reach:''}" data-range="${reach||''}" data-height="${t.height||0}" tabindex="0" role="button" aria-label="Гекс ${t.q},${t.r}: ${u?u.name+', '+u.hp+' ХП':{plain:'поле',rock:'скала',cover:'укрытие',mud:'топь',bridge:'мостки',forest:'деревья',water:'вода',rubble:'осыпь'}[t.kind]}" data-q="${t.q}" data-r="${t.r}">${PixelSprites.img(art.png,p.x-40,p.y-40,art.w,art.h,'pixel-terrain')}<polygon points="${poly}" fill="transparent" stroke="${reach==='blocked'?'#c2b089':'transparent'}" stroke-width="1" ${reach==='blocked'?'stroke-dasharray="4 4"':''}/>${bomb?PixelSprites.img(bomb.png,p.x-14,p.y-8,28,24,'pixel-mine'):''}${t.height?`<text x="${p.x+20}" y="${p.y-12}" font-size="11" fill="#f1d799">▲${t.height}</text>`:''}${!editorActive&&path?.path.length&&mode==='move'&&!u?`<text class="tile-label" x="${p.x}" y="${p.y+5}" text-anchor="middle">${movementAP(unit(selected),path.cost)} ОД</text>`:''}</g>`;
}
const MAP_KEY='tuman.battle.layouts.v1',KINDS=['plain','rock','forest','cover','mud','water','rubble','bridge'];
function spawnCells(scene){if(scene==='convoy')return [[4,3],[4,4],[4,6],[3,7],[10,4],[11,6],[10,6],[12,4]];return scene==='rescue'?[[7,5],[5,5],[4,3],[4,7],[9,5],[11,3],[11,7],[12,5]]:Array.from({length:8},(_,i)=>[i<4?2:13,3+i%4])}
function validateLayout(data){if(!data||data.format!=='tuman-battle-map'||data.version!==1||data.width!==W||data.height!==H||!['equal','cover','rescue','convoy'].includes(data.scenario)||!Array.isArray(data.tiles)||data.tiles.length!==W*H)throw Error('Неверный формат поля: нужен JSON редактора, 16×10.');const seen=new Set(),tiles=data.tiles.map(t=>{if(!t||!Number.isInteger(t.q)||!Number.isInteger(t.r)||t.q<0||t.q>=W||t.r<0||t.r>=H||!KINDS.includes(t.kind)||!Number.isInteger(t.height)||t.height<0||t.height>2||seen.has(key(t.q,t.r)))throw Error('Повреждённые клетки поля.');seen.add(key(t.q,t.r));return {q:t.q,r:t.r,kind:t.kind,height:t.height,...(t.fort===true&&t.kind==='cover'?{fort:true}:{})}});if(spawnCells(data.scenario).some(([q,r])=>['rock','forest','water'].includes(tiles.find(t=>t.q===q&&t.r===r).kind)))throw Error('Нельзя ставить непроходимую поверхность на стартовые позиции героев.');if(data.scenario==='convoy'&&tiles.some(t=>reservedCell('convoy',t.q,t.r)&&(['rock','forest','water'].includes(t.kind)||t.height!==0)))throw Error('Маршрут повозки и выходы должны оставаться проходимыми на высоте 0.');return {format:data.format,version:1,width:W,height:H,scenario:data.scenario,tiles}}
function layoutSnapshot(){return {format:'tuman-battle-map',version:1,width:W,height:H,scenario:s.scenario,tiles:Object.values(s.tiles).map(t=>({q:t.q,r:t.r,kind:t.kind,height:t.height||0,...(t.fort?{fort:true}:{})}))}}
function loadLayouts(){for(const source of ['storage','embedded'])try{const raw=source==='storage'?localStorage.getItem(MAP_KEY):$('labMapData').textContent,data=raw?JSON.parse(raw):{};for(const scene of ['equal','cover','rescue','convoy'])if(data[scene]){const m=validateLayout(data[scene]);if(m.scenario===scene)customMaps[scene]=m}}catch{/* Browser storage may be unavailable; file import/export remains usable. */}}
function editorMessage(message){$('editorStatus').textContent=message}
function toggleEditor(){if(editorActive){editorActive=false;notice='Поле готово. Можно начинать бой.';render();return}if(busy||s.round!==1||s.side!==0||s.actions||s.winner!==null||s.units.some(u=>u.skipped)){notice='Редактор доступен до первого действия. Начните бой заново.';render();return}editorActive=true;mode='move';hover=null;notice='';render();editorMessage('Выберите поверхность и высоту, затем нажимайте клетки. Поле запоминается для текущего сценария при перезапуске.')}
function paintTile(q,r){if(!editorActive||busy||!cell(q,r))return false;if(at(q,r)||reservedCell(s.scenario,q,r)){editorMessage('Стартовая клетка, маршрут повозки или выход защищены от изменений.');return false}const kind=$('terrainBrush').value,height=$('heightBrush').value,t=cell(q,r);t.kind=kind;if(height!=='keep')t.height=Number(height);delete t.fort;customMaps[s.scenario]=layoutSnapshot();s.edits=(s.edits||0)+1;render();editorMessage(`Изменён гекс ${q},${r}, высота ${t.height}. Для хранения между запусками сохраните в браузере или скачайте JSON.`);return true}
function importLayout(data){if(!editorActive)throw Error('Сначала откройте редактор до начала боя.');const m=validateLayout(data);customMaps[m.scenario]=m;reset(m.scenario);editorActive=true;render();editorMessage('Поле загружено. Можно изменить его или закрыть редактор и начать бой.');return m}
function restoreLayout(){if(!editorActive)return;delete customMaps[s.scenario];try{localStorage.setItem(MAP_KEY,JSON.stringify(customMaps))}catch{}reset(s.scenario);editorActive=true;render();editorMessage('Восстановлено исходное поле сценария.')}
$('editorToggle').onclick=toggleEditor;
$('saveLayout').onclick=()=>{customMaps[s.scenario]=layoutSnapshot();try{localStorage.setItem(MAP_KEY,JSON.stringify(customMaps));editorMessage('Сохранено в этом браузере. Для переноса на другой компьютер скачайте поле JSON.')}catch{editorMessage('Хранилище браузера недоступно. Используйте «Скачать поле JSON».')}};
$('exportLayout').onclick=()=>download(JSON.stringify(layoutSnapshot(),null,2),'tuman-battle-map-'+s.scenario+'.json','application/json');
$('importLayout').onclick=()=>$('layoutFile').click();$('layoutFile').onchange=async e=>{const file=e.target.files[0];if(!file)return;try{if(file.size>100000)throw Error('Слишком большой файл поля.');importLayout(JSON.parse(await file.text()))}catch(error){editorMessage(error.message||'Не удалось загрузить поле.')}finally{e.target.value=''}};$('restoreLayout').onclick=restoreLayout;
function figure(u){return PixelSprites.figure(u)}
function reservedCell(scene,q,r){return scene==='convoy'&&((r===5&&q>=7)||(q===0&&r>=4&&r<=6))}
function occupied(q,r){return !!at(q,r)||!!(s.objective&&s.objective.wagon.q===q&&s.objective.wagon.r===r)}
const atExit=u=>!!s.objective?.exits.some(t=>t.q===u.q&&t.r===u.r);
function carryCheck(u,id){if(editorActive||busy||s.side!==0||s.winner!==null)return 'Действие сейчас недоступно';const t=s.units.find(v=>v.id===id);if(!s.objective||!u||!alive(u)||u.side!==0||u.type==='prisoner'||u.evacuated||u.skipped)return 'Выберите действующего героя';if(u.carrying)return 'Герой уже несёт товарища';if(u.ap<1)return 'Нужно 1 ОД';if(!t||t===u||t.side!==0||t.hp>0||t.evacuated||t.carriedBy)return 'Нужен товарищ без сознания';if(distance(u,t)>1)return 'Подойдите к раненому';return ''}
function carryHero(u,id){if(carryCheck(u,id))return false;const t=s.units.find(v=>v.id===id);u.ap--;u.stride=0;u.carrying=t.id;t.carriedBy=u.id;t.q=u.q;t.r=u.r;t.ap=0;t.stride=0;s.actions++;log(`${u.name} несёт ${t.name}. Движение дороже на 1 шаг за клетку.`);render();return true}
function dropCargo(u){if(!u.carrying)return;const t=s.units.find(v=>v.id===u.carrying);u.carrying=null;t.carriedBy=null;const place=dirs.map(([dq,dr])=>cell(u.q+dq,u.r+dr)).find(c=>c&&!['rock','forest','water'].includes(c.kind)&&Math.abs(c.height-cell(u.q,u.r).height)<=1&&!occupied(c.q,c.r));t.q=place?.q??u.q;t.r=place?.r??u.r;log(`${u.name} упал: ${t.name} остаётся на поле.`)}
function deliveryCheck(u){if(editorActive||busy||s.side!==0||s.winner!==null)return 'Действие сейчас недоступно';return !u?.carrying?'Герой никого не несёт':!alive(u)||u.evacuated?'Герой недоступен':!atExit(u)?'Нужен синий гекс выхода':''}
function deliverCargo(u){if(deliveryCheck(u))return false;const t=s.units.find(v=>v.id===u.carrying);t.evacuated=true;t.carriedBy=null;t.ap=0;t.stride=0;u.carrying=null;s.actions++;log(`${t.name} передан в безопасность. ${u.name} может вернуться за остальными.`);finish();render();return true}
function evacuationCheck(u){if(editorActive||busy||s.side!==0||s.winner!==null)return 'Действие сейчас недоступно';if(!u||!alive(u)||u.side!==0||u.type==='prisoner'||u.evacuated)return 'Выберите действующего героя';if(s.objective.prisoner.status!=='evacuated')return 'Сначала выведите пленника';if(!atExit(u))return 'Подойдите на синий гекс выхода';const others=s.units.filter(t=>t.side===0&&!t.evacuated&&t!==u&&t.id!==u.carrying);if(others.length&&!others.some(t=>alive(t)&&!t.carriedBy))return 'На поле останутся раненые. Сначала вынесите их.';return ''}
function evacuateHero(u){if(evacuationCheck(u))return false;if(u.carrying){const t=s.units.find(v=>v.id===u.carrying);t.evacuated=true;t.carriedBy=null;t.ap=0;t.stride=0;u.carrying=null}u.evacuated=true;u.ap=0;u.stride=0;s.actions++;log(`${u.name} эвакуирован и больше не участвует в бою.`);selected=actors().find(t=>t.side===0&&alive(t))?.id||'p0';finish();render();return true}

function setupConvoy(){const positions=spawnCells('convoy');s.units.forEach((u,i)=>Object.assign(u,{q:positions[i][0],r:positions[i][1]}));
 s.objective={type:'prisoner-convoy',wagon:{q:7,r:5,stopped:false},prisoner:{id:'prisoner',name:'Пленник',type:'prisoner',side:0,q:7,r:5,status:'caged',hp:16,max:16,ap:0,stride:0,stress:0,barrier:0,guard:false,power:0,exposed:0,slow:0,cooldown:0,heals:0,skipped:false,wake:false},exits:[{q:0,r:4},{q:0,r:5},{q:0,r:6}],escaped:false,cleared:false,outcome:null,resultText:'',stoppedBy:null};
 for(let q=7;q<W;q++)Object.assign(cell(q,5),{kind:'plain',height:0});for(const t of s.objective.exits)Object.assign(cell(t.q,t.r),{kind:'plain',height:0});
 for(const [q,r] of [[5,3],[5,7],[8,3],[10,7]])cell(q,r).kind='cover';for(const [q,r] of [[6,2],[8,8]])cell(q,r).kind='rock';for(const [q,r] of [[5,6],[7,7]])cell(q,r).kind='mud';
 log('Повозка идёт к правому краю. Остановите её, освободите пленника и выведите его через синие гексы слева.');
}
function endObjective(winner,outcome,text){if(s.winner!==null)return true;s.winner=winner;s.ended=Date.now();s.objective.outcome=outcome;s.objective.resultText=text;if(winner===0)for(const u of s.units.filter(u=>u.side===0&&u.hp<=0&&!u.evacuated)){u.hp=1;u.ap=0;u.stride=0}log(text);return true}
function releaseCell(){const w=s.objective.wagon;return dirs.map(([dq,dr])=>cell(w.q+dq,w.r+dr)).filter(t=>t&&!['rock','forest','water'].includes(t.kind)&&Math.abs(t.height-cell(w.q,w.r).height)<=1&&!occupied(t.q,t.r)&&!s.mines.some(m=>m.q===t.q&&m.r===t.r)).sort((a,b)=>a.q-b.q||Math.abs(a.r-5)-Math.abs(b.r-5))[0]}
function objectiveCheck(u,a){const o=s.objective;if(!o)return 'В этом бою нет повозки';if(editorActive||busy||s.side!==0||s.winner!==null)return 'Действие сейчас недоступно';if(a==='evacuateHero')return evacuationCheck(u);if(a==='deliverCargo')return deliveryCheck(u);if(a.startsWith('carry:'))return carryCheck(u,a.slice(6));if(a==='selectPrisoner')return o.prisoner.status==='free'?'':'Пленник ещё не освобождён';if(!u||!alive(u)||u.side!==0||u.type==='prisoner'||u.skipped)return 'Выберите героя в сознании';if(u.ap<2)return 'Нужно 2 ОД';if(distance(u,o.wagon)!==1)return 'Подойдите героем на соседний гекс повозки';if(a==='stopWagon')return o.wagon.stopped?'Повозка уже остановлена':o.prisoner.status!=='caged'?'Пленник уже освобождён':'';if(a==='freePrisoner'){if(!o.wagon.stopped)return 'Сначала остановите повозку';if(o.prisoner.status!=='caged')return 'Пленник уже освобождён';if(!releaseCell())return 'Нужен свободный гекс рядом с повозкой для выхода пленника';return ''}return 'Неизвестное действие'}
function objectiveAction(a){const u=unit(selected),error=objectiveCheck(u,a);if(error){notice=error;render();return false}const o=s.objective;if(a==='evacuateHero'){evacuateHero(u);return true}if(a==='deliverCargo'){deliverCargo(u);return true}if(a.startsWith('carry:')){carryHero(u,a.slice(6));return true}if(a==='selectPrisoner'){selected='prisoner';mode='move';hover=null;notice='Выведите пленника на синий выход слева. Не подпускайте охрану.';render();return true}u.ap-=2;s.actions++;if(a==='stopWagon'){o.wagon.stopped=true;o.stoppedBy='hero';log(`${u.name}: колёса выведены из строя. Повозка остановлена.`)}else{const dest=releaseCell();Object.assign(o.prisoner,{q:dest.q,r:dest.r,status:'free',ap:1,stride:0,skipped:false});o.releasedRound=s.round;log(`${u.name}: пленник освобождён. У него 1 ОД сейчас, 2 ОД в начале следующих ходов.`);selected='prisoner';mode='move'}notice='';render();return true}
function capturePrisoner(u){const o=s.objective;if(!o||o.prisoner.status!=='free'||s.side!==1||s.winner!==null||!alive(u)||u.side!==1||u.ap<2||distance(u,o.prisoner)!==1)return false;u.ap-=2;s.actions++;o.prisoner.status='recaptured';o.prisoner.ap=0;o.prisoner.stride=0;log(`${u.name}: пленник повторно захвачен.`);finish();return true}
function captureApproach(u){const p=s.objective.prisoner;let best=null;for(const v of paths(u,W*H*3).values()){if(distance(v,p)!==1)continue;if(!best||v.cost<best.cost)best=v}if(!best||!best.path.length)return null;let spent=0,dest=null,from=u;for(const t of best.path){spent+=stepCost(u,cell(t.q,t.r),from);from=t;if(spent>movementBudget(u))break;dest=t}return dest}
async function advanceWagon(token){const o=s.objective;if(!o||o.wagon.stopped||s.winner!==null||token!==serial)return;for(let i=0;i<2;i++){if(token!==serial||s.winner!==null)return;const next={q:o.wagon.q+1,r:5};if(occupied(next.q,next.r)){log('Путь повозки перекрыт героем: она не продвигается.');break}const tile=cell(next.q,next.r);if(!tile||['rock','forest','water'].includes(tile.kind)||Math.abs(tile.height-cell(o.wagon.q,o.wagon.r).height)>1){log('Маршрут повозки перекрыт рельефом.');break}o.wagon.q=next.q;const trap=s.mines.find(m=>m.q===next.q&&m.r===next.r&&m.side===0);if(trap){s.mines=s.mines.filter(m=>m!==trap);o.wagon.stopped=true;o.stoppedBy='mine';log('Мина повредила ходовую часть. Повозка остановлена, пленник не пострадал.')}if(o.prisoner.status==='caged'){o.prisoner.q=o.wagon.q;o.prisoner.r=o.wagon.r}if(o.wagon.q===W-1){o.escaped=true;finish()}render();await pause(200);if(o.wagon.stopped)break}if(token!==serial)return;if(!o.escaped&&!o.wagon.stopped)log(`Повозка продвинулась: до выхода ${W-1-o.wagon.q} клеток.`)}
function renderObjective(){const panel=$('objectivePanel'),layer=$('lab-objectives'),o=s.objective;panel.hidden=!o;if(!o){panel.innerHTML='';layer.replaceChildren();return}const u=unit(selected),p=o.prisoner,w=o.wagon;
 panel.innerHTML=`<div class="sectionline"><div><h2>Перехват пленника</h2><p><b>1.</b> ${w.stopped?'✓ Повозка остановлена':'Остановите повозку: до её выхода '+(W-1-w.q)+' клеток'} · <b>2.</b> ${p.status==='caged'?'Освободите пленника':p.status==='free'?'✓ Пленник свободен':p.status==='evacuated'?'✓ Пленник выведен':'Пленник захвачен'} · <b>3.</b> ${p.status==='evacuated'?'Разбейте охрану или эвакуируйте героев: '+s.units.filter(t=>t.side===0&&t.evacuated).length+'/4':'Выведите его на синие гексы слева'}</p><small>Охрану можно обойти. Остановка и освобождение — по 2 ОД соседнего героя. Мина тоже останавливает повозку. Повторный захват — провал. После спасения пленника нужно разбить охрану или вывести весь отряд. Перенос раненого: 1 ОД, +1 шаг за клетку.</small></div><div class="buttons">${['stopWagon','freePrisoner','selectPrisoner','evacuateHero',...(u?.carrying?['deliverCargo']:[]),...s.units.filter(t=>t.side===0&&t.hp<=0&&!t.evacuated&&!t.carriedBy).map(t=>'carry:'+t.id)].map(a=>{const error=objectiveCheck(u,a);return `<button data-objective="${a}" ${error?'disabled':''} title="${error||'Доступно'}">${{stopWagon:'Остановить · 2 ОД',freePrisoner:'Освободить · 2 ОД',selectPrisoner:'Управлять пленником',evacuateHero:'Эвакуировать героя',deliverCargo:'Передать раненого в безопасность'}[a]||'Нести '+s.units.find(t=>t.id===a.slice(6))?.name+' · 1 ОД'}</button>`}).join('')}</div></div>`;
 if(!layer.querySelector('#objectiveZones'))layer.innerHTML='<g id="objectiveZones" pointer-events="none"></g><g id="wagonGroup" class="unit"></g>';
 const from=point(7,5),end=point(15,5);$('objectiveZones').innerHTML=`<path d="M${from.x} ${from.y+22}L${end.x} ${end.y+22}" stroke="#dbb377" stroke-width="3" stroke-dasharray="9 9" opacity=".6"/>`+o.exits.map(t=>{const c=point(t.q,t.r),poly=Array.from({length:6},(_,i)=>{const a=(i*60-30)*Math.PI/180;return `${c.x+Math.cos(a)*36},${c.y+Math.sin(a)*36}`}).join(' ');return `<polygon points="${poly}" fill="#65b6cc" fill-opacity=".2" stroke="#94d3e3" stroke-width="3"/><text x="${c.x}" y="${c.y+4}" text-anchor="middle" fill="#d4f1f1" font-size="12">ВЫХОД</text>`}).join('')+`<text x="${end.x}" y="${end.y-35}" fill="#ecc995" text-anchor="middle" font-size="12">ВЫЕЗД →</text>`;
 const pos=point(w.q,w.r),wagon=$('wagonGroup');wagon.style.cssText=`transform:translate(${pos.x}px,${pos.y}px);${!$('motion').checked?'transition:none':''}`;const wagonArt=PixelSprites.wagon(w.stopped,p.status==='caged');wagon.innerHTML=PixelSprites.img(wagonArt.png,-48,-50,96,80,'pixel-wagon')+`<text y="-56" text-anchor="middle" font-size="12" fill="#f3dbad" stroke="#14271e" stroke-width="2" paint-order="stroke">${w.stopped?'ОСТАНОВЛЕНА':'ПОВОЗКА'}</text>`;
}
$('objectivePanel').onclick=e=>{const b=e.target.closest('[data-objective]');if(b&&!b.disabled)objectiveAction(b.dataset.objective)};

function unitsMarkup(){return actors().map(u=>{const p=point(u.q,u.r),t=stats(u),team=u.side?'#db8d78':'#8cc7d0';return `<g class="unit" data-unit="${u.id}" style="transform:translate(${p.x}px,${p.y}px);${!$('motion').checked?'transition:none;':''}">${PixelSprites.img(PixelSprites.object('shadow').png,-32,18,64,20,'pixel-shadow')}<ellipse cy="24" rx="25" ry="9" fill="none" stroke="${team}" stroke-width="${u.id===selected?3:1.5}"/>${u.id===selected?'<ellipse class="selected-ring" cy="24" rx="29" ry="12"/>':''}${u.barrier?PixelSprites.img(PixelSprites.object('barrier').png,-32,-62,64,88,'barrier-aura'):''}<g ${!alive(u)?'transform="translate(0,17) rotate(80) scale(.65)" opacity=".6"':''}>${figure(u)}${u.carrying?PixelSprites.img(PixelSprites.object('casualty').png,-26,-20,52,26,'pixel-casualty')+'<text x="0" y="-40" text-anchor="middle" fill="#e7b79e" font-size="11">РАНЕНЫЙ</text>':''}</g><rect x="-25" y="37" width="50" height="5" rx="2" fill="#18261e"/><rect x="-25" y="37" width="${50*u.hp/u.max}" height="5" fill="${u.side?'#e1a38a':'#b9d88c'}"/>${t.barrier?`<rect x="-25" y="44" width="50" height="3" fill="#1b3b4b"/><rect x="-25" y="44" width="${50*u.barrier/t.barrier}" height="3" fill="#8fd4e9"/>`:''}<text y="-70" text-anchor="middle" fill="#f3e4bf" font-size="12" paint-order="stroke" stroke="#14271e" stroke-width="2">${u.hp} ХП · ${u.ap} ОД</text></g>`}).join('')}

function render(){
 if(!unit(selected))selected=actors().find(t=>t.side===0&&alive(t))?.id||'p0';const u=unit(selected),reachable=!editorActive&&u&&alive(u)&&s.side===0&&!busy?paths(u):new Map();
 // Preserve SVG unit elements between updates so CSS can animate movement.
 const board=$('board');if(!board.querySelector('#lab-tiles'))board.innerHTML='<g id="lab-tiles"></g><g id="lab-objectives"></g><g id="lab-units"></g><g id="lab-effects"></g>';
 $('lab-tiles').innerHTML=Object.values(s.tiles).map(t=>tileMarkup(t,reachable)).join('');
 for(const old of [...$('lab-units').children])if(!actors().some(u=>u.id===old.dataset.unit))old.remove();const temp=document.createElementNS('http://www.w3.org/2000/svg','svg');temp.innerHTML=unitsMarkup();for(const fresh of [...temp.children]){const old=board.querySelector(`[data-unit="${fresh.dataset.unit}"]`);if(old){old.setAttribute('style',fresh.getAttribute('style'));old.innerHTML=fresh.innerHTML}else $('lab-units').appendChild(fresh)}
 renderObjective();
 $('phase').textContent=`Раунд ${s.round} · ${s.winner!==null?'Бой завершён':s.side===0?'Ваш ход':'Ход противника'}`;
 $('goal').textContent={equal:'Равные составы на открытом поле. Проверьте роли героев и цену сближения.',cover:'Используйте укрытия, обходите скалы, учитывайте стоимость топи.',rescue:'Поднимите Бориса, затем выиграйте бой. Решите, чем пожертвовать ради спасения.',convoy:'Остановите повозку → освободите пленника → выведите его на синие гексы слева. Затем разбейте охрану или эвакуируйте своих героев.'}[s.scenario];
 $('selected').textContent=u?`${u.name} · ${role(u)} · ${u.level||1} ур.`:'Выберите героя';$('stats').textContent=u?`${u.hp}/${u.max} ХП · ${u.ap}/${u.type==='prisoner'?2:3} ОД · ${u.stride} оплач. шагов · стресс ${u.stress}${u.slow?' · замедлен':''} · крит ${Math.round(Math.min(1,s.critChance+(PROFILES[u.sub]?.crit||0))*100)}%${u.carrying?' · несёт '+s.units.find(t=>t.id===u.carrying).name:''}${engaged(u)&&stats(u).range>1?' · дальние атаки заблокированы':''}\nБарьер ${u.barrier}/${stats(u).barrier||0} · уклонение ${Math.round((stats(u).dodge||0)*100)}%${u.type==='warrior'?' · блок '+Math.round(Strike.blockChance(u.type,true,u.guardBlock)*100)+'%':''}\n`+Object.keys(DAMAGE).map(k=>`${DAMAGE[k]}: ${defense(u,k)} (−${Math.round(reduction(defense(u,k))*100)}%)`).join(' · '):'';
 $('editorPanel').hidden=!editorActive;$('editorToggle').textContent=editorActive?'Готово — к бою':'Редактор поля';
 const disabled=editorActive||!u||!alive(u)||busy||s.side!==0||s.winner!==null;
 $('actions').innerHTML=u?(u.type==='prisoner'?['move','skip']:['move','attack',...abilities(u),'guard','skip']).map(a=>{const d=spec(u,a),shot=blockedShot(u,d),off=shot||disabled||u.skipped||u.ap<d.cost||(a==='guard'&&u.guard)||(a==='powerarmor'&&u.power)||(d.kind==='heal'&&!u.heals)||(d.buff&&u[d.buff])||(!['move','attack','guard','skip'].includes(a)&&cooldownUntil(u,a)>s.round);return `<button data-action="${a}" ${off?'disabled':''} class="${mode===a?'active':''}" title="${shot?'Рядом враг — сначала отойдите. ':''}${d.tip}">${d.name}<small>${shot?'Рядом враг · ':''}${a==='move'?'3 шага за 1 ОД':a==='skip'?'Явный пропуск':d.cost+' ОД'}${a==='attack'?' · дальн. '+d.range:d.kind==='heal'?' · осталось '+u.heals:!['move','guard','skip','bridge'].includes(a)&&cooldownUntil(u,a)>s.round?' · перезарядка '+(cooldownUntil(u,a)-s.round):''}</small></button>`}).join(''):'';
 $('forecast').textContent=hover&&u?forecast(u,unit(hover),mode==='move'?'attack':mode).text:mode==='move'?'Выберите светлый гекс для движения или противника для обычной атаки.':u?spec(u,mode).tip:'Выберите героя.';
 $('notice').textContent=notice;$('end').textContent=pending().length?`Остались действия · ${pending().length}`:'Завершить ход отряда';$('pending').innerHTML=pendingOpen?'<p>У этих героев остались действия:</p>'+pending().map(h=>`<div class="pending-row"><button data-pick="${h.id}">${h.name}: ${h.ap} ОД, ${h.stride} шаг.</button><button data-skip="${h.id}">Пропустить</button></div>`).join('')+(pending().length?'<button id="skipAll">Явно пропустить всем перечисленным</button>':''):'';$('end').disabled=editorActive||busy||s.side!==0||s.winner!==null;
 $('roster').innerHTML=s.units.map(h=>`<button class="hero ${h.side?'enemy':''} ${h.id===selected?'active':''}" data-select="${h.id}" ${h.side||busy||h.evacuated||h.carriedBy?'disabled':''}><svg class="roster-sprite" viewBox="-40 -64 80 96" aria-hidden="true">${figure(h)}</svg><b>${h.name}</b>${role(h)} · ${h.level||1} ур.<div class="hp"><i style="width:${h.hp/h.max*100}%"></i></div>${h.hp}/${h.max} ХП${stats(h).barrier?' · щит '+h.barrier:''}${stats(h).dodge?' · уклонение '+Math.round(stats(h).dodge*100)+'%':''} · ${h.ap} ОД · ${h.stride} шаг.${h.skipped?' · пропуск':''}${h.evacuated?' · эвакуирован':h.carriedBy?' · несут':h.hp<=0?' · без сознания':''}</button>`).join('');
 $('log').innerHTML=s.log.slice(0,12).map(t=>'<p>'+t+'</p>').join('');$('result').hidden=s.winner===null;
 if(s.winner!==null)$('result').textContent=`${s.objective?s.objective.resultText:s.winner===0?'Победа':'Поражение'} · ${s.round} раундов · ${s.actions} действий · подъёмов: ${s.revives}. Выберите другой сценарий или повторите этот.`;
}
$('board').addEventListener('click',e=>{const t=e.target.closest('[data-q]');if(t)chooseTile(+t.dataset.q,+t.dataset.r)});
$('board').addEventListener('keydown',e=>{if(['Enter',' '].includes(e.key)){const t=e.target.closest('[data-q]');if(t){e.preventDefault();chooseTile(+t.dataset.q,+t.dataset.r)}}});
function showHover(e){if(editorActive)return;const t=e.target.closest('[data-q]');if(!t)return;const h=at(+t.dataset.q,+t.dataset.r),u=unit(selected);hover=h?.id||null;if(spec(u,mode)?.tile&&u){$('forecast').textContent=tileCheck(u,{q:+t.dataset.q,r:+t.dataset.r},mode)||spec(u,mode).tip;return}if(h&&u)$('forecast').textContent=forecast(u,h,mode==='move'?'attack':mode).text;else if(u&&mode==='move'){const p=paths(u).get(key(+t.dataset.q,+t.dataset.r));$('forecast').textContent=p?.path.length?`Перемещение: ${movementAP(u,p.cost)} ОД (${p.cost} шагов). Останется ${u.ap-movementAP(u,p.cost)} ОД.`:'Этот гекс недоступен для перемещения.'}}
$('board').addEventListener('pointerover',showHover);$('board').addEventListener('focusin',showHover);
$('actions').addEventListener('click',e=>{const b=e.target.closest('[data-action]');if(b&&!b.disabled)setMode(b.dataset.action)});
$('roster').addEventListener('click',e=>{const b=e.target.closest('[data-select]');if(b&&!b.disabled&&s.side===0){selected=b.dataset.select;mode='move';hover=null;notice='';render()}});
$('pending').onclick=e=>{const b=e.target.closest('button');if(!b)return;if(b.id==='skipAll'){skipAll();return}if(b.dataset.skip)skip(unit(b.dataset.skip));if(b.dataset.pick){selected=b.dataset.pick;mode='move';hover=null;render()}};
for(const id of ['playerLevel','enemyLevel','enemyType','critChance','warriorSub','archerSub','rogueSub','mageSub'])$(id).onchange=()=>reset($('scenario').value);
$('playerLevel').onchange=()=>{if($('autoEnemyLevel').checked)$('enemyLevel').value=$('playerLevel').value;reset($('scenario').value)};$('enemyLevel').onchange=()=>{$('autoEnemyLevel').checked=false;reset($('scenario').value)};$('autoEnemyLevel').onchange=()=>reset($('scenario').value);
$('critChance').oninput=$('critChance').onchange=()=>{const chance=Math.max(0,Math.min(50,Number($('critChance').value)||0))/100;if(chance!==s.critChance)reset($('scenario').value)};
$('squad').onchange=()=>{$('engineerSub').disabled=$('squad').value!=='engineer';reset($('scenario').value)};$('engineerSub').onchange=()=>reset($('scenario').value);
let zoom=1;function mapZoom(){const b=$('board');b.style.width=Math.max(950,b.parentElement.clientWidth*zoom)+'px'}$('zoomIn').onclick=()=>{zoom=Math.min(2.5,zoom+.25);mapZoom()};$('zoomOut').onclick=()=>{zoom=Math.max(1,zoom-.25);mapZoom()};$('zoomFit').onclick=()=>{zoom=1;mapZoom()};window.addEventListener('resize',mapZoom);mapZoom();
$('end').onclick=endTurn;$('scenario').onchange=()=>reset($('scenario').value);$('restart').onclick=()=>reset(s.scenario);$('motion').onchange=render;
function download(text,name,type){const a=document.createElement('a'),url=URL.createObjectURL(new Blob([text],{type}));a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),30000)}
$('download').onclick=()=>{const clone=document.documentElement.cloneNode(true);clone.querySelector('#lab-tiles')?.replaceChildren();clone.querySelector('#lab-units')?.replaceChildren();clone.querySelector('#feedback').textContent='';for(const select of clone.querySelectorAll('select'))for(const option of select.options)option.toggleAttribute('selected',option.value===$(select.id).value);for(const input of clone.querySelectorAll('input[type=checkbox]'))input.toggleAttribute('checked',$(input.id).checked);clone.querySelector('#critChance').setAttribute('value',$('critChance').value);const maps={...customMaps,[s.scenario]:layoutSnapshot()};clone.querySelector('#labMapData').textContent=JSON.stringify(maps);download('<!doctype html>'+clone.outerHTML,'tuman-i-kosti-battle-lab-088.html','text/html')};
$('report').onclick=()=>download(JSON.stringify({version:'0.8.8-lab',combat:'block-dodge',scenario:s.scenario,playerLevel:s.playerLevel,enemyLevel:s.enemyLevel,enemyType:s.enemyType,critChance:s.critChance,crits:s.crits,loadout:s.loadout,engineerSubclass:s.sub,winner:s.winner,objective:s.objective?{outcome:s.objective.outcome,heroesEvacuated:s.units.filter(u=>u.side===0&&u.evacuated).map(u=>u.id),heroesRemaining:s.units.filter(u=>u.side===0&&!u.evacuated).map(u=>u.id),stage:s.objective.prisoner.status,wagonStopped:s.objective.wagon.stopped,stoppedBy:s.objective.stoppedBy,guardsAlive:s.units.filter(u=>u.side===1&&alive(u)).length}:null,rounds:s.round,seconds:Math.round(((s.ended||Date.now())-s.started)/1000),actions:s.actions,moves:s.moves,damage:s.damage,absorbed:s.absorbed,dodges:s.dodges,blocks:s.blocks,layout:layoutSnapshot(),heals:s.heals,revives:s.revives,heroes:s.units.map(u=>({name:u.name,role:role(u),level:u.level||1,side:u.side,hp:u.hp,evacuated:!!u.evacuated,carriedBy:u.carriedBy||null,carrying:u.carrying||null,barrier:u.barrier,dodge:stats(u).dodge||0,stress:u.stress,defenses:Object.fromEntries(Object.keys(DAMAGE).map(k=>[k,defense(u,k)]))})),feedback:$('feedback').value},null,2),'battle-feedback-'+s.scenario+'.json','application/json');
loadLayouts();reset($('scenario').value||'equal');return {get state(){return s},reset,forecast,paths,check,apply,guard,endTurn,chooseTile,setMode,render,get selected(){return selected},get busy(){return busy},distance,los,approach,skip,skipAll,pending,reduction,defense,damageForecast,movementAP,movementBudget,deploy,tileCheck,spec,role,activateArmor,engaged,blockedShot,hit,startSide,get editing(){return editorActive},toggleEditor,paintTile,importLayout,layoutSnapshot,restoreLayout,objectiveAction,objectiveCheck,advanceWagon,capturePrisoner,carryHero,carryCheck,evacuateHero,evacuationCheck,deliverCargo,stats,healing,abilities,cooldownUntil,syncPacks,figure};
})();
</script></body></html>

```

### `src/capital.js`

```js
// Capital construction, operating costs and class-wide development.
const Capital = (() => {
  const classes = {warrior:'plaza', rogue:'den', archer:'range', acolyte:'magicacademy',engineer:'engineering'};
  const legacy = ['prison','shield','fury','assassin','thief','sniper','swift','chapel','light','cult','elemental','cathedral','cathedral08'];
  const ranks = {recruit:['Стартовый уровень',7], attack:['Атака',3], defense:['Защита',3]};
  // Prototype values. Each row describes the two floor-2 options and the floor-3 capstone.
  const branchUpgrades={
    bastion:[{armor:5},{support:3},{armor:12}],
    berserker:[{damage:2},{penetration:10},{damage:6}],
    captain:[{support:3},{armor:4},{support:7}],
    assassin:[{penetration:12},{damage:2},{penetration:30}],
    thief:[{evasion:5},{damage:2},{evasion:12}],
    sniper:[{accuracy:5},{range:1},{accuracy:12,damage:3}],
    swift:[{evasion:4},{accuracy:6},{damage:4,evasion:6}],
    priest:[{heal:3},{mana:2},{heal:8}],
    cultist:[{magicPen:10},{mana:2},{magicPen:25,damage:2}],
    elementalist:[{damage:2},{magicPen:10},{damage:5,magicPen:15}],
    armorer:[{armor:5},{support:3},{armor:8,support:3}],
    demolitionist:[{damage:2},{penetration:15},{damage:5,penetration:15}],
    fortifier:[{support:3},{evasion:4},{support:7,armor:4}],
  };
  const names={armor:'броня, п.п.',support:'броня соседям, п.п.',damage:'урон',penetration:'пробивание, %',evasion:'уклонение, п.п.',accuracy:'точность, п.п.',range:'дальность',heal:'сила лечения',mana:'мана',magicPen:'маг. пробивание, %'};
  const describe=effect=>Object.entries(effect).map(([k,v])=>'+'+v+' '+names[k]).join(', ');
  const upkeep = {workshop:3,forge:3,tower:5,tower2:7,hospital:3,magicacademy:3,shrine:2};
  BUILD.walls={name:'Городские стены',icon:'▥',cost:80,work:24,effects:{}};
  BUILD.hall = {name:'Ратуша',icon:'♜',cost:40,work:16,effects:{},text:'Открывает этажи классовых зданий.'};
  BUILD.engineering={name:'Инженерный двор',icon:'⚒',cost:40,work:18,effects:{},text:'Улучшения Инженера и его подклассов.'};
  BUILD.tower2={name:'Высокая магическая башня',from:'tower',icon:'♜',cost:65,crystal:4,work:24,effects:{},text:'Открывает вторую ячейку зачарования экипировки.'};
  BUILD.tavern2={name:'Большая таверна',from:'tavern',icon:'☷',cost:55,work:22,effects:{},text:'Увеличивает число кандидатов до 15.'};
  BUILD.barracks={name:'Казармы',icon:'⚑',cost:45,work:20,effects:{armyArmor:3},text:'+3 п.п. физической брони всем героям.'};
  SUBS.armorer={name:'Бронник',cls:'engineer',text:'+8 п.п. брони.'};
  SUBS.demolitionist={name:'Подрывник',cls:'engineer',text:'+3 урона.'};
  SUBS.fortifier={name:'Фортификатор',cls:'engineer',text:'Соседние союзники получают +4 п.п. брони.'};
  for(const key of Object.values(classes)){
    BUILD[key].effects={};
    BUILD[key].text='Общие ранги класса и подклассов. Первый этаж открывает покупки рангов.';
  }
  SUBS.captain = {name:'Капитан',cls:'warrior',text:'Поддерживает соседних союзников.'};

  function init(f) {
    const t = f.town;
    t.projects ??= t.queue ? [{...t.queue, gold:BUILD[t.queue.id].cost, crystal:BUILD[t.queue.id].crystal||0, work:BUILD[t.queue.id].work}] : [];
    t.queue = null;
    if(t.wallQueue){
      const stone=t.wallQueue.type==='stone', work=stone?24:32, gold=stone?80:120;
      t.projects.push({id:'walls',kind:'walls',plot:f.city,work,gold,crystal:0,progress:Math.max(0,work-t.wallQueue.left*4),next:t.wallQueue.type});
      t.wallQueue=null;
    }
    t.hall ??= 1;
    t.classRanks ??= {};
    t.facings ??= {};
  }

  function level(f, cls) { return f.town.classRanks?.[cls]?.floor || 1; }
  function project(f,p,key,kind) {
    init(f);
    const t=f.town, d=BUILD[key], old=t.buildings[p];
    if (!d || t.projects.some(q=>q.plot===p)) return null;
    const cls=Object.keys(classes).find(c=>classes[c]===key);
    let next=1;
    if(['tavern2','tower2'].includes(key)&&t.hall<2) return null;
    if(kind==='walls') {
      if(p!==f.city||t.walls==='rampart')return null;
      const next=t.walls==='palisade'?'stone':'rampart';
      return {id:key,plot:p,kind,next,gold:next==='stone'?80:120,crystal:0,work:next==='stone'?24:32,progress:0};
    }
    if(kind==='hall') {
      if(p!==f.city || key!=='hall' || t.hall>=5) return null;
      next=t.hall+1;
    } else if(kind==='floor') {
      if(!cls || old!==key || level(f,cls)>=3) return null;
      next=level(f,cls)+1;
      const upgrades=t.classRanks[cls]||{};
      if(t.hall<next || (next===2 ? !(upgrades.attack||upgrades.defense||upgrades.recruit) : !Object.keys(upgrades).some(k=>k.endsWith(':1')||k.endsWith(':2')))) return null;
    } else {
      if(!t.plots.includes(p)||legacy.includes(key)||['hall','walls'].includes(key)||(d.from ? old!==d.from : !!old)) return null;
      if(Object.entries(t.buildings).some(([plot,b])=>+plot!==p&&lineage(b).includes(key))||t.projects.some(q=>q.id===key)) return null;
      if(d.requires?.some(k=>!hasBuilding(f,k))||d.requiresAny&&!d.requiresAny.some(k=>hasBuilding(f,k))||d.excludes?.some(k=>hasBuilding(f,k))) return null;
    }
    return {id:key,plot:p,kind,cls,next,gold:d.cost+(next-1)*15,crystal:d.crystal||0,work:d.work+(next-1)*8,progress:0,mirror:!!UI.cityMirror};
  }

  function enqueue(f,p,key,kind='build') {
    const q=project(f,p,key,kind);
    if(!q||!pay(f,q.gold,q.crystal)) return false;
    f.town.projects.push(q);
    if(f.id===0) FX.city(p,'start',BUILD[key].name+': в очереди');
    return true;
  }

  function edit(f,p,action) {
    init(f);
    const list=f.town.projects, index=list.findIndex(q=>q.plot===p), q=list[index];
    if(!q) return false;
    if(action==='pause') q.paused=!q.paused;
    if(action==='first') list.unshift(list.splice(index,1)[0]);
    if(action==='cancel') {
      const left=q.work-q.progress;
      f.gold+=Math.floor(q.gold*left/q.work);
      f.crystal+=Math.floor(q.crystal*left/q.work);
      list.splice(index,1);
    }
    return true;
  }

  function economy(f) {
    const e=cityEffects(f), buildings=Object.values(f.town.buildings);
    const due=buildings.reduce((sum,b)=>sum+(upkeep[b]||0),0);
    const paid=Math.min(due,f.gold+e.gold), efficiency=due?paid/due:1;
    const losses={};
    for(const b of buildings.filter(b=>upkeep[b])) {
      const loss={};
      for(const k of ['prod','crystal','food','heal']) {
        const full=lineage(b).reduce((sum,t)=>sum+(BUILD[t].effects[k]||0),0);
        loss[k]=full-Math.round(full*efficiency);
        e[k]-=loss[k];
      }
      if(Object.values(loss).some(Boolean)) losses[b]=loss;
    }
    return {...e,due,paid,efficiency,losses};
  }

  function tick(f,production) {
    init(f);
    const t=f.town;
    for(const q of [...t.projects]) {
      if(production<=0) break;
      const def=BUILD[q.id];
      if(q.paused || def.requires?.some(k=>!hasBuilding(f,k)) || def.requiresAny&&!def.requiresAny.some(k=>hasBuilding(f,k))) continue;
      const used=Math.min(production,q.work-q.progress);
      q.progress+=used;
      production-=used;
      if(q.progress<q.work) break;
      if(q.kind==='hall') t.hall=q.next;
      else if(q.kind==='walls') t.walls=q.next;
      else if(q.kind==='floor') (t.classRanks[q.cls]??={}).floor=q.next;
      else {
        t.buildings[q.plot]=q.id;
        t.facings[q.plot]=q.mirror;
      }
      if(['tavern','tavern2'].includes(q.id)) refreshCandidates(f);
      t.projects.splice(t.projects.indexOf(q),1);
      if(f.id===0) {
        FX.city(q.plot,'complete',BUILD[q.id].name);
        TurnFlow.notice('building','Работы завершены',BUILD[q.id].name,'city');
      }
      log(f.name+': выполнено — '+BUILD[q.id].name+'.');
    }
  }

  function bonuses(f,h) {
    init(f);
    const stored=h.classRanks??={};
    const live=hasBuilding(f,classes[h.cls]) ? f.town.classRanks[h.cls]||{} : {};
    for(const [k,v] of Object.entries(live)) {
      if(k==='attack'||k==='defense'||h.sub&&k.startsWith(h.sub+':')) stored[k]=Math.max(stored[k]||0,v);
    }
    return stored;
  }

  function branchEffects(h,stored){
    const out={};
    for(const [i,effect] of (branchUpgrades[h.sub]||[]).entries()){
      if(!stored[h.sub+':'+(i+1)])continue;
      for(const [k,v] of Object.entries(effect))out[k]=(out[k]||0)+v;
    }
    return out;
  }

  function buy(f,cls,key) {
    init(f);
    if(!classes[cls]||!hasBuilding(f,classes[cls])) return false;
    const tree=f.town.classRanks[cls]??={};
    const [sub,slot]=key.split(':');
    const branch=SUBS[sub]?.cls===cls&&!SUBS[sub].parent&&['1','2','3'].includes(slot);
    const limit=ranks[key]?.[1]||(branch&&level(f,cls)>=(slot==='3'?3:2)?1:0);
    const n=tree[key]||0;
    if(n>=limit||!pay(f,15+(n+1)*10+(branch?20:0))) return false;
    tree[key]=n+1;
    for(const h of f.armies.flatMap(a=>a.heroes)) if(h.cls===cls) bonuses(f,h);
    Development.updateCandidates(f);
    return true;
  }

  function demolish(f,p) {
    init(f);
    if(!f.town.buildings[p]||f.town.projects.some(q=>q.plot===p)) return false;
    const cls=Object.keys(classes).find(c=>classes[c]===f.town.buildings[p]);
    if(cls) {
      for(const h of f.armies.flatMap(a=>a.heroes)) if(h.cls===cls) bonuses(f,h);
      delete f.town.classRanks[cls];
    }
    delete f.town.buildings[p];
    delete f.town.facings[p];
    Development.updateCandidates(f);
    return true;
  }

  function branches(cls) { return Object.entries(SUBS).filter(([,s])=>s.cls===cls&&!s.parent); }
  function recruitLevel(f,cls) {
    return hasBuilding(f,classes[cls]) ? 1+(f.town.classRanks?.[cls]?.recruit||0) : 1;
  }
  function offeredSub(f,h,i) {
    const list=branches(h.cls);
    return h.level>=6&&list.length ? list[i%list.length][0] : null;
  }

  function cityPanel(f,p) {
    init(f);
    const t=f.town, e=economy(f), key=t.buildings[p], cls=Object.keys(classes).find(c=>classes[c]===key);
    const rows=t.projects.map(q=>`<li><b>${BUILD[q.id].name}</b> · ${q.progress}/${q.work} ОП${q.paused?' · пауза':''}
      ${button('capitalEdit',q.paused?'Возобновить':'Пауза',`data-pos="${q.plot}" data-v="pause"`)}
      ${button('capitalEdit','В начало',`data-pos="${q.plot}" data-v="first"`)}
      ${button('capitalEdit','Отменить',`data-pos="${q.plot}" data-v="cancel"`)}</li>`).join('');
    const row=(k,name,max)=> {
      const rank=t.classRanks[cls]?.[k]||0, cost=25+rank*10+(k.includes(':')?20:0);
      return button('classBuy',`${name} · ${rank}/${max} · ${cost} зол.`,`data-id="${cls}" data-v="${k}"`,rank>=max||f.gold<cost);
    };
    const floors=cls?Object.entries(ranks).map(([k,[name,max]])=>row(k,name,max)).join('')+
      (level(f,cls)>=2?branches(cls).map(([k,s])=>`<p>${s.name} ${branchUpgrades[k].map((effect,i)=>i===2&&level(f,cls)<3?'':row(k+':'+(i+1),describe(effect),1)).join(' ')}</p>`).join(''):''):'';
    return `<div class="card"><h3>Ратуша · уровень ${t.hall}/5</h3>
      ${button('capitalHall','Улучшить ратушу', '', !afford(f,project(f,f.city,'hall','hall')))}
      <p>ОП за ход ${e.prod} · содержание ${e.paid}/${e.due} зол. · эффективность ${Math.round(e.efficiency*100)}%</p>
      ${Object.entries(e.losses).map(([k,loss])=>`<p>${BUILD[k].name} · ${Object.entries(loss).filter(([,v])=>v).map(([m,v])=>'−'+v+' '+METRIC[m]).join(', ')}</p>`).join('')}
      <h3>Очередь строительства</h3>${rows?'<ol>'+rows+'</ol>':'<p>Очередь пуста</p>'}
      ${button('capitalMirror',UI.cityMirror?'Отражение включено':'Отразить новую постройку')}
      ${cls?`<h3>${BUILD[key].name} · этаж ${level(f,cls)}/3</h3>${floors}${button('capitalFloor','Добавить этаж',`data-pos="${p}"`,!afford(f,project(f,p,key,'floor')))}<p>Этаж 2 требует ратушу 2 и покупку на первом этаже. Этаж 3 требует ратушу 3 и покупку на втором этаже.</p>`:''}</div>`;
  }
  const afford=(f,q)=>q&&f.gold>=q.gold&&f.crystal>=q.crystal;
  return {afford,classes,legacy,init,project,enqueue,edit,economy,tick,demolish,branches,bonuses,branchEffects,buy,recruitLevel,offeredSub,level,cityPanel};
})();
Game.capital=Capital;

```

### `src/talents.js`

```js
// Personal choices are stored separately from any permanent city bonuses.
const Talents = (() => {
  const alternatives = ['Нападение','Защита','Поддержка'];
  const base = (h,l) => h.talents?.base?.[l];
  const unlocked = (h,l) => h.talents?.sub?.includes(l);
  function data(h) { return h.talents ??= {base:{},sub:[],active:h.cls==='warrior'?['power']:[]}; }

  function choose(h,l,k) {
    const t=data(h);
    if(!Number.isInteger(l)||l<2||l>h.level||l>8) return false;
    if(l<=5) {
      if(!alternatives.includes(k)||base(h,l)) return false;
      t.base[l]=k;
    } else {
      if(!h.sub||unlocked(h,l)||l>6&&!unlocked(h,l-1)) return false;
      t.sub.push(l);
    }
    return true;
  }

  function reset(h,f,a) {
    if(a.pos!==f.city||!pay(f,h.level*8)) return false;
    delete h.talents;
    data(h);
    return true;
  }

  function effects(h) {
    let attack=0, defense=0, support=0;
    for(let l=2;l<=5;l++) {
      const k=base(h,l);
      if(k===alternatives[0]) attack+=1;
      if(k===alternatives[1]&&(l!==2||h.cls!=='warrior')) defense+=3;
      if(k===alternatives[2]) support+=2;
    }
    attack+=(unlocked(h,6)?2:0)+(unlocked(h,8)?3:0);
    defense+=(unlocked(h,7)?5:0);
    return {attack,defense,support,counter:h.cls==='warrior'&&base(h,2)==='Защита',power:data(h).active.includes('power')};
  }

  function render(h,a) {
    const f=owner(a), t=data(h), rank=Capital.bonuses(f,h);
    const label=(l,k)=>k==='Нападение'?'+1 урона':k==='Защита'?(l===2&&h.cls==='warrior'?'Контратака после блока, раз за раунд':'+3 п.п. брони'):'+2 п.п. брони соседним союзникам';
    const row=l=>`<p>Уровень ${l} · ${base(h,l)||'выбор свободен'}</p><div class="stack">${alternatives.map(k=>button('talentChoose',k+' · '+label(l,k),`data-id="${h.id}" data-pos="${l}" data-v="${k}"`,h.level<l||!!base(h,l))).join('')}</div>`;
    const points=Math.max(0,Math.min(4,h.level-1))-Object.keys(t.base).length, subPoints=Math.max(0,h.level-5)-t.sub.length;
    return `<details><summary>Таланты · ${points} базовых / ${subPoints} подкласса</summary>
      <p>Ранги здания: атака ${rank.attack||0} · защита ${rank.defense||0}</p>
      ${[2,3,4,5].map(row).join('')}
      ${h.sub?[6,7,8].map((l,i)=>button('talentChoose',`Ур. ${l} · ${SUBS[h.sub].name} · ${['+2 урона','+5 п.п. брони','+3 урона'][i]}`,`data-id="${h.id}" data-pos="${l}"`,h.level<l||unlocked(h,l)||l>6&&!unlocked(h,l-1))).join(''):''}
      ${h.cls==='warrior'?button('talentPower',t.active.includes('power')?'Снять «Мощный удар»':'Экипировать «Мощный удар»',`data-id="${h.id}"`,a.pos!==f.city):''}
      ${button('talentReset','Сбросить · '+h.level*8+' зол.',`data-id="${h.id}"`,a.pos!==f.city||f.gold<h.level*8)}
    </details>`;
  }
  return {data,choose,reset,effects,render};
})();
Game.talents=Talents;

```

### `src/tactics.js`

```js
// Deterministic tactical terrain; generation does not consume gameplay randomness.
const Tactics=(()=>{
 const tiles={ground:{name:'Открытая земля',cost:1},tree:{name:'Густые деревья',blocked:true,blocksSight:true},rock:{name:'Скалы',blocked:true,blocksSight:true},water:{name:'Глубокая вода',blocked:true},bush:{name:'Кустарник',cost:1,cover:3},fence:{name:'Низкая ограда',cost:3,cover:6},rubble:{name:'Каменистая осыпь',cost:2,cover:3},mud:{name:'Грязь',cost:2},marsh:{name:'Топь',cost:3},shallow:{name:'Мелководье',cost:2},hill:{name:'Возвышенность',cost:2,height:1}};
 const profiles={plain:['rock','bush','mud'],forest:['tree','bush','mud'],hill:['rock','rubble','hill'],mountain:['rock','rubble','hill'],river:['water','bush','shallow'],swamp:['tree','bush','marsh']};
 function generate(terrain,pos){const profile=profiles[terrain]||profiles.plain;let seed=((S.seed||1)^Math.imul(pos+1,2654435761))>>>0;const rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;},out=Array(48).fill('ground'),slots=[];for(const y of [1,2,4])for(const x of [2,3])slots.push([x,y]);for(let i=slots.length-1;i>0;i--){const j=Math.floor(rng()*(i+1));[slots[i],slots[j]]=[slots[j],slots[i]];}for(let i=0;i<slots.length;i++){const [x,y]=slots[i],kind=profile[i%3];out[y*8+x]=out[y*8+7-x]=kind;}return{terrain,cells:out};}
 function field(b=S.battle){if(!b)return null;if(!b.field){b.field=generate(cell(b.meta.pos??0).terrain,b.meta.pos??0);for(const u of b.units)if(tiles[b.field.cells[u.pos]]?.blocked)b.field.cells[u.pos]='ground';}return b.field;}
 function tile(p,b=S.battle){const kind=field(b)?.cells[p]||'ground';return{kind,...(tiles[kind]||tiles.ground)};}
 function describe(p){const t=tile(p);return`${t.name}. ${t.blocked?'Непроходимо.':`Стоимость входа: ${t.cost} ${t.cost===1?'очко':'очка'} движения.`}${t.blocksSight?' Перекрывает линию видимости.':''}${t.cover?' Повышает шанс уклонения от дальних атак на '+t.cover*5+' п.п.':''}${t.height?' +1 к дальним атакам по целям ниже вас.':''}`;}
 function cube(p){const y=Math.floor(p/8),x=p%8-(y-(y&1))/2;return{x,y:-x-y,z:y};}
 function line(a,b){const n=dist(a,b,8),v=cube(a),w=cube(b),out=[];for(let i=0;i<=n;i++){const t=n?i/n:0,x=v.x+(w.x-v.x)*t+1e-6,y=v.y+(w.y-v.y)*t+1e-6,z=v.z+(w.z-v.z)*t-2e-6;let rx=Math.round(x),ry=Math.round(y),rz=Math.round(z);const dx=Math.abs(rx-x),dy=Math.abs(ry-y),dz=Math.abs(rz-z);if(dx>dy&&dx>dz)rx=-ry-rz;else if(dy>dz)ry=-rx-rz;else rz=-rx-ry;out.push(rz*8+rx+(rz-(rz&1))/2);}return out;}
 function sight(a,b){return line(a,b).slice(1,-1).every(p=>!tile(p).blocksSight);}
 function cover(u,t){const cover=dist(u.pos,t.pos,8)>1?(tile(t.pos).cover||0):0;return cover+(cover&&t.monster?.startsWith('goblin')?1:0);}
 function elevation(u,t){return dist(u.pos,t.pos,8)>1&&(tile(u.pos).height||0)>(tile(t.pos).height||0)?1:0;}
 function canAttack(u,t){return !!u&&!!t&&dist(u.pos,t.pos,8)<=u.range&&(!u.range||u.range===1||!activeUnits(S.battle,1-u.side).some(v=>dist(v.pos,u.pos,8)===1))&&sight(u.pos,t.pos);}
 function paths(u){const budget=u.attackedRound===S.battle.round?0:Math.max(0,(u.ap>0?3:0)-(u.snaredUntil>=S.battle.round?1:0)),costs=new Map([[u.pos,0]]),prev=new Map(),q=[u.pos];while(q.length){q.sort((a,b)=>costs.get(a)-costs.get(b));const p=q.shift();for(const i of nb(p,8,6)){const t=tile(i);if(t.blocked||activeUnits(S.battle,1-u.side).some(v=>v.pos===i))continue;const cost=costs.get(p)+(t.cost||1);if(cost>budget||cost>=(costs.get(i)??Infinity))continue;costs.set(i,cost);prev.set(i,p);q.push(i);}}for(const p of costs.keys())if(p!==u.pos&&occupiedBattle(p))costs.delete(p);return{costs,prev};}
 function route(u,to){const {costs,prev}=paths(u);if(!costs.has(to))return[];const out=[];for(let p=to;p!==u.pos;p=prev.get(p)){if(p==null)return[];out.unshift(p);}return out;}
 return{tiles,profiles,generate,field,tile,describe,line,sight,cover,elevation,canAttack,paths,route};
})();

```

### `src/turns.js`

```js
// Turn decisions and public start-of-turn news. Persisted separately from animation state.
const TurnFlow=(()=>{
 function flow(){if(!S)return null;let t=S.turnFlow;if(!t||t.turn!==S.turn){const previous=t;S.turnFlow=t={turn:S.turn,decisions:{},incoming:previous?.incoming||[],collecting:!!previous?.collecting,report:previous?.report||null};}return t;}
 const signature=value=>JSON.stringify(value);
 function legalBuild(){const f=player();if(f.town.projects?.some(q=>!q.paused))return null;for(const p of f.town.plots)for(const [b,d]of Object.entries(BUILD))if(f.gold>=d.cost&&f.crystal>=(d.crystal||0)&&buildPreview(f,p,b).ok)return{plot:p,building:b};return null;}
 function canAct(a){if(a.escort||!living(a).length||a.mp<1)return false;const siege=S.sieges.find(s=>s.attacker===a.id);if(siege)return false;return nb(a.pos).some(p=>{const hostile=S.factions.some(f=>!f.dead&&f.id!==0&&f.city===p)||allArmies().some(t=>t.owner!==0&&t.pos===p&&living(t).length);return hostile||TERRAIN[cell(p).terrain].cost<=a.mp;})||['camp','ruin','event','village'].includes(cell(a.pos).site?.type);}
 function tasks(includeDeferred=false){if(!S||S.result||!S.factions.length)return[];const f=player(),t=flow(),out=[],add=(key,title,text,route,data,sig)=>out.push({key,title,text,route,data,sig:signature(sig)});
  for(const [i,a]of f.armies.entries()){
   if(canAct(a))add('army:'+a.id,`Отряд ${i+1} ждёт приказа`,`${a.mp} очков перемещения. Отдайте приказ или оставьте отряд на месте до следующего хода.`,'army',a.id,[a.pos,a.mp,a.heroes.map(h=>h.id)]);
   if(Relations.activeConflict(a)&&a.mp>0&&living(a).length)add('conflict:'+a.id,`Спор в отряде ${i+1}`,a.conflict.reason+' После трёх ходов без решения верность спорящих снижается.','conflict',a.id,a.conflict);
   for(const h of a.heroes)if(availableSub(h,f).length)add('hero:'+h.id,`${h.name}: доступен подкласс`,'Откройте карточку героя и выберите постоянный подкласс.','hero',{army:a.id,hero:h.id},[h.level,h.sub,availableSub(h,f).map(([k])=>k)]);
  }
  const build=legalBuild();if(build)add('build','Город не строит здание','Есть место и ресурсы для строительства. Выберите постройку или решите копить ресурсы.','build',build,[f.gold,f.crystal,f.town.plots,f.town.buildings]);
  const plot=Array.from({length:256},(_,p)=>p).find(p=>dist(f.city,p)===2&&!f.town.plots.includes(p)&&nb(p).some(j=>f.town.plots.includes(j)));
  if(f.town.claims>0&&plot!=null)add('growth','Доступно расширение города',`Можно присоединить клеток: ${f.town.claims}. Выберите место во втором кольце.`,'growth',plot,[f.town.claims,f.town.plots]);
  if(S.decree&&!S.decree.status[0].main&&decreeInfo(f).ready)add('decree','Можно исполнить королевский указ',`${decreeInfo(f).title}. Основная часть ещё не сдана; срок — ход ${S.decree.deadline}.`,'king',null,S.decree.id);
  for(const s of S.sieges){const a=findArmy(s.attacker);if(a?.owner===0&&s.progress>=fortification(S.factions[s.defender]))add('siege:'+s.id,'Осада готова к штурму',`${CITIES[s.defender]}: можно начать штурм или продолжить ожидание.`,'hex',S.factions[s.defender].city,[s.id,s.progress]);}
  for(const v of Development.decisions())add(v.key,v.title,v.text,'development',v.data,v.sig);
  return out.map(v=>({...v,deferred:t.decisions[v.key]===v.sig})).filter(v=>includeDeferred||!v.deferred);
 }
 function defer(key){const v=tasks().find(v=>v.key===key);if(!v)return false;flow().decisions[key]=v.sig;save();render();return true;}
 function resume(key){delete flow().decisions[key];save();render();}
 function allDeferred(){for(const v of tasks())flow().decisions[v.key]=v.sig;save();render();}
 function openTasks(){const list=tasks(true),left=list.filter(v=>!v.deferred);show('turnTasks',`<div class="eyebrow">Ход ${S.turn} · приказы и решения</div><h2>${left.length?'Остались незавершённые действия':'Все решения приняты'}</h2><p>Ход продолжится, когда каждый доступный важный пункт будет выполнен или явно отложен на этот ход. Проверка обновляется после ваших действий.</p><div class="turn-task-list">${list.map(v=>`<div class="card turn-task ${v.deferred?'deferred':''}"><div><b>${esc(v.title)}</b><p class="muted">${esc(v.text)}</p>${v.deferred?'<small>Пропущено в этом ходу</small>':''}</div><div class="stack">${button('turnGo','Перейти',`data-id="${esc(v.key)}"`)}${v.deferred?button('turnResume','Вернуть в список',`data-id="${esc(v.key)}"`):button('turnDefer',v.route==='army'?'Оставить на месте':'Пропустить в этом ходу',`data-id="${esc(v.key)}"`)}</div></div>`).join('')||'<div class="rule">Все отряды получили приказы, доступные решения приняты.</div>'}</div><div class="stack">${button('end','Завершить ход →','',!!left.length,'gold')}</div>`);}
 function go(v){if(!v)return;closeModal();if(['army','conflict','hero'].includes(v.route)){const a=findArmy(v.route==='hero'?v.data.army:v.data);if(!a)return;UI.army=a.id;UI.selected=a.pos;Painter.home();render();if(v.route==='hero')renderRoster(v.data.hero);if(v.route==='conflict'){if(Relations.activeConflict(a))openEvent('conflict',a.pos,{...a.conflict});else say('Этот спор уже разрешён.');}}
  if(v.route==='build'){UI.cityPlot=v.data.plot;UI.building=v.data.building;renderCity();}
  if(v.route==='growth'){UI.cityPlot=v.data;renderCity();}
  if(v.route==='king')renderKing();if(v.route==='development'){UI.devTab=v.data||'research';Development.render();}
  if(v.route==='hex'){UI.selected=v.data;const a=S.sieges.map(s=>findArmy(s.attacker)).find(a=>a?.owner===0&&dist(a.pos,v.data)<=1);if(a)UI.army=a.id;Painter.focus(v.data);render();}
 }
 function check(){const t=flow();if(t.report?.pending){openReport();return false;}if(tasks().length){openTasks();return false;}return true;}
 function begin(){const t=flow();t.collecting=true;t.incoming=[];}
 function notice(kind,title,text,route=null,data=null){const t=flow();if(!t?.collecting)return;t.incoming.push({kind,title,text,route,data});}
 function finish(){const t=flow();t.collecting=false;t.decisions={};const f=player(),items=t.incoming.splice(0);
  if(S.turn>=S.decree.deadline-1&&!S.decree.status[0].main)items.push({kind:'king',title:'Приближается срок королевского указа',text:`${decreeInfo(f).title}: выполните основную часть до конца хода ${S.decree.deadline}.`,route:'king'});
  for(const a of player().armies)if(Relations.activeConflict(a)&&!items.some(v=>v.kind==='event'&&v.data===a.id))items.push({kind:'event',title:'Спор ждёт решения',text:a.conflict.reason,route:'conflict',data:a.id});
  for(const s of S.sieges){const a=findArmy(s.attacker);if(s.defender===0||a?.owner===0)items.push({kind:'siege',title:s.defender===0?'Столица в осаде':'Продолжается ваша осада',text:`${CITIES[s.defender]}: ${s.progress}/${fortification(S.factions[s.defender])} очков. ${s.progress>=fortification(S.factions[s.defender])?'Доступен штурм.':'Укрепления задерживают штурм.'}`,route:s.defender===0?'city':'hex',data:S.factions[s.defender].city});}
  for(const c of S.convoys.filter(c=>c.owner===0))if(!items.some(v=>v.kind==='convoy'&&v.data===c.id))items.push({kind:'convoy',title:'Ваша повозка в пути',text:`${c.cargo.map(h=>h.name).join(', ')}. До города примерно ${Math.ceil(path(c.pos,c.dest).length/2)} ход.`,route:'cargo'});
  t.report={turn:S.turn,pending:true,items};save();const state=S,report=t.report;FX.whenIdle(()=>{if(S===state&&flow().report===report&&report.pending&&!S.battle&&!S.aftermath&&!S.result)openReport();});
 }
 function openReport(){const report=flow().report;if(!report){say('Сводка появится в начале следующего хода.');return;}show('turnReport',`<div class="eyebrow">Начало хода ${report.turn}</div><h2>События нового хода</h2><p class="muted">Изменения за ход соперников и начало вашего хода.</p><div class="turn-news-list">${report.items.map((v,i)=>`<div class="card turn-news" data-kind="${esc(v.kind)}"><b>${esc(v.title)}</b><p>${esc(v.text)}</p>${v.route?button('turnNewsGo','Перейти',`data-pos="${i}"`):''}</div>`).join('')||'<div class="rule">Важных событий нет. Отряды восстановили очки перемещения.</div>'}</div><div class="stack">${button('turnReportDone','К приказам','','','gold')}</div>`);}
 function dismiss(){const r=flow()?.report;if(r)r.pending=false;save();if(UI.modal==='turnReport')closeModal();render();}
 function dispatch(action,key,index){if(action==='turnTasks'){openTasks();return true;}if(action==='turnReport'){openReport();return true;}if(action==='turnReportDone'){dismiss();return true;}if(action==='turnDefer'){defer(key);return true;}if(action==='turnResume'){resume(key);return true;}if(action==='turnGo'){go(tasks(true).find(v=>v.key===key));return true;}if(action==='turnNewsGo'){const v=flow().report?.items[index];dismiss();if(v){if(v.route==='city'){UI.cityPlot=player().town.plots[0];renderCity();}else if(v.route==='cargo')renderCargo();else if(v.route==='roster')renderRoster();else go({route:v.route,data:v.data});}return true;}return false;}
 function welcome(){const t=flow();t.report={turn:S.turn,pending:true,items:[{kind:'king',title:'Король объявил поиск преемника',text:decreeInfo(player()).title+'. '+decreeInfo(player()).text,route:'king'},{kind:'heroes',title:'Первый отряд готов',text:player().armies[0].heroes.map(h=>h.name).join(' и ')+': два героя первого уровня. Отдайте им приказ и выберите первую постройку.',route:'army',data:player().armies[0].id}]};save();openReport();}
 return{tasks,defer,resume,allDeferred,check,begin,notice,finish,openTasks,openReport,dismiss,dispatch,welcome,initialize:flow};
})();

```

### `src/painter.js`

```js
const Painter=(()=>{
 const R=55,Y=.72,SQ=Math.sqrt(3),img=new Image(),frames=ATLAS_META.frames;
 let ready=false,grid=false,zoom=1,focusPoint={x:220,y:130},battleCam=null,hover=null,battleHover=null,battleHoverId=null;
 const wp=(i,w=N)=>({x:SQ*R*(i%w+(Math.floor(i/w)%2)/2),y:R*1.5*Y*Math.floor(i/w)}),hash=(a,b)=>{let n=Math.imul(a+13,374761393)^Math.imul(b+37,668265263);n=Math.imul(n^(n>>>13),1274126177);return((n^(n>>>16))>>>0)/4294967295;};
 function poly(ctx,p,r=R){ctx.moveTo(p.x+SQ*r/2,p.y-r*Y/2);for(let j=1;j<6;j++){const a=(j*60-30)*Math.PI/180;ctx.lineTo(p.x+Math.cos(a)*r,p.y+Math.sin(a)*r*Y);}ctx.closePath();}
 function sprite(ctx,n,x,y,height,flip=false){if(!ready)return;const [sx,sy,sw,sh]=frames[n],w=height*sw/sh;ctx.save();ctx.translate(Math.round(x),Math.round(y));if(flip)ctx.scale(-1,1);ctx.drawImage(img,sx,sy,sw,sh,Math.round(-w/2),Math.round(-height),Math.round(w),Math.round(height));ctx.restore();}
 // World units keep their original footprint; the canvas backing store uses native pixels.
 function surface(cv){const w=cv.clientWidth/2,h=cv.clientHeight/2,dpr=window.devicePixelRatio||1,pw=Math.max(1,Math.round(w*2*dpr)),ph=Math.max(1,Math.round(h*2*dpr));if(cv.width!==pw||cv.height!==ph){cv.width=pw;cv.height=ph;}const ctx=cv.getContext('2d');ctx.setTransform(pw/w,0,0,ph/h,0,0);ctx.imageSmoothingEnabled=false;return{w,h,ctx};}
 function label(ctx,text,x,y,color='#ead49e',size=9){ctx.save();const t=ctx.getTransform(),dpr=window.devicePixelRatio||1,scale=Math.hypot(t.a,t.b)/dpr,fontSize=clamp(size*scale,12,22),px=Math.round(t.a*x+t.c*y+t.e)/dpr,py=Math.round(t.b*x+t.d*y+t.f)/dpr;ctx.setTransform(dpr,0,0,dpr,0,0);ctx.font=`600 ${fontSize}px system-ui,sans-serif`;const w=ctx.measureText(text).width+10;ctx.fillStyle='#203027ed';ctx.fillRect(px-w/2,py-fontSize,w,fontSize+6);ctx.fillStyle=color;ctx.textAlign='center';ctx.fillText(text,px,py+1);ctx.restore();}
 // Animate the two lower sprite regions around their hips; the source atlas is unchanged.
 function walker(ctx,n,x,y,height,flip,phase){if(phase==null){sprite(ctx,n,x,y,height,flip);return;}if(!ready)return;const [sx,sy,sw,sh]=frames[n],w=height*sw/sh,step=Math.sin(phase),lift=Math.abs(Math.cos(phase))*.6,hip=-height*.27;
  ctx.save();ctx.translate(x,y-lift);if(flip)ctx.scale(-1,1);
  // The torso leans a little into the movement, while the legs alternate their stride.
  ctx.save();ctx.beginPath();ctx.rect(-w,-height-4,w*2,height*.73+4);ctx.clip();ctx.translate(step*.45,0);ctx.rotate(.025);ctx.drawImage(img,sx,sy,sw,sh,-w/2,-height,w,height);ctx.restore();
  for(let leg=0;leg<2;leg++){const direction=leg?-1:1,pivot=(leg?.18:-.18)*w;ctx.save();ctx.translate(pivot,hip);ctx.rotate(direction*step*.2);ctx.translate(-pivot,-hip);ctx.beginPath();ctx.rect(leg?0:-w/2,hip,w/2,height*.27+4);ctx.clip();ctx.drawImage(img,sx,sy,sw,sh,-w/2,-height,w,height);ctx.restore();}
  ctx.restore();}

 function terrain(ctx,t,p,i){const base=TERRAIN[t].color,opacity=ctx.globalAlpha;ctx.save();ctx.beginPath();poly(ctx,p,R+.7);ctx.clip();ctx.fillStyle=base;ctx.fillRect(p.x-R,p.y-R,R*2,R*2);const pal=t==='river'?['#7aa19a','#98b5a0','#426e70']:t==='forest'?['#637748','#738454','#3b5436']:['#87905c','#798454','#9c9d6c'];for(let k=0;k<90;k++){const x=Math.floor(p.x-R+hash(i,k)*R*2),y=Math.floor(p.y-R*Y+hash(k,i+5)*R*Y*2);ctx.fillStyle=pal[k%3];ctx.globalAlpha=.4*opacity;ctx.fillRect(x,y,t==='river'?5:3,1);if(k%18===0&&t==='plain'){ctx.globalAlpha=.7*opacity;ctx.fillStyle='#c0af72';ctx.fillRect(x,y-2,2,2);}}ctx.restore();}
 function shadow(ctx,x,y,r=17){ctx.fillStyle='#1b332750';ctx.beginPath();ctx.ellipse(x,y,r,r*.26,0,0,Math.PI*2);ctx.fill();}
 function arrowLine(ctx,points,color,width){if(points.length<2)return;ctx.strokeStyle=color;ctx.lineWidth=width;ctx.lineJoin='round';ctx.lineCap='round';ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.stroke();}
 function monster(ctx,key,x,y,height=58,flip=false,phase=null){const d=Bestiary.species[key]||Bestiary.species.bandit,kind=d.look;if(kind==='bandit'){sprite(ctx,d.range>1?10:13,x,y,height,flip);return;}ctx.save();ctx.translate(x,y);ctx.scale((flip?-1:1)*height/48,height/48);const stride=phase==null?0:Math.sin(phase)*3;ctx.lineJoin='round';ctx.lineCap='round';ctx.lineWidth=3;ctx.strokeStyle='#263027';
  const polygon=(points,color)=>{ctx.fillStyle=color;ctx.beginPath();points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();ctx.fill();};
  if(kind==='wolf'||kind==='boar'){const boar=kind==='boar',fur=boar?'#7b6652':'#9baca0';ctx.strokeStyle=boar?'#493d32':'#4e5c54';ctx.lineWidth=5;for(const [j,xx]of [-13,-4,9,16].entries()){ctx.beginPath();ctx.moveTo(xx,-13);ctx.lineTo(xx+(j%2?stride:-stride),-2);ctx.stroke();}ctx.fillStyle=fur;ctx.beginPath();ctx.ellipse(0,-17,22,10,0,0,Math.PI*2);ctx.fill();polygon([[13,-22],[25,-28],[29,-17],[24,-10],[13,-13]],fur);polygon([[17,-23],[16,-33],[24,-26]],'#65776b');polygon([[-18,-18],[-29,-25],[-24,-13]],fur);ctx.fillStyle='#ece4cb';ctx.fillRect(23,-17,6,3);if(boar){polygon([[25,-13],[32,-18],[29,-9]],'#efdfb8');ctx.strokeStyle='#4b4034';for(let j=0;j<6;j++){ctx.beginPath();ctx.moveTo(-13+j*5,-23);ctx.lineTo(-14+j*5,-28);ctx.stroke();}}ctx.fillStyle='#292c24';ctx.fillRect(23,-22,2,2);}
  else if(kind==='spider'){ctx.strokeStyle='#655446';ctx.lineWidth=2.5;for(let j=0;j<4;j++)for(const side of [-1,1]){ctx.beginPath();ctx.moveTo(side*5,-12);ctx.lineTo(side*(17+j*2),-24+j*6+(j%2?stride:-stride));ctx.lineTo(side*(26-j),-1+j%2*3);ctx.stroke();}ctx.fillStyle='#54493d';ctx.beginPath();ctx.ellipse(-3,-17,13,10,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#8c7655';ctx.beginPath();ctx.ellipse(7,-10,8,7,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#dfb47e';ctx.fillRect(11,-14,3,2);ctx.fillRect(10,-8,3,2);}
  else if(kind==='skeleton'){ctx.strokeStyle='#e0d5ac';ctx.lineWidth=3;for(const [side,offset]of [[-1,stride],[1,-stride]]){ctx.beginPath();ctx.moveTo(side*4,-18);ctx.lineTo(side*7,-9);ctx.lineTo(side*8+offset,-1);ctx.moveTo(side*4,-31);ctx.lineTo(side*12,-22);ctx.lineTo(side*14,-14);ctx.stroke();}ctx.beginPath();ctx.moveTo(0,-34);ctx.lineTo(0,-16);for(let j=0;j<4;j++){ctx.moveTo(-6,-29+j*3);ctx.lineTo(6,-29+j*3);}ctx.stroke();ctx.fillStyle='#e5d9b4';ctx.beginPath();ctx.ellipse(0,-39,7,8,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#433e31';ctx.fillRect(-4,-42,3,3);ctx.fillRect(2,-42,3,3);ctx.strokeStyle='#b7b8a5';ctx.beginPath();ctx.moveTo(14,-12);ctx.lineTo(20,-35);ctx.stroke();}
  else {const ogre=kind==='ogre',zombie=kind==='zombie',kobold=kind==='kobold',skin=ogre?'#a5a077':zombie?'#909a70':kobold?'#b98352':'#8ea85e',width=ogre?13:8;ctx.strokeStyle=skin;ctx.lineWidth=ogre?8:5;for(const side of [-1,1]){ctx.beginPath();ctx.moveTo(side*5,-16);ctx.lineTo(side*(ogre?9:6)+(side>0?stride:-stride),-2);ctx.moveTo(side*width,-30);ctx.lineTo(side*(width+5),-13);ctx.stroke();}polygon([[-width,-34],[width,-34],[width+2,-15],[-width,-15]],zombie?'#645f47':ogre?'#716447':'#63583b');ctx.fillStyle=skin;ctx.beginPath();ctx.ellipse(0,-40,ogre?11:9,ogre?10:8,0,0,Math.PI*2);ctx.fill();if(!ogre&&!zombie){polygon([[-7,-43],[-18,-46],[-10,-36]],skin);polygon([[7,-43],[18,-46],[10,-36]],skin);}ctx.fillStyle='#d7cc90';ctx.fillRect(-5,-42,3,2);ctx.fillRect(3,-42,3,2);ctx.fillStyle='#453d2b';ctx.fillRect(-4,-35,8,2);if(kobold)polygon([[5,-40],[15,-36],[7,-32]],skin);ctx.strokeStyle=ogre?'#745236':'#bdb798';ctx.lineWidth=ogre?7:2;ctx.beginPath();ctx.moveTo(width+6,-10);ctx.lineTo(width+11,ogre?-40:-37);ctx.stroke();if(d.range>1){ctx.strokeStyle='#bd9b5f';ctx.lineWidth=2;ctx.beginPath();ctx.arc(width+8,-25,12,-Math.PI/2,Math.PI/2);ctx.stroke();}}
  ctx.restore();}
 function lair(ctx,family,x,y,h){const f=Bestiary.families[family]||Bestiary.families.bandits;if(family==='bandits'){sprite(ctx,7,x,y,h);return;}if(family==='undead')sprite(ctx,5,x,y,h);else if(family==='spiders'){sprite(ctx,3,x,y,h);ctx.strokeStyle='#c9d4bfaa';ctx.lineWidth=1;for(let i=0;i<6;i++){const a=i*Math.PI/3;ctx.beginPath();ctx.moveTo(x,y-28);ctx.lineTo(x+Math.cos(a)*24,y-28+Math.sin(a)*18);ctx.stroke();}for(const r of [9,17,24]){ctx.beginPath();ctx.ellipse(x,y-28,r,r*.75,0,0,Math.PI*2);ctx.stroke();}}else if(['goblins','kobolds','ogres'].includes(family))sprite(ctx,7,x,y,h);else{ctx.fillStyle='#777c66';ctx.beginPath();ctx.ellipse(x,y-12,30,20,0,Math.PI,Math.PI*2);ctx.fill();ctx.fillStyle='#26372c';ctx.beginPath();ctx.ellipse(x,y-10,16,13,0,Math.PI,Math.PI*2);ctx.fill();}monster(ctx,f.pack[0],x+17,y+10,32,false);}
 function windTime(){return FX.settings.enabled?performance.now()/1000:0;}
 function grass(ctx,p,i){if(cell(i).terrain!=='plain'&&cell(i).terrain!=='swamp')return;const time=windTime();ctx.save();ctx.lineWidth=.8;for(let j=0;j<6;j++){const x=p.x-32+hash(i,j+90)*64,y=p.y-17+hash(j,i+90)*32,phase=time*1.2+hash(i,j)*6,sway=time?Math.sin(phase)*2.7:0;ctx.strokeStyle=j%2?'#b0b77c':'#8da16b';ctx.beginPath();ctx.moveTo(x-1,y+3);ctx.quadraticCurveTo(x+sway*.5,y-1,x+sway,y-5);ctx.moveTo(x+1,y+3);ctx.quadraticCurveTo(x+sway*.7+2,y,x+sway+3,y-3);ctx.stroke();}ctx.restore();}
 function windTree(ctx,n,x,y,height){ctx.save();ctx.translate(x,y);const time=windTime();if(time)ctx.rotate(Math.sin(time*.85+x*.013+y*.006)*.018+Math.sin(time*1.7+x*.01)*.004);sprite(ctx,n,0,0,height);ctx.restore();}
 function mill(ctx,x,y,h){ctx.save();ctx.translate(x,y);ctx.scale(h/82,h/82);ctx.lineJoin='round';ctx.lineWidth=1.6;ctx.strokeStyle='#493c28';ctx.fillStyle='#6f7154';ctx.beginPath();ctx.ellipse(0,0,23,7,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#c1ad7b';ctx.beginPath();ctx.moveTo(-19,-3);ctx.lineTo(-13,-56);ctx.lineTo(12,-56);ctx.lineTo(19,-3);ctx.closePath();ctx.fill();ctx.stroke();ctx.fillStyle='#8e8058';ctx.beginPath();ctx.moveTo(7,-55);ctx.lineTo(18,-3);ctx.lineTo(10,1);ctx.lineTo(2,-53);ctx.closePath();ctx.fill();ctx.fillStyle='#a96032';ctx.beginPath();ctx.moveTo(-20,-53);ctx.lineTo(-1,-73);ctx.lineTo(18,-53);ctx.closePath();ctx.fill();ctx.stroke();ctx.strokeStyle='#784929';for(let j=0;j<3;j++){ctx.beginPath();ctx.moveTo(-15+j*5,-56-j*4);ctx.lineTo(12-j*3,-56-j*4);ctx.stroke();}ctx.fillStyle='#473b2a';ctx.fillRect(-7,-20,11,18);ctx.fillStyle='#e6bf67';ctx.fillRect(-8,-42,7,10);ctx.strokeStyle='#685037';ctx.strokeRect(-8,-42,7,10);ctx.fillStyle='#998e69';for(let j=0;j<8;j++)ctx.fillRect(-15+(j*13)%30,-8-Math.floor(j/3)*12,6,2);
  ctx.translate(1,-49);ctx.rotate(windTime()*.18+.4);for(let j=0;j<4;j++){ctx.save();ctx.rotate(j*Math.PI/2);ctx.fillStyle='#e0d2a5';ctx.strokeStyle='#745334';ctx.lineWidth=1.4;ctx.beginPath();ctx.moveTo(3,-5);ctx.lineTo(5,-34);ctx.lineTo(15,-33);ctx.lineTo(10,-7);ctx.closePath();ctx.fill();ctx.stroke();ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(5,-34);for(let k=0;k<4;k++){ctx.moveTo(5,-11-k*6);ctx.lineTo(12,-10-k*6);}ctx.stroke();ctx.restore();}ctx.fillStyle='#775439';ctx.beginPath();ctx.arc(0,0,4,0,Math.PI*2);ctx.fill();ctx.restore();}
 function draw(){const cv=$('map');if(!cv.clientWidth||!cv.clientHeight)return;const{w,h,ctx}=surface(cv);ctx.fillStyle='#253c2d';ctx.fillRect(0,0,w,h);if(!S){ctx.fillStyle='#486047';for(let k=0;k<100;k++)ctx.fillRect(hash(k,3)*w,hash(k,7)*h,2,1);return;}const f=player(),selected=army(),props=[],troops=[];ctx.save();ctx.translate(w/2,h/2);ctx.scale(zoom,zoom);ctx.translate(-focusPoint.x,-focusPoint.y);
 for(let i=0;i<256;i++){const propStart=props.length,p=wp(i);if(Math.abs(p.x-focusPoint.x)>w/2/zoom+130||Math.abs(p.y-focusPoint.y)>h/2/zoom+160)continue;const c=cell(i),city=S.factions.find(t=>t.city===i),known=f.seen[i]||city||c.site?.type==='court';if(known){ctx.fillStyle='#2a4032';ctx.beginPath();poly(ctx,p,R+.7);ctx.fill();ctx.globalAlpha=FX.revealAlpha(i);terrain(ctx,city?'plain':c.terrain,p,i);grass(ctx,p,i);ctx.globalAlpha=1;}else{ctx.fillStyle=['#293f30','#2d4333'][i%2];ctx.beginPath();poly(ctx,p,R+1);ctx.fill();}if(known&&c.terrain==='forest'&&!city){for(let j=0;j<2;j++)props.push({n:(i+j)%4?3:4,x:p.x+(j?22:-22),y:p.y+(j?10:-10),h:85+hash(i,j)*20});}if(city){props.push({n:1,x:p.x,y:p.y+10,h:102,label:CITIES[city.id],color:COLORS[city.id]});}else if(known&&c.site){const s=c.site;if(s.type==='village'){props.push({n:0,x:p.x-15,y:p.y+10,h:78,label:S.villages[s.id].name});props.push({n:2,x:p.x+35,y:p.y-10,h:82});}else if(s.type==='court')props.push({n:1,x:p.x,y:p.y+8,h:125,label:'Королевский двор'});else if(s.type==='camp'&&!s.cleared)props.push({n:7,creatureFamily:s.family||'bandits',x:p.x,y:p.y+9,h:66,label:Bestiary.families[s.family||'bandits'].lair});else if(s.type==='ruin')props.push({n:5,x:p.x,y:p.y+10,h:64});else if(s.type==='event')props.push({n:6,x:p.x,y:p.y+7,h:50});}
 for(let j=propStart;j<props.length;j++)props[j].alpha=FX.revealAlpha(i);
 if(known&&grid){ctx.strokeStyle='#d1c99335';ctx.lineWidth=.7;ctx.beginPath();poly(ctx,p,R-1);ctx.stroke();}if(i===UI.selected||i===hover){ctx.strokeStyle=i===UI.selected?'#f2ce7c':'#d1d0a2';ctx.lineWidth=i===UI.selected?2:1;ctx.beginPath();poly(ctx,p,R-1);ctx.stroke();}}
 // Walls follow only outer edges of owned city hexes, including growth in ring two.
 for(const f2 of S.factions){if(f2.dead)continue;const owned=[f2.city,...f2.town.plots];ctx.strokeStyle=f2.id===0?'#c8b987':'#947964';ctx.lineWidth=f2.town.walls==='palisade'?3:5;for(const i of owned){if(!f.seen[i])continue;const p=wp(i);for(let e=0;e<6;e++){const angle=(e*60)*Math.PI/180,mx=p.x+Math.cos(angle)*SQ*R/2,my=p.y+Math.sin(angle)*SQ*R*Y/2;const neigh=nb(i).find(j=>{const q=wp(j);return Math.hypot(q.x-(p.x+Math.cos(angle)*SQ*R),(q.y-(p.y+Math.sin(angle)*SQ*R*Y))/Y)<R*.2;});if(neigh!=null&&owned.includes(neigh))continue;const a=(e*60-30)*Math.PI/180,b=(e*60+30)*Math.PI/180;ctx.beginPath();ctx.moveTo(p.x+Math.cos(a)*R,p.y+Math.sin(a)*R*Y);ctx.lineTo(p.x+Math.cos(b)*R,p.y+Math.sin(b)*R*Y);ctx.stroke();}}}
 if(UI.shipping){const p=path(UI.shipping.pos,f.city);arrowLine(ctx,[wp(UI.shipping.pos),...p.map(i=>wp(i))],'#ead49e',3);}for(const c of [...S.convoys,...FX.ghosts()])if(c.owner===0||visible(f,c.pos)){const p=FX.position('map',c.id,c.pos,wp);props.push({n:14,x:p.x,y:p.y+14,h:55,label:c.owner===0?'Ваша повозка':'Повозка',color:COLORS[c.owner]});}
 for(const r of S.remains)if(f.seen[r.pos]){const p=wp(r.pos);ctx.fillStyle='#5e4637';ctx.fillRect(p.x-9,p.y+10,18,7);label(ctx,'Останки',p.x,p.y+31,'#cdb492',8);}
 props.sort((a,b)=>a.y-b.y);for(const p of props){ctx.save();ctx.globalAlpha=p.alpha??1;shadow(ctx,p.x,p.y,p.h*.24);if(p.creatureFamily)lair(ctx,p.creatureFamily,p.x,p.y,p.h);else if(p.n===3||p.n===4)windTree(ctx,p.n,p.x,p.y,p.h);else if(p.n===2)mill(ctx,p.x,p.y,p.h);else sprite(ctx,p.n,p.x,p.y,p.h);ctx.restore();}
 for(const a of allArmies())if(living(a).length&&(a.owner===0||visible(f,a.pos))){const p=FX.position('map',a.id,a.pos,wp);a.heroes.forEach((h,i)=>troops.push({h,x:p.x+(i-(a.heroes.length-1)/2)*22,y:p.y+35+(i%2?7:0),phase:p.moving?(FX.active?.p||0)*Math.PI*4+i*.7:null,flip:p.moving?p.flip:a.owner!==0,owner:a.owner}));if(a.id===UI.army){ctx.strokeStyle='#f0ce7c';ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(p.x,p.y+37,46,13,0,0,Math.PI*2);ctx.stroke();}label(ctx,`${a.owner===0?'Отряд '+(f.armies.indexOf(a)+1):HOUSES[a.owner]} · ${a.heroes.length}`,p.x,p.y+63,COLORS[a.owner],9);}
 troops.sort((a,b)=>a.y-b.y);for(const t of troops){shadow(ctx,t.x,t.y,10);walker(ctx,t.h.cls==='acolyte'?(t.h.id.charCodeAt(t.h.id.length-1)%2?11:12):C[t.h.cls].sprite,t.x,t.y,46,t.flip,t.phase);}for(const p of props)if(p.label){ctx.save();ctx.globalAlpha=p.alpha??1;label(ctx,p.label,p.x,p.y-p.h-8,p.color);ctx.restore();}
 for(const si of S.sieges){const pos=S.factions[si.defender].city;if(f.seen[pos]){const p=wp(pos);label(ctx,`Осада ${si.progress}/${fortification(S.factions[si.defender])}`,p.x,p.y+82,'#e8a98d',10);}}
 FX.overlay(ctx,'map',wp);
 ctx.restore();const shade=ctx.createRadialGradient(w*.45,h*.4,h*.15,w*.5,h*.5,w*.7);shade.addColorStop(0,'#071c1300');shade.addColorStop(1,'#10281955');ctx.fillStyle=shade;ctx.fillRect(0,0,w,h);if(!ready){ctx.fillStyle='#edd9a2';ctx.font='12px Georgia';ctx.fillText('Готовим пиксельный мир…',80,50);}}
 function mapPick(x,y){const cv=$('map'),r=cv.getBoundingClientRect(),px=(x-r.left)/2/zoom+focusPoint.x-cv.clientWidth/4/zoom,py=(y-r.top)/2/zoom+focusPoint.y-cv.clientHeight/4/zoom;return hexPick(px,py,N,N);}
 function hexPick(x,y,w,h){let out=null,best=Infinity;for(let i=0;i<w*h;i++){const p=wp(i,w),dx=Math.abs(x-p.x),dy=Math.abs((y-p.y)/Y);if(dx<=SQ*R/2&&dy<=R&&dx/SQ+dy<=R){const d=dx*dx+dy*dy;if(d<best){out=i;best=d;}}}return out;}
 const cv=$('map');let drag=null;cv.addEventListener('pointerdown',e=>{if(e.button!==0)return;drag={x:e.clientX,y:e.clientY,lx:e.clientX,ly:e.clientY,moved:false};cv.setPointerCapture(e.pointerId);});cv.addEventListener('pointermove',e=>{if(drag){if(Math.hypot(e.clientX-drag.x,e.clientY-drag.y)>5)drag.moved=true;if(drag.moved){focusPoint.x-=(e.clientX-drag.lx)/2/zoom;focusPoint.y-=(e.clientY-drag.ly)/2/zoom;draw();}drag.lx=e.clientX;drag.ly=e.clientY;}else if(S){const p=mapPick(e.clientX,e.clientY);if(p!==hover){hover=p;draw();}}});cv.addEventListener('pointerup',e=>{if(!drag)return;const click=!drag.moved;drag=null;if(!click||!S||processing||FX.busy||S.battle||S.aftermath)return;const p=mapPick(e.clientX,e.clientY);if(p!=null){UI.selected=p;render();}});cv.addEventListener('pointercancel',()=>drag=null);cv.addEventListener('wheel',e=>{e.preventDefault();zoom=clamp(zoom*Math.exp(-e.deltaY*.001),.12,2);draw();},{passive:false});cv.addEventListener('keydown',e=>{const d={ArrowLeft:[-40,0],ArrowRight:[40,0],ArrowUp:[0,-40],ArrowDown:[0,40]}[e.key];if(d){e.preventDefault();focusPoint.x+=d[0];focusPoint.y+=d[1];draw();}});
 function tacticalFeature(ctx,t,p){ctx.save();
  if(t.kind==='tree'){shadow(ctx,p.x,p.y+8,26);sprite(ctx,3,p.x,p.y+10,72);}
  if(t.kind==='rock'){shadow(ctx,p.x,p.y+9,28);for(let j=0;j<3;j++){const x=p.x+(j-1)*15,y=p.y+(j%2)*8;ctx.beginPath();ctx.moveTo(x-16,y+7);ctx.lineTo(x-12,y-18);ctx.lineTo(x+1,y-31);ctx.lineTo(x+18,y-12);ctx.lineTo(x+20,y+7);ctx.closePath();ctx.fillStyle=['#747d72','#8d9382','#626f64'][j];ctx.fill();ctx.strokeStyle='#39483d';ctx.lineWidth=2;ctx.stroke();ctx.beginPath();ctx.moveTo(x+1,y-31);ctx.lineTo(x+4,y+3);ctx.stroke();}}
  if(t.kind==='bush'){for(let j=0;j<5;j++){ctx.fillStyle=j%2?'#647b43':'#425c35';ctx.beginPath();ctx.ellipse(p.x+(j-2)*11,p.y+3-(j%2)*5,15,10,0,0,Math.PI*2);ctx.fill();}}
  if(t.kind==='rubble'){ctx.fillStyle='#a4a589';for(let j=0;j<9;j++)ctx.fillRect(p.x-28+(j*17)%57,p.y-12+(j*11)%30,8,5);}
  if(['water','shallow','marsh','mud'].includes(t.kind)){ctx.fillStyle={water:'#446f79',shallow:'#70958c',marsh:'#536e4c',mud:'#665d43'}[t.kind];ctx.beginPath();ctx.ellipse(p.x,p.y,36,20,0,0,Math.PI*2);ctx.fill();ctx.strokeStyle=t.kind==='mud'?'#847558':'#9bb4a080';ctx.lineWidth=2;for(let j=0;j<3;j++){ctx.beginPath();ctx.moveTo(p.x-21+j*6,p.y-8+j*7);ctx.lineTo(p.x+16-j*4,p.y-8+j*7);ctx.stroke();}if(t.kind==='marsh'){ctx.strokeStyle='#b3b77c';for(let j=0;j<5;j++){ctx.beginPath();ctx.moveTo(p.x-22+j*11,p.y+4);ctx.lineTo(p.x-25+j*12,p.y-12-j%2*5);ctx.stroke();}}}
  if(t.kind==='hill'){ctx.fillStyle='#8b8758';ctx.beginPath();ctx.ellipse(p.x,p.y,36,19,0,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#b1a574';ctx.lineWidth=2;for(let j=0;j<3;j++){ctx.beginPath();ctx.ellipse(p.x,p.y+4-j*4,28-j*7,10-j*2,0,Math.PI,Math.PI*2);ctx.stroke();}}
  if(t.cover)label(ctx,`${t.cost>1?'×'+t.cost+' · ':''}КБ +${t.cover}`,p.x,p.y+29,'#d8e6b7',6);
  else if(t.cost>1)label(ctx,`×${t.cost}${t.height?' · ↑':''}`,p.x,p.y+29,'#ebd49a',6);
  ctx.restore();}
 function battle(){const cv=$('battleCanvas'),b=S?.battle;if(!cv||!b)return;if(battleHoverId!==b.id){battleHover=null;battleHoverId=b.id;}const{w,h,ctx}=surface(cv),field=Tactics.field(),z=Math.min(w/(SQ*R*8+65),h/(R*1.5*Y*6+65)),target={x:SQ*R*7.5/2,y:R*1.5*Y*5/2-12};battleCam={cv,z,target};ctx.fillStyle='#2c4330';ctx.fillRect(0,0,w,h);ctx.save();ctx.translate(w/2,h/2);ctx.scale(z,z);ctx.translate(-target.x,-target.y);const selected=b.units.find(u=>u.id===UI.battleSelected),reach=selected&&selected.ap>0&&!selected.surrender?battleReach(selected):new Map(),base=field.terrain==='forest'?'plain':field.terrain==='river'?'plain':field.terrain;
  for(let i=0;i<48;i++){const p=wp(i,8),t=Tactics.tile(i);terrain(ctx,base,p,i);if(reach.has(i)){ctx.fillStyle='#b9cb8d25';ctx.beginPath();poly(ctx,p,R-1);ctx.fill();}if(grid||reach.has(i)||t.blocked){ctx.strokeStyle=t.blocked?'#bf9f6a66':reach.has(i)?'#b7c388':'#b1b58835';ctx.lineWidth=1;ctx.beginPath();poly(ctx,p,R-1);ctx.stroke();}}
  const actors=b.units.filter(u=>!u.retreated).map(u=>({unit:u,y:wp(u.pos,8).y}));for(let i=0;i<48;i++)if(Tactics.tile(i).kind!=='ground')actors.push({tile:i,y:wp(i,8).y});actors.sort((a,b)=>a.y-b.y);
  for(const actor of actors){if(actor.tile!=null){tacticalFeature(ctx,Tactics.tile(actor.tile),wp(actor.tile,8));continue;}const u=actor.unit,p=FX.position('battle',u.id,u.pos,i=>wp(i,8)),visualHP=FX.hp(u);if(visualHP<=0){ctx.fillStyle='#6f5140';ctx.fillRect(p.x-6,p.y,12,4);continue;}shadow(ctx,p.x,p.y+14);const n=u.cls?u.cls==='acolyte'?(u.hero?.charCodeAt(u.hero.length-1)%2?11:12):C[u.cls].sprite:u.range>1?10:13;u.monster?monster(ctx,u.monster,p.x,p.y+14,u.monster==='ogre'?72:58,p.moving?p.flip:u.side!==b.human,p.moving?(FX.active?.p||0)*Math.PI*4:null):walker(ctx,n,p.x,p.y+14,58,p.moving?p.flip:u.side!==b.human,p.moving?(FX.active?.p||0)*Math.PI*4:null);if(u.id===UI.battleSelected){ctx.strokeStyle='#edca78';ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(p.x,p.y+14,24,9,0,0,Math.PI*2);ctx.stroke();}ctx.fillStyle='#27382c';ctx.fillRect(p.x-18,p.y+21,36,4);ctx.fillStyle=u.side===b.human?'#a6c788':'#ca8d77';ctx.fillRect(p.x-18,p.y+21,36*visualHP/u.max,4);}
  for(const u of b.units)if(FX.hp(u)>0){const p=FX.position('battle',u.id,u.pos,i=>wp(i,8));label(ctx,u.surrender?'Сдался':u.name,p.x,p.y-53,u.surrender?'#e5cc83':u.side===b.human?'#c9dfb2':'#e6aa92',9);}
  if(battleHover!=null){ctx.strokeStyle='#f2d28c';ctx.lineWidth=2;ctx.beginPath();poly(ctx,wp(battleHover,8),R-2);ctx.stroke();}
  FX.overlay(ctx,'battle',i=>wp(i,8));ctx.restore();
  const pick=e=>{const r=cv.getBoundingClientRect(),x=(e.clientX-r.left)/2/z+target.x-w/2/z,y=(e.clientY-r.top)/2/z+target.y-h/2/z;return hexPick(x,y,8,6);};
  const info=p=>{if($('battleHexInfo')&&p!=null)$('battleHexInfo').textContent=Tactics.describe(p)+(selected&&reach.has(p)?` Путь: ${reach.get(p)}/${Bestiary.speed(selected)} очков движения за 1 ОД.`:'');};
  cv.onclick=e=>{const p=pick(e);if(p!=null){info(p);if(!FX.busy)clickBattle(p);}};
  cv.onpointermove=e=>{const p=pick(e);info(p);if(p!==battleHover){battleHover=p;battle();}};
  cv.onpointerleave=()=>{if(battleHover!=null){battleHover=null;battle();}};
 }

 function thumbnails(){if(!ready)return;for(const cv of document.querySelectorAll('canvas[data-hero]')){const ctx=cv.getContext('2d');cv.width=cv.classList.contains('heroThumb')?75:36;cv.height=cv.classList.contains('heroThumb')?75:45;ctx.imageSmoothingEnabled=false;const cls=cv.dataset.hero,n=cls==='acolyte'?12:C[cls].sprite;sprite(ctx,n,cv.width/2,cv.height-1,cv.height-3);}}
 function monsterThumbnails(){for(const cv of document.querySelectorAll('canvas[data-monster]')){cv.width=75;cv.height=75;const ctx=cv.getContext('2d');ctx.imageSmoothingEnabled=false;monster(ctx,cv.dataset.monster,38,69,58);}}
 function focus(pos){focusPoint=wp(pos);focusPoint.x+=75;focusPoint.y+=15;zoom=.95;draw();}
 function home(){if(S)focus(army()?.pos??player().city);}
 function control(k){if(k==='home')home();if(k==='in')zoom=clamp(zoom*1.25,.12,2);if(k==='out')zoom=clamp(zoom*.8,.12,2);if(k==='all'){focusPoint={x:SQ*R*15.5/2,y:R*1.5*Y*15/2};zoom=Math.min($('map').clientWidth/2/(SQ*R*17),$('map').clientHeight/2/(R*1.5*Y*18));}draw();}
 function project(pos,mode='map'){if(mode==='battle'&&battleCam){const {cv,z,target}=battleCam,r=cv.getBoundingClientRect(),p=wp(pos,8);return{x:r.left+2*(cv.clientWidth/4+(p.x-target.x)*z),y:r.top+2*(cv.clientHeight/4+(p.y-target.y)*z)};}const r=$('map').getBoundingClientRect(),p=wp(pos);return{x:r.left+2*($('map').clientWidth/4+(p.x-focusPoint.x)*zoom),y:r.top+2*($('map').clientHeight/4+(p.y-focusPoint.y)*zoom)};}
 let ambientFrames=0,ambientLast=0;
 function ambient(now){requestAnimationFrame(ambient);if(now-ambientLast<66||!ready||!S||document.hidden||UI.modal||S.battle||FX.busy||!FX.settings.enabled)return;ambientLast=now;ambientFrames++;draw();}
 requestAnimationFrame(ambient);
 img.onload=()=>{ready=true;draw();thumbnails();if(S?.battle)battle();};img.src=ATLAS_URL;window.addEventListener('resize',()=>{draw();if(S?.battle)battle();});
 return{draw,battle,thumbnails,monsterThumbnails,focus,home,control,project,grid(){grid=!grid;draw();if(S?.battle)battle();},get ready(){return ready;},get ambient(){return{frames:ambientFrames,enabled:FX.settings.enabled};}};
})();

```

### `src/tooltips.js`

```js
const Tips=(()=>{
 const el=document.createElement('div');el.id='abilityTooltip';el.role='tooltip';el.hidden=true;document.body.append(el);let target=null,timer;
 function hide(){clearTimeout(timer);if(target)target.removeAttribute('aria-describedby');target=null;el.hidden=true;}
 function show(t){if(!t?.isConnected)return;target=t;el.textContent=t.dataset.tip;el.hidden=false;t.setAttribute('aria-describedby','abilityTooltip');const r=t.getBoundingClientRect(),w=el.offsetWidth,h=el.offsetHeight;el.style.left=Math.max(10,Math.min(innerWidth-w-10,r.left))+'px';el.style.top=Math.max(10,r.top-h-8>=10?r.top-h-8:Math.min(innerHeight-h-10,r.bottom+8))+'px';}
 document.addEventListener('pointerover',e=>{const t=e.target.closest('[data-tip]');if(!t||t===target)return;hide();target=t;timer=setTimeout(()=>show(t),180);});
 document.addEventListener('pointerout',e=>{if(target?.contains(e.target)&&!target.contains(e.relatedTarget))hide();});
 document.addEventListener('focusin',e=>{const t=e.target.closest('[data-tip]');if(t){hide();show(t);}});
 document.addEventListener('focusout',e=>{if(target?.contains(e.target)&&!target.contains(e.relatedTarget))hide();});
 document.addEventListener('click',hide);document.addEventListener('keydown',e=>{if(e.key==='Escape')hide();});window.addEventListener('resize',hide);document.addEventListener('scroll',hide,true);
 function ability(u,k){
  if(!u)return '';
  if(k==='bolt')return 'Астральный болт\nДальность: 4 гекса. Укрытие помогает цели уклониться.\nЦена: 2 маны и 1 ОД.';
  if(k==='heal')return `Лечение\nДо ${14+(u.branch?.heal||0)+(['priest','highpriest'].includes(u.sub)?8:0)} ХП союзнику. Лечение поднимает недееспособного героя до истечения отсчёта.\nДальность: 4 гекса. Цена: 3 маны и 1 ОД.`;
  if(k==='ward')return 'Оберег\n+10 п.п. физической брони до конца следующего раунда.\nЦена: 2 маны и 1 ОД.';
  if(k==='curse')return 'Проклятье\nСнижает атаку и вызывает стресс.\nЦена: 2 маны и 1 ОД.';
  if(k==='skill'){
   if(u.cls==='acolyte')return 'Медитация\nВосстанавливает до 4 маны. Цена: 1 ОД.';
   if(u.cls==='warrior')return 'Мощный удар\n150% обычного урона. Цена: 1 ОД. Перезарядка: 1 раунд.';
   return 'Особая атака\n+5 урона при попадании. Цена: 1 ОД. Один раз за бой.';
  }
  if(k==='support')return 'Прикрыть друга\n+5 п.п. физической брони, пока вы рядом и в строю.\nЦена: 1 ОД. Один раз за бой на пару.';
  if(k==='guard')return 'Оборона\n+10 п.п. физической брони до следующего хода. Воин гарантированно блокирует следующий физический удар, который его настигнет. После брони блок вдвое снижает урон.\nЦена: 1 ОД.';
  return '';
 }
 function button(a,text,extra,disabled,u,k){const tip=Tips.ability(u,k);return`<span class="ability-tip" tabindex="${disabled?0:-1}" data-tip="${esc(tip)}">${globalButton(a,text,extra,disabled)}</span>`;}
 // Kept separate from the exported method so the game's button helper stays in scope.
 function globalButton(a,text,extra,disabled){return `<button data-a="${a}" ${extra||''} ${disabled?'disabled':''}>${text}</button>`;}
 return{ability,button,hide};
})();

```

### `template.html`

```html
<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Туман и кости · Наследники короны прототип 1.0</title><style>
:root{color-scheme:dark;--bg:#16231d;--paper:#243328;--deep:#19281f;--line:#667255;--gold:#e9c77c;--text:#eee5cc;--muted:#b2bba5;--bad:#e99d89;--good:#abc993}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.45 system-ui,sans-serif}button,select,input{font:inherit}button{background:#304330;color:var(--text);border:1px solid #6a7758;border-radius:5px;padding:8px 12px;cursor:pointer}button:hover:not(:disabled){background:#495c3b;border-color:var(--gold)}button:disabled{opacity:.38;cursor:default}button.gold{background:var(--gold);border-color:var(--gold);color:#263025;font-weight:700}button.active{outline:2px solid var(--gold)}button.small{font-size:12px;padding:5px 8px}.danger{color:var(--bad)}.good{color:var(--good)}.muted,small{color:var(--muted);font-size:12px}h1,h2,h3{font-family:Georgia,serif;font-weight:normal;margin:0 0 10px}h1{font-size:21px}h2{color:var(--gold);font-size:27px}h3{font-size:19px;color:#e9d9ad}p{margin:6px 0 12px}.eyebrow{font-size:10px;letter-spacing:1.8px;text-transform:uppercase;color:var(--gold)}header{height:76px;padding:10px 20px;background:#17271ff5;border-bottom:1px solid #827953;display:flex;align-items:center;justify-content:space-between;gap:15px;position:relative;z-index:2}.topres{display:flex;gap:24px;align-items:center}.topres b{font-size:22px;color:var(--gold)}.topres small{display:block}#shell{height:calc(100dvh - 76px);min-height:610px;position:relative;overflow:hidden}#map{width:100%;height:100%;display:block;image-rendering:auto;touch-action:none}#nav{position:absolute;left:14px;top:16px;display:flex;flex-direction:column;gap:8px;width:112px}#nav button{background:#1d3028ed;text-align:left;box-shadow:0 2px 15px #0005}#mapTools{position:absolute;left:142px;top:16px;display:flex;gap:5px;background:#1c3027df;padding:6px;border-radius:6px}#sidebar{position:absolute;right:14px;top:16px;width:292px;max-height:calc(100% - 174px);overflow:auto;background:#1b2d24ee;border:1px solid #7c8059;padding:16px;border-radius:8px;box-shadow:0 8px 25px #0005}#armies{position:absolute;left:14px;bottom:154px;display:flex;gap:6px;max-width:calc(100% - 340px);overflow:auto;padding:3px}#armies button{white-space:nowrap;background:#1a2d24ed}#armybar{position:absolute;left:14px;right:330px;bottom:14px;min-height:125px;border:1px solid #96916a;background:#192b22f5;border-radius:8px;padding:10px 14px;box-shadow:0 4px 25px #0008}#turnbox{position:absolute;bottom:14px;right:14px;width:300px;min-height:125px;background:#1b2d24f2;border:1px solid #96916a;border-radius:8px;padding:12px}#endTurn{width:100%;margin-top:8px}#portraits{display:flex;gap:10px;margin-top:6px}.portrait{width:122px;padding:6px;border:1px solid #59654b;border-radius:5px;background:#27382a;cursor:pointer}.portrait canvas{float:left;margin-right:6px;image-rendering:pixelated}.portrait b{font-size:12px}.portrait small{font-size:10px;display:block}.bar{height:4px;background:#45503e;margin:5px 0;border-radius:3px;overflow:hidden}.bar i{display:block;height:100%;background:var(--gold)}.row{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:9px}.stack{display:flex;flex-wrap:wrap;gap:7px;margin:9px 0}.card{border:1px solid #526047;border-radius:7px;background:#1c2e23;padding:12px;margin:9px 0}.badge{font-size:11px;padding:3px 7px;border:1px solid #697354;border-radius:14px}.modal{position:fixed;inset:0;background:#07100de3;z-index:10;display:flex;align-items:center;justify-content:center;padding:20px;overflow:auto}.modal[hidden]{display:none}.window{width:min(1050px,100%);max-height:94dvh;overflow:auto;background:#233528;border:1px solid #a79d6f;border-radius:10px;padding:24px;box-shadow:0 20px 90px #0009}.window.wide{width:min(1360px,100%)}.window.narrow{width:min(740px,100%)}.three{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.two{display:grid;grid-template-columns:1fr 1fr;gap:18px}.citylayout{display:grid;grid-template-columns:minmax(340px,1fr) 360px;gap:20px}.citymap{background:#1b3026;border:1px solid #64734f;border-radius:7px}.citymap svg{width:100%;display:block}.plot{cursor:pointer}.plot:hover polygon{stroke:#ffe6a2;stroke-width:3}.rule{border-left:3px solid var(--gold);padding:12px;background:#31422e;margin:10px 0}.battlelayout{display:grid;grid-template-columns:minmax(360px,1fr) 285px;gap:16px}#battleCanvas{width:100%;height:430px;display:block;image-rendering:auto;background:#394e32;touch-action:none}.log{max-height:150px;overflow:auto;font-size:12px}.introtitle{font-size:45px;line-height:1.1;margin:20px 0}.candidate{cursor:pointer}.candidate.active{border:2px solid var(--gold)}.hint{font-size:12px;background:#34432b;border:1px solid #687752;padding:10px;border-radius:5px}#toast{position:fixed;z-index:30;bottom:28px;left:50%;transform:translateX(-50%);padding:12px 20px;background:#eed49d;color:#263025;border-radius:6px;max-width:90vw;box-shadow:0 8px 30px #0008}#toast[hidden]{display:none}a{color:var(--gold)}table{border-collapse:collapse;width:100%;font-size:13px}td,th{padding:8px;text-align:left;border-bottom:1px solid #536143}.synergy{color:#cce6a7}.heroThumb{height:75px;width:75px;image-rendering:pixelated;float:left;margin:0 10px 5px 0}.screenOnly{color:var(--muted);font-size:11px}button.warn{border-color:#b27c61}.pill{display:inline-block;padding:3px 8px;border-radius:10px;background:#3b4d34;font-size:11px;margin:2px}#phase{font-size:12px;color:var(--muted)}@media(max-width:1050px){header{height:auto;min-height:76px;flex-wrap:wrap}.topres{gap:15px}#shell{height:calc(100dvh - 100px)}#sidebar{width:245px}#armybar{right:280px}#turnbox{width:250px}#armies{max-width:calc(100% - 280px)}.portrait{width:100px}.citylayout{grid-template-columns:1fr}.three{grid-template-columns:1fr 1fr}.two{grid-template-columns:1fr}.battlelayout{grid-template-columns:1fr}#battleCanvas{height:360px}}@media(max-width:650px){header{padding:8px}.topres{gap:10px}.topres b{font-size:17px}h1{font-size:17px}#shell{height:900px;min-height:900px}#nav{left:8px;top:8px;width:auto;flex-direction:row;flex-wrap:wrap;right:8px}#nav button{font-size:11px;padding:7px}#mapTools{left:8px;top:95px}#sidebar{right:8px;top:auto;bottom:180px;max-height:210px;width:230px;font-size:12px}#armies{left:8px;bottom:153px;max-width:calc(100% - 16px)}#armybar{left:8px;right:8px;bottom:8px;min-height:140px}#portraits{gap:5px}.portrait{flex:1;width:auto;min-width:0;padding:4px}.portrait canvas{float:none;margin:0}.portrait b{font-size:10px}.portrait small{font-size:9px}#turnbox{bottom:auto;top:140px;right:8px;width:170px;min-height:90px;padding:7px}.window{padding:14px}.modal{padding:6px}.three{grid-template-columns:1fr}.citylayout{grid-template-columns:minmax(0,1fr)}.introtitle{font-size:32px}.battlelayout{grid-template-columns:minmax(0,1fr)}#battleCanvas{height:320px}}

body.fxbusy button[data-a]:not([data-a="animationSettings"]):not([data-a="export"]):not([data-a="zoom"]):not([data-a="grid"]){pointer-events:none;filter:saturate(.6)}body.fxbusy #map,body.fxbusy #battleCanvas{cursor:wait}.fx-progress{position:fixed;bottom:165px;left:50%;transform:translateX(-50%);z-index:45;display:flex;align-items:center;gap:14px;padding:9px 14px;background:#1a2b24f0;border:1px solid #b49e68;border-radius:7px;box-shadow:0 5px 30px #0008;font-size:12px}.fx-progress[hidden],.dice-panel[hidden],#fxSettings[hidden]{display:none}.dice-panel{position:fixed;z-index:50;left:50%;bottom:205px;transform:translateX(-50%);width:min(420px,94vw);background:linear-gradient(145deg,#213c30f5,#14261ff7);border:1px solid #ccb37d;border-radius:14px;padding:17px 22px;box-shadow:0 18px 65px #000b;display:grid;grid-template-columns:100px 1fr;gap:14px;align-items:center;pointer-events:none}.dice-panel svg{width:94px;height:100px;overflow:visible;filter:drop-shadow(0 0 10px #a2d1a32a)}.dice-panel[data-result="critical"]{border-color:#ffe294;box-shadow:0 0 35px #d7b85855,0 18px 65px #000b}.dice-panel[data-result="failure"]{border-color:#d2987e}.dice-panel h3{font-size:17px;margin-bottom:6px}.dice-panel p{margin:3px 0;font-size:12px}.dice-panel #diceOutcome{font-size:14px;color:#f0d28f;min-height:20px}.fxSettingsBackdrop{position:fixed;inset:0;z-index:70;background:#07150dbb;display:flex;align-items:center;justify-content:center;padding:20px}.fxSettingsBox{width:min(450px,100%);background:#203729;border:1px solid #ad9b6c;border-radius:10px;padding:24px}.fxSettingsBox label{display:block;margin:15px 0}.fxSettingsBox select{padding:5px 9px;margin-left:12px}.city-scaffold .scaffold-glow{animation:scaffoldGlow 1.8s ease-in-out infinite}@keyframes scaffoldGlow{0%,100%{opacity:.45}50%{opacity:.9}}@media(prefers-reduced-motion:reduce){.city-scaffold .scaffold-glow{animation:none}}body.fx-disabled .city-scaffold .scaffold-glow{animation:none}@media(max-width:650px){.fx-progress{bottom:10px;width:94%;justify-content:space-between}.dice-panel{bottom:68px;grid-template-columns:82px 1fr;padding:13px}.dice-panel svg{width:78px;height:84px}}
.turn-task.deferred{opacity:.7;border-style:dashed}.turn-task p{margin:6px 0}.turn-task-list,.turn-news-list{max-height:62dvh;overflow:auto}.turn-news[data-kind="king"]{border-color:var(--gold)}.turn-news[data-kind="event"],.turn-news[data-kind="siege"]{border-color:#ba8d75}#turnbox .stack{margin:7px 0;gap:5px}@media(max-width:650px){#turnbox .stack button{font-size:10px;padding:4px}.turn-task-list,.turn-news-list{max-height:65dvh}}
#abilityTooltip{position:fixed;z-index:90;max-width:min(330px,calc(100vw - 20px));padding:12px 15px;background:#14271ff5;color:var(--text);border:1px solid var(--gold);border-radius:7px;box-shadow:0 8px 30px #000a;white-space:pre-line;font-size:12px;line-height:1.5;pointer-events:none}#abilityTooltip[hidden]{display:none}.ability-tip{display:inline-flex;border-radius:5px}.ability-tip:focus-visible{outline:2px solid var(--gold);outline-offset:3px}#battleHexInfo{min-height:64px;margin-top:8px}
.dev-panels{display:block}.dev-panels section[hidden]{display:none}.dev-panels section>label{display:block;margin:12px 0}.dev-panels select{max-width:100%;padding:6px;border-radius:4px}.dev-panels .card{margin:10px 0}.relation-history{margin:10px 0}
.topres{flex-wrap:wrap;row-gap:4px;max-width:100%}
</style></head><body><header><div><div class="eyebrow">Туман и кости · знания и мастерство · пробный бой · прототип 1.0</div><h1>Наследники короны</h1></div><div class="topres" id="resources"></div><div class="stack"><button class="small" id="openBattleLab">Пробный бой</button><button class="small" data-a="downloadGame">Копия игры</button><button class="small" data-a="animationSettings">Анимации</button><button class="small" data-a="help">Правила</button><button class="small" data-a="export">Экспорт</button><button class="small" data-a="import">Загрузить</button><button class="small" data-a="new">Новая партия</button></div></header><div id="shell"><canvas id="map" aria-label="Карта королевства" tabindex="0"></canvas><nav id="nav"></nav><div id="mapTools"><button class="small" data-a="zoom" data-v="in">＋</button><button class="small" data-a="zoom" data-v="out">−</button><button class="small" data-a="zoom" data-v="home">Отряд</button><button class="small" data-a="zoom" data-v="all">Вся карта</button><button class="small" data-a="grid">Сетка</button></div><aside id="sidebar"></aside><div id="armies"></div><section id="armybar"></section><section id="turnbox"><div id="phase"></div><button id="endTurn" class="gold" data-a="end">Завершить ход →</button></section></div><div id="modal" class="modal" hidden></div><div id="toast" hidden></div><input id="file" type="file" accept=".json" hidden><div id="fxProgress" class="fx-progress" hidden><span id="fxLabel">Анимация</span><button id="fxSkip" class="small">Пропустить · пробел</button></div><div id="dicePanel" class="dice-panel" data-result="rolling" hidden><div id="fxDie"><svg viewBox="0 0 100 108" aria-label="Результат кубика"><defs><radialGradient id="dieGreen"><stop stop-color="#9fcea1"/><stop offset=".55" stop-color="#467b61"/><stop offset="1" stop-color="#203d35"/></radialGradient></defs><polygon points="50,4 91,28 91,76 50,101 9,76 9,28" fill="url(#dieGreen)" stroke="#d7c58a" stroke-width="2"/><path d="M50 4 50 27 16 74 84 74 50 27 91 28 M9 28 50 27 M16 74 50 101 84 74 M9 76 16 74 M91 76 84 74" fill="none" stroke="#c5d2a5" stroke-opacity=".5"/><text id="diceValue" x="50" y="63" text-anchor="middle" fill="#ffe5a4" font-size="33" font-family="Georgia" font-weight="bold">20</text><text id="diceSides" x="50" y="94" text-anchor="middle" fill="#ead7a8" font-size="10">d20</text></svg></div><div><h3 id="diceTitle">Бросок</h3><p id="diceFormula"></p><p id="diceOutcome" aria-live="polite"></p></div></div><div id="fxSettings" class="fxSettingsBackdrop" hidden></div><script>
/*__ASSETS__*/
/*__ANIMATIONS__*/
/*__TURNS__*/
/*__TACTICS__*/
/*__TOOLTIPS__*/
/*__RELATIONS__*/
/*__BESTIARY__*/
/*__GAME__*/
/*__DEVELOPMENT__*/
/*__CAPITAL__*/
/*__TALENTS__*/
/*__STRIKE__*/
/*__BATTLE_RULES__*/
/*__PAINTER__*/
/*__BATTLE_LAB__*/
</script></body></html>

```

### `tools/build.py`

```python
"""Build a self-contained HTML game; no network or third-party Python packages."""
from pathlib import Path
import base64,json
root=Path(__file__).resolve().parents[1]
s=(root/'template.html').read_text()
assets='const ATLAS_URL='+json.dumps('data:image/png;base64,'+base64.b64encode((root/'assets/atlas.png').read_bytes()).decode())+';\nconst ATLAS_META='+(root/'assets/atlas.json').read_text()+';'
s=s.replace('/*__ASSETS__*/',assets).replace('/*__ANIMATIONS__*/',(root/'src/animations.js').read_text()).replace('/*__TURNS__*/',(root/'src/turns.js').read_text()).replace('/*__TACTICS__*/',(root/'src/tactics.js').read_text()).replace('/*__TOOLTIPS__*/',(root/'src/tooltips.js').read_text()).replace('/*__RELATIONS__*/',(root/'src/relations.js').read_text()).replace('/*__BESTIARY__*/',(root/'src/bestiary.js').read_text()).replace('/*__GAME__*/',(root/'src/game.js').read_text()).replace('/*__DEVELOPMENT__*/',(root/'src/development.js').read_text()).replace('/*__PAINTER__*/',(root/'src/painter.js').read_text())
s=s.replace('/*__CAPITAL__*/',(root/'src/capital.js').read_text()).replace('/*__TALENTS__*/',(root/'src/talents.js').read_text()).replace('/*__BATTLE_RULES__*/',(root/'src/battle_rules.js').read_text())
strike=(root/'src/strike.js').read_text()
s=s.replace('/*__STRIKE__*/',strike)
lab=(root/'src/battle-lab.html').read_text().replace('/*__PIXEL_SPRITES__*/',(root/'src/pixel_sprites.js').read_text()).replace('/*__STRIKE__*/',strike)
# srcdoc is embedded as a JS string; escape script terminators in the outer HTML.
lab_json=json.dumps(lab,ensure_ascii=False).replace('</','<\\/')
lab_module="""(()=>{let overlay=null;document.getElementById('openBattleLab').onclick=()=>{if(overlay)return;overlay=document.createElement('div');overlay.id='battleLabOverlay';overlay.style.cssText='position:fixed;inset:0;z-index:100;background:#14251f;padding-top:46px';const close=document.createElement('button');close.textContent='← Вернуться к игре';close.style.cssText='position:absolute;top:5px;left:12px';close.onclick=()=>{overlay.remove();overlay=null};const frame=document.createElement('iframe');frame.title='Пробный бой 4 на 4';frame.style.cssText='width:100%;height:100%;border:0';frame.srcdoc=__LAB__;overlay.append(close,frame);document.body.append(overlay)}})();""".replace('__LAB__',lab_json)
s=s.replace('/*__BATTLE_LAB__*/',lab_module)
(root/'battle-lab.html').write_text(lab)
(root/'index.html').write_text(s)
print('Built index.html:',len(s.encode()),'bytes')

```

### `tests/test_current_prototype.py`

```python
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

```

### `tests/test_animations.py`

```python
"""Presentation checks: real gameplay hooks, deterministic results, settings and skip."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from pathlib import Path
from playwright.sync_api import sync_playwright
import os
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}'
passed=[]
def ok(s): passed.append(s);print('PASS:',s,flush=True)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox','--disable-webgl'])
    page=browser.new_page(viewport={'width':1500,'height':1000})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(url);page.wait_for_function('Game.painter.ready')
    page.evaluate('Game.newGame(2026);Game.fx.configure({enabled:true,speed:1})')
    page.evaluate('''()=>{const s=Game.state; s.map[35].searched=true;s.map[35].site=null;s.factions[0].seen[36]=false;Game.moveTo(s.factions[0].armies[0],35);}''')
    page.wait_for_function("Game.fx.active?.type==='move'")
    assert page.evaluate('Game.state.factions[0].armies[0].pos')==35
    assert page.evaluate('Game.fx.revealAlpha(36)')==0
    page.wait_for_function('Game.fx.active?.p>.15')
    point=page.evaluate("Game.fx.position('map',Game.state.factions[0].armies[0].id,35,p=>({x:p,y:0})).x")
    assert 34<point<35
    page.click('#fxSkip')
    assert not page.evaluate('Game.fx.busy')
    assert page.evaluate('Game.fx.revealAlpha(36)')==1
    ok('Map motion interpolates; new terrain waits its turn; skip keeps final gameplay state')
    page.evaluate('''()=>{Game.newGame(300);Game.fx.configure({speed:1});Game.fx.roll(17,20,{mode:'map',label:'Проверка харизмы',modifier:3,dc:15,success:true});}''')
    page.wait_for_function("document.querySelector('#dicePanel').dataset.result==='success'&&!document.querySelector('#dicePanel').hidden")
    assert page.locator('#diceValue').text_content()=='17'
    assert page.locator('#diceFormula').inner_text()=='17 + 3 = 20 · КС 15'
    page.screenshot(path='/tmp/v05-dice.png')
    page.keyboard.press('Space');assert not page.evaluate('Game.fx.busy')
    ok('Animated die lands on the actual value with modifier and difficulty; keyboard skip works')
    assert page.evaluate('''()=>{
      Game.newGame(301);
      const a=Game.state.factions[0].armies[0];
      Game.startBattle(a,null,{kind:'ambush',family:'bandits',title:'Проверка анимаций',pos:a.pos});
      if(Game.fx.busy)return false;
      const b=Game.state.battle,u=b.units.find(u=>u.cls==='warrior'),t=b.units.find(u=>u.side===1);
      Object.assign(u,{pos:18,damage:10});
      Object.assign(t,{pos:19,hp:100,max:100,physicalArmor:0});
      const random=Math.random;
      Math.random=()=>.9;
      try {return Game.attackBattle(u,t)&&t.hp===90;} finally {Math.random=random;}
    }''')
    page.wait_for_function("Game.fx.active?.kind==='slash'")
    assert page.locator('#dicePanel').is_hidden()
    page.evaluate('Game.fx.configure({speed:4})');page.wait_for_function('!Game.fx.busy')
    assert page.evaluate("Game.fx.history.every(e=>e.type!=='dice')")
    ok('Battle starts without initiative dice and a real attack plays only the impact')
    page.evaluate('''()=>{const b=Game.state.battle,u=b.units.find(u=>u.side===0&&u.cls==='acolyte'),t=b.units.find(u=>u.side===0&&u.cls==='warrior');u.pos=17;u.ap=2;t.hp=1;Game.fx.configure({speed:1});Game.spellBattle(u,t,'heal');Game.render();}''')
    page.wait_for_function("Game.fx.active?.kind==='heal'")
    assert page.evaluate('Game.fx.hp(Game.state.battle.units.find(u=>u.side===0&&u.cls===\'warrior\'))')==1
    page.screenshot(path='/tmp/v05-heal.png')
    page.evaluate('Game.fx.finish()')
    assert page.evaluate('Game.fx.hp(Game.state.battle.units.find(u=>u.side===0&&u.cls===\'warrior\'))')>1
    ok('Healing displays pre-impact HP, then resolves to the saved healed value')
    assert page.evaluate('''() => {
      Game.newGame(306);
      const a=player().armies[0], random=Math.random;
      Object.assign(S.map[35],{terrain:'plain',searched:false,site:null});
      Math.random=()=>0;
      try {return Game.moveTo(a,35)&&S.battle.meta.kind==='ambush';} finally {Math.random=random;}
    }''')
    page.wait_for_function('!Game.fx.busy')
    assert page.locator('#dicePanel').is_hidden()
    assert page.evaluate("Game.fx.history.some(e=>e.type==='move')&&Game.fx.history.every(e=>e.type!=='dice')")
    ok('An ambush starts from map movement and the dice animation stays out of the battle window')
    page.evaluate('Game.newGame(302);Game.fx.configure({speed:1})')
    page.click('#nav [data-a=city]');page.click('[data-a=construct]')
    page.wait_for_function("Game.fx.active?.type==='city'")
    assert page.locator('.city-scaffold').count()>0
    page.wait_for_function('document.querySelectorAll(".fx-construction").length>0')
    page.screenshot(path='/tmp/v05-construction.png')
    page.evaluate('Game.fx.finish();const f=Game.state.factions[0];f.town.projects[0].progress=f.town.projects[0].work;Game.tickFaction(f);Game.renderCity()')
    page.wait_for_function("Game.fx.active?.kind==='complete'")
    page.evaluate('Game.fx.finish()')
    ok('Construction has persistent scaffolding and distinct start and completion effects')
    page.evaluate("""()=>{Game.newGame(304);Game.fx.configure({enabled:true,speed:1});const f=Game.state.factions[0],c=Game.makeConvoy(f,35,'bodies',[Game.createHero('warrior',2)]);Game.fx.finish();Math.random=()=>.5;Game.tickConvoys();}""")
    assert page.evaluate('Game.state.convoys.length')==0
    assert page.evaluate('Game.fx.ghosts().length')==1
    assert page.evaluate("Game.fx.queue.some(e=>e.type==='move')")
    page.evaluate('Game.fx.configure({speed:4})');page.wait_for_function('!Game.fx.busy')
    assert page.evaluate('Game.fx.ghosts().length')==0
    assert page.evaluate('Game.state.factions[0].morgue.length')==1
    ok('Arriving wagon remains visible through its travel animation, then unloads')
    page.evaluate("""()=>{Game.newGame(305);Game.fx.configure({enabled:true,speed:1});const a=Game.state.factions[0].armies[0];Game.startBattle(a,null,{kind:'ambush',title:'Движение в бою',pos:a.pos});Game.fx.finish();const b=Game.state.battle,u=b.units.find(u=>u.side===0);b.side=b.human;u.ap=2;Game.ui.battleSelected=u.id;Game.ui.mode='attack';const target=[...Game.battleReach(u).keys()].find(p=>p!==u.pos);Game.clickBattle(target);}""")
    page.wait_for_function("Game.fx.active?.type==='move'")
    before=page.evaluate('Game.state.battle.units.map(u=>u.pos)')
    page.evaluate('Game.clickBattle(25)')
    assert page.evaluate('Game.state.battle.units.map(u=>u.pos)')==before
    page.evaluate('Game.fx.finish();Game.fx.configure({autoDetail:true,speed:4});Game.autoBattle()')
    assert page.evaluate("Game.fx.queue.some(e=>e.type==='effect')&&Game.fx.queue.every(e=>e.type!=='dice')")
    page.wait_for_function('!Game.fx.busy',timeout=60000)
    ok('Tactical motion locks duplicate commands; detailed autobattle plays recorded actions')
    # Compare identical seeded gameplay with and without the presentation timeline.
    result=page.evaluate('''()=>{const run=enabled=>{Game.newGame(303);Game.fx.configure({enabled});let count=0;Math.random=()=>{count++;return .5};const a=Game.state.factions[0].armies[0];Game.startBattle(a,null,{kind:'ambush',title:'RNG',pos:a.pos});Game.fx.finish();const b=Game.state.battle,u=b.units.find(u=>u.side===0&&u.cls==='warrior'),t=b.units.find(u=>u.side===1);u.pos=18;t.pos=19;u.range=1;t.hp=t.max=100;t.ac=-100;Game.attackBattle(u,t);const state=JSON.stringify(Game.state);Game.fx.finish();return{state,count}};return[run(true),run(false)]}''')
    assert result[0]==result[1]
    ok('Enabled and disabled animations consume identical randomness and produce identical game state')
    page.evaluate('Game.fx.configure({enabled:true,speed:4,autoDetail:false});Game.autoBattle()')
    assert page.evaluate("Game.fx.queue.every(e=>e.kind==='summary')")
    page.wait_for_function('!Game.fx.busy')
    ok('Default autobattle stays brief instead of replaying every action')
    page.evaluate("Game.fx.roll(9,20,{mode:'map'});Game.fx.configure({enabled:false,speed:2})")
    assert not page.evaluate('Game.fx.busy')
    page.reload();page.wait_for_function('Game.painter.ready')
    assert page.evaluate('Game.fx.settings')=={'enabled':False,'speed':2,'autoDetail':False}
    ok('Disabling immediately unlocks controls; speed and preferences persist after reload')
    reduced=browser.new_context(reduced_motion='reduce')
    rp=reduced.new_page();rp.goto(url)
    assert not rp.evaluate('Game.fx.settings.enabled')
    reduced.close()
    assert not errors,errors
    ok('Reduced-motion preference respected; no browser errors during animated gameplay')
    browser.close()
server.shutdown()
print(f'{len(passed)} animation scenarios passed.')

```

### `tests/test_battle_lab.py`

```python
"""Browser scenarios for movement packets, typed mitigation, engineers and explicit passes."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright
import os,json
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
passed=[]
def ok(text):passed.append(text);print('PASS:',text,flush=True)
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
 p=browser.new_page(viewport={'width':1600,'height':1100});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto(base+'/battle-lab.html');p.uncheck('#motion');p.fill('#critChance','0');p.dispatch_event('#critChance','change')
 assert p.locator('.tile').count()==160
 assert p.evaluate('Lab.state.units.length===8&&Lab.state.units.every(u=>u.ap===3)')
 assert p.evaluate('Lab.state.units.filter(u=>u.type==="engineer").length')==2
 ok('Expanded 16x10 map keeps four heroes per side, including engineers')
 p.locator('[data-q="3"][data-r="3"]').click()
 assert p.evaluate('Lab.state.units[0].ap===2&&Lab.state.units[0].stride===2')
 p.locator('[data-q="5"][data-r="3"]').click()
 assert p.evaluate('Lab.state.units[0].ap===2&&Lab.state.units[0].stride===0')
 p.locator('[data-q="6"][data-r="3"]').click()
 assert p.evaluate('Lab.state.units[0].ap===1&&Lab.state.units[0].stride===2')
 p.locator('[data-q="12"][data-r="3"]').click()
 assert p.evaluate('Lab.state.units[0].q===6&&Lab.state.units[0].ap===1')
 p.evaluate("Object.assign(Lab.state.units[4],{q:7,r:3});Lab.render()")
 p.click('[data-action="attack"]');p.locator('[data-q="7"][data-r="3"]').click()
 assert p.evaluate('Lab.state.units[0].ap===0&&Lab.state.units[0].stride===2')
 p.click('[data-action="move"]');p.locator('[data-q="6"][data-r="2"]').click()
 assert p.evaluate('Lab.state.units[0].ap===0&&Lab.state.units[0].stride===1&&Lab.pending().some(u=>u.id==="p0")')
 ok('Three cells cost one AP across separate clicks; exceeding the remaining movement budget is rejected')
 result=p.evaluate("()=>{Lab.reset('cover');const u=Lab.state.units[0];Object.assign(u,{q:5,r:3});const normal=Lab.paths(u).get('6,3');u.slow=1;const slow=Lab.paths(u).get('6,3');return {normal:normal.cost,slow:slow.cost,rock:Lab.paths(u).has('7,3')}}")
 assert result=={'normal':2,'slow':3,'rock':False}
 ok('Mud and slowing spend extra steps; rocks remain impassable')
 result=p.evaluate("()=>{Lab.reset();const vals=[0,25,50,100,200].map(Lab.reduction),u=Lab.state.units[0],t=Lab.state.units[4];const damage={};for(const type of ['piercing','slashing','magic'])damage[type]=Lab.damageForecast(u,t,{baseDamage:10,damage:type}).normalDamage;return {vals,damage}}")
 assert result['damage']=={'piercing':7,'slashing':5,'magic':8}
 assert abs(result['vals'][1]-1/3)<1e-8 and result['vals'][2]==.5
 assert result['vals'][3]-result['vals'][2]>result['vals'][4]-result['vals'][3]>0
 ok('Three defenses mitigate their own damage type with diminishing percentage gains')
 result=p.evaluate('''()=>{const hits=[];for(let i=0;i<30;i++){Lab.reset();const u=Lab.state.units[i%4],t=Lab.state.units[4];Object.assign(t,{q:u.q+(Lab.spec(u,'attack').range>1?2:1),r:u.r});const f=Lab.forecast(u,t,'attack'),before=t.hp;Lab.state.seed=i*197;Lab.apply(u,t,'attack');hits.push(f.ok&&[f.normalDamage,f.blockedDamage].includes(before-t.hp)&&u.ap===2)}return hits.every(Boolean)}''')
 assert result
 p.evaluate("Lab.reset();Lab.guard(Lab.state.units[4]);Lab.state.units[0].q=12;Lab.render()")
 f=p.evaluate("Lab.forecast(Lab.state.units[0],Lab.state.units[4],'attack')")
 assert f['defense']==75 and not p.evaluate('Lab.guard(Lab.state.units[4])')
 assert f['block']==1 and f['blockedDamage']<f['normalDamage']
 result=p.evaluate('''() => {
   const [u,,,,t]=Lab.state.units;
   const forecast=Lab.forecast(u,t,'attack'), before=t.hp;
   Lab.state.seed=0;
   if(!Lab.apply(u,t,'attack')||t.hp!==before-forecast.blockedDamage||t.guardBlock)return false;
   if(!Lab.apply(u,t,'attack')||t.hp!==before-forecast.blockedDamage-forecast.normalDamage)return false;
   return Lab.state.blocks===1;
 }''')
 assert result
 ok('Real hits match fixed forecasts, and defense prepares a single block on top of the armor')
 result=p.evaluate('''() => {
   Lab.reset('equal');
   const u=Lab.state.units[0], t=Lab.state.units[5];
   Object.assign(t,{q:u.q+1,r:u.r});
   Lab.state.seed=2048;
   const before=t.hp;
   return Lab.apply(u,t,'break')&&t.hp===before&&!t.exposed&&u.ap===1&&Lab.state.dodges===1;
 }''')
 assert result
 ok('Dodge avoids all damage and the attack debuff while the attacker spends the AP')
 p.evaluate("Lab.reset('cover')");p.click('[data-select="p1"]');p.click('[data-action="attack"]')
 assert p.locator('.range-clear').count()>0
 assert p.locator('[data-q="15"][data-r="9"]').get_attribute('data-range')==''
 p.evaluate("Lab.state.tiles['4,4'].kind='rock';Lab.render()")
 assert p.locator('[data-q="6"][data-r="4"]').get_attribute('data-range')=='blocked'
 p.click('[data-action="frost"]');assert p.locator('.range-clear').count()>0
 p.click('[data-select="p3"]');p.click('[data-action="heal"]');assert p.locator('.range-clear').count()>0
 ok('Ranged attacks, specials and healing highlight radius; blocked line of sight is distinguished')
 p.select_option('#scenario','rescue');p.click('[data-action="heal"]');p.locator('[data-q="7"][data-r="5"]').hover()
 assert 'Подъём с 1 ОД' in p.inner_text('#forecast')
 p.locator('[data-q="7"][data-r="5"]').click()
 assert p.evaluate('Lab.state.units[0].hp===10&&Lab.state.units[0].ap===1&&Lab.state.units[3].ap===1')
 p.click('[data-select="p0"]');p.locator('[data-q="8"][data-r="5"]').click()
 assert p.evaluate('Lab.state.units[0].ap===0&&Lab.state.units[0].stride===2')
 assert p.locator('[data-action="attack"]').is_disabled()
 ok('Revived hero has one AP, buying at most three steps and no extra attack')
 p.evaluate('Lab.reset()');p.click('#end')
 assert p.evaluate('Lab.state.round===1&&Lab.state.side===0')
 assert p.locator('[data-skip]').count()==4
 p.click('[data-skip="p0"]');assert p.evaluate('Lab.state.units[0].skipped&&Lab.state.units[0].ap===0')
 p.click('#skipAll');p.click('#end');p.wait_for_function('!Lab.busy')
 assert p.evaluate('Lab.state.round===2&&Lab.state.units.filter(u=>u.side===0).every(u=>!u.skipped&&u.stride===0)')
 ok('End turn blocks outstanding heroes; individual and explicit group passes allow progress')
 p.evaluate("Lab.reset();Object.assign(Lab.state.units[4],{q:3,r:3});Lab.render()")
 p.click('[data-action="break"]');p.locator('[data-q="3"][data-r="3"]').click()
 assert p.evaluate('Lab.state.units[0].ap===1&&Lab.state.units[0].cooldown===3&&Lab.state.units[4].exposed===1')
 p.evaluate('Lab.skipAll()');p.click('#end');p.wait_for_function('!Lab.busy')
 assert p.evaluate('Lab.state.round===2&&Lab.state.units[4].exposed===0&&Lab.state.units[0].cooldown===3')
 ok('Special costs and cooldowns remain valid; physical-defense debuff expires after target turn')
 p.select_option('#engineerSub','armorer');p.click('[data-select="p2"]');p.click('[data-action="powerarmor"]')
 assert p.evaluate('Lab.state.units[2].ap===1&&Lab.state.units[2].power===2&&Lab.defense(Lab.state.units[2],"piercing")===60&&Lab.spec(Lab.state.units[2],"attack").baseDamage===8')
 assert not p.evaluate('Lab.activateArmor(Lab.state.units[2])')
 assert 'Бронник' in p.inner_text('#selected')
 ok('Armorer activates personal power armor, raises all defenses and damage, and cannot stack it')
 p.select_option('#engineerSub','demolitionist');p.click('[data-select="p2"]');p.click('[data-action="mine"]');p.locator('[data-q="4"][data-r="5"]').click()
 assert p.evaluate('Lab.state.mines.length===1&&Lab.state.units[2].ap===1')
 p.evaluate("Object.assign(Lab.state.units[0],{q:3,r:5});Object.assign(Lab.state.units[4],{q:5,r:5});for(const u of Lab.state.units.filter(u=>u.side===1&&u.id!=='e0')){u.hp=0;u.ap=0}Lab.skipAll()")
 p.click('#end');p.wait_for_function('!Lab.busy')
 assert p.evaluate('Lab.state.mines.length===0&&Lab.state.units[4].hp<Lab.state.units[4].max&&Lab.state.log.some(t=>t.includes("Мина"))')
 ok('Demolitionist lays a mine; an enemy walking onto it takes real typed damage and consumes the trap')
 p.select_option('#engineerSub','fortifier');p.click('[data-select="p2"]');p.click('[data-action="fortify"]');p.locator('[data-q="4"][data-r="5"]').click()
 assert p.evaluate("Lab.state.tiles['4,5'].fort&&Lab.state.tiles['4,5'].kind==='cover'")
 p.evaluate("Lab.state.tiles['3,5'].kind='mud';Lab.render()")
 p.click('[data-action="bridge"]');p.locator('[data-q="3"][data-r="5"]').click()
 assert p.evaluate("Lab.state.tiles['3,5'].kind==='bridge'&&Lab.state.units[2].ap===0")
 result=p.evaluate("()=>{const u=Lab.state.units[1],t=Lab.state.units[4];Object.assign(t,{q:4,r:5});return Lab.damageForecast(u,t,Lab.spec(u,'attack')).cover}")
 assert result==35
 ok('Fortifier builds an improved ranged cover and bridge; bridge remains available during fortification cooldown')
 p.select_option('#engineerSub','base');p.check('#motion');p.evaluate('Lab.skipAll()');p.click('#end');p.click('#restart');p.wait_for_timeout(700)
 assert p.evaluate('Lab.state.round===1&&Lab.state.side===0&&!Lab.busy&&Lab.state.actions===0')
 p.uncheck('#motion');p.fill('#critChance','0');p.dispatch_event('#critChance','change')
 ok('Restart cancels pending animated AI actions')
 p.evaluate("Lab.reset();for(const u of Lab.state.units.filter(u=>u.side===1)){u.hp=0;u.ap=0};Object.assign(Lab.state.units[4],{q:3,r:3,hp:1});Lab.state.units[3].hp=0;Lab.state.units[3].ap=0;Lab.render()")
 p.click('[data-action="attack"]');p.locator('[data-q="3"][data-r="3"]').click()
 assert p.evaluate('Lab.state.winner===0&&Lab.state.units[3].hp===1')
 assert p.locator('#result').is_visible() and p.locator('#end').is_disabled()
 ok('Battle ends when a squad falls; winners revive allies at one HP')
 p.select_option('#squad','classic')
 with p.expect_download() as dl:p.click('#download')
 dl.value.save_as('/tmp/battle-lab-copy.html')
 copy=browser.new_page();copy.route('**/*',lambda route:route.abort());copy.set_content(Path('/tmp/battle-lab-copy.html').read_text())
 assert copy.evaluate('Lab.state.round===1&&Object.keys(Lab.state.tiles).length===160')
 assert copy.evaluate("document.getElementById('squad').value!=='engineer'||!document.getElementById('engineerSub').disabled")
 copy.close();p.locator('summary').last.click()
 with p.expect_download() as dl:p.click('#report')
 result=json.loads(Path(dl.value.path()).read_text())
 assert result['version']=='0.8.8-lab' and result['combat']=='block-dodge' and 'blocks' in result
 ok('Standalone backup boots offline; exported report identifies updated version')
 p.goto(base);p.wait_for_function('Game.painter.ready');p.get_by_role('button',name='Пробный бой 4 на 4',exact=True).click()
 frame=p.frame_locator('#battleLabOverlay iframe');frame.locator('#phase').wait_for();p.locator('#battleLabOverlay > button').click()
 p.evaluate('Game.newGame(813);Game.fx.configure({enabled:false})');before=p.evaluate('JSON.stringify(Game.state)')
 p.evaluate("document.getElementById('openBattleLab').click()")
 frame.locator('#engineerSub').select_option('armorer');frame.locator('#end').click();frame.locator('#skipAll').click();frame.locator('#end').click()
 p.wait_for_timeout(200);p.locator('#battleLabOverlay > button').click()
 assert p.evaluate('JSON.stringify(Game.state)')==before
 ok('Integrated experiment leaves campaign state unchanged')
 p.goto(base+'/battle-lab.html');p.uncheck('#motion');p.fill('#critChance','0');p.dispatch_event('#critChance','change')
 summaries=p.evaluate("""async()=>{const results=[];for(const sub of ['base','armorer','demolitionist','fortifier']){document.getElementById('engineerSub').value=sub;for(const scenario of ['equal','cover','rescue']){Lab.reset(scenario);let rounds=0;while(Lab.state.winner===null&&rounds++<30){for(const u of Lab.state.units.filter(u=>u.side===0&&u.hp>0)){document.querySelector('[data-select="'+u.id+'"]').click();let n=0;while((u.ap>0||u.stride>0)&&Lab.state.winner===null&&n++<10){let done=false;if(u.type==='acolyte'){const t=Lab.state.units.filter(t=>t.side===0&&t.hp<=t.max-10).sort((a,b)=>a.hp-b.hp).find(t=>!Lab.check(u,t,'heal'));if(t)done=Lab.apply(u,t,'heal')}if(!done){const options=[];for(const t of Lab.state.units.filter(t=>t.side===1&&t.hp>0)){const f=Lab.forecast(u,t,'attack');if(f.ok)options.push({t,f})}options.sort((a,b)=>a.t.hp-b.t.hp);if(options.length)done=Lab.apply(u,options[0].t,'attack')}if(!done){const dest=Lab.approach(u,Lab.state.units.filter(t=>t.side===1&&t.hp>0));if(dest){await Lab.chooseTile(dest.q,dest.r);done=true}}if(!done)break}}if(Lab.state.winner===null){Lab.skipAll();await Lab.endTurn()}}results.push({sub,scenario,winner:Lab.state.winner,round:Lab.state.round,actions:Lab.state.actions})}}return results}""")
 assert all(r['winner'] is not None and r['round']<=30 for r in summaries),summaries
 print('Completion metrics:',summaries,flush=True)
 ok('All scenarios reach a result with each engineer subclass; no AI or turn-lock deadlocks')
 p.goto(base+'/battle-lab.html');p.select_option('#scenario','cover');p.click('[data-select="p1"]');p.click('[data-action="attack"]');p.screenshot(path='/tmp/battle-lab-084-cover.png',full_page=True)
 p.set_viewport_size({'width':390,'height':844});p.screenshot(path='/tmp/battle-lab-084-mobile.png',full_page=True)
 assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert not errors,errors
 ok('Desktop and mobile preserve readable controls and contained map scrolling without browser errors')
 browser.close()
server.shutdown()
print(f'{len(passed)} battle lab scenarios passed.')

```

### `tests/test_battle_editor.py`

```python
"""Regression scenarios for ranged engagement, class defenses, barrier and custom terrain."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright
import json,os
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/battle-lab.html'
passed=[]
def ok(t):passed.append(t);print('PASS:',t,flush=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
 p=b.new_page(viewport={'width':1700,'height':1200});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto(url);p.uncheck('#motion');p.fill('#critChance','0');p.dispatch_event('#critChance','change')
 p.evaluate("Object.assign(Lab.state.units[4],{q:3,r:4});Object.assign(Lab.state.units[5],{q:6,r:4});Lab.render()")
 p.click('[data-select="p1"]')
 assert p.locator('[data-action="attack"]').is_disabled() and p.locator('[data-action="frost"]').is_disabled()
 assert 'Рядом враг' in p.locator('[data-action="attack"]').get_attribute('title')
 assert not p.evaluate("Lab.apply(Lab.state.units[1],Lab.state.units[5],'attack')")
 assert p.evaluate('Lab.state.units[1].ap')==3
 p.locator('[data-q="1"][data-r="4"]').click()
 assert p.locator('[data-action="attack"]').is_enabled()
 assert p.evaluate("Lab.forecast(Lab.state.units[1],Lab.state.units[5],'attack').ok")
 p.evaluate("Object.assign(Lab.state.units[6],{q:0,r:4});Lab.render()")
 assert p.locator('[data-action="attack"]').is_disabled()
 ok('Adjacent enemies prevent ranged shots and specials; moving away must clear all adjacent threats')
 result=p.evaluate("()=>{Lab.reset();const mage=Lab.state.units[3],enemy=Lab.state.units[4],ally=Lab.state.units[0];Object.assign(enemy,{q:3,r:6});ally.hp=10;return {shot:Lab.check(mage,enemy,'attack'),heal:Lab.check(mage,ally,'heal'),plan:Lab.approach(mage,[enemy])}}")
 assert 'Рядом враг' in result['shot'] and result['heal']=='' and result['plan'] is not None
 ok('Engagement also blocks offensive magic while healing remains legal; escape path exists')
 result=p.evaluate("()=>{Lab.reset();const u=Lab.state.units[0],t=Lab.state.units[3],d={baseDamage:10,damage:'piercing',name:'Тест',undodgeable:true};const a=Lab.hit(u,t,d),after1={hp:t.hp,barrier:t.barrier},c=Lab.hit(u,t,d),after2={hp:t.hp,barrier:t.barrier};Lab.startSide(1);const enemyTurn=t.barrier;Lab.startSide(0);const ownTurn=t.barrier;for(let i=0;i<5;i++)Lab.startSide(0);return {a,c,after1,after2,enemyTurn,ownTurn,cap:t.barrier}}")
 assert result['after1']=={'hp':18,'barrier':3} and result['after2']=={'hp':12,'barrier':0}
 assert result['enemyTurn']==0 and result['ownTurn']==4 and result['cap']==12
 ok('Mage barrier absorbs post-defense damage, regenerates only on own turns and caps at twelve')
 result=p.evaluate("()=>{Lab.reset();const u=Lab.state.units[0],t=Lab.state.units[3];Lab.hit(u,t,{baseDamage:1000,damage:'piercing',name:'Тест',undodgeable:true});Lab.startSide(0);return {hp:t.hp,barrier:t.barrier,ap:t.ap}}")
 assert result=={'hp':0,'barrier':0,'ap':0}
 ok('Unconscious mage gains neither barrier nor actions')
 result=p.evaluate("()=>{let misses=0,hits=0;for(let i=0;i<40;i++){Lab.reset();const u=Lab.state.units[0],t=Lab.state.units[5];Object.assign(t,{q:3,r:3});Lab.state.seed=i*1000003;const before=t.hp;Lab.apply(u,t,'break');if(t.hp===before){misses++;if(t.exposed||u.ap!==1||u.cooldown!==3)throw Error('Miss caused a debuff or free action')}else hits++}return {misses,hits}}")
 assert 0<result['misses']<40 and result['hits']>0
 p.select_option('#squad','classic');p.click('[data-select="p2"]');assert 'уклонение 25%' in p.inner_text('#stats')
 p.click('[data-select="p1"]');assert 'уклонение 20%' in p.inner_text('#stats')
 ok('Dodge genuinely avoids attacks and debuffs but still spends attacker AP and cooldown; percentages are visible')
 p.evaluate('Lab.reset()');assert p.locator('#board .hero-figure').count()==8
 assert p.locator('.hero-figure[data-class="warrior"] image.pixel-body').count()>0
 assert p.locator('.hero-figure[data-class="acolyte"] image.pixel-body').count()>0
 assert p.locator('.barrier-aura').count()==2
 ok('Heroes render as distinct equipped figures, with a separate mage barrier aura')
 p.click('#editorToggle');assert p.evaluate('Lab.editing')
 assert p.locator('#end').is_disabled() and p.locator('[data-action="attack"]').is_disabled()
 p.select_option('#terrainBrush','rock');p.select_option('#heightBrush','1');p.locator('[data-q="6"][data-r="3"]').click()
 assert p.evaluate("Lab.state.tiles['6,3'].kind==='rock'&&Lab.state.tiles['6,3'].height===1&&Lab.state.actions===0")
 p.locator('[data-q="2"][data-r="3"]').click()
 assert p.evaluate("Lab.state.tiles['2,3'].kind==='plain'")
 assert 'защищен' in p.inner_text('#editorStatus')
 p.click('#saveLayout');p.click('#restart')
 assert p.evaluate("!Lab.editing&&Lab.state.tiles['6,3'].kind==='rock'")
 p.reload();p.uncheck('#motion');p.fill('#critChance','0');p.dispatch_event('#critChance','change')
 assert p.evaluate("Lab.state.tiles['6,3'].kind==='rock'&&Lab.state.tiles['6,3'].height===1")
 ok('Editor pauses combat, protects hero starts and preserves custom terrain across restart and reload')
 p.click('#editorToggle')
 with p.expect_download() as dl:p.click('#exportLayout')
 layout=json.loads(Path(dl.value.path()).read_text());assert len(layout['tiles'])==160
 before=p.evaluate('JSON.stringify(Lab.state.tiles)')
 p.locator('#layoutFile').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{"format":"bad"}'})
 p.wait_for_function("document.getElementById('editorStatus').textContent.includes('Неверный')")
 assert p.evaluate('JSON.stringify(Lab.state.tiles)')==before
 p.click('#restoreLayout');assert p.evaluate("Lab.state.tiles['6,3'].kind==='plain'")
 p.locator('#layoutFile').set_input_files({'name':'map.json','mimeType':'application/json','buffer':json.dumps(layout).encode()})
 p.wait_for_function("document.getElementById('editorStatus').textContent.includes('загружено')")
 assert p.evaluate("Lab.state.tiles['6,3'].kind==='rock'")
 ok('Map export/import round-trips; invalid input leaves the current map untouched')
 with p.expect_download() as dl:p.click('#download')
 raw=Path(dl.value.path()).read_text()
 fresh=b.new_context();copy=fresh.new_page();copy.route('**/*',lambda route:route.abort());copy.set_content(raw)
 assert copy.evaluate("Lab.state.tiles['6,3'].kind==='rock'&&Lab.state.tiles['6,3'].height===1&&!Lab.editing")
 fresh.close()
 ok('Standalone game copy includes the custom terrain without requiring browser storage or network')
 p.click('#restoreLayout');p.click('#editorToggle');p.evaluate("const u=Lab.state.units[0];Object.assign(u,{q:5,r:3});Lab.state.tiles['6,3'].height=1;Lab.render()")
 assert p.evaluate("Lab.paths(Lab.state.units[0]).get('6,3').cost")==2
 p.evaluate("Lab.state.tiles['6,3'].height=2;Lab.render()")
 assert not p.evaluate("Lab.paths(Lab.state.units[0]).has('6,3')")
 assert not p.evaluate('Lab.los({q:5,r:3},{q:8,r:3})')
 p.evaluate("Lab.state.tiles['6,3'].height=0;Lab.state.tiles['6,3'].kind='water';Lab.render()")
 assert not p.evaluate("Lab.paths(Lab.state.units[0]).has('6,3')")
 p.evaluate("Lab.state.tiles['6,3'].kind='forest'")
 assert not p.evaluate('Lab.los({q:5,r:3},{q:8,r:3})')
 ok('Elevation changes path cost and line of sight; steep cliffs, forests and water block movement')
 p.evaluate('Lab.reset()');p.locator('[data-q="3"][data-r="3"]').click();p.click('#editorToggle')
 assert not p.evaluate('Lab.editing') and 'до первого действия' in p.inner_text('#notice')
 ok('Editor cannot change the battlefield after combat actions have begun')
 p.evaluate("Lab.reset('cover')");p.click('#editorToggle');p.select_option('#terrainBrush','water');p.locator('[data-q="6"][data-r="6"]').click();p.screenshot(path='/tmp/battle-lab-083-editor.png',full_page=True)
 p.click('#editorToggle');p.click('[data-select="p3"]');p.click('[data-action="attack"]');p.screenshot(path='/tmp/battle-lab-083-figures.png',full_page=True)
 p.set_viewport_size({'width':390,'height':844});p.click('#editorToggle')
 assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert not errors,errors
 ok('Editor and figures work on desktop and narrow screens without script errors')
 b.close()
server.shutdown()
print(len(passed),'editor and combat scenarios passed.')

```

### `tests/test_progression.py`

```python
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
 result=p.evaluate("()=>{const u=Lab.state.units[0],t=Lab.state.units[4],d={name:'Крит',baseDamage:10,damage:'magic',undodgeable:true};t.hp=100;Lab.state.critChance=1;const f=Lab.damageForecast(u,t,d),r=Lab.hit(u,t,d);return {critical:r.critical,damage:r.damage,hp:t.hp,forecast:f.criticalDamage,stress:t.stress}}")
 assert result=={'critical':True,'damage':12,'hp':88,'forecast':12,'stress':10}
 p.fill('#critChance','0');p.dispatch_event('#critChance','change')
 result=p.evaluate("()=>{const u=Lab.state.units[0],t=Lab.state.units[4];return Lab.hit(u,t,{name:'Обычный',baseDamage:10,damage:'magic',undodgeable:true})}")
 assert result['critical'] is False and result['damage']==8
 ok('Critical multiplier is applied before defense, matches forecast and increases stress; zero percent disables it')
 p.select_option('#playerLevel','5');p.select_option('#enemyLevel','3')
 assert p.evaluate('Lab.state.units[0].max===48&&Lab.state.units[3].max===26&&Lab.state.units[3].barrier===20&&Lab.state.units[4].max===40')
 p.select_option('#warriorSub','bastion');assert p.evaluate('Lab.defense(Lab.state.units[0],"piercing")')==48
 p.select_option('#warriorSub','berserker');assert p.evaluate('Lab.spec(Lab.state.units[0],"attack").baseDamage')==12
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
 result=p.evaluate("()=>{const u=Lab.state.units[4],v=Lab.state.units[5],t=Lab.state.units[0];Object.assign(u,{q:3,r:3});Object.assign(v,{q:3,r:2});const pack=Lab.spec(u,'attack',t).baseDamage;v.q=12;v.r=0;return {pack,alone:Lab.spec(u,'attack',t).baseDamage}}")
 assert result['pack']-result['alone']==2
 p.select_option('#playerLevel','2');p.select_option('#enemyType','spiders')
 result=p.evaluate("()=>{const u=Lab.state.units[4],t=Lab.state.units[0];Object.assign(u,{q:4,r:3});Lab.state.side=1;const ok=Lab.apply(u,t,'web');return {ok,slow:t.slow}}")
 assert result=={'ok':True,'slow':1}
 p.select_option('#enemyType','undead');assert p.evaluate('Lab.defense(Lab.state.units[4],"piercing")>Lab.defense(Lab.state.units[4],"slashing")')
 p.evaluate("Lab.state.critChance=1;Lab.hit(Lab.state.units[0],Lab.state.units[4],{name:'Крит',baseDamage:100,damage:'magic',undodgeable:true})")
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
 p.evaluate("Lab.reset('convoy');Object.assign(Lab.state.units[0],{q:4,r:5,hp:0,ap:0});Object.assign(Lab.state.units[1],{q:4,r:4});Lab.carryHero(Lab.state.units[1],'p0');Lab.hit(Lab.state.units[4],Lab.state.units[1],{name:'Удар',baseDamage:1000,damage:'magic',undodgeable:true,noCrit:true});Lab.render()")
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

```

### `tests/test_subclass_skills.py`

```python
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
 before=p.evaluate("({d:Lab.spec(Lab.state.units[0],'attack').baseDamage,r:Lab.defense(Lab.state.units[0],'piercing')})")
 p.click('[data-action="rage"]')
 after=p.evaluate("({d:Lab.spec(Lab.state.units[0],'attack').baseDamage,r:Lab.defense(Lab.state.units[0],'piercing')})")
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
 loss=p.evaluate('100-Lab.state.units[4].hp')
 assert loss in {2*f['normalDamage'], f['normalDamage']+f['blockedDamage'], 2*f['blockedDamage']}
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
 normal=p.evaluate("Lab.spec(Lab.state.units[3],'smite').baseDamage");undead=p.evaluate("Lab.spec(Lab.state.units[3],'smite',Lab.state.units[4]).baseDamage");assert undead==normal+4
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

```

### `tests/test_relations_and_bestiary.py`

```python
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
 assert p.evaluate('''()=>{
   Game.newGame(709);
   const a=Game.state.factions[0].armies[0];
   Game.startBattle(a,null,{kind:'ambush',family:'spiders',title:'Паучья засада',pos:a.pos});
   const b=Game.state.battle, spider=b.units.find(u=>u.monster==='spider'), hero=b.units.find(u=>u.cls==='warrior');
   b.field.cells.fill('ground');b.side=spider.side;spider.pos=18;hero.pos=19;
   return Game.attackBattle(spider,hero)&&hero.snaredUntil===b.round+1;
 }''')
 assert p.evaluate('Game.bestiary.speed(Game.state.battle.units.find(u=>u.cls==="warrior"))')==1
 p.screenshot(path='/tmp/v07-spiders.png')
 p.evaluate('Game.state.battle.round+=2')
 assert p.evaluate('Game.bestiary.speed(Game.state.battle.units.find(u=>u.cls==="warrior"))')==2
 p.evaluate('''()=>{Game.newGame(710);const a=Game.state.factions[0].armies[0];Game.startBattle(a,null,{kind:'ambush',family:'wolves',title:'Волчья стая',pos:a.pos});const b=Game.state.battle;b.field.cells.fill('ground');const w=b.units.filter(u=>u.monster==='wolf'),hero=b.units.find(u=>u.side===0);w[0].pos=18;w[1].pos=10;hero.pos=19;}''')
 assert p.evaluate('''()=>{const b=Game.state.battle;return Game.bestiary.attackBonus(b.units.find(u=>u.monster==='wolf'),b.units.find(u=>u.side===0))}''')==2
 ok('Spider hits actually slow movement and expire; wolves receive their pack attack bonus')
 result=p.evaluate("""()=>{
   Game.newGame(711);
   const a=Game.state.factions[0].armies[0];
   Game.relations.adjust(a.heroes[0],a.heroes[1],2,'Спасение в бою');
   Game.startBattle(a,null,{kind:'ambush',family:'bandits',title:'Проверка прикрытия',pos:a.pos});
   const b=Game.state.battle, [warrior,ally,enemy]=b.units;
   b.field.cells.fill('ground');
   warrior.pos=9;
   Object.assign(ally,{pos:17,physicalArmor:0,hp:100,max:100});
   Object.assign(enemy,{pos:18,damage:20});
   function damage(){
     b.side=1;ally.hp=100;enemy.ap=3;
     if(!Game.attackBattle(enemy,ally))throw Error('Expected a legal physical attack');
     return 100-ally.hp;
   }
   const exposed=damage();
   b.side=0;warrior.ap=2;
   const supported=Game.relations.support(warrior,ally);
   const covered=damage();
   b.side=0;
   const moved=Game.moveBattle(warrior,1);
   return {exposed,supported,covered,moved,uncoveredAfterMove:damage()};
 }""")
 assert result=={'exposed':20,'supported':True,'covered':19,'moved':True,'uncoveredAfterMove':20}
 ok('Manual support reduces fixed physical damage while the friend stays adjacent')
 result=p.evaluate("""()=>{Game.newGame(712);const s=Game.state,a=s.factions[0].armies[0];a.pos=35;s.map[35].site={type:'camp',cleared:false};Game.startBattle(a,null,{kind:'camp',family:'bandits',title:'Старый бой',pos:35});const legacy=JSON.parse(JSON.stringify(s));for(const c of legacy.map)if(c.site)delete c.site.family;for(const v of legacy.villages)delete v.threatFamily;for(const u of legacy.battle.units)delete u.monster;delete legacy.battle.meta.family;legacy.factions[0].armies[0].conflict={first:a.heroes[0].id,second:a.heroes[1].id,created:1};const before=JSON.stringify(legacy.battle.units),loaded=Game.load(legacy);return{loaded,sameUnits:before===JSON.stringify(Game.state.battle.units),clearedTimer:!Game.state.factions[0].armies[0].conflict,family:Game.state.map[35].site.family};}""")
 assert result=={'loaded':True,'sameUnits':True,'clearedTimer':True,'family':'bandits'}
 ok('Legacy saves keep their current battle and remove only the old causeless calendar dispute')
 assert not errors,errors
 b.close()
server.shutdown();print(f'{len(passed)} relationship and creature scenarios passed.')

```
