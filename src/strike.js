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
