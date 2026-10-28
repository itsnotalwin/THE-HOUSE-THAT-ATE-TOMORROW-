extends Node2D
class_name HouseWorld
## Two authored rooms. Mode changes artwork, never physical room geometry.

const SPEED: float = 72.0
const ROOM_SIZE := Vector2(512.0, 352.0)
const VISITOR_SHEET: Texture2D = preload("res://assets/visitor_sheet.png")
const FIG_SHEET: Texture2D = preload("res://assets/fig_sheet.png")
const ATLAS_HERE: Texture2D = preload("res://assets/foyer_atlas_here.png")
const ATLAS_ALMOST: Texture2D = preload("res://assets/foyer_atlas_almost.png")
const STREET_BACKGROUND: Texture2D = preload("res://assets/street_background.png")

var player: CharacterBody2D
var current_room: String = "street"
var reduced_motion: bool = false
var _enabled: bool = false
var _almost: bool = false
var _solved: bool = false
var _layout: Dictionary = {}
var _atlas_data: Dictionary = {}
var _targets: Array = []
var _room_root: Node2D
var _sortable: Node2D
var _ceiling: Node2D
var _player_sprite: Sprite2D
var _fig_sprite: Sprite2D
var _camera: Camera2D
var _notice: Polygon2D
var _door_markers: Array[Polygon2D] = []
var _mode_sprites: Array[Sprite2D] = []
var _ceiling_sprites: Array[Sprite2D] = []
var _almost_objects: Array[Node2D] = []
var _facing: Vector2 = Vector2.DOWN
var _direction_row: int = 0
var _walk_time: float = 0.0
var _ambient_time: float = 0.0


func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	_atlas_data = _read_dictionary("res://assets/foyer_atlas.json")
	set_physics_process(true)
	set_process(true)


func load_room(room_id: String, spawn: Vector2, almost: bool, solved: bool) -> void:
	current_room = "hall" if room_id == "hall" or room_id == "entrance_hall" else "street"
	_almost = almost
	_solved = solved
	if _atlas_data.is_empty():
		_atlas_data = _read_dictionary("res://assets/foyer_atlas.json")
	if is_instance_valid(_room_root):
		remove_child(_room_root)
		_room_root.queue_free()
	_mode_sprites.clear()
	_ceiling_sprites.clear()
	_almost_objects.clear()
	_door_markers.clear()
	_notice = null
	_room_root = Node2D.new()
	_room_root.name = "AuthoredRoom"
	add_child(_room_root)
	_sortable = Node2D.new()
	_sortable.name = "DepthSortedFurnitureAndResidents"
	_sortable.y_sort_enabled = true
	_room_root.add_child(_sortable)
	_ceiling = Node2D.new()
	_ceiling.name = "Ceiling"
	_ceiling.z_index = 20
	_room_root.add_child(_ceiling)
	_layout = _read_dictionary("res://data/%s_layout.json" % current_room)
	_targets = _layout.get("targets", [])
	if current_room == "hall":
		_build_hall()
	else:
		_build_street()
	_build_collisions()
	_build_player(spawn)
	_build_fig()
	set_mode(_almost)
	set_solved(_solved)
	_walk_time = 0.0
	_ambient_time = 0.0
	queue_redraw()


