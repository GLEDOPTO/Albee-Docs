# -*- coding: utf-8 -*-
"""
生成 Docsify 站点副本。

把中英两套 md 各复制一份到 site/en/ 与 site/zh/，并把所有文档压平到同一层，
同时改写链接、图片路径与锚点。这样 Docsify 只需最朴素的配置即可正确工作
（同级文档互链、图片统一 assets/img/），无需任何插件或 alias。

用法：python build-site.py
改完 md 后重新跑一次即可（仓库里也配了 GitHub Actions 自动跑）。
"""
import io
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

REPO_URL = "https://github.com/GLEDOPTO/Albee-Docs"

SOURCES = [
    # (源根目录, 源子目录列表, 输出目录, 资源前缀)
    # 资源（图片/PDF/xlsx）由浏览器按页面 URL 解析，不是 Docsify 的 basePath：
    # 英文站页面在 /Albee-Docs/     -> 前缀 ""
    # 中文站页面在 /Albee-Docs/zh/  -> 前缀 "../"
    ("docs-en", ["", "docs"], "site/en", ""),
    ("中文版本", ["", "docs"], "site/zh", "../"),
]

IMG_EXT = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
SRC_RE = re.compile(r'src="([^"]+)"')
HEAD_RE = re.compile(r"^#{1,6}\s+(.*)$", re.M)

