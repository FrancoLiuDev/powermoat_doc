#!/usr/bin/env python3
"""
Word 文件保護工具
為 Word 文件加上密碼保護或唯讀限制
"""

import sys
from pathlib import Path

def protect_word_document():
    """
    保護 Word 文件的方法說明
    """
    
    print("=" * 60)
    print("📄 Word 文件保護方法")
    print("=" * 60)
    print()
    
    print("方法 1: 轉換成 PDF（最簡單，推薦）")
    print("-" * 60)
    print("PDF 文件較難被編輯，適合分發閱讀")
    print()
    print("使用 pandoc:")
    print("  pandoc input.md -o output.pdf")
    print()
    print("使用 LibreOffice 轉換:")
    print("  libreoffice --headless --convert-to pdf output.docx")
    print()
    
    print("方法 2: Word 文件設定唯讀（需要 Microsoft Office）")
    print("-" * 60)
    print("在 Word 中:")
    print("  1. 檔案 → 資訊 → 保護文件")
    print("  2. 選擇「限制編輯」")
    print("  3. 勾選「僅允許此類型的編輯」")
    print("  4. 選擇「不允許任何變更（唯讀）」")
    print("  5. 點擊「是，開始強制保護」")
    print("  6. 設定密碼（可選）")
    print()
    
    print("方法 3: Word 文件加密（需要 Python 套件）")
    print("-" * 60)
    print("安裝套件:")
    print("  pip install python-docx msoffcrypto-tool")
    print()
    print("加密文件:")
    print("  python3 tools/protect_word.py input.docx output.docx password123")
    print()
    
    print("方法 4: 使用 LibreOffice 加密")
    print("-" * 60)
    print("在 LibreOffice Writer 中:")
    print("  1. 檔案 → 另存新檔")
    print("  2. 勾選「使用密碼儲存」")
    print("  3. 輸入密碼")
    print()
    
    print("方法 5: 轉換成唯讀的 HTML")
    print("-" * 60)
    print("HTML 文件可以閱讀但不易直接編輯原始內容")
    print("  pandoc input.md -o output.html --standalone")
    print()

def encrypt_docx(input_file, output_file, password):
    """
    使用 msoffcrypto 加密 Word 文件
    需要先安裝: pip install msoffcrypto-tool
    """
    try:
        import msoffcrypto
        
        with open(input_file, "rb") as f:
            file = msoffcrypto.OfficeFile(f)
            file.load_key(password=password)
            
            with open(output_file, "wb") as output:
                file.encrypt(password, output)
        
        print(f"✅ 文件已加密: {output_file}")
        print(f"🔐 密碼: {password}")
        
    except ImportError:
        print("❌ 錯誤: 請先安裝 msoffcrypto-tool")
        print("   執行: pip install msoffcrypto-tool")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 加密失敗: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) == 1:
        # 顯示說明
        protect_word_document()
    elif len(sys.argv) == 4:
        # 加密文件
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        password = sys.argv[3]
        
        if not Path(input_file).exists():
            print(f"❌ 錯誤: 找不到文件 {input_file}")
            sys.exit(1)
        
        encrypt_docx(input_file, output_file, password)
    else:
        print("使用方法:")
        print("  顯示說明: python3 protect_word.py")
        print("  加密文件: python3 protect_word.py input.docx output.docx password")

if __name__ == "__main__":
    main()
