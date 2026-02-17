#!/usr/bin/env python3
"""
EXIF地理数据批量移除工具
递归移除指定目录下所有JPG文件的GPS EXIF数据
"""

import sys
import os
from pathlib import Path

import piexif


def pause():
    """等待用户按键（仅在交互模式下）"""
    if sys.stdin.isatty():
        try:
            input("按回车键退出...")
        except EOFError:
            pass


def remove_gps_data(jpg_path: Path) -> tuple[bool, str]:
    """
    移除单个JPG文件的GPS EXIF数据

    Returns:
        (success, status): status为 'success', 'skipped', 'failed'
    """
    try:
        # 读取EXIF数据
        exif_dict = piexif.load(str(jpg_path))

        if exif_dict is None:
            return (True, "skipped")

        # 检查是否存在GPS数据
        if "GPS" not in exif_dict or not exif_dict["GPS"]:
            return (True, "skipped")

        # 删除GPS IFD
        exif_dict["GPS"] = {}

        # 序列化并写回
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, str(jpg_path))

        return (True, "success")

    except piexif.InvalidImageDataError:
        # 不是有效的图片文件
        return (True, "skipped")
    except Exception as e:
        return (False, f"failed: {e}")


def scan_jpg_files(directory: Path) -> list[Path]:
    """递归扫描目录下所有JPG文件"""
    jpg_files = []
    for ext in ["*.jpg", "*.jpeg", "*.JPG", "*.JPEG"]:
        jpg_files.extend(directory.rglob(ext))
    # 去重（大小写重叠的情况）
    return list(set(jpg_files))


def main():
    # 检查参数
    if len(sys.argv) < 2:
        print("EXIF地理数据批量移除工具")
        print()
        print("用法:")
        print("  exif_geo_remover.exe <文件夹路径>")
        print()
        print("说明:")
        print("  递归移除指定目录及其子目录下所有JPG文件的GPS地理数据")
        print("  可将文件夹拖拽到exe文件上运行")
        print()
        pause()
        sys.exit(1)

    target_path = Path(sys.argv[1])

    # 验证路径
    if not target_path.exists():
        print(f"错误: 路径不存在 - {target_path}")
        pause()
        sys.exit(1)

    if not target_path.is_dir():
        print(f"错误: 不是有效的文件夹 - {target_path}")
        pause()
        sys.exit(1)

    print(f"扫描目录: {target_path}")
    print()

    # 扫描文件
    jpg_files = scan_jpg_files(target_path)

    if not jpg_files:
        print("未找到JPG文件")
        pause()
        sys.exit(0)

    print(f"找到 {len(jpg_files)} 个JPG文件")
    print("开始处理...")
    print()

    # 统计
    stats = {
        "total": len(jpg_files),
        "success": 0,  # 成功移除GPS
        "skipped": 0,  # 跳过（无GPS或无EXIF）
        "failed": 0,  # 失败
    }
    failed_files = []

    # 处理每个文件
    for i, jpg_path in enumerate(jpg_files, 1):
        success, status = remove_gps_data(jpg_path)

        if status == "success":
            stats["success"] += 1
        elif status == "skipped":
            stats["skipped"] += 1
        else:
            stats["failed"] += 1
            failed_files.append((jpg_path, status))

        # 进度显示
        if i % 100 == 0 or i == len(jpg_files):
            print(f"  进度: {i}/{len(jpg_files)}")

    # 输出结果
    print()
    print("=" * 50)
    print("处理完成")
    print("=" * 50)
    print(f"  总文件数: {stats['total']}")
    print(f"  移除GPS: {stats['success']}")
    print(f"  已跳过:  {stats['skipped']} (无GPS数据)")
    print(f"  失败:    {stats['failed']}")

    if failed_files:
        print()
        print("失败文件:")
        for path, reason in failed_files[:10]:  # 最多显示10个
            print(f"  - {path}: {reason}")
        if len(failed_files) > 10:
            print(f"  ... 还有 {len(failed_files) - 10} 个")

    print()
    pause()


if __name__ == "__main__":
    main()
