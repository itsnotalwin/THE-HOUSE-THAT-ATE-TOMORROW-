extends SceneTree

var world: Node2D
var failures: Array[String] = []

func _initialize() -> void:
	call_deferred("run")

func check(ok: bool, message: String) -> void:
	if not ok:
		failures.append(message)
		print("FAIL: " + message)

func run() -> void:
	for action: String in ["move_left", "move_right", "move_up", "move_down"]:
		if not InputMap.has_action(action):
			InputMap.add_action(action)
	var viewport := SubViewport.new()
	viewport.size = Vector2i(384, 216)
	root.add_child(viewport)
	world = load("res://scripts/world.gd").new()
	viewport.add_child(world)
	await process_frame
	for room: String in ["street", "hall"]:
		world.load_room(room, Vector2(256, 290), false, true)
		await physics_frame
		var layout: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/%s_layout.json" % room))
		for target: Dictionary in layout["targets"]:
			var id: String = target["id"]
			world.player.position = world.get_target_position(id)
			await physics_frame
			var actual: String = world.get_target_id()
			check(actual == id, "%s/%s approach selected %s" % [room, id, actual])
			var foot := Rect2(world.player.position - Vector2(5, 6), Vector2(10, 6))
			for raw: Array in layout["collision_rects_px"]:
				var obstacle := Rect2(float(raw[0]), float(raw[1]), float(raw[2]), float(raw[3]))
				check(not foot.intersects(obstacle), "%s/%s approach overlaps obstacle" % [room, id])
		print(room + ": target selection checked")
	world.load_room("hall", Vector2(256, 300), false, false)
	await physics_frame
	world.player.position = world.get_target_position("notice")
	await physics_frame
	check(world.get_target_id() != "notice", "Notice available before puzzle solution")
	world.set_solved(true)
	check(world.get_target_id() == "notice", "Notice unavailable after puzzle solution")
	world.player.position = Vector2(256, 300)
	world.set_enabled(true)
	Input.action_press("move_up")
	for i: int in range(120):
		await physics_frame
	Input.action_release("move_up")
	var before_mode: Vector2 = world.player.position
	for i: int in range(20):
		world.set_mode(i % 2 == 0)
	check(world.player.position.is_equal_approx(before_mode), "Mode switching moved player")
	check(world.player.position.y > 111.0, "Player passed through north wall")
	check(world.player.position.y < 180.0, "Player did not move up central hall")
	Input.action_press("move_right")
	world.set_enabled(false)
	var paused: Vector2 = world.player.position
	for i: int in range(10):
		await physics_frame
	Input.action_release("move_right")
	check(world.player.position.is_equal_approx(paused), "Disabled world still moves")
	print("World smoke: %s; %d failures" % ["PASS" if failures.is_empty() else "FAIL", failures.size()])
	quit(0 if failures.is_empty() else 1)
