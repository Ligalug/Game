const Tips=(()=>{
 const el=document.createElement('div');el.id='abilityTooltip';el.role='tooltip';el.hidden=true;document.body.append(el);let target=null,timer;
 function hide(){clearTimeout(timer);if(target)target.removeAttribute('aria-describedby');target=null;el.hidden=true;}
 function show(t){if(!t?.isConnected)return;target=t;el.textContent=t.dataset.tip;el.hidden=false;t.setAttribute('aria-describedby','abilityTooltip');const r=t.getBoundingClientRect(),w=el.offsetWidth,h=el.offsetHeight;el.style.left=Math.max(10,Math.min(innerWidth-w-10,r.left))+'px';el.style.top=Math.max(10,r.top-h-8>=10?r.top-h-8:Math.min(innerHeight-h-10,r.bottom+8))+'px';}
 document.addEventListener('pointerover',e=>{const t=e.target.closest('[data-tip]');if(!t||t===target)return;hide();target=t;timer=setTimeout(()=>show(t),180);});
 document.addEventListener('pointerout',e=>{if(target?.contains(e.target)&&!target.contains(e.relatedTarget))hide();});
 document.addEventListener('focusin',e=>{const t=e.target.closest('[data-tip]');if(t){hide();show(t);}});
 document.addEventListener('focusout',e=>{if(target?.contains(e.target)&&!target.contains(e.relatedTarget))hide();});
 document.addEventListener('click',hide);document.addEventListener('keydown',e=>{if(e.key==='Escape')hide();});window.addEventListener('resize',hide);document.addEventListener('scroll',hide,true);
 function ability(u,k){if(!u)return'';let text='';const end=u.sub==='swift'?'Расходует 1 ОД.':'Завершает действия героя.';
  if(k==='bolt')text=`Магический болт\nДальность: 4 гекса; нужна линия видимости.\nПопадание: d20 + атака против магической КБ. Урон: d${u.die} + ${u.damage+(u.sub==='elementalist'?6:0)+Relations.rivalBonus(u)}. Укрытие даёт цели +2 КБ.\nЦена: 2 маны. ${end}`;
  if(k==='heal')text=`Лечение\nВосстанавливает до ${14+(['priest','highpriest'].includes(u.sub)?8:0)} ХП союзнику или себе. Поднимает героя без сознания с 1 ОД.\nДальность: 4 гекса; нужна линия видимости.\nЦена: 3 маны. Завершает действия героя.`;
  if(k==='ward')text='Оберег\nДаёт союзнику или себе +3 ко всем видам КБ до конца следующего раунда.\nДальность: 4 гекса; нужна линия видимости.\nЦена: 2 маны. Завершает действия героя.';
  if(k==='curse')text=`Проклятье\nСнижает атаку врага на 3 до конца следующего раунда; добавляет ${u.sub==='cultist'?22:10} стресса герою.\nДальность: 4 гекса; нужна линия видимости.\nЦена: 2 маны. Завершает действия героя.`;
  if(k==='skill')text=u.cls==='acolyte'?'Медитация\nВосстанавливает до 4 маны, не выше максимума.\nЦена: 1 ОД. Можно повторять.':u.cls==='warrior'?'Второе дыхание\nВосстанавливает себе до 14 ХП.\nЦена: 1 ОД. Один раз за бой.':`Особая атака\nВыберите противника. Для попадания бросаются два d20, используется лучший результат.\nПри попадании: дополнительно ${u.cls==='rogue'?7:5} урона.\n${end} Один раз за бой.`;
  if(k==='support')text='Прикрыть друга\nДруг на соседней клетке получает +2 ко всем видам КБ, пока вы рядом и в строю, до начала следующего хода вашей стороны.\nДоступно при доверии от +2. Цена: 1 ОД. Каждая пара — один раз за бой. Выберите цель сами.';
  if(k==='guard')text='Оборона\n+2 ко всем видам КБ до начала следующего хода вашей стороны.\nРасходует все оставшиеся ОД.';
  return text;
 }
 function button(a,text,extra,disabled,u,k){const tip=Tips.ability(u,k);return`<span class="ability-tip" tabindex="${disabled?0:-1}" data-tip="${esc(tip)}">${globalButton(a,text,extra,disabled)}</span>`;}
 // Kept separate from the exported method so the game's button helper stays in scope.
 function globalButton(a,text,extra,disabled){return `<button data-a="${a}" ${extra||''} ${disabled?'disabled':''}>${text}</button>`;}
 return{ability,button,hide};
})();
