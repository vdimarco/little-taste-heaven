# Little Taste of Heaven Visualizer

An experimental music-visualization project for **Leach - Little Taste of Heaven**.

The goal is to make the recording itself drive the visuals. Audio features such as onset strength, spectral brightness, chroma, section boundaries, and harmony become animation controls for Blender.

## First experiment

Render a 15-second sequence from **2:26 to 2:41**.

The main visual event is **2:32**:
- the sung word "heaven" lands at about 2:32
- the arrangement opens into a wide F# color harmony
- measured pitch classes around the moment include F#, A#, C#, E#, G#, and D#
- the working harmonic interpretation is **F#maj13(add9)**

The visual idea is to let six musical layers separate in space, then bloom into one structure.

## Known timing landmarks

- 0:58 - rapid keyboard texture begins to sharpen
- 1:02.23 - instrumental structural boundary
- 1:20.66 - first vocal entrance: "All you were to me"
- 2:32.00 - "heaven" pivot and harmonic bloom

## Project layout

- `audio/` local source audio, ignored by Git
- `analysis/` extracted JSON/CSV features
- `scripts/analyze_audio.py` audio feature extraction
- `blender/visualize.py` Blender scene driver
- `renders/` local render output, ignored by Git
- `docs/analysis.md` musical findings and design notes

## Setup

1. Put your local FLAC at `audio/little-taste-of-heaven.flac`.
2. Create a Python environment.
3. Install dependencies from `requirements.txt`.
4. Run:

```bash
python scripts/analyze_audio.py audio/little-taste-of-heaven.flac
```

5. Open Blender and run:

```bash
blender --background --python blender/visualize.py
```

The Blender script reads `analysis/features.json`.

## Copyright

The recording is not committed to this repository. Supply a local copy you are authorized to use.
