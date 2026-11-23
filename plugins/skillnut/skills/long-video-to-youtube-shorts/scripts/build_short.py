"""Build a 1080x1920 Short: titles on top, content in the middle (top 70% together),
camera strip in the bottom 30%. Usage: python build_short.py spec.json
Set "font" in the spec to a bold TTF on non-Windows machines."""
import json, os, subprocess, sys

spec = json.load(open(sys.argv[1], encoding="utf-8"))
work = spec["work"]
os.makedirs(work, exist_ok=True)
SFX = spec.get("sfx_dir", "")
FONT = spec.get("font", "C:/Windows/Fonts/ariblk.ttf").replace(":", "\\:", 1)
W, H, CAM_H = 1080, 1920, 576
CAM_Y = H - CAM_H
TITLE_H = spec.get("title_h", 540)

FPS = 30
# Snap every cut to the frame grid. Video can only cut on whole frames while audio cuts exactly;
# unsnapped, the rounding accumulates across segments and the lips drift behind the voice.
snap = lambda t: round(t * FPS) / FPS
segs = [[snap(a), snap(b)] for a, b in spec["segments"]]  # source seconds
if "top_starts" in spec:
    spec["top_starts"] = [snap(t) for t in spec["top_starts"]]
total = sum(round((b - a) * FPS) for a, b in segs) / FPS

inputs, fc = [], []
def add_input(path, a, b):
    # read a little past the end so every segment has enough frames to fill its exact frame count
    inputs.extend(["-ss", f"{a:.3f}", "-t", f"{b - a + 0.2:.3f}", "-i", path])
    return len(inputs) // 6 - 1

cam_v, top_v, aud = [], [], []
for i, (a, b) in enumerate(segs):
    ci = add_input(spec["camera"], a, b)
    # top visuals can come from a different moment than the speech (same duration)
    ta = spec["top_starts"][i] if "top_starts" in spec else a
    ti = add_input(spec["top"], ta, ta + (b - a))
    # audio must follow the speech times; only reuse an input that was seeked to [a, b]
    if spec["audio"] == spec["camera"]:
        src = ci
    elif spec["audio"] == spec["top"] and ta == a:
        src = ti
    else:
        src = add_input(spec["audio"], a, b)
    # Every segment is exactly N frames of video and exactly N/FPS seconds of audio, so the two
    # can never drift apart across cuts, however many segments there are.
    nf = round((b - a) * FPS)
    d = nf / FPS
    ns = round(d * 48000)
    vcut = f"setpts=PTS-STARTPTS,fps={FPS},tpad=stop_mode=clone:stop=6,trim=end_frame={nf},setpts=PTS-STARTPTS"
    fc.append(f"[{ci}:v]{vcut}[cv{i}]")
    fc.append(f"[{ti}:v]{vcut}[tv{i}]")
    fc.append(f"[{src}:a]aresample=48000,asetpts=PTS-STARTPTS,apad,atrim=end_sample={ns},asetpts=PTS-STARTPTS,"
              f"afade=t=in:d=0.03,afade=t=out:st={max(d-0.04,0):.3f}:d=0.04[a{i}]")
    cam_v.append(f"[cv{i}]"); top_v.append(f"[tv{i}]"); aud.append(f"[a{i}]")

n = len(segs)
fc.append("".join(cam_v) + f"concat=n={n}:v=1:a=0[camc]")
fc.append("".join(top_v) + f"concat=n={n}:v=1:a=0[topc]")
fc.append("".join(aud) + f"concat=n={n}:v=0:a=1,loudnorm=I=-16:TP=-2:LRA=11,aresample=48000[voice]")

c = spec["cam"]  # scale width, crop x, crop y
fc.append(f"[camc]scale={c['w']}:-2,crop={W}:{CAM_H}:{c['x']}:{c['y']},setsar=1[cam]")
t = spec["top_crop"]  # x, y, w, h in source pixels
area_h = CAM_Y - 8 - TITLE_H
fc.append(f"[topc]crop={t['w']}:{t['h']}:{t['x']}:{t['y']},scale={W}:{area_h}:force_original_aspect_ratio=decrease,setsar=1[top]")
fc.append(f"color=c=0x0E0D14:s={W}x{H}:r=30:d={total:.3f}[bg]")
fc.append(f"[bg][cam]overlay=0:{CAM_Y}:shortest=1[b1]")
fc.append(f"[b1][top]overlay=(W-w)/2:{TITLE_H}+({area_h}-h)/2[b2]")

draws = [f"drawbox=x=0:y={CAM_Y-6}:w={W}:h=6:color=0x5E51F8:t=fill",
         f"drawbox=x=0:y=0:w='{W}*t/{total:.3f}':h=12:color=0xFACC15:t=fill"]
for k, ti in enumerate(spec["titles"]):
    t0, t1 = ti["t0"], ti["t1"]
    for j, key in enumerate(("l1", "l2")):
        txt = ti.get(key)
        if not txt:
            continue
        tf = os.path.join(work, f"t{k}_{j}.txt").replace("\\", "/")
        open(tf, "w", encoding="utf-8").write(txt)
        tfe = tf.replace(":", "\\:")
        if j == 0:
            box = ti.get("box", "0x5E51F8"); fcol = ti.get("color", "white")
            # shrink so text plus box padding fits the frame (Arial Black caps ~0.8em wide)
            size = min(ti.get("s1", 96), int(1030 / (0.8 * len(txt) + 0.52)))
            style = f"fontsize={size}:fontcolor={fcol}:box=1:boxcolor={box}:boxborderw={int(size*0.26)}:y={ti.get('y1', 200)}"
            st = t0
        else:
            size = min(ti.get("s2", 60), int(1040 / (0.8 * len(txt))))
            style = f"fontsize={size}:fontcolor={ti.get('color2', 'white')}:y={ti.get('y2', 390)}"
            st = t0 + ti.get("d2", 0.3)
        draws.append(f"drawtext=fontfile='{FONT}':textfile='{tfe}':expansion=none:{style}:x=(w-text_w)/2:"
                     f"enable='between(t,{st:.3f},{t1:.3f})':alpha='min(1,(t-{st:.3f})/0.12)'")
fc.append("[b2]" + ",".join(draws) + "[vout]")

# sound effects
sfx = [s for s in spec.get("sfx", []) if os.path.exists(os.path.join(SFX, s["name"] + ".mp3"))]
skipped = [s["name"] for s in spec.get("sfx", []) if s not in sfx]
if skipped:
    print("No sound file for " + ", ".join(skipped) + ", so those effects were skipped")
mix = ["[voice]"]
for k, s in enumerate(sfx):
    inputs.extend(["-i", os.path.join(SFX, s["name"] + ".mp3")])
    idx = sum(1 for x in inputs if x == "-i") - 1
    ms = int(s["t"] * 1000)
    fc.append(f"[{idx}:a]aresample=48000,volume={s.get('vol', 0.5)},adelay={ms}|{ms}[x{k}]")
    mix.append(f"[x{k}]")
fc.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,alimiter=limit=0.95[aout]")

graph = os.path.join(work, "graph.txt")
open(graph, "w", encoding="utf-8").write(";\n".join(fc))
cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-/filter_complex", graph, "-map", "[vout]", "-map", "[aout]",
       "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{total:.3f}", spec["out"]]
subprocess.run(cmd, check=True)
print(f"OK {spec['out']} {total:.2f}s")
