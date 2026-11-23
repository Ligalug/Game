class_name KingdomRng
extends RefCounted

const MASK: int = 0xffffffff
var state: int

func _init(initial_seed: int = 0) -> void:
	state = initial_seed & MASK

func next_u32() -> int:
	# Matches the unsigned LCG in src/game.js newGame.
	state = (state * 1664525 + 1013904223) & MASK
	return state

func fraction() -> float:
	return float(next_u32()) / 4294967296.0

