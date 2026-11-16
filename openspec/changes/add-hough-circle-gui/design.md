# Design

## Context

OpenCV `HoughCircles` 已能在两张示例图上得到稳定结果：硬币 `param2=30, radius=120–200` → 2 圆；饼干盘 `param2=30, radius=200–270` → 1 圆。工具需要在保持检测逻辑可测试的前提下提供图形界面。见 `proposal.md`。

## Goals / Non-Goals

**Goals:**
- 单窗口完成导入、调参、预览、导出。
- 检测逻辑与 Tkinter 解耦，可在无显示器环境测试。
- 两套示例预设直接满足验收。

**Non-Goals:**
- 不处理视频流、批量目录或实时相机；录制的视频文件检测见 [`../add-video-detection/`](../add-video-detection/)（规划中）。
- 不做自动参数搜索。
- 不打包为可执行文件。

## Decisions

- 使用 Tkinter：系统自带，依赖最少；Pillow 负责 BGR→RGB 与缩放显示。
- `detector.py` 提供 `detect_circles(image, params)` 与 `annotate_image(image, circles)`，不导入 Tkinter。
- `presets.py` 保存硬币、饼干盘和通用参数；按文件名匹配预设，也可手动切换。
- UI 使用左侧参数面板 + 右侧 Canvas；滑块变化后 150 ms 防抖检测，避免连续拖动时阻塞。
- 检测在原始分辨率上执行；显示仅做等比缩放，避免缩放影响圆心与半径。
- 导出使用 Pillow 保存标注图，兼容含非 ASCII 字符的路径。
- 异常通过 `messagebox` 与状态栏反馈，不静默吞掉。

## Risks / Trade-offs

- Hough 参数对光照和尺度敏感 → 提供预设与实时调参；验收只锁定两张示例图。
- 检测在 UI 线程执行，超大图可能短暂卡顿 → 当前图片尺寸有限，先不引入线程。
- 预设按文件名匹配，用户重命名后需手动选择 → 预设按钮始终可见。

## Migration

无迁移，新增项目。
