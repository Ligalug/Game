class_name Preferences
extends RefCounted

const BUSES: Array[String] = ["Master","Music","SFX","UI","Ambience"]
const SPEEDS: Array[float] = [0.5,1.0,1.5,2.0]
var gains: Dictionary = {"Master":80,"Music":55,"SFX":80,"UI":65,"Ambience":60}
var speed: float = 1.0
var fullscreen: bool = false
var store: SaveStore

func _init(path: String = "user://preferences.json") -> void:
	store = SaveStore.new(path)
	var value: Variant = store.read_record()
	if value is Dictionary and value.get("format") == 1:
		var saved: Variant = value.get("gains")
		if saved is Dictionary:
			for bus: String in BUSES:
				if KingdomSession.is_uint(saved.get(bus),100): gains[bus] = int(saved[bus])
		if value.get("speed") in SPEEDS: speed = float(value.speed)
		if value.get("fullscreen") is bool: fullscreen = value.fullscreen

func apply_audio() -> void:
	for bus: String in BUSES:
		var index: int = AudioServer.get_bus_index(bus)
		var fraction: float = float(gains[bus])/100.0
		if index >= 0:
			AudioServer.set_bus_mute(index, fraction == 0)
			AudioServer.set_bus_volume_db(index, linear_to_db(maxf(0.001,fraction)))

func apply_window() -> void:
	if DisplayServer.get_name() != "headless":
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_FULLSCREEN if fullscreen else DisplayServer.WINDOW_MODE_WINDOWED)

func persist() -> Error:
	return store.write_record({"format":1,"gains":gains,"speed":speed,"fullscreen":fullscreen})

