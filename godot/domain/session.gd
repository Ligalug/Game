class_name KingdomSession
extends RefCounted

const FORMAT: int = 1
var initial_seed: int
var rng: KingdomRng
var members: Array[int] = []
var turn: int = 1

func _init(seed_value: int = 0) -> void:
	initial_seed = seed_value & KingdomRng.MASK
	rng = KingdomRng.new(initial_seed)

func encode() -> Dictionary:
	return {"format":FORMAT,"seed":initial_seed,"rng":rng.state,"turn":turn,"members":members.duplicate()}

static func is_uint(value: Variant, upper: int) -> bool:
	if typeof(value) not in [TYPE_INT, TYPE_FLOAT]: return false
	var n: float = float(value)
	return is_finite(n) and n == floor(n) and n >= 0 and n <= upper

static func decode(raw: Variant, candidates: int) -> KingdomSession:
	if not raw is Dictionary: return null
	for key: String in ["format","seed","rng","turn"]:
		if not is_uint(raw.get(key), KingdomRng.MASK): return null
	if int(raw.format) != FORMAT or int(raw.turn) < 1: return null
	if not raw.get("members") is Array or raw.members.size() != 2: return null
	var s: KingdomSession = KingdomSession.new(int(raw.seed))
	for value: Variant in raw.members:
		if not is_uint(value,candidates-1) or int(value) in s.members: return null
		s.members.append(int(value))
	s.turn = int(raw.turn)
	s.rng.state = int(raw.rng)
	return s

