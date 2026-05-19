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
import zlib
import hashlib
from urllib import request, error

# ========== 靜態參數設定 ==========
# 將所有文件中的 IP 替換為此靜態 IP
STATIC_IP = "124.218.37.90"

# ========== 排序設定 ==========
# 定義目錄顯示順序 (未列出的將會排在最後, 按字母順序)
FOLDER_ORDER = [
    "PSS主程式",
    "系統選項管理",
    "管理指南",
    "印表機設定及驅動",
    "印表機管理",
    "異常處理",
    "使用者管理設定",
    "報表",
    "列印審核",
    "稽核",
]

# 定義特定目錄下的檔案顯示順序 (未列出的將會排在最後, 按字母順序)
# 格式: "目錄名": ["檔案名1", "檔案名2"...] (不含 .html 副檔名)
FILE_ORDER = {
    "PSS主程式": [
        "PSS_漫遊列印_主程式", 
        "PSS列印漫游設定", 
        "列印伺服器管理"
    ],
    "使用者管理設定": [
        "應用系統角色說明", 
        "使用者群組觀念說明", 
        "使用者帳號維護", 
        "使用者群組維護", 
        "使用者群組異動",   
        "使用者角色異動", 
        "使用者資料匯入", 
        "員工資料維護", 
        "部門資料維護",
        "權限管控模擬情境", 
        
    ],
    "列印審核": [
        "啟用文件審核", 
        "無浮水印之印表機啟用審核", 
        "部門審核", 
        "部門審核者進行審核作業"
    ],
    "印表機管理": [
        "印表機管理維護", 
        "印表機群組維護", 
        "漫遊列印_裝置權限管控", 
        "裝置管理維護"
    ],
    "印表機設定及驅動": [
        "驅動程式安裝_FUJI", 
        "驅動程式安裝_HP"
    ],
    "報表": [
        "制式報表", 
        "報表排程"
    ],
    "稽核": [
        "白名單維護", 
        "稽核列印紀錄", 
        "稽核員帳號維護", 
        "稽核規則維護", 
        "通報事件紀錄", 
        "關鍵字維護"
    ],
    "管理指南": [
        "相關服務"
    ],
     "異常處理": [
        "無法漫游列印", 
    ],
    "系統選項管理": [
        "OCR", 
        "一般", 
        "一般排程", 
        "一般進階設定", 
        "代碼檔維護", 
        "列印伺服器", 
        "列印成本維護", 
        "列印權限維護", 
        "浮水印", 
        "系統紀錄", 
        "通知", 
        "額度角色維護"
    ]
}
# ==================================

PLANTUML_SERVER = "https://www.plantuml.com/plantuml/svg/"

DOC_CSS = """@import url('https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown.min.css');

body {
    margin: 24px auto;
    max-width: 980px;
    padding: 0 24px;
}

img {
    max-width: 100%;
    height: auto;
}

pre.plantuml {
    background: #f6f8fa;
    border-radius: 8px;
    padding: 12px;
}
"""

INDEX_CSS = """* {
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
"""


def create_shared_css(output_dir):
    """建立統一管理的 CSS 檔案。"""
    assets_dir = output_dir / 'assets'
    assets_dir.mkdir(parents=True, exist_ok=True)

    doc_css_path = assets_dir / 'doc.css'
    index_css_path = assets_dir / 'index.css'

    with open(doc_css_path, 'w', encoding='utf-8') as f:
        f.write(DOC_CSS)

    with open(index_css_path, 'w', encoding='utf-8') as f:
        f.write(INDEX_CSS)


def _plantuml_encode(data):
    """PlantUML text encoding (deflate + custom base64)."""
    def encode6bit(b):
        if b < 10:
            return chr(48 + b)
        b -= 10
        if b < 26:
            return chr(65 + b)
        b -= 26
        if b < 26:
            return chr(97 + b)
        b -= 26
        if b == 0:
            return '-'
        if b == 1:
            return '_'
        return '?'

    def append3bytes(b1, b2, b3):
        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F
        return ''.join([encode6bit(c1 & 0x3F), encode6bit(c2 & 0x3F), encode6bit(c3 & 0x3F), encode6bit(c4 & 0x3F)])

    compressed = zlib.compress(data.encode('utf-8'))
    compressed = compressed[2:-4]  # 移除 zlib header 與 checksum，符合 PlantUML deflate 規格

    encoded = []
    for i in range(0, len(compressed), 3):
        b1 = compressed[i]
        b2 = compressed[i + 1] if i + 1 < len(compressed) else 0
        b3 = compressed[i + 2] if i + 2 < len(compressed) else 0
        encoded.append(append3bytes(b1, b2, b3))

    return ''.join(encoded)


