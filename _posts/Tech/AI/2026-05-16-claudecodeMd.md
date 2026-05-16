---
layout: post
category: AI
title: claudecode CLAUDE.md
tags: AI
---

基于https://github.com/multica-ai/andrej-karpathy-skills/blob/main/README.zh.md 改动



# The full 12-rule CLAUDE.md (copy-paste ready)

````

These rules apply to every task in this project unless explicitly overridden.
Bias: caution over speed on non-trivial work. Use judgment on trivial tasks.

## Rule 1 — Think Before Coding
State assumptions explicitly. If uncertain, ask rather than guess.
Present multiple interpretations when ambiguity exists.
Push back when a simpler approach exists.
Stop when confused. Name what's unclear.

## Rule 2 — Simplicity First
Minimum code that solves the problem. Nothing speculative.
No features beyond what was asked. No abstractions for single-use code.
Test: would a senior engineer say this is overcomplicated? If yes, simplify.

## Rule 3 — Surgical Changes
Touch only what you must. Clean up only your own mess.
Don't "improve" adjacent code, comments, or formatting.
Don't refactor what isn't broken. Match existing style.

## Rule 4 — Goal-Driven Execution
Define success criteria. Loop until verified.
Don't follow steps. Define success and iterate.
Strong success criteria let you loop independently.

## Rule 5 — Use the model only for judgment calls
Use me for: classification, drafting, summarization, extraction.
Do NOT use me for: routing, retries, deterministic transforms.
If code can answer, code answers.

## Rule 6 — Token budgets are not advisory
Per-task: 4,000 tokens. Per-session: 30,000 tokens.
If approaching budget, summarize and start fresh.
Surface the breach. Do not silently overrun.

## Rule 7 — Surface conflicts, don't average them
If two patterns contradict, pick one (more recent / more tested).
Explain why. Flag the other for cleanup.
Don't blend conflicting patterns.

## Rule 8 — Read before you write
Before adding code, read exports, immediate callers, shared utilities.
"Looks orthogonal" is dangerous. If unsure why code is structured a way, ask.

## Rule 9 — Tests verify intent, not just behavior
Tests must encode WHY behavior matters, not just WHAT it does.
A test that can't fail when business logic changes is wrong.

## Rule 10 — Checkpoint after every significant step
Summarize what was done, what's verified, what's left.
Don't continue from a state you can't describe back.
If you lose track, stop and restate.

## Rule 11 — Match the codebase's conventions, even if you disagree
Conformance > taste inside the codebase.
If you genuinely think a convention is harmful, surface it. Don't fork silently.

## Rule 12 — Fail loud
"Completed" is wrong if anything was skipped silently.
"Tests pass" is wrong if any were skipped.
Default to surfacing uncertainty, not hiding it.
````







# CLAUDE.md 从 4 条到 12 条：Multi-step Agent 失败模式补全（笔记版）

> 来源：Mnilax 在 X 上对 Karpathy CLAUDE.md 模板的扩展实验  
> 核心结论：4 条规则解决“单次生成错误”，12 条规则覆盖“多步 Agent 崩溃”

---

# 一、背景：为什么要扩展 CLAUDE.md

## 1. Karpathy 原版 4 条解决的问题（1 月环境）

主要针对：

- 单轮代码生成错误
- 过度复杂化
- 静默假设
- 修改范围过大

👉 本质：**“一次性 coding mistake”**

---

## 2. 5 月之后的问题变化

真实问题升级为：

- 多步 Agent 执行（multi-step workflows）
- 跨文件修改冲突
- Hook / Skill 级联问题
- 长任务状态漂移（drift）
- 多代码库风格冲突

👉 本质：**“系统性执行失败”**

---

# 二、原版 4 条规则（基线）

## 规则 1：先思后码
- 明确假设
- 不确定先问
- 避免盲猜

---

## 规则 2：简单优先
- 最少代码
- 不过度抽象
- 不做“以防万一设计”

---

## 规则 3：外科手术式修改
- 只改必要部分
- 不顺手重构
- 不破坏局部无关代码

---

## 规则 4：目标驱动
- 明确成功标准
- 允许模型自主迭代
- 不强制步骤执行

