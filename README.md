# Media Archive × NotebookLM

这是 JioJioJoy《NotebookLM 工作流保姆级教程》的公开配套 Skill 包。它把视频里已经跑通的流程封装成一个可复用入口：

```text
调取小宇宙近 30 天收听记录
        ↓
跟你确认哪些需要处理
        ↓
逐集导入 NotebookLM 做深度分析
        ↓
汇总为 Markdown 笔记保存到 Obsidian
```

Media Archive 同时支持 **video + podcast**：视频中用“小宇宙近 30 天”演示批量播客流程；对 YouTube、Bilibili 等公开视频或单条播客链接，也可以从同一入口导入 NotebookLM 生成有来源约束的笔记。

## 最快用法：把 GitHub 地址直接发给 Agent

如果你只想直接使用成品，不需要按视频重新封装一遍。把下面这段发给 Codex 或其他支持 Agent Skills 的 Agent：

```text
请帮我安装这个公开 Skill：
https://github.com/joyjiangyi/media-archive-notebooklm

安装后请检查并引导我完成以下初始化：
1. 安装或确认 notebooklm skill 可用，并运行 notebooklm login 与 notebooklm auth check。
2. 安装或确认 xiaoyuzhou-history 可用，并引导我完成小宇宙手机号/验证码登录。
3. 检查 media-archive 已成功加载。

完成后先不要批量处理，等我说“清理小宇宙最近听过的播客”再开始；开始后必须先列出候选节目并让我确认。
```

初始化完成后，平时只需说：

```text
清理小宇宙最近听过的播客
```

> Agent 如果要安装第三方 `xiaoyuzhou-history`，先让它说明来源、权限和审查结果。手机号、验证码、Cookie 和会话文件不应被写入 Skill 或上传 GitHub。

### 为什么这套组合更节省 Agent 上下文和 Token

长视频或长播客无需把完整逐字稿塞进当前 Agent 对话。Media Archive 会先把媒体交给 NotebookLM 建立独立来源，再围绕这个来源定向提问并只取回所需结果。这样可以减少长文本对当前上下文的占用，把 Token 更集中地用在分析、判断和输出上。实际节省程度取决于来源长度、提问方式和 Agent 环境，本项目不承诺固定比例。

## 自己封装：成片里的安装顺序

下面是视频演示的教学路线：先分别跑通基础 Skill，再用 Skill Creator 封装为 Media Archive。如果你已经按上一节安装公开包，不需要重复执行这一遍。

### 1. 安装 Skill Creator

把下面这句原文发给你当前使用的 Agent：

```text
请为你当前所在的 Agent 环境安装或启用「Skill Creator」。让我以后能够创建、修改、验证符合 Agent Skills 开放规范的 Skill。
```

### 2. 安装 NotebookLM Skill

```text
请帮我安装 notebooklm skill，地址：
https://github.com/teng-lin/notebooklm-py
```

安装后完成 Google 登录和授权检查：

```bash
notebooklm login
notebooklm auth check
```

### 3. 找到并安装小宇宙历史记录工具

成片里先让 Agent 搜现成工具，而不是自己重新开发：

```text
帮我搜索能导出小宇宙最近 30 天完播记录和链接的公开 Skill 或工具
```

确认来源和权限后：

```text
帮我安装 xiaoyuzhou-history，并引导我完成登录授权。
```

> `xiaoyuzhou-history` 会涉及账号登录。安装前请先审核它的来源、代码和所需权限；不要把手机号、验证码、Cookie 或会话文件提交到仓库。本仓库不捆绑它的第三方代码。

### 4. 安装这个配套 Skill 包

```bash
git clone https://github.com/joyjiangyi/media-archive-notebooklm.git
cd media-archive-notebooklm
./install.sh
```

如果本地已经存在同名 Skill，安装脚本会拒绝覆盖。请先审查差异，再决定是否使用 `./install.sh --force`；强制安装前会自动备份原目录。

## 先跑通一集：成片原文

先用一条小宇宙链接验证 NotebookLM 的导入和分析链路：

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

如果来源里没有可验证的时间戳，Skill 会标明限制，而不会自行编造。

## 跑完整流程

完成登录后，可先单独检查近 30 天的记录：

```text
帮我列出小宇宙最近 30 天听过的播客
```

或使用成片中的完整工作流指令：

```text
请使用 xiaoyuzhou-history skill 调取我近 30 天的收听记录，跟我确认哪些需要处理。确认后，把每一集的链接通过 notebooklm skill 导入我的笔记本，做深度分析，最后把每一条播客分析结果汇总成一份 Markdown 笔记，保存到 Obsidian。
```

安装本仓库后，可以直接触发同一套流程：

```text
清理小宇宙最近听过的播客
```

Media Archive 必须先列出候选节目并等你确认；在你明确选择之前，不会批量导入 NotebookLM。

## 成片里的 Skill Creator 封装原文

```text
请使用 Skill Creator，帮我把刚才这套流程打包成一个新的 skill，名字叫 media-archive。它的功能是：调取小宇宙近 30 天收听记录 → 导入 NotebookLM 深度分析 → 汇总成 Markdown 笔记保存到 Obsidian。
```

## 附加能力：单集公开链接适配

仓库仍包含 `xiaoyuzhou-media`，用于解析一条公开小宇宙单集页的元数据、Show Notes 和公开音频 URL。这是 NotebookLM 不接受原始单集页时的兼容降级，不是成片中“近 30 天听过记录”的替代品。

```bash
python3 skills/xiaoyuzhou-media/scripts/extract_xiaoyuzhou.py \
  "https://www.xiaoyuzhoufm.com/episode/<EPISODE_ID>"
```

## 处理单条视频或播客

成片重点演示小宇宙批量工作流，但 Media Archive 不仅限于小宇宙。对一条公开视频或播客链接，可直接说：

```text
用 $media-archive 存档这条视频或播客，通过 NotebookLM 生成中文深度笔记：<URL>
```

Skill 会保留原始链接和已确认元数据，先尝试导入原始媒体来源，再根据可验证来源生成笔记并说明限制。

## 仓库内容

- `media-archive`：成片主流程的统一入口与人工确认门
- `notebooklm-media`：NotebookLM 登录、导入、深度分析与结果回传
- `xiaoyuzhou-media`：单个公开小宇宙链接的可选适配器
- `skills/media-archive/references/video-prompts.md`：成片里出现的提示词原文集合

## 隐私、版权与限制

- 仅处理公开来源或你有权访问的内容。
- 仓库不包含也不会上传 NotebookLM Cookie、小宇宙登录信息、浏览器配置或 Obsidian 个人库路径。
- 公开音频 URL 仅可在授权范围内用于个人分析，不代表获得再分发许可。
- `notebooklm-py` 使用非官方 NotebookLM 接口，Google 更新后可能需要升级上游版本。
- 登录、删除、覆盖、长时间批量任务和下载产物均需先获得你的明确确认。

## 验证

```bash
python3 scripts/validate.py
```

## License

MIT。第三方项目各自遵循其原许可证。
