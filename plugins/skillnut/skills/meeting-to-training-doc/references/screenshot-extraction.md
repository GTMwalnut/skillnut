# Screenshot extraction from a meeting recording (step by step)

The construction manual for turning a screen-share recording into the illustrations in a training document. It assumes a harness with a shell, Python, and file access. Follow it in order.

Requirements: `ffmpeg` and `ffprobe` on PATH, Python with `Pillow`. Check both before promising screenshots.

## 1. Get the file, early

Meeting tools serve media over signed URLs with a short life. Two things to do before anything else:

1. **Read the expiry** out of the URL (an `Expires=` epoch, commonly) and convert it. Tell the user the date.
2. **HEAD the URL** to confirm the video actually exists and note its size (read the status line, `content-type` and `content-length` in the output), then download it to local disk. Never work off the remote URL: every seek re-downloads.

```bash
curl -sI "<signed url>"
curl -sL -o call.mp4 "<signed url>"
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,duration -of default=nw=1 call.mp4
```

Typical notetaker output is 1280x720 at a low frame rate. That is enough: interface text survives a 2x upscale after cropping.

**If there is no video stream, stop here** and tell the user the document will be text-only. Some tools record audio only, and duplicate recordings of the same meeting frequently differ on exactly this.

## 2. Map the session before extracting anything

Do not start pulling full frames at guessed timestamps. Build a cheap visual index first, read it, and only then extract what you need. This one habit is the difference between a twenty-minute job and a two-hour one.

Pull one small frame every fifteen seconds across the period where the screen was shared, then tile them into labelled contact sheets:

```bash
mkdir -p frames sheets shots
for t in $(seq 150 15 1740); do
  ffmpeg -v error -ss $t -i call.mp4 -frames:v 1 -q:v 3 "frames/f_$(printf %04d $t).jpg" -y
done
```

Tile them with Pillow, twenty per sheet, each thumbnail labelled with its timestamp. **Do not use ffmpeg's `drawtext` for the labels**: it needs a fontconfig setup that is frequently absent on Windows and segfaults rather than failing cleanly. Label in Pillow instead.

```python
from PIL import Image, ImageDraw, ImageFont
import glob, os

frames = sorted(glob.glob("frames/f_*.jpg"))
TW, TH, COLS, ROWS, PAD, LBL = 440, 248, 4, 5, 6, 20
F = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 16)
per = COLS * ROWS

for si, batch in enumerate([frames[i:i+per] for i in range(0, len(frames), per)], 1):
    W = COLS*(TW+PAD)+PAD; H = ROWS*(TH+LBL+PAD)+PAD
    sheet = Image.new("RGB", (W, H), (24, 24, 28)); d = ImageDraw.Draw(sheet)
    for i, fp in enumerate(batch):
        sec = int(os.path.basename(fp)[2:6])
        im = Image.open(fp).resize((TW, TH), Image.LANCZOS)
        x = PAD + (i % COLS)*(TW+PAD); y = PAD + (i // COLS)*(TH+LBL+PAD)
        sheet.paste(im, (x, y))
        d.text((x+4, y+TH+2), f"{sec//60:02d}:{sec%60:02d}", fill=(255, 220, 90), font=F)
    sheet.save(f"sheets/sheet_{si:02d}.jpg", quality=88)
```

Now look at the sheets. You are reading for: when the share starts, which screen is up at each point, where dialogs and menus open, and where the presenter's own video or a slide deck is showing instead of the product. Write down the timestamps worth extracting. The transcript gives you the anchors; the sheets tell you whether the anchor second actually shows the thing.

## 3. Find the crop box once

Read one full-resolution frame and locate the shared screen inside it. A meeting client puts the shared content in a window with participant tiles beside it and a control bar below; you want only the shared content.

```bash
ffmpeg -v error -ss 315 -i call.mp4 -frames:v 1 -q:v 2 probe.jpg -y
```

Look at `probe.jpg`, note the pixel bounds of the shared region, and reuse that box for every extraction. In a 1280x720 notetaker recording the shared area is commonly around `(105, 75)` to `(975, 645)`, but measure rather than assume.