---

## 局限性总结

无法覆盖：

- 长任务执行（multi-step）
- 工程一致性问题
- 测试质量问题
- 状态漂移问题
- 多 agent 协作问题

---

# 三、扩展的 8 条规则（关键补丁）

---

## 规则 5：模型只做“判断”，不做“控制流”

### ❌ 不适合：
- retry 逻辑
- routing
- 状态机
- 确定性转换

### ✅ 适合：
- 分类
- 摘要
- 信息抽取
- 草拟

📌 本质：
> LLM = 判断器，不是控制器

---

## 规则 6：Token 预算强约束

- 单任务 ≤ 4k token
- 单会话 ≤ 30k token

必须：

- 主动 summary
- 主动 reset context
- 不允许 silent overflow

📌 本质：
> 防止上下文漂移 + 无限制循环

---

## 规则 7：冲突必须显式处理

禁止：

- 折中实现
- 混合两种架构

必须：

- 明确选择一种
- 另一种标记废弃

📌 本质：
> 避免“双系统融合污染”

---

## 规则 8：写代码前必须读上下文

要求：

- 读当前文件结构
- 读调用方
- 读公共工具

禁止：

- “看起来不冲突”假设

📌 本质：
> 防止局部无知修改

---

## 规则 9：测试必须表达“意图”，不是“行为”

错误测试：

- 只验证 output

正确测试：

- 验证 WHY（业务意义）

📌 本质：
> 防止“假绿测试”

---

## 规则 10：长任务必须 checkpoint

每个关键步骤：

- 状态总结
- 已完成确认
- 剩余任务说明

📌 本质：
> 防止 multi-step drift

---

## 规则 11：遵循代码库既有规范

- 一致性 > 个人偏好
- 不允许“更优风格替换”

📌 本质：
> 防止风格 fragmentation

---

## 规则 12：显式失败（Fail loud）

禁止：

- 静默跳过
- 隐性失败
- 假成功

必须：

- 明确暴露不确定性
- 明确失败原因

📌 本质：
> 防止“看起来成功的失败”

---

# 四、实验结果（核心结论）

## 测试设置

- 30 个代码库
- 50 个标准任务
- 6 周实验

---

## 结果变化

| 配置      | 错误率 |
| --------- | ------ |
| 4 条规则  | 41%    |
| +8 条规则 | ~3%    |

---

## 关键观察

新增规则的作用：

- 覆盖“系统级错误”（不是单点错误）
- 补足 multi-step agent 缺陷
- 防止状态漂移与假成功

---

# 五、失败模式分类（很重要）

## 1. 单步错误（Karpathy 已覆盖）

- 写错逻辑
- 过度设计
- 假设错误

---

## 2. 多步错误（新增规则覆盖）

- 状态漂移
- 中途偏航
- 误以为成功
- checkpoint 缺失

---

## 3. 系统级错误

- token 爆炸
- context 混乱
- 多 agent 冲突
- 风格分裂

---

# 六、关键洞察（核心总结）

## 1. CLAUDE.md 的本质

不是提示词，而是：

> “失败模式约束系统（failure-mode contract）”

---

## 2. 4 条 vs 12 条的本质区别

| 层级  | 覆盖范围         |
| ----- | ---------------- |
| 4 条  | 单次生成错误     |
| 12 条 | 多步执行系统错误 |

---

## 3. 最重要设计原则

### ✔ 每条规则必须回答：
> “它防止的具体失败是什么？”

否则就是噪音

---

## 4. 规则数量不是越多越好

实验结论：

- >12 条 → 合规率下降
- 18 条 → 行为退化（pattern matching）

📌 最优区间：8–12 条

---

# 七、实用建议（可直接用）

## CLAUDE.md 设计原则

1. 从真实 bug 反推规则
2. 每条规则必须有 failure 对应
3. 控制在 ≤ 12 条
4. 避免抽象语义（如“认真思考”）
5. 优先防系统性错误，而不是语法错误

---

# 八、一句话总结

> CLAUDE.md 的进化本质是：从“防写错代码”，升级为“防多步 Agent 崩溃”。

---

