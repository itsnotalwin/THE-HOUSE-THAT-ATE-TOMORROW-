extends SceneTree
## Full chapter integration: real scene, input routing, dialogue signals and disk saves.
## Target approaches are teleported between steps; this does not certify player routes.

var failures: int = 0
var assertions: int = 0
var game: Control
var state: Node
var test_save: String
var original_save: String


func _initialize() -> void:
	call_deferred("_run")


func expect(condition: bool, message: String) -> void:
	assertions += 1
	if not condition:
		failures += 1
		push_error(message)


func _settle() -> void:
	await process_frame
	await physics_frame
	await process_frame


func _tap(code: Key) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.physical_keycode = code
	event.pressed = true
	Input.parse_input_event(event)
	await process_frame
	event = event.duplicate()
	event.pressed = false
	Input.parse_input_event(event)
	await _settle()


func _interact(id: String) -> void:
	expect(not game.ui.is_modal(), "Interaction %s starts outside a modal" % id)
	game.world.player.position = game.world.get_target_position(id)
	await _settle()
	expect(game.world.get_target_id() == id, "Safe approach selects %s" % id)
	await _tap(KEY_E)


func _finish_lines() -> void:
	var safety: int = 0
	while not game._lines.is_empty() and safety < 30:
		safety += 1
		await _tap(KEY_E)
	expect(safety < 30, "Conversation finishes without an input loop")


func _blocked_movement(message: String) -> void:
	var before: Vector2 = game.world.get_player_position()
	Input.action_press("move_right")
	for frame: int in range(12):
		await physics_frame
	Input.action_release("move_right")
	expect(game.world.get_player_position().is_equal_approx(before), message)


func _scene() -> void:
	game = load("res://scenes/main.tscn").instantiate()
	root.add_child(game)
	await _settle()


