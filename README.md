# hough-circle-gui

基于 OpenCV 的霍夫圆检测图形工具：导入实拍图片，调整检测参数，实时预览标注结果，并导出标注图。

## 功能

- 导入 JPG、JPEG、PNG、BMP 图片。
- 调整 `dp`、`minDist`、`param1`、`param2`、`minRadius`、`maxRadius`。
- 在画布上预览检测到的圆、圆心与编号。
- 导出带标注的 PNG 或 JPG。
- 内置「硬币」与「饼干盘」两组示例参数，便于快速验收。

## 环境

已验证环境：

| 组件 | 版本 |
|---|---|
| OS | Ubuntu 24.04.5 LTS（WSL2） |
| Python | 3.12.3 |
| OpenCV | 4.6.0 |
| Tkinter | 8.6 |
| Pillow | 10.2.0 |

依赖：

```bash
sudo apt install -y python3-tk
python3 -m pip install -r requirements.txt
```

## 运行

```bash
python3 main.py
```

## 验收

| 图片 | 预期结果 |
|---|---|
| `examples/coins.jpg` | 2 个圆，标出两枚硬币外缘 |
| `examples/cookie-plate.jpg` | 1 个圆，标出盘沿 |

验收命令与检测参数在实现完成后记录于本节。

## 目录

```text
hough-circle-gui/
├─ main.py                 # 图形界面入口
├─ hough_circle_gui/       # 检测逻辑与 UI
├─ tests/                  # 自动化测试
├─ examples/               # 验收图片与来源说明
├─ requirements.txt
└─ README.md
```

## 图片授权

见 [examples/SOURCES.md](examples/SOURCES.md)。
