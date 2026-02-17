# EXIF地理数据批量移除工具设计

## 概述

Windows平台命令行工具，用于批量移除JPG文件EXIF信息中的GPS地理数据。

## 需求

- **输入**: 文件夹路径（命令行参数或拖拽到exe）
- **处理**: 递归扫描所有子目录下的JPG文件，移除GPS EXIF数据
- **输出**: 简洁的统计信息（处理总数、成功、跳过、失败）

## 技术选型

- **语言**: Python 3.x
- **EXIF库**: piexif（专为EXIF设计，GPS标签处理直接明确）
- **打包工具**: PyInstaller（单文件exe模式）

## 架构

```
ExifGeoDataBatchRemover.exe
├── CLI入口 - 解析命令行参数
├── 文件扫描器 - 递归查找 .jpg/.jpeg 文件
├── EXIF处理器 - 使用piexif移除GPS IFD
└── 进度统计 - 输出处理结果
```

## 核心功能

### 1. CLI入口
- 接收sys.argv参数
- 验证路径有效性
- 无参数时显示使用说明

### 2. 文件扫描
- 使用pathlib递归扫描
- 支持大小写不敏感的 .jpg/.jpeg 扩展名

### 3. EXIF处理
- 使用piexif.load()读取EXIF
- 删除 'GPS' IFD（piexif.GPSIFD）
- 使用piexif.dump()和piexif.insert()写回
- 无EXIF或无GPS的文件跳过

### 4. 统计输出
- 显示处理进度（每100个文件）
- 最终统计：总数、成功、跳过、失败

## 错误处理

| 场景 | 行为 |
|------|------|
| 无效路径 | 提示错误，退出 |
| 无EXIF的JPG | 跳过 |
| 无GPS数据 | 跳过 |
| 读写错误 | 记录失败，继续 |
| 权限错误 | 提示，跳过 |

## 打包配置

```bash
pyinstaller --onefile --console exif_geo_remover.py
```

预期exe体积：10-15MB

## 项目结构

```
ExifGeoDataBatchRemover/
├── src/
│   └── exif_geo_remover.py    # 主程序
├── requirements.txt           # 依赖：piexif, pyinstaller
├── build.bat                  # 打包脚本
└── docs/plans/                # 设计文档
```
