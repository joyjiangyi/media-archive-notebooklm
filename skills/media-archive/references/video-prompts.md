# Video-original prompts

These prompts were transcribed from the prompt cards and screen recordings used in JioJioJoy's `NotebookLM保姆级教程.mp4`. Preserve the wording when reproducing the tutorial.

## Install Skill Creator

```text
请为你当前所在的 Agent 环境安装或启用「Skill Creator」。让我以后能够创建、修改、验证符合 Agent Skills 开放规范的 Skill。
```

## Install NotebookLM Skill

```text
请帮我安装 notebooklm skill，地址：
https://github.com/teng-lin/notebooklm-py
```

## Analyze one episode

```text
帮我把这期播客
🛸 https://www.xiaoyuzhoufm.com/episode/6a719a98ab3a91c24a0f95e2 导入
NotebookLM，按以下框架做深度分析，输出中文笔记：
核心主题
分章节概要（每章节时间段）
3-5 个关键观点
可行动建议
适合关联的知识库标签
要求：不要编造来源之外的事实、数据或引语。
```

## Generate and download an infographic

```text
帮我把这份分析在NotebookLM生成一张信息图 再下载到本地
```

## Search for an existing Xiaoyuzhou tool

```text
帮我搜索能导出小宇宙最近 30 天完播记录和链接的公开 Skill 或工具
```

## Install the history skill

```text
帮我安装 xiaoyuzhou-history，并引导我完成登录授权。
```

## List the last 30 days

```text
帮我列出小宇宙最近 30 天听过的播客
```

## Compose the full workflow

```text
请使用 xiaoyuzhou-history skill 调取我近 30 天的收听记录，跟我确认哪些需要处理。确认后，把每一集的链接通过 notebooklm skill 导入我的笔记本，做深度分析，最后把每一条播客分析结果汇总成一份 Markdown 笔记，保存到 Obsidian。
```

## Package it with Skill Creator

```text
请使用 Skill Creator，帮我把刚才这套流程打包成一个新的 skill，名字叫 media-archive。它的功能是：调取小宇宙近 30 天收听记录 → 导入 NotebookLM 深度分析 → 汇总成 Markdown 笔记保存到 Obsidian。
```

## One-sentence trigger shown on screen

```text
清理小宇宙最近听过的播客
```
