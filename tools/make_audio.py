#!/usr/bin/env python3
"""Compose and render original quiet slice audio; no external samples.

Requires Python 3 and numpy. The motif, envelopes, harmonic spectra and rain
are authored here. Circular note tails preserve continuity across music loops.
All exports are mono 22,050 Hz signed 16-bit PCM WAV files.
"""
from pathlib import Path
import hashlib
import math
import wave

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
RATE = 22050
TAU = math.tau
REPORT = []


def frequency(midi):
    return 440.0 * 2.0 ** ((midi - 69) / 12.0)


def note(midi, seconds=3.8, spectral=False):
    time = np.arange(round(seconds * RATE), dtype=np.float64) / RATE
    fundamental = frequency(midi)
    # Soft struck metal / felt piano: quick rounded attack, long quiet decay.
    attack = 1.0 - np.exp(-time / (0.018 if spectral else 0.008))
    decay = np.exp(-time / (1.25 if spectral else 0.85))
    release = np.minimum(1.0, np.maximum(0.0, (seconds - time) / 0.22)) ** 2
    partials = [(1.0, 1.0), (2.0, 0.17), (3.0, 0.07), (4.0, 0.025)]
    if spectral:
        partials = [(1.0, 0.88), (2.0, 0.12), (3.0, 0.10), (5.0, 0.035)]
    sound = np.zeros(time.shape, dtype=np.float64)
    for multiple, amount in partials:
        partial_decay = np.exp(-time * (multiple - 1.0) * 0.22)
        sound += amount * partial_decay * np.sin(TAU * fundamental * multiple * time)
    return sound * attack * decay * release


def add(sound, voice, start, amplitude, circular=False):
    first = round(start * RATE)
    if circular:
        indices = (np.arange(len(voice)) + first) % len(sound)
        np.add.at(sound, indices, voice * amplitude)
    elif first < len(sound):
        size = min(len(voice), len(sound) - first)
        sound[first:first + size] += voice[:size] * amplitude


def music(spectral=False):
    sound = np.zeros(24 * RATE, dtype=np.float64)
    # Eight quiet three-second chords; an original D-minor/add-nine miniature.
    roots = [50, 53, 48, 45, 50, 58, 53, 45]
    chords = [(62, 65, 69, 76), (65, 69, 72, 74), (60, 64, 67, 74), (57, 62, 64, 69),
              (62, 65, 69, 74), (62, 65, 70, 74), (60, 65, 69, 72), (57, 61, 64, 69)]
    for bar, (root, chord) in enumerate(zip(roots, chords)):
        offset = bar * 3.0
        add(sound, note(root, 4.8, spectral), offset, 0.12, True)
        for index, pitch in enumerate(chord):
            # Leave space between gestures; no constant busy arpeggiator.
            onset = offset + [0.12, 0.88, 1.52, 2.34][index]
            add(sound, note(pitch + (12 if spectral and index == 3 else 0),
                            4.8 if spectral else 3.4, spectral),
                onset, [0.085, 0.055, 0.07, 0.04][index], True)
    # Barely audible periodic room-tone harmonics, with exact loop frequencies.
    time = np.arange(len(sound), dtype=np.float64) / RATE
    for cycle, amplitude in [(1468, 0.0035), (2202, 0.002), (2936, 0.001)]:
        sound += amplitude * np.sin(TAU * cycle * time / 24.0)
    sound -= np.mean(sound)
    return sound


def rain():
    rng = np.random.default_rng(31159)
    length = 8 * RATE
    raw = rng.normal(0.0, 1.0, length)
    # Circular moving-average filters keep the continuous noise field seamless.
    soft = sum(np.roll(raw, shift) for shift in range(16)) / 16.0
    middle = sum(np.roll(raw, shift) for shift in range(4)) / 4.0
    time = np.arange(length, dtype=np.float64) / RATE
    amplitude = 0.052 + 0.006 * np.sin(TAU * time / 8.0)
    sound = (soft * 0.8 + middle * 0.2) * amplitude
    for onset in [0.32, 1.78, 2.55, 3.91, 5.12, 6.64, 7.25]:
        drop = note(int(rng.integers(79, 89)), 0.11, True)
        add(sound, drop, onset, 0.0035, True)
    # A tiny endpoint taper suppresses the one residual noise discontinuity.
    fade = round(0.008 * RATE)
    ramp = np.linspace(0.0, 1.0, fade)
    sound[:fade] *= ramp
    sound[-fade:] *= ramp[::-1]
    return sound


def cue(pitches, starts, duration, spectral=False):
    sound = np.zeros(round(duration * RATE), dtype=np.float64)
    for pitch, start in zip(pitches, starts):
        add(sound, note(pitch, min(1.5, duration - start), spectral), start, 0.15)
    tail = min(round(RATE * 0.06), len(sound))
    sound[-tail:] *= np.linspace(1.0, 0.0, tail) ** 2
    return sound


