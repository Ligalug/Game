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
