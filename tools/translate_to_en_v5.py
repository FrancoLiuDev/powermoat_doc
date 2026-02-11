#!/usr/bin/env python3
"""
Translate root directory MD files to English in root_en keying off a comprehensive mapping.
Version 5: Added missing translations for Driver Installation, Printer Management, etc.
"""
import os
import re
from pathlib import Path
import shutil

SOURCE_DIR = "root"
TARGET_DIR = "root_en"

# 1. Directory Mapping
DIR_MAP = {
    "系統選項管理": "System_Option_Management",
    "印表機管理": "Printer_Management",
    "列印審核": "Print_Audit",
    "報表": "Reports",
    "稽核": "Audit",
    "管理指南": "Management_Guide",
    "使用者管理設定": "User_Management_Settings",
    "PSS主程式": "PSS_Main_Program",
    "印表機設定及驅動": "Printer_Settings_and_Drivers",
}

# 2. File Mapping (filename stem -> new stem)
FILE_MAP = {
    "系統紀錄": "System_Records",
    "代碼檔維護": "Code_File_Maintenance",
    "通知": "Notification",
    "浮水印": "Watermark",
    "OCR": "OCR",
    "一般": "General",
    "一般排程": "General_Schedule",
    "一般進階設定": "General_Advanced_Settings",
    "列印成本維護": "Print_Cost_Maintenance",
    "列印權限維護": "Print_Permission_Maintenance",
    "額度角色維護": "Quota_Role_Maintenance",
    "部門審核": "Department_Audit",
    "啟用文件審核": "Enable_Document_Audit",
    "無浮水印之印表機啟用審核": "Audit_Enable_No_Watermark_Printer",
    "部門審核者進行審核作業": "Department_Auditor_Operation",
    "印表機管理維護": "Printer_Management_Maintenance",
    "印表機群組維護": "Printer_Group_Maintenance",
    "漫遊列印_裝置權限管控": "Roaming_Print_Device_Permission_Control",
    "裝置管理維護": "Device_Management_Maintenance",
    "相關服務": "Related_Services",
    "白名單維護": "Whitelist_Maintenance",
    "關鍵字維護": "Keyword_Maintenance",
    "稽核規則維護": "Audit_Rule_Maintenance",
    "通報事件紀錄": "Notification_Event_Record",
    "稽核列印紀錄": "Audit_Print_Record",
    "稽核員帳號維護": "Auditor_Account_Maintenance",
    "制式報表": "Standard_Reports",
    "報表排程": "Report_Schedule",
    "驅動程式安裝_FUJI": "Driver_Installation_FUJI",
    "驅動程式安裝_HP": "Driver_Installation_HP",
    "Windows Server LPR 安裝": "Windows_Server_LPR_Installation",
    "列印伺服器管理": "Print_Server_Management",
    "PSS列印漫游設定": "PSS_Print_Roaming_Settings",
    "PSS_漫遊列印_主程式": "PSS_Print_Roaming_Main_Program",
    "使用者帳號維護": "User_Account_Maintenance",
    "使用者群組異動": "User_Group_Change",
    "使用者群組維護": "User_Group_Maintenance",
    "使用者群組觀念說明": "User_Group_Concept",
    "使用者角色異動": "User_Role_Change",
    "使用者資料匯入": "User_Data_Import",
    "員工資料維護": "Employee_Data_Maintenance",
    "應用系統角色說明": "Application_System_Role_Description",
    "部門資料維護": "Department_Data_Maintenance",
    "權限管控模擬情境": "Permission_Control_Simulation_Scenario",
}

