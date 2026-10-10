# -*- coding: utf-8 -*-
"""
生成 Docsify 站点副本。

把中英两套 md 各复制一份到 site/en/ 与 site/zh/，并把所有文档压平到同一层，
同时改写链接与图片路径。这样 Docsify 只需最朴素的配置即可正确工作
（同级文档互链、图片统一 ../assets/img/），无需任何插件或 alias。

用法：python build-site.py
改完 md 后重新跑一次即可。
"""
import io
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

SOURCES = [
    # (源根目录, 源子目录列表, 输出目录)
    ("docs-en", ["", "docs"], "site/en"),
    ("中文版本", ["", "docs"], "site/zh"),
]

IMG_EXT = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
SRC_RE = re.compile(r'src="([^"]+)"')


def rewrite_path(path):
    """把源路径改写为压平后的站点内路径。"""
    if path.startswith(("http://", "https://", "mailto:", "#", "data:")):
        return None
    anchor = ""
    if "#" in path:
        path, anchor = path.split("#", 1)
        anchor = "#" + anchor
    low = path.lower()
    if low.endswith(IMG_EXT):
        idx = path.find("assets/img/")
        if idx >= 0:
            return "../" + path[idx:] + anchor
        return "../assets/img/" + os.path.basename(path) + anchor
    if low.endswith(".pdf"):
        return "../manual/" + os.path.basename(path)
    if low.endswith((".md", ".markdown")):
        return os.path.basename(path) + anchor
    return None


def rewrite_markdown(text):
    def link_sub(m):
        new = rewrite_path(m.group(1))
        return "](%s)" % new if new else m.group(0)

    def src_sub(m):
        new = rewrite_path(m.group(1))
        return 'src="%s"' % new if new else m.group(0)

    text = LINK_RE.sub(link_sub, text)
    text = SRC_RE.sub(src_sub, text)
    return text


def build(lang_root, subdirs, out_dir):
    out = os.path.join(ROOT, out_dir)
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)

    count = 0
    for sub in subdirs:
        src = os.path.join(ROOT, lang_root, sub) if sub else os.path.join(ROOT, lang_root)
        if not os.path.isdir(src):
            continue
        for name in sorted(os.listdir(src)):
            if not name.endswith(".md"):
                continue
            content = io.open(os.path.join(src, name), encoding="utf-8").read()
            io.open(os.path.join(out, name), "w", encoding="utf-8",
                    newline="\n").write(rewrite_markdown(content))
            count += 1
    return count


def build_sidebar(src_file, out_file):
    """从仓库根的侧边栏生成压平后的侧边栏。"""
    text = io.open(src_file, encoding="utf-8").read()
    text = LINK_RE.sub(lambda m: "](%s)" % (os.path.basename(m.group(1).split("#")[0]) +
                                            ("#" + m.group(1).split("#")[1] if "#" in m.group(1) else ""))
                       if m.group(1).endswith(".md") else m.group(0), text)
    io.open(out_file, "w", encoding="utf-8", newline="\n").write(text)


def fix_cross_language(out_dir, other_dir, target_prefix):
    """把指向另一语言文档的链接改为跨站跳转（压平后这些文件不在本目录）。"""
    other_names = set(f for f in os.listdir(other_dir) if f.endswith(".md"))
    changed = 0
    for name in sorted(os.listdir(out_dir)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(out_dir, name)
        text = io.open(path, encoding="utf-8").read()

        def sub(m):
            target = m.group(1)
            base = os.path.basename(target)
            if base in other_names and not os.path.exists(os.path.join(out_dir, base)):
                anchor = ""
                if "#" in target:
                    anchor = "#" + target.split("#", 1)[1]
                return "](%s%s%s)" % (target_prefix, base[:-3], anchor)
            return m.group(0)

        new = LINK_RE.sub(sub, text)
        if new != text:
            io.open(path, "w", encoding="utf-8", newline="\n").write(new)
            changed += 1
    return changed


def main():
    total = 0
    for lang_root, subdirs, out_dir in SOURCES:
        n = build(lang_root, subdirs, out_dir)
        total += n
        print("%-10s -> %-10s  %d files" % (lang_root, out_dir, n))

    build_sidebar(os.path.join(ROOT, "_sidebar.md"),
                  os.path.join(ROOT, "site", "en", "_sidebar.md"))
    build_sidebar(os.path.join(ROOT, "zh", "_sidebar.md"),
                  os.path.join(ROOT, "site", "zh", "_sidebar.md"))

    en_dir = os.path.join(ROOT, "site", "en")
    zh_dir = os.path.join(ROOT, "site", "zh")
    n1 = fix_cross_language(en_dir, zh_dir, "zh/#/")
    n2 = fix_cross_language(zh_dir, en_dir, "../#/")
    print("cross-language links fixed: en=%d zh=%d" % (n1, n2))
    print("total docs:", total)


if __name__ == "__main__":
    main()
