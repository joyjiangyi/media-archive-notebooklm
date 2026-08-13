# Media Archive × NotebookLM

把公开视频和播客链接变成可复用的 Markdown 知识笔记。YouTube、Bilibili、小红书等视频链接，以及小宇宙、RSS 等播客链接，都可以从同一个 `media-archive` 入口开始处理。

这不是只为播客设计的工具：**Media Archive 同时包含 Video Archive 和 Podcast Archive。** 仓库把三个 Codex Skills 组合成一条可降级的工作流：

```text
                    ┌─ 视频：YouTube 等原始链接 ─────────┐
媒体链接 → 类型识别 ┤                                  ├→ NotebookLM → Markdown 归档
                    └─ 播客：原始链接 / 小宇宙音频直链 ─┘
```

## 支持的媒体

| 类型 | 常见来源 | 处理方式 |
|---|---|---|
| 视频 | YouTube、Bilibili、小红书及其他公开视频链接 | 优先把原始视频链接交给 NotebookLM；平台不受支持时，使用可验证的字幕、描述或文本兜底 |
| 播客 | 小宇宙、RSS、公开音频及其他播客链接 | 优先使用原始节目页；小宇宙页面不受支持时可提取公开音频链接，再以 Show Notes 文本兜底 |

## 包含的 Skills

- `media-archive`：统一入口与工作流编排
- `notebooklm-media`：导入视频、播客、音频、网页或文本来源，并生成有来源约束的笔记
- `xiaoyuzhou-media`：小宇宙播客的可选适配器，负责解析单集页、Show Notes 和公开音频链接

## 安装

需要 Python 3.10+。NotebookLM 集成依赖开源项目 [notebooklm-py](https://github.com/teng-lin/notebooklm-py)。

```bash
git clone https://github.com/joyjiangyi/media-archive-notebooklm.git
cd media-archive-notebooklm
./install.sh
python3 -m pip install "notebooklm-py[browser]"
notebooklm login
```

重启 Codex 后即可使用。视频示例：

```text
用 $media-archive 存档这个 YouTube 视频，并用 NotebookLM 生成中文深度笔记：<YOUTUBE_URL>
```

播客示例：

```text
用 $media-archive 存档这个小宇宙节目，并用 NotebookLM 生成中文深度笔记：<URL>
```

单独提取小宇宙公开音频链接：

```bash
python3 skills/xiaoyuzhou-media/scripts/extract_xiaoyuzhou.py \
  "https://www.xiaoyuzhoufm.com/episode/<EPISODE_ID>"
```

## 工作流与降级机制

1. Media Archive 先判断来源是视频还是播客，并保留原始链接与已确认元数据。
2. 视频优先导入原始链接；若平台不受支持，则使用来源中可验证的字幕、描述或文本。
3. 播客优先导入原始节目页；小宇宙页面不受支持时，改用提取出的公开音频 URL。
4. 音频仍失败时，导入元数据与 Show Notes 生成的 Markdown。
5. 所有输出必须标注实际导入路径、证据来源和局限，不虚构转录、引语或时间戳。

## 隐私与版权

- 仓库不包含也不会读取你的 NotebookLM Cookie、浏览器配置或认证文件。
- 仅处理公开来源或你有权访问的材料。
- 音频直链用于授权范围内的个人分析，不代表获得再分发许可。
- `notebooklm-py` 使用非官方 NotebookLM 接口，Google 更新后可能需要升级上游版本。

## 验证

```bash
python3 scripts/validate.py
```

## License

MIT。第三方项目各自遵循其原许可证。
