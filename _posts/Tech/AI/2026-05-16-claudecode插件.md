---
layout: post
category: AI
title: Claude Code：Superpower vs OMC vs Harness
tags: AI
---

# Claude Code：Superpower vs OMC vs Harness

## 一句话总结

| 工具                   | 定位                    |
| ---------------------- | ----------------------- |
| Superpower             | AI 工程化开发方法论     |
| OMC (oh-my-claudecode) | 多 Agent 自动化框架     |
| Harness                | 可复用 AI 工作流/流水线 |

---

# 1. Superpower

## 是什么

Superpower 本质是一套：

- prompt engineering
- workflow discipline
- structured development flow

目标：

让 Claude 更像高级工程师。

强调：

```text
Analyze
→ Plan
→ Implement
→ Review
```

而不是直接乱写代码。

---

## 特点

### 优点

- 输出稳定
- 幻觉少
- 代码质量高
- review 很强
- 适合正式项目
- 对大仓库友好

### 缺点

- 啰嗦
- 节奏慢
- token 消耗高
- 喜欢先 planning
- 不适合“一句话出功能”

---

## 适合场景

### 非常适合

- Go 后端
- Infra
- 微服务
- 大仓库
- 重构
- review
- debugging

### 不太适合

- prototype
- vibe coding
- 快速 UI 生成

---

## 安装（常见方式）

通常是：

### 方式1：skills

```bash
~/.claude/skills/
```

例如：

```bash
git clone xxx superpower
```

---

### 方式2：commands

```bash
~/.claude/commands/
```

---

### 方式3：项目级（推荐）

```bash
project/.claude/
```

避免污染全局。

---

## 常见命令

```bash
/sp:plan
/sp:review
/sp:debug
/sp:implement
```

或者：

```bash
/use planner
```

---

## 推荐使用方式

### 第一步

```text
先分析
不要写代码
```

---

### 第二步

```text
输出 implementation plan
```

---

### 第三步

```text
一步一步实现
```

---

### 第四步

```text
review 当前改动
```

---

## 最佳实践

不要：

```text
帮我做完 xxx
```

而是：

```text
先分析 router
```

然后：

```text
只改 config 层
```

最后：

```text
补 tests
```

---

# 2. OMC（oh-my-claudecode）

## 是什么

OMC 是：

> 多 Agent AI 编排框架

目标：

让多个 AI agent 协作开发。

例如：

- architect
- implementer
- reviewer
- qa
- security

自动并行工作。

---

## 特点

### 优点

- 自动化强
- 并行执行
- 功能开发快
- 爽感强
- autopilot 能力强

### 缺点

- token 爆炸
- 容易失控
- context 漂移
- agent 相互污染
- debug 难

---

## 适合场景

### 非常适合

- prototype
- side project
- overnight coding
- 大规模改造
- 自动修 bug

### 不太适合

- 高稳定性项目
- 强 controllability 场景

---

## 安装（常见方式）

通常：

```bash
git clone oh-my-claudecode
```

然后：

```bash
./install.sh
```

或者：

```bash
npm install
```

它会注册：

```text
agents/
commands/
workflows/
```

---

## 常见命令

```bash
/omc:autopilot
/omc:team
/ralph
```

---

## 典型工作方式

```text
需求
→ architect agent
→ implementation agent
→ reviewer agent
→ qa agent
```

自动 orchestrate。

---

## 推荐使用方式

适合：

```text
帮我生成 admin dashboard
```

或者：

```text
批量重构 provider
```

---

## 不推荐

不要长期：

```text
全程 autopilot
```

容易：

- 越改越乱
- context 爆炸
- token 爆炸

---

# 3. Harness

## 是什么

Harness 本质是：

> AI workflow automation pipeline

类似：

- CI/CD
- reusable workflow
- automation pipeline

核心价值：

把 AI 工作流标准化。

---

## 特点

### 优点

- 可复用
- 降低随机性
- 团队统一流程
- 降低 prompt 重复
- 长期收益很高

### 缺点

- 初期需要设计
- 要维护 workflow

---

## 适合场景

### 非常适合

- 团队协作
- 固定开发套路
- incident response
- bugfix
- PR review
- provider integration

---

## 安装（常见方式）

通常是：

```text
.claude/harnesses/
```

或者：

```text
.claude/workflows/
```

例如：

```yaml
name: fix-bug

steps:
  - analyze logs
  - locate issue
  - write test
  - patch
  - run tests
```

---

## 使用方式

```bash
/harness fix-bug
```

或者：

```bash
/workflow payment-review
```

---

## 最推荐的 Harness

### bugfix

```text
日志分析
→ 定位问题
→ 写 failing test
→ 修复
→ 回归测试
```

---

### incident-analysis

```text
trace
→ timeout
→ dependency
→ root cause
```

---

### provider-integration

```text
阅读 API
→ 生成 SDK
→ 增加 config
→ 增加 test
```

---

# 三者核心区别

| 对比            | Superpower      | OMC        | Harness |
| --------------- | --------------- | ---------- | ------- |
| 本质            | 方法论          | 多 Agent   | 工作流  |
| 核心            | 工程 discipline | 自动化协作 | 标准化  |
| 风格            | 稳              | 猛         | 工程化  |
| 自动化          | 中              | 很强       | 强      |
| 并行            | 弱              | 强         | 可配置  |
| controllability | 强              | 中         | 很强    |
| token 消耗      | 中高            | 很高       | 中      |
| 学习成本        | 低              | 中         | 中      |
| 长期价值        | 高              | 中         | 很高    |

---

# 推荐组合

## 日常开发（最推荐）

```text
Superpower + Harness
```

原因：

- 稳
- 可控
- 工程化
- 成本低

---

## 大任务

临时：

```text
OMC Autopilot
```

例如：

- 大规模 refactor
- overnight coding
- prototype

---

# 推荐目录结构

```text
project/
└── .claude/
    ├── skills/
    │   └── superpower/
    │
    ├── agents/
    │   └── omc/
    │
    ├── harnesses/
    │   ├── bugfix.yaml
    │   ├── review.yaml
    │   └── provider.yaml
    │
    └── CLAUDE.md
```

---

# 如何区分当前用了哪个

## 看 commands

```bash
/help
/commands
```

---

## 看风格

### Superpower

```text
先分析
先 plan
```

---

### OMC

```text
Launching agents...
Running reviewer...
```

---

### Harness

```text
Running workflow...
Step 1/5...
```

---

# 最终建议

## 如果你是：

### 后端 / Infra / 工程化开发

优先：

```text
Harness > Superpower > OMC
```

---

## 如果你是：

### prototype / AI coding / vibe coding

优先：

```text
OMC > Harness > Superpower
```

---

# 个人推荐组合（比较稳）

```text
日常：
  Superpower + Harness

大任务：
  临时开 OMC

小问题：
  纯净 Claude
```

这样：
- 不容易 prompt 冲突
- controllability 更高
- token 更健康
- 长期体验最好


