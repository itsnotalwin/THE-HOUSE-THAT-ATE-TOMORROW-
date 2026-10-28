# Original slice audio

Composed and synthesized for this project by Codex on 27 October 2026. The motifs, instrument spectra, envelopes and rain synthesis are original; no recordings, sample packs or existing songs were copied.

Source: `../tools/make_audio.py` (Python 3 and numpy). All exports are mono 22,050 Hz, signed 16-bit PCM WAV. The generator is deterministic. No blanket public distribution license is assigned.

Here uses sparse felt-piano-like chords; Almost uses the same harmonic pacing with longer, quieter bell tails. Rain is seeded circularly filtered noise. The short cues support inspection, shifting, success, a notice and focus; none carries information that is absent from the visual interface.

## Measured export checks

| File | Duration | Loop | Peak dBFS | RMS dBFS | Loop endpoint jump |
| --- | ---: | --- | ---: | ---: | ---: |
| `audio_here.wav` | 24.00s | yes | -13.74 | -26.62 | 0.001373 |
| `audio_almost.wav` | 24.00s | yes | -14.10 | -26.13 | 0.000122 |
| `audio_rain.wav` | 8.00s | yes | -23.08 | -37.23 | 0.000000 |
| `audio_inspect.wav` | 0.55s | no | -17.00 | -23.02 | 0.000000 |
| `audio_toggle.wav` | 1.40s | no | -12.77 | -23.20 | 0.000000 |
| `audio_success.wav` | 2.00s | no | -12.77 | -24.68 | 0.000000 |
| `audio_notice.wav` | 0.90s | no | -14.89 | -22.93 | 0.000000 |
| `audio_focus.wav` | 0.16s | no | -25.32 | -33.78 | 0.000000 |

Total WAV size: 2,690,894 bytes. All headers and frame counts decode correctly; no PCM clipping; every loop boundary jump is below 0.015 full scale. The music uses circular note tails; rain uses an 8ms endpoint taper. These numerical checks do not replace listening in the eventual build.

## Runtime behavior

`../scripts/audio.gd` keeps both musical loops aligned and crossfades between them. Repeated context updates do not restart tracks. Ambient rain rises on the street and stays very quiet indoors. Master/music/SFX sliders are respected; zero mutes and pauses the corresponding players. Playback begins on the first non-title context, after the player starts or continues the game. Browser autoplay still depends on the browser accepting that user gesture.

## Checksums

- `68a736f73b931fdb5e7c743ab708fe6cba490533464ab64e9bf715d10794d176` — `audio_here.wav`
- `721594f99831aca463c7fb50c74666920e9e44801104898be83cd6dab5e412a1` — `audio_almost.wav`
- `9c917ee15292d6cecf576a14792a40dad220844bc6fefb036650bd5080e618a8` — `audio_rain.wav`
- `60f4719c4e9a4bfbd346f15fb896f9bad70408f2e6180fc030a7c88c5290ea84` — `audio_inspect.wav`
- `1ed5a838aa68040f3b10aa619e68ea1dd597be1966288596d46b74fa9369a981` — `audio_toggle.wav`
- `e704d5dac8c4bc5de6efb7560ebd089522810681f2d90c2ad399a022c50ebf1c` — `audio_success.wav`
- `6ff8e226fffa149d44aa08a0935ae88276d3501880bab264a0f6e00764e71cbf` — `audio_notice.wav`
- `1aa66f7316dace40b7d296fb38c5698f77ba80e667b6b21d33550ccae121b504` — `audio_focus.wav`
