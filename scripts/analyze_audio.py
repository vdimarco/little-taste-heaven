#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import librosa
import numpy as np


def summarize_window(values, times, start, end):
    mask = (times >= start) & (times < end)
    if not np.any(mask):
        return 0.0
    return float(np.mean(values[mask]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("audio")
    parser.add_argument("--out", default="analysis/features.json")
    args = parser.parse_args()

    audio_path = Path(args.audio)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    y, sr = librosa.load(audio_path, sr=None, mono=True)

    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    onset = librosa.onset.onset_strength(y=y, sr=sr)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

    onset_times = librosa.times_like(onset, sr=sr)
    centroid_times = librosa.times_like(centroid, sr=sr)
    chroma_times = librosa.times_like(chroma, sr=sr)

    pitch_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    windows = {
        "keyboard_before": [56.0, 58.0],
        "keyboard_after": [58.0, 60.0],
        "vocal_entry": [80.0, 83.0],
        "heaven_pivot": [151.8, 157.3],
    }

    result = {
        "sample_rate": sr,
        "duration": float(len(y) / sr),
        "tempo_bpm": float(np.atleast_1d(tempo)[0]),
        "landmarks": {
            "keyboard_turn": 58.0,
            "instrumental_boundary": 62.229,
            "first_vocal": 80.66,
            "heaven_pivot": 152.0,
        },
        "windows": {},
    }

    for name, (start, end) in windows.items():
        chroma_mask = (chroma_times >= start) & (chroma_times < end)
        pitch_energy = np.mean(chroma[:, chroma_mask], axis=1) if np.any(chroma_mask) else np.zeros(12)
        ranked = np.argsort(pitch_energy)[::-1]
        result["windows"][name] = {
            "start": start,
            "end": end,
            "onset_strength": summarize_window(onset, onset_times, start, end),
            "spectral_centroid_hz": summarize_window(centroid, centroid_times, start, end),
            "pitch_classes": [
                {"note": pitch_names[int(i)], "strength": float(pitch_energy[i])}
                for i in ranked[:6]
            ],
        }

    out_path.write_text(json.dumps(result, indent=2))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
