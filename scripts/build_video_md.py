import json, os, re, glob, datetime

ROOT = "/home/user/IELTS-tutor/data"
INFO_DIR = os.path.join(ROOT, "raw", "info")
SUBS_DIR = os.path.join(ROOT, "raw", "subs")
OUT_DIR = os.path.join(ROOT, "videos")
os.makedirs(OUT_DIR, exist_ok=True)

def vtt_to_text(path):
    if not os.path.exists(path):
        return None
    lines = open(path, encoding="utf-8", errors="ignore").read().splitlines()
    out = []
    last = None
    for ln in lines:
        ln = ln.strip()
        if not ln or ln == "WEBVTT" or "-->" in ln or ln.isdigit():
            continue
        if ln.startswith("Kind:") or ln.startswith("Language:"):
            continue
        ln = re.sub(r"<[^>]+>", "", ln)
        ln = re.sub(r"\[.*?\]", "", ln).strip()
        if not ln:
            continue
        if ln == last:
            continue
        out.append(ln)
        last = ln
    text = " ".join(out)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def fmt_duration(secs):
    try:
        secs = int(secs)
    except Exception:
        return str(secs)
    m, s = divmod(secs, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"

def main():
    built = 0
    skipped = 0
    for path in sorted(glob.glob(os.path.join(INFO_DIR, "*.json"))):
        vid = os.path.splitext(os.path.basename(path))[0]
        out_path = os.path.join(OUT_DIR, f"{vid}.md")
        info = json.load(open(path, encoding="utf-8"))
        title = info.get("title") or info.get("flat_title") or vid
        duration = info.get("lengthSeconds") or info.get("duration") or 0
        desc = (info.get("description") or "").strip()
        publish = info.get("publishDate") or "unknown"
        transcript = vtt_to_text(os.path.join(SUBS_DIR, f"{vid}.vtt"))

        lines = []
        lines.append(f"# {title}")
        lines.append("")
        lines.append(f"- **Video ID:** {vid}")
        lines.append(f"- **URL:** https://www.youtube.com/watch?v={vid}")
        lines.append(f"- **Duration:** {fmt_duration(duration)} ({duration}s)")
        lines.append(f"- **Published:** {publish}")
        lines.append("")
        lines.append("## Description")
        lines.append("")
        lines.append(desc if desc else "_(no description)_")
        lines.append("")
        lines.append("## Transcript")
        lines.append("")
        if transcript:
            lines.append(transcript)
        else:
            lines.append("_(no transcript available — short clip or captions missing)_")
        lines.append("")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        built += 1
    print(f"built/updated {built} video markdown files")

if __name__ == "__main__":
    main()