def export(name, sound, loop=False, target_peak=0.23):
    peak = float(np.max(np.abs(sound)))
    if peak > target_peak:
        sound = sound * (target_peak / peak)
    pcm = np.round(np.clip(sound, -1.0, 1.0) * 32767).astype('<i2')
    path = OUT / ("audio_" + name + ".wav")
    with wave.open(str(path), 'wb') as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(RATE)
        output.writeframes(pcm.tobytes())
    decoded = pcm.astype(np.float64) / 32767.0
    rms = float(np.sqrt(np.mean(decoded ** 2)))
    jump = float(abs(decoded[0] - decoded[-1]))
    assert np.max(np.abs(pcm.astype(np.int32))) < 32767, name + ': clipped'
    assert not loop or jump < 0.015, name + ': excessive loop seam'
    assert 0.0 < rms < 0.15, name + ': missing or excessively loud signal'
    with wave.open(str(path), 'rb') as source:
        assert source.getnchannels() == 1 and source.getsampwidth() == 2
        assert source.getframerate() == RATE and source.getnframes() == len(pcm)
    REPORT.append({
        'name': path.name, 'seconds': len(pcm) / RATE, 'loop': loop,
        'peak_dbfs': 20 * math.log10(max(float(np.max(np.abs(decoded))), 1e-12)),
        'rms_dbfs': 20 * math.log10(max(rms, 1e-12)), 'seam': jump,
        'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()
    })


def main():
    OUT.mkdir(exist_ok=True)
    export('here', music(False), True)
    export('almost', music(True), True)
    export('rain', rain(), True, 0.12)
    export('inspect', cue([74], [0], 0.55), target_peak=0.17)
    export('toggle', cue([62, 69, 76], [0, 0.13, 0.26], 1.4, True))
    export('success', cue([62, 65, 69, 74], [0, 0.16, 0.32, 0.56], 2.0))
    export('notice', cue([57, 58], [0, 0.22], 0.9, True), target_peak=0.18)
    export('focus', cue([81], [0], 0.16), target_peak=0.07)
    total = sum(item['bytes'] for item in REPORT)
    assert total < 8 * 1024 * 1024
    lines = [
        '# Original slice audio', '',
        'Composed and synthesized for this project by Codex on 27 October 2026. '
        'The motifs, instrument spectra, envelopes and rain synthesis are original; '
        'no recordings, sample packs or existing songs were copied.', '',
        'Source: `../tools/make_audio.py` (Python 3 and numpy). '
        'All exports are mono 22,050 Hz, signed 16-bit PCM WAV. '
        'The generator is deterministic. No blanket public distribution license is assigned.', '',
        'Here uses sparse felt-piano-like chords; Almost uses the same harmonic pacing '
        'with longer, quieter bell tails. Rain is seeded circularly filtered noise. '
        'The short cues support inspection, shifting, success, a notice and focus; '
        'none carries information that is absent from the visual interface.', '',
        '## Measured export checks', '',
        '| File | Duration | Loop | Peak dBFS | RMS dBFS | Loop endpoint jump |',
        '| --- | ---: | --- | ---: | ---: | ---: |'
    ]
    for item in REPORT:
        lines.append(f"| `{item['name']}` | {item['seconds']:.2f}s | {'yes' if item['loop'] else 'no'} | "
                     f"{item['peak_dbfs']:.2f} | {item['rms_dbfs']:.2f} | {item['seam']:.6f} |")
    lines += ['', f'Total WAV size: {total:,} bytes. All headers and frame counts decode correctly; '
              'no PCM clipping; every loop boundary jump is below 0.015 full scale. '
              'The music uses circular note tails; rain uses an 8ms endpoint taper. '
              'These numerical checks do not replace listening in the eventual build.', '',
              '## Runtime behavior', '',
              '`../scripts/audio.gd` keeps both musical loops aligned and crossfades between them. '
              'Repeated context updates do not restart tracks. Ambient rain rises on the street '
              'and stays very quiet indoors. Master/music/SFX sliders are respected; zero mutes '
              'and pauses the corresponding players. Playback begins on the first non-title '
              'context, after the player starts or continues the game. Browser autoplay '
              'still depends on the browser accepting that user gesture.', '',
              '## Checksums', '']
    lines += [f"- `{item['sha256']}` — `{item['name']}`" for item in REPORT]
    (OUT / 'AUDIO_PROVENANCE.md').write_text('\n'.join(lines) + '\n')
    print(f'Exported and checked {len(REPORT)} original WAV files ({total:,} bytes).')
    for item in REPORT:
        print(f"{item['name']}: {item['seconds']:.2f}s, {item['peak_dbfs']:.1f}dBFS peak, seam {item['seam']:.6f}")


if __name__ == '__main__':
    main()
