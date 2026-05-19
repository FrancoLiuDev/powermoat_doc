#!/usr/bin/env python3
"""
Markdown 文件打包工具
將所有 MD 文件轉換成 HTML，並創建索引頁面
"""

import os
import sys
import subprocess
import tempfile
import hashlib
import zlib
import re
from pathlib import Path
from urllib import request, error

PLANTUML_SERVER = "https://www.plantuml.com/plantuml/svg/"


def _plantuml_encode(data):
    def encode6bit(b):
        if b < 10: return chr(48 + b)
        b -= 10
        if b < 26: return chr(65 + b)
        b -= 26
        if b < 26: return chr(97 + b)
        b -= 26
        if b == 0: return '-'
        if b == 1: return '_'
        return '?'

    def append3bytes(b1, b2, b3):
        c1, c2 = b1 >> 2, ((b1 & 0x3) << 4) | (b2 >> 4)
        c3, c4 = ((b2 & 0xF) << 2) | (b3 >> 6), b3 & 0x3F
        return ''.join([encode6bit(x & 0x3F) for x in [c1, c2, c3, c4]])

    compressed = zlib.compress(data.encode('utf-8'))[2:-4]
    encoded = []
    for i in range(0, len(compressed), 3):
        b1 = compressed[i]
        b2 = compressed[i + 1] if i + 1 < len(compressed) else 0
        b3 = compressed[i + 2] if i + 2 < len(compressed) else 0
        encoded.append(append3bytes(b1, b2, b3))
    return ''.join(encoded)


def fetch_plantuml_svg(plantuml_src, output_dir):
    """使用本機 plantuml 或線上服務產生 SVG，存到 assets/plantuml。"""
    plantuml_dir = output_dir / 'assets' / 'plantuml'
    plantuml_dir.mkdir(parents=True, exist_ok=True)
    file_name = f"{hashlib.sha256(plantuml_src.encode('utf-8')).hexdigest()[:16]}.svg"
    svg_path = plantuml_dir / file_name

    if not svg_path.exists():
        try:
            result = subprocess.run(
                ['plantuml', '-tsvg', '-pipe'],
                input=plantuml_src.encode('utf-8'),
                capture_output=True, check=True,
            )
            svg_path.write_bytes(result.stdout)
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            pass

    if not svg_path.exists():
        try:
            url = f"{PLANTUML_SERVER}{_plantuml_encode(plantuml_src)}"
            with request.urlopen(url, timeout=15) as resp:
                svg_path.write_bytes(resp.read())
        except (error.URLError, TimeoutError, OSError):
            return f"{PLANTUML_SERVER}{_plantuml_encode(plantuml_src)}"

    return f"assets/plantuml/{file_name}"


def replace_plantuml_blocks(content, output_dir):
    """將 ```plantuml 區塊替換成 SVG 圖片，並移除原始語法。"""
    pattern = re.compile(r'```\s*plantuml\s*\n(.*?)\n```', re.IGNORECASE | re.DOTALL)

    def repl(match):
        src = match.group(1).strip()
        if not src:
            return ''
        image_path = fetch_plantuml_svg(src, output_dir)
        image_src = image_path if image_path.startswith('http') else f"../{image_path}"
        return f'<p><img src="{image_src}" alt="" /></p>'

    return pattern.sub(repl, content)


def convert_md_to_html(md_file, output_dir):
    """將 MD 文件轉換成 HTML"""
    md_path = Path(md_file)
    html_filename = md_path.stem + '.html'
    html_path = output_dir / html_filename

    # 讀取並前處理 MD 內容
    content = md_path.read_text(encoding='utf-8')
    content = replace_plantuml_blocks(content, output_dir)

    # 寫入臨時 MD 檔
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8')
    tmp.write(content)
    tmp.close()

    # 使用 pandoc 轉換
    cmd = [
        'pandoc',
        tmp.name,
        '-o', str(html_path),
        '--standalone',
        '--toc',
        '--toc-depth=3',
        '--metadata', f'title={md_path.stem}'
    ]

    try:
        subprocess.run(cmd, check=True)
        return html_filename
    except subprocess.CalledProcessError:
        print(f"❌ 轉換失敗: {md_file}")
        return None
    finally:
        Path(tmp.name).unlink(missing_ok=True)

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
