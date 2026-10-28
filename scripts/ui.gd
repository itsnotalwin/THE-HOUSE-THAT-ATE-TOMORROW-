class_name SliceUI
extends Control
## High-resolution interface over the native 384x216 world viewport.
## No game state is owned here. The coordinator supplies text and handles actions.

signal action_requested(action: String)
signal dialogue_advanced
signal choice_selected(id: String)
signal setting_changed(key: String, value: Variant)

const PAPER := Color("f4dbb9")
const PLUM := Color("25152e")
const INK := Color("11101c")
const BLUSH := Color("ef93b4")
const MOON := Color("c7d8e9")
const MINT := Color("9adbc7")
const AMBER := Color("f6b56b")
const WINE := Color("752c58")

var _built: bool = false
var _font_size: int = 22
var _font: Font
var _serif: Font
var _title: Control
var _hud: Control
var _modal: Control
var _modal_center: CenterContainer
var _dialogue: PanelContainer
var _dialogue_content: VBoxContainer
var _dialogue_choices: Array = []
var _objective: Label
var _mode: Label
var _mode_icon: TextureRect
var _room: Label
var _prompt: Label
var _prompt_panel: PanelContainer
var _toast_panel: PanelContainer
var _toast_label: Label
var _toast_remaining: float = 0.0
var _has_save: bool = false
var _current_panel: String = ""
var _dialogue_continue: Button


func _ready() -> void:
	_ensure_built()


func _process(delta: float) -> void:
	if _toast_remaining > 0.0:
		_toast_remaining = maxf(0.0, _toast_remaining - delta)
		_toast_panel.visible = _toast_remaining > 0.0


func _unhandled_key_input(event: InputEvent) -> void:
	# Enter and Space are handled by the focused Godot Button. E is the
	# dialogue shortcut only when there is no decision to make.
	if event is InputEventKey and event.pressed and not event.echo:
		if _built and _dialogue.visible and _dialogue_choices.is_empty() and event.physical_keycode == KEY_E:
			get_viewport().set_input_as_handled()
			dialogue_advanced.emit()


func _ensure_built() -> void:
	if _built:
		return
	_built = true
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	_font = load("res://assets/DejaVuSans.ttf") as Font
	_serif = load("res://assets/DejaVuSerif-Bold.ttf") as Font
	var skin := Theme.new()
	skin.default_font = _font
	skin.default_font_size = _font_size
	skin.set_color("font_color", "Label", PAPER)
	skin.set_color("font_color", "Button", PAPER)
	skin.set_color("font_hover_color", "Button", PAPER)
	skin.set_color("font_focus_color", "Button", PAPER)
	skin.set_color("font_pressed_color", "Button", PAPER)
	skin.set_color("font_disabled_color", "Button", MOON.darkened(0.25))
	skin.set_stylebox("normal", "Button", _texture_style("button_normal.png"))
	skin.set_stylebox("hover", "Button", _texture_style("button_focused.png"))
	skin.set_stylebox("pressed", "Button", _texture_style("button_focused.png"))
	skin.set_stylebox("disabled", "Button", _texture_style("button_disabled.png"))
	var focus := StyleBoxFlat.new()
	focus.bg_color = Color.TRANSPARENT
	focus.border_color = BLUSH
	focus.set_border_width_all(2)
	focus.set_corner_radius_all(2)
	focus.expand_margin_left = 2.0
	focus.expand_margin_right = 2.0
	focus.expand_margin_top = 2.0
	focus.expand_margin_bottom = 2.0
	skin.set_stylebox("focus", "Button", focus)
	skin.set_stylebox("focus", "CheckBox", focus)
	skin.set_stylebox("focus", "HSlider", focus)
	skin.set_stylebox("panel", "PanelContainer", _texture_style("dialogue_panel.png"))
	theme = skin
	_build_title()
	_build_hud()
	_build_dialogue()
	_modal = Control.new()
	_full(_modal, self)
	_modal.mouse_filter = Control.MOUSE_FILTER_STOP
	var shade := ColorRect.new()
	shade.color = Color(0.035, 0.025, 0.065, 0.83)
	_full(shade, _modal)
	shade.mouse_filter = Control.MOUSE_FILTER_STOP
	_modal_center = CenterContainer.new()
	_full(_modal_center, _modal)
	_modal_center.offset_left = 40.0
	_modal_center.offset_right = -40.0
	_modal_center.offset_top = 28.0
	_modal_center.offset_bottom = -28.0
	_modal.visible = false
	_build_toast()
	_title.visible = false
	_dialogue.visible = false
	_hud.visible = false


