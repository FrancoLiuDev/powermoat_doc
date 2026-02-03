#!/usr/bin/env python3
"""
MD to HTML 打包工具 - 一次完成
直接从MD文件转换为HTML并复制图片，无需临时文件
"""

import sys
import re
import shutil
import subprocess
from pathlib import Path

# 静态IP配置
STATIC_IP = "124.218.37.90"
IMAGE_BASE_URL = f"http://{STATIC_IP}/html/doc/images/"

def process_md_images(md_content):
    """将MD中的#@img_标记替换为完整URL"""
    def replace_img(match):
        img_path = match.group(1)
        full_url = f"{IMAGE_BASE_URL}{img_path}"
        return f"[![image]({full_url})]({full_url})"
    
    return re.sub(r'#@img_([^\s]+)', replace_img, md_content)

def md_to_html(md_content, title="Document"):
    """使用pandoc将MD转换为HTML"""
    import tempfile
    
    # 创建临时MD文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(md_content)
        temp_md = f.name
    
    # 创建临时HTML文件
    temp_html = tempfile.mktemp(suffix='.html')
    
    try:
        # 运行pandoc
        cmd = [
            'pandoc',
            temp_md,
            '-o', temp_html,
            '--standalone',
            '--metadata', f'title={title}'
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        
        # 读取HTML
        with open(temp_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        return html_content
    finally:
        # 清理临时文件
        Path(temp_md).unlink(missing_ok=True)
        Path(temp_html).unlink(missing_ok=True)

def extract_and_copy_images(html_content, output_dir, source_images_dir):
    """提取并复制图片"""
    # 提取图片路径
    pattern = re.compile(rf'(?:src|href)="({re.escape(IMAGE_BASE_URL)}[^"]+)"')
    matches = pattern.findall(html_content)
    
    image_paths = []
    for match in matches:
        rel_path = match.replace(IMAGE_BASE_URL, '')
        if rel_path not in image_paths:
            image_paths.append(rel_path)
    
    if not image_paths:
        return html_content, 0
    
    print(f"🔍 找到 {len(image_paths)} 个图片引用")
    
    # 创建images目录
    images_dir = output_dir / 'images'
    images_dir.mkdir(parents=True, exist_ok=True)
    
    copied_count = 0
    for img_path in image_paths:
        src_file = source_images_dir / img_path
        dst_file = images_dir / img_path
        
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        
        if src_file.exists():
            shutil.copy2(src_file, dst_file)
            print(f"   ✅ {img_path}")
            copied_count += 1
        else:
            print(f"   ⚠️  未找到: {img_path}")
    
    # 更新HTML中的图片路径
    updated_content = html_content.replace(IMAGE_BASE_URL, 'images/')
    
    # 添加CSS样式
    css_style = '''
<style>
img {
    max-width: 80%;
    height: auto;
    display: block;
    margin: 10px 0;
}
</style>
'''
    
    if '</head>' in updated_content:
        updated_content = updated_content.replace('</head>', css_style + '</head>')
    elif '<body>' in updated_content:
        updated_content = updated_content.replace('<body>', css_style + '<body>')
    
    return updated_content, copied_count

def pack_md_to_html(md_file, output_dir='dist_html', source_images_dir='images'):
    """一次完成：MD -> HTML + 图片复制"""
    md_path = Path(md_file)
    
    if not md_path.exists():
        print(f"❌ 错误: 找不到文件 {md_file}")
        return False
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 输出HTML文件名
    output_html = output_path / f"{md_path.stem}.html"
    
    print(f"📄 读取: {md_file}")
    print(f"📤 输出: {output_html}")
    print()
    
    # 读取MD文件
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 处理图片标记
    print("🔄 处理 #@img_ 标记...")
    processed_md = process_md_images(md_content)
    
    # 转换为HTML
    print("📝 转换 MD -> HTML...")
    html_content = md_to_html(processed_md, md_path.stem)
    
    # 复制图片
    print("🖼️  复制图片...")
    updated_html, copied_count = extract_and_copy_images(
        html_content,
        output_path,
        Path(source_images_dir)
    )
    
    # 写入HTML文件
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    
    print()
    print(f"✅ 完成: {output_html}")
    print(f"📊 复制了 {copied_count} 个图片文件")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("MD to HTML 打包工具")
        print("=" * 60)
        print()
        print("使用方法:")
        print("  python3 pack_md_to_html.py <MD文件> [输出目录] [图片源目录]")
        print()
        print("参数:")
        print("  MD文件          要打包的Markdown文件")
        print("  输出目录        打包后的输出目录 (默认: ./dist_html)")
        print("  图片源目录      图片源文件目录 (默认: ./images)")
        print()
        print("范例:")
        print("  python3 pack_md_to_html.py docs/MANTIS.md")
        print("  python3 pack_md_to_html.py docs/MANTIS.md output")
        print("  python3 pack_md_to_html.py docs/MANTIS.md dist_html /path/to/images")
        print()
        print("功能:")
        print("  ✅ 自动处理 #@img_ 标记")
        print("  ✅ 转换 MD -> HTML")
        print("  ✅ 复制图片到本地 images 目录")
        print("  ✅ 更新图片路径为相对路径")
        print("  ✅ 图片最大宽度 80%")
        print("  ✅ 一次完成，无需临时文件")
        sys.exit(1)
    
    md_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'dist_html'
    source_images_dir = sys.argv[3] if len(sys.argv) > 3 else 'images'
    
    print()
    print("=" * 60)
    print("📦 MD to HTML 打包工具")
    print("=" * 60)
    print()
    
    success = pack_md_to_html(md_file, output_dir, source_images_dir)
    
    if success:
        print()
        print("=" * 60)
        print("✨ 打包完成！")
        print("=" * 60)

if __name__ == "__main__":
    main()