# Docsify slugify 的剥离字符集（src/core/render/slugify.js）。
# 注意：中文顿号「、」(U+3001) 不在此集合内，所以不会被剥掉。
STRIP_RE = re.compile(
    u"[\u2000-\u206F\u2E00-\u2E7F\\\\'!\"#$%&()*+,./:;<=>?@\\[\\]^`{|}~]"
)
# 归一化：只保留字母、数字、汉字，用于跨规则比对锚点
KEEP_RE = re.compile(u"[^0-9A-Za-z\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


def docsify_slug(text):
    """复刻 Docsify slugify：小写化 -> 去标签 -> 去标点 -> 空格转连字符
    -> 折叠重复连字符 -> 数字开头补下划线。"""
    slug = text.strip()
    slug = re.sub(r"[A-Z]+", lambda m: m.group(0).lower(), slug)
    slug = re.sub(r"<[^>]+>", "", slug)
    slug = STRIP_RE.sub("", slug)
    slug = re.sub(r"\s", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = re.sub(r"^(\d)", r"_\1", slug)
    return slug


def norm_key(s):
    """压成「只留字数字与汉字」的小写串，用于把 GitHub 风格锚点对上 Docsify slug。"""
    return KEEP_RE.sub("", s).lower()


def collect_anchors(lang_root, subdirs):
    """扫描源 md，得到 {页面名: {归一化键: 该页真实 slug}}。

    文档里的目录锚点是按 GitHub 风格写的（"1-getting-started"、
    "一按键与操作"），而 Docsify 生成的 id 是另一套规则
    （"_1-getting-started"、"一、按键与操作"）。直接照搬会点不动，
    因此这里先算出每页真实 slug，再按归一化键建立映射。
    """
    pages = {}
    for sub in subdirs:
        src = os.path.join(ROOT, lang_root, sub) if sub else os.path.join(ROOT, lang_root)
        if not os.path.isdir(src):
            continue
        for name in sorted(os.listdir(src)):
            if not name.endswith(".md"):
                continue
            text = io.open(os.path.join(src, name), encoding="utf-8").read()
            mapping = {}
            seen = {}
            for head in HEAD_RE.findall(text):
                slug = docsify_slug(head)
                n = seen.get(slug, 0)
                seen[slug] = n + 1
                real = slug if n == 0 else "%s-%d" % (slug, n)
                # 首次出现优先，重复标题不去覆盖
                mapping.setdefault(norm_key(slug), real)
                mapping.setdefault(norm_key(real), real)
            pages[name[:-3]] = mapping
    return pages


def resolve_anchor(anchor, page, anchors):
    """把文档里写的锚点换成该页真实的 Docsify slug；对不上就原样保留。"""
    return (anchors.get(page) or {}).get(norm_key(anchor), anchor)


def split_anchor(target):
    """拆出链接里的锚点；Docsify 路由 "#/xxx" 不拆。"""
    if target.startswith("#/"):
        return target, ""
    if "#" in target:
        base, anchor = target.split("#", 1)
        return base, anchor
    return target, ""


def rewrite_path(path, res_prefix):
    """把源路径改写为压平后的站点内路径。返回 (新路径, 是否资源文件)。

    资源文件（图片/PDF/xlsx）的【链接】若不处理，Docsify 的 linkCompiler
    会把它交给 router.toURL 变成 "#/..." 页面路由，点击后 404。
    因此 link_sub 对资源文件追加 " :ignore"（Docsify 官方配置），
    让它按普通外链（target=_blank）交给浏览器解析。
    """
    if path.startswith(("http://", "https://", "mailto:", "#", "data:")):
        return None, False
    anchor = ""
    if "#" in path:
        path, anchor = path.split("#", 1)
        anchor = "#" + anchor
    # 指向 assets 目录本身的链接：线上站没有目录页，改指仓库目录（绝对 URL 天然不被编译）
    segs = [s for s in path.split("/") if s not in ("", ".", "..")]
    if segs == ["assets"] or segs == ["assets", "img"]:
        return REPO_URL + "/tree/master/" + "/".join(segs), False
    low = path.lower()
    if low.endswith(IMG_EXT):
        idx = path.find("assets/img/")
        if idx >= 0:
            return res_prefix + path[idx:] + anchor, True
        return res_prefix + "assets/img/" + os.path.basename(path) + anchor, True
    if low.endswith((".pdf", ".xlsx")):
        idx = path.find("assets/")
        if idx >= 0:
            return res_prefix + path[idx:], True
        return res_prefix + "manual/" + os.path.basename(path), True
    if low.endswith((".md", ".markdown")):
        return os.path.basename(path) + anchor, False
    return None, False


def rewrite_markdown(text, res_prefix, page_name, anchors):
    def link_sub(m):
        target = m.group(1)
        base, anchor = split_anchor(target)

        if anchor:
            # 统一写成 "<目标页>.md?id=<真实 slug>"。
            # 不能写成 "#/page?id=x"：Docsify 的 History.toURL 对 "#" 开头
            # 走 local 分支，会把整串塞进当前页，跳成
            # #/当前页?id=/page?id=x，等于没跳。
            if base == "":
                out_base = page_name + ".md"
                page = page_name
            elif base.lower().endswith((".md", ".markdown")):
                out_base = os.path.basename(base)
                page = out_base.rsplit(".", 1)[0]
            else:
                new, is_res = rewrite_path(target, res_prefix)
                if new is None:
                    return m.group(0)
                return "](%s \":ignore\")" % new if is_res else "](%s)" % new
            return "](%s?id=%s)" % (out_base, resolve_anchor(anchor, page, anchors))

        new, is_res = rewrite_path(target, res_prefix)
        if new is None:
            return m.group(0)
        # 资源链接追加 " :ignore"：Docsify 不编译、按外链新窗口打开，
        # 否则会被当成 "#/..." 页面路由而 404。
        return "](%s \":ignore\")" % new if is_res else "](%s)" % new

    def src_sub(m):
        new, _ = rewrite_path(m.group(1), res_prefix)
        return 'src="%s"' % new if new else m.group(0)

    text = LINK_RE.sub(link_sub, text)
    text = SRC_RE.sub(src_sub, text)
    return text


def build(lang_root, subdirs, out_dir, res_prefix, anchors):
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
                    newline="\n").write(
                rewrite_markdown(content, res_prefix, name[:-3], anchors))
            count += 1
    return count


def build_sidebar(src_file, out_file, anchors):
    """从仓库根的侧边栏生成压平后的侧边栏（锚点同样做 slug 修正）。"""
    text = io.open(src_file, encoding="utf-8").read()

    def sub(m):
        target = m.group(1)
        base, anchor = split_anchor(target)
        if not base.lower().endswith(".md"):
            return m.group(0)
        out_base = os.path.basename(base)
        if anchor:
            page = out_base[:-3]
            return "](%s?id=%s)" % (out_base, resolve_anchor(anchor, page, anchors))
        return "](%s)" % out_base

    text = LINK_RE.sub(sub, text)
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
            base = os.path.basename(target.split("?")[0].split("#")[0])
            if base in other_names and not os.path.exists(os.path.join(out_dir, base)):
                query = ""
                if "?" in target:
                    query = "?" + target.split("?", 1)[1]
                return "](%s%s%s)" % (target_prefix, base[:-3], query)
            return m.group(0)

        new = LINK_RE.sub(sub, text)
        if new != text:
            io.open(path, "w", encoding="utf-8", newline="\n").write(new)
            changed += 1
    return changed


def main():
    total = 0
    for lang_root, subdirs, out_dir, res_prefix in SOURCES:
        anchors = collect_anchors(lang_root, subdirs)
        n = build(lang_root, subdirs, out_dir, res_prefix, anchors)
        total += n
        print("%-10s -> %-10s  %d files" % (lang_root, out_dir, n))
        globals().setdefault("_ANCHORS", {})[out_dir] = anchors

    en_anchors = _ANCHORS["site/en"]
    zh_anchors = _ANCHORS["site/zh"]

    build_sidebar(os.path.join(ROOT, "_sidebar.md"),
                  os.path.join(ROOT, "site", "en", "_sidebar.md"), en_anchors)
    build_sidebar(os.path.join(ROOT, "zh", "_sidebar.md"),
                  os.path.join(ROOT, "site", "zh", "_sidebar.md"), zh_anchors)

    en_dir = os.path.join(ROOT, "site", "en")
    zh_dir = os.path.join(ROOT, "site", "zh")
    n1 = fix_cross_language(en_dir, zh_dir, "zh/#/")
    n2 = fix_cross_language(zh_dir, en_dir, "../#/")
    print("cross-language links fixed: en=%d zh=%d" % (n1, n2))
    print("total docs:", total)


if __name__ == "__main__":
    main()
