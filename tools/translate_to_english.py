#!/usr/bin/env python3
"""
将root目录下的所有MD文件翻译成英文，保存到root_en目录
"""
import os
import re
from pathlib import Path
import shutil

# 翻译映射表 - 常用术语
TRANSLATION_MAP = {
    # 目录名称
    "PSS主程式": "PSS_Main_Program",
    "印表機設定及驅動": "Printer_Setup_and_Drivers",
    "使用者管理設定": "User_Management_Settings",
    "PRINTER": "PRINTER",
    "PSS_WEB_APP": "PSS_WEB_APP",
    "TROUBLE_SHOOTING": "TROUBLE_SHOOTING",
    "USECASE": "USECASE",
    "USER_MANAGEMENT": "USER_MANAGEMENT",
    "PSS": "PSS",
    
    # 文件名称
    "列印伺服器管理": "Print_Server_Management",
    "PSS列印漫游設定": "PSS_Print_Roaming_Settings",
    "PSS_漫遊列印_主程式": "PSS_Print_Roaming_Main_Program",
    "驅動程式安裝_FUJI": "Driver_Installation_FUJI",
    "驅動程式安裝_HP": "Driver_Installation_HP",
    "HP_驅動程式安裝": "HP_Driver_Installation",
    "調閱系統LOG": "System_Log_Retrieval",
    "0102_使用者無法列印": "0102_User_Cannot_Print",
    "HP_印表機綁定": "HP_Printer_Binding",
    "PSS_一般設定": "PSS_General_Settings",
    "PowerMoat管理系統維運手冊": "PowerMoat_Management_System_Operations_Manual",
    
    # 常用标题和术语
    "專案概述": "Project Overview",
    "專案功能清單": "Project Feature List",
    "一、": "1. ",
    "二、": "2. ",
    "三、": "3. ",
    "四、": "4. ",
    "五、": "5. ",
    "六、": "6. ",
    "七、": "7. ",
    "八、": "8. ",
    "九、": "9. ",
    "十、": "10. ",
    "安裝前環境準備": "Pre-installation Environment Preparation",
    "硬體需求": "Hardware Requirements",
    "軟體需求": "Software Requirements",
    "作業需求": "Operational Requirements",
    "安裝檔": "Installation Files",
    "安裝步驟": "Installation Steps",
    "驅動程式安裝": "Driver Installation",
    "驅動程式安裝環境準備": "Driver Installation Environment Preparation",
    "列印驅動程式": "Print Driver",
    "印表機": "Printer",
    "漫遊列印": "Print Roaming",
    "主程式": "Main Program",
    "伺服器": "Server",
    "管理": "Management",
    "設定": "Settings",
    "安裝": "Installation",
    "配置": "Configuration",
    "操作": "Operation",
    "需安裝": "Requires installation of",
    "或以上版本": "or higher",
    "以管理者": "As administrator",
    "登錄": "Login",
    "執行": "Execute",
    "指令": "Command",
    "點擊": "Click",
    "選取": "Select",
    "確認": "Confirm",
    "關閉": "Close",
    "開啟": "Open",
    "進行": "Proceed",
    "操作": "Operation",
    "資料夾": "Folder",
    "安裝程式": "Installer",
    "解壓縮": "Extract",
    "路徑": "Path",
    "預設": "Default",
    "系統": "System",
    "類型": "Type",
    "依續": "Proceed in sequence",
    "確認是否": "Verify if",
    "成功": "Successful",
    "新增": "Add",
    "項目": "Item",
    "需先取得": "First obtain",
    "安裝檔": "Installation file",
    "打開": "Open",
    "選擇": "Choose",
    "進入": "Enter",
    "包含": "Including",
    "後台": "Backend",
    "資料庫": "Database",
    "前端程式": "Frontend program",
    "環境": "Environment",
    "準備": "Preparation",
    "解壓": "Extract to",
    "程式": "program",
    "無": "without",
    "檔": "file",
    "及": "and",
    "取得": "obtain",
    "需": "need to",
    "先": "first",
}

