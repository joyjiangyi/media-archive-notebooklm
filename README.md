# Media Archive × NotebookLM

把公开视频或播客链接变成可复用的 Markdown 知识笔记。这个仓库把三个 Codex Skills 组合成一条可降级的工作流：

```text
媒体链接 → 平台识别 → 小宇宙元数据/音频直链 → NotebookLM → 结构化 Markdown 笔记
```

## 包含的 Skills

- `media-archive`：统一入口与工作流编排
- `xiaoyuzhou-media`：解析小宇宙公开单集页、Show Notes 和公开音频链接
- `notebooklm-media`：导入 NotebookLM，并在原链接不受支持时自动切换到音频或文本兜底

## 安装

需要 Python 3.10+。NotebookLM 集成依赖开源项目 [notebooklm-py](https://github.com/teng-lin/notebooklm-py)。

```bash
git clone https://github.com/joyjiangyi/media-archive-notebooklm.git
cd media-archive-notebooklm
./install.sh
python3 -m pip install "notebooklm-py[browser]"
notebooklm login
```

重启 Codex 后即可使用：

```text
用 $media-archive 存档这个小宇宙节目，并用 NotebookLM 生成中文深度笔记：<URL>
```

单独提取小宇宙公开音频链接：

```bash
python3 skills/xiaoyuzhou-media/scripts/extract_xiaoyuzhou.py \
  "https://www.xiaoyuzhoufm.com/episode/<EPISODE_ID>"
```

## 降级机制

1. NotebookLM 先导入原始节目页。
2. 原始页不受支持时，改用公开音频 URL。
3. 音频仍失败时，导入元数据与 Show Notes 生成的 Markdown。
4. 所有输出必须标注证据来源和局限，不虚构转录、引语或时间戳。

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
