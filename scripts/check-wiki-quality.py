#!/usr/bin/env python3
"""
wiki quality check — 自检 5 项
1. 死链(0 真)
2. 索引同步
3. frontmatter 9 字段
4. log.md 24h 内更新
5. 总大小 < 10 MB

Usage:
    python3 scripts/check-wiki-quality.py
    python3 scripts/check-wiki-quality.py --strict  # CI 模式:任何 ERROR 退出 1
    python3 scripts/check-wiki-quality.py --json    # 输出 JSON
"""
import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# === 配置 ===
WIKI_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FRONTMATTER = {
    "title", "created", "updated", "type", "tags"
}  # source(单数)也算通过 — 因为 wiki 实际用单数
SOURCE_FIELD_ALIASES = {"source", "sources"}
LOG_FILE = WIKI_ROOT / "log.md"
INDEX_FILE = WIKI_ROOT / "index.md"
SKIP_DIRS = {".git", ".obsidian", ".claude", ".claudian", ".codegraph",
             ".trash", "_archive", "raw"}
# 2026-06-04 v6.x 排除 agents/ai-harness-exploration* (完整 skill 源码,含 wikilink 示例占位符 + 文档模板,不是 wiki content)
# 2026-06-04 v6.x 排除 agents/skills-github-gh-cli* (同样:skill 镜像,SKILL.md 含示例占位符)
# 2026-06-05 v6.x 排除 agents/skills-markitdown-converter* (同样:skill 镜像)
SKIP_PREFIXES = ("agents/ai-harness-exploration", "agents/skills-github-gh-cli", "agents/skills-markitdown-converter")
SIZE_LIMIT_MB = 10
LOG_FRESH_HOURS = 24

# === 工具 ===
def iter_md_files():
    """遍历所有 content .md(跳过 SKIP_DIRS 顶层目录)"""
    for root, dirs, files in os.walk(WIKI_ROOT):
        # 顶层目录跳过
        rel_root = Path(root).relative_to(WIKI_ROOT)
        top = rel_root.parts[0] if rel_root.parts else ""
        if top in SKIP_DIRS:
            dirs[:] = []
            continue
        # 跳过 _drafts 子目录
        dirs[:] = [d for d in dirs if d != "_drafts"]
        for f in files:
            if f.endswith(".md") and not f.startswith(".#"):
                p = Path(root) / f
                # 跳过 SKIP_PREFIXES 前缀(2026-06-04 排除 ai-harness-exploration 完整源码)
                rel_str = p.relative_to(WIKI_ROOT).as_posix()
                if any(rel_str.startswith(pref) for pref in SKIP_PREFIXES):
                    continue
                yield p

def get_frontmatter(path):
    """提取 YAML frontmatter,返回 dict"""
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return None, text
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[m.end():]

def find_wikilinks(text):
    """找 [[wikilink]],排除 code block 和 inline code"""
    # 简单去除 ```...``` 块
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    # 去除 inline code
    text = re.sub(r"`[^`]+`", "", text)
    return set(re.findall(r"\[\[([^\]]+)\]\]", text))

def collect_existing_targets():
    """收集所有 .md 路径(无 .md 后缀),用于死链检测
    包括 content + raw(源文件也允许被引用)"""
    targets = set()
    # 遍历全部 .md(不跳 raw)— 因为 raw 文件是公开可引用的源
    for root, dirs, files in os.walk(WIKI_ROOT):
        rel_root = Path(root).relative_to(WIKI_ROOT)
        top = rel_root.parts[0] if rel_root.parts else ""
        if top in {".git", ".obsidian", ".claude", ".claudian", ".codegraph", ".trash", "_archive"}:
            dirs[:] = []
            continue
        # 跳过 _drafts 子目录
        dirs[:] = [d for d in dirs if d != "_drafts"]
        for f in files:
            if f.endswith(".md") and not f.startswith(".#"):
                p = Path(root) / f
                rel = p.relative_to(WIKI_ROOT)
                # 多种 wikilink 形式
                targets.add(str(rel.with_suffix("")))            # concepts/foo
                targets.add(str(rel.with_suffix("")) + ".md")    # concepts/foo.md
                targets.add(rel.stem)                            # foo
                targets.add(rel.name)                            # foo.md
    return targets

# === 检查函数 ===
def check_dead_links():
    """1. 死链"""
    targets = collect_existing_targets()
    dead = []
    for p in iter_md_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        for link in find_wikilinks(text):
            # 跳过:URL/标签/heading
            if link.startswith(("http", "tag:", "#", "/")):
                continue
            # 取基础(去掉 |alias)— 先 unescape markdown 表格中的 \|
            base = link.replace("\\|", "|").split("|")[0].split("#")[0].strip()
            if not base:
                continue
            # 多种形式都试
            candidates = [
                base,
                base + ".md",
                base.replace("/", os.sep),
            ]
            if not any(c in targets or c.replace(os.sep, "/") in targets for c in candidates):
                dead.append((str(p.relative_to(WIKI_ROOT)), link))
    return dead

