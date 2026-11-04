// Familiar fantasy creatures, with original prototype statistics for this game's d20 rules.
const Bestiary=(()=>{
 const species={
  bandit:{name:'Разбойник',hp:24,ac:12,pierce:13,slash:13,atk:6,die:6,damage:3,range:1,speed:3,look:'bandit',text:'Боец ближнего боя.'},
  banditArcher:{name:'Разбойник-стрелок',hp:22,ac:12,pierce:13,slash:12,atk:6,die:6,damage:3,range:4,speed:3,look:'bandit',text:'Стреляет с четырёх гексов.'},
  wolf:{name:'Волк',hp:22,ac:12,pierce:12,slash:12,atk:6,die:6,damage:3,range:1,speed:4,look:'wolf',text:'Стая: +2 к атаке, если ещё один волк стоит рядом с целью.'},
  spider:{name:'Гигантский паук',hp:27,ac:13,pierce:13,slash:12,atk:6,die:6,damage:3,range:1,speed:3,look:'spider',text:'Попадание опутывает: −1 к движению до конца следующего раунда.'},
  spinner:{name:'Паук-плетельщик',hp:20,ac:12,pierce:12,slash:11,atk:6,die:4,damage:2,range:3,speed:3,look:'spider',text:'Стреляет липкой паутиной с трёх гексов; попадание замедляет.'},
  goblin:{name:'Гоблин',hp:20,ac:13,pierce:13,slash:12,atk:6,die:6,damage:2,range:1,speed:4,look:'goblin',text:'Маленькая цель: получает ещё +1 КБ в укрытии от дальних атак.'},
  goblinArcher:{name:'Гоблин-лучник',hp:18,ac:13,pierce:13,slash:12,atk:6,die:6,damage:2,range:4,speed:4,look:'goblin',text:'Подвижный стрелок; ещё +1 КБ в укрытии от дальних атак.'},
  kobold:{name:'Кобольд-копейщик',hp:23,ac:12,pierce:14,slash:12,atk:6,die:6,damage:3,range:1,speed:3,look:'kobold',text:'Защищён от колющих атак.'},
  slinger:{name:'Кобольд-пращник',hp:20,ac:12,pierce:13,slash:11,atk:6,die:6,damage:2,range:3,speed:4,look:'kobold',text:'Быстрый стрелок с пращой.'},
  skeleton:{name:'Скелет',hp:25,ac:12,pierce:16,slash:11,atk:6,die:6,damage:3,range:1,speed:3,look:'skeleton',text:'Кости трудно пробить стрелами: высокая КБ от колющего урона.'},
  zombie:{name:'Зомби',hp:40,ac:10,pierce:10,slash:10,atk:5,die:6,damage:4,range:1,speed:1,look:'zombie',text:'Медленный, но живучий. Нежить не проходит проверки стресса.'},
  ogre:{name:'Огр',hp:72,ac:11,pierce:12,slash:11,atk:7,die:10,damage:5,range:1,speed:2,look:'ogre',level:2,text:'Опасный противник с большим запасом здоровья и тяжёлой дубиной.'},
  boar:{name:'Дикий вепрь',hp:35,ac:12,pierce:12,slash:12,atk:6,die:8,damage:3,range:1,speed:3,look:'boar',text:'Наскок: +2 урона, если перед атакой двигался в этом раунде.'}
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
 function create(a,meta,of){const count=of?4:Math.min(4,Math.max(2,a.heroes.length));if(of)return Array.from({length:count},(_,i)=>({id:id('u'),name:'Страж крепости',side:1,pos:(i+1)*8+6,hp:34,max:34,pierce:16,slash:17,ac:15,atk:8,die:6,damage:3,range:i===count-1?4:1,speed:3,ap:2,mana:0,stress:0,level:1,surrender:false,resolveChecked:false}));
  const key=families[meta.family]?meta.family:meta.kind==='protect'?S.villages[meta.village].threatFamily||'bandits':meta.kind==='ambush'?choose(meta.pos??a.pos,true):family(meta.pos??a.pos),f=families[key];meta.family=key;if(['Засада','Разбойники','Лагерь разбойников'].includes(meta.title))meta.title=f.name+(meta.kind==='ambush'?' — засада':'');const n=key==='ogres'?(count<=2?1:2):key==='boars'?2:count;
  return Array.from({length:n},(_,i)=>{const k=f.pack[i%f.pack.length],d=species[k];return{id:id('u'),name:d.name,monster:k,side:1,pos:(i+1)*8+6,hp:d.hp,max:d.hp,pierce:d.pierce,slash:d.slash,ac:d.ac,atk:d.atk,die:d.die,damage:d.damage,range:d.range,speed:d.speed,ap:2,mana:0,stress:0,level:d.level||1,surrender:false,resolveChecked:false};});
 }
 function attackBonus(u,t){return u.monster==='wolf'&&activeUnits(S.battle,u.side).some(z=>z!==u&&z.monster==='wolf'&&dist(z.pos,t.pos,8)<=1)?2:0;}
 function damageBonus(u){return u.monster==='boar'&&u.movedRound===S.battle.round?2:0;}
 function onHit(u,t){if(['spider','spinner'].includes(u.monster)&&t.hp>0){t.snaredUntil=S.battle.round+1;S.battle.log.unshift(`${t.name} опутан паутиной: движение −1 до конца следующего раунда.`);FX.effect('curse',u.pos,t.pos,{label:'Липкая паутина',text:'Движение −1'});}}
 function speed(u){return Math.max(1,u.speed-(u.snaredUntil>=S.battle.round?1:0));}
 function describe(key){const f=families[key]||families.bandits;return `${f.name}. Угроза: ${f.danger.toLowerCase()}. ${f.pack.map(k=>species[k].name+': '+species[k].text).join(' ')}`;}
 return{species,families,hash,choose,family,populate,upgrade,create,attackBonus,damageBonus,onHit,speed,describe};
})();
