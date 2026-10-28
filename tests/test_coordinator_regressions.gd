extends SceneTree
## Regressions around title-screen settings, Continue, and confirmation escape.

var assertions: int = 0
var failures: int = 0
var state: Node
var game: Control


func _initialize() -> void:
	call_deferred("_run")


func expect(condition: bool, message: String) -> void:
	assertions += 1
	if not condition:
		failures += 1
		push_error(message)


func _run() -> void:
	state = root.get_node("GameState")
	var old_save: String = state.save_path
	var old_settings: String = state.settings_path
	var fixture: String = "user://coordinator-test-%s" % str(Time.get_ticks_usec())
	state.save_path = fixture + ".json"
	state.settings_path = fixture + ".cfg"
	state.start_new()
	game = load("res://scenes/main.tscn").instantiate()
	root.add_child(game)
	await process_frame
	expect(not state.has_save() and not game.playing, "Fresh title must not create a story")
	game._setting_changed("music_volume", 0.1)
	game._setting_changed("text_size", 26)
	expect(FileAccess.file_exists(state.settings_path), "Title preferences must persist before New Game")
	expect(not state.has_save() and not game.ui._has_save, "Changing title settings must not enable Continue")
	game.queue_free()
	await process_frame
	state.settings = state.DEFAULT_SETTINGS.duplicate(true)
	game = load("res://scenes/main.tscn").instantiate()
	root.add_child(game)
	await process_frame
	expect(is_equal_approx(state.settings["music_volume"], 0.1) and state.settings["text_size"] == 26, "A fresh coordinator must restore preferences without a story save")
	expect(not state.has_save(), "Restoring preferences must not create story progress")
	game._start_new()
	expect(state.has_save(), "Starting a story should create its first save")
	state.set_flag("intro_letter_read")
	state.set_flag("fig_met")
	game._enter_room("hall", Vector2(256, 300))
	state.set_flag("almost_unlocked")
	state.toggle_mode()
	game._save(false)
	game._show_title()
	game._setting_changed("sfx_volume", 0.25)
	game._action("continue")
	expect(game.playing and state.room == "hall" and state.mode_almost, "Continue must restore the saved room and mode")
	expect(game.sound._context == "hall:true:false", "Continue must switch audio from title to the restored room and mode")
	expect(state.get_flag("almost_unlocked") and is_equal_approx(state.settings["sfx_volume"], 0.25), "Title preference changes must preserve existing progression")
	game._show_title()
	game.ui._request_new_game()
	expect(game.ui.panel_name() == "confirm_new", "New Game must confirm before replacing a save")
	var escape := InputEventKey.new()
	escape.physical_keycode = KEY_ESCAPE
	escape.pressed = true
	game._unhandled_input(escape)
	expect(game.ui.panel_name() == "title" and state.get_flag("almost_unlocked"), "Escape must dismiss New Game confirmation without replacing progress")
	var preferences: Dictionary = state.settings.duplicate(true)
	var invalid := FileAccess.open(state.settings_path, FileAccess.WRITE)
	invalid.store_string("[preferences]\nsettings=12\n")
	invalid.close()
	expect(not state.load_preferences() and state.settings == preferences, "Malformed preferences must preserve active settings")
	game.queue_free()
	await process_frame
	# Give the audio server time to release playback instances before exit.
	await create_timer(0.1).timeout
	for suffix: String in [".json", ".json.bak", ".json.tmp", ".json.bak.tmp", ".cfg", ".cfg.tmp"]:
		DirAccess.remove_absolute(ProjectSettings.globalize_path(fixture + suffix))
	state.save_path = old_save
	state.settings_path = old_settings
	print("Coordinator regressions: %d assertions, %d failures" % [assertions, failures])
	quit(1 if failures else 0)
