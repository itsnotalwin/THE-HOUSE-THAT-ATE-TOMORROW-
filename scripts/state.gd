extends Node
## Persistent state for the Street + Entrance Hall slice.
## Puzzle transitions have explicit prerequisites; saves are validated before use.

signal changed
signal saved(success: bool)

const SCHEMA_VERSION: int = 1
const FLAG_NAMES: Array[String] = [
	"intro_letter_read", "fig_met", "almost_unlocked", "clue_guest_title",
	"guestbook_solved", "erasure_notice_read"
]
const DEFAULT_SETTINGS: Dictionary = {
	"master_volume": 1.0,
	"music_volume": 0.35,
	"sfx_volume": 0.7,
	"reduced_motion": false,
	"text_size": 22
}
const HINTS: Array[String] = [
	"The book expects a kind of guest, not a name.",
	"Look at the portrait in The Almost.",
	"Use the title THE VISITOR."
]

var flags: Dictionary = {
	"intro_letter_read": false, "fig_met": false, "almost_unlocked": false,
	"clue_guest_title": false, "guestbook_solved": false, "erasure_notice_read": false
}
var room: String = "street"
var player_position: Vector2 = Vector2(256, 280)
var mode_almost: bool = false
var hint_tier: int = 0
var settings: Dictionary = DEFAULT_SETTINGS.duplicate(true)
var save_path: String = "user://house_slice_save.json"
var settings_path: String = "user://house_slice_settings.cfg"
var last_error: String = ""
var recovered_backup: bool = false


func start_new() -> void:
	for key: String in FLAG_NAMES:
		flags[key] = false
	room = "street"
	player_position = Vector2(256, 280)
	mode_almost = false
	hint_tier = 0
	settings = _sanitize_settings(settings)
	last_error = ""
	recovered_backup = false
	changed.emit()


func get_flag(name: String) -> bool:
	return bool(flags.get(name, false))


func set_flag(name: String, value: bool = true) -> void:
	if not FLAG_NAMES.has(name) or get_flag(name) == value:
		return
	if value:
		if name == "almost_unlocked" and not get_flag("fig_met"):
			return
		if name == "clue_guest_title" and not get_flag("almost_unlocked"):
			return
		if name == "guestbook_solved" and not get_flag("clue_guest_title"):
			return
		if name == "erasure_notice_read" and not get_flag("guestbook_solved"):
			return
	flags[name] = value
	# Disabling a prerequisite cannot leave an impossible persistent progression.
	if not get_flag("fig_met"):
		flags["almost_unlocked"] = false
	if not get_flag("almost_unlocked"):
		flags["clue_guest_title"] = false
		mode_almost = false
	if not get_flag("clue_guest_title"):
		flags["guestbook_solved"] = false
	if not get_flag("guestbook_solved"):
		flags["erasure_notice_read"] = false
	changed.emit()


func enter_room(name: String, position: Vector2) -> void:
	if not _valid_room(name) or not _valid_position(position):
		return
	room = name
	player_position = position
	if room == "street":
		mode_almost = false
	changed.emit()


func toggle_mode() -> bool:
	if not get_flag("almost_unlocked") or room != "hall":
		return false
	mode_almost = not mode_almost
	changed.emit()
	return true


func learn_title() -> bool:
	if room != "hall" or not mode_almost or not get_flag("almost_unlocked"):
		return false
	set_flag("clue_guest_title")
	return true


func attempt_guestbook(choice: String) -> bool:
	if room != "hall" or choice != "visitor":
		return false
	if not get_flag("almost_unlocked") or not get_flag("clue_guest_title"):
		return false
	set_flag("guestbook_solved")
	return true


func next_hint() -> String:
	if get_flag("erasure_notice_read"):
		return "The house knows your name. Visit the newly opened door."
	if get_flag("guestbook_solved"):
		return "Read the red notice that arrived on the left sideboard."
	if not get_flag("almost_unlocked"):
		return "Speak to Fig. He has something that shows what nearly happened."
	hint_tier = mini(hint_tier + 1, HINTS.size())
	changed.emit()
	return HINTS[hint_tier - 1]