func _read_dictionary(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("Missing room data: " + path)
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


func _build_hall() -> void:
	var placements: Array = _layout.get("placements", [])
	for entry: Dictionary in placements:
		var asset_name: String = str(entry.get("asset", ""))
		var layer: String = str(entry.get("layer", ""))
		var mode: String = str(entry.get("mode", "both"))
		var coordinates: Array = entry.get("position_px", [0, 0])
		var top_left := Vector2(float(coordinates[0]), float(coordinates[1]))
		var object_data: Dictionary = _atlas_data["objects"][asset_name]
		var atlas_rect: Array = object_data["atlas_rect_px"]
		var native_size := Vector2(float(atlas_rect[2]), float(atlas_rect[3]))
		var sprite := Sprite2D.new()
		sprite.name = asset_name
		sprite.texture = ATLAS_HERE
		sprite.region_enabled = true
		sprite.region_rect = Rect2(float(atlas_rect[0]), float(atlas_rect[1]), native_size.x, native_size.y)
		sprite.centered = false
		_mode_sprites.append(sprite)
		if layer in ["floor", "floor_border", "wall", "trim", "architecture", "rug"] or asset_name == "nameplate":
			sprite.position = top_left
			sprite.z_index = -10
			_room_root.add_child(sprite)
		elif layer == "ceiling":
			sprite.position = top_left
			_ceiling.add_child(sprite)
			_ceiling_sprites.append(sprite)
		else:
			var baseline: float = top_left.y + native_size.y
			if asset_name == "guestbook":
				baseline = 224.0
			elif asset_name == "candle":
				baseline = 224.0 if top_left.x < 200.0 else 240.0
			elif asset_name == "ghost_reader":
				baseline = 240.0
			var depth_anchor := Node2D.new()
			depth_anchor.name = asset_name + "FootAnchor"
			depth_anchor.position = Vector2(top_left.x, baseline)
			_sortable.add_child(depth_anchor)
			sprite.position = Vector2(0.0, top_left.y - baseline)
			depth_anchor.add_child(sprite)
		if mode == "almost":
			_almost_objects.append(sprite)
	# A real warning notice appears on the existing sideboard after the puzzle.
	_notice = Polygon2D.new()
	_notice.name = "DepartmentWarning"
	_notice.polygon = PackedVector2Array([Vector2(0, 0), Vector2(13, 0), Vector2(13, 15), Vector2(0, 15)])
	_notice.color = Color("a74758")
	_notice.position = Vector2(132, 182)
	_notice.z_index = 21
	_room_root.add_child(_notice)
	var notice_mark := Line2D.new()
	_notice.add_child(notice_mark)
	notice_mark.points = PackedVector2Array([Vector2(4, 3), Vector2(9, 3), Vector2(9, 5), Vector2(4, 5), Vector2(4, 8), Vector2(9, 8)])
	notice_mark.width = 1.0
	notice_mark.default_color = Color("f4dbb9")
	for x: float in [104.0, 408.0]:
		var marker := Polygon2D.new()
		marker.polygon = PackedVector2Array([Vector2(-10, 0), Vector2(10, 0), Vector2(14, 5), Vector2(-14, 5)])
		marker.position = Vector2(x, 110)
		marker.color = Color("f6b56b")
		marker.z_index = -5
		_room_root.add_child(marker)
		_door_markers.append(marker)


func _build_street() -> void:
	var background := Sprite2D.new()
	background.name = "OriginalNativeStreet"
	background.texture = STREET_BACKGROUND
	background.centered = false
	background.z_index = -20
	_room_root.add_child(background)


func _build_collisions() -> void:
	for coordinates: Array in _layout.get("collision_rects_px", []):
		var rect := Rect2(float(coordinates[0]), float(coordinates[1]), float(coordinates[2]), float(coordinates[3]))
		var body := StaticBody2D.new()
		body.position = rect.position + rect.size / 2.0
		body.collision_layer = 1
		body.collision_mask = 0
		var collision := CollisionShape2D.new()
		var shape := RectangleShape2D.new()
		shape.size = rect.size
		collision.shape = shape
		body.add_child(collision)
		_room_root.add_child(body)


func _build_player(spawn: Vector2) -> void:
	player = CharacterBody2D.new()
	player.name = "Visitor"
	player.motion_mode = CharacterBody2D.MOTION_MODE_FLOATING
	player.collision_layer = 2
	player.collision_mask = 1
	player.safe_margin = 0.01
	var floor_y: float = 121.0 if current_room == "hall" else 191.0
	player.position = Vector2(clampf(spawn.x, 24.0, 488.0), clampf(spawn.y, floor_y, 337.0))
	_sortable.add_child(player)
	var collision := CollisionShape2D.new()
	var shape := RectangleShape2D.new()
	shape.size = Vector2(10, 6)
	collision.shape = shape
	collision.position = Vector2(0, -3)
	player.add_child(collision)
	_player_sprite = Sprite2D.new()
	_player_sprite.texture = VISITOR_SHEET
	_player_sprite.hframes = 5
	_player_sprite.vframes = 4
	_player_sprite.centered = false
	_player_sprite.position = Vector2(-12, -30)
	player.add_child(_player_sprite)
	_camera = Camera2D.new()
	_camera.name = "NativePixelCamera"
	_camera.position_smoothing_enabled = false
	_camera.limit_left = 0
	_camera.limit_top = 0
	_camera.limit_right = 512
	_camera.limit_bottom = 352
	_camera.position = Vector2.ZERO
	player.add_child(_camera)
	_camera.make_current()
	_camera.reset_smoothing()
	_direction_row = 0
	_facing = Vector2.DOWN


func _build_fig() -> void:
	var fig_anchor := Node2D.new()
	fig_anchor.name = "Fig"
	fig_anchor.position = Vector2(220, 244) if current_room == "hall" else Vector2(294, 198)
	_sortable.add_child(fig_anchor)
	_fig_sprite = Sprite2D.new()
	_fig_sprite.texture = FIG_SHEET
	_fig_sprite.hframes = 4
	_fig_sprite.centered = false
	_fig_sprite.position = Vector2(-12, -22)
	fig_anchor.add_child(_fig_sprite)


func set_mode(value: bool) -> void:
	_almost = value
	for sprite: Sprite2D in _mode_sprites:
		sprite.texture = ATLAS_ALMOST if _almost else ATLAS_HERE
	for item: Node2D in _almost_objects:
		item.visible = _almost
	queue_redraw()


func set_solved(value: bool) -> void:
	_solved = value
	if is_instance_valid(_notice):
		_notice.visible = value
	for marker: Polygon2D in _door_markers:
		marker.visible = value
	queue_redraw()


func set_enabled(value: bool) -> void:
	_enabled = value
	if is_instance_valid(player) and not value:
		player.velocity = Vector2.ZERO
		_player_sprite.frame = _direction_row * 5


func get_player_position() -> Vector2:
	return player.position if is_instance_valid(player) else Vector2(256, 290)


func _physics_process(delta: float) -> void:
	if not is_instance_valid(player) or not _enabled:
		return
	var movement := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	player.velocity = movement * SPEED
	player.move_and_slide()
	if movement.length_squared() > 0.01:
		_facing = movement.normalized()
		if absf(movement.x) > absf(movement.y):
			_direction_row = 2 if movement.x > 0.0 else 1
		else:
			_direction_row = 0 if movement.y > 0.0 else 3
		_walk_time += delta
		_player_sprite.frame = _direction_row * 5 + 1 + int(_walk_time * 6.0) % 4
	else:
		_walk_time = 0.0
		_player_sprite.frame = _direction_row * 5


func _process(delta: float) -> void:
	_update_ceiling_visibility()
	if not is_instance_valid(_fig_sprite) or not _enabled:
		return
	_ambient_time += delta
	var cycle: float = fmod(_ambient_time, 5.6)
	_fig_sprite.frame = 1 if cycle > 5.2 and cycle < 5.34 else (2 if cycle > 3.6 and cycle < 4.0 else 0)
	if current_room == "street" and not reduced_motion:
		queue_redraw()


func _update_ceiling_visibility() -> void:
	if not is_instance_valid(player):
		return
	var visitor_bounds := Rect2(player.position + Vector2(-12, -30), Vector2(24, 32))
	for sprite: Sprite2D in _ceiling_sprites:
		var overlaps: bool = Rect2(sprite.position, sprite.region_rect.size).intersects(visitor_bounds)
		sprite.modulate.a = 0.22 if overlaps else 1.0


func _draw() -> void:
	# Quiet rain stays in native pixels and carries no gameplay information.
	if current_room == "street" and not reduced_motion:
		for i: int in range(25):
			var x: float = float((i * 83 + 31) % 512)
			var y: float = fmod(float(i * 47) + _ambient_time * 44.0, 352.0)
			draw_line(Vector2(x, floorf(y)), Vector2(x - 1.0, floorf(y) + 3.0), Color(0.45, 0.58, 0.77, 0.2), 1.0)


func _target() -> Dictionary:
	if not is_instance_valid(player):
		return {}
	var best: Dictionary = {}
	var best_score: float = INF
	for target: Dictionary in _targets:
		if bool(target.get("requires_solved", false)) and not _solved:
			continue
		var coordinates: Array = target["approach_px"]
		var point := Vector2(float(coordinates[0]), float(coordinates[1]))
		var offset: Vector2 = point - player.position
		var distance: float = offset.length()
		var radius: float = float(target.get("radius_px", 30.0))
		if distance > radius:
			continue
		if distance > 2.0:
			var sight := PhysicsRayQueryParameters2D.create(player.global_position + Vector2(0, -3), to_global(point) + Vector2(0, -3), 1)
			if not get_world_2d().direct_space_state.intersect_ray(sight).is_empty():
				continue
		# Facing breaks ties without making precise pixel positioning necessary.
		var facing_bonus: float = _facing.dot(offset.normalized()) * 5.0 if distance > 1.0 else 5.0
		var score: float = distance - facing_bonus
		if score < best_score:
			best_score = score
			best = target
	return best


func get_target_id() -> String:
	return str(_target().get("id", ""))


func get_target_label() -> String:
	return str(_target().get("label", ""))


func get_target_position(id: String) -> Vector2:
	for target: Dictionary in _targets:
		if str(target.get("id", "")) == id:
			var coordinates: Array = target["approach_px"]
			return Vector2(float(coordinates[0]), float(coordinates[1]))
	return get_player_position()
