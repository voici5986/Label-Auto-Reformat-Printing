#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将PNG图标转换为ICO格式
用于Windows应用程序图标
"""

from PIL import Image

def png_to_ico(png_path, ico_path, sizes=[16, 32, 48, 64, 128, 256]):
    """
    将PNG转换为多尺寸ICO文件
    
    Args:
        png_path: PNG文件路径
        ico_path: 输出ICO文件路径
        sizes: 图标尺寸列表
    """
    # 打开原始PNG图片
    img = Image.open(png_path)
    
    # 如果有透明通道，保持透明
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # 创建不同尺寸的图标
    images = []
    for size in sizes:
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        images.append(resized)
    
    # 保存为ICO文件（包含多个尺寸）
    images[0].save(
        ico_path,
        format='ICO',
        sizes=[(img.width, img.height) for img in images]
    )
    
    print(f"Success! Created icon: {ico_path}")
    print(f"Sizes: {', '.join([f'{s}x{s}' for s in sizes])}")

if __name__ == "__main__":
    try:
        # 使用现有的label.png创建图标
        png_to_ico('label.png', 'label.ico')
        print("\nIcon conversion completed!")
    except Exception as e:
        print(f"Error: {e}")