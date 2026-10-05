"""
Resumable, block-aware scraper for the IELTS Advantage YouTube channel.

Fetches per-video metadata (title, description, publish date, caption track
URL) by requesting the public watch page directly (no yt-dlp player API calls,
which trip YouTube's bot defenses faster). For videos >=90s it also downloads
the English auto/manual caption track as .vtt.

Resumable: skips any video id that already has data/raw/info/<id>.json.
Block-aware: Google occasionally redirects requests from this shared egress
IP to a captcha wall (google.com/sorry). When detected, the script sleeps a
long cooldown (COOLDOWN_SECONDS) and retries the SAME video rather than
racing through retries and burning the IP's reputation further.

Safe to kill and re-run at any time (nohup'd, detached from any one shell).
"""
import json, re, random, time, os
import requests

REPO = "/home/user/IELTS-tutor"
RAW = os.path.join(REPO, "data", "raw")
INFO_DIR = os.path.join(RAW, "info")
SUBS_DIR = os.path.join(RAW, "subs")
os.makedirs(INFO_DIR, exist_ok=True)
os.makedirs(SUBS_DIR, exist_ok=True)

UPLOADS_JSON = os.path.join(RAW, "uploads.json")
LOG = os.path.join(RAW, "scrape.log")

MIN_DELAY = 20.0
MAX_DELAY = 35.0
COOLDOWN_SECONDS = 25 * 60  # wait this long when hard-blocked, then retry same video
MAX_BLOCK_RETRIES = 200  # ~80+ hours of cooldowns before giving up on a single video

UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
]

session = requests.Session()


def log(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def is_blocked(resp):
    if resp is None:
        return False
    url = resp.url or ""
    if "google.com/sorry" in url or "/sorry/index" in url:
        return True
    if resp.status_code == 429:
        return True
    return False


def fetch(url):
    """Returns a Response on success (200, not a block page), or None on
    normal failure. Raises nothing; on a detected block it sleeps a long
    cooldown internally and keeps retrying the same request."""
    block_attempts = 0
    while True:
        headers = {"User-Agent": random.choice(UAS), "Accept-Language": "en-US,en;q=0.9"}
        try:
            resp = session.get(url, headers=headers, timeout=25, allow_redirects=True)
        except Exception as e:
            log(f"  ! request error {e}, retrying in 60s")
            time.sleep(60)
            continue

        if is_blocked(resp):
            block_attempts += 1
            log(f"  !! BLOCKED (status={resp.status_code}, url={resp.url[:90]}) "
                f"— cooldown {COOLDOWN_SECONDS}s (block attempt {block_attempts})")
            if block_attempts >= MAX_BLOCK_RETRIES:
                log("  !! giving up on this URL after too many blocks")
                return None
            time.sleep(COOLDOWN_SECONDS)
            continue

        if resp.status_code != 200:
            log(f"  ! HTTP {resp.status_code} for {url[:90]}")
            return resp

        return resp


def extract_json_var(html, varname):
    m = re.search(varname + r'\s*=\s*(\{.*?\})\s*;\s*(?:var |</script|\n)', html)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def main():
    entries = json.load(open(UPLOADS_JSON))["entries"]
    total = len(entries)
    log(f"=== starting run, {total} videos total ===")
    done = 0
    for i, e in enumerate(entries, 1):
        vid = e["id"]
        duration = e.get("duration") or 0
        info_path = os.path.join(INFO_DIR, f"{vid}.json")
        if os.path.exists(info_path):
            done += 1
            continue

        resp = fetch(f"https://www.youtube.com/watch?v={vid}")
        if resp is None or resp.status_code != 200:
            log(f"[{i}/{total}] {vid} FAILED metadata fetch, will retry on next run")
            time.sleep(random.uniform(5, 9))
            continue

        html = resp.text
        player = extract_json_var(html, "ytInitialPlayerResponse")
        record = {"id": vid, "flat_title": e.get("title"), "duration": duration}
        caption_url = None
        if player:
            vd = player.get("videoDetails", {})
            record["title"] = vd.get("title")
            record["description"] = vd.get("shortDescription")
            record["lengthSeconds"] = vd.get("lengthSeconds")
            record["keywords"] = vd.get("keywords")
            mf = player.get("microformat", {}).get("playerMicroformatRenderer", {})
            record["publishDate"] = mf.get("publishDate")
            record["category"] = mf.get("category")
            tracks = player.get("captions", {}).get("playerCaptionsTracklistRenderer", {}).get("captionTracks", [])
            en_tracks = [t for t in tracks if (t.get("languageCode") or "").startswith("en")]
            chosen = en_tracks[0] if en_tracks else (tracks[0] if tracks else None)
            if chosen:
                caption_url = chosen["baseUrl"]
                record["caption_lang"] = chosen.get("languageCode")
                record["caption_kind"] = chosen.get("kind")
        else:
            log(f"[{i}/{total}] {vid} no player response parsed (unusual page?)")

        with open(info_path, "w") as f:
            json.dump(record, f, ensure_ascii=False, indent=1)

        if caption_url and duration >= 90:
            sub_path = os.path.join(SUBS_DIR, f"{vid}.vtt")
            if not os.path.exists(sub_path):
                time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
                sresp = fetch(caption_url.replace("\\u0026", "&") + "&fmt=vtt")
                if sresp is not None and sresp.status_code == 200 and sresp.content:
                    with open(sub_path, "wb") as f:
                        f.write(sresp.content)
                else:
                    log(f"[{i}/{total}] {vid} transcript fetch empty/failed")

        done += 1
        if i % 10 == 0 or i == total:
            log(f"[{i}/{total}] progress, done={done}/{total}")

        time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

    log(f"=== finished run, done={done}/{total} ===")


if __name__ == "__main__":
    main()
