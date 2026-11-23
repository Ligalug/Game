extends SceneTree

var shell: Control
var failure: String = ""
var started: int
var rendered_frames: int = 0

func _initialize() -> void:
	if "--evidence" not in OS.get_cmdline_user_args():
		printerr("Use the isolated --evidence profile.")
		quit(2)
		return
	run.call_deferred()

func check(condition: bool, message: String) -> void:
	if not condition and failure.is_empty():
		failure = message
		push_error(message)

func press(id: String) -> void:
	var control: Button = shell.page.get_node(id) as Button
	check(not control.disabled, "Disabled control " + id)
	control.pressed.emit()

func settle(page_name: String) -> void:
	var limit: int = Time.get_ticks_msec() + 3000
	while (shell.changing or shell.location != page_name) and Time.get_ticks_msec() < limit:
		await process_frame
	check(shell.location == page_name and not shell.changing, "Navigation to " + page_name)

func run() -> void:
	change_scene_to_file("res://ui/shell.tscn")
	await scene_changed
	shell = current_scene
	var initial: Button = shell.page.get_node("Resume")
	check(initial.disabled, "Fresh profile should have an empty slot")
	press("Options")
	await settle("settings")
	var fullscreen: CheckButton = shell.page.get_node("Fullscreen")
	if DisplayServer.get_name() != "headless":
		fullscreen.button_pressed = true
		await process_frame
		check(DisplayServer.window_get_mode() == DisplayServer.WINDOW_MODE_FULLSCREEN, "Fullscreen did not apply")
		fullscreen.button_pressed = false
		await process_frame
		check(DisplayServer.window_get_mode() == DisplayServer.WINDOW_MODE_WINDOWED, "Window mode did not return")
	var slider: HSlider = shell.page.get_node("UI")
	slider.value = 0
	check(AudioServer.is_bus_mute(AudioServer.get_bus_index("UI")), "Silent UI bus")
	slider.value = 65
	press("Speed3")
	await process_frame
	check(Preferences.new(shell.prefs.store.path).speed == 2.0, "Speed was not written")
	press("Back")
	await settle("menu")
	for i in 10:
		press("NewCampaign")
		await settle("new")
		press("Candidate%d" % i)
		press("Candidate%d" % ((i + 1) % 10))
		var seed_field: LineEdit = shell.page.get_node("Seed")
		seed_field.text = str(900 + i)
		press("Start")
		if i > 0:
			var dialog: ConfirmationDialog = shell.get_child(-1) as ConfirmationDialog
			check(dialog != null, "Overwrite confirmation missing")
			if dialog:
				dialog.confirmed.emit()
				dialog.hide()
		await settle("session")
		check(shell.session.initial_seed == 900 + i, "New seed mismatch")
		press("Back")
		await settle("menu")
		press("Resume")
		await settle("session")
		check(shell.session.members[0] == i and shell.session.initial_seed == 900 + i, "Resume mismatch")
		press("Back")
		await settle("menu")
	press("Library")
	await settle("codex")
	for i in 7:
		press("Tab%d" % i)
		check(shell.page.items.item_count > 0 and not shell.page.detail.text.is_empty(), "Empty catalogue section")
	press("Back")
	await settle("menu")
	if DisplayServer.get_name() != "headless":
		started = Time.get_ticks_usec()
		for i in 180:
			await process_frame
			rendered_frames += 1
		var average: float = rendered_frames * 1000000.0 / (Time.get_ticks_usec() - started)
		print("MENU_FPS_AVERAGE=%.2f" % average)
	print("UI_START_SAVE_RESUME=10" if failure.is_empty() else failure)
	quit(0 if failure.is_empty() else 1)

