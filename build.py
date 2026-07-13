#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描 photos/ 文件夹,生成缩略图(thumbs/)和照片清单(photos.js)。

用法: python build.py
依赖: pip install Pillow

规则:
- photos/ 下的一级子文件夹名 = 分类名(会显示在网站导航里)
- 直接放在 photos/ 根目录的图片只出现在"全部"里
- 支持 jpg / jpeg / png / webp
- 照片按拍摄时间(EXIF)倒序排列,没有拍摄时间的按文件名排
- 文件名若不是相机默认命名(如 DSC_0001),会作为图片标题显示在灯箱里
"""
import json
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("缺少 Pillow,请先运行: pip install Pillow")

ROOT = Path(__file__).resolve().parent
PHOTOS_DIR = ROOT / "photos"
THUMBS_DIR = ROOT / "thumbs"
ORIGINALS_DIR = ROOT / "originals"   # 放同名原图 -> 灯箱出现"下载原图"按钮
SITE_JSON = ROOT / "site.json"
OUT_JS = ROOT / "photos.js"

EXTS = {".jpg", ".jpeg", ".png", ".webp"}
THUMB_MAX_EDGE = 900          # 缩略图长边像素
THUMB_QUALITY = 82            # 缩略图 JPEG 质量

# 相机/手机默认文件名模式 -> 不作为标题显示
BORING = re.compile(
    r"^(dsc|dscf|dsc_|img|img_|_mg|dji|gopr|pxl|mmexport|wx_camera|screenshot|photo|p\d{3,}|\d[\d\s_-]*)",
    re.IGNORECASE,
)


def exif_datetime(img):
    """尽力读取拍摄时间,失败返回空串。"""
    try:
        ex = img.getexif()
        dt = None
        try:
            dt = ex.get_ifd(0x8769).get(36867)  # DateTimeOriginal
        except Exception:
            pass
        if not dt:
            dt = ex.get(306)  # DateTime
        return str(dt) if dt else ""
    except Exception:
        return ""


def title_from(filename):
    stem = Path(filename).stem.replace("_", " ").replace("-", " ").strip()
    if not stem or BORING.match(stem):
        return ""
    return stem


def build():
    if not PHOTOS_DIR.is_dir():
        PHOTOS_DIR.mkdir(parents=True)
        print("已创建空的 photos/ 文件夹,把照片放进去后重新运行。")

    site = {}
    if SITE_JSON.is_file():
        try:
            site = json.loads(SITE_JSON.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"警告: site.json 解析失败({e}),将使用默认信息。")

    THUMBS_DIR.mkdir(exist_ok=True)

    entries = []
    valid_thumbs = set()

    files = [p for p in sorted(PHOTOS_DIR.rglob("*")) if p.suffix.lower() in EXTS and p.is_file()]

    for src in files:
        rel = src.relative_to(PHOTOS_DIR)
        cat = rel.parts[0] if len(rel.parts) > 1 else ""

        try:
            with Image.open(src) as im:
                im = ImageOps.exif_transpose(im)
                w, h = im.size
                shot = exif_datetime(im)

                thumb_rel = rel.with_suffix(".jpg")
                thumb_path = THUMBS_DIR / thumb_rel
                valid_thumbs.add(thumb_path)

                need = (not thumb_path.exists()) or (src.stat().st_mtime > thumb_path.stat().st_mtime)
                if need:
                    thumb_path.parent.mkdir(parents=True, exist_ok=True)
                    t = im.copy()
                    t.thumbnail((THUMB_MAX_EDGE, THUMB_MAX_EDGE), Image.LANCZOS)
                    if t.mode in ("RGBA", "P", "LA"):
                        bg = Image.new("RGB", t.size, (255, 255, 255))
                        bg.paste(t, mask=t.convert("RGBA").split()[-1])
                        t = bg
                    elif t.mode != "RGB":
                        t = t.convert("RGB")
                    t.save(thumb_path, "JPEG", quality=THUMB_QUALITY, optimize=True, progressive=True)
        except Exception as e:
            print(f"跳过 {rel}(无法处理: {e})")
            continue

        entry = {
            "src": "photos/" + rel.as_posix(),
            "thumb": "thumbs/" + thumb_rel.as_posix(),
            "w": w,
            "h": h,
            "c": cat,
            "t": title_from(src.name),
            "d": shot,
        }
        if (ORIGINALS_DIR / rel).is_file():
            entry["o"] = "originals/" + rel.as_posix()
        entries.append(entry)

    # 清理已删除照片的缩略图
    removed = 0
    for t in list(THUMBS_DIR.rglob("*.jpg")):
        if t not in valid_thumbs:
            t.unlink()
            removed += 1
    for d in sorted(THUMBS_DIR.rglob("*"), reverse=True):
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()

    # 排序: 有拍摄时间的按时间倒序,其余按文件名倒序排在后面
    entries.sort(key=lambda e: (e["d"] or "0000", e["src"]), reverse=True)

    js = (
        "// 本文件由 build.py 自动生成,请勿手动编辑\n"
        f"window.SITE = {json.dumps(site, ensure_ascii=False)};\n"
        f"window.PHOTOS = {json.dumps(entries, ensure_ascii=False)};\n"
    )
    OUT_JS.write_text(js, encoding="utf-8")

    cats = sorted({e["c"] for e in entries if e["c"]})
    n_orig = sum(1 for e in entries if "o" in e)
    print(f"完成: {len(entries)} 张照片,{len(cats)} 个分类 {cats},{n_orig} 张有原图,清理旧缩略图 {removed} 张。")


if __name__ == "__main__":
    build()
