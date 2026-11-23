// Run from a checkout containing the pinned prototype, or supply its root.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const project=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const upstream=path.resolve(process.argv[2]||path.join(project,'..'));
const verify=process.argv.includes('--check');
const files=['game','strike','bestiary','talents','capital','battle_rules'];
const hashes={};
const ctx=vm.createContext({document:{getElementById:()=>({addEventListener(){}}),addEventListener(){}},queueMicrotask(){}});
ctx.window=ctx;
function run(code){return vm.runInContext(code,ctx,{timeout:2500});}
for(const name of files){
  const file='src/'+name+'.js';
  let source=fs.readFileSync(path.join(upstream,file),'utf8');
  hashes[file]=crypto.createHash('sha1').update('blob '+Buffer.byteLength(source)+'\0'+source).digest('hex');
  if(name==='capital'){
    // Class buildings provided by the web's development module have no authorised
    // numeric definition in the six inputs. Предварительно, D01: only retain source IDs.
    run("for (const id of ['plaza','magicacademy']) if(!BUILD[id]) BUILD[id]={external_definition:true};");
    source=source.replace('return {afford,classes,legacy','return {upkeep,ranks,branchUpgrades,afford,classes,legacy');
  }
  run(source);
}
const result=run(`(()=>{
 const f={id:0,city:34,gold:0,crystal:0,bag:[],armies:[],kills:0,town:{plots:[],projects:[]}};
 S={turn:1,factions:[f],villages:[]};newDecree();
 const decrees={};for(const type of ['tribute','patrol','relations','artifact']){
   S.decree.type=type;const d=decreeInfo(f);decrees[type]={name:d.title,text:d.text};
 }
 serial=0;const keys=Object.keys(C);
 const starters=Array.from({length:10},(_,i)=>createHero(keys[i%keys.length]));
 const defenses={crit:Strike.criticalMultiplier,hero_dodge:Strike.heroDodge,warrior_block:Strike.blockChance('warrior',true,false)};
 const talents={};for(const cls of keys){talents[cls]={};for(let l=2;l<=8;l++){
    const opts={};for(const k of ['Нападение','Защита','Поддержка']){
      const h={cls,sub:'example',level:8,talents:{base:{},sub:[],active:[]}};
      if(l>6)h.talents.sub=Array.from({length:l-6},(_,i)=>6+i);
      if(Talents.choose(h,l,k))opts[l<=5?k:'Ветка подкласса']=Talents.effects(h);
    }talents[cls][l]=opts;
 }}
 return {classes:C,subclasses:SUBS,monsters:Bestiary.species,encounters:Bestiary.families,buildings:BUILD,
 legacy_buildings:Capital.legacy,class_buildings:Capital.classes,branch_upgrades:Capital.branchUpgrades,ranks:Capital.ranks,upkeep:Capital.upkeep,
 spells:SPELLS,magic_schools:BattleRules.schools,talents,decrees,terrains:TERRAIN,traits:TRAITS,houses:HOUSES,cities:CITIES,
 names:NAMES,starters,limits:{board:N,party:MAX_PARTY,rounds:LIMIT},defenses};
})()`);
const damage=run(`(()=>{let vectors=[];for(const armor of [0,25,90,120])for(const hit of [false,true])for(const block of [false,true]){
 let components=[{type:'physical',value:8.5,penetration:15},{type:'fire',value:3,penetration:0}];
 let target={physicalArmor:armor,resists:{fire:25}};vectors.push({components,target,critical:hit,blocked:block,expected:BattleRules.damage(components,target,hit,block)});
}return vectors;})()`);
const newGameRng=run('newGame.toString()').match(/let z=seed>>>0;const random=\(\)=>\{[^}]+\};/);
if(!newGameRng) throw Error('Inspect the RNG initializer in newGame before refreshing reference values');
const rng=run(`[0,1,42,4294967295].map(seed=>{${newGameRng[0]}return {seed,values:Array.from({length:6},()=>random()*4294967296)}})`);
const development=fs.readFileSync(path.join(upstream,'src/development.js'),'utf8');
hashes['src/development.js']=crypto.createHash('sha1').update('blob '+Buffer.byteLength(development)+'\0'+development).digest('hex');
// The owner approved this module for recipes and spells only. Evaluate its authored
// table initializers, stopping before the rest of the module patches the web UI.
const begin=development.indexOf('const studies='), end=development.indexOf('const enchantments=');
if(begin<0||end<=begin)throw Error('Development table boundary changed');
const supplement=run('(()=>{'+development.slice(begin,end)+';return {recipes,studies,spells:SPELLS}})()');
const refunds=run(`[[25,12,5],[7,3,2],[18,6,0],[18,6,6]].map(([paid,work,progress])=>{
 const f={gold:0,crystal:0,town:{projects:[{uid:'q',gold:paid,crystal:0,progress,work}]}};
 Capital.edit(f,'q','cancel'); return {paid,work,progress,expected:f.gold};
})`);
const doc='docs/DESIGN_GLOBAL_MAP.md';
const designText=fs.readFileSync(path.join(upstream,doc),'utf8');
const origins={};
for(const name of [doc,'AGREED_RULES.md','CLAUDE_CHANGES.md']){
  const bytes=fs.readFileSync(path.join(upstream,name));
  origins[name]=crypto.createHash('sha1').update('blob '+bytes.length+'\0').update(bytes).digest('hex');
}
const sections=designText.split(/(?=^## )/m);
const decisions={};
for(const [key,title] of Object.entries({
  combat:'бой без кубиков, блок и уклонение',loot:'добыча, автоматическая отправка',
  villages:'деревни удалены из игры',movement:'запас ОД и автоматическое движение',
  routes:'предел ОД, размещение отрядов',vision:'радиус обзора, лесные и горные препятствия',
  placement:'свободное размещение зданий внутри столицы',work:'источники производства столицы',
  rescue:'эвакуация спасателей, чужие останки'
})){
  const match=sections.find(s=>s.split('\n')[0].includes(title));
  if(!match) throw Error('Missing design decision '+key);
  const [heading,...lines]=match.trim().split('\n');
  decisions[key]={source:doc,heading:heading.replace(/^## /,''),lines:lines.filter(Boolean)};
}
const data={source_commit:'b07f1941692c605ff76a061647874bc42b00bd75',hashes,document_hashes:origins,decisions,...result,
 retired_decrees:['relations'],
 ...supplement,refund_vectors:refunds,recipe_policy:{permanent_discovery:true,instant_forge:true},
 damage_vectors:damage,rng_vectors:rng};
const target=path.join(project,'data/catalog.json');
const json=JSON.stringify(data,null,2)+'\n';
if(verify){if(fs.readFileSync(target,'utf8')!==json)throw Error('catalog differs from executing prototype sources');}
else fs.writeFileSync(target,json);
console.log('Reference data verified',Object.fromEntries(['classes','subclasses','monsters','buildings','spells','decrees'].map(k=>[k,Object.keys(data[k]).length])));

