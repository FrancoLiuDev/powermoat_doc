#!/usr/bin/env python3
"""
將 root 目錄下的所有 MD 文件轉換成 HTML
保持目錄結構，輸出到 dist/html
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil
import re

# ========== 靜態參數設定 ==========
# 將所有文件中的 IP 替換為此靜態 IP
STATIC_IP = "124.218.37.90"
# ==================================

def convert_md_to_html(md_file, output_dir, base_dir):
    """轉換單個 MD 文件為 HTML"""
    md_path = Path(md_file)
    
    # 讀取 MD 文件內容
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替換參數化的 IP 為靜態 IP
    content = content.replace('#@ip', STATIC_IP)
    
    # 替換 #@img_ 為完整的圖片 URL
    # 例如: #@img_A0004/0011.png -> [![image](http://STATIC_IP/html/doc/images/A0004/0011.png)](http://STATIC_IP/html/doc/images/A0004/0011.png)
    def replace_image_path(match):
        img_path = match.group(1)
        full_url = f"http://{STATIC_IP}/html/en/images/{img_path}"
        return f"[![image]({full_url})]({full_url})"
    
    content = re.sub(r'#@img_([^\s]+)', replace_image_path, content)
    
    # 計算相對路徑
    rel_path = md_path.relative_to(base_dir)
    
    # 創建對應的輸出目錄
    output_subdir = output_dir / rel_path.parent
    output_subdir.mkdir(parents=True, exist_ok=True)
    
    # 創建臨時文件來保存替換後的內容
    temp_md_file = output_subdir / f"temp_{md_path.name}"
    with open(temp_md_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 輸出文件名
    html_filename = md_path.stem + '.html'
    html_path = output_subdir / html_filename
    
    # 使用 pandoc 轉換
    cmd = [
        'pandoc',
        str(temp_md_file),
        '-o', str(html_path),
        '--standalone',
        '--toc',
        '--toc-depth=3',
        '--metadata', f'title={md_path.stem}',
        '--css', 'https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown.min.css'
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        # 刪除臨時文件
        temp_md_file.unlink()
        return html_path
    except subprocess.CalledProcessError as e:
        print(f"❌ 轉換失敗: {md_file}")
        print(f"   錯誤: {e.stderr.decode()}")
        # 清理臨時文件
        if temp_md_file.exists():
            temp_md_file.unlink()
        return None

def find_all_md_files(directory):
    """遞迴查找所有 MD 文件"""
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append(Path(root) / file)
    return md_files

def create_index_html(output_dir, html_files, base_dir):
    """創建索引頁面"""
    index_path = output_dir / 'index.html'
    
    # 組織文件結構
    file_tree = {}
    for html_file in html_files:
        rel_path = html_file.relative_to(output_dir)
        parts = rel_path.parts
        
        if len(parts) > 1:
            folder = parts[0]
            if folder not in file_tree:
                file_tree[folder] = []
            file_tree[folder].append(rel_path)
        else:
            if 'root' not in file_tree:
                file_tree['root'] = []
            file_tree['root'].append(rel_path)
    
    html_content = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文件索引</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .folder {
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .folder-title {
            font-size: 1.5em;
            font-weight: 600;
            color: #667eea;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .file-list {
            list-style: none;
        }
        
        .file-item {
            margin: 10px 0;
            padding: 15px;
            background: #f6f8fa;
            border-radius: 8px;
            transition: all 0.3s;
        }
        
        .file-item:hover {
            background: #e1e4e8;
            transform: translateX(5px);
        }
        
        .file-item a {
            color: #0969da;
            text-decoration: none;
            font-size: 1.1em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .file-item a:hover {
            text-decoration: underline;
        }
        
        .icon {
            font-size: 1.5em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 文件索引</h1>
            <p>選擇要查看的文件</p>
        </div>
"""
    
    # 添加文件列表
    for folder, files in sorted(file_tree.items()):
        html_content += f"""
        <div class="folder">
            <div class="folder-title">
                <span class="icon">📁</span>
                <span>{folder}</span>
            </div>
            <ul class="file-list">
"""
        for file_path in sorted(files):
            file_name = file_path.stem
            html_content += f"""
                <li class="file-item">
                    <a href="{file_path}">
                        <span class="icon">📄</span>
                        <span>{file_name}</span>
                    </a>
                </li>
"""
        html_content += """
            </ul>
        </div>
"""
    
    html_content += """
    </div>
</body>
</html>
"""
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return index_path

def main():
    # 設定路徑
    root_dir = Path('root_en')
    output_dir = Path('dist/html_en')
    
    if not root_dir.exists():
        print(f"❌ 錯誤: 找不到 root_en 目錄")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("📄 MD to HTML Conversion Tool (English)")
    print("=" * 60)
    print()
    print(f"📂 Input directory: {root_dir}")
    print(f"📤 Output directory: {output_dir}")
    print(f"🌐 Static IP: {STATIC_IP}")
    print()
    
    # 清空並重建輸出目錄
    if output_dir.exists():
        print("🗑️  清空舊的輸出目錄...")
        shutil.rmtree(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    print("✅ 創建輸出目錄")
    print()
    
    # 查找所有 MD 文件
    print("🔍 搜尋 MD 文件...")
    md_files = find_all_md_files(root_dir)
    
    if not md_files:
        print(f"❌ 在 {root_dir} 中沒有找到 MD 文件")
        sys.exit(1)
    
    print(f"   找到 {len(md_files)} 個 MD 文件")
    print()
    
    # 轉換所有文件
    print("🔄 開始轉換為 HTML...")
    html_files = []
    
    for i, md_file in enumerate(md_files, 1):
        rel_path = md_file.relative_to(root_dir)
        print(f"   [{i}/{len(md_files)}] {rel_path}")
        
        html_file = convert_md_to_html(md_file, output_dir, root_dir)
        if html_file:
            html_files.append(html_file)
            print(f"        ✅ {html_file.relative_to(output_dir)}")
    
    print()
    
    # 創建索引頁面
    print("📝 創建索引頁面...")
    index_path = create_index_html(output_dir, html_files, root_dir)
    print(f"   ✅ {index_path}")
    
    print()
    print("=" * 60)
    print("✨ 轉換完成！")
    print(f"📂 輸出目錄: {output_dir}")
    print(f"📄 轉換了 {len(html_files)} 個文件")
    print(f"🌐 索引頁面: {index_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