func _texture_style(filename: String) -> StyleBox:
	var tex: Texture2D = _texture(filename)
	if tex == null:
		var fallback := StyleBoxFlat.new()
		fallback.bg_color = PLUM
		fallback.border_color = AMBER
		fallback.set_border_width_all(1)
		fallback.set_content_margin_all(12.0)
		return fallback
	var box := StyleBoxTexture.new()
	box.texture = tex
	box.texture_margin_left = 8.0
	box.texture_margin_right = 8.0
	box.texture_margin_top = 8.0
	box.texture_margin_bottom = 8.0
	box.content_margin_left = 16.0
	box.content_margin_right = 16.0
	box.content_margin_top = 10.0
	box.content_margin_bottom = 10.0
	return box


func _texture(filename: String) -> Texture2D:
	var path: String = "res://assets/" + filename
	if ResourceLoader.exists(path):
		return load(path) as Texture2D
	return null


func _full(node: Control, parent: Node) -> void:
	parent.add_child(node)
	node.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)


func _label(text: String, size: int = 22, color: Color = PAPER, heading: bool = false) -> Label:
	var label := Label.new()
	label.text = text
	label.add_theme_font_size_override("font_size", size)
	label.add_theme_color_override("font_color", color)
	if heading:
		label.add_theme_font_override("font", _serif)
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return label


func _body(text: String, size: int = 0, color: Color = PAPER) -> Label:
	var label: Label = _label(text, _font_size if size == 0 else size, color)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	return label


func _button(text: String, callback: Callable, min_width: float = 0.0) -> Button:
	var button := Button.new()
	button.text = text
	button.custom_minimum_size = Vector2(min_width, 42.0)
	button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	button.focus_mode = Control.FOCUS_ALL
	button.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	button.add_theme_font_size_override("font_size", _font_size)
	button.pressed.connect(callback)
	button.focus_entered.connect(func() -> void: button.text = "› " + text)
	button.focus_exited.connect(func() -> void: button.text = text)
	return button


func _action_button(text: String, action: String, min_width: float = 0.0) -> Button:
	return _button(text, func() -> void: action_requested.emit(action), min_width)


func _focus(button: Control) -> void:
	_focus_if_visible.call_deferred(button)


func _focus_if_visible(button: Control) -> void:
	# A second panel can replace the first before its deferred focus runs.
	if is_instance_valid(button) and button.is_inside_tree() and button.is_visible_in_tree():
		button.grab_focus()


func _clear(parent: Node) -> void:
	for child: Node in parent.get_children():
		parent.remove_child(child)
		child.queue_free()


func _build_title() -> void:
	_title = Control.new()
	_full(_title, self)
	_title.mouse_filter = Control.MOUSE_FILTER_STOP
	var background := TextureRect.new()
	background.texture = _texture("mansion_background.png")
	background.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	background.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	background.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_full(background, _title)
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var veil := ColorRect.new()
	veil.color = Color(0.03, 0.02, 0.06, 0.16)
	_full(veil, _title)
	veil.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var logo := TextureRect.new()
	logo.texture = _texture("title_wordmark.png")
	logo.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	logo.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	logo.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_title.add_child(logo)
	logo.set_anchors_and_offsets_preset(Control.PRESET_TOP_LEFT)
	logo.position = Vector2(32, 116)
	logo.size = Vector2(490, 206)
	logo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	# Render the exact tagline as independent high-resolution text, so its
	# small-window presentation does not inherit a tiny baked font size.
	var tagline := _label("Tomorrow is missing.\nThe cat denies everything.", 20)
	_title.add_child(tagline)
	tagline.position = Vector2(44, 335)
	tagline.size = Vector2(466, 56)
	tagline.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	var menu := VBoxContainer.new()
	menu.name = "TitleActions"
	_title.add_child(menu)
	menu.position = Vector2(151, 411)
	menu.size = Vector2(252, 216)
	menu.add_theme_constant_override("separation", 5)
	var version := _label("A strange house. A missing tomorrow.", 16, MOON)
	_title.add_child(version)
	version.position = Vector2(40, 34)


