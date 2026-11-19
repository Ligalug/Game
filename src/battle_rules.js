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
      FX.impact(u,t,0,type,{defense:'dodge',school:magic?school:null});
      b.log.unshift(`${u.name} → ${t.name}: уклонение.`);
      return true;
    }
    u.didHit=true;
    const raw=Math.max(1,u.damage+Relations.rivalBonus(u)+Bestiary.damageBonus(u)+(special&&u.cls!=='warrior'?5:0));
    const protection=activeUnits(b,t.side).filter(v=>v!==t&&dist(v.pos,t.pos,8)===1).reduce((n,v)=>n+(v.talents?.support||0)+(v.sub==='captain'?3:v.sub==='fortifier'?4:0),0);
    const target={...t,physicalArmor:(t.physicalArmor??Math.max(0,(t.slash||10)-10)*3)+protection+(t.guard?10:0)+(t.friendCover&&activeUnits(b,t.side).some(u=>u.id===t.friendCover&&dist(u.pos,t.pos,8)===1)?5:0)+(t.wardUntil>=b.round?10:0)+(t.greaterWard>=b.round?15:0)};
    const dealt=damage([{type:magic?school:'physical',penetration:magic?(u.branch?.magicPen||0):(u.branch?.penetration||0),value:raw*(special&&u.cls==='warrior'?1.5:1)*(free?.75:1)}],target,critical,blocked);
    if(blocked) t.guardBlock=false;
    const before=t.hp, effect=FX.impact(u,t,dealt,type,{critical,defense:blocked?'block':null,school:magic?school:null});
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
    // With a house as winner the gear becomes shared loot; after a defeat by monsters it stays with the remains.
    if(m.winner!=null) {
      m.loot.push(...h.items);
      h.items=[];
    }
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
