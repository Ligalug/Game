// Transient presentation timeline. Never changes game state or consumes game RNG.
const FX=(()=>{
 const $=id=>document.getElementById(id);
 const SCHOOL={fire:{name:'Пламя',c:['#ff9a4a','#ffd08a']},water:{name:'Лёд и вода',c:['#6fc3ff','#d6f2ff']},air:{name:'Ветер и молния',c:['#e2f6ff','#ffffff']},earth:{name:'Камень',c:['#c09a62','#ead3a2']},light:{name:'Свет',c:['#ffe58a','#fff7cf']},dark:{name:'Тьма',c:['#a77bd6','#dcc5ff']},astral:{name:'Магический болт',c:['#94d7ed','#bdebf9']}};
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
 function impact(u,t,amount,type,{critical=false,defense=null,school=null}={}){
   const label=defense==='dodge'?'Уклонение':defense==='block'?'Блок':critical?'Критическое попадание':type==='magic'?(SCHOOL[school]?.name||'Магия'):'Атака';
   return effect(type,u.pos,t.pos,{actor:u.id,target:t.id,hpBefore:t.hp,hpAfter:t.hp,amount,critical,defense,school,label});
 }
 // Presentation-only poses for the current battle effect: attacker lunge or recoil, target recoil, flash, shield, dodge, fall and rise.
 function pose(u){
   const e=current;
   if(!e||e.type!=='effect'||e.mode!=='battle'||!u||e.battleId!==S?.battle?.id)return null;
   const p=e.p||0,out={from:e.from,to:e.to,crit:!!e.critical};let any=false;
   if(['slash','arrow','magic'].includes(e.kind)){
     if(u.id===e.actor){any=true;if(e.kind==='slash')out.lunge=Math.sin(Math.min(1,p/.65)*Math.PI);else out.recoil=p<.3?Math.sin(p/.3*Math.PI):0;}
     if(u.id===e.target&&p>.45){
       any=true;const k=(p-.45)/.55;
       if(e.defense==='dodge')out.dodge=Math.sin(k*Math.PI);
       else{out.shake=Math.sin(k*42)*(1-k)*(e.critical?5:3);out.knock=Math.sin(Math.min(1,k*2)*Math.PI)*(e.critical?1.5:1);out.flash=Math.max(0,1-k*2.4);if(e.defense==='block')out.shield=1-k;if(e.hpAfter!=null&&e.hpAfter<=0)out.fall=ease(Math.min(1,k*1.6));}
     }
   }
   if(['heal','revive'].includes(e.kind)&&u.id===e.target&&e.hpBefore!=null&&e.hpBefore<=0){any=true;out.rise=ease(Math.min(1,p*1.4));}
   return any?out:null;
 }
 // Camera shake for critical hits, deterministic (no game randomness is consumed).
 function shake(){
   const e=current;
   if(!e||e.type!=='effect'||e.mode!=='battle'||!e.critical||e.defense==='dodge'||(e.p||0)<.45)return{x:0,y:0};
   const k=((e.p||0)-.45)/.55,a=5*(1-k);
   return{x:Math.sin(k*61)*a,y:Math.cos(k*53)*a*.6};
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
       const sc=(SCHOOL[e.school]||SCHOOL.astral).c;
       ctx.strokeStyle=e.kind==='magic'?sc[0]:'#e9dbaf';ctx.fillStyle=e.kind==='magic'?sc[1]:'#e8dcae';ctx.beginPath();ctx.moveTo(px-(to.x-from.x)*.14,py-(to.y-from.y)*.14);ctx.lineTo(px,py);ctx.stroke();ctx.fillRect(px-2,py-2,4,4);
       if(e.kind==='magic'&&p<.55){for(let k=1;k<=4;k++){ctx.globalAlpha=.6-k*.12;ctx.fillStyle=sc[k%2];const q=Math.max(0,t-k*.06);ctx.fillRect(from.x+(to.x-from.x)*q-2,from.y+(to.y-from.y)*q-26,4,4);}ctx.globalAlpha=1;ctx.fillStyle=sc[1];ctx.beginPath();ctx.arc(px,py,4.5,0,Math.PI*2);ctx.fill();}
     }else{const u=Math.sin(Math.min(1,p/.65)*Math.PI);ctx.translate(from.x+(to.x-from.x)*u*.16,from.y+(to.y-from.y)*u*.16);ctx.strokeStyle='#e8dcbb';ctx.beginPath();ctx.moveTo(5-14*u,-45);ctx.lineTo(18,-15+12*u);ctx.stroke();ctx.translate(-(from.x+(to.x-from.x)*u*.16),-(from.y+(to.y-from.y)*u*.16));}
     if(p>.45){
       ctx.globalAlpha=Math.max(0,1-(p-.45)/.55);
       const sc=(SCHOOL[e.school]||SCHOOL.astral).c;
       ctx.fillStyle=e.defense?'#bdebf9':e.critical?'#ffe195':e.kind==='magic'?sc[1]:'#f3b293';
       const text=e.defense==='dodge'?'Уклонение':e.defense==='block'?`Блок · −${e.amount}`:`−${e.amount}`;
       ctx.fillText(text,x,y-48-(p-.45)*30);
       const n=e.defense==='dodge'?0:e.critical?14:e.kind==='magic'?12:8,size=e.school==='earth'?4:3;
       for(let k=0;k<n;k++){const a=k*Math.PI*2/n,r=6+(p-.45)*(e.critical?48:34);if(e.kind==='magic')ctx.fillStyle=sc[k%2];ctx.fillRect(x+Math.cos(a)*r,y-22+Math.sin(a)*r*.7+(e.school==='earth'?(p-.45)*30:0),size,size-1);}
       if(e.defense==='block'){ctx.globalAlpha=Math.max(0,1-(p-.45)/.55);ctx.strokeStyle='#f3dd98';ctx.lineWidth=3;ctx.beginPath();ctx.arc(x,y-24,20+(p-.45)*14,-Math.PI*.8,-Math.PI*.2);ctx.stroke();}
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
 return{pose,shake,roll,move,reveal,effect,impact,city,position,revealAlpha,hp,ghosts,overlay,paintCity,auto,whenIdle,finish,reset,configure,openSettings,mute(v){muted+=v?1:-1;muted=Math.max(0,muted);},get busy(){return !!current||queue.length>0;},get active(){return current?{...current}:null;},get queue(){return queue.map(e=>({...e}));},get history(){return history.slice();},get settings(){return{...settings};}};
})();