def check_index_sync():
    """2. 索引同步 — scratchpad 任务工作区不强求索引"""
    if not INDEX_FILE.exists():
        return -1, 0
    index_text = INDEX_FILE.read_text(encoding="utf-8", errors="ignore")
    indexed = set()
    for m in re.finditer(r"\[\[([^\]]+)\]\]", index_text):
        # unescape \| -> |, then split alias
        link = m.group(1).replace("\\|", "|").split("|")[0].split("#")[0].strip()
        if link:
            indexed.add(link)
    # 收集所有 content .md(跳过 scratchpad)
    all_files = set()
    for p in iter_md_files():
        rel = p.relative_to(WIKI_ROOT)
        if rel.parts[0] == "scratchpad":
            continue
        all_files.add(rel.with_suffix("").as_posix())
    missing = []
    for f in sorted(all_files):
        if f not in indexed and not f.endswith(("index", "README", "AGENTS", "CLAUDE")):
            missing.append(f)
    return len(indexed), missing

def check_frontmatter():
    """3. frontmatter 9 字段
    - 顶层文件(README/AGENTS/CLAUDE/log/index)跳过
    - agents/* 用 Agent schema(id/owner/capabilities/interfaces)— 不强求 6 字段
    - 其他文件需要 6 必填字段
    """
    missing = []
    for p in iter_md_files():
        rel = p.relative_to(WIKI_ROOT)
        # 跳过特殊文件
        if rel.name in {"README.md", "AGENTS.md", "CLAUDE.md", "log.md", "index.md"}:
            continue
        # agents/* 用 Agent schema,跳过
        if rel.parts[0] == "agents":
            continue
        # scratchpad/* 是任务工作区,不强求
        if rel.parts[0] == "scratchpad":
            continue
        fm, _ = get_frontmatter(p)
        if fm is None:
            missing.append((str(rel), "no frontmatter"))
            continue
        for k in REQUIRED_FRONTMATTER:
            if k not in fm:
                missing.append((str(rel), f"missing: {k}"))
        # source/sources 二选一
        if not (SOURCE_FIELD_ALIASES & set(fm.keys())):
            missing.append((str(rel), "missing: source"))
    return missing

def check_log_fresh():
    """4. log.md 24h 内更新"""
    if not LOG_FILE.exists():
        return None
    mtime = datetime.fromtimestamp(LOG_FILE.stat().st_mtime)
    age_hours = (datetime.now() - mtime).total_seconds() / 3600
    return age_hours

def check_size():
    """5. 总大小"""
    total = sum(p.stat().st_size for p in iter_md_files())
    return total / (1024 * 1024)

# === 主流程 ===
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="CI mode")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    report = {
        "timestamp": datetime.now().isoformat(),
        "wiki_root": str(WIKI_ROOT),
    }

    # 1. 死链
    dead = check_dead_links()
    report["dead_links"] = {
        "count": len(dead),
        "items": dead[:20],  # 最多 20 个示例
    }

    # 2. 索引
    idx_count, missing = check_index_sync()
    report["index_sync"] = {
        "indexed": idx_count,
        "missing": len(missing),
        "missing_list": missing[:20],
    }

    # 3. frontmatter
    fm_missing = check_frontmatter()
    report["frontmatter"] = {
        "missing_count": len(fm_missing),
        "items": fm_missing[:20],
    }

    # 4. log
    log_age = check_log_fresh()
    report["log_freshness_hours"] = round(log_age, 1) if log_age else None

    # 5. size
    size_mb = check_size()
    report["size_mb"] = round(size_mb, 2)

    # === 判定 ===
    errors = []
    if dead:
        errors.append(f"死链 {len(dead)} 个")
    if missing and len(missing) > 5:
        errors.append(f"索引缺失 {len(missing)} 个(>5)")
    if fm_missing and len(fm_missing) > 5:
        errors.append(f"frontmatter 缺字段 {len(fm_missing)} 个(>5)")
    if log_age and log_age > LOG_FRESH_HOURS:
        errors.append(f"log.md {log_age:.1f}h 未更新(>{LOG_FRESH_HOURS}h)")
    if size_mb > SIZE_LIMIT_MB:
        errors.append(f"wiki 大小 {size_mb:.1f}MB 超过 {SIZE_LIMIT_MB}MB")

    report["status"] = "PASS" if not errors else "FAIL"
    report["errors"] = errors

    # === 输出 ===
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("=" * 50)
        print(f"Wiki Quality Check — {report['timestamp']}")
        print("=" * 50)
        print(f"1. 死链:        {len(dead)} 真")
        print(f"2. 索引:        {idx_count} 已索引, {len(missing)} 缺")
        print(f"3. frontmatter: {len(fm_missing)} 缺字段")
        print(f"4. log.md:      {log_age:.1f}h 前更新" if log_age else "4. log.md:    ⚠ 不存在")
        print(f"5. 总大小:      {size_mb:.2f} MB")
        print("-" * 50)
        if errors:
            print(f"❌ FAIL: {'; '.join(errors)}")
        else:
            print("✅ PASS: 所有检查通过")
        print("=" * 50)

    if args.strict and errors:
        sys.exit(1)

if __name__ == "__main__":
    main()
