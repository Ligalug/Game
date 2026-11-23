extends Control

const PAGES: Dictionary={"menu":preload("res://ui/menu.tscn"),"settings":preload("res://ui/settings.tscn"),"new":preload("res://ui/new_game.tscn"),"session":preload("res://ui/session_page.tscn"),"codex":preload("res://ui/codex.tscn")}
const CATALOG: JSON=preload("res://data/catalog.json")
const SOUND: AudioStreamWAV=preload("res://assets/ui_select.wav")
var catalog: Dictionary=CATALOG.data
var prefs: Preferences
var save_store: SaveStore
var session: KingdomSession
var page: KingdomPage
var location: String=""
var changing: bool=false
var curtain: ColorRect=ColorRect.new()
var music: AudioStreamPlayer=AudioStreamPlayer.new()
var click: AudioStreamPlayer=AudioStreamPlayer.new()
var sample: AudioStreamPlayer=AudioStreamPlayer.new()

func _ready() -> void:
	var prefix: String="user://"
	for arg: String in OS.get_cmdline_user_args():
		if arg=="--evidence":
			prefix="user://evidence/%d-%d/" % [OS.get_process_id(),Time.get_ticks_usec()]
			DirAccess.make_dir_recursive_absolute(prefix)
	save_store=SaveStore.new(prefix+"campaign.json")
	prefs=Preferences.new(prefix+"preferences.json")
	prefs.apply_audio()
	prefs.apply_window()
	var backdrop: TextureRect=TextureRect.new()
	backdrop.texture=preload("res://assets/keep_at_dusk.png")
	backdrop.mouse_filter=Control.MOUSE_FILTER_IGNORE
	backdrop.expand_mode=TextureRect.EXPAND_IGNORE_SIZE
	add_child(backdrop)
	backdrop.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var theme_loop: AudioStreamWAV=preload("res://assets/menu_lute.wav").duplicate() as AudioStreamWAV
	theme_loop.loop_mode=AudioStreamWAV.LOOP_FORWARD
	theme_loop.loop_end=theme_loop.data.size()/2
	music.stream=theme_loop
	music.bus=&"Music"
	music.volume_db=-32
	add_child(music)
	music.play()
	create_tween().tween_property(music,"volume_db",0.0,1.0)
	click.stream=SOUND
	click.bus=&"UI"
	add_child(click)
	sample.stream=SOUND
	add_child(sample)
	curtain.color=Color("#111b17")
	curtain.mouse_filter=Control.MOUSE_FILTER_IGNORE
	curtain.modulate.a=0
	add_child(curtain)
	curtain.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	open_page("menu")

func click_sound() -> void:
	click.play()

func audition(bus: String) -> void:
	sample.bus=bus
	sample.play()

func open_page(id: String) -> void:
	if is_instance_valid(page):
		remove_child(page)
		page.queue_free()
	location=id
	var scene: PackedScene=PAGES[id]
	page=scene.instantiate() as KingdomPage
	add_child(page)
	page.mount(self)
	move_child(curtain,-1)
	var first: Control=page.find_next_valid_focus()
	if first: first.grab_focus()

func refresh_page() -> void:
	open_page.call_deferred(location)

func go(id: String) -> void:
	if changing or id==location: return
	changing=true
	curtain.mouse_filter=Control.MOUSE_FILTER_STOP
	var fade: Tween=create_tween()
	fade.tween_property(curtain,"modulate:a",1.0,0.15/prefs.speed)
	fade.tween_callback(open_page.bind(id))
	fade.tween_property(curtain,"modulate:a",0.0,0.21/prefs.speed)
	await fade.finished
	changing=false
	curtain.mouse_filter=Control.MOUSE_FILTER_IGNORE

func start_session(seed_value: int,members: Array[int]) -> void:
	if members.size()!=2 or changing: return
	if save_store.exists():
		var confirm: ConfirmationDialog=ConfirmationDialog.new()
		confirm.dialog_text="Заменить сохранённую партию новым отрядом?"
		confirm.ok_button_text="Заменить"
		confirm.cancel_button_text="Отмена"
		add_child(confirm)
		confirm.confirmed.connect(_create.bind(seed_value,members.duplicate()))
		confirm.visibility_changed.connect(func() -> void:
			if not confirm.visible: confirm.queue_free())
		confirm.popup_centered()
	else: _create(seed_value,members)

func _create(seed_value: int,members: Array[int]) -> void:
	var draft: KingdomSession=KingdomSession.new(seed_value)
	draft.members.assign(members)
	if save_store.write_record(draft.encode())!=OK:
		alert("Не удалось создать сохранение.")
		return
	session=draft
	go("session")

func resume_session() -> void:
	var loaded: KingdomSession=save_store.load_session(catalog.starters.size())
	if loaded==null:
		alert("Сохранение повреждено или его версия не поддерживается.")
		return
	session=loaded
	go("session")

func save_session(notify_user: bool) -> void:
	var status: Error=save_store.write_record(session.encode())
	if status!=OK: alert("Не удалось записать сохранение.")
	elif notify_user: alert("Партия сохранена.")

func alert(message: String) -> void:
	var dialog: AcceptDialog=AcceptDialog.new()
	dialog.title="Туман и кости"
	dialog.dialog_text=message
	add_child(dialog)
	dialog.visibility_changed.connect(func() -> void:
		if not dialog.visible: dialog.queue_free())
	dialog.popup_centered()

func _unhandled_key_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel") and location!="menu" and not changing:
		go("menu")

