class_name ReferenceRules
extends RefCounted

static func damage(parts: Array, target: Dictionary, critical: bool, blocked: bool, multiplier: float) -> int:
	var total: float = 0.0
	for part: Dictionary in parts:
		var school: String = part["type"]
		var rating: float = target.get("physicalArmor", 0) if school == "physical" else target.get("resists", {}).get(school, 0)
		var effective: float = clampf(rating, 0, 90) * (1.0 - clampf(part.get("penetration", 0), 0, 100) / 100.0)
		total += float(part["value"]) * (multiplier if critical else 1.0) * (1.0 - effective / 100.0)
	return maxi(1, floori(total * (0.5 if blocked else 1.0) + 0.5))

static func construction_refund(paid: int, work: int, progress: int) -> int:
	if work <= 0: return 0
	return clampi(ceili(float(paid) * (work - progress) / work - 1e-9), 0, paid)