func _build_hud() -> void:
	_hud = Control.new()
	_full(_hud, self)
	_hud.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var objective_panel := PanelContainer.new()
	_hud.add_child(objective_panel)
	objective_panel.position = Vector2(24, 20)
	objective_panel.size = Vector2(765, 54)
	objective_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_objective = _label("", 20)
	_objective.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	objective_panel.add_child(_objective)
	var mode_panel := PanelContainer.new()
	_hud.add_child(mode_panel)
	mode_panel.set_anchors_and_offsets_preset(Control.PRESET_TOP_RIGHT)
	mode_panel.offset_left = -213
	mode_panel.offset_right = -24
	mode_panel.offset_top = 20
	mode_panel.offset_bottom = 74
	mode_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var mode_row := HBoxContainer.new()
	mode_row.add_theme_constant_override("separation", 10)
	mode_panel.add_child(mode_row)
	_mode_icon = TextureRect.new()
	_mode_icon.texture = _texture("icon_sun.png")
	_mode_icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_mode_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_mode_icon.custom_minimum_size = Vector2(24, 24)
	_mode_icon.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	mode_row.add_child(_mode_icon)
	_mode = _label("The Here", 19)
	mode_row.add_child(_mode)
	_room = _label("", 16, MOON)
	_hud.add_child(_room)
	_room.position = Vector2(32, 80)
	_prompt_panel = PanelContainer.new()
	_hud.add_child(_prompt_panel)
	_prompt_panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER_BOTTOM)
	_prompt_panel.offset_left = -290
	_prompt_panel.offset_right = 290
	_prompt_panel.offset_top = -96
	_prompt_panel.offset_bottom = -48
	_prompt_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_prompt = _label("", 20)
	_prompt.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_prompt_panel.add_child(_prompt)
	var controls := _label("WASD / arrows  Move     E  Inspect     Space  The Almost     N / I  Notebook     Esc  Pause", 16, MOON)
	_hud.add_child(controls)
	controls.set_anchors_and_offsets_preset(Control.PRESET_CENTER_BOTTOM)
	controls.offset_left = -552
	controls.offset_right = 552
	controls.offset_top = -31
	controls.offset_bottom = -8
	controls.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER


func _build_dialogue() -> void:
	_dialogue = PanelContainer.new()
	add_child(_dialogue)
	_dialogue.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
	_dialogue.offset_left = 30
	_dialogue.offset_right = -30
	_dialogue.offset_top = -230
	_dialogue.offset_bottom = -30
	_dialogue.mouse_filter = Control.MOUSE_FILTER_STOP
	_dialogue_content = VBoxContainer.new()
	_dialogue_content.add_theme_constant_override("separation", 12)
	_dialogue.add_child(_dialogue_content)


func _build_toast() -> void:
	_toast_panel = PanelContainer.new()
	add_child(_toast_panel)
	_toast_panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER_TOP)
	_toast_panel.offset_left = -370
	_toast_panel.offset_right = 370
	_toast_panel.offset_top = 112
	_toast_panel.offset_bottom = 162
	_toast_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_toast_label = _label("", 18, MINT)
	_toast_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_toast_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_toast_panel.add_child(_toast_label)
	_toast_panel.visible = false


func show_title(has_save: bool) -> void:
	_ensure_built()
	hide_panels()
	_has_save = has_save
	_title.visible = true
	_hud.visible = false
	_current_panel = "title"
	var menu: VBoxContainer = _title.get_node("TitleActions") as VBoxContainer
	_clear(menu)
	var continue_button: Button = _action_button("Continue", "continue")
	continue_button.disabled = not has_save
	continue_button.custom_minimum_size.y = 36
	continue_button.add_theme_font_size_override("font_size", 20)
	menu.add_child(continue_button)
	var new_button: Button = _button("New Game", _request_new_game)
	new_button.custom_minimum_size.y = 36
	new_button.add_theme_font_size_override("font_size", 20)
	menu.add_child(new_button)
	for item: Array in [["Settings", "settings"], ["Credits", "credits"]]:
		var button: Button = _action_button(str(item[0]), str(item[1]))
		button.custom_minimum_size.y = 36
		button.add_theme_font_size_override("font_size", 20)
		menu.add_child(button)
	if not OS.has_feature("web"):
		var quit_button: Button = _action_button("Quit", "quit")
		quit_button.custom_minimum_size.y = 36
		quit_button.add_theme_font_size_override("font_size", 20)
		menu.add_child(quit_button)
	_focus(continue_button if has_save else new_button)


