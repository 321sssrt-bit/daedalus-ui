---
status: accepted
---

# 旧答卷只做本地扁平归档

旧 40 题答卷在重做前移动到 `archive/<harness>-<model>-<思考档位>/` 留底，`archive/` 由 Git 忽略，不上传 GitHub，也不进入新版展厅。这样保留本机恢复能力，同时让公开仓库只承载符合当前 50 题与身份标注规则的答卷。