def fetch_plantuml_svg(plantuml_src, output_dir):
    """下載 PlantUML SVG 到本地 assets/plantuml 目錄。"""
    encoded = _plantuml_encode(plantuml_src)
    image_url = f"{PLANTUML_SERVER}{encoded}"
    plantuml_dir = output_dir / 'assets' / 'plantuml'
    plantuml_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{hashlib.sha256(plantuml_src.encode('utf-8')).hexdigest()[:16]}.svg"
    svg_path = plantuml_dir / file_name

    if not svg_path.exists():
        try:
            result = subprocess.run(
                ['plantuml', '-tsvg', '-pipe'],
                input=plantuml_src.encode('utf-8'),
                capture_output=True,
                check=True,
            )
            svg_path.write_bytes(result.stdout)
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            pass

    if not svg_path.exists():
        try:
            with request.urlopen(image_url, timeout=15) as response:
                svg_path.write_bytes(response.read())
        except (error.URLError, TimeoutError, OSError):
            return image_url

    return f"assets/plantuml/{file_name}"


def replace_plantuml_blocks(content, output_dir, path_prefix):
    """將 ```plantuml 程式區塊轉成可直接顯示的 SVG 圖片連結。"""
    pattern = re.compile(r'```\s*plantuml\s*\n(.*?)\n```', re.IGNORECASE | re.DOTALL)

    def repl(match):
        plantuml_src = match.group(1).strip()
        if not plantuml_src:
            return match.group(0)
        image_path = fetch_plantuml_svg(plantuml_src, output_dir)
        image_src = image_path if image_path.startswith('http') else f"{path_prefix}{image_path}"
        return f'<p><img src="{image_src}" alt="" /></p>'

    return pattern.sub(repl, content)

def convert_md_to_html(md_file, output_dir, base_dir):
    """轉換單個 MD 文件為 HTML"""
    md_path = Path(md_file)
    
    # 讀取 MD 文件內容
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 計算相對路徑
    rel_path = md_path.relative_to(base_dir)
    
    # 計算回到根目錄的相對路徑前綴
    # 例如: 根目錄檔案 -> "", 子目錄檔案 -> "../", 子子目錄 -> "../../"
    depth = len(rel_path.parts) - 1
    path_prefix = "../" * depth

    # 替換參數化的 IP 為靜態 IP
    content = content.replace('#@ip', STATIC_IP)

    # 將 PlantUML 程式區塊轉為圖片
    content = replace_plantuml_blocks(content, output_dir, path_prefix)

    # 替換 #@img_ 為相對路徑的圖片 URL
    # 例如: #@img_A0004/0011.png -> [![image](../images/A0004/0011.png)](../images/A0004/0011.png)
    def replace_image_path(match):
        img_path = match.group(1)
        full_url = f"{path_prefix}images/{img_path}"
        return f"[![image]({full_url})]({full_url})"
    
    content = re.sub(r'#@img_([^\s]+)', replace_image_path, content)
    
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
        '--css', f'{path_prefix}assets/doc.css'
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
    <link rel="stylesheet" href="assets/index.css" />
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 文件索引</h1>
            <p>選擇要查看的文件</p>
        </div>
"""
    
    # 輔助函數：取得目錄排序權重
    def get_folder_weight(item):
        folder_name = item[0]
        try:
            return (0, FOLDER_ORDER.index(folder_name), folder_name)
        except ValueError:
            return (1, 0, folder_name) # 未定義的排在最後

    # 輔助函數：取得檔案排序權重
    def get_file_weight(file_path, current_folder):
        file_stem = file_path.stem
        # 檢查是否有針對此目錄及檔案的排序設定
        if current_folder in FILE_ORDER:
            try:
                return (0, FILE_ORDER[current_folder].index(file_stem), file_stem)
            except ValueError:
                pass
        return (1, 0, file_stem) # 未定義的排在最後

    # 添加文件列表
    for folder, files in sorted(file_tree.items(), key=get_folder_weight):
        html_content += f"""
        <div class="folder">
            <div class="folder-title">
                <span class="icon">📁</span>
                <span>{folder}</span>
            </div>
            <ul class="file-list">
"""
        # 使用 lambda 包裝 current_folder
        for file_path in sorted(files, key=lambda f: get_file_weight(f, folder)):
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
    root_dir = Path('root')
    output_dir = Path('dist/html')
    
    if not root_dir.exists():
        print(f"❌ 錯誤: 找不到 root 目錄")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("📄 MD 轉 HTML 工具")
    print("=" * 60)
    print()
    print(f"📂 輸入目錄: {root_dir}")
    print(f"📤 輸出目錄: {output_dir}")
    print(f"🌐 靜態 IP: {STATIC_IP}")
    print()
    
    # 清空並重建輸出目錄
    if output_dir.exists():
        print("🗑️  清空舊的輸出目錄...")
        shutil.rmtree(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    print("✅ 創建輸出目錄")
    create_shared_css(output_dir)
    print("✅ 產生統一 CSS: assets/doc.css, assets/index.css")
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