func _request_new_game() -> void:
	if not _has_save:
		action_requested.emit("new_game")
		return
	var box: VBoxContainer = _card("Begin again?", 650)
	box.add_child(_body("Starting a new story replaces your current chapter. Your sound and comfort settings will stay."))
	var keep: Button = _button("Keep my story", func() -> void: show_title(true))
	box.add_child(keep)
	box.add_child(_action_button("Start a new story", "new_game"))
	_focus(keep)
	_current_panel = "confirm_new"


func set_hud(objective: String, mode_text: String, prompt: String, room_label: String) -> void:
	_ensure_built()
	_objective.text = objective
	_mode.text = mode_text
	var almost: bool = mode_text.to_lower().contains("almost")
	_mode.add_theme_color_override("font_color", MINT if almost else PAPER)
	_mode_icon.texture = _texture("icon_moon.png" if almost else "icon_sun.png")
	_room.text = room_label
	_prompt.text = prompt
	_prompt_panel.visible = not prompt.is_empty() and not _dialogue.visible


func show_dialogue(speaker: String, text: String, choices: Array = [], portrait: int = 0) -> void:
	_ensure_built()
	_title.visible = false
	_modal.visible = false
	_hud.visible = true
	_dialogue.visible = true
	_prompt_panel.visible = false
	_dialogue_choices = choices.duplicate(true)
	_current_panel = "dialogue"
	_clear(_dialogue_content)
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 22)
	_dialogue_content.add_child(row)
	if speaker.to_lower() == "fig":
		var portrait_box := Control.new()
		portrait_box.custom_minimum_size = Vector2(128, 128)
		portrait_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
		row.add_child(portrait_box)
		var frame := TextureRect.new()
		frame.texture = _texture("portrait_frame.png")
		frame.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		frame.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		_full(frame, portrait_box)
		frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
		var face := TextureRect.new()
		var atlas := AtlasTexture.new()
		atlas.atlas = _texture("fig_portraits.png")
		atlas.region = Rect2(clampi(portrait, 0, 2) * 64, 0, 64, 64)
		face.texture = atlas
		face.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		face.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		portrait_box.add_child(face)
		face.position = Vector2(13, 13)
		face.size = Vector2(102, 102)
		face.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var words := VBoxContainer.new()
	words.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	words.add_theme_constant_override("separation", 6)
	row.add_child(words)
	words.add_child(_label(speaker, 26, AMBER, true))
	words.add_child(_body(text))
	var actions := HBoxContainer.new()
	actions.add_theme_constant_override("separation", 12)
	words.add_child(actions)
	var first: Button = null
	if choices.is_empty():
		_dialogue_continue = _button("Continue  ·  E / Enter", func() -> void: dialogue_advanced.emit())
		actions.add_child(_dialogue_continue)
		first = _dialogue_continue
	else:
		for value: Variant in choices:
			var choice: Dictionary = value as Dictionary
			var id: String = str(choice.get("id", ""))
			var choice_text: String = str(choice.get("text", id))
			var button: Button = _button(choice_text, func() -> void: choice_selected.emit(id))
			button.add_theme_font_size_override("font_size", mini(_font_size, 22))
			actions.add_child(button)
			if first == null:
				first = button
	if first != null:
		_focus(first)


func close_dialogue() -> void:
	_ensure_built()
	_dialogue.visible = false
	_dialogue_choices.clear()
	_current_panel = ""
	get_viewport().gui_release_focus()


