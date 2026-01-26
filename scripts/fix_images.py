#!/usr/bin/env python3
"""
图片修复脚本

作用：
- 修复缺失图片
- 修复“文件存在但损坏/过小/扩展名与真实格式不一致”等问题

注意：
- 需要联网访问原文链接
- 可能会更新 markdown 中的图片文件名（当真实格式与旧扩展名不一致时）
"""

import re
import json
import hashlib
import requests
import time
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from typing import Dict, Optional, Tuple, List

class ImageFixer:
    def __init__(self):
        self.content_dir = Path("content/posts")
        self.images_dir = Path("public/images/posts")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.fixed = 0
        self.failed = 0

    def _detect_image_kind(self, probe: bytes) -> str:
        if probe.startswith(b'\xff\xd8\xff'):
            return 'jpeg'
        if probe.startswith(b'\x89PNG\r\n\x1a\n'):
            return 'png'
        if probe.startswith(b'GIF87a') or probe.startswith(b'GIF89a'):
            return 'gif'
        if len(probe) >= 12 and probe[0:4] == b'RIFF' and probe[8:12] == b'WEBP':
            return 'webp'
        if len(probe) >= 12 and probe[4:8] == b'ftyp' and (b'avif' in probe[8:24] or b'avis' in probe[8:24]):
            return 'avif'
        s = probe.lstrip()
        if s.startswith(b'<!DOCTYPE html') or s.startswith(b'<html') or s.startswith(b'<head'):
            return 'html'
        if s.startswith(b'{') or s.startswith(b'['):
            return 'json'
        return 'unknown'

    def _kind_from_ext(self, ext: str) -> Optional[str]:
        e = (ext or '').lower()
        if e in ('.jpg', '.jpeg'):
            return 'jpeg'
        if e == '.png':
            return 'png'
        if e == '.gif':
            return 'gif'
        if e == '.webp':
            return 'webp'
        if e == '.avif':
            return 'avif'
        return None

    def _ext_for_kind(self, kind: str) -> Optional[str]:
        return {
            'jpeg': '.jpg',
            'png': '.png',
            'gif': '.gif',
            'webp': '.webp',
            'avif': '.avif',
        }.get(kind)

    def _read_head_tail(self, p: Path, head: int = 64, tail: int = 64) -> bytes:
        size = p.stat().st_size
        with p.open('rb') as f:
            h = f.read(head)
            if size <= head + tail:
                return h
            try:
                f.seek(max(0, size - tail))
                t = f.read(tail)
            except Exception:
                t = b''
        return h + t

    def _is_valid_image_file(self, p: Path, kind: str) -> bool:
        try:
            size = p.stat().st_size
            if size < 64:
                return False
            probe = self._read_head_tail(p)
            if kind == 'jpeg':
                return probe.startswith(b'\xff\xd8') and probe.endswith(b'\xff\xd9')
            if kind == 'png':
                return probe.startswith(b'\x89PNG\r\n\x1a\n') and (b'IEND' in probe)
            if kind == 'gif':
                return (probe.startswith(b'GIF87a') or probe.startswith(b'GIF89a')) and probe.endswith(b'\x3b')
            if kind == 'webp':
                if len(probe) < 12 or probe[0:4] != b'RIFF' or probe[8:12] != b'WEBP':
                    return False
                try:
                    riff_size = int.from_bytes(probe[4:8], 'little')
                    return (riff_size + 8) <= (size + 16)
                except Exception:
                    return True
            if kind == 'avif':
                return len(probe) >= 12 and probe[4:8] == b'ftyp'
            return False
        except Exception:
            return False
    
    def load_problem_files(self):
        """从健康报告加载有图片问题的文件"""
        report_path = Path("data/article_health_report.json")
        if not report_path.exists():
            print("请先运行 article_health_check.py")
            return []
        
        report = json.load(open(report_path, encoding='utf-8'))
        files = set()
        for issue in report['issues']:
            if issue['type'] in {
                'missing_image',
                'image_too_small',
                'image_not_image',
                'image_unknown_type',
                'image_type_mismatch',
                'image_possibly_truncated',
                'image_read_error',
            }:
                files.add(issue['file'])
        return list(files)
    
    def get_source_url(self, md_file: Path) -> str:
        """从文章提取原文链接"""
        content = md_file.read_text(encoding='utf-8')
        match = re.search(r'source_url:\s*["\']?([^"\'\n]+)', content)
        if match:
            return match.group(1).strip()
        return None
    
    def get_problem_images(self, md_file: Path) -> list:
        """获取文章中缺失/损坏/格式不匹配的图片"""
        content = md_file.read_text(encoding='utf-8')
        problems = []
        
        for match in re.finditer(r'!\[[^\]]*\]\((/images/posts/([^)]+))\)', content):
            full_path, filename = match.groups()
            img_path = self.images_dir / filename
            if not img_path.exists():
                problems.append({'path': full_path, 'filename': filename, 'reason': 'missing'})
                continue

            try:
                size = img_path.stat().st_size
                probe = self._read_head_tail(img_path)
                kind = self._detect_image_kind(probe)
                ext_kind = self._kind_from_ext(img_path.suffix)

                if size < 1024:
                    problems.append({'path': full_path, 'filename': filename, 'reason': f'too_small({size})'})
                    continue

                if kind in ('html', 'json', 'unknown'):
                    problems.append({'path': full_path, 'filename': filename, 'reason': f'not_image({kind})'})
                    continue

                if ext_kind and ext_kind != kind:
                    problems.append({'path': full_path, 'filename': filename, 'reason': f'mismatch({ext_kind}->{kind})'})
                    continue

                if not self._is_valid_image_file(img_path, kind):
                    problems.append({'path': full_path, 'filename': filename, 'reason': 'possibly_truncated'})
                    continue
            except Exception as e:
                problems.append({'path': full_path, 'filename': filename, 'reason': f'read_error({e})'})
        
        return problems
    
    def _pick_best_from_srcset(self, srcset: str) -> Optional[str]:
        best_url = None
        best_score = -1.0
        for part in srcset.split(','):
            item = part.strip()
            if not item:
                continue
            pieces = item.split()
            url = pieces[0]
            score = 0.0
            if len(pieces) >= 2:
                d = pieces[1].strip()
                try:
                    if d.endswith('w'):
                        score = float(d[:-1])
                    elif d.endswith('x'):
                        score = float(d[:-1]) * 10000.0
                except Exception:
                    score = 0.0
            if score >= best_score:
                best_score = score
                best_url = url
        return best_url

    def _extract_all_from_srcset(self, srcset: str) -> List[str]:
        urls: List[str] = []
        for part in srcset.split(','):
            item = part.strip()
            if not item:
                continue
            pieces = item.split()
            if not pieces:
                continue
            urls.append(pieces[0])
        return urls

    def fetch_original_images(self, source_url: str) -> Dict[str, str]:
        """从原文获取图片 hash -> URL 映射（hash = md5(absolute_url)[:12]）"""
        try:
            resp = self.session.get(source_url, timeout=30, headers={'Referer': source_url})
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            images: Dict[str, str] = {}
            for img in soup.find_all('img'):
                candidates: List[str] = []

                # 1) srcset：把所有候选都纳入（历史文章的 hash 可能来自 src，不一定来自最大图）
                for key in ['srcset', 'data-srcset']:
                    srcset = img.get(key)
                    if srcset:
                        candidates.extend(self._extract_all_from_srcset(srcset))

                # 2) 常见字段：都纳入
                for key in ['src', 'data-src', 'data-lazy-src', 'data-original', 'data-url']:
                    v = img.get(key)
                    if v:
                        candidates.append(v)

                # 去重 + 过滤无效
                seen = set()
                clean: List[str] = []
                for c in candidates:
                    if not c:
                        continue
                    c = c.strip()
                    if not c or c in seen:
                        continue
                    seen.add(c)
                    cl = c.lower()
                    if cl.startswith('data:') or '.svg' in cl:
                        continue
                    clean.append(c)

                for src in clean:
                    full_url = urljoin(source_url, src)
                    img_hash = hashlib.md5(full_url.encode()).hexdigest()[:12]
                    # 只存第一条命中的 URL（够用；下载时会按真实格式落盘）
                    images.setdefault(img_hash, full_url)
            
            return images
        except Exception as e:
            print(f"    获取原文失败: {e}")
            return {}
    
    def download_image(self, url: str, referer: Optional[str] = None) -> Tuple[bool, Optional[Path], Optional[str]]:
        """
        下载单张图片，按真实格式落盘。
        返回 (ok, saved_path, kind)
        """
        try:
            headers = {'Accept': 'image/avif,image/webp,image/*,*/*;q=0.8'}
            if referer:
                headers['Referer'] = referer
            resp = self.session.get(url, timeout=30, headers=headers)
            resp.raise_for_status()
            
            data = resp.content
            if not data or len(data) < 256:
                return False, None, None

            probe = data[:64] + data[-64:]
            kind = self._detect_image_kind(probe)
            ext = self._ext_for_kind(kind)
            if not ext:
                ct = (resp.headers.get('content-type') or '').lower()
                if 'image/jpeg' in ct:
                    kind, ext = 'jpeg', '.jpg'
                elif 'image/png' in ct:
                    kind, ext = 'png', '.png'
                elif 'image/gif' in ct:
                    kind, ext = 'gif', '.gif'
                elif 'image/webp' in ct:
                    kind, ext = 'webp', '.webp'
                elif 'image/avif' in ct:
                    kind, ext = 'avif', '.avif'

            if not ext or kind in ('html', 'json', 'unknown'):
                return False, None, None

            # 文件名以 url hash 为主（与 ContentExtractorV2 保持一致）
            img_hash = hashlib.md5(url.encode()).hexdigest()[:12]
            save_path = self.images_dir / f"{img_hash}{ext}"
            save_path.write_bytes(data)
            return True, save_path, kind
        except:
            return False, None, None
    
    def fix_article(self, filename: str) -> dict:
        """修复单篇文章的图片"""
        md_file = self.content_dir / filename
        if not md_file.exists():
            return {'status': 'not_found'}
        
        md_text = md_file.read_text(encoding='utf-8')

        # 获取问题图片（缺失/损坏/格式错）
        problems = self.get_problem_images(md_file)
        if not problems:
            return {'status': 'no_problem', 'fixed': 0}
        
        # 获取原文链接
        source_url = self.get_source_url(md_file)
        if not source_url:
            return {'status': 'no_source_url', 'missing': len(problems)}
        
        print(f"  原文: {source_url}")
        print(f"  问题图片: {len(problems)} 张")
        
        # 从原文获取图片
        original_images = self.fetch_original_images(source_url)
        if not original_images:
            return {'status': 'fetch_failed', 'missing': len(problems)}
        
        # 下载并在必要时更新 markdown 引用（扩展名可能变化）
        fixed_count = 0
        for img in problems:
            old_filename = img['filename']
            base_hash = Path(old_filename).stem  # 12位 hash

            url = original_images.get(base_hash)
            if not url:
                print(f"    ? {old_filename} 未在原文找到（hash={base_hash}）")
                continue

            ok, saved_path, kind = self.download_image(url, referer=source_url)
            if not ok or not saved_path:
                print(f"    ✗ {old_filename} 下载失败")
                continue

            new_filename = saved_path.name
            if new_filename != old_filename:
                md_text = md_text.replace(f"/images/posts/{old_filename}", f"/images/posts/{new_filename}")
                print(f"    ✓ {old_filename} -> {new_filename} ({kind})")
            else:
                print(f"    ✓ {old_filename} ({kind})")
            fixed_count += 1

        if fixed_count > 0:
            md_file.write_text(md_text, encoding='utf-8')

        return {'status': 'ok', 'fixed': fixed_count, 'missing': len(problems)}
    
    def fix_all(self):
        """修复所有有问题的文章"""
        files = self.load_problem_files()
        print(f"找到 {len(files)} 篇需要修复图片的文章\n")
        
        for i, filename in enumerate(files):
            print(f"[{i+1}/{len(files)}] {filename}")
            result = self.fix_article(filename)
            
            if result.get('fixed', 0) > 0:
                self.fixed += result['fixed']
            if result.get('status') == 'fetch_failed':
                self.failed += result.get('missing', 0)
            
            time.sleep(1)  # 避免请求过快
            print()
        
        print("=" * 50)
        print(f"修复完成！")
        print(f"  成功下载: {self.fixed} 张图片")
        print(f"  失败: {self.failed} 张")


if __name__ == "__main__":
    fixer = ImageFixer()
    fixer.fix_all()