# 3. Content Replacement Map (Regex or simple replace)
# Order matters! Specific terms before general terms.
CONTENT_MAP = {
    # Image Captions
    r"!\[一張含有(.*?)的圖片 自動產生的描述\]": r"![Description automatically generated containing \1]",
    "一張含有": "A picture containing", # Fallback
    "的圖片 自動產生的描述": "Description automatically generated", # Fallback
    "圖片": "image",
    "文字": "text",
    "螢幕擷取畫面": "screenshot",
    "軟體": "software",
    "電腦圖示": "computer icon",
    "手機": "cell phone",
    "字型": "font",
    "圖表": "diagram",
    "設計": "design",
    "數字": "number",
    # "行": "line", # Removing single char match as it is too aggressive
    "標示": "logo",
    "多媒體軟體": "multimedia software",
    "室內": "indoor",
    "網頁": "webpage",
    
    # Common UI Terms
    "詳見：": "See: ",
    "\[新增\]": "[Add]",
    "\[一般\]": "[General]",
    "\[設定\]": "[Settings]",
    "\[註冊\]": "[Register]",
    "\[取消註冊\]": "[Unregister]",
    "\[用量\]": "[Usage]",
    "\[印表機\]": "[Printer]",
    
    # Section Headers (also used in content)
    "## 系統紀錄": "## System Records",
    "## 代碼檔維護": "## Code File Maintenance",
    "## 通知": "## Notification",
    "## 浮水印": "## Watermark",
    "## OCR": "## OCR",
    "## 一般": "## General",
    "## 一般排程": "## General Schedule",
    "## 一般進階設定": "## General Advanced Settings",
    "## 列印成本維護": "## Print Cost Maintenance",
    "## 列印權限維護": "## Print Permission Maintenance",
    "## 額度角色維護": "## Quota Role Maintenance",
    "## 部門審核": "## Department Audit",
    "## 啟用文件審核": "## Enable Document Audit",
    "## 無浮水印之印表機啟用審核": "## Audit Enable Analysis for Non-Watermark Printers",
    "## 部門審核者進行審核作業": "## Department Auditor Operation",
    "## 印表機管理維護": "## Printer Management Maintenance",
    "## 印表機群組維護": "## Printer Group Maintenance",
    "## 漫遊列印/裝置權限管控": "## Roaming Print / Device Permission Control",
    "## 裝置管理維護": "## Device Management Maintenance",
    "## 相關服務": "## Related Services",
    "## 白名單維護": "## Whitelist Maintenance",
    "## 關鍵字維護": "## Keyword Maintenance",
    "## 稽核規則維護": "## Audit Rule Maintenance",
    "## 通報事件紀錄": "## Notification Event Record",
    "## 稽核列印紀錄": "## Audit Print Record",
    "## 稽核員帳號維護": "## Auditor Account Maintenance",
    "## 制式報表": "## Standard Reports",
    "## 報表排程": "## Report Schedule",
    
    # Specific Translation for FUJI Driver
    "FUJI 列印驅動程式安裝": "FUJI Print Driver Installation",
    "一、驅動程式安裝環境準備": "1. Driver Installation Environment Preparation",
    "1.1 硬體需求": "1.1 Hardware Requirements",
    "1.2 作業需求": "1.2 Operational Requirements",
    "需先取得 Fuji 驅動程式資料夾": "Must first obtain the Fuji driver folder",
    "1.3 安裝步驟": "1.3 Installation Steps",
    "解壓縮安裝資料夾": "Unzip the installation folder",
    "打開 Print Server -> Driver項目,操作 Add Driver": "Open Print Server -> Driver item, operate Add Driver",
    "選擇系統類型": "Select system type",
    "開啟 Fuji 驅動程式資料夾": "Open Fuji driver folder",
    "依續perform安裝": "Perform installation sequentially",
    "確認是否有新增項目": "Check if there is a new item",
    "確認安裝是否成功": "Check if installation is successful",

    # Printer Management
    "印表機管理的資料會自動從 Windows控制台中的印表機帶入 (不須新增)": "Printer management data will be automatically imported from printers in Windows Control Panel (no need to add)",
    "印表機設定：": "Printer Settings:",
    "裝置: 若有對應的實體裝置，請設定。未設置表示為虛擬印表機。": "Device: If there is a corresponding physical device, please set it. Not set indicates a virtual printer.",
    "驅動程式類型: 請設定此印表機之驅動程式類型": "Driver Type: Please set the driver type for this printer",
    "L/M/H，預設執行效能為L，可依情況調整。": "L/M/H, default performance is L, adjustable according to situation.",
    "Qos類型": "QoS Type",
    "部門審核者perform審核作業": "Department auditors perform audit operations",
    "部門啟用審核及設定部門審核者": "Department Enable Audit and Set Department Auditors",
    "例：建立一個 VP 的印表機群組": "Example: Create a VP printer group",
    "漫遊列印/裝置權限管控": "Roaming Print / Device Permission Control",

    # Common Sentences / Phrases
    "設定列印費用歸屬至成本中心": "Set print cost allocation to cost center",
    "建立一個新的成本中心": "Create a new cost center",
    "應用：部門資料維護中的成本中心欄位": "Application: Cost center field in Department Data Maintenance",
    "成本中心：部門成本歸屬至成本中心，部門對應至成本中心。": "Cost Center: Department costs are allocated to cost centers; departments map to cost centers.",
    "系統中的相關異動皆記錄備查，供稽核調閱。": "Relevant system changes are recorded for future reference and audit retrieval.",
    "啟用文件審核時，此部門的人員之列印作業皆需要進行審核。": "When document audit is enabled, print jobs for personnel in this department require audit.",
    "審核者及審核者代理人須為此部門的人員。": "Auditors and deputy auditors must be personnel of this department.",
    "當有人員之列印作業需要進行審核時，系統會發送通知信件至審核者及審核者代理人。": "When a print job requires audit, the system sends a notification email to the auditor and deputy auditor.",
    "設定此印表機的列印作業 \"不啟用浮水印\" 但必須通過 \"主管審核\" 才能放行。": "Set print jobs for this printer to 'Disable Watermark' but require 'Manager Audit' for release.",
    "審核者登入系統後，於個人儀表板頁面可以查看待審核的文件清單。": "After the auditor logs in, they can view the list of pending documents on their dashboard.",
    "可進行單筆審核或勾選多筆進行批次審核。": "Single or batch audits can be performed.",
    "可點選連結進入文件詳細頁面進行文件內容查閱。": "Click the link to enter the document details page to view document content.",
    "文件審核必須輸入審核意見。": "Audit comments must be entered for document audit.",
    "可進行文件內容影像瀏覽後再進行審核作業。": "You can browse the document content image before auditing.",
    "可多台一起進行註冊作業，註冊結果參考訊息如下：": "Multiple devices can be registered together. Reference message for registration results:",
    "選擇註冊的印表機伺服器：代表此事務機相關認證、授權及工作紀錄將託管於此伺服器。": "Select the registered printer server: Authentication, authorization, and job records for this MFP will be hosted on this server.",
    "選擇欲處理的模組": "Select the module to process",
    "勾選要綁定的裝置": "Check the device to bind",
    "點選": "Click",
    "按鈕進行綁定作業": "button to perform binding",
    "按鈕進行解除綁定作業": "button to perform unbinding",
    "解除綁定": "Unbind",
    "選擇欲解除綁定的模組": "Select the module to unbind",
    "啟用管控: 啟用後，系統將監控此印表機的列印工作，進行相關作業。": "Enable Control: After enabling, the system will monitor print jobs for this printer and perform related operations.",
    "管制佇列列印: 啟用後，系統將管制列印工作，直到此工作被授權後才放行。": "Control Queue Printing: After enabling, the system will control print jobs until they are authorized for release.",
    "啟用審核: 啟用後，通過此印表機的列印工作必須經過審核通過後才放行。": "Enable Audit: After enabling, print jobs passing through this printer must be audited before release.",
    "啟用備存: 啟用後，通過此印表機的列印工作將備存處理(必須啟用管控)。": "Enable Backup: After enabling, print jobs passing through this printer will be backed up (Control must be enabled).",
    "啟用浮水印: 啟用後，通過此印表機的列印工作將套用浮水印作業。": "Enable Watermark: After enabling, print jobs passing through this printer will have watermarks applied.",
    "浮水印印表機: 若此印表機佇列無法正常執行浮水印作業時，可以設定代理的印表機佇列來執行浮水印。": "Watermark Printer: If this printer queue cannot perform watermark operations normally, a proxy printer queue can be set to execute watermarks.",
    "建立一個新的印表機群組": "Create a new printer group",
    "編輯": "Edit",
    "的印表機群組裝置基本資訊": "printer group device basic information",
    "的印表機群組包含的印表機": "printer group included printers",
    "設定漫遊列印之虛擬印表機(共用)，End User只需要安裝單一的印表機即可。": "Set up a virtual printer for roaming print (shared); End Users only need to install a single printer.",
    "將管制佇列列印啟用，通過此印表機的列印工作將暫存於伺服器上，等待使用者至任一裝置上進行授權認證取件。": "Enable control queue printing; print jobs through this printer will be temporarily stored on the server, waiting for the user to authenticate and retrieve at any device.",
    "設定實體印表機，裝置對應至實體裝置。": "Set physical printer; device mapping to physical device.",
    "管制佇列列印需取消。": "Control queue printing needs to be disabled.",
    "透過 WebUI 查看伺服器的相關服務是否正常執行中": "Check if relevant server services are running normally via WebUI",
    "於伺服器的服務查看": "Check in Server Services",
    "於伺服器的IIS查看": "Check in Server IIS",
    "列印文件影像備存批次作業服務": "Print document image backup batch service",
    "系統核心批次作業服務": "System core batch service",
    "OCR服務": "OCR service",
    "列印監控作業服務": "Print monitoring operation service",
    "App Pool of MFP AIP 服務介面": "App Pool of MFP AIP Service Interface",
    "App Pool of Print Queue API服務介面": "App Pool of Print Queue API Service Interface",
    "App Pool of MFP Oxpd 服務介面": "App Pool of MFP Oxpd Service Interface",
    "App Pool of Web管理介面": "App Pool of Web Management Interface",

    # Added for Device_Management_Maintenance.md
    "PSS 系統建立一個新的裝置": "PSS system creates a new device",
    "例：一台新進的單工印表機，建立資料": "Example: A newly added single-function printer, creating data for",
    "裝置基本資訊": "device basic information",
    "裝置類型": "Device Type",
    "事務機功能：勾選是否要啟用影印、掃描、傳真等功能。": "MFP Functions: Check whether to enable copy, scan, fax, etc.",
    "讀卡機：是否要啟用讀卡機認證，需設定讀卡機之Vender ID及 Product ID。": "Card Reader: Whether to enable card reader authentication; Vendor ID and Product ID must be set.",
    "實體印表機註冊作業：裝置管理維護": "Physical Printer Registration: Device Management Maintenance",
    "針對HP印表機綁定註冊": "Binding registration for HP printers",
    "可進行裝置之用量頁擷取": "Allows device usage page retrieval",
    "進行": "perform",
}