func _card(title: String, width: float = 720.0) -> VBoxContainer:
	_ensure_built()
	_modal.visible = true
	_dialogue.visible = false
	_clear(_modal_center)
	var panel := PanelContainer.new()
	panel.custom_minimum_size.x = width
	_modal_center.add_child(panel)
	var margin := MarginContainer.new()
	for side: String in ["left", "right", "top", "bottom"]:
		margin.add_theme_constant_override("margin_" + side, 16)
	panel.add_child(margin)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 16)
	margin.add_child(box)
	box.add_child(_label(title, 30, PAPER, true))
	return box


func show_pause() -> void:
	var box: VBoxContainer = _card("Take a breath", 570)
	box.add_child(_body("Tomorrow can wait a little longer.", 20, MOON))
	var resume: Button = _action_button("Resume", "resume")
	box.add_child(resume)
	box.add_child(_action_button("Notebook & inventory", "notebook"))
	box.add_child(_action_button("Settings", "settings"))
	box.add_child(_action_button("Save & return to title", "title"))
	_focus(resume)
	_current_panel = "pause"


func show_notebook(clues: Array, items: Array, objective: String, hint: String) -> void:
	var box: VBoxContainer = _card("The Visitor’s notebook", 970)
	_current_panel = "notebook"
	var objective_label: Label = _body(objective, _font_size, AMBER)
	box.add_child(objective_label)
	var columns := HBoxContainer.new()
	columns.add_theme_constant_override("separation", 26)
	box.add_child(columns)
	var notes := VBoxContainer.new()
	notes.custom_minimum_size = Vector2(540, 0)
	notes.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	notes.add_theme_constant_override("separation", 12)
	columns.add_child(notes)
	notes.add_child(_label("Clues", 24, BLUSH, true))
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size = Vector2(0, 180)
	scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	notes.add_child(scroll)
	var entries := VBoxContainer.new()
	entries.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	entries.add_theme_constant_override("separation", 12)
	scroll.add_child(entries)
	if clues.is_empty():
		entries.add_child(_body("Nothing certain yet. Inspect the letter and speak to Fig.", 20, MOON))
	else:
		for clue: Variant in clues:
			var clue_text: String = str(clue)
			if clue is Dictionary:
				var clue_data: Dictionary = clue as Dictionary
				clue_text = str(clue_data.get("text", clue_data.get("title", "")))
			entries.add_child(_body("• " + clue_text, mini(_font_size, 22)))
	if not hint.is_empty():
		notes.add_child(_body("Fig’s advice: " + hint, 19, MINT))
	var inventory := VBoxContainer.new()
	inventory.custom_minimum_size.x = 280
	inventory.add_theme_constant_override("separation", 10)
	columns.add_child(inventory)
	inventory.add_child(_label("Inventory", 24, BLUSH, true))
	if items.is_empty():
		inventory.add_child(_body("Just a curious mind.", 20, MOON))
	else:
		for item: Variant in items:
			var item_text: String = str(item)
			var icon_name: String = "icon_letter.png"
			if item is Dictionary:
				var item_data: Dictionary = item as Dictionary
				item_text = str(item_data.get("name", item_data.get("text", "")))
				icon_name = str(item_data.get("icon", "icon_letter.png"))
			elif item_text.to_lower().contains("mirror"):
				icon_name = "icon_mirror.png"
			var item_row := HBoxContainer.new()
			item_row.add_theme_constant_override("separation", 10)
			inventory.add_child(item_row)
			var icon := TextureRect.new()
			icon.texture = _texture(icon_name)
			icon.custom_minimum_size = Vector2(48, 48)
			icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
			icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
			icon.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
			item_row.add_child(icon)
			item_row.add_child(_body(item_text, 20))
	var actions := HBoxContainer.new()
	actions.add_theme_constant_override("separation", 16)
	box.add_child(actions)
	var close: Button = _action_button("Close notebook", "resume")
	actions.add_child(close)
	actions.add_child(_action_button("Ask Fig for a hint", "hint"))
	_focus(close)


