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

- [x] 4.1 运行 GUI，加载 coins.jpg 与 cookie-plate.jpg，确认标注 2 圆/1 圆并导出截图。
- [x] 4.2 更新 README 的运行、测试、验收参数与目录说明。
- [x] 4.3 提交实现并保持工作区干净。

## 验收记录

- 2026-11-13：`python3 -m unittest discover -s tests -v` → 7 tests OK。
- 2026-11-13：`examples/coins.jpg` + Coins 预设 → 2 圆，圆心约 `(193, 193, r180)`、`(567, 191, r179)`；导出 `docs/acceptance/coins-annotated.png`。
- 2026-11-13：`examples/cookie-plate.jpg` + Cookie Plate 预设 → 1 圆，圆心约 `(263, 259, r245)`；导出 `docs/acceptance/cookie-plate-annotated.png`。
- 2026-11-13：GUI 启动并进入事件循环；`minDist=800` 使硬币图从 2 圆变为 1 圆。
- 2026-11-13：`openspec validate add-hough-circle-gui --strict` → valid。

## 完成进度

- 任务：13/13 已完成（2026-11-13 完成，2026-11-17 复核）。
- 代码：图片导入、调参、预览、预设与导出均已实现；当前 `main` 可直接运行。
- 验收：`examples/coins.jpg`（760×385）→ 2 圆；`examples/cookie-plate.jpg`（520×520）→ 1 圆；测试 7/7 通过。
- OpenSpec：`openspec validate add-hough-circle-gui --strict` 通过。

## 未验证事项

- 仅在 Ubuntu 24.04.5 LTS（WSL2 + X11）实测；Windows、macOS 原生窗口、高 DPI 和不同 Tk 主题未验证。
- 仅锁定两张示例图；其他分辨率、光照、遮挡、重叠圆和低对比度场景未验证。
- 4K 或超大图片在主线程检测时的卡顿和内存占用未测量。
- 导出 JPEG 分支、非 ASCII/长路径、只读目录只在人工错误路径中检查过，未纳入自动化测试。
- 按文件名自动匹配预设的行为未做 UI 自动化；重命名图片后需手动选择预设。
- 视频、批量目录和实时相机输入未实现，见 `openspec/changes/add-video-detection/`。

## 后续待办

1. 实现 `openspec/changes/add-video-detection/`，完成视频导入、播放定位、逐帧检测与当前帧导出。
2. 为检测逻辑和 UI 状态增加无显示器回归用例，覆盖图像导入失败、导出失败和参数边界。
3. 评估大图检测的线程化、缓存或抽帧策略，避免界面长时间无响应。
4. 如需分发，补充打包、跨平台和高 DPI 验证。