func _run() -> void:
	state = root.get_node("GameState")
	original_save = state.save_path
	test_save = "user://slice-test-%s.json" % str(Time.get_ticks_usec())
	state.save_path = test_save
	await _scene()
	expect(game.ui.panel_name() == "title" and not game.playing, "Boot waits at the title")
	expect(not state.has_save(), "Fresh test has no Continue progress")
	game.ui.action_requested.emit("new_game")
	await _settle()
	expect(game.playing and state.room == "street", "New Game enters the street")
	expect(state.has_save(), "Starting the chapter creates a valid save")
	await _tap(KEY_SPACE)
	expect(not state.mode_almost, "Space cannot reveal Almost before the mirror")
	await _interact("house_door")
	await _finish_lines()
	expect(state.room == "street", "Letter gate prevents entering the house")
	await _interact("fig")
	await _finish_lines()
	expect(not state.get_flag("fig_met"), "Fig asks for the letter before introducing the house")
	await _interact("letter")
	expect(game.ui.panel_name() == "dialogue", "E opens the targeted letter")
	expect(not state.get_flag("intro_letter_read"), "Opening the letter alone does not grant its reward")
	await _blocked_movement("Dialogue blocks movement")
	await _tap(KEY_ESCAPE)
	expect(game.ui.panel_name() == "dialogue" and not state.get_flag("intro_letter_read"), "Escape cannot discard required dialogue callbacks")
	var old_index: int = game._line_index
	await _tap(KEY_E)
	expect(game._line_index == old_index + 1, "One E press advances exactly one dialogue line")
	await _finish_lines()
	expect(state.get_flag("intro_letter_read"), "Finished letter adds the inventory clue")
	await _interact("house_door")
	await _finish_lines()
	expect(state.room == "street", "Fig introduction remains required after the letter")
	await _interact("fig")
	await _finish_lines()
	expect(state.get_flag("fig_met"), "Street conversation meets Fig")
	await _interact("house_door")
	expect(state.room == "hall" and game.world.current_room == "hall", "Door transitions both state and world into the hall")
	await _interact("street_exit")
	await _finish_lines()
	expect(state.room == "hall", "The Guestbook gates departure")
	await _interact("guestbook")
	await _finish_lines()
	expect(not state.get_flag("guestbook_solved"), "Guestbook requires the mirror and discovered clue")
	await _interact("fig")
	await _finish_lines()
	expect(state.get_flag("almost_unlocked"), "Hall conversation grants the mirror")
	await _tap(KEY_N)
	expect(game.ui.panel_name() == "notebook", "N opens the notebook")
	await _blocked_movement("Notebook blocks movement")
	game.ui.action_requested.emit("hint")
	await _settle()
	expect(state.hint_tier == 1 and not state.get_flag("clue_guest_title"), "Notebook hint progresses guidance without granting the clue")
	await _tap(KEY_ESCAPE)
	expect(not game.ui.is_modal(), "Escape closes the notebook")
	await _interact("portrait")
	await _finish_lines()
	expect(not state.get_flag("clue_guest_title"), "Here portrait does not reveal the hidden name")
	await _tap(KEY_SPACE)
	expect(state.mode_almost, "Space enters Almost after Fig gives the mirror")
	await _interact("portrait")
	expect(not state.get_flag("clue_guest_title"), "Almost clue waits for its conversation callback")
	await _finish_lines()
	expect(state.get_flag("clue_guest_title"), "Almost portrait records THE VISITOR")
	await _tap(KEY_SPACE)
	expect(not state.mode_almost and state.get_flag("clue_guest_title"), "Returning Here preserves the learned title")
	await _interact("guestbook")
	expect(game._choice_handler.is_valid(), "Guestbook offers choices once the clue is known")
	await _tap(KEY_E)
	expect(game._choice_handler.is_valid() and not state.get_flag("guestbook_solved"), "E cannot accidentally select a dialogue choice")
	game.ui.choice_selected.emit("owner")
	await _settle()
	await _finish_lines()
	expect(not state.get_flag("guestbook_solved"), "Wrong Guestbook answer leaves the puzzle retryable")
	await _interact("guestbook")
	game.ui.choice_selected.emit("visitor")
	await _settle()
	await _finish_lines()
	expect(state.get_flag("guestbook_solved"), "Correct discovered title solves the Guestbook")
	await _interact("kitchen_door")
	await _finish_lines()
	expect(game.ui.panel_name() != "completion", "Unlocked door first asks the Visitor to read the notice")
	await _interact("notice")
	await _finish_lines()
	expect(state.get_flag("erasure_notice_read"), "Notice records the chapter's warning")
	await _interact("kitchen_door")
	expect(game.ui.panel_name() == "completion", "Unlocked door presents the chapter ending after the notice")
	await _blocked_movement("Chapter completion blocks movement")
	game.ui.action_requested.emit("resume")
	await _settle()
	expect(not game.ui.is_modal(), "Continue exploring returns control to the hall")
	await _tap(KEY_ESCAPE)
	expect(game.ui.panel_name() == "pause", "Escape pauses exploration")
	await _blocked_movement("Pause blocks movement")
	game.ui.action_requested.emit("title")
	await _settle()
	expect(game.ui.panel_name() == "title" and not game.playing, "Save & title returns to the title screen")
	var expected: Dictionary = state._snapshot().duplicate(true)
	# Recreate the scene and clear live state: Continue must load the disk snapshot.
	game.queue_free()
	await _settle()
	state.start_new()
	await _scene()
	expect(not game.playing and game.ui.panel_name() == "title", "Reloaded app still waits for Continue")
	game.ui.action_requested.emit("continue")
	await _settle()
	expect(game.playing and state._snapshot() == expected, "Continue restores every persisted chapter field")
	expect(game.world.current_room == "hall" and game.world.get_player_position().is_equal_approx(state.player_position), "Continue restores the actual room and player position")
	await _interact("library_door")
	expect(game.ui.panel_name() == "completion", "The second opened door also reaches the saved chapter ending")
	game.queue_free()
	await _settle()
	# The headless audio backend releases its last playback references asynchronously.
	await create_timer(0.1).timeout
	state.save_path = original_save
	for suffix: String in ["", ".bak", ".tmp", ".bak.tmp"]:
		var path: String = ProjectSettings.globalize_path(test_save + suffix)
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(path)
	print("Slice integration: %d assertions, %d failures" % [assertions, failures])
	quit(1 if failures else 0)
