# Scratchpad — 3rd Notebook Sync Test (2026-06-04 18:40)

> **状态**: active
> **TTL**: short (3 天, 2026-06-07 过期)
> **Owner**: hermes-3rd
> **类型**: scratchpad ns (namespace 隔离测试)

---

## 目的

验证 wiki scratchpad 机制在多 Agent 协作下能正常:
1. **写 scratchpad namespace 隔离** (不被其他 namespace 污染)
2. **scratchpad index 同步** (看 main-claude 的 scratchpad/README.md 规则)
3. **scratchpad → cloud push 链路** (跟普通 wiki 写一样的 git push 流程)
4. **scratchpad vs _drafts 边界** (3rd 写的"边界内容"放到 _drafts, 不污染正式)

## 触发

用户说"ABCD 全做", D = scratchpad 同步测试. 3rd 第一次正式写 scratchpad.

## 计划

- [x] **Step 1**: 读 `scratchpad/README.md` 找规范
- [x] **Step 2**: 写本 namespace 内的"测试文件" (本 md 自身)
- [ ] **Step 3**: push 到云端
- [ ] **Step 4**: 验证 main-claude pull 能看到本 namespace
- [ ] **Step 5**: 写一份到 `_drafts/` 验证"拒绝内容 → _drafts" 规则

## 进度 (18:40 开始)

### 18:40 — 读 scratchpad/README.md

读了 main-claude 6-4 14:00 写的 scratchpad 规范:
- scratchpad/ 是 "短期共享工作记忆"
- 3 类 TTL: ephemeral (1 小时) / short (3 天) / long (1 月)
- namespace 隔离: 每个 agent / 每个 task 一个子目录
- _drafts/ 是"拒绝的边界写入" 的着陆区 (按 README § 写入协议)

### 18:42 — 写本 namespace 内的测试

(本文件)

## 笔记本 + Wiki 双写流程 (3rd 标准)

```
笔记本 terminal → cat > file << 'EOF' (heredoc, 避免 MSYS 路径陷阱)
       ↓
同步到 E:\hermes\wiki\ (本仓库)
       ↓
git status + git add + git commit (Co-authored-by: Hermes 3rd)
       ↓
git push origin main (走 _netrc, 不用 GitHub API header)
       ↓
云端 wiki 立即可见
       ↓
main-claude 下次 pull 自动同步到他本地
```

## 踩坑 (本 namespace 内)

- ✅ 路径翻译陷阱 (write_file 写 /tmp/ → 实际 C:\tmp\) — 改用 heredoc
- ✅ 死链模板占位符 (check 脚本会误报 <name> 这种) — 用斜体 *（待建: ...）*
- ⚠️ 改前一定要 git fetch + pull --rebase (6-4 18:25 那次落后 1 个 commit)
- ⚠️ 配本仓库 local git user (wiki-git-sync 不 persist 到 .git/config)

## 关联

- 笔记本 wiki: `E:\hermes\wiki\`
- 云端: https://github.com/AK47ZZQ/agent-wiki
- 主对话: [[agents/main-claude]]
- 笔记本协作者: [[agents/hermes-3rd]]
- Scratchpad 规范: [[scratchpad/README]]
- Git 协作协议: [[protocols/git-collaboration-multi-agent]]
