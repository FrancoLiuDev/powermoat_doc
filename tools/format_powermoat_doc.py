#!/usr/bin/env python3
"""
格式化PowerMoat管理系統維運手冊，使其符合PSS文档样式
"""
import re

def format_document(input_file, output_file):
    """格式化文档"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 先清理图片前的描述文字
    # 移除类似 "![一張含有...的圖片\n> 自動產生的描述" 这样的描述
    content = re.sub(r'!\[一張含有[^\]]*\]\s*\n>\s*自動產生的描述', '', content)
    content = re.sub(r'!\[[^\]]*自動產生的描述[^\]]*\]', '', content)
    
    # 2. 替换图片路径为 #@img_ 格式
    # 原格式: ](images/media/imageXX.png) 或相关变体
    # 新格式: #@img_A0005/imageXX.png
    def replace_image(match):
        full_match = match.group(0)
        # 提取图片文件名
        img_match = re.search(r'images/media/([^)}\s]+)', full_match)
        if img_match:
            img_name = img_match.group(1)
            return f"\n\n#@img_A0005/{img_name}\n"
        return full_match
    
    # 匹配所有包含 images/media 的引用
    content = re.sub(r'(?:!\[[^\]]*\])?\(images/media/[^)]+\)(?:\{[^}]+\})?', replace_image, content)
    
    # 2. 清理目录部分（保留但简化）
    # 移除带有下划线样式的链接
    content = re.sub(r'\[\[([^\]]+)\]\{\.underline\}\s+\d+\]\(#[^)]+\)', r'\1', content)
    
    # 3. 清理表格中的多余空格
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # 移除行首的多余 > 引用符号
        line = line.lstrip('> ').rstrip()
        
        # 移除 {#xxx .ad} 这样的标记
        line = re.sub(r'\s*\{#[^}]+\}', '', line)
        
        # 移除 {.underline} 这样的样式标记
        line = re.sub(r'\{\.underline\}', '', line)
        
        cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    # 4. 优化标题格式
    # 将 "=====" 样式的标题转换为 "##" 样式
    content = re.sub(r'^(.+)\n=+\s*$', r'## \1', content, flags=re.MULTILINE)
    content = re.sub(r'^(.+)\n-+\s*$', r'### \1', content, flags=re.MULTILINE)
    
    # 5. 清理多余的空行（超过2个连续空行的情况）
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    # 6. 添加文档头部（参考PSS_漫遊列印_主程式.md的样式）
    header = """# PowerMoat 管理系統維運手冊

## 專案概述

PowerMoat 系統維運手冊 - 包含系統安裝、配置、操作及維護的完整指南。

**文件版本**: v20250827  
**更新日期**: 2025/8/27  
**編寫**: Peter Lai  
**公司**: 互成合資安系統整合股份有限公司

---

"""
    
    # 移除原始的标题部分
    content = re.sub(r'^\s*\*\*互成合.*?\*\*.*?目錄.*?====\s*', '', content, flags=re.DOTALL)
    
    # 组合最终内容
    final_content = header + content
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"✅ 格式化完成: {output_file}")

if __name__ == "__main__":
    input_file = "root/PSS/PowerMoat管理系統維運手冊.md"
    output_file = "root/PSS/PowerMoat管理系統維運手冊.md"
    
    format_document(input_file, output_file)