func objective() -> String:
	if not get_flag("intro_letter_read"):
		return "Read the letter waiting outside the house."
	if room == "street":
		return "Speak to Fig and enter the house."
	if not get_flag("almost_unlocked"):
		return "Ask Fig why the Guestbook refuses your name."
	if not get_flag("clue_guest_title"):
		return "Find a name the Guestbook will accept."
	if not get_flag("guestbook_solved"):
		return "Return to the Guestbook. Try the title the portrait revealed."
	if not get_flag("erasure_notice_read"):
		return "Read the new red notice."
	return "The house knows your name. Visit the newly opened door."


func set_settings(update: Dictionary) -> void:
	var merged: Dictionary = settings.duplicate(true)
	for key: Variant in update:
		if DEFAULT_SETTINGS.has(key):
			merged[key] = update[key]
	settings = _sanitize_settings(merged)
	changed.emit()


func save_preferences() -> bool:
	# Preferences also belong to players who have not started a story yet.
	# Keep them separate so a title-screen adjustment cannot enable Continue.
	var config := ConfigFile.new()
	config.set_value("preferences", "settings", _sanitize_settings(settings))
	var absolute: String = ProjectSettings.globalize_path(settings_path)
	if DirAccess.make_dir_recursive_absolute(absolute.get_base_dir()) != OK:
		last_error = "The settings folder could not be created."
		return false
	var temporary: String = absolute + ".tmp"
	if config.save(temporary) != OK:
		last_error = "Settings could not be saved."
		return false
	if DirAccess.rename_absolute(temporary, absolute) != OK:
		DirAccess.remove_absolute(temporary)
		last_error = "Settings could not be finalized."
		return false
	return true


func load_preferences() -> bool:
	var config := ConfigFile.new()
	if config.load(settings_path) != OK:
		return false
	var stored: Variant = config.get_value("preferences", "settings", null)
	if not stored is Dictionary:
		return false
	settings = _sanitize_settings(stored)
	changed.emit()
	return true


func _valid_room(name: String) -> bool:
	return name == "street" or name == "hall"


func _valid_position(position: Vector2) -> bool:
	return is_finite(position.x) and is_finite(position.y) \
		and position.x >= 8.0 and position.x <= 504.0 \
		and position.y >= 112.0 and position.y <= 344.0


func _is_number(value: Variant) -> bool:
	return typeof(value) == TYPE_INT or typeof(value) == TYPE_FLOAT


func _sanitize_settings(source: Dictionary) -> Dictionary:
	var clean: Dictionary = DEFAULT_SETTINGS.duplicate(true)
	for key: String in ["master_volume", "music_volume", "sfx_volume"]:
		var value: Variant = source.get(key, DEFAULT_SETTINGS[key])
		if _is_number(value) and is_finite(float(value)):
			clean[key] = clampf(float(value), 0.0, 1.0)
	var reduced: Variant = source.get("reduced_motion", false)
	if typeof(reduced) == TYPE_BOOL:
		clean["reduced_motion"] = reduced
	var text: Variant = source.get("text_size", 22)
	if _is_number(text) and is_finite(float(text)):
		clean["text_size"] = clampi(int(text), 18, 30)
	return clean


func _snapshot() -> Dictionary:
	return {
		"schema_version": SCHEMA_VERSION,
		"room": room,
		"player_position": [player_position.x, player_position.y],
		"mode_almost": mode_almost,
		"flags": flags.duplicate(true),
		"hint_tier": hint_tier,
		"settings": _sanitize_settings(settings)
	}


func _validated_payload(source: Variant) -> Dictionary:
	if typeof(source) != TYPE_DICTIONARY:
		return {}
	var data: Dictionary = source
	var schema: Variant = data.get("schema_version")
	if not _is_number(schema) or float(schema) != float(SCHEMA_VERSION):
		return {}
	if typeof(data.get("room")) != TYPE_STRING or not _valid_room(data["room"]):
		return {}
	var position: Variant = data.get("player_position")
	if typeof(position) != TYPE_ARRAY or position.size() != 2:
		return {}
	if not _is_number(position[0]) or not _is_number(position[1]):
		return {}
	var point: Vector2 = Vector2(float(position[0]), float(position[1]))
	if not _valid_position(point):
		return {}
	if typeof(data.get("mode_almost")) != TYPE_BOOL or typeof(data.get("flags")) != TYPE_DICTIONARY:
		return {}
	var loaded_flags: Dictionary = {}
	for key: String in FLAG_NAMES:
		if typeof(data["flags"].get(key)) != TYPE_BOOL:
			return {}
		loaded_flags[key] = data["flags"][key]
	if loaded_flags["almost_unlocked"] and not loaded_flags["fig_met"]:
		return {}
	if loaded_flags["clue_guest_title"] and not loaded_flags["almost_unlocked"]:
		return {}
	if loaded_flags["guestbook_solved"] and not loaded_flags["clue_guest_title"]:
		return {}
	if loaded_flags["erasure_notice_read"] and not loaded_flags["guestbook_solved"]:
		return {}
	if data["mode_almost"] and (not loaded_flags["almost_unlocked"] or data["room"] != "hall"):
		return {}
	var tier: Variant = data.get("hint_tier", 0)
	if not _is_number(tier) or not is_finite(float(tier)) or float(tier) != floor(float(tier)) or float(tier) < 0 or float(tier) > 3:
		return {}
	var loaded_settings: Variant = data.get("settings", {})
	if typeof(loaded_settings) != TYPE_DICTIONARY:
		return {}
	return {
		"schema_version": SCHEMA_VERSION, "room": data["room"],
		"player_position": [point.x, point.y], "mode_almost": data["mode_almost"],
		"flags": loaded_flags, "hint_tier": int(tier),
		"settings": _sanitize_settings(loaded_settings)
	}


