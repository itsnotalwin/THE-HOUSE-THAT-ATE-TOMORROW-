class_name SliceAudio
extends Node
## Original procedural music, room ambience and cues. No GameState dependency.

const CUE_FILES: Dictionary = {
	"inspect": "res://assets/audio_inspect.wav",
	"interact": "res://assets/audio_inspect.wav",
	"toggle": "res://assets/audio_toggle.wav",
	"success": "res://assets/audio_success.wav",
	"notice": "res://assets/audio_notice.wav",
	"focus": "res://assets/audio_focus.wav",
}

var master_volume: float = 1.0
var music_volume: float = 0.35
var sfx_volume: float = 0.7
var _here: AudioStreamPlayer
var _almost: AudioStreamPlayer
var _rain: AudioStreamPlayer
var _cues: Array[AudioStreamPlayer] = []
var _cue_cache: Dictionary = {}
var _cue_index: int = 0
var _started: bool = false
var _almost_mix: float = 0.0
var _rain_mix: float = 0.0
var _fade: Tween
var _context: String = ""


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_here = _make_loop("res://assets/audio_here.wav")
	_almost = _make_loop("res://assets/audio_almost.wav")
	_rain = _make_loop("res://assets/audio_rain.wav")
	for index in range(4):
		var player := AudioStreamPlayer.new()
		player.name = "Cue%d" % index
		add_child(player)
		_cues.append(player)
	for cue_name: String in CUE_FILES:
		var path: String = CUE_FILES[cue_name]
		_cue_cache[cue_name] = load(path) as AudioStream
	_apply_levels()


func _make_loop(path: String) -> AudioStreamPlayer:
	var player := AudioStreamPlayer.new()
	var original := load(path) as AudioStreamWAV
	if original != null:
		var stream := original.duplicate() as AudioStreamWAV
		stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
		stream.loop_begin = 0
		stream.loop_end = int(round(stream.get_length() * stream.mix_rate))
		player.stream = stream
	add_child(player)
	return player


func apply_settings(settings: Dictionary) -> void:
	master_volume = _setting(settings, "master_volume", master_volume)
	music_volume = _setting(settings, "music_volume", music_volume)
	sfx_volume = _setting(settings, "sfx_volume", sfx_volume)
	_apply_levels()


func _setting(settings: Dictionary, key: String, fallback: float) -> float:
	var value: Variant = settings.get(key, fallback)
	if value is float or value is int:
		var number: float = float(value)
		if is_finite(number):
			return clampf(number, 0.0, 1.0)
	return fallback


func set_context(room: String, almost: bool, on_title: bool = false) -> void:
	if not is_node_ready():
		return
	# The initial title stays silent. Starting/continuing is the first gesture.
	if not _started and on_title:
		return
	if not _started:
		_started = true
		_here.play()
		_almost.play()
		_rain.play()
	var key: String = "%s:%s:%s" % [room, almost, on_title]
	if key == _context:
		return
	_context = key
	var target_almost: float = 1.0 if almost and not on_title else 0.0
	var target_rain: float = 1.0 if room == "street" and not on_title else 0.08
	if _fade != null and _fade.is_valid():
		_fade.kill()
	_fade = create_tween().set_parallel(true)
	_fade.tween_method(_set_almost_mix, _almost_mix, target_almost, 0.9)
	_fade.tween_method(_set_rain_mix, _rain_mix, target_rain, 1.2)
	_apply_levels()


func _set_almost_mix(value: float) -> void:
	_almost_mix = value
	_apply_levels()


func _set_rain_mix(value: float) -> void:
	_rain_mix = value
	_apply_levels()


func _set_gain(player: AudioStreamPlayer, gain: float, muted: bool) -> void:
	if player == null:
		return
	player.volume_db = linear_to_db(maxf(gain, 0.00001))
	player.stream_paused = muted


func _apply_levels() -> void:
	var music_gain: float = master_volume * music_volume
	var music_muted: bool = music_gain <= 0.0
	_set_gain(_here, music_gain * (1.0 - _almost_mix) * 0.8, music_muted)
	_set_gain(_almost, music_gain * _almost_mix * 0.8, music_muted)
	_set_gain(_rain, music_gain * _rain_mix * 0.8, music_muted)
	var cue_gain: float = master_volume * sfx_volume * 0.8
	for player: AudioStreamPlayer in _cues:
		_set_gain(player, cue_gain, cue_gain <= 0.0)


func play_cue(cue_name: String) -> void:
	if not is_node_ready() or _cues.is_empty():
		return
	if master_volume <= 0.0 or sfx_volume <= 0.0:
		return
	if not _cue_cache.has(cue_name):
		return
	var player: AudioStreamPlayer = _cues[_cue_index]
	_cue_index = (_cue_index + 1) % _cues.size()
	player.stop()
	player.stream = _cue_cache[cue_name] as AudioStream
	_set_gain(player, master_volume * sfx_volume * 0.8, false)
	player.play()
