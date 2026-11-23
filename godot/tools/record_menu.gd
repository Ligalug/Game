extends SceneTree

var shell: Control
var directory: String
var frame: int=0

func _initialize() -> void:
	directory=OS.get_environment("FOG_EVIDENCE_DIR")
	if directory=="" or "--evidence" not in OS.get_cmdline_user_args():
		printerr("Set FOG_EVIDENCE_DIR and pass -- --evidence.")
		quit(2)
		return
	change_scene_to_file("res://ui/shell.tscn")

func press(name: String) -> void:
	var b: Button=shell.page.get_node(name)
	b.grab_focus()
	b.pressed.emit()

func capture(path: String) -> void:
	await RenderingServer.frame_post_draw
	var im: Image=root.get_texture().get_image()
	im.save_png(directory.path_join(path+".png"))

func _process(_delta: float) -> bool:
	if not current_scene: return false
	shell=current_scene
	frame+=1
	match frame:
		48: capture("01-menu")
		168: press("Options")
		216: capture("02-settings")
		264: shell.page.get_node("Music").value=32
		312: press("ListenMusic")
		360: shell.page.get_node("SFX").value=55
		384: press("ListenSFX")
		432: press("Speed3")
		504: press("Speed0")
		576: press("Speed1")
		600: shell.page.get_node("Music").value=55
		612: shell.page.get_node("SFX").value=80
		648: press("Back")
		708: press("NewCampaign")
		780: press("Candidate0")
		828: press("Candidate2")
		864: shell.page.get_node("Seed").text="24680"
		888: capture("03-first-party")
		936: press("Start")
		1008: capture("04-session")
		1080: press("Back")
		1140: press("Resume")
		1200: press("Back")
		1260: press("Library")
		1308: press("Tab2")
		1344: capture("05-codex")
		1380: press("Tab6")
		1452: press("Back")
		1584:
			print("EVIDENCE_SECONDS=66")
			quit()
	return false
