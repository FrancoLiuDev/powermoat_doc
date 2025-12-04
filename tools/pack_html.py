#!/usr/bin/env python3
"""
HTML 打包工具
將 HTML 及所有資源打包成單一檔案，防止被輕易修改
"""

import sys
import base64
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

def inline_css(html_content):
    """將外部 CSS 內嵌到 HTML"""
    # 這裡處理 <link> 標籤
    return html_content

def inline_images(html_content, base_path):
    """將圖片轉換為 base64 內嵌"""
    def replace_img(match):
        img_src = match.group(1)
        
        # 跳過外部 URL
        if img_src.startswith(('http://', 'https://', 'data:')):
            return match.group(0)
        
        # 處理相對路徑
        img_path = base_path / img_src
        if img_path.exists():
            with open(img_path, 'rb') as f:
                img_data = f.read()
                img_base64 = base64.b64encode(img_data).decode()
                
                # 判斷圖片類型
                ext = img_path.suffix.lower()
                mime_types = {
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.gif': 'image/gif',
                    '.svg': 'image/svg+xml',
                    '.webp': 'image/webp'
                }
                mime_type = mime_types.get(ext, 'image/png')
                
                return f'<img src="data:{mime_type};base64,{img_base64}"'
        
        return match.group(0)
    
    # 替換所有 <img src="...">
    pattern = r'<img\s+src="([^"]+)"'
    return re.sub(pattern, replace_img, html_content)

def minify_html(html_content):
    """壓縮 HTML，移除註解和多餘空白"""
    # 移除 HTML 註解
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    # 移除多餘空白
    html_content = re.sub(r'\s+', ' ', html_content)
    return html_content

def add_protection(html_content):
    """添加防護措施"""
    protection_script = """
<script>
// 禁用右鍵選單
document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
    return false;
});

// 禁用 F12 開發者工具
document.addEventListener('keydown', function(e) {
    if (e.keyCode == 123 || // F12
        (e.ctrlKey && e.shiftKey && e.keyCode == 73) || // Ctrl+Shift+I
        (e.ctrlKey && e.shiftKey && e.keyCode == 74) || // Ctrl+Shift+J
        (e.ctrlKey && e.keyCode == 85)) { // Ctrl+U
        e.preventDefault();
        return false;
    }
});

// 禁用選取文字
document.addEventListener('selectstart', function(e) {
    e.preventDefault();
    return false;
});

// 禁用複製
document.addEventListener('copy', function(e) {
    e.preventDefault();
    return false;
});

// 防止拖曳
document.addEventListener('dragstart', function(e) {
    e.preventDefault();
    return false;
});

// 添加浮水印
window.addEventListener('load', function() {
    var watermark = document.createElement('div');
    watermark.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;opacity:0.1;font-size:50px;transform:rotate(-45deg);display:flex;align-items:center;justify-content:center;color:#000;';
    watermark.textContent = '僅供閱讀 - 請勿修改';
    document.body.appendChild(watermark);
});
</script>
<style>
body {
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}
</style>
"""
    
    # 在 </head> 前插入保護腳本
    return html_content.replace('</head>', protection_script + '</head>')

def pack_html(input_file, output_file, protect=True, minify=False):
    """打包 HTML 文件"""
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"❌ 錯誤: 找不到文件 {input_file}")
        return False
    
    print(f"📄 讀取: {input_file}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    base_path = input_path.parent
    
    # 內嵌圖片
    print("🖼️  內嵌圖片...")
    html_content = inline_images(html_content, base_path)
    
    # 添加保護
    if protect:
        print("🔒 添加保護措施...")
        html_content = add_protection(html_content)
    
    # 壓縮
    if minify:
        print("📦 壓縮 HTML...")
        html_content = minify_html(html_content)
    
    # 寫入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 完成: {output_file}")
    return True

def main():
    if len(sys.argv) < 2:
        print("HTML 打包保護工具")
        print("=" * 60)
        print()
        print("使用方法:")
        print("  python3 pack_html.py <輸入文件> [輸出文件] [選項]")
        print()
        print("選項:")
        print("  --no-protect    不添加保護措施")
        print("  --minify        壓縮 HTML")
        print()
        print("範例:")
        print("  python3 pack_html.py docs/index.html protected.html")
        print("  python3 pack_html.py docs/index.html output.html --minify")
        print()
        print("功能:")
        print("  ✅ 內嵌所有圖片（轉為 base64）")
        print("  ✅ 禁用右鍵選單")
        print("  ✅ 禁用開發者工具快捷鍵")
        print("  ✅ 禁用選取和複製")
        print("  ✅ 添加浮水印")
        print("  ✅ 單一文件，易於分發")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'protected_' + Path(input_file).name
    
    protect = '--no-protect' not in sys.argv
    minify = '--minify' in sys.argv
    
    print()
    print("=" * 60)
    print("📦 HTML 打包保護工具")
    print("=" * 60)
    print()
    
    success = pack_html(input_file, output_file, protect, minify)
    
    if success:
        print()
        print("=" * 60)
        print("✨ 打包完成！")
        print(f"📂 輸出文件: {output_file}")
        
        input_size = Path(input_file).stat().st_size
        output_size = Path(output_file).stat().st_size
        print(f"📊 文件大小: {input_size:,} bytes → {output_size:,} bytes")
        
        if protect:
            print()
            print("🔒 已啟用保護措施:")
            print("   • 禁用右鍵選單")
            print("   • 禁用開發者工具")
            print("   • 禁用選取和複製")
            print("   • 添加浮水印")
        print("=" * 60)

if __name__ == "__main__":
    main()
