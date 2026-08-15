# Daedalus lifecycle

唯一的仓库生命周期入口：

```text
python -m daedalus validate
python -m daedalus build --output dist
python -m daedalus starter --output dist/daedalus-clean.zip
```

三个命令都向标准输出写 JSON 回执，失败时退出码非零。`build` 和
`starter` 一定先验证；失败不会留下新的可发布产物。

## v4 答卷合同

登记表 `models/_index.json`：

```json
{
  "schemaVersion": 3,
  "submissions": [
    {
      "harness": "codex",
      "model": "gpt-5.6-sol",
      "reasoningEffort": "xhigh",
      "displayName": "Codex · GPT-5.6 Sol · xhigh",
      "path": "models/codex/gpt-5.6-sol/xhigh"
    }
  ]
}
```

每份答卷目录中使用 `model.json`，并声明 `schemaVersion: 4` 与
`specVersion: 2`。每个 piece 必须登记同名的 `.html`、`.spec.md` 和
`.intent.md`；前者是页面，中者是可验收复现合同，后者只放设计意图和
辅助复刻提示词。完成答卷的 `status` 为 `complete`，并严格登记
001–050；弃权答卷的 `status` 为 `forfeited`，另含：

```json
{
  "schemaVersion": 4,
  "specVersion": 2,
  "pieces": [
    {
      "id": "001",
      "slug": "scheme-name",
      "file": "001-scheme-name.html",
      "spec": "001-scheme-name.spec.md",
      "intent": "001-scheme-name.intent.md",
      "status": "complete"
    }
  ]
}
```

```json
{"forfeit": {"phrase": "我是鸡", "reason": "非空原因"}}
```

`model.json` 的 `runReceipt` 指向同目录的 `run-receipt.json`。回执格式：

```json
{
  "schemaVersion": 1,
  "mainAgent": {"model": "gpt-5.6-sol", "reasoningEffort": "xhigh"},
  "subagents": [
    {"model": "gpt-5.6-sol", "reasoningEffort": "xhigh", "purpose": "可选说明"}
  ]
}
```

子 Agent 列表可以为空；只要存在，就必须与主 Agent 的模型和思考档位一致。

## 产物

`build --output dist` 原子生成：

- `dist/site/index.html`：综合静态展厅；
- `dist/site/submissions/<identity>/index.html`：独立答卷展厅；
- `dist/daedalus-offline-gallery.zip`：离线展厅；
- `dist/build-receipt.json`：构建证据。

预览 iframe 不含 `allow-same-origin`，独立打开使用 `noopener noreferrer`。
`starter` 只打包规则、题库、决策记录和生命周期工具，并写入空的 v3 登记表。
