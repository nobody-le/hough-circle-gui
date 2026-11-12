# Proposal

## Why

霍夫圆检测对 `dp`、阈值和半径范围敏感，命令行反复改参难以直观判断结果。需要一个图形界面，让使用者导入实拍图片、调参并立即看到标注效果，同时能把结果导出给队友复核。

## What Changes

- 新增基于 Tkinter 的桌面 GUI。
- 支持导入 JPG、JPEG、PNG、BMP 图片并在画布中预览。
- 提供 `dp`、`minDist`、`param1`、`param2`、`minRadius`、`maxRadius` 六项参数调节。
- 实时绘制检测到的圆、圆心与编号，并显示圆数量。
- 支持导出带标注的 PNG/JPG。
- 内置硬币与饼干盘两组参数预设。
- 增加检测逻辑测试与两张示例图的验收。

## Capabilities

### New Capabilities

- `hough-circle-gui`: 提供霍夫圆检测的导入、调参、预览、导出与示例验收行为。

### Modified Capabilities

无。

## Impact

- 新增 Python 包 `hough_circle_gui`、入口 `main.py`、测试与示例图。
- 依赖 OpenCV、Tkinter、Pillow；不改变系统环境。
