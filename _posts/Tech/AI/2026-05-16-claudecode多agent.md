---
layout: post
category: AI
title: Claude Code 多 Agent 架构
tags: AI
---

# Claude Code 多 Agent 架构（修正版面试笔记）



# 一、核心问题：为什么需要 Multi-Agent

单 Agent 在复杂任务中的瓶颈：

- 上下文膨胀（调研 / 编码 / 评审混在一起）
- 职责混乱（推理目标漂移）
- 无法并发（所有步骤串行）
- 工具使用空间过大（action space 无约束）

---

# 二、整体架构本质

Claude Code 的 multi-agent 不是“多进程系统”，而是：

> 单 runtime + 多执行上下文（execution context）+ 状态驱动调度

核心不是“多个 agent”，而是：

- 多个隔离的执行上下文
- 同一个 LLM runtime
- 共享任务状态存储

---

# 三、三种 Agent 组织形态

## 1. 父子模型（Subagent）

- 主 agent 控制整体流程
- 通过工具触发 subagent
- subagent 执行子任务并返回结果

本质：

> 逻辑子上下文（不是独立系统）

---

## 2. 协作模型（Peer Agents）

- 多 agent 并列
- 通过共享状态或消息协作

特点：

- 灵活但复杂
- 状态同步成本高
- 工程中较少直接采用

---

## 3. Coordinator-Worker 模式

- Coordinator：任务拆分 + 调度 + 合成
- Worker：执行具体任务

特点：

- 高并发能力
- 适合大规模任务拆解
- 工业级常用结构

---

# 四、Subagent 的本质：逻辑隔离

## 1. 不是“独立 agent”，而是执行上下文

Subagent =

> 独立 state slice + tool 权限过滤 + message loop

共享：

- runtime
- 基础执行框架

不共享：

- 当前 context state
- tool 权限视图（部分裁剪）
- message history 分支

---

## 2. 工具隔离（Tool Filtering）

目标：限制 action space

三层过滤逻辑：

- 全局禁止工具（防递归 / 控制权）
- agent 类型限制（custom agent 更严格）
- async agent 白名单（后台 agent 最小权限）

本质：

> 降低 agent 可行动空间，而非安全沙箱

---

## 3. 上下文隔离（Field-level state slicing）

不是“全拷贝 or 全共享”，而是逐字段决策：

### 常见策略：

- 文件读取缓存 → 复制（避免互相污染）
- 全局 UI 状态 → 禁止写（避免冲突）
- task registry → 保留（避免孤儿任务）
- agentId / depth → 递增（用于追踪）

核心思想：

> isolation 是字段级语义决策，不是整体策略

---

# 五、通信机制（核心设计）

## 1. 父 → 子通信

机制：

- SendMessage 写入 subagent task state
- pendingMessages 数组作为“信箱”
- subagent 在 execution loop 中轮询读取

本质：

> shared state + event polling（不是 MQ）

---

## 2. 子 → 父通信

机制：

- subagent 生成结构化文本（XML-like payload）
- 注入父 agent conversation history
- 作为“用户消息”处理

本质：

> 系统事件 → 对话消息（message embedding）

优点：

- 兼容 LLM prompt 结构
- 无需额外 event system
- 可持久化

---

## 3. 状态结构（简化模型）

每个 subagent task 包含：

- status（running / done / failed）
- pendingMessages（输入队列）
- result（输出结果）
- progress（执行进度）
- messages（对话历史）

---

# 六、并发模型

## 核心机制

- 多个 LLM API request 并发执行
- worker 之间互不阻塞
- coordinator / parent 不等待所有子任务完成

本质：

> API-level concurrency（不是线程并发）

---

## 自动后台化（auto-background）

规则：

- 短任务：同步等待结果
- 长任务（>阈值）：自动 background
- 完成后异步通知父 agent

本质：

> sync → async 的自动降级机制

---

# 七、Fork Subagent（优化机制）

## 核心目标

> 降低 token 成本 + 提升 cache 命中率

---

## 核心思想

Fork subagent =

> 保持 request prefix byte-level deterministic

---

## 必须一致的部分：

- system prompt
- tool list（顺序 + 内容）
- user context prefix
- system context
- message history prefix

---

## 关键结论

- Fork 不等于 cache
- cache 是结果，不是设计目标
- 核心是“请求前缀一致性”

---

# 八、Coordinator 模式（调度层）

## 角色变化

| 模式 | 主 agent |
|------|----------|
| 普通模式 | 执行 + 调度 |
| Coordinator | 强调度倾向（delegation-first） |

---

## Coordinator 职责

- 拆分任务
- 派发 worker
- 收集结果
- 合成最终输出

但仍然可以：

- 直接回答简单问题
- 自主执行部分任务

---

## Worker 工具限制

worker 不具备：

- 派发其他 worker 权限
- coordinator 内部调度工具
- 合成输出能力

本质：

> 防止递归调度结构（避免树爆炸）

---

## 并行机制

- 一次 LLM 输出可包含多个 worker 调用
- worker 同时启动
- 结果异步返回

效果：

- 从串行任务 → 并行 fan-out

---

## 任务流水线

1. 并行调研（workers）
2. coordinator 合成理解
3. 并行执行（workers）
4. 并行验证（workers）

关键原则：

> coordinator 必须理解，而不是转发

---

# 九、三种模式对比

| 维度 | Subagent | Fork | Coordinator |
|------|----------|------|-------------|
| 并发 | 中 | 中 | 高 |
| 隔离强度 | 中 | 低（同源） | 高（结构隔离） |
| 成本优化 | 无 | 强（cache） | 中 |
| 结构形态 | 父子 | 克隆分支 | 扁平 worker |
| 适用场景 | 局部任务 | 快速分身 / cache优化 | 大任务拆解 |

---

# 十、5 个核心设计原则（面试重点）

## 1. 上下文隔离必须字段级控制

不是整体复制或隔离，而是按语义字段决策。

---

## 2. 通信必须基于消息模型

- 写 state（父→子）
- 写 conversation event（子→父）

避免函数调用式阻塞。

---

## 3. 工具权限是 action space 控制

不是安全沙箱，而是：

> 控制 agent 可行动空间

---

## 4. prompt cache 是工程优化能力

关键在：

> request prefix deterministic design

---

## 5. 并行优先 + coordinator 合成

- worker 并行执行
- coordinator 负责理解与整合

---

# 十一、一句话工程级总结

Claude Code multi-agent 本质是：

> 一个基于共享状态的事件驱动执行系统，通过字段级上下文切分实现逻辑隔离，通过异步消息模拟 agent 通信，通过 API 并发实现执行并行，通过 prompt 前缀确定性实现 cache 优化，并通过 coordinator bias 实现任务调度。

---

# 十二、面试用精简回答（可直接背）

> 它不是多进程 agent 架构，而是单 runtime 下的多执行上下文系统。  
> subagent 通过字段级 state slicing 实现隔离，通过 message queue（pendingMessages）实现异步通信，通过 coordinator 模式实现任务分发与并行执行。  
> 并发来自 API-level async execution，而优化则依赖 prompt prefix deterministic design 来提升 cache 命中率。

---