def translate_text(text):
    """简单的文本翻译 - 使用翻译映射表"""
    result = text
    
    # 按照长度排序，优先匹配较长的词组
    sorted_keys = sorted(TRANSLATION_MAP.keys(), key=len, reverse=True)
    
    for chinese, english in [(k, TRANSLATION_MAP[k]) for k in sorted_keys]:
        result = result.replace(chinese, english)
    
    return result

def translate_markdown_file(input_file, output_file):
    """翻译单个Markdown文件"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 保护图片引用不被翻译
    img_pattern = r'#@img_[^\s\n]+'
    images = re.findall(img_pattern, content)
    
    # 临时替换图片引用
    for i, img in enumerate(images):
        content = content.replace(img, f"___IMAGE_PLACEHOLDER_{i}___")
    
    # 保护代码块不被翻译
    code_blocks = re.findall(r'```[^`]*```', content, re.DOTALL)
    for i, code in enumerate(code_blocks):
        content = content.replace(code, f"___CODE_PLACEHOLDER_{i}___")
    
    # 保护行内代码不被翻译
    inline_codes = re.findall(r'`[^`]+`', content)
    for i, code in enumerate(inline_codes):
        content = content.replace(code, f"___INLINE_CODE_PLACEHOLDER_{i}___")
    
    # 翻译文本
    translated = translate_text(content)
    
    # 恢复图片引用
    for i, img in enumerate(images):
        translated = translated.replace(f"___IMAGE_PLACEHOLDER_{i}___", img)
    
    # 恢复代码块
    for i, code in enumerate(code_blocks):
        translated = translated.replace(f"___CODE_PLACEHOLDER_{i}___", code)
    
    # 恢复行内代码
    for i, code in enumerate(inline_codes):
        translated = translated.replace(f"___INLINE_CODE_PLACEHOLDER_{i}___", code)
    
    # 写入输出文件
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(translated)

def translate_directory_name(name):
    """翻译目录名"""
    return TRANSLATION_MAP.get(name, name)

def main():
    root_dir = Path('root')
    output_dir = Path('root_en')
    
    if not root_dir.exists():
        print(f"❌ 错误: 找不到 {root_dir} 目录")
        return
    
    print()
    print("=" * 60)
    print("📄 MD文件英文翻译工具")
    print("=" * 60)
    print()
    print(f"📂 源目录: {root_dir}")
    print(f"📤 目标目录: {output_dir}")
    print()
    
    # 清空并重建输出目录
    if output_dir.exists():
        print("🗑️  清空旧的输出目录...")
        shutil.rmtree(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    print("✅ 创建输出目录")
    print()
    
    # 查找所有MD文件
    md_files = list(root_dir.rglob('*.md'))
    
    if not md_files:
        print(f"❌ 在 {root_dir} 中没有找到 MD 文件")
        return
    
    print(f"🔍 找到 {len(md_files)} 个 MD 文件")
    print()
    print("🔄 开始翻译...")
    
    translated_count = 0
    
    for md_file in md_files:
        # 计算相对路径
        rel_path = md_file.relative_to(root_dir)
        
        # 翻译路径中的每个部分
        path_parts = []
        for part in rel_path.parts[:-1]:  # 除了文件名的所有目录
            translated_part = translate_directory_name(part)
            path_parts.append(translated_part)
        
        # 翻译文件名
        file_stem = rel_path.stem
        translated_stem = translate_directory_name(file_stem)
        
        # 构建输出路径
        if path_parts:
            output_path = output_dir / Path(*path_parts) / f"{translated_stem}.md"
        else:
            output_path = output_dir / f"{translated_stem}.md"
        
        print(f"   翻译: {rel_path}")
        print(f"   → {output_path.relative_to(output_dir)}")
        
        # 翻译文件
        translate_markdown_file(md_file, output_path)
        translated_count += 1
        print(f"   ✅ 完成")
        print()
    
    print("=" * 60)
    print("✨ 翻译完成！")
    print(f"📂 输出目录: {output_dir}")
    print(f"📄 翻译了 {translated_count} 个文件")
    print("=" * 60)

if __name__ == "__main__":
    main()