Include the browser address bar in the crop when there is one. The URL is free navigation documentation, and it is what lets the training document tell the reader which page each screenshot is of.

## 4. Extract the anchor frames

Take the timestamps from the transcript where the presenter did or named something, adjust them against the contact sheets, and extract at full resolution. Crop, then upscale 2x with LANCZOS so interface text stays crisp when placed in a document.

```python
import subprocess, os
from PIL import Image

CROP, SCALE = (105, 75, 975, 645), 2
SHOTS = [("S01", 210, "Segments list"), ("S06", 692, "Import dialog")]  # id, seconds, label

for sid, t, label in SHOTS:
    raw = f"shots/{sid}_raw.png"
    subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", "call.mp4",
                    "-frames:v", "1", raw, "-y"], check=True)
    im = Image.open(raw).convert("RGB").crop(CROP)
    im.resize((im.width*SCALE, im.height*SCALE), Image.LANCZOS).save(f"shots/{sid}.png")
    os.remove(raw)
```

Aim for one screenshot per module, two or three for a module with a multi-step dialog. A document with a picture of every screen is not more useful than one with a picture of every *decision*.

## 5. Cut detail crops for individual controls

A full screen shows context; a detail crop shows the control. Cut them for anything where the reader needs to find one specific button, menu, or field: a dropdown menu, a cost summary, a filter panel, an empty-state call to action.

Express the box as fractions of the shot so it survives a resolution change:

```python
DETAILS = {"D_menu": ("S12", (0.82, 0.30, 1.00, 0.60))}  # l, t, r, b as fractions

for did, (src, fr) in DETAILS.items():
    im = Image.open(f"shots/{src}.png"); W, H = im.size
    im.crop((int(fr[0]*W), int(fr[1]*H), int(fr[2]*W), int(fr[3]*H))).save(f"shots/{did}.png")
```

**Verify every detail crop before it ships.** Guessed fractions miss their target more often than they hit it. Montage them and look. When a crop misses twice, stop guessing and read the parent shot at full resolution to get the real coordinates, or fall back to the full screenshot with a locator sentence, which is never wrong, only less pointed.

## 6. Compress

Interface screenshots are large, flat-coloured images, which is the ideal case for palette compression. Converting to an adaptive 256-colour palette is visually lossless on UI and cuts size roughly threefold. Do this to every image before embedding; a document with twenty full-resolution PNGs runs to 15 MB and will not survive email.

```python
im = Image.open(path).convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=256)
im.save(path, optimize=True)
```

Do not use JPEG. It is bigger than palette PNG at comparable quality here and it rings around text.

## 7. Verification checklist

Before any screenshot goes into a document:

1. **Right moment.** The frame shows the thing the caption claims. Check every one; an anchor timestamp taken from the transcript is often a few seconds before the presenter actually opened the screen.
2. **Legible.** Read the smallest label you intend to reference. If you cannot, extract a tighter crop rather than shipping a screenshot the reader must squint at.
3. **Overlay noted.** A floating self-view window covering part of the screen is normal and unavoidable. Choose a frame where it covers the least, and tell the reader in the document to ignore it.
4. **Nothing sensitive.** Demos expose customer names, credit balances, internal counts, email addresses, and open browser tabs. Scan each image and raise anything questionable with the user before delivering.
5. **Compressed.** Every image palette-converted, total document size sane.

## 8. Traps

| Trap | What happens | Fix |
|---|---|---|
| Very long inline shell scripts | `ENAMETOOLONG` on spawn | Write the script to a file, then run it |
| `drawtext` in an ffmpeg filter | Fontconfig error, then segfault | Label with Pillow after extraction |
| Working from the remote URL | Every seek re-downloads | Download once, work locally |
| Extracting before mapping | Frames of the wrong screen, repeatedly | Contact sheets first, always |
| Guessing detail-crop boxes | Empty or off-target crops | Verify by montage; read the parent at full res if it misses twice |
| Trusting a spoken number | The transcript mis-heard it | Read the figure off the frame; the screen wins |
| Signed URL expiry | Video gone mid-build | Check expiry at the start, download immediately |