def translate_content(content):
    # 1. Apply Regex Replacements
    for k, v in CONTENT_MAP.items():
        if k.startswith("r") and len(k) > 1: # naive regex detection
             pass
    
    # Simple string replace descending by length of key
    sorted_keys = sorted(CONTENT_MAP.keys(), key=len, reverse=True)
    for k in sorted_keys:
        if k.startswith(r"!"):
             # handle the regex for image description
             # !\[一張含有(.*?)的圖片 自動產生的描述\]
             pattern = r"!\[一張含有(.*?)的圖片 自動產生的描述\]"
             content = re.sub(pattern, r"![Description automatically generated containing \1]", content)
        else:
             content = content.replace(k, CONTENT_MAP[k])
             
    return content

def update_links(content):
    # Update internal md links to use the new English filenames
    
    def replacer(match):
        full_match = match.group(0)
        link_text = match.group(1)
        rel_path = match.group(2)
        
        # Analyze path
        parts = rel_path.split('/')
        
        new_parts = []
        for p in parts:
            if p == "root":
                new_parts.append("root_en")
            elif p in DIR_MAP:
                new_parts.append(DIR_MAP[p])
            elif p.endswith(".md"):
                stem = p[:-3]
                if stem in FILE_MAP:
                    new_parts.append(FILE_MAP[stem] + ".md")
                else:
                    new_parts.append(p)
            else:
                new_parts.append(p)
        
        new_rel_path = "/".join(new_parts)
        return f"[{link_text}]({new_rel_path})"

    # Regex to find links. Limit to .md links
    pattern = r"\[(.*?)\]\((.*?\.md)\)"
    content = re.sub(pattern, replacer, content)
    return content

def main():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if not file.endswith(".md"):
                continue
                
            source_path = Path(root) / file
            
            # Determine relative path from SOURCE_DIR
            rel_path = source_path.relative_to(SOURCE_DIR)
            
            # Construct target path
            target_parts = []
            for part in rel_path.parts[:-1]: # Directories
                target_parts.append(DIR_MAP.get(part, part))
            
            file_stem = rel_path.stem
            new_stem = FILE_MAP.get(file_stem, file_stem)
            target_parts.append(new_stem + ".md")
            
            target_rel_path = Path(*target_parts)
            target_path = Path(TARGET_DIR) / target_rel_path
            
            # Create directories
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Read, Translate, Write
            content = source_path.read_text(encoding='utf-8')
            content = translate_content(content)
            content = update_links(content)
            
            # Also translate the Title line if it matches file stem (H1 header)
            if file_stem in FILE_MAP:
                old_h1 = f"# {file_stem}"
                new_h1 = f"# {FILE_MAP[file_stem]}"
                content = content.replace(old_h1, new_h1)
            
            target_path.write_text(content, encoding='utf-8')
            print(f"Translated: {source_path} -> {target_path}")

if __name__ == "__main__":
    main()
