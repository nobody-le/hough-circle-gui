# Spec Delta

## Purpose

定义霍夫圆检测图形工具的用户可见行为，覆盖图片导入、参数调节、结果预览、标注导出，以及两张实拍图的验收结果。

## ADDED Requirements

### Requirement: 导入图片

工具 SHALL 允许用户从本地选择 JPG、JPEG、PNG 或 BMP 图片，并在画布中按比例完整显示。读取失败时 MUST 提示错误并保留当前图片状态。

#### Scenario: 成功导入

- **WHEN** 用户选择一张受支持的图片
- **THEN** 画布显示该图片，状态栏显示文件名与尺寸

#### Scenario: 导入失败

- **WHEN** 用户选择的文件无法解码
- **THEN** 工具提示错误，原图片和检测结果保持不变

### Requirement: 调整检测参数

工具 SHALL 提供 `dp`、`minDist`、`param1`、`param2`、`minRadius`、`maxRadius` 六项可调参数，并在参数变化后重新检测当前图片。

#### Scenario: 修改参数

- **WHEN** 用户拖动任一参数滑块
- **THEN** 界面显示新数值，并在短暂防抖后刷新检测结果

#### Scenario: 应用示例预设

- **WHEN** 用户选择硬币或饼干盘预设
- **THEN** 六项参数切换到该预设值并刷新预览

### Requirement: 预览检测结果

工具 SHALL 在图片上绘制检测到的圆、圆心和编号，并显示本次检测到的圆数量。

#### Scenario: 检测到圆

- **WHEN** 当前参数得到至少一个圆
- **THEN** 画布显示标注，状态栏显示圆数量

#### Scenario: 未检测到圆

- **WHEN** 当前参数没有得到圆
- **THEN** 画布显示原图，圆数量为 0，不报错

### Requirement: 导出标注图

工具 SHALL 将当前带标注的图片导出为 PNG 或 JPG，并保留原图尺寸。

#### Scenario: 导出成功

- **WHEN** 用户选择保存路径并确认
- **THEN** 目标文件包含当前标注结果，尺寸与原图一致

#### Scenario: 取消导出

- **WHEN** 用户在保存对话框中取消
- **THEN** 不创建文件，界面状态不变

### Requirement: 示例图验收

使用硬币预设处理 `examples/coins.jpg` 时，工具 MUST 检测并标注 2 个圆，对应两枚硬币外缘；使用饼干盘预设处理 `examples/cookie-plate.jpg` 时，MUST 检测并标注 1 个圆，对应盘沿。

#### Scenario: 硬币图

- **WHEN** 加载 `examples/coins.jpg` 并应用硬币预设
- **THEN** 检测结果为 2 个圆

#### Scenario: 饼干盘图

- **WHEN** 加载 `examples/cookie-plate.jpg` 并应用饼干盘预设
- **THEN** 检测结果为 1 个圆
