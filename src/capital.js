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
    // Stable identifiers: hall and walls share the capital plot, so the plot alone is ambiguous.
    for(const q of t.projects) q.uid ??= id('q');
  }

  // Every hero who still belongs to the house: squads, retreating heroes, the morgue and own wagons.
  function heroesOf(f) {
    return [...f.armies.flatMap(a=>a.heroes),...(f.retreats||[]).map(r=>r.hero),...(f.morgue||[]),
      ...S.convoys.filter(c=>c.owner===f.id&&c.kind!=='prisoners').flatMap(c=>c.cargo)];
  }

  function level(f, cls) { return f.town.classRanks?.[cls]?.floor || 1; }
  function project(f,p,key,kind) {
    init(f);
    const t=f.town, d=BUILD[key], old=t.buildings[p];
    // Hall and walls both sit on the capital plot and may be queued together; any other plot takes one project at a time.
    const civic=k=>k==='hall'||k==='walls';
    if (!d || t.projects.some(q=>q.plot===p&&!(civic(q.kind)&&civic(kind)&&q.kind!==kind))) return null;
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
    // The id is issued only for a real queued project: previews must not consume the serial counter.
    q.uid=id('q');
    f.town.projects.push(q);
    if(f.id===0) FX.city(p,'start',BUILD[key].name+': в очереди');
    return true;
  }

  // key: project uid (interface) or plot number (older callers and tests).
  function edit(f,key,action) {
    init(f);
    const list=f.town.projects, index=list.findIndex(q=>typeof key==='string'?q.uid===key:q.plot===key), q=list[index];
    if(!q) return false;
    if(action==='pause') q.paused=!q.paused;
    if(action==='first') list.unshift(list.splice(index,1)[0]);
    if(action==='cancel') {
      const left=q.work-q.progress;
      // Design 2026-11-08: refund = ceil(paid × remaining share), never more than paid.
      const refund=paid=>Math.min(paid,Math.ceil(paid*left/q.work-1e-9));
      f.gold+=refund(q.gold);
      f.crystal+=refund(q.crystal);
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

  // Returns production left after the construction queue; crafting may use it.
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
    return Math.max(0,production);
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
    for(const h of heroesOf(f)) if(h.cls===cls) bonuses(f,h);
    Development.updateCandidates(f);
    return true;
  }

  function demolish(f,p) {
    init(f);
    if(!f.town.buildings[p]||f.town.projects.some(q=>q.plot===p)) return false;
    const cls=Object.keys(classes).find(c=>classes[c]===f.town.buildings[p]);
    if(cls) {
      for(const h of heroesOf(f)) if(h.cls===cls) bonuses(f,h);
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
      ${button('capitalEdit',q.paused?'Возобновить':'Пауза',`data-id="${q.uid}" data-pos="${q.plot}" data-v="pause"`)}
      ${button('capitalEdit','В начало',`data-id="${q.uid}" data-pos="${q.plot}" data-v="first"`)}
      ${button('capitalEdit','Отменить',`data-id="${q.uid}" data-pos="${q.plot}" data-v="cancel"`)}</li>`).join('');
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
