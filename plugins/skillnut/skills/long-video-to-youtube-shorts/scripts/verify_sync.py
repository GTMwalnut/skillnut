"""Verify a rendered Short against its spec: is each cut the right moment, and are the lips in sync?

Two independent measurements per segment:
  - voice: the output audio located in the source audio (loudness envelope, 10 ms steps)
  - picture: output camera frames matched to source camera frames by pixel difference at three
    points in the segment (exact frame matching; far more reliable than motion correlation)
The lip-sync gap is picture offset minus voice offset (positive = sound arrives late).

Usage: python verify_sync.py spec.json [--legacy]
  --legacy  measure a render made by the old builder (unsnapped cuts) for comparison
Pass: voice match about 0.85 or higher, and every lip-sync gap between -40 ms and +100 ms.
The window is lopsided on purpose (broadcast guidance, ITU-R BT.1359): viewers notice sound that
arrives EARLY (negative gap) from about 45 ms, but sound that arrives LATE (positive gap) only from
about 125 ms. Frame matching has about one frame (33 ms) of jitter; a gap that grows from cut to cut
is real drift.
"""
import json
import subprocess
import sys

import numpy as np

FPS, CAM_Y, CAM_H = 30, 1344, 576
EDGE = 0.25  # stay clear of cut edges and fades


def run(args):
    return subprocess.run(["ffmpeg", "-v", "error", *args], capture_output=True).stdout


def audio_env(path, ss, t, rate=100):
    x = np.abs(np.frombuffer(run(["-ss", f"{ss:.3f}", "-t", f"{t:.3f}", "-i", path, "-ac", "1", "-ar", "8000",
                                  "-f", "s16le", "-"]), dtype=np.int16).astype(float))
    step = 8000 // rate
    n = len(x) // step
    return x[:n * step].reshape(n, step).mean(axis=1)


def frames(path, ss, count, vf):
    raw = run(["-ss", f"{ss:.4f}", "-i", path, "-frames:v", str(count), "-vf",
               vf + ",scale=160:86,format=gray", "-f", "rawvideo", "-"])
    return np.frombuffer(raw, dtype=np.uint8).reshape(-1, 86, 160).astype(float)


def voice_offset(spec, a, pos, t, search=0.2, rate=100):
    src = audio_env(spec["audio"], a + EDGE - search, t + 2 * search, rate)
    got = audio_env(spec["out"], pos + EDGE, t, rate)
    k0 = int(search * rate)
    best = (-2.0, 0)
    for k in range(0, 2 * k0 + 1):
        s = src[k:k + len(got)]
        if len(s) == len(got) and s.std() > 0 and got.std() > 0:
            best = max(best, (float(np.corrcoef(s, got)[0, 1]), k - k0))
    return best[0], best[1] * 1000 / rate


def picture_offset(spec, a, pos, d, search=4):
    """Median offset in ms over three probe points; positive = output shows a later source frame."""
    cam = spec["cam"]
    src_vf = f"scale={cam['w']}:-2,crop=1080:{CAM_H}:{cam['x']}:{cam['y']}"
    out_vf = f"crop=1080:{CAM_H}:0:{CAM_Y}"
    offs = []
    for frac in (0.25, 0.5, 0.75):
        t = max(EDGE, min(d - EDGE, d * frac))
        got = frames(spec["out"], pos + t, 1, out_vf)
        cand = frames(spec["camera"], a + t - search / FPS, 2 * search + 1, src_vf)
        if len(got) and len(cand):
            err = [float(np.mean((c - got[0]) ** 2)) for c in cand]
            offs.append((int(np.argmin(err)) - search) * 1000 / FPS)
    return float(np.median(offs)) if offs else float("nan")


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    legacy = "--legacy" in sys.argv
    pos, ok = 0.0, True
    for i, (a, b) in enumerate(spec["segments"]):
        if legacy:
            d_out = np.ceil((b - a) * FPS - 1e-6) / FPS  # old builder: video rounded up per cut, audio exact
            d_audio = b - a
        else:
            a, b = round(a * FPS) / FPS, round(b * FPS) / FPS
            d_out = d_audio = round((b - a) * FPS) / FPS
        d = b - a
        r, v_ms = voice_offset(spec, a, pos, max(0.5, d - 2 * EDGE))
        p_ms = picture_offset(spec, a, pos, d)
        gap = p_ms - v_ms
        # under 1.5 s there is too little audio left after trimming the edges for a fair match score
        short = d < 1.5
        bad = (r < 0.85 and not short) or gap < -40 or gap > 100
        ok = ok and not bad
        print(f"segment {i + 1} ({a:.2f}-{b:.2f}s): voice {v_ms:+.0f} ms (match {r:.2f}), "
              f"picture {p_ms:+.0f} ms, lip-sync gap {gap:+.0f} ms{' (short cut)' if short else ''}{'   <-- CHECK' if bad else ''}")
        pos += d_audio if legacy else d_out
    print("ALL GOOD" if ok else "FIX BEFORE HANDOVER")


if __name__ == "__main__":
    main()
