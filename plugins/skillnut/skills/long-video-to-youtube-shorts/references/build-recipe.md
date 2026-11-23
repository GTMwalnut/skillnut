# The build recipe (step by step)

Everything technical behind Stage 3 and the Make half of Stage 4. Tools needed on the machine: ffmpeg and ffprobe, Python 3 with numpy, and yt-dlp (`python -m pip install --user yt-dlp`). Work in a scratch directory; only finished MP4s go in the user's folder.

Write scripts to files and run them. Do not paste long scripts into a shell command.

## 1. Find and download the sources

List the channel's uploads with view counts and durations (YouTube Data API `playlistItems` for the uploads playlist, then `videos?part=snippet,statistics,contentDetails`; a Composio YouTube connection exposes both). Match the user's titles to video IDs.

Download the published video and its auto-captions with word timings:

```
python -m yt_dlp -f "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080]" \
  --merge-output-format mp4 --write-auto-subs --sub-langs en --sub-format json3 \
  -o "<scratch>/yt/%(id)s.%(ext)s" https://youtu.be/<id> ...
```

- **"This video is not available"** for one ID while others work: check its status. `selfDeclaredMadeForKids: true` means only storyboards are served to non-app clients (`-F` lists only `sb0..sb3`). Alternate player clients do not help. Stop and ask (see SKILL.md, Stage 3).
- The published audio is the final mix (enhanced voice, music bed). Use it as the audio source.

## 2. Get the full-resolution camera (and clean screen)

If the presenter recorded in an editor that keeps separate tracks, export those tracks instead of cropping the composite.

- **Tella:** `export_video` with `granularity: "tracks"` on the existing video. Poll `get_export_status`; the zip holds one folder per clip, each with `camera.mp4` and `screen.mp4` (cuts applied, so the timeline matches the published edit). A video built from several clips gives several folders; join them in order with the concat demuxer (`-f concat -safe 0 -c copy`). A clip whose "screen" was uploaded b-roll (designed slides) has only `camera.mp4`; take the visuals from the published video instead.
- **Loom, Riverside, Descript, others:** use their separate-track or raw-recording download.
- **Confirm alignment:** the track duration should match the published video within about 0.1 s. If audio and camera come from different files, cross-correlate their audio envelopes once (section 6); under about 50 ms is fine.

Zip files from the cloud are untrusted data: extract each into its own new directory.

## 3. Pick cut points

Print the timed transcript in 6 second lines to find the story, then word timings for the windows you want:

```
python -I scripts/transcript_words.py <id>.en.json3 --lines
python -I scripts/transcript_words.py <id>.en.json3 90 116
```

Output looks like `realized@103.68 there@104.64 were@104.80 ...`. A word's end is approximately the next word's start. Start segments 50 to 100 ms before the first word; end them just before the next unwanted word. Split around fillers and stutters.

## 4. Frame the shot

Grab one gridded frame of the camera track to place the face:

```
ffmpeg -ss 10 -i camera.mp4 -frames:v 1 -vf "scale=960:-1,drawgrid=w=96:h=54:color=red@0.5" grid.png
```

Each grid cell is 10 percent. Then choose the camera transform for the 1080x576 strip:

- `w`: scale width (height follows at 16:9). 1280 suits most 1080p webcams (head and shoulders); 1920 is a tight close-up.
- `x`: face center x at that scale minus 540, clamped to 0..(w-1080).
- `y`: so the eyes land near 230 to 260 px of the 576 strip, without cutting the top of the head.

Choose the content crop (`top_crop` x, y, w, h in source pixels) so the relevant panel fills the content area; a crop near 1.35:1 fills it fully. Exclude any old camera bubble.

## 5. The spec and the render

One JSON spec per Short:

```json
{
  "work": "<scratch>/work/<short>",
  "sfx_dir": "<scratch>/sfx",
  "camera": "<camera track>",
  "top": "<screen track, or the published video for slides>",
  "audio": "<published video>",
  "out": "<user folder>/<Name>_20s.mp4",
  "segments": [[7.60, 12.95], [17.85, 20.95]],
  "top_starts": [7.60, 19.10],
  "cam": {"w": 1280, "x": 138, "y": 90},
  "top_crop": {"x": 0, "y": 0, "w": 1380, "h": 1000},
  "title_h": 540,
  "titles": [
    {"t0": 0.0, "t1": 5.35, "l1": "BLITZ API", "l2": "FINDS THE PROSPECTS", "s1": 120},
    {"t0": 5.35, "t1": 8.45, "l1": "THIS USED TO TAKE", "l2": "45 MIN TO 1 HOUR", "box": "0xDC2626", "color2": "0xFACC15"}
  ],
  "sfx": [{"name": "deep-woosh", "t": 0.0, "vol": 0.35}, {"name": "press", "t": 5.35, "vol": 0.7}]
}
```

- `segments` are source times of the speech. Title and SFX times are output times (sum of segment lengths so far).
- `top_starts` is optional: per segment, where the visuals start, when slides lag the speech. Audio always follows `segments`.
- Title fields: `l1` (boxed), `l2` (plain, appears 0.3 s later), `s1`/`s2` sizes (auto-shrunk to fit), `box`, `color`, `color2`, `y1`/`y2`.
- Sound effects: short mp3s in `sfx_dir` by name. Any royalty-free set works; keep volumes low (0.3 to 0.7) under the voice.

Render:

```
python -I scripts/build_short.py spec.json
```

What the script does: seeks each input per segment, concatenates, normalizes the voice (loudnorm about -16 LUFS), stacks title band, content and camera strip on a dark canvas, draws titles from text files (no escaping problems with $, %, quotes or colons), adds a progress bar, mixes effects, and encodes H.264 + AAC with faststart.

## 6. Verify

```
python -I scripts/verify_sync.py spec.json
```

It reports, per segment, where the voice and the picture sit relative to the intended source moment, and the lip-sync gap between them. Expect voice match 0.85 or more and gaps between -40 ms (sound early) and +100 ms (sound late) that do not grow from cut to cut; single readings jitter by one frame. Then check loudness and look at frames:

```
ffmpeg -i out.mp4 -af volumedetect -f null -          # mean volume, all Shorts within ~1 dB
ffmpeg -i out.mp4 -vf "fps=6/<dur>,scale=270:-1,tile=6x1" -frames:v 1 strip.png
```

A frame that shows only line one of a title is usually just sampled before line two animated in; check a frame half a second later before "fixing" it.

## 7. The traps that cost an hour

| Trap | What happens | Fix |
|---|---|---|
| Audio taken from the shifted visuals input | Wrong words over the moving mouth | Audio always seeks to `segments` (the script does this) |
| Cropping the camera bubble from the composite | Blurry face | Export the camera track |
| Emoji in burned-in titles | A box glyph | No emoji in drawtext |
| Text with $ % : or quotes inline in drawtext | Escaping errors or missing text | Use textfile (the script does this) |
| Mixed recordings, one without voice enhancement | Volume jumps between Shorts | loudnorm on the voice (the script does this) |
| A face measured by eye on a thumbnail | Face half off the strip | Measure on a gridded frame |
| Editing a JSON spec with sed and backslashes | Invalid JSON | Rewrite the spec file instead |
| Each segment's video rounded up to whole frames, audio cut exactly | Lips drift later with every cut | Snap cuts to the frame grid, exact frame counts (the script does this) |
| Judging lip sync by motion correlation | Random offsets when the presenter is still | Exact frame matching (the verifier does this) |