func show_settings(settings: Dictionary) -> void:
	apply_settings(settings)
	var box: VBoxContainer = _card("Make yourself comfortable", 720)
	_current_panel = "settings"
	var first: HSlider = null
	for item: Array in [["Master volume", "master_volume", 1.0], ["Music", "music_volume", 0.35], ["Effects", "sfx_volume", 0.7]]:
		var key: String = str(item[1])
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation", 22)
		box.add_child(row)
		var title_label: Label = _label(str(item[0]), 21)
		title_label.custom_minimum_size.x = 200
		row.add_child(title_label)
		var slider := HSlider.new()
		slider.min_value = 0.0
		slider.max_value = 1.0
		slider.step = 0.05
		slider.value = float(settings.get(key, item[2]))
		slider.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		slider.custom_minimum_size = Vector2(270, 38)
		slider.focus_mode = Control.FOCUS_ALL
		row.add_child(slider)
		var amount: Label = _label("%d%%" % roundi(slider.value * 100.0), 18, MOON)
		amount.custom_minimum_size.x = 62
		row.add_child(amount)
		slider.value_changed.connect(func(value: float) -> void:
			amount.text = "%d%%" % roundi(value * 100.0)
			setting_changed.emit(key, value)
		)
		if first == null:
			first = slider
	var motion := CheckBox.new()
	motion.text = "Reduced motion"
	motion.button_pressed = bool(settings.get("reduced_motion", false))
	motion.custom_minimum_size.y = 42
	box.add_child(motion)
	motion.toggled.connect(func(value: bool) -> void: setting_changed.emit("reduced_motion", value))
	var size_row := HBoxContainer.new()
	size_row.add_theme_constant_override("separation", 16)
	box.add_child(size_row)
	size_row.add_child(_label("Reading size", 21))
	var standard: Button = _button("Standard", func() -> void:
		_font_size = 22
		setting_changed.emit("text_size", 22)
	)
	size_row.add_child(standard)
	var large: Button = _button("Large", func() -> void:
		_font_size = 26
		setting_changed.emit("text_size", 26)
	)
	size_row.add_child(large)
	box.add_child(_body("Dialogue stays on screen until you continue. Use arrow keys to adjust a focused slider.", 18, MOON))
	box.add_child(_action_button("Back", "back"))
	if first != null:
		_focus(first)


func apply_settings(settings: Dictionary) -> void:
	_ensure_built()
	_font_size = 26 if int(settings.get("text_size", 22)) >= 26 else 22
	theme.default_font_size = _font_size


func show_credits() -> void:
	var box: VBoxContainer = _card("The household ledger", 760)
	_current_panel = "credits"
	box.add_child(_body("The House That Ate Tomorrow", 26, BLUSH))
	box.add_child(_body("Original pixel artwork, interface and implementation created with Codex for this project. Mansion title illustration generated with OpenAI ImageGen.", 21))
	box.add_child(_body("Lettering uses DejaVu fonts. Copyright and license notices are included with the project. No third-party game sprite packs are used.", 20, MOON))
	box.add_child(_body("This first chapter follows the supplied story and puzzle design: a house of unfinished possibilities, and a cat who is definitely upper management.", 20))
	var back: Button = _action_button("Back", "back")
	box.add_child(back)
	_focus(back)


func show_completion() -> void:
	var box: VBoxContainer = _card("Tomorrow is still missing.", 760)
	_current_panel = "completion"
	box.add_child(_body("The Guestbook accepts you. The house has a witness.", 24, AMBER))
	box.add_child(_body("But the notice is clear: the Department of Unfinished Things plans to close this home next tomorrow. Someone here knows why the clocks have stopped.", 22))
	box.add_child(_body("You have reached the end of this playable chapter. Your progress is saved; the hall remains yours to explore.", 20, MOON))
	var explore: Button = _action_button("Continue exploring", "resume")
	box.add_child(explore)
	box.add_child(_action_button("Return to title", "title"))
	_focus(explore)


func toast(text: String) -> void:
	_ensure_built()
	_toast_label.text = text
	_toast_remaining = 3.6
	_toast_panel.visible = true


func hide_panels() -> void:
	_ensure_built()
	_title.visible = false
	_modal.visible = false
	_dialogue.visible = false
	_dialogue_choices.clear()
	_hud.visible = true
	_current_panel = ""
	get_viewport().gui_release_focus()


func is_modal() -> bool:
	return _built and (_title.visible or _modal.visible or _dialogue.visible)


func panel_name() -> String:
	return _current_panel
