# Tasks

## 1. 项目骨架与规格

- [x] 1.1 初始化 Git、README、.gitignore、示例图与来源说明；`git log` 确认初始提交。
- [x] 1.2 初始化 OpenSpec 与 AGENTS.md；`openspec list` 识别项目。
- [x] 1.3 完成 proposal/specs/design/tasks；`openspec validate add-hough-circle-gui --strict` 通过。

## 2. 检测核心

- [x] 2.1 实现 `detect_circles` 与 `annotate_image`；用两张示例图验证分别得到 2/1 个圆。
- [x] 2.2 实现硬币、饼干盘、通用预设；验证参数值符合设计。
- [x] 2.3 添加 unittest，覆盖两图圆数量、标注尺寸和参数校验；`python3 -m unittest discover -s tests -v` 通过。

## 3. 图形界面

- [x] 3.1 实现导入与画布等比预览；验证打开两张示例图后尺寸显示正确。
- [x] 3.2 实现六项滑块、预设与防抖刷新；验证拖动后圆数量随参数更新。
- [x] 3.3 实现导出标注图；验证导出文件尺寸与原图一致。
- [x] 3.4 处理导入/导出失败与取消路径；验证无异常崩溃。

## 4. 验收与文档

- [ ] 4.1 运行 GUI，加载 coins.jpg 与 cookie-plate.jpg，确认标注 2 圆/1 圆并导出截图。
- [ ] 4.2 更新 README 的运行、测试、验收参数与目录说明。
- [ ] 4.3 提交实现并保持工作区干净。
