#!/usr/bin/env python3
"""
将root目录下的所有MD文件翻译成英文 - 改进版
使用更完整的翻译映射
"""
import os
import re
from pathlib import Path
import shutil

# 完整的翻译映射表
TRANSLATIONS = {
    # 标题和章节
    "列印驅動程式安裝": "Print Driver Installation",
    "驅動程式安裝環境準備": "Driver Installation Environment Preparation",
    "硬體需求": "Hardware Requirements",
    "作業需求": "Operational Requirements", 
    "軟體需求": "Software Requirements",
    "安裝步驟": "Installation Steps",
    "安裝前環境準備": "Pre-installation Environment Preparation",
    "安裝檔": "Installation Files",
    "專案概述": "Project Overview",
    "系統安裝步驟": "System Installation Steps",
    "系統啟動": "System Startup",
    "操作指南": "Operation Guide",
    
    # 常用短语
    "需先取得": "First obtain",
    "驅動程式安裝檔": "driver installation file",
    "驅動程式": "driver",
    "安裝程式": "installer",
    "點擊安裝程式": "Click the installer",
    "點擊解壓縮": "Click Extract",
    "解壓縮": "Extract",
    "解壓路徑預設": "Default extraction path",
    "關閉安裝程式": "Close the installer",
    "進行無印表機安裝": "proceed with driverless printer installation",
    "打開": "Open",
    "操作": "perform",
    "選擇系統類型": "Select system type",
    "選擇": "Select",
    "開啟": "Open",
    "資料夾": "folder",
    "依續進行安裝": "Continue with the installation",
    "選取": "Select",
    "確認是否有新增項目": "Verify if the item has been added",
    "確認安裝是否成功": "Verify if the installation was successful",
    "確認": "Confirm",
    "點擊": "Click",
    "進行": "proceed",
    "項目": "item",
    
    # 技术术语
    "印表機": "printer",
    "列印": "print",
    "漫遊列印": "print roaming",
    "伺服器": "server",
    "主程式": "main program",
    "管理": "management",
    "設定": "settings",
    "安裝": "installation",
    "配置": "configuration",
    "後台": "backend",
    "資料庫": "database",
    "前端程式": "frontend program",
    "包含": "including",
    
    # 目录名称
    "PSS主程式": "PSS_Main_Program",
    "印表機設定及驅動": "Printer_Setup_and_Drivers",
    "使用者管理設定": "User_Management_Settings",
    
    # 文件名称
    "列印伺服器管理": "Print_Server_Management",
    "PSS列印漫游設定": "PSS_Print_Roaming_Settings",
    "PSS_漫遊列印_主程式": "PSS_Print_Roaming_Main_Program",
    "驅動程式安裝_FUJI": "Driver_Installation_FUJI",
    "驅動程式安裝_HP": "Driver_Installation_HP",
    
    # 数字章节
    "一、": "## ",
    "二、": "## ",
    "三、": "## ",
    "四、": "## ",
    "五、": "## ",
    "六、": "## ",
    "七、": "## ",
    "八、": "## ",
    "九、": "## ",
    "十、": "## ",
    
    # 其他常用词
    "及": "and",
    "或": "or",
    "以": "with",
    "與": "and",
    "於": "in",
    "為": "as",
    "需": "need",
    "將": "will",
    "已": "already",
    "是": "is",
    "有": "have",
    "的": "",
    "，": ",",
    "。": ".",
}

def translate_content(text):
    """翻译文本内容"""
    # 保护特殊标记
    protected = []
    
    # 1. 保护图片引用
    def protect_image(match):
        protected.append(('img', match.group(0)))
        return f"__PROTECTED_{len(protected)-1}__"
    text = re.sub(r'#@img_[^\s\n]+', protect_image, text)
    
    # 2. 保护代码块
    def protect_code(match):
        protected.append(('code', match.group(0)))
        return f"__PROTECTED_{len(protected)-1}__"
    text = re.sub(r'```[^`]*```', protect_code, text, flags=re.DOTALL)
    
    # 3. 保护行内代码
    def protect_inline(match):
        protected.append(('inline', match.group(0)))
        return f"__PROTECTED_{len(protected)-1}__"
    text = re.sub(r'`[^`]+`', protect_inline, text)
    
    # 4. 保护路径
    def protect_path(match):
        protected.append(('path', match.group(0)))
        return f"__PROTECTED_{len(protected)-1}__"
    text = re.sub(r'[A-Z]:\\[^\s\n]+', protect_path, text)
    
    # 按长度排序翻译词条，优先匹配长词
    sorted_items = sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    
    for chinese, english in sorted_items:
        if chinese in text:
            text = text.replace(chinese, english)
    
    # 恢复保护的内容
    for i, (ptype, content) in enumerate(protected):
        text = text.replace(f"__PROTECTED_{i}__", content)
    
    return text

def translate_file(input_path, output_path):
    """翻译单个文件"""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    translated = translate_content(content)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(translated)

def translate_name(name):
    """翻译文件/目录名"""
    return TRANSLATIONS.get(name, name)

def main():
    root_dir = Path('root')
    output_dir = Path('root_en')
    
    print("\n" + "=" * 60)
    print("📄 ROOT to ROOT_EN Translation Tool")
    print("=" * 60)
    print(f"\n📂 Source: {root_dir}")
    print(f"📤 Target: {output_dir}\n")
    
    if output_dir.exists():
        print("🗑️  Removing old output directory...")
        shutil.rmtree(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    print("✅ Created output directory\n")
    
    md_files = list(root_dir.rglob('*.md'))
    print(f"🔍 Found {len(md_files)} MD files\n")
    print("🔄 Translating...\n")
    
    for md_file in md_files:
        rel_path = md_file.relative_to(root_dir)
        
        # 翻译路径
        parts = []
        for part in rel_path.parts[:-1]:
            parts.append(translate_name(part))
        
        # 翻译文件名
        stem = translate_name(rel_path.stem)
        
        # 构建输出路径
        if parts:
            output_path = output_dir / Path(*parts) / f"{stem}.md"
        else:
            output_path = output_dir / f"{stem}.md"
        
        print(f"   {rel_path}")
        print(f"   → {output_path.relative_to(output_dir)}")
        
        translate_file(md_file, output_path)
        print(f"   ✅ Done\n")
    
    print("=" * 60)
    print(f"✨ Translation complete!")
    print(f"📂 Output: {output_dir}")
    print(f"📄 Translated {len(md_files)} files")
    print("=" * 60)

if __name__ == "__main__":
    main()
