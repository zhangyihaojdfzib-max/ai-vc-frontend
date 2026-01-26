#!/usr/bin/env python3
"""
normalize_images.py

目标：
1) 修复历史遗留：图片内容格式 != 文件扩展名（最常见的“乱码/不显示/显示一半”根因）
2) 同步更新 markdown 中的引用路径（/images/posts/<filename>）

默认 dry-run，只打印计划执行的变更；加 --apply 才会真正修改文件。

用法：
  python scripts/normalize_images.py
  python scripts/normalize_images.py --apply
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, Optional, Tuple


def read_head_tail(p: Path, head: int = 64, tail: int = 64) -> bytes:
    size = p.stat().st_size
    with p.open("rb") as f:
        h = f.read(head)
        if size <= head + tail:
            return h
        try:
            f.seek(max(0, size - tail))
            t = f.read(tail)
        except Exception:
            t = b""
    return h + t


def detect_image_kind(probe: bytes) -> str:
    # JPEG
    if probe.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    # PNG
    if probe.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    # GIF
    if probe.startswith(b"GIF87a") or probe.startswith(b"GIF89a"):
        return "gif"
    # WebP
    if len(probe) >= 12 and probe[0:4] == b"RIFF" and probe[8:12] == b"WEBP":
        return "webp"
    # AVIF
    if len(probe) >= 12 and probe[4:8] == b"ftyp" and (b"avif" in probe[8:24] or b"avis" in probe[8:24]):
        return "avif"

    s = probe.lstrip()
    if s.startswith(b"<!DOCTYPE html") or s.startswith(b"<html") or s.startswith(b"<head"):
        return "html"
    if s.startswith(b"{") or s.startswith(b"["):
        return "json"
    return "unknown"


def kind_from_ext(ext: str) -> Optional[str]:
    e = (ext or "").lower()
    if e in (".jpg", ".jpeg"):
        return "jpeg"
    if e == ".png":
        return "png"
    if e == ".gif":
        return "gif"
    if e == ".webp":
        return "webp"
    if e == ".avif":
        return "avif"
    if e == ".svg":
        return "svg"
    return None


def canonical_ext_for_kind(kind: str) -> Optional[str]:
    return {
        "jpeg": ".jpg",
        "png": ".png",
        "gif": ".gif",
        "webp": ".webp",
        "avif": ".avif",
    }.get(kind)


def is_valid_image_file(p: Path, kind: str) -> bool:
    """
    不引入第三方依赖的轻量校验：
    - jpeg/png/gif 通过尾部终止符做截断判断
    - webp 通过 RIFF size 字段与文件大小做粗校验
    - avif 仅做 ftyp 存在性校验（更严格需要解码库）
    """
    try:
        size = p.stat().st_size
        if size < 64:
            return False
        probe = read_head_tail(p)
        if kind == "jpeg":
            return probe.startswith(b"\xff\xd8") and probe.endswith(b"\xff\xd9")
        if kind == "png":
            return probe.startswith(b"\x89PNG\r\n\x1a\n") and (b"IEND" in probe)
        if kind == "gif":
            return (probe.startswith(b"GIF87a") or probe.startswith(b"GIF89a")) and probe.endswith(b"\x3b")
        if kind == "webp":
            if len(probe) < 12 or probe[0:4] != b"RIFF" or probe[8:12] != b"WEBP":
                return False
            try:
                riff_size = int.from_bytes(probe[4:8], "little")
                return (riff_size + 8) <= (size + 16)
            except Exception:
                return True
        if kind == "avif":
            return len(probe) >= 12 and probe[4:8] == b"ftyp"
        return False
    except Exception:
        return False


def build_rename_map(images_dir: Path) -> Tuple[Dict[str, str], Dict[str, int]]:
    rename: Dict[str, str] = {}
    stats = {
        "total": 0,
        "ok": 0,
        "mismatch": 0,
        "unknown": 0,
        "not_image": 0,
        "too_small": 0,
        "conflict": 0,
    }

    for p in images_dir.iterdir():
        if not p.is_file():
            continue
        stats["total"] += 1

        size = p.stat().st_size
        if size < 1024:
            stats["too_small"] += 1

        probe = read_head_tail(p)
        kind = detect_image_kind(probe)
        if kind in ("html", "json"):
            stats["not_image"] += 1
            continue
        if kind == "unknown":
            stats["unknown"] += 1
            continue

        ext_kind = kind_from_ext(p.suffix)
        desired_ext = canonical_ext_for_kind(kind)
        if not desired_ext:
            stats["unknown"] += 1
            continue

        # ".jpeg" 与 ".jpg" 视为一致（统一到 .jpg）
        if ext_kind == kind and p.suffix.lower() == desired_ext:
            stats["ok"] += 1
            continue
        if ext_kind == kind and p.suffix.lower() in (".jpg", ".jpeg") and desired_ext == ".jpg":
            # 统一 jpeg 扩展名
            if p.suffix.lower() == ".jpeg":
                new_name = f"{p.stem}{desired_ext}"
                target = images_dir / new_name
                if target.exists():
                    stats["conflict"] += 1
                else:
                    rename[p.name] = new_name
                    stats["mismatch"] += 1
            else:
                stats["ok"] += 1
            continue

        if ext_kind != kind:
            new_name = f"{p.stem}{desired_ext}"
            target = images_dir / new_name
            if target.exists():
                # 已存在正确扩展名的文件：仅在目标文件“看起来有效”时才更新引用
                stats["conflict"] += 1
                if is_valid_image_file(target, kind):
                    rename[p.name] = new_name
            else:
                rename[p.name] = new_name
            stats["mismatch"] += 1
            continue

        stats["ok"] += 1

    return rename, stats


IMG_REF_RE = re.compile(r"(/images/posts/([0-9a-f]{12})(\.[a-z0-9]+))", re.IGNORECASE)


def build_best_by_stem(images_dir: Path, rename: Dict[str, str]) -> Dict[str, str]:
    """
    给每个 stem(12位hash)选一个“最可能正确”的现存文件名，用于修复 md 中引用了不存在扩展名的情况。
    规则（优先级从高到低）：
    - 文件可识别且轻量校验通过
    - 扩展名与识别类型一致（canonical）
    - 文件更大（通常更可能是原图/非占位）
    """
    best: Dict[str, Tuple[str, int, bool]] = {}  # stem -> (filename, size, is_canonical)

    for p in images_dir.iterdir():
        if not p.is_file():
            continue
        # 关键：按“重命名后的名字”评估（否则会和 markdown 替换互相抵消）
        effective_name = rename.get(p.name, p.name)
        stem = Path(effective_name).stem.lower()
        size = p.stat().st_size
        probe = read_head_tail(p)
        kind = detect_image_kind(probe)
        if kind in ("html", "json", "unknown"):
            continue
        if not is_valid_image_file(p, kind):
            continue

        desired_ext = canonical_ext_for_kind(kind)
        is_canonical = desired_ext is not None and Path(effective_name).suffix.lower() == desired_ext

        prev = best.get(stem)
        if not prev:
            best[stem] = (effective_name, size, is_canonical)
            continue

        prev_name, prev_size, prev_canonical = prev
        # canonical 胜出
        if is_canonical and not prev_canonical:
            best[stem] = (effective_name, size, is_canonical)
            continue
        # 同 canonical 情况下选更大
        if is_canonical == prev_canonical and size > prev_size:
            best[stem] = (effective_name, size, is_canonical)
            continue

    return {stem: v[0] for stem, v in best.items()}


def apply_markdown_updates(content_dir: Path, images_dir: Path, rename: Dict[str, str], apply: bool) -> Tuple[int, int]:
    """
    返回 (被修改的 markdown 文件数量, 被修复的缺失引用数量)（dry-run 模式下也会统计“将会修改”）。
    """
    changed_files = 0
    fixed_missing_refs = 0

    # 按“应用后”的文件集合判断存在性：existing - old + new
    existing_files = {p.name for p in images_dir.iterdir() if p.is_file()}
    effective_files = set(existing_files)
    for old, new in rename.items():
        effective_files.discard(old)
        effective_files.add(new)

    best_by_stem = build_best_by_stem(images_dir, rename)

    md_files = list(content_dir.glob("*.md"))
    for md in md_files:
        text = md.read_text(encoding="utf-8")
        new_text = text
        for old, new in rename.items():
            new_text = new_text.replace(f"/images/posts/{old}", f"/images/posts/{new}")

        # 修复：md 引用的文件不存在，但同 stem 有别的扩展名文件存在
        def repl(m: re.Match) -> str:
            nonlocal fixed_missing_refs
            full = m.group(1)
            stem = m.group(2).lower()
            filename = f"{stem}{m.group(3).lower()}"
            # 这里必须用 effective_files（否则 dry-run 会把 planned rename 又改回去）
            if filename in effective_files:
                return full
            best_name = best_by_stem.get(stem)
            if not best_name:
                return full
            fixed_missing_refs += 1
            return f"/images/posts/{best_name}"

        new_text = IMG_REF_RE.sub(repl, new_text)

        if new_text != text:
            changed_files += 1
            if apply:
                md.write_text(new_text, encoding="utf-8")
    return changed_files, fixed_missing_refs


def apply_renames(images_dir: Path, rename: Dict[str, str]) -> Tuple[int, int]:
    renamed = 0
    skipped = 0
    for old, new in rename.items():
        src = images_dir / old
        dst = images_dir / new
        if not src.exists():
            skipped += 1
            continue
        if dst.exists():
            # 只更新引用，不覆盖已有文件
            skipped += 1
            continue
        src.rename(dst)
        renamed += 1
    return renamed, skipped


def main():
    parser = argparse.ArgumentParser(description="Normalize local image extensions and update markdown references.")
    parser.add_argument("--apply", action="store_true", help="Actually perform renames and markdown edits.")
    parser.add_argument("--content-dir", default="content/posts", help="Markdown directory (default: content/posts).")
    parser.add_argument("--images-dir", default="public/images/posts", help="Images directory (default: public/images/posts).")
    args = parser.parse_args()

    content_dir = Path(args.content_dir)
    images_dir = Path(args.images_dir)
    if not content_dir.exists():
        raise SystemExit(f"content dir not found: {content_dir}")
    if not images_dir.exists():
        raise SystemExit(f"images dir not found: {images_dir}")

    rename, stats = build_rename_map(images_dir)
    print("=== normalize_images.py ===")
    print(f"mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"images_dir: {images_dir}")
    print(f"content_dir: {content_dir}")
    print(f"stats: {stats}")
    print(f"planned renames: {len(rename)}")

    # 先更新 markdown（避免先改名导致引用暂时断裂）
    changed_md, fixed_missing_refs = apply_markdown_updates(content_dir, images_dir, rename, apply=args.apply)
    print(f"markdown files to update: {changed_md}")
    print(f"missing refs auto-fixed (same stem, different ext): {fixed_missing_refs}")

    if rename and args.apply:
        renamed, skipped = apply_renames(images_dir, rename)
        print(f"renamed images: {renamed}, skipped: {skipped} (skipped usually means conflict/target exists)")

    # 打印少量样例
    if rename:
        print("\nexamples (up to 20):")
        for i, (old, new) in enumerate(rename.items()):
            if i >= 20:
                break
            print(f"  {old} -> {new}")


if __name__ == "__main__":
    main()

