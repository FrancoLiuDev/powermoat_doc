#!/usr/bin/env python3
"""
HTML打包工具 - 复制图片到本地images目录
将HTML中引用的远程图片复制到本地images目录，并更新路径
"""

import sys
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

# 静态IP配置
STATIC_IP = "124.218.37.90"
IMAGE_BASE_URL = f"http://{STATIC_IP}/html/doc/images/"

def extract_image_paths(html_content):
    """从HTML中提取所有图片路径"""
    image_paths = []
    
    # 匹配 <img src="http://STATIC_IP/html/doc/images/XXX/YYY.png">
    pattern = re.compile(rf'<img[^>]+src="({re.escape(IMAGE_BASE_URL)}[^"]+)"')
    matches = pattern.findall(html_content)
    
    for match in matches:
        # 提取相对路径部分 (例如: A0001/0001.png)
        rel_path = match.replace(IMAGE_BASE_URL, '')
        if rel_path not in image_paths:
            image_paths.append(rel_path)
    
    # 也匹配 <a href="..."> 中的图片链接
    pattern_link = re.compile(rf'<a[^>]+href="({re.escape(IMAGE_BASE_URL)}[^"]+)"')
    matches_link = pattern_link.findall(html_content)
    
    for match in matches_link:
        rel_path = match.replace(IMAGE_BASE_URL, '')
        if rel_path not in image_paths:
            image_paths.append(rel_path)
    
    return image_paths

def copy_images_to_local(html_file, output_dir, source_images_dir):
    """复制图片到本地目录"""
    html_path = Path(html_file)
    output_path = Path(output_dir)
    source_path = Path(source_images_dir)
    
    # 读取HTML内容
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 提取图片路径
    image_paths = extract_image_paths(html_content)
    
    if not image_paths:
        print("⚠️  未找到需要复制的图片")
        return html_content, 0
    
    print(f"🔍 找到 {len(image_paths)} 个图片引用")
    
    # 创建images目录
    images_dir = output_path / 'images'
    images_dir.mkdir(parents=True, exist_ok=True)
    
    copied_count = 0
    
    for img_path in image_paths:
        # 源文件路径
        src_file = source_path / img_path
        
        # 目标文件路径
        dst_file = images_dir / img_path
        
        # 创建目标目录
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 复制文件
        if src_file.exists():
            shutil.copy2(src_file, dst_file)
            print(f"   ✅ {img_path}")
            copied_count += 1
        else:
            print(f"   ⚠️  未找到: {img_path}")
    
    # 更新HTML中的图片路径为相对路径
    updated_content = html_content.replace(IMAGE_BASE_URL, 'images/')
    
    return updated_content, copied_count

def pack_html_with_images(input_file, output_dir=None, source_images_dir='images'):
    """打包HTML并复制图片"""
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"❌ 错误: 找不到文件 {input_file}")
        return False
    
    # 如果未指定输出目录，使用输入文件所在目录
    if output_dir is None:
        output_dir = input_path.parent / 'packed'
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 输出HTML文件名
    output_html = output_path / input_path.name
    
    print(f"📄 读取: {input_file}")
    print(f"📤 输出: {output_html}")
    print()
    
    # 复制图片到本地
    print("🖼️  复制图片...")
    updated_content, copied_count = copy_images_to_local(
        input_file, 
        output_path, 
        source_images_dir
    )
    
    # 写入更新后的HTML
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print()
    print(f"✅ 完成: {output_html}")
    print(f"📊 复制了 {copied_count} 个图片文件")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("HTML 打包工具 - 复制图片到本地")
        print("=" * 60)
        print()
        print("使用方法:")
        print("  python3 pack_html_with_images.py <HTML文件> [输出目录] [图片源目录]")
        print()
        print("参数:")
        print("  HTML文件        要打包的HTML文件")
        print("  输出目录        打包后的输出目录 (默认: ./packed)")
        print("  图片源目录      图片源文件目录 (默认: ./images)")
        print()
        print("范例:")
        print("  python3 pack_html_with_images.py docs/index.html")
        print("  python3 pack_html_with_images.py docs/index.html output")
        print("  python3 pack_html_with_images.py docs/index.html output /path/to/images")
        print()
        print("功能:")
        print("  ✅ 从远程URL中提取图片路径")
        print("  ✅ 复制图片到本地 images 目录")
        print("  ✅ 更新HTML中的图片路径为相对路径")
        print("  ✅ 保持目录结构 (如: images/A0001/0001.png)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    source_images_dir = sys.argv[3] if len(sys.argv) > 3 else 'images'
    
    print()
    print("=" * 60)
    print("📦 HTML 打包工具 - 图片本地化")
    print("=" * 60)
    print()
    
    success = pack_html_with_images(input_file, output_dir, source_images_dir)
    
    if success:
        print()
        print("=" * 60)
        print("✨ 打包完成！")
        print("=" * 60)

if __name__ == "__main__":
    main()
