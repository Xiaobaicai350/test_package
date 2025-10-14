# 第五阶段：Scrapy框架

## 🎯 学习目标

1. 理解Scrapy架构设计
2. 掌握Scrapy核心组件
3. 学会编写Spider爬虫
4. 使用Pipeline处理数据
5. 配置中间件

## 📖 Scrapy简介

Scrapy是Python最强大的爬虫框架

### 为什么使用Scrapy？

**优点**：
- ✅ 高性能（异步IO）
- ✅ 完整的框架（不需要自己造轮子）
- ✅ 强大的扩展性
- ✅ 自动去重
- ✅ 丰富的中间件
- ✅ 分布式支持

**缺点**：
- ❌ 学习曲线陡
- ❌ 异步编程较复杂
- ❌ 对简单任务显得笨重

### Scrapy vs requests

```
项目规模          推荐方案
─────────────────────────────
小型（<1000页）   requests + BS4
中型（1000-10万） Scrapy
大型（>10万）     Scrapy + 分布式
```

## 🏗️ Scrapy架构

```
┌─────────────────────────────────────────────┐
│                  引擎 (Engine)               │
│         (控制整个系统的数据流)                │
└─────────────────┬───────────────────────────┘
                  │
      ┌───────────┴───────────┐
      │                       │
┌─────▼────┐           ┌─────▼────┐
│ Scheduler │           │  Downloader │
│  调度器    │←─────────→│   下载器    │
└──────────┘           └───────────┘
      │                       │
      │                       │
┌─────▼────────────────────────▼────┐
│            Spider                  │
│           爬虫逻辑                  │
└────────────────┬───────────────────┘
                 │
           ┌─────▼─────┐
           │  Pipeline │
           │  数据管道  │
           └───────────┘
```

## 📝 核心组件

### 1. Spider（爬虫）
- 定义爬取逻辑
- 解析响应数据
- 提取Item
- 生成新的请求

### 2. Item（数据容器）
- 定义数据结构
- 类似字典但更强大
- 支持类型检查

### 3. Pipeline（管道）
- 处理Item
- 清洗数据
- 验证数据
- 存储到数据库

### 4. Middleware（中间件）
- 下载中间件：处理请求和响应
- Spider中间件：处理Spider的输入输出

### 5. Settings（配置）
- 全局配置
- 并发数
- 延迟时间
- 等等...

## 🚀 快速开始

```bash
# 安装Scrapy
pip install scrapy

# 创建项目
scrapy startproject myproject

# 生成Spider
cd myproject
scrapy genspider example example.com

# 运行爬虫
scrapy crawl example

# 导出数据
scrapy crawl example -o data.json
```

## 📚 学习路径

1. 安装和项目结构
2. 编写第一个Spider
3. Item和Pipeline
4. 选择器（CSS/XPath）
5. Request和Response
6. 中间件配置
7. Scrapy Shell调试
8. 分布式爬虫（Scrapy-Redis）

## ⏭️ 下一步

完成本阶段后，进入第六阶段学习高级技术。

