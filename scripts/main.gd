extends Control
## Coordinates the approved first chapter. The UI, world and persistence remain separate.

const WorldScript = preload("res://scripts/world.gd")
const UIScript = preload("res://scripts/ui.gd")
const AudioScript = preload("res://scripts/audio.gd")

var world: Node2D
var ui: Control
var sound: Node
var world_view: SubViewport
var world_image: TextureRect
var playing: bool = false
var _dialogues: Dictionary = {}
var _lines: Array = []
var _line_index: int = 0
var _after_dialogue: Callable
var _choice_handler: Callable
var _settings_origin: String = "title"
var _hint: String = ""
var _autosave_elapsed: float = 0.0
var _last_target: String = ""


func _ready() -> void:
	_register_controls()
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string("res://data/dialogue.json"))
	if parsed is Dictionary:
		_dialogues = parsed
	world_view = SubViewport.new()
	world_view.name = "PixelWorld"
	world_view.size = Vector2i(384, 216)
	world_view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	world_view.handle_input_locally = false
	world_view.canvas_item_default_texture_filter = Viewport.DEFAULT_CANVAS_ITEM_TEXTURE_FILTER_NEAREST
	add_child(world_view)
	world = WorldScript.new()
	world_view.add_child(world)
	world_image = TextureRect.new()
	world_image.name = "WorldPresentation"
	world_image.texture = world_view.get_texture()
	world_image.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	world_image.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	world_image.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	world_image.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(world_image)
	world_image.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	sound = AudioScript.new()
	add_child(sound)
	ui = UIScript.new()
	ui.name = "Interface"
	add_child(ui)
	ui.action_requested.connect(_action)
	ui.dialogue_advanced.connect(_advance_dialogue)
	ui.choice_selected.connect(_choose)
	ui.setting_changed.connect(_setting_changed)
	GameState.changed.connect(_sync)
	# Read valid settings/progress without entering the world until Continue is chosen.
	if GameState.has_save():
		GameState.load_game()
	GameState.load_preferences()
	_apply_settings()
	_show_title()
	get_tree().auto_accept_quit = false
	if OS.get_cmdline_user_args().has("--qa-smoke"):
		_start_new()


func _register_controls() -> void:
	var bindings: Dictionary = {
		"move_left": [KEY_A, KEY_LEFT], "move_right": [KEY_D, KEY_RIGHT],
		"move_up": [KEY_W, KEY_UP], "move_down": [KEY_S, KEY_DOWN],
		"interact": [KEY_E, KEY_ENTER], "almost": [KEY_SPACE, KEY_TAB],
		"notebook": [KEY_N, KEY_I], "pause": [KEY_ESCAPE]
	}
	for action_name: String in bindings:
		if not InputMap.has_action(action_name):
			InputMap.add_action(action_name)
		for code: int in bindings[action_name]:
			var event := InputEventKey.new()
			event.physical_keycode = code
			InputMap.action_add_event(action_name, event)


func _process(delta: float) -> void:
	if not playing or not is_instance_valid(world):
		return
	world.set_enabled(not ui.is_modal())
	_update_hud()
	if ui.is_modal():
		return
	GameState.player_position = world.get_player_position()
	_autosave_elapsed += delta
	if _autosave_elapsed >= 15.0:
		_autosave_elapsed = 0.0
		_save(false)


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.echo:
		return
	if event.is_action_pressed("pause"):
		get_viewport().set_input_as_handled()
		if ui.panel_name() == "dialogue":
			# Finish required conversation callbacks rather than silently discarding rewards.
			ui.toast("Finish this conversation with E / Enter.")
		elif ui.panel_name() in ["settings", "credits"]:
			_action("back")
		elif ui.panel_name() == "confirm_new":
			_show_title()
		elif playing and ui.is_modal():
			_resume()
		elif playing:
			world.set_enabled(false)
			ui.show_pause()
		return
	if not playing or ui.is_modal():
		return
	if event.is_action_pressed("interact"):
		get_viewport().set_input_as_handled()
		interact_target(world.get_target_id())
	elif event.is_action_pressed("almost"):
		get_viewport().set_input_as_handled()
		if GameState.toggle_mode():
			sound.play_cue("toggle")
			_save(false)
		else:
			ui.toast("The mirror works inside the house." if GameState.get_flag("almost_unlocked") else "Speak to Fig about the Guestbook first.")
	elif event.is_action_pressed("notebook"):
		get_viewport().set_input_as_handled()
		_open_notebook()