func _read_payload(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	# Reject accidental giant/corrupted files before parsing.
	if file.get_length() > 65536:
		file.close()
		return {}
	var text: String = file.get_as_text()
	file.close()
	var parser: JSON = JSON.new()
	if parser.parse(text) != OK:
		return {}
	return _validated_payload(parser.data)


func has_save() -> bool:
	return not _read_payload(save_path).is_empty() or not _read_payload(save_path + ".bak").is_empty()


func save_game() -> bool:
	last_error = ""
	var payload: Dictionary = _validated_payload(_snapshot())
	if payload.is_empty():
		return _save_failed("Progress could not be saved because its state is invalid.")
	var absolute: String = ProjectSettings.globalize_path(save_path)
	var temporary: String = absolute + ".tmp"
	var backup: String = absolute + ".bak"
	if DirAccess.make_dir_recursive_absolute(absolute.get_base_dir()) != OK:
		return _save_failed("The save folder could not be created.")
	var file: FileAccess = FileAccess.open(temporary, FileAccess.WRITE)
	if file == null:
		return _save_failed("The save file could not be opened. Your previous save is unchanged.")
	file.store_string(JSON.stringify(payload, "\t"))
	file.flush()
	var write_error: Error = file.get_error()
	file.close()
	if write_error != OK or _read_payload(temporary).is_empty():
		DirAccess.remove_absolute(temporary)
		return _save_failed("The new save could not be verified. Your previous save is unchanged.")
	# Back up only validated progress. Never replace a good backup with corrupt data.
	if not _read_payload(absolute).is_empty():
		var backup_temp: String = backup + ".tmp"
		if DirAccess.copy_absolute(absolute, backup_temp) != OK:
			DirAccess.remove_absolute(temporary)
			return _save_failed("The previous save could not be backed up. It is unchanged.")
		if DirAccess.rename_absolute(backup_temp, backup) != OK:
			DirAccess.remove_absolute(temporary)
			DirAccess.remove_absolute(backup_temp)
			return _save_failed("The backup could not be finalized. Your previous save is unchanged.")
	# Rename inside one directory replaces the primary only after verification.
	if DirAccess.rename_absolute(temporary, absolute) != OK:
		DirAccess.remove_absolute(temporary)
		return _save_failed("The save could not be finalized. Your previous save is unchanged.")
	recovered_backup = false
	saved.emit(true)
	return true


func _save_failed(message: String) -> bool:
	last_error = message
	saved.emit(false)
	return false


func load_game() -> bool:
	last_error = ""
	recovered_backup = false
	var payload: Dictionary = _read_payload(save_path)
	if payload.is_empty():
		payload = _read_payload(save_path + ".bak")
		recovered_backup = not payload.is_empty()
	if payload.is_empty():
		last_error = "No readable save was found. Your current progress has not changed."
		return false
	# Commit the loaded snapshot only after every field has passed validation.
	room = payload["room"]
	player_position = Vector2(payload["player_position"][0], payload["player_position"][1])
	mode_almost = payload["mode_almost"]
	flags = payload["flags"].duplicate(true)
	hint_tier = payload["hint_tier"]
	settings = payload["settings"].duplicate(true)
	if recovered_backup:
		last_error = "Recovered the previous autosave. The newest save was unreadable."
	changed.emit()
	return true
