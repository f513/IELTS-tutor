"""Merge the 6 classification batches + uploads.json into:
  - data/classification.json  (machine-readable, full record per video)
  - data/catalog.md           (human-readable table, grouped by section)

Idempotent: safe to re-run whenever classification_parts/output_*.json or
raw/info/*.json (for refined needs_review passes) change.
"""
import json, os

ROOT = "/home/user/IELTS-tutor"
DATA = os.path.join(ROOT, "data")


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
    uploads = {e["id"]: e for e in json.load(open(os.path.join(DATA, "raw", "uploads.json")))["entries"]}

    classified = {}
    for i in range(1, 7):
        path = os.path.join(DATA, "classification_parts", f"output_{i}.json")
        for it in json.load(open(path)):
            classified[it["id"]] = it

    # apply needs_review refinement pass (title+description), overrides title-only calls
    for letter in ("a", "b"):
        path = os.path.join(DATA, "classification_review", f"output_{letter}.json")
        if os.path.exists(path):
            for it in json.load(open(path)):
                classified[it["id"]] = it

    records = []
    for vid, up in uploads.items():
        c = classified.get(vid, {})
        records.append({
            "id": vid,
            "title": up.get("title"),
            "duration": up.get("duration") or 0,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "section": c.get("section", "general"),
            "subtype": c.get("subtype", "advice"),
            "secondary_subtypes": c.get("secondary_subtypes", []),
            "confidence": c.get("confidence", "low"),
            "needs_review": c.get("needs_review", True),
            "reason": c.get("reason", ""),
        })

    records.sort(key=lambda r: (r["section"], r["subtype"], r["title"] or ""))
    with open(os.path.join(DATA, "classification.json"), "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=1)

    # human-readable catalog.md, grouped by section then subtype
    sections_order = ["reading", "listening", "speaking", "writing", "general"]
    subtypes_order = ["training", "exam", "advice", "tips"]

    lines = ["# Каталог видео — IELTS Advantage", "",
             f"Всего видео: {len(records)}. Авто-классификация по заголовкам "
             f"(первая волна); `needs_review=true` — уточнить по транскрипту позже.",
             ""]

    by_section = {}
    for r in records:
        by_section.setdefault(r["section"], []).append(r)

    for sec in sections_order:
        items = by_section.get(sec, [])
        if not items:
            continue
        lines.append(f"## {sec.capitalize()} ({len(items)})")
        lines.append("")
        by_subtype = {}
        for r in items:
            by_subtype.setdefault(r["subtype"], []).append(r)
        for sub in subtypes_order:
            sub_items = by_subtype.get(sub, [])
            if not sub_items:
                continue
            lines.append(f"### {sub} ({len(sub_items)})")
            lines.append("")
            lines.append("| Title | Duration | needs_review | Link |")
            lines.append("|---|---|---|---|")
            for r in sub_items:
                flag = "⚠️" if r["needs_review"] else ""
                lines.append(f"| {r['title']} | {fmt_duration(r['duration'])} | {flag} | [{r['id']}]({r['url']}) |")
            lines.append("")

    with open(os.path.join(DATA, "catalog.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"wrote {len(records)} records to classification.json and catalog.md")


if __name__ == "__main__":
    main()
