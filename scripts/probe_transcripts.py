"""One-shot probe: is the YouTube /api/timedtext captcha wall still up?

Run this occasionally (every few hours, not more often — re-checking too
often is exactly what keeps an IP's bot-reputation elevated). On success
(non-empty caption body) it writes data/raw/transcripts_unblocked.flag so
scripts/scrape.py can be told to resume real transcript fetching, and exits
0. On failure it exits 1 and logs why (still-empty body vs an outright
captcha/429 redirect).
"""
import re, json, random, sys, os
import requests

REPO = "/home/user/IELTS-tutor"
FLAG_PATH = os.path.join(REPO, "data", "raw", "transcripts_unblocked.flag")

TEST_VIDEO_ID = "CA7b8z-gKQA"  # known long video with an English auto-caption track (verified in data/raw/info)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def main():
    s = requests.Session()
    headers = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}

    resp = s.get(f"https://www.youtube.com/watch?v={TEST_VIDEO_ID}", headers=headers, timeout=25)
    if resp.status_code != 200 or "google.com/sorry" in resp.url:
        print(f"BLOCKED on watch page: status={resp.status_code} url={resp.url[:100]}")
        return 1

    m = re.search(r'ytInitialPlayerResponse\s*=\s*(\{.*?\})\s*;\s*(?:var |</script|\n)', resp.text)
    if not m:
        print("watch page OK but no ytInitialPlayerResponse (unexpected page shape)")
        return 1
    data = json.loads(m.group(1))
    status = data.get("playabilityStatus", {})
    if status.get("status") not in (None, "OK"):
        print(f"soft-blocked: playabilityStatus={status.get('status')} reason={status.get('reason')!r}")
        return 1
    tracks = data.get("captions", {}).get("playerCaptionsTracklistRenderer", {}).get("captionTracks", [])
    if not tracks:
        print("watch page OK but no caption tracks listed for this video")
        return 1

    cap_resp = s.get(tracks[0]["baseUrl"] + "&fmt=vtt", headers=headers, timeout=25)
    if cap_resp.status_code == 200 and len(cap_resp.content) > 0:
        with open(FLAG_PATH, "w") as f:
            f.write("unblocked\n")
        print(f"SUCCESS: got {len(cap_resp.content)} bytes of captions. "
              f"Wrote {FLAG_PATH} — re-enable FETCH_TRANSCRIPTS in scrape.py and restart it.")
        return 0

    print(f"still blocked: caption fetch status={cap_resp.status_code} len={len(cap_resp.content)}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
