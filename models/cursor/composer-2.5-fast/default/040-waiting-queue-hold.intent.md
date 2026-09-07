# 040 等候

## 意图元数据

- 意图版本：1
- 对应规范：`040-waiting-queue-hold.spec.md`
- 说明：本文件不参与结构、尺寸、状态或交互验收。

## 设计意图

浅蓝排队室：旋转 spinner + 竖向步骤条让用户知道「卡在哪一步」，ETA 渐变卡给时间预期。放到一边比取消更显眼，符合已提交不愿干等的场景。

## 适用场景与目标用户

政务/金融类 App 提交后的异步审核等待；用户可留页或转后台通知。

## 非目标

无实时 WebSocket 进度、无客服入口。

## 复刻提示词

Light blue mobile waiting room：spinner、3-step vertical timeline with active step、gradient ETA card、「放到一边」primary + cancel link、countdown text updates.
