"""Read a YouTube auto-caption file (json3) and print word timings.

Usage:
  python transcript_words.py <file.json3> --lines        timed lines (~6 s each) to find the story
  python transcript_words.py <file.json3> <from> <to>    every word with its start time, in seconds
"""
import json
import sys


def load_words(path):
    d = json.load(open(path, encoding="utf-8"))
    words = []
    for ev in d.get("events", []):
        t0 = ev.get("tStartMs", 0)
        for seg in ev.get("segs", []) or []:
            txt = seg.get("utf8", "").strip()
            if txt:
                words.append(((t0 + seg.get("tOffsetMs", 0)) / 1000, txt))
    return sorted(words)


def main():
    path = sys.argv[1]
    words = load_words(path)
    if len(sys.argv) > 2 and sys.argv[2] == "--lines":
        line, start = [], None
        for t, w in words:
            start = t if start is None else start
            line.append(w)
            if t - start > 6:
                print(f"{start:7.2f}  {' '.join(line)}")
                line, start = [], None
        if line:
            print(f"{start:7.2f}  {' '.join(line)}")
        return
    a, b = float(sys.argv[2]), float(sys.argv[3])
    print(" ".join(f"{w}@{t:.2f}" for t, w in words if a <= t <= b))


if __name__ == "__main__":
    main()
