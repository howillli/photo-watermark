---
name: photo-watermark
description: Add a white-bordered watermark frame to photos. Extracts EXIF data to display camera model and shooting parameters (aperture, shutter speed, ISO). Supports major camera brands including Sony, Fujifilm, Nikon, Canon, Panasonic, Vivo, Apple, and Huawei with logo display. Use when generating professional photo watermarks, processing photography metadata, or creating signature frames for images.
---

# 照片水印生成器 (Photo Watermark Generator)

## 快速开始

为照片添加带有白边底框的专业水印，包含：
- **左侧**：相机品牌Logo + 相机型号
- **右侧**：光圈、快门速度、ISO参数

支持品牌：索尼(Sony)、富士(Fujifilm)、尼康(Nikon)、佳能(Canon)、松下(Panasonic/Lumix)、vivo、苹果(Apple)、华为(Huawei)

## 使用方式

### Python脚本方式

```python
# 直接调用
from scripts.add_photo_watermark import add_watermark_to_image

# 自动读取EXIF并生成水印
add_watermark_to_image("photo.jpg", "output.jpg", border_size=120)
```

### 命令行方式

```bash
python scripts/add_photo_watermark.py <输入图片> [输出图片]

# 示例
python scripts/add_photo_watermark.py photo.jpg
python scripts/add_photo_watermark.py photo.jpg watermarked.jpg
```

## 生成品牌Logo

如需重新生成品牌Logo文件：

```bash
python scripts/generate_logos.py
```

## 功能特性

### 1. EXIF数据读取
- 自动提取照片中的EXIF元数据
- 获取相机制造商(Make)和型号(Model)
- 读取光圈值(FNumber)、快门速度(ExposureTime)、ISO感光度

### 2. 品牌自动识别
根据相机信息自动匹配品牌：
- Sony/α/Alpha → 索尼
- Fujifilm/Fuji/GFX/X-T/X-Pro → 富士
- Nikon/Z/D/Coolpix → 尼康
- Canon/EOS/PowerShot → 佳能
- Panasonic/Lumix → 松下
- vivo → vivo
- Apple/iPhone/iPad → 苹果
- Huawei/P/Mate/Honor → 华为

### 3. 水印布局
- **位置**：图片底部
- **样式**：白色底框
- **左侧**：品牌Logo图标 + 相机型号名称（黑色粗体）
- **右侧**：光圈 | 快门 | ISO（灰色字体）
- **参数自动格式化**：
  - 光圈：f/2.8 格式
  - 快门：1/125s 或 2s 格式
  - ISO：ISO 400 格式

### 4. 输出格式
- 默认输出为JPEG格式
- 质量设置为95%
- 保持原始图片比例

## 示例

输入图片：`IMG_2024.jpg` (Sony α7 IV拍摄, f/1.8, 1/250s, ISO 640)

输出效果：
```
┌─────────────────────────────────────────────┐
│                                             │
│         [原始图片内容]                       │
│                                             │
├─────────────────────────────────────────────┤
│ [索尼Logo] α7 IV                f/1.8 │ 1/250s │ ISO 640 │
└─────────────────────────────────────────────┘
```

## 处理流程

为照片添加水印的步骤：

1. **读取图片**：加载原始图片文件
2. **提取EXIF**：获取相机型号和拍摄参数
3. **品牌识别**：根据相机信息匹配品牌Logo
4. **创建底框**：在图片底部添加白色边框
5. **添加水印**：
   - 在底框左侧放置品牌Logo和相机型号
   - 在底框右侧放置拍摄参数
6. **保存输出**：生成带水印的最终图片

## 文件结构

```
photo-watermark/
├── assets/
│   └── logos/
│       ├── sony.png       # 品牌Logo图片
│       ├── fujifilm.png
│       ├── nikon.png
│       ├── canon.png
│       ├── panasonic.png
│       ├── vivo.png
│       ├── apple.png
│       └── huawei.png
├── scripts/
│   ├── add_photo_watermark.py   # 主水印脚本
│   └── generate_logos.py        # Logo生成器
└── SKILL.md                     # 本说明文档
```

## 边界情况处理

### 无EXIF数据
如果图片没有EXIF信息，将显示：
- 相机型号：Unknown Camera
- 拍摄参数：N/A | N/A | ISO N/A
- 品牌Logo：显示通用标识或文字

### 未知品牌
如果相机品牌不在支持列表中，将：
- 显示相机型号文字
- 不显示品牌Logo图标

### 参数缺失
如果部分EXIF参数缺失（如没有光圈信息），该参数将显示为"N/A"。

## 自定义配置

可以通过修改 `add_photo_watermark.py` 中的参数调整水印样式：

```python
# 调整底框高度
border_size = 120  # 像素

# 调整字体大小
left_font_size = max(24, int(border_size * 0.35))
right_font_size = max(20, int(border_size * 0.30))

# 调整Logo大小
logo_size = (int(border_size * 0.5), int(border_size * 0.5))
```

## 注意事项

- 支持的图片格式：JPEG（推荐）、PNG、TIFF、BMP等（需PIL支持）
- 输出始终为JPEG格式
- 需要安装 Pillow 库：`pip install Pillow`
