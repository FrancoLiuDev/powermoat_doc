#!/usr/bin/env python3
"""
Markdown 文件打包工具
將所有 MD 文件轉換成 HTML，並創建索引頁面
"""

import os
import sys
import subprocess
from pathlib import Path

def convert_md_to_html(md_file, output_dir):
    """將 MD 文件轉換成 HTML"""
    md_path = Path(md_file)
    html_filename = md_path.stem + '.html'
    html_path = output_dir / html_filename
    
    # 使用 pandoc 轉換
    cmd = [
        'pandoc',
        str(md_file),
        '-o', str(html_path),
        '--standalone',
        '--toc',
        '--toc-depth=3',
        '--metadata', f'title={md_path.stem}'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        return html_filename
    except subprocess.CalledProcessError as e:
        print(f"❌ 轉換失敗: {md_file}")
        return None

def create_index_html(html_files, output_dir, title="專案文件"):
    """創建索引頁面"""
    index_path = output_dir / 'index.html'
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #24292f;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}
        
        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .card-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }}
        
        .card {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            text-decoration: none;
            color: inherit;
            display: block;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}
        
        .card-icon {{
            font-size: 3em;
            margin-bottom: 15px;
        }}
        
        .card-title {{
            font-size: 1.4em;
            font-weight: 600;
            margin-bottom: 10px;
            color: #667eea;
        }}
        
        .card-description {{
            color: #666;
            font-size: 0.95em;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            margin-top: 50px;
            opacity: 0.8;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}
            
            .card-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 {title}</h1>
            <p>選擇您要查看的文件</p>
        </div>
        
        <div class="card-grid">
"""
    
    # 添加文件卡片
    icons = ['📄', '📋', '📝', '📑', '📰', '📊', '📈', '📉', '🗂️', '📌']
    for i, html_file in enumerate(html_files):
        icon = icons[i % len(icons)]
        name = Path(html_file).stem
        html_content += f"""
            <a href="{html_file}" class="card">
                <div class="card-icon">{icon}</div>
                <div class="card-title">{name}</div>
                <div class="card-description">點擊查看文件內容</div>
            </a>
"""
    
    html_content += """
        </div>
        
        <div class="footer">
            <p>© 2025 專案文件系統</p>
        </div>
    </div>
</body>
</html>
"""
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return index_path

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 pack_to_html.py <MD文件目錄> [輸出目錄] [標題]")
        print("範例: python3 pack_to_html.py ./test ./docs '專案文件'")
        sys.exit(1)
    
    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('./docs')
    title = sys.argv[3] if len(sys.argv) > 3 else "專案文件"
    
    # 創建輸出目錄
    output_dir.mkdir(exist_ok=True)
    
    # 查找所有 MD 文件
    md_files = list(input_dir.glob('*.md'))
    
    if not md_files:
        print(f"❌ 在 {input_dir} 中沒有找到 MD 文件")
        sys.exit(1)
    
    print(f"📚 找到 {len(md_files)} 個 MD 文件")
    print(f"📤 輸出目錄: {output_dir}")
    print()
    
    # 轉換所有 MD 文件
    html_files = []
    for md_file in md_files:
        print(f"🔄 轉換: {md_file.name}")
        html_file = convert_md_to_html(md_file, output_dir)
        if html_file:
            html_files.append(html_file)
            print(f"   ✅ 完成: {html_file}")
    
    # 創建索引頁面
    print()
    print("📝 創建索引頁面...")
    index_path = create_index_html(html_files, output_dir, title)
    print(f"✅ 索引頁面已創建: {index_path}")
    
    print()
    print("=" * 50)
    print(f"✨ 打包完成！")
    print(f"📂 輸出目錄: {output_dir}")
    print(f"🌐 請開啟: {index_path}")
    print("=" * 50)

if __name__ == "__main__":
    main()
