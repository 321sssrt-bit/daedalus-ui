# 038 故障

## 意图元数据

- 意图版本：1
- 对应规范：`038-error-fault-line.spec.md`
- 说明：本文件不参与结构、尺寸、状态或交互验收。

## 设计意图

工业暗色故障页：橙色「断线」强调是可修复的临时状态，而非用户过错。工单号 monospace 便于复制报修，重试为主、回首页为次。

## 适用场景与目标用户

任意 mobile App 的全局网络/服务不可用页；用户需要知道发生了什么、有无追踪号、下一步做什么。

## 非目标

无详细 stack trace、无在线客服聊天入口。

## 复刻提示词

Dark industrial mobile error：orange accent fault line under warning icon、human copy、FLT ticket code、primary retry + ghost home button。
