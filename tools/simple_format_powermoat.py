#!/usr/bin/env python3
"""
格式化PowerMoat管理系統維運手冊 - 简化版
只进行必要的图片路径替换
"""
import re

def format_document(input_file, output_file):
    """格式化文档"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单替换: images/media/imageXX.png -> #@img_A0005/imageXX.png
    content = re.sub(r'images/media/', '#@img_A0005/', content)
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 图片路径替换完成: {output_file}")
    
    # 统计替换数量
    count = content.count('#@img_A0005/')
    print(f"📸 共替换 {count} 个图片引用")

if __name__ == "__main__":
    input_file = "root/PSS/PowerMoat管理系統維運手冊.md"
    output_file = "root/PSS/PowerMoat管理系統維運手冊.md"
    
    format_document(input_file, output_file)
