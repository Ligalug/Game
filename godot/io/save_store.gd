class_name SaveStore
extends RefCounted

var path: String
# Предварительно, S01. Меню использует один слот партии, настройки хранятся отдельно.

func _init(filename: String = "user://campaign.json") -> void:
	path = filename

func read_record() -> Variant:
	if not FileAccess.file_exists(path):
		if FileAccess.file_exists(path + ".bak"): return _read(path + ".bak")
		return null
	return _read(path)

func _read(filename: String) -> Variant:
	var file: FileAccess = FileAccess.open(filename, FileAccess.READ)
	if file == null: return null
	var parser: JSON = JSON.new()
	return parser.data if parser.parse(file.get_as_text()) == OK else null

func exists() -> bool:
	return FileAccess.file_exists(path) or FileAccess.file_exists(path + ".bak")

func load_session(count: int) -> KingdomSession:
	var raw: Variant = read_record()
	var session: KingdomSession = KingdomSession.decode(raw,count)
	if session != null: return session
	if raw is Dictionary and KingdomSession.is_uint(raw.get("format"),KingdomRng.MASK) and int(raw.format) > KingdomSession.FORMAT:
		return null
	if FileAccess.file_exists(path + ".bak"):
		return KingdomSession.decode(_read(path + ".bak"),count)
	return null

func write_record(data: Dictionary) -> Error:
	var temp: String = path + ".tmp"
	var backup: String = path + ".bak"
	var file: FileAccess = FileAccess.open(temp, FileAccess.WRITE)
	if file == null: return FileAccess.get_open_error()
	file.store_string(JSON.stringify(data))
	file.flush()
	var err: Error = file.get_error()
	file.close()
	if err != OK: return err
	if _read(temp) == null: return ERR_FILE_CORRUPT
	if FileAccess.file_exists(path):
		if FileAccess.file_exists(backup):
			err = DirAccess.remove_absolute(backup)
			if err != OK: return err
		err = DirAccess.rename_absolute(path,backup)
		if err != OK: return err
	err = DirAccess.rename_absolute(temp,path)
	if err != OK and FileAccess.file_exists(backup):
		DirAccess.rename_absolute(backup,path)
	return err

