# hough-circle-gui

基于 OpenCV 的霍夫圆检测图形工具：导入实拍图片，调整检测参数，实时预览标注结果，并导出标注图。

## 功能

- 导入 JPG、JPEG、PNG、BMP 图片。
- 调整 `dp`、`minDist`、`param1`、`param2`、`minRadius`、`maxRadius`。
- 在画布上预览检测到的圆、圆心与编号。
- 导出带标注的 PNG 或 JPG。
- 内置「硬币」与「饼干盘」两组示例参数。

## 环境

已验证环境：

| 组件 | 版本 |
|---|---|
| OS | Ubuntu 24.04.5 LTS（WSL2） |
| Python | 3.12.3 |
| OpenCV | 4.6.0 |
| Tkinter | 8.6 |
| Pillow | 10.2.0 |

## 安装

```bash
sudo apt install -y python3-tk
python3 -m pip install -r requirements.txt
```

系统已提供 OpenCV、Tkinter、Pillow 时可跳过安装，直接运行。

## 运行

```bash
python3 main.py
```

界面操作：

- `Open Image` 选择本地图片。
- `Coins Sample` / `Plate Sample` 载入验收图片并自动应用预设。
- `Preset` 切换 `Auto`、`Coins`、`Cookie Plate` 或手动参数。
- 六个滑块调整检测参数；停止拖动约 150 ms 后自动刷新。
- `Detect` 立即重新检测。
- `Export Annotated` 导出当前标注图。

界面标签使用英文；本机未安装中文字体，避免 Tk 显示方框。

## 测试

```bash
python3 -m unittest discover -s tests -v
```

当前结果：7 个测试全部通过。

## 验收

实际运行日期：2026-11-13。

| 图片 | 预设 | dp | minDist | param1 | param2 | 半径范围 | 结果 |
|---|---|---|---|---|---|---|---|
| `examples/coins.jpg` | Coins | 1.2 | 250 | 100 | 30 | 120–200 | 2 个圆，两枚硬币外缘 |
| `examples/cookie-plate.jpg` | Cookie Plate | 1.2 | 250 | 100 | 30 | 200–270 | 1 个圆，盘沿 |

标注结果已导出到 `exports/`（目录不入库）：

- `coins-annotated.png`：两个圆分别位于两枚硬币外缘。
- `cookie-plate-annotated.png`：一个圆贴合饼干盘盘沿。

其他已验证行为：

- GUI 可正常进入事件循环。
- 导入无法解码的图片会提示错误并保留当前图片。
- 导出到不可写路径会提示错误，不崩溃。
- `openspec validate add-hough-circle-gui --strict` 通过。

## 目录

```text
hough-circle-gui/
├─ main.py                    # 图形界面入口
├─ hough_circle_gui/
│  ├─ app.py                  # Tkinter 界面、预览、导出
│  ├─ detector.py             # 霍夫圆检测与标注
│  └─ presets.py              # 硬币/饼干盘/通用参数
├─ tests/test_detector.py     # 检测逻辑测试
├─ examples/                  # 验收图片与来源说明
├─ openspec/                  # OpenSpec 变更记录
├─ requirements.txt
├─ AGENTS.md
└─ README.md
```

## 图片授权

见 [examples/SOURCES.md](examples/SOURCES.md)。
