"""Re.en コラム書き直しの反映（2026-10）。

使い方: python3 scripts/apply_reen_rewrite.py <データJSONのフォルダ> [--check]
  1. フォルダ内の *.json（BRIEFの形式の配列）を、editorial_calendar_matching.json に反映する（authored=true）
  2. 重複記事（MERGE）を削除し、301リダイレクトを vercel.json に追加し、ほかの記事のリンクを付け替える
  3. 題名の「(Vol.N)」を、カレンダーと全ページから外す
  4. 書き直したページの本文を、write_matching_article_contents.py で再生成できるよう、目印を外す
  5. 関連記事（同じカテゴリ・近いテーマ）を、各ページに3本ずつ入れる
その後、run_matching_column_pipeline.py の手順（write → rewrite → fix_toc → rebuild → seo_fix）を実行する。
"""
import glob
import html as htmllib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAL = os.path.join(ROOT, "editorial_calendar_matching.json")
MARK = "<!-- authored:cc -->"

MERGE = {2: 54, 40: 54, 59: 26, 103: 26, 70: 46, 75: 64, 108: 64, 68: 63, 76: 45, 102: 61, 16: 28, 60: 42,
         71: 166, 109: 15, 50: 11, 48: 12, 57: 12, 23: 12, 52: 24, 13: 24, 55: 62, 38: 14, 43: 77, 72: 53,
         37: 67, 6: 106, 4: 56, 69: 104, 21: 20, 22: 20}

BAD = ["監修", "体験談", "密会", "バレない", "バレずに", "身バレしない", "隠し方", "ごまかし"]


def num(fn):
    return int(re.search(r"(\d+)", os.path.basename(fn)).group(1))


def plain(h):
    return htmllib.unescape(re.sub(r"<[^>]+>", "", h))


def body_len(e):
    t = e["lead"] + "".join(s["text"] for s in e["body_sections"]) + "".join(
        "".join(e["highlight_box"]["items"]) for _ in [0])
    t += "".join(q["a"] for q in e["faqs"])
    return len(re.sub(r"\s+", "", plain(t)))


def validate(e, existing):
    errs = []
    for k in ("filename", "headline", "title", "description", "lead", "body_sections", "highlight_box", "faqs"):
        if not e.get(k):
            errs.append(f"{k}が空")
    if errs:
        return errs
    if "Vol." in e["title"] or "Vol." in e["headline"]:
        errs.append("Volが残っている")
    if not e["title"].endswith("| Re.en Column"):
        errs.append("titleの語尾")
    if len(e["faqs"]) != 3 or not all(q["q"].endswith(("？", "?")) for q in e["faqs"]):
        errs.append("FAQは3問・疑問形")
    if not 3 <= len(e["body_sections"]) <= 5:
        errs.append("H2は3〜5個")
    n_h3 = sum(len(re.findall(r"<h3", s["text"])) for s in e["body_sections"])
    if n_h3 < 6:
        errs.append(f"H3が少ない（{n_h3}）")
    blob = json.dumps(e, ensure_ascii=False)
    for w in BAD:
        if w in blob:
            errs.append(f"禁止語: {w}")
    if "style=" in "".join(s["text"] for s in e["body_sections"]):
        errs.append("style属性")
    for m in re.findall(r'href="/column-detail-(\d+)"', blob):
        if int(m) in MERGE or int(m) not in existing:
            errs.append(f"リンク先が存在しない/削除: {m}")
    if body_len(e) < 2600:
        errs.append(f"本文が短い（{body_len(e)}字）")
    if "実在の人物ではありません" not in blob:
        errs.append("想定ケースの注記が無い")
    return errs


def main():
    src = sys.argv[1]
    check = "--check" in sys.argv
    cal = json.load(open(CAL, encoding="utf-8"))
    cmap = {c["filename"]: c for c in cal}
    existing = {num(f) for f in glob.glob(os.path.join(ROOT, "column-detail-*.html"))} - set(MERGE)
    entries = []
    for f in sorted(glob.glob(os.path.join(src, "*.json"))):
        entries += json.load(open(f, encoding="utf-8"))
    bad = 0
    for e in entries:
        errs = validate(e, existing)
        if errs:
            bad += 1
            print("NG", e.get("filename"), " / ".join(errs))
    print(f"{len(entries)}本 検査NG {bad}本")
    if check or bad:
        sys.exit(1 if bad else 0)

    # 1. カレンダー
    for e in entries:
        fn = e["filename"]
        page = open(os.path.join(ROOT, fn), encoding="utf-8").read()
        old = cmap.get(fn)
        if not old:
            old = {"vol": num(fn), "filename": fn}
            img = re.search(r'images/column_[a-z0-9_]+\.webp', page)
            old["banner_img"] = img.group(0) if img else "images/column_second_partner.webp"
            cal.append(old)
            cmap[fn] = old
        cat = e.get("category_name")
        if not cat:
            m = re.search(r'<span class="article-header__category">([^<]+)</span>', page)
            cat = m.group(1) if m else old.get("category_name", "お悩み")
        old.update({k: e[k] for k in ("headline", "title", "description", "lead", "body_sections", "highlight_box", "faqs")})
        old["category_name"] = cat
        if e.get("keywords"):
            old["keywords"] = e["keywords"]
        old["authored"] = True
        # 2. 目印を外して再生成させる
        page = page.replace(MARK, "")
        open(os.path.join(ROOT, fn), "w", encoding="utf-8").write(page)

    # 3. 統合
    vj = json.load(open(os.path.join(ROOT, "vercel.json"), encoding="utf-8"))
    have = {r["source"] for r in vj["redirects"]}
    for s, d in MERGE.items():
        fn = os.path.join(ROOT, f"column-detail-{s}.html")
        if os.path.exists(fn):
            os.remove(fn)
        for src_path in (f"/column-detail-{s}", f"/column-detail-{s}.html"):
            if src_path not in have:
                vj["redirects"].insert(0, {"source": src_path, "destination": f"/column-detail-{d}", "permanent": True})
    json.dump(vj, open(os.path.join(ROOT, "vercel.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    cal = [c for c in cal if num(c["filename"]) not in MERGE]

    # 4. Volを外す
    vol = re.compile(r"\s*\(Vol\.\d+\)")
    for c in cal:
        c["title"] = vol.sub("", c["title"])
        c["headline"] = vol.sub("", c["headline"])
    json.dump(cal, open(CAL, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(cal, open(os.path.join(ROOT, "scripts", "editorial_calendar_matching.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    for f in glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "docs", "**", "*.html"), recursive=True):
        s = open(f, encoding="utf-8").read()
        n = vol.sub("", s)
        for sn, d in MERGE.items():
            n = re.sub(rf'href="(/?)column-detail-{sn}(\.html)?"', rf'href="\1column-detail-{d}"', n)
        if n != s:
            open(f, "w", encoding="utf-8").write(n)
    print("反映完了。続けて、パイプラインの手順を実行してください。")


if __name__ == "__main__":
    main()
