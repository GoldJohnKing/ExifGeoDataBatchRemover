# ExifGeoDataBatchRemover

一个用于批量移除 JPG 图片 EXIF 地理位置数据的 Windows 命令行工具。

## 功能特点

- **递归扫描** - 自动扫描指定目录及所有子目录中的 JPG/JPEG 文件
- **选择性移除** - 仅移除 GPS 信息，保留其他 EXIF 元数据（如拍摄时间、相机型号等）
- **进度显示** - 每处理 100 个文件显示一次进度
- **统计报告** - 完成后显示处理统计（总数、成功、跳过、失败）
- **拖拽运行** - 支持将文件夹拖拽到 exe 文件上直接运行
- **容错处理** - 单个文件出错不影响整体处理，最后统一报告

## 使用方法

### 方式一：直接使用可执行文件（推荐）

从 [Releases](../../releases) 下载 `ExifGeoDataBatchRemover.exe`，然后：

```bash
# 命令行运行
ExifGeoDataBatchRemover.exe <文件夹路径>

# 或者直接将文件夹拖拽到 exe 文件上
```

### 方式二：从源码构建

**前置要求：**
- Python 3.x
- pip 或 uv 包管理器

**安装依赖：**
```bash
pip install -r requirements.txt
```

**构建可执行文件：**

Windows:
```bash
build.bat
```

WSL/Linux（交叉编译为 Windows exe）:
```bash
./build.sh
```

手动构建:
```bash
pyinstaller --onefile --console --name "ExifGeoDataBatchRemover" src/exif_geo_remover.py
```

## 示例输出

```
扫描目录: C:\Users\Photos

找到 500 个JPG文件
开始处理...

  进度: 100/500
  进度: 200/500
  ...

==================================================
处理完成
==================================================
  总文件数: 500
  移除GPS: 320
  已跳过:  175 (无GPS数据)
  失败:    5

按回车键退出...
```

## 项目结构

```
ExifGeoDataBatchRemover/
├── src/
│   └── exif_geo_remover.py    # 主程序
├── dist/
│   └── ExifGeoDataBatchRemover.exe  # 构建产物
├── docs/plans/
│   └── 2026-02-17-exif-geo-remover-design.md  # 设计文档
├── requirements.txt           # 依赖
├── build.bat                  # Windows 构建脚本
└── build.sh                   # WSL 构建脚本
```

## 技术栈

| 组件 | 技术 |
|------|------|
| 语言 | Python 3.x |
| EXIF 库 | [piexif](https://github.com/hMatoba/Piexif) |
| 构建工具 | [PyInstaller](https://pyinstaller.org/) |
| 目标平台 | Windows |

## 使用场景

- 分享照片前移除位置信息，保护隐私
- 批量处理大量照片的地理信息
- 发布到社交媒体前清理敏感位置数据

## 许可证

MIT License
