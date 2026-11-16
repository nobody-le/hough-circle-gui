# 项目约定

## 项目

`hough-circle-gui` 是一个基于 OpenCV 的霍夫圆检测桌面工具。用户导入实拍图片后，通过图形界面调整检测参数、预览标注结果并导出标注图。

## 技术栈

- Python 3.12
- OpenCV 4.6
- Tkinter 8.6（系统 `python3-tk`）
- Pillow 10.x

## 常用命令

```bash
python3 main.py
python3 -m unittest discover -s tests -v
```

## 代码结构

- `main.py`：图形界面入口。
- `hough_circle_gui/detector.py`：纯检测逻辑，禁止依赖 Tkinter。
- `hough_circle_gui/presets.py`：硬币、饼干盘和通用（Auto）参数预设。
- `hough_circle_gui/app.py`：Tkinter 界面、预览与导出。
- `tests/`：检测逻辑与验收场景测试。
- `examples/`：验收图片与来源说明。

## 开发规则

- 一次工作分支只解决一个 OpenSpec change；先完成 proposal/specs/design/tasks，再实现。
- 检测逻辑与 UI 分离，`detector.py` 必须可在无显示器环境中测试。
- 修改参数语义时同步更新 `presets.py`、测试和 README。
- 不静默吞异常；文件读取、导出失败要反馈到界面。
- 验收必须覆盖 `examples/coins.jpg`（2 个圆）和 `examples/cookie-plate.jpg`（1 个圆）。
- 提交信息使用 `<type>: <short description>`，例如 `feat: 实现霍夫圆检测界面`。
- 导出目录 `exports/`、虚拟环境和缓存不入库。
