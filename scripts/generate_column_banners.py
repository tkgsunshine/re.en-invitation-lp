"""記事ごとのアイキャッチ画像を作る（2026-10）。

写真は約25種類しかなく、約115本の記事で使い回されていた。そこで、記事ごとに
「写真（色・切り出しを記事ごとに変える）＋カテゴリ＋短いキャッチコピー」の画像を作り、
一覧・記事ヒーロー・OGPの画像を、すべて記事固有にする。

- 出力: images/banners/column-detail-N.webp（1200x630）／ images/og/column-detail-N.jpg（OGP用）
- editorial_calendar_matching.json の banner_img を、作った画像に更新する
- 既存ページのヒーロー画像も差し替える（run_matching_column_pipeline.py の最初にも呼ばれ、新しい記事の分を作る）
何度実行しても、同じ記事には同じ画像ができる（画像がある記事は作り直さない。--force で作り直す）。
"""
import glob
import hashlib
import json
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "images", "banners")
OG = os.path.join(ROOT, "images", "og")
FONTS = ["/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf", "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"]
W, H = 1200, 630
GOLD = (212, 175, 105)
SPLIT = re.compile(r"[｜|。？！：]")


def font(size):
    for f in FONTS:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def catch_copy(headline):
    parts = [p.strip() for p in SPLIT.split(headline) if p.strip()]
    if not parts:
        return headline[:24]
    # 先頭の句が10〜26字ならそれを、短すぎる・長すぎるときは、8〜26字の次の句を使う
    if 10 <= len(parts[0]) <= 26:
        text = parts[0]
    else:
        cand = [p for p in parts if 8 <= len(p) <= 26]
        text = cand[0] if cand else parts[0][:26]
    return text


def wrap(text, per_line=13):
    lines, cur = [], ""
    for ch in text:
        cur += ch
        if len(cur) >= per_line and ch in "、，のをにはでがと" or len(cur) >= per_line + 2:
            lines.append(cur)
            cur = ""
    if cur:
        lines.append(cur)
    if len(lines) > 1 and len(lines[-1]) <= 2:  # 1〜2文字だけの行を避ける
        lines[-2] += lines[-1]
        lines.pop()
    return lines[:3]


def make(n, headline, category, src_photo):
    h = hashlib.md5(f"column-detail-{n}".encode()).digest()
    photo = Image.open(os.path.join(ROOT, src_photo)).convert("RGB")
    # 切り出し位置・拡大率・向きを記事ごとに変える
    zoom = 1.0 + (h[0] % 40) / 100
    pw, ph = photo.size
    cw = int(pw / zoom)
    ch = int(cw * H / W)
    ch = min(ch, ph)
    cw = int(ch * W / H)
    x0 = int((pw - cw) * (h[1] / 255))
    y0 = int((ph - ch) * (h[2] / 255))
    img = photo.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)
    if h[3] % 2:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    # 左から右へ暗くするグラデーション（文字を読みやすく）
    ov = Image.new("RGBA", (W, H))
    px = ov.load()
    for x in range(W):
        a = int(235 - 140 * (x / W))
        for y in range(H):
            px[x, y] = (10, 10, 12, a)
    img = Image.alpha_composite(img.convert("RGBA"), ov)
    d = ImageDraw.Draw(img)
    # カテゴリのチップ
    cf = font(30)
    tw = d.textlength(category, font=cf)
    d.rounded_rectangle((70, 74, 70 + tw + 44, 74 + 52), radius=6, fill=GOLD)
    d.text((92, 80), category, font=cf, fill=(20, 20, 22))
    # キャッチコピー
    lines = wrap(catch_copy(headline))
    f = font(68 if len(max(lines, key=len)) <= 12 else 60)
    y = 170
    for line in lines:
        d.text((70, y), line, font=f, fill=(255, 255, 255), stroke_width=1, stroke_fill=(255, 255, 255))
        y += int(f.size * 1.35)
    # 区切り線とブランド
    d.rectangle((70, H - 118, 190, H - 114), fill=GOLD)
    d.text((70, H - 96), "Re.en  COLUMN", font=font(30), fill=GOLD)
    img = img.convert("RGB")
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(OG, exist_ok=True)
    img.save(os.path.join(OUT, f"column-detail-{n}.webp"), "WEBP", quality=82, method=6)
    img.save(os.path.join(OG, f"column-detail-{n}.jpg"), "JPEG", quality=86)


def main():
    force = "--force" in sys.argv
    if not any(os.path.exists(f) for f in FONTS):
        print("日本語フォントが無いため、バナー生成を飛ばします（文字化けした画像を作らない）。")
        return
    cp = os.path.join(ROOT, "editorial_calendar_matching.json")
    cal = json.load(open(cp, encoding="utf-8"))
    made = 0
    for c in cal:
        m = re.search(r"column-detail-(\d+)\.html$", c["filename"])
        if not m:
            continue
        n = int(m.group(1))
        rel = f"images/banners/column-detail-{n}.webp"
        have = os.path.exists(os.path.join(ROOT, rel))
        src = c.get("source_photo")
        if not src:
            cur = c.get("banner_img", "")
            src = cur if cur and "banners/" not in cur and os.path.exists(os.path.join(ROOT, cur)) else "images/column_second_partner.webp"
            c["source_photo"] = src
        if force or not have:
            make(n, c["headline"], c.get("category_name", "コラム"), src)
            made += 1
        c["banner_img"] = rel
        page = os.path.join(ROOT, c["filename"])
        if os.path.exists(page):
            s = open(page, encoding="utf-8").read()
            s2 = re.sub(r'(<header class="article-header">.*?<img src=")[^"]+(")', lambda mm: mm.group(1) + rel + mm.group(2), s, count=1, flags=re.S)
            if s2 != s:
                open(page, "w", encoding="utf-8").write(s2)
    json.dump(cal, open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"generate_column_banners: {made}枚を作成")


if __name__ == "__main__":
    main()
