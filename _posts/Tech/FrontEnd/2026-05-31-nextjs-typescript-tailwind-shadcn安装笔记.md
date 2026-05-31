---
layout: post
category: Tech
title: Next.js + TypeScript + Tailwind + shadcn/ui 学习安装笔记
tags: Frontend
---

# Next.js + TypeScript + Tailwind + shadcn/ui 学习安装笔记

## 技术栈介绍

| 技术 | 用途 |
| ---- | ---- |
| Next.js | React 全栈框架，支持 App Router、SSR、API Routes |
| TypeScript | JavaScript 超集，提供类型检查 |
| Tailwind CSS | Utility-first CSS 框架 |
| shadcn/ui | 基于 Radix UI 的可复用组件库 |

---

## 环境准备

```bash
node --version    # v24.3.0
npm --version     # 11.4.2
pnpm --version    # 9.13.2
```

### 安装 pnpm

```bash
npm install -g pnpm
```

---

## 一、安装 Next.js + TypeScript + Tailwind

### 1. 创建项目

```bash
npx create-next-app@latest nextjs-learn \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --use-npm \
  --yes
```

参数说明：

| 参数 | 说明 |
| ---- | ---- |
| `--typescript` | 启用 TypeScript |
| `--tailwind` | 启用 Tailwind CSS |
| `--eslint` | 添加 ESLint 配置 |
| `--app` | 使用 App Router（Next.js 13+） |
| `--src-dir` | 源码放在 src/ 目录 |
| `--import-alias "@/*"` | 路径别名配置 |
| `--use-pnpm` | 使用 pnpm（更快） |
| `--yes` | 所有选项默认 yes |

### 2. 安装依赖

```
next
react
react-dom

devDependencies:
@tailwindcss/postcss
@types/node
@types/react
@types/react-dom
eslint
eslint-config-next
tailwindcss
typescript
```

### 3. 目录结构

```
src/
├─ app/           # App Router 页面
├─ components/    # React 组件
└─ lib/          # 工具函数
```

---

## 二、安装 shadcn/ui

### 1. 初始化

```bash
npx shadcn@latest init -y --defaults
```

这会：

- 创建 `components.json` 配置文件
- 更新 `tailwind.config.ts`
- 更新 `src/app/globals.css`
- 安装基础依赖

### 2. 添加组件

```bash
npx shadcn@latest add card badge input --yes
```

常用组件：

| 组件 | 用途 |
| ---- | ---- |
| button | 按钮 |
| card | 卡片容器 |
| badge | 徽章 |
| input | 输入框 |
| dialog | 对话框 |
| select | 下拉选择 |

### 3. 组件结构

```
src/components/ui/
├─ button.tsx
├─ card.tsx
├─ badge.tsx
└─ input.tsx
```

---

## 三、配置文件

### components.json

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "src/app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

### lib/utils.ts

```typescript
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

---

## 四、使用示例

### Button

```tsx
import { Button } from "@/components/ui/button"

export default function Demo() {
  return <Button>Click me</Button>
}
```

### Card

```tsx
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

export function DemoCard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Title</CardTitle>
      </CardHeader>
      <CardContent>
        Content here
      </CardContent>
    </Card>
  )
}
```

---

## 五、Tailwind CSS 基础

### 常用类

```html
<!-- 布局 -->
<div class="flex items-center justify-between">

<!-- 间距 -->
<p class="m-4 p-4">

<!-- 颜色 -->
<button class="bg-primary text-white">

<!-- 响应式 -->
<div class="hidden md:block">
```

### 配置主题

在 `tailwind.config.ts` 中自定义：

```typescript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: "#xxx"
      }
    }
  }
}
```

---

## 六、常用命令

```bash
# 开发
npm run dev

# 构建
npm run build

# 生产
npm run start

# lint
npm run lint
```

---

## 七、常见问题

### Q: shadcn/ui 和 Tailwind 版本兼容？

A: shadcn/ui 需要 Tailwind CSS v4，当前通过 `@tailwindcss/postcss` 集成。

### Q: 如何升级 shadcn？

```bash
npx shadcn@latest upgrade
```

### Q: 组件样式不生效？

检查 `globals.css` 是否包含：

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---