func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT and playing and is_instance_valid(ui):
		_save(false)
		world.set_enabled(false)
		if not ui.is_modal():
			ui.show_pause()
	elif what == NOTIFICATION_WM_CLOSE_REQUEST:
		if playing:
			_save(false)
		get_tree().quit()


func _action(action: String) -> void:
	sound.play_cue("focus")
	match action:
		"new_game": _start_new()
		"continue":
			if GameState.load_game():
				GameState.load_preferences()
				playing = true
				world_image.show()
				world.load_room(GameState.room, GameState.player_position, GameState.mode_almost, GameState.get_flag("guestbook_solved"))
				_apply_settings()
				_sync()
				_resume()
				ui.toast("Recovered your previous save." if GameState.recovered_backup else "Welcome back, Visitor.")
			else:
				ui.toast(GameState.last_error)
		"resume": _resume()
		"notebook": _open_notebook()
		"hint":
			_hint = GameState.next_hint()
			_save(false)
			_open_notebook()
		"settings":
			_settings_origin = "pause" if playing else "title"
			ui.show_settings(GameState.settings)
			world.set_enabled(false)
		"credits":
			_settings_origin = "title"
			ui.show_credits()
		"back":
			if _settings_origin == "pause" and playing:
				ui.show_pause()
			else:
				_show_title()
		"title":
			if playing and not _save(false):
				ui.toast("Couldn't save. Please try again before returning to title.")
				return
			_show_title()
		"quit":
			if playing:
				_save(false)
			get_tree().quit()


func _start_new() -> void:
	GameState.start_new()
	_hint = ""
	playing = true
	world_image.show()
	_enter_room("street", Vector2(256, 290))
	ui.toast("Move with WASD / arrows. E to inspect. N for your notebook.")


func _show_title() -> void:
	playing = false
	world.set_enabled(false)
	world_image.hide()
	_lines.clear()
	_choice_handler = Callable()
	_after_dialogue = Callable()
	ui.show_title(GameState.has_save())
	sound.set_context("street", false, true)


func _resume() -> void:
	ui.hide_panels()
	world.set_enabled(playing)
	_update_hud()


func _enter_room(room: String, point: Vector2) -> void:
	GameState.enter_room(room, point)
	world.load_room(room, point, GameState.mode_almost, GameState.get_flag("guestbook_solved"))
	_resume()
	_sync()
	_save(false)


func _sync() -> void:
	if not is_instance_valid(world) or not is_instance_valid(ui):
		return
	world.set_mode(GameState.mode_almost)
	world.set_solved(GameState.get_flag("guestbook_solved"))
	sound.set_context(GameState.room, GameState.mode_almost, not playing)
	_update_hud()


func _update_hud() -> void:
	if not playing:
		return
	var prompt: String = world.get_target_label()
	if not prompt.is_empty():
		prompt = "E  ·  " + prompt
	var mode_label: String = "The Almost" if GameState.mode_almost else "The Here"
	var location: String = "Forgotten Street" if GameState.room == "street" else "Entrance Hall"
	ui.set_hud(GameState.objective(), mode_label, prompt, location)


func _save(show_notice: bool = true) -> bool:
	if playing:
		GameState.player_position = world.get_player_position()
	var ok: bool = GameState.save_game()
	if not ok:
		ui.toast("Couldn't save: " + GameState.last_error)
	elif show_notice:
		ui.toast("Progress saved.")
	return ok


