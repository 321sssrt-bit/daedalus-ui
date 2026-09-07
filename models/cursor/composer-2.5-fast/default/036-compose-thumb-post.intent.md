# 036 编辑发布

## 意图元数据

- 意图版本：1
- 对应规范：`036-compose-thumb-post.spec.md`
- 说明：本文件不参与结构、尺寸、状态或交互验收。

## 设计意图

珊瑚色拇指帖编辑器：暖粉背景降低写作压力，顶栏「取消 | 发布」符合 mobile compose 惯例。字数与草稿状态合一行，发布门槛防误触空帖。

## 适用场景与目标用户

轻社交/笔记 App 移动端发帖；单手快速记录想法并选择发布或暂存。

## 非目标

无图片附件、@提及、话题标签选择器。

## 复刻提示词

Coral mobile compose screen：optional title + body、500 char counter with warn state、disabled publish until 10 chars、save draft pill button。
