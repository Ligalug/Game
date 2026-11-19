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