func _setting_changed(key: String, value: Variant) -> void:
	GameState.set_settings({key: value})
	_apply_settings()
	if not GameState.save_preferences():
		ui.toast(GameState.last_error)
	# Retain settings in existing story snapshots, but never create a story
	# merely because someone adjusted the title-screen volume.
	if playing or GameState.has_save():
		_save(false)


func _apply_settings() -> void:
	ui.apply_settings(GameState.settings)
	sound.apply_settings(GameState.settings)
	world.set("reduced_motion", bool(GameState.settings.get("reduced_motion", false)))


func _open_notebook() -> void:
	if not playing:
		return
	var clues: Array = []
	var items: Array = []
	if GameState.get_flag("intro_letter_read"):
		clues.append("Tomorrow has gone missing. The Department sent me to this house.")
		items.append({"name":"Department letter", "icon":"icon_letter.png"})
	if GameState.get_flag("almost_unlocked"):
		clues.append("The mirror reveals The Almost: things that might have happened. Press Space to look.")
		items.append({"name":"Pocket mirror", "icon":"icon_mirror.png"})
	if GameState.get_flag("clue_guest_title"):
		clues.append("The portrait's nameplate reads THE VISITOR in The Almost. Try that title in the Guestbook.")
	if GameState.get_flag("guestbook_solved"):
		clues.append("The Guestbook accepted THE VISITOR. The house recognizes me; the doors have unlocked.")
	if GameState.get_flag("erasure_notice_read"):
		clues.append("A red notice orders the house closed NEXT TOMORROW. The clocks have stopped at 11:59.")
	world.set_enabled(false)
	ui.show_notebook(clues, items, GameState.objective(), _hint)


func _say(key: String, done: Callable = Callable()) -> void:
	var entries: Array = _dialogues.get(key, [])
	_say_lines(entries, done)


func _say_lines(entries: Array, done: Callable = Callable()) -> void:
	_lines = entries.duplicate(true)
	_line_index = 0
	_after_dialogue = done
	_choice_handler = Callable()
	world.set_enabled(false)
	_show_line()


func _show_line() -> void:
	if _line_index >= _lines.size():
		_finish_dialogue()
		return
	var line: Dictionary = _lines[_line_index]
	ui.show_dialogue(str(line.get("speaker", "Visitor")), str(line.get("text", "")), [], int(line.get("portrait", 0)))


func _advance_dialogue() -> void:
	if _choice_handler.is_valid() or _lines.is_empty():
		return
	_line_index += 1
	_show_line()


func _finish_dialogue() -> void:
	_lines.clear()
	var callback: Callable = _after_dialogue
	_after_dialogue = Callable()
	ui.close_dialogue()
	if callback.is_valid():
		callback.call()
	if not ui.is_modal():
		_resume()


func _choices(speaker: String, text: String, options: Array, callback: Callable) -> void:
	_lines.clear()
	_after_dialogue = Callable()
	_choice_handler = callback
	world.set_enabled(false)
	ui.show_dialogue(speaker, text, options)


func _choose(id: String) -> void:
	if not _choice_handler.is_valid():
		return
	var callback: Callable = _choice_handler
	_choice_handler = Callable()
	ui.close_dialogue()
	callback.call(id)
	if not ui.is_modal():
		_resume()


