extends SceneTree

const StateScript = preload("res://scripts/state.gd")
var failures: int = 0
var assertions: int = 0
var state: Node
var path: String


func _initialize() -> void:
	call_deferred("_run")


func expect(condition: bool, message: String) -> void:
	assertions += 1
	if not condition:
		failures += 1
		push_error(message)


func _write(data: Variant) -> void:
	var file: FileAccess = FileAccess.open(path, FileAccess.WRITE)
	file.store_string(data if typeof(data) == TYPE_STRING else JSON.stringify(data))
	file.close()


func _remove_backups() -> void:
	for suffix: String in [".bak", ".bak.tmp", ".tmp"]:
		if FileAccess.file_exists(path + suffix):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(path + suffix))


func _snapshot() -> Dictionary:
	return state._snapshot().duplicate(true)


func _unlock() -> void:
	state.set_flag("intro_letter_read")
	state.set_flag("fig_met")
	state.enter_room("hall", Vector2(256, 300))
	state.set_flag("almost_unlocked")


func _run() -> void:
	state = StateScript.new()
	root.add_child(state)
	path = "user://state-test-%s.json" % str(Time.get_ticks_usec())
	state.save_path = path
	expect(not state.has_save(), "Fresh test must have no save")
	var fresh: Dictionary = _snapshot()
	for prerequisite_flag: String in ["almost_unlocked", "clue_guest_title", "guestbook_solved", "erasure_notice_read", "unknown_flag"]:
		state.set_flag(prerequisite_flag)
	expect(_snapshot() == fresh, "Out-of-order flags and unknown flags must not advance progress")
	state.enter_room("attic", Vector2(256, 280))
	state.enter_room("hall", Vector2(NAN, 280))
	expect(_snapshot() == fresh, "Invalid room transitions must preserve the current room and position")
	expect(not state.toggle_mode(), "Mode is unavailable before Fig gives the mirror")
	expect(not state.learn_title(), "Cannot discover a title without the mirror")
	expect(not state.attempt_guestbook("visitor"), "Guessing the correct answer early must not solve the puzzle")
	_unlock()
	expect(not state.learn_title(), "Here portrait must not reveal the title")
	expect(not state.attempt_guestbook("visitor"), "Mirror alone must not bypass clue discovery")
	expect(state.toggle_mode(), "Hall mode should toggle after mirror unlock")
	expect(state.learn_title(), "Almost portrait should add the clue")
	expect(not state.attempt_guestbook("landlord"), "Wrong Guestbook answer must fail safely")
	expect(not state.get_flag("guestbook_solved"), "Wrong answer must leave puzzle unsolved")
	expect(state.attempt_guestbook("visitor"), "Learned title should solve Guestbook in either mode")
	var after_solve: Dictionary = _snapshot()
	expect(state.attempt_guestbook("visitor"), "Repeated correct answer should remain successful")
	expect(_snapshot() == after_solve, "Repeat solve must not duplicate rewards or mutate state")
	for count: int in range(100):
		state.toggle_mode()
	expect(state.get_flag("guestbook_solved") and state.get_flag("clue_guest_title"), "Rapid mode changes must retain puzzle progress")
	expect(state.mode_almost, "Even toggle count should restore starting mode")
	state.set_flag("erasure_notice_read")
	expect(state.next_hint() == state.objective(), "Completed notice hint must point forward instead of repeating a discovered clue")
	state.set_settings({"master_volume": 0.6, "reduced_motion": true, "text_size": 26})
	state.next_hint()
	var saved_snapshot: Dictionary = _snapshot()
	expect(state.save_game(), "Valid state must save")
	expect(state.has_save(), "Saved progress must enable Continue")
	state.start_new()
	expect(not state.get_flag("guestbook_solved"), "New game clears puzzle progress")
	expect(state.settings["text_size"] == 26, "New game preserves accessibility settings")
	expect(state.load_game(), "Saved progress must load")
	expect(_snapshot() == saved_snapshot, "Save roundtrip must retain room, position, mode, flags and settings")
	# A second valid write preserves the prior valid save as a recovery copy.
	state.player_position = Vector2(240, 296)
	expect(state.save_game(), "A second save must atomically replace the primary")
	_write("{truncated")
	expect(state.has_save(), "A valid backup should keep Continue available")
	expect(state.load_game() and state.recovered_backup, "Corrupt primary should recover its previous valid backup")
	expect(_snapshot() == saved_snapshot, "Backup recovery must restore the actual earlier snapshot")
	_remove_backups()
	var live: Dictionary = _snapshot()
	for bad: Variant in ["{broken", [], {"schema_version": 9}]:
		_write(bad)
		expect(not state.load_game(), "Malformed or unsupported save must fail")
		expect(_snapshot() == live, "Rejected load must not replace active progress")
	var malformed: Dictionary = live.duplicate(true)
	malformed["schema_version"] = 9
	_write(malformed)
	expect(not state.load_game() and _snapshot() == live, "A complete but unsupported-schema save must leave active progress intact")
	malformed = live.duplicate(true)
	malformed["flags"]["clue_guest_title"] = false
	_write(malformed)
	expect(not state.load_game(), "Solved puzzle without its required clue is invalid")
	malformed = live.duplicate(true)
	malformed["player_position"] = [999999, -1]
	_write(malformed)
	expect(not state.load_game(), "Out-of-room positions must be rejected")
	malformed = live.duplicate(true)
	malformed["flags"]["fig_met"] = "true"
	_write(malformed)
	expect(not state.load_game(), "String flags must not become truthy state")
	malformed = live.duplicate(true)
	malformed["settings"] = {"master_volume": 4, "music_volume": -2, "sfx_volume": "loud", "text_size": 2, "reduced_motion": "false"}
	_write(malformed)
	expect(state.load_game(), "Valid progress may recover malformed optional settings")
	expect(state.settings["master_volume"] == 1.0 and state.settings["music_volume"] == 0.0, "Volume settings must stay bounded")
	expect(state.settings["sfx_volume"] == 0.7 and state.settings["text_size"] == 18, "Invalid settings fall back or clamp safely")
	expect(not state.settings["reduced_motion"], "String false must not become true")
	state.start_new()
	_unlock()
	expect(state.next_hint() == state.HINTS[0], "First hint is indirect")
	expect(state.next_hint() == state.HINTS[1], "Second hint points to the portrait")
	expect(state.next_hint() == state.HINTS[2], "Third hint gives the exact title")
	expect(state.next_hint() == state.HINTS[2] and state.hint_tier == 3, "Hint tier is bounded and repeatable")
	state.enter_room("street", Vector2(256, 280))
	expect(not state.mode_almost and not state.toggle_mode(), "Street remains Here and cannot expose hall-only clues")
	expect(not state.attempt_guestbook("visitor"), "Guestbook cannot resolve from another room")
	state.enter_room("hall", Vector2(256, 300))
	state.toggle_mode()
	state.learn_title()
	state.attempt_guestbook("visitor")
	state.set_flag("erasure_notice_read")
	state.set_flag("fig_met", false)
	expect(not state.mode_almost and not state.get_flag("almost_unlocked") and not state.get_flag("clue_guest_title") and not state.get_flag("guestbook_solved") and not state.get_flag("erasure_notice_read"), "Removing a prerequisite must roll back dependent progression safely")
	expect(state.save_game(), "A valid rollback state must remain saveable")
	var previous_save: String = FileAccess.get_file_as_string(path)
	state.player_position = Vector2(INF, 280)
	expect(not state.save_game(), "Non-finite positions must not be persisted")
	expect(FileAccess.get_file_as_string(path) == previous_save, "A rejected save must not change the previous primary file")
	state.free()
	_remove_backups()
	if FileAccess.file_exists(path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	print("State tests: %s assertions, %s failures" % [assertions, failures])
	quit(1 if failures else 0)