func interact_target(id: String) -> void:
	if id.is_empty() or not playing or ui.is_modal():
		return
	sound.play_cue("inspect")
	match id:
		"letter":
			_say("letter", func() -> void:
				GameState.set_flag("intro_letter_read")
				_save()
			)
		"fig": _talk_fig()
		"house_door":
			if not GameState.get_flag("intro_letter_read"):
				_say_lines([{"speaker":"Fig", "text":"Your letter, please. The one sticking out of the mailbox. We must begin with the paperwork."}])
			elif not GameState.get_flag("fig_met"):
				_say_lines([{"speaker":"Visitor", "text":"The cat beside the door is looking at me as if I require a permit. I should speak to him first."}])
			else:
				_enter_room("hall", Vector2(256, 300))
				ui.toast("The Guestbook waits beside the runner. Fig has followed you inside.")
		"street_exit":
			if not GameState.get_flag("guestbook_solved"):
				_say_lines([{"speaker":"Fig", "text":"The house cannot let an unregistered guest leave. Please settle matters with the Guestbook. I can offer a hint."}])
			else:
				_enter_room("street", Vector2(256, 212))
		"guestbook": _guestbook()
		"portrait":
			if GameState.mode_almost:
				_say("portrait_almost", func() -> void:
					GameState.learn_title()
					_save()
					ui.toast("Clue added: THE VISITOR. Open N to read your notebook.")
				)
			else:
				_say("portrait_here")
		"notice":
			if GameState.get_flag("guestbook_solved"):
				_say("notice", func() -> void:
					GameState.set_flag("erasure_notice_read")
					_save()
					sound.play_cue("notice")
				)
		"kitchen_door", "library_door":
			if not GameState.get_flag("guestbook_solved"):
				_say_lines([{"speaker":"Fig", "text":"Residents only. The Guestbook is quite firm about that. Try registering before attempting architecture."}])
			elif not GameState.get_flag("erasure_notice_read"):
				_say_lines([{"speaker":"Visitor", "text":"The door is unlocked. But that new red notice deserves a look before I go further."}])
			else:
				world.set_enabled(false)
				ui.show_completion()
		"clock", "books", "tea", "flowers", "street_sign", "window": _say(id)


func _talk_fig() -> void:
	if GameState.room == "street":
		if not GameState.get_flag("intro_letter_read"):
			_say_lines([{"speaker":"Fig", "text":"Read your letter. I can't possibly be ominous until you've read your letter."}])
		elif not GameState.get_flag("fig_met"):
			_say("fig_street", func() -> void:
				GameState.set_flag("fig_met")
				_save()
			)
		else:
			_say_lines([{"speaker":"Fig", "text":"The door is at the top of the steps. Do try not to shake the doorknob. It gets attached."}])
	elif not GameState.get_flag("almost_unlocked"):
		_say("mirror", func() -> void:
			GameState.set_flag("almost_unlocked")
			_save()
			ui.toast("Pocket mirror acquired. Press Space to reveal The Almost.")
		)
	else:
		_choices("Fig", "What requires upper management?", [
			{"id":"hint", "text":"A little guidance"},
			{"id":"house", "text":"What is this house?"},
			{"id":"bye", "text":"I'll keep looking"}
		], func(choice: String) -> void:
			if choice == "hint":
				_hint = GameState.next_hint()
				_save(false)
				_say_lines([{"speaker":"Fig", "text":_hint}])
			elif choice == "house":
				_say_lines([{"speaker":"Fig", "text":"A place for things that almost happened. Unwritten books. Unspoken apologies. Very nearly adequate tea."}, {"speaker":"Fig", "text":"It is also a home. The distinction matters.", "portrait":2}])
		)


func _guestbook() -> void:
	if GameState.get_flag("guestbook_solved"):
		_say_lines([{"speaker":"Guestbook", "text":"THE VISITOR — PRESENT.\nYour name stays on the page, even when you look away."}])
	elif not GameState.get_flag("almost_unlocked"):
		_say("book_declined")
	elif not GameState.get_flag("clue_guest_title"):
		_say("book_needs_clue")
	else:
		_choices("Guestbook", "Under which title should the house welcome you?", [
			{"id":"owner", "text":"The Owner"},
			{"id":"visitor", "text":"The Visitor"},
			{"id":"inspector", "text":"The Inspector"}
		], func(choice: String) -> void:
			if GameState.attempt_guestbook(choice):
				_save(false)
				sound.play_cue("success")
				_say("book_accepted", func() -> void: ui.toast("Progress saved. A red notice has arrived on the left sideboard."))
			else:
				_say_lines([{"speaker":"Guestbook", "text":"DECLINED. An ambitious claim. Please consult the portrait before applying for a promotion."}])
		)
