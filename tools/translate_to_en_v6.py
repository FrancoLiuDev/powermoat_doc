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
    "列印伺服器": "Print_Server",
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
    "[新增]": "[Add]",
    "[一般]": "[General]",
    "[設定]": "[Settings]",
    "[註冊]": "[Register]",
    "[取消註冊]": "[Unregister]",
    "[用量]": "[Usage]",
    "[印表機]": "[Printer]",
    
    # Escaped UI Terms (found in some markdown files)
    "\\[新增\\]": "[Add]",
    "\\[一般\\]": "[General]",
    "\\[設定\\]": "[Settings]",
    "\\[註冊\\]": "[Register]",
    "\\[取消註冊\\]": "[Unregister]",
    "\\[用量\\]": "[Usage]",
    "\\[印表機\\]": "[Printer]",
    "\\[確認\\]": "[Confirm]",
    "\\[關閉\\]": "[Close]",
    "\\[套用\\]": "[Apply]",
    "\\[Edit圖示\\]": "[Edit Icon]",
    "\\[刪除圖示\\]": "[Delete Icon]",
    "\\[新建立\\]": "[New]",
    "\\[系統管理-一般\\]": "[System Management-General]",
    "\\[基本\\]": "[Basic]",
    "\\[欄位對應\\]": "[Field Mapping]",
    "\\[排程\\]": "[Schedule]",
    "\\[額度角色維護\\]": "[Quota Role Maintenance]",
    "\\[Printer群組維護\\]": "[Printer Group Maintenance]",
    "\\[Security - Watermark\\]": "[Security - Watermark]",
    "\\[Windows Server LPR 安裝\\]": "[Windows Server LPR Installation]",
    "\\[Employee Data Import\\]": "[Employee Data Import]",
    "\\[File Import\\]": "[File Import]",
    
    # General Terms found by grep
    "部門審核者perform審核作業": "Department auditors perform audit operations",
    "無浮水印之Printer啟用審核": "Enable Audit for Non-Watermark Printers",
    "資安列印系統的伺服器設定": "Security Print System Server Settings",
    "列出未成功perform OCR 的文件紀錄": "List document records that failed to perform OCR",
    "部門": "Department",
    "備註": "Remark",
    "安全": "Security",
    "風險指數": "Risk Index",
    "星期幾": "Day of Week",
    "月（": "Month (",
    "審核作業": "Audit Operation",
    "不啟用": "Disable",
    "雙認證": "Dual Authentication",
    "單一點數": "Single Point",
    "黑白彩色點數": "BW/Color Points",
    "功能清單會啟用": "Function list will enable",
    "需重新登入": "Re-login required",
    "批次程式排程": "Batch Program Schedule",
    "資安關鍵詞": "Security Keywords",
    "比對": "comparison",
    "產生": "Generate",
    "列印伺服器設定 -- 內容": "Print Server Settings -- Content",
    "系統Support多台伺服器 PSS Server": "System supports multiple PSS Servers",
    "每台 PSS Server提供以下功能": "Each PSS Server provides the following functions",
    "收取列印、影印、掃描、傳真的影像檔案": "Receive print, copy, scan, fax image files",
    "影像檔案 OCR辨識": "Image file OCR recognition",
    "賦予一個Account具備Auditor角色": "Assign an Auditor role to an Account",
    "賦予一個Account具備白名單": "Assign a Whitelist to an Account",
    "通報等級設定與稽核規則design": "Notification Level Setting and Audit Rule Design",
    "通報等級設定": "Notification Level Setting",
    "稽核規則design": "Audit Rule Design",
    "依據關鍵字的設定加以組合規則，以制定通報等級": "Combine rules based on keyword settings to formulate notification levels",
    "關鍵字分類設定": "Keyword Category Setting",
    "新增Data": "Add Data",
    "EditData": "Edit Data",
    "刪除Data": "Delete Data",
    "User角色異動資料": "User Role Change Data",
    "User群組異動資料": "User Group Change Data",
    "User群組觀念說明": "User Group Concept Description",
    "Quota Control": "Quota Control",
    "Usable Printers": "Usable Printers",
    "Set Employee Data Import PSS System User Schedule": "Set Employee Data Import PSS System User Schedule",
    "Set File Import PSS System User Schedule": "Set File Import PSS System User Schedule",
    "Created a new employee record": "Created a new employee record",
    "Set AD relevant data": "Set AD relevant data",
    "Set AD corresponding employee data file fields": "Set AD corresponding employee data file fields",
    "Set import cycle time": "Set import cycle time",
    "由 DB 匯入員工資料檔": "Import employee data file from DB",
    "Set DB relevant data": "Set DB relevant data",
    "Set DB corresponding employee data file fields": "Set DB corresponding employee data file fields",
    "Adjust Department Quota": "Adjust Department Quota",
     
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

    # Added for Driver_Installation_HP.md
    "HP 列印驅動程式安裝": "HP Print Driver Installation",
    "需先取得 HP 驅動程式安裝檔": "Must first obtain the HP driver installation file",
    "點擊安裝程式": "Click installer",
    "點擊解壓縮": "Click unzip",
    "解壓路徑預設": "Unzip path defaults to",
    "關閉安裝程式,perform無印表機安裝": "Close the installer, perform installation without printer",
    "開啟 HP 驅動程式資料夾": "Open HP driver folder",
    "選取 v7.0.1": "Select v7.0.1",
    
    # Added for Windows_Server_LPR_Installation.md
    "## 專案概述": "## Project Overview",
    "漫游設定需要 LPD / LPR 安裝,此文件說明服務安裝步驟": "Roaming settings require LPD / LPR installation; this document explains the service installation steps.",
    "1、設定前環境準備": "1. Environment Preparation Before Setup",
    "1.1 系統需求": "1.1 System Requirements",
    "1.2 安裝步驟": "1.2 Installation Steps",
    "以管理者(administrator)登錄 Windows Server": "Log in to Windows Server as administrator",

    # Added for Print_Server_Management.md
    "PSS Powermoat 列印伺服器管理": "PSS Powermoat Print Server Management",
    "PSS列印伺服器(PSS Server) 基本設定,服務狀態及欄位定義": "PSS Print Server (PSS Server) basic settings, service status, and field definitions",
    "一、綁定前環境準備": "1. Environment Preparation Before Binding",
    "PSS Powermoat 己安裝完畢": "PSS Powermoat has been installed",
    "1.2 主要功能簡介": "1.2 Introduction to Main Functions",
    "列印伺服器維護包含以下功能用途": "Print server maintenance includes the following functional uses",
    "#### 伺服器服務狀態提示": "#### Server Service Status Prompt",
    "#### 伺服器印表機數提示/操作": "#### Server Printer Count Prompt/Operation",
    "#### 伺服器設定": "#### Server Settings",

    # Added for PSS_Print_Roaming_Main_Program.md
    "PSS Powermoat 漫遊列印 主程式": "PSS Powermoat Roaming Print Main Program",
    "安裝漫遊列印主程式，包含後台,資料庫,前端程式。": "Install roaming print main program, including backend, database, and frontend programs.",
    "一、安裝前環境準備": "1. Environment Preparation Before Installation",
    "1.2 software需求": "1.2 Software Requirements",
    "1.3 安裝檔": "1.3 Installation Files",
    "1.4 安裝步驟": "1.4 Installation Steps",
    "需安裝Windows Server 2022 或以上版本": "Need to install Windows Server 2022 or higher version",
    "需安裝資料庫": "Need to install database",
    "PowerShell 執行": "Execute via PowerShell",
    "執行PowerShell指令,開啟安裝選項視窗, 以 (D:) 為例": "Execute PowerShell command, open installation option window, taking (D:) as an example",
    "及全選PSS 服務": "and select all PSS services",
    "執行完成需約20分鐘": "Execution takes about 20 minutes",
    "當出現安裝SQL解壓路徑時,只需點擊[確認]": "When SQL unzip path appears, just click [Confirm]",
    "當出現安裝SQL Server 安裝選項時": "When SQL Server installation options appear",
    "點擊 New SQL Server": "Click New SQL Server",
    "不選取 [ ]SQL Server Replication , [ ]SQL Machine Learning": "Do not select [ ]SQL Server Replication , [ ]SQL Machine Learning",
    "SQL Server 安裝完成,點擊[關閉]": "SQL Server installation completed, click [Close]",
    "點擊右上方關閉SQL Server 安裝選項": "Click top right to close SQL Server installation options",
    "當出現安裝 Microsoft SQL Studio 安裝選項時": "When Microsoft SQL Studio installation options appear",
    "點擊安裝 Microsoft SQL Studio": "Click Install Microsoft SQL Studio",
    "Microsoft SQL Studio 安裝完成,點擊[關閉]": "Microsoft SQL Studio installation completed, click [Close]",
    "出現安裝 Erlang OTP... ClickNext/安裝": "Install Erlang OTP appears... Click Next/Install",
    "Erlang 安裝完成,點擊[關閉/Close]": "Erlang installation completed, click [Close]",
    "出現安裝 Rabbit MQ Server... ClickNext/安裝": "Install Rabbit MQ Server appears... Click Next/Install",
    "Rabbit MQ Server 安裝完成,點擊[關閉/Close]": "Rabbit MQ Server installation completed, click [Close]",
    "重新啟動電腦": "Restart computer",

    # Added for PSS_Print_Roaming_Settings.md
    "PSS Powermoat 列印漫游設定": "PSS Powermoat Print Roaming Settings",
    "PSS列印伺服器(PSS Server) 基本設定,列印漫游設定主要分為兩部份": "PSS Print Server (PSS Server) basic settings, print roaming settings are mainly divided into two parts",
    "虛擬印表機 Queue 安裝 (Roamig LPR,Roamig 兩台虛擬印表機安裝 )": "Virtual Printer Queue Installation (Installation of two virtual printers: Roaming LPR, Roaming)",
    "漫游的列印派送至實體印表機 (N 台)": "Roaming print dispatched to physical printers (N units)",
    "2、設定前環境準備": "2. Environment Preparation Before Setup",
    "實體印表機需要各列表機 IP,以及設定印表機密碼": "Physical printers require IP for each printer and a set printer password",
    "需在 Printer Server 安裝 Windows Server LPR/LPD 服務,請參考說明 [Windows Server LPR 安裝]": "Please install Windows Server LPR/LPD service on Printer Server, refer to instructions [Windows Server LPR Installation]",
    "2.1 虛擬印表機 Printer_Roaming_LPR 安裝 (使用者列印佇列)": "2.1 Virtual Printer Printer_Roaming_LPR Installation (User Print Queue)",
    "開啟 Print Management software界面": "Open Print Management software interface",
    "開啟 Print Server -> ports 項目,使用 Add Port": "Open Print Server -> ports item, use Add Port",
    "接續選擇 Add Port -> Local Port -> Port Name (nil) -> Close": "Continue to select Add Port -> Local Port -> Port Name (nil) -> Close",
    "使用者應該見到一個新的 Port (nil),如果沒有顯示請重新操作一次": "Users should see a new Port (nil); if not displayed, please operate again",
    "打開 Print Server -> Printers項目,操作 Add Printer": "Open Print Server -> Printers item, operate Add Printer",
    "選擇 Add a new printer using an existing port -> nil (Local port)": "Select Add a new printer using an existing port -> nil (Local port)",
    "選擇 \"Use an existing printer driver on the computer\"": "Select \"Use an existing printer driver on the computer\"",
    "輸入設定": "Input settings",
    "選擇建立 LPR Port (New LPR Port)": "Select Create LPR Port (New LPR Port)",
    "輸入 IP 以及 Printer Name": "Input IP and Printer Name",
    "IP: 本機 IP": "IP: Local IP",
    "Printer Name: 己建立的虛擬印表機名稱": "Printer Name: Name of the created virtual printer",
    "操作完成後檢查是否有新增一個 Port": "After operation, check if a new Port is added",
    "2.2 虛擬印表機 Printer_Roaming 安裝 (使用者列印佇列)": "2.2 Virtual Printer Printer_Roaming Installation (User Print Queue)",
    "選擇 Add a new printer using an existing port -> xxx.xxx.xxx.xxx:Printer_Roaming_LPR": "Select Add a new printer using an existing port -> xxx.xxx.xxx.xxx:Printer_Roaming_LPR",
    "選擇印表機 Driver": "Select Printer Driver",
    "輸入虛擬印表機名稱": "Input virtual printer name",
    "此印表機名稱是提供使用者漫游列印的對象": "This printer name is the target for user roaming print",
    "2.3 實體印表機 (漫游列印印表機)": "2.3 Physical Printer (Roaming Print Printer)",
    
    # Added for Print_Permission_Maintenance.md
    "設定該列印權限角色，具備列印、影印、掃描、傳真四項功能；列印、影印區分彩色與黑白權限。": "Set this print permission role to have print, copy, scan, and fax functions; print and copy distinguish between color and BW permissions.",
    "由 AD 匯入員工資料檔欄位": "import employee data fields from AD",
    "例：建立一個\"一般權限角色\" general\\_role：僅允許黑白列印、黑白影印及掃瞄功能": "Example: Create a 'General Permission Role' general_role: Only allow BW print, BW copy, and scan functions",
    "列印權限角色 -- 應用在使用者群組": "Print Permission Role -- Applied to User Groups",

    # Added for Print_Cost_Maintenance.md
    "例：建立一個一般列印成本角色 general\\_cost：一般印表機的列印成本。": "Example: Create a general print cost role general_cost: Print cost for general printers.",
    "Edit列印成本角色內容": "Edit Print Cost Role Content",
    "設定列印大小、黑白彩色對應額度的點數。": "Set points for print size, BW/Color corresponding quota.",
    "應用：裝置管理維護：設定該裝置的列印本": "Application: Device Management Maintenance: Set print cost for the device",
    "各印表機裝置可以設定不同的列印成本。": "Different print costs can be set for each printer device.",
    
    # Added for Watermark.md
    "安全-浮水印": "Security - Watermark",
    "建立一個新浮水印版型": "Create a new watermark template",
    "動態浮水印功能：浮水印可設定多個版型以對應不同人員的浮水印。": "Dynamic Watermark Function: Multiple watermark templates can be set for different personnel.",
    "浮水印版型design": "Watermark Template Design",
    "操作：可在design區中對浮水印物件直接以滑鼠拖曳、選轉、縮放。": "Operation: Directly drag, rotate, and scale watermark objects in the design area.",
    "浮水印物件": "Watermark Object",
    "提供浮水印使用的系統參數：": "System parameters provided for watermark use:",
    "帳號": "Account",
    "印表機": "Printer",
    "日期": "Date",
    "時間": "Time",
    "電腦名稱": "Computer Name",
    "擁有者(FUJFILM限定)": "Owner (FUJFILM only)",
    "浮水印樣式": "Watermark Style",
    "提供浮水印的font的變化": "Provide font variations for watermark",
    "font大小": "Font Size",
    "顏色深淺": "Color Depth",
    "外框": "Outline",
    "旋轉": "Rotate",
    "字寬": "Char Width",
    "字高": "Char Height",
    
    # Added for General_Advanced_Settings.md
    "系統內的進階設定可以透過此頁面perform調整，惟設定內容請諮詢原廠人員，以避免造成系統不穩定之情形。": "Advanced settings in the system can be adjusted through this page, but please consult original manufacturer personnel for settings to avoid system instability.",
    
    # Added for Quota_Role_Maintenance.md
    "額度類別：選擇\"點數\"方需設定此功能。": "Quota Category: This function needs to be set only when \"Points\" is selected.",
    "列印額度設定須知：列印額度設定時，列印人員及所屬的部門必須均有額度方有權列印。": "Print Quota Setting Note: When setting print quota, both the printing personnel and their department must have quota to be authorized to print.",
    "例：建立一個一般額度角色 normal\\_qouta：每月 1000點": "Example: Create a general quota role normal_quota: 1000 points per month",
    "額度角色：可以應用於使用者群組及部門。": "Quota Role: Can be applied to user groups and departments.",
    "新增後，進入Edit詳細資料": "After adding, enter Edit detailed information",
    "重置額度": "Reset Quota",
    "重置此額度角色所關聯的使用者額度及部門額度。": "Reset user quota and department quota associated with this quota role.",
    "應用 1：使用者群組 -- 該使用者群組的使用的額度": "Application 1: User Group -- Quota used by this user group",
    "應用 2：部門 -- 該部門的使用額度 (部門總用量不可超過部門額度)": "Application 2: Department -- Quota used by this department (Total department usage cannot exceed department quota)",
    "應用：使用者群組 -- 控管使用者的列印額度": "Application: User Group -- Control user print quota",
    "屬於該使用者群組的使用者套用此額度角色的列印額度。": "Users belonging to this user group apply the print quota of this quota role.",
    "應用：部門 -- 控管部門的列印額度": "Application: Department -- Control department print quota",
    "管控部門列印額度：該部門當月列印總計不可超過額度角色的列印額度。": "Control Department Print Quota: Total print usage of this department for the month cannot exceed print quota of the quota role.",

    # Added for OCR.md
    "安全-OCR": "Security - OCR",
    "設定啟動 OCR及警示通知內容。": "Set to enable OCR and alert notification content.",

    # Added for General.md
    "列印文件：列印文件的影像檔案處理方式": "Print Document: Image file processing method for print documents",
    "文件備存：強制一律備存/ 強制一律不備存/ 依印表機及使用者權限設定": "Document Backup: Force Always Backup/ Force Never Backup/ Set by Printer and User Permission",
    "備存天數：最大5位數": "Backup Days: Max 5 digits",
    "備存檔案加密": "Backup File Encryption",
    "調閱文件影像浮水印": "View Document Image Watermark",
    "調閱文件影像安全模式：不啟用/ PINCODE / 雙認證": "View Document Image Security Mode: Disable/ PINCODE/ Dual Authentication",
    "列印佇列：漫遊列印的文件保留在佇列的時間 (分鐘)": "Print Queue: Time (minutes) roaming print documents remain in queue",
    "保留時間(分)：最大3位數": "Retention Time (min): Max 3 digits",
    "額度管理：計算列印、影印、傳真文件的紙張大小的成本計價": "Quota Management: Calculate cost pricing for paper size of print, copy, and fax documents",
    "額度類別：關閉/單一點數/黑白彩色點數，額度可以控管個人每月印量。": "Quota Category: Close/Single Point/Black White Color Points, quota can control individual monthly print volume.",
    "選擇：單一點數/黑白彩色點數 功能清單會啟用 [額度角色維護]。 (需重新登入)": "Select: Single Point/Black White Color Points function list will enable [Quota Role Maintenance]. (Re-login required)",
    "密碼政策管理：制定PowerMoat 系統帳號密碼的原則政策": "Password Policy Management: Formulate policy principles for PowerMoat system account passwords",
    "最低長度(字元)：設定密碼最低長度。": "Minimum Length (characters): Set minimum password length.",
    "至少1個小寫字母：密碼至少包含1個小寫字母。": "At least 1 lowercase letter: Password must contain at least 1 lowercase letter.",
    "至少1個大寫字母：密碼至少包含1個大寫字母。": "At least 1 uppercase letter: Password must contain at least 1 uppercase letter.",
    "至少1個number：密碼至少包含1個number。": "At least 1 number: Password must contain at least 1 number.",
    "至少1個特殊字元：密碼至少包含1個特殊字元。": "At least 1 special character: Password must contain at least 1 special character.",
    "不與前N個密碼重複：密碼不可與前N個重複。": "Do not repeat with previous N passwords: Password cannot repeat with previous N.",
    "有效天數：密碼超過有效天數必須變更。": "Effective Days: Password must be changed after effective days.",
    "帳號鎖定：制定PowerMoat 系統帳號登入失敗的政策": "Account Lockout: Formulate policy for PowerMoat system account login failures",
    "啟用：是否啟用": "Enable: Whether to enable",
    "登入失敗次數：超過失敗次數，帳號將鎖定。": "Login Failure Count: Account will be locked if failure count exceeds limit.",
    "鎖定時間(分鐘)：帳號鎖定後，超過此分鐘數後將自動解除鎖定。": "Lockout Time (minutes): After account lockout, lock will be automatically released after this many minutes.",
    
    # Added for General_Schedule.md
    "針對各項批次程式的啟用或是排程，可以透過此頁面perform調整。": "Activation or scheduling of various batch programs can be adjusted through this page.",
    
    # Added for Notification.md
    "設定 SMTP 伺服器相關資訊": "Set SMTP Server Information",
    "設定系統相關事件發生時，通知管理員或特定收件者。": "Set to notify administrators or specific recipients when relevant system events occur.",
    "列印通知範本：設定列印作業的系統通知 Email範本，提供修改內容。": "Print Notification Template: Set system notification Email template for print jobs, providing content modification.",
    "掃描通知：設定掃描作業的系統通知 Email範本，提供修改內容。": "Scan Notification: Set system notification Email template for scan jobs, providing content modification.",
    "測試通知：測試 SMTP 是否設定正常。": "Test Notification: Test if SMTP setting is normal.",

    # Added for Standard_Reports.md
    "PowerMoat 提供了多份制式化報表，涵蓋了使用者、印表機、安全等面向的各式報表，匯出格式支援 CSV、EXCEL、PDF 三種格式。": "PowerMoat provides multiple standard reports covering users, printers, security, etc. Export formats support CSV, EXCEL, and PDF.",
    "Standard Reports清單及簡易說明": "Standard Reports List and Simple Description",
    "類別": "Category",
    "報表名稱": "Report Name",
    "用途說明": "Usage Description",
    "使用者列印統計": "User Print Statistics",
    "查看每位使用者的使用狀況": "View usage status of each user",
    "部門列印統計": "Department Print Statistics",
    "分析各部門的列印使用狀況": "Analyze print usage status of each department",
    "使用者群組列印統計": "User Group Print Statistics",
    "統計使用者群組的使用狀況": "Statistic user group usage status",
    "未取件列印統計": "Uncollected Print Statistics",
    "顯示列印後未取件的使用狀況": "Show usage status of uncollected prints",
    "成本中心列印統計": "Cost Center Print Statistics",
    "依成本中心統計列印的使用狀況": "Statistic print usage status by cost center",
    "印表機清單": "Printer List",
    "列出系統內所有印表機設定的資訊": "List all printer setting information in the system",
    "裝置清單": "Device List",
    "列出系統內所有裝置及設定的資訊": "List all device and setting information in the system",
    "印表機列印統計": "Printer Print Statistics",
    "統計印表機的使用情況": "Statistic printer usage",
    "裝置列印統計": "Device Print Statistics",
    "統計裝置的使用情況": "Statistic device usage",
    "裝置列印ESG統計": "Device Print ESG Statistics",
    "統計裝置的ESG使用情況": "Statistic device ESG usage",
    "HP裝置用量統計": "HP Device Usage Statistics",
    "以HP用量頁統計裝置的使用情況": "Statistic device usage by HP usage page",
    "HP裝置耗材預警報表": "HP Device Consumable Alert Report",
    "以HP耗材頁統計裝置的 耗材使用情況": "Statistic device consumable usage by HP consumable page",
    "風險指數報表": "Risk Index Report",
    "分析文件的風險指數": "Analyze document risk index",
    "無OCR結果報表": "No OCR Result Report",
    "列出未成功perform OCR 的文件紀錄": "List document records that failed to perform OCR",
    
    # Added for Report_Schedule.md
    "對於制式化報表，可依照需求制訂排程執行，並寄送給相關報表收件者。": "For standard reports, schedules can be formulated according to needs and sent to relevant report recipients.",

    # Added for Auditor_Account_Maintenance.md
    "稽核管理員可依需求賦予稽核員的角色": "Audit administrators can assign auditor roles as needed",
    "例：將 tomchan 賦予稽核員角色": "Example: Assign tomchan the auditor role",
    "修改其相關設定(ex: 稽核部門範圍)": "Modify relevant settings (ex: Audit department scope)",
    
    # Added for Audit_Rule_Maintenance.md
    "通報等級設定與稽核規則design": "Notification Level Setting and Audit Rule Design",
    "通報等級設定：設定各種不同的通報等級": "Notification Level Setting: Set various notification levels",
    "新增通報等級 (通報類別：立即、批次、只紀錄)": "Add Notification Level (Notification Category: Immediate, Batch, Log Only)",
    "通報等級設定：修改。點擊[Edit圖示] 即可進入Edit修改": "Notification Level Setting: Modify. Click [Edit Icon] to enter Edit",
    "通報等級設定：刪除。點擊[刪除圖示] 即可刪除。": "Notification Level Setting: Delete. Click [Delete Icon] to delete.",
    "稽核規則design：依據關鍵字的設定加以組合規則，以制定通報等級": "Audit Rule Design: Combine rules based on keyword settings to formulate notification levels",
    "稽核規則design：可perform新增、修改、刪除。": "Audit Rule Design: Can perform Add, Modify, Delete.",
    "條件: 依照需求設定偵測條件 (ex: 通用關鍵字(score) \>= 1)": "Condition: Set detection conditions as needed (ex: General Keyword (score) >= 1)",
    "通報等級: 當符合上述條件時，需執行哪個通報等級。": "Notification Level: Which notification level to execute when the above conditions are met.",
    "多條件規則設定範例": "Multiple Condition Rule Setting Example",
    "當文件內容有 \"機密\" 且 (文件內容 有 \"design圖\" 或是 \"電路\") 則條件成立，將觸發通報事件。": "When document content has 'Confidential' AND (document content has 'Design Diagram' OR 'Circuit'), the condition is met, triggering a notification event.",
    
    # Added for Audit_Print_Record.md
    "查詢條件：": "Query Conditions:",
    "列印開始日期及結束日期：指定查詢的日期區間": "Print Start Date and End Date: Specify query date range",
    "使用者帳號：指定某一個使用者的紀錄": "User Account: Specify records of a user",
    "指定某一個部門的紀錄": "Specify records of a department",
    "裝置名稱：指定某一台裝置的紀錄": "Device Name: Specify records of a device",
    "執行狀態：指定列印作業的執行狀態(預設為：列印完成)": "Execution Status: Specify print job execution status (Default: Print Completed)",
    "備註：指定備註的text": "Remark: Specify remark text",
    "風險指數：指定風險指數必須超過此分數": "Risk Index: Risk index must exceed this score",
    "關鍵字全文檢索：文件OCR內容包含指定的關鍵字": "Keyword Full-text Search: Document OCR content contains specified keywords",
    "篩選條件儲存": "Filter Condition Save",
    "查詢條件名稱相同則覆蓋舊有的條件。": "If query condition name is the same, overwrite old condition.",
    "篩選條件載入": "Filter Condition Load",
    "選擇條件項目後，可套用帶入套用篩選條件 或 套用並執行。": "After selecting condition item, apply to load filter condition or apply and execute.",
    "稽核調閱列印詳細紀錄": "Audit Retrieval Print Detailed Record",
    "風險資訊：顯示此份文件加總的風險指數": "Risk Info: Display total risk index of this document",
    "列印資訊：顯示此份文件的相關資訊": "Print Info: Display relevant info of this document",
    "右方為影像及OCR內容顯示區塊": "Right side is image and OCR content display block",
    "上方搜尋框可以輸入搜尋字串，若符合時將於頁碼前顯示": "Search box above can input search string; if matched, it will match before page number",
    "風險資訊區塊顯示符合關鍵字比對的結果": "Risk info block displays results matching keyword comparison",
    "OCR辨識內容顯示此影像的text內容，若符合關鍵字將以高亮度區塊顯示": "OCR recognition content displays text content of this image; if keywords match, they will be highlighted",
    "影像檔縮圖點擊後即可顯示大圖檢視。": "Image thumbnail can be clicked to display large image view.",
    "調閱影像安全模式(PINCODE)": "View Image Security Mode (PINCODE)",
    "若啟用時，調閱影像時需要輸入 PIN CODE(系統會寄送至Email信箱)後才能perform影像檢視。": "If enabled, PIN CODE (sent to email) must be entered to perform image view.",
    "調閱影像安全模式(雙認證)": "View Image Security Mode (Dual Authentication)",
    "當啟用雙認證模式時，須為每位稽核者指定第二稽核員。": "When dual authentication mode is enabled, a second auditor must be assigned for each auditor.",
    "第二稽核員可以是指定的應用系統角色(可以多個) 或是 指定的帳號(可以多個)": "Second auditor can be specified application roles (multiple) or specified accounts (multiple)",
    "調閱影像時，須登入指定的第二稽核員後方可調閱影像。": "When viewing image, must log in as specified second auditor to view image.",

    # Added for Keyword_Maintenance.md
    "關鍵字分類設定、新增關鍵字": "Keyword Category Setting, Add Keyword",
    "關鍵字分類設定：可依據不同分類設定關鍵字、與部門perform檢核。": "Keyword Category Setting: Set keywords based on different categories, perform verification with departments.",
    "關鍵字分類修改維護 [Edit圖示]": "Keyword Category Modification Maintenance [Edit Icon]",
    "新增關鍵字：關鍵字分類下可設定不同關鍵字、分數、計數規則。": "Add Keyword: Different keywords, scores, and counting rules can be set under keyword category.",
    "累計: 若設定為Y，表示風險分數 = 關鍵字出現次數 N * 分數": "Cumulative: If set to Y, Risk Score = Keyword Occurrence Count N * Score",
    "正規表示式: 若設定為 Y，表示關鍵字以正規表示式來偵測，以下為兩個案例:": "Regex: If set to Y, keyword is detected by regex; following are two examples:",
    "身分證號": "ID Number",
    "cell phone門號": "Cell Phone Number",
    "修改關鍵字：選擇要修改的關鍵字，點擊 [Edit圖示]": "Modify Keyword: Select keyword to modify, click [Edit Icon]",
    "直接performEdit。": "perform Edit directly.",

    # Added for Notification_Event_Record.md
    "達到通報等級的列印Job 進入通報事件紀錄，簡易的案件管理。": "Print Jobs reaching notification level enter notification event record, simple case management.",
    "篩選條件: 可依照事件時間、使用者帳號、部門、裝置及事件狀態來查詢。": "Filter Conditions: Query by event time, user account, department, device, and event status.",
    "事件紀錄清單可Click": "Event record list can Click",
    "查看事件詳細資料。": "View event detailed data.",
    "查看列印文件的詳細資料。": "View print document detailed data.",
    "可以多筆選取後perform批次結案作業。": "Can select multiple items to perform batch closing.",
    "通報事件詳細頁面": "Notification Event Detailed Page",
    "右上方 Job ID [1] 連結，可以快速連結到列印文件詳細頁perform調閱。": "Top right Job ID [1] link, can quickly link to print document detail page to perform retrieval.",
    "事件狀態預設為 [新建立]，稽核員可perform審核並輸入備註意見後perform結案。": "Event status defaults to [New]; auditor can perform audit and input remarks then perform closing.",

    # Added for Whitelist_Maintenance.md
    "稽核管理員可依據需求設定白名單，白名單的帳號將不perform四工備存作業。": "Audit administrators can set whitelists as needed; whitelist accounts will not perform four-factor backup operations.",
    "例：將 peterlai 賦予白名單": "Example: Assign peterlai to whitelist",
    
    # Added for User_Role_Change.md
    "事前預約使用者角色異動": "Pre-schedule User Role Change",
    "案例：Peter原本是一般使用者，於2025/08/28~2025/09/05 賦予稽核角色": "Case: Peter was originally a normal user, assigned auditor role from 2025/08/28~2025/09/05",
    
    # Added for User_Group_Concept.md
    "使用者群組管理項目": "User Group Management Items",
    "印表機功能使用權限": "Printer Function Usage Permission",
    "列印功能權限維護": "Print Function Permission Maintenance",
    "列印、影印、掃描、傳真 + 黑白/彩色": "Print, Copy, Scan, Fax + BW/Color",
    "額度控管": "Quota Control",
    "可使用的印表機": "Usable Printers",
    "使用者群組建立前置作業": "Pre-work for User Group Creation",
    "建立列印權限角色": "Create Print Permission Role",
    "建立額度角色": "Create Quota Role",
    "建立印表機群組": "Create Printer Group",
    "建立浮水印": "Create Watermark",
    
    # Added for User_Account_Maintenance.md
    "新增、Edit、刪除使用者資料": "Add, Edit, Delete User Data",
    "建立一個新的使用者帳號": "Create a new user account",
    "注意事項": "Notes",
    "Email欄位必須符合 <xxxx@xxx.xxx> 格式，必須有 \"@\"": "Email field must match <xxxx@xxx.xxx> format, must have \"@\"",
    "印表機認證時，會檢核Email欄位": "When authenticating printer, Email field will be checked",
    "當帳號因登入錯誤次數過多導致被鎖定，可以於使用者詳細頁手動perform解除鎖定狀態。": "When account is locked due to too many login failures, lock status can be manually released on user detail page.",
    
    # Added for User_Data_Import.md
    "功能說明：使用者資料2種匯入方式": "Function Description: 2 ways to import user data",
    "員工資料匯入": "Employee Data Import",
    "檔案匯入": "File Import",
    "設定員工資料匯入 PSS系統使用者排程": "Set Employee Data Import PSS System User Schedule",
    "設定檔案匯入 PSS系統使用者排程": "Set File Import PSS System User Schedule",
    "選取匯入檔案後，要按下 [套用] 按鈕，方會有效。": "After selecting import file, must press [Apply] button to be effective.",
    "計畫排程的設定": "Schedule Settings",
    "分鐘": "Minute",
    "小時": "Hour",
    "一個月中的第幾天": "Day of Month",
    "週日至週六": "Sunday to Saturday",
    "星期六": "Saturday",
    "例：每個星期六的": "Example: Every Saturday at",
    "晚上": "Night",
    "運行": "Run",
    
    # Added for Application_System_Role_Description.md
    "應用系統角色區分為以下:": "Application system roles are divided into:",
    "管理員": "Administrator",
    "具備所有系統設定的權限，除了稽核管理。": "Approves all system setting permissions, except audit management.",
    "稽核員": "Auditor",
    "具備稽核管理之相關權限(ex: 稽核調閱、關鍵字設定等)": "Approves audit management relevant permissions (ex: audit retrieval, keyword settings, etc.)",
    "使用者": "User",
    "一般使用者，可查詢個人的列印紀錄。": "General user, can query personal print records.",
    "稽核管理員": "Audit Manager",
    "管理稽核員": "Manage Auditors",
    "指定稽核範圍、雙認證規則等": "Specify audit scope, dual authentication rules, etc.",
    "支援": "Support",
    "可以使用事務性功能(ex: 報表管理)": "Can use transactional functions (ex: Report Management)",
    
    # Added for Permission_Control_Simulation_Scenario.md
    "新進員工預設不開放任何裝置列印/影印/掃描/傳真等功能，待提出申請單後再開放使用黑白/彩色權限等功能。設定步驟如下展示:": "New employees default to no functions (print/copy/scan/fax); open BW/Color permissions after application. Setup steps shown below:",
    "設定三個列印權限角色，並設定相對應的功能": "Set three print permission roles, and set corresponding functions",
    "設定三個使用者群組，並設定相對應的列印權限角色": "Set three user groups, and set corresponding print permission roles",
    "設定某位使用者的群組": "Set a user's group",
    
    # Added for Employee_Data_Maintenance.md
    "功能說明：員工資料有 3項功能": "Function Description: Employee Data has 3 functions",
    "員工資料維護：新增/修改/刪除": "Employee Data Maintenance: Add/Modify/Delete",
    "員工資料匯入：匯入來源 AD、Database，設定排程作業": "Employee Data Import: Import source AD, Database, set scheduled tasks",
    "建立一筆新的員工資料": "Create a new employee record",
    "資料來源設定": "Data Source Setting",
    "建立一筆新的AD 匯入員工資料的設定資料": "Create a new AD import employee data setting",
    "員工資料檔匯入方式 -- 有2種匯入方式": "Employee data file import method -- 2 import methods",
    "新增設定一筆由 AD 匯入員工資料檔的排程": "Add setting for a schedule to import employee data file from AD",
    "設定AD相關資料": "Set AD relevant data",
    "設定AD對應員工資料檔欄位": "Set AD corresponding employee data file fields",
    "設定匯入的週期時間": "Set import cycle time",
    "由 DB 匯入員工資料檔 (須依客戶端環境perform客製化)": "Import employee data file from DB (Needs customization based on client environment)",
    "設定DB相關資料": "Set DB relevant data",
    "設定DB對應員工資料檔欄位": "Set DB corresponding employee data file fields",
    
    # Added for User_Group_Change.md
    "事前預約使用者群組異動": "Pre-schedule User Group Change",
    "案例：Peter原本是\"預設\"使用者群組，於2025/08/28~2025/09/05 賦予 \"Color\" 使用者群組": "Case: Peter was originally \"Default\" user group, assigned \"Color\" user group from 2025/08/28~2025/09/05",
    
    # Added for User_Group_Maintenance.md
    "建立一個新的使用者群組：一般使用者群組": "Create a new user group: General User Group",
    "規劃一般使用者的相關權限": "Plan relevant permissions for general users",
    "顯示該使用者群組內的使用者帳號": "Display user accounts in this user group",
    "可以從這裡進入Edit群組內的使用者帳號": "Can enter Edit user accounts in the group from here",
    
    # Added for Department_Data_Maintenance.md
    "新增、Edit、刪除部門資料": "Add, Edit, Delete Department Data",
    "建立一個新的部門": "Create a new department",
    "業務一課": "Sales Section 1",
    "調整部門額度": "Adjust Department Quota",
    
    "PSS 系統建立一個新的裝置": "PSS system creates a new device",
    # Final Cleanup of Remaining Chinese
    "無浮水印之": "Non-Watermark ",
    "啟用審核": "Enable Audit",
    "群組維護": "Group Maintenance",
    "管理維護": "Management Maintenance",
    "資料維護": "Data Maintenance",
    "審核者": "Auditor",
    "符號": "Icon",
    "進入": "Enter",
    "額度調整": "Quota Adjustment",
    "四工備存作業": "Four-factor backup operation",
    "賴安": "Ryan",
    "客製化": "Customization",
    "須依客戶端環境": "Must depend on client environment",
    "關鍵字分類修改維護": "Keyword Category Modification Maintenance",
    "\\[編輯圖示\\]": "[Edit Icon]",
    "\\\[Edit圖示\\\]": "[Edit Icon]",
    "\\\[新增\\\]": "[Add]",
    "\\\[一般\\\]": "[General]",
    "\\\[設定\\\]": "[Settings]",
    "\\\[註冊\\\]": "[Register]",
    "\\\[取消註冊\\\]": "[Unregister]",
    "\\\[用量\\\]": "[Usage]",
    "\\\[印表機\\\]": "[Printer]",
    "月（": "Month (",
    "執行狀態": "Execution Status",
    "部們": "Department",
    "部門": "Department",
    "備註": "Remark",
    "安全": "Security",
    "風險指數": "Risk Index",
    "顯示此份文件加總的": "Display the total",
    "列印資訊": "Print Info",
    "顯示此份文件的相關資訊": "Display relevant info of this document",
    "右方為影像及OCR內容顯示區塊": "Right side is image and OCR content display block",
    "上方搜尋框可以輸入搜尋字串": "Search box above can input search string",
    "若符合時將於頁碼前顯示": "if matched, it will be displayed before page number",
    "風險資訊區塊顯示符合關鍵字比對的結果": "Risk info block displays results matching keyword comparison",
    "若符合關鍵字將以高亮度區塊顯示": "if keywords match, they will be highlighted",
    "影像檔縮圖點擊後即可顯示大圖檢視": "Click image thumbnail to display large view",
    "通報等級設定": "Notification Level Setting",
    "稽核規則": "Audit Rule",
    "設定各種不同的": "Set various different",
    "通報類別": "Notification Category",
    "立即": "Immediate",
    "批次": "Batch",
    "只紀錄": "Log Only",
    "稽核規則design": "Audit Rule Design",
    "條件": "Condition",
    "依照需求設定偵測條件": "Set detection conditions as needed",
    "通用關鍵字": "General Keyword",
    "當符合上述條件時，需執行哪個通報等級": "Which notification level to execute when the above conditions are met",
    "多條件規則設定範例": "Multiple Condition Rule Setting Example",
    "當文件內容有": "When document content has",
    "且": "AND",
    "或是": "OR",
    "則條件成立，將觸發通報事件": "the condition is met, triggering a notification event",
    "機密": "Confidential",
    "電路": "Circuit",

    # Phase 2 Final Cleanup
    "裝置Management Maintenance": "Device Management Maintenance",
    "依續perform安裝": "Follow the steps to perform installation",
    "無Printer安裝": "Installation without Printer",
    "software需求": "Software Requirements",
    "點擊確認": "Click Confirm",
    "出現安裝": "When installation of ... appears",
    "開啟 Print Management software界面": "Open Print Management software interface",
    "[Add]：建立一個新列印權限角色": "[Add]: Create a new print permission role",
    "[Add]：建立一個新列印成本角色": "[Add]: Create a new print cost role",
    "Edit列印成本角色內容": "Edit Print Cost Role Content",
    "浮水印版型design": "Watermark Template Design",
    "可在design區中對Watermark Object直接以滑鼠拖曳、選轉、縮放。": "You can drag, rotate, and scale the Watermark Object directly with the mouse in the design area.",
    "font的變化": "font variations",
    "font大小": "font size",
    "系統內的進階設定可以透過此頁面perform調整，惟設定內容請諮詢原廠人員，以避免造成系統不穩定之情形。": "Advanced system settings can be adjusted through this page; however, please consult the original manufacturer to avoid system instability.",
    "資安列印系統的伺服器設定": "Security Print System Server Settings",
    "系統支援多台伺服器": "System supports multiple servers",
    "控制多台印表機": "Control multiple printers",
    "控制印表機": "Control printer",
    "收取列印、影印、掃描、傳真的影像檔案": "Receive print, copy, scan, and fax image files",
    "影像檔案 OCR辨識、比對\"資安關鍵詞\"，產生風險指數": "Image file OCR recognition, matching 'security keywords', generating risk index",
    "列印伺服器設定 -- 內容": "Print Server Settings -- Content",
    "列出未成功perform OCR 的文件紀錄": "List document records that failed to perform OCR",
    "AuditorAccount維護": "Auditor Account Maintenance",
    "賦予一個Account具備Auditor角色": "Assign an Auditor role to an Account",
    "Notification Level Setting與Audit Ruledesig": "Notification Level Setting and Audit Rule Design",
    "點擊[Edit Icon] 即可EnterEdit修改": "Click [Edit Icon] to enter edit mode for modification",
    "點擊[Delete Icon] 即可刪除": "Click [Delete Icon] to delete",
    "可perform新增、修改、刪除": "can perform add, modify, delete",
    "(文件內容 有 \"design圖\" OR \"Circuit\")": "(Document content contains 'Design Diagram' OR 'Circuit')",
    "指定Remark的text": "Specify the text of the Remark",
    "OCR辨識內容顯示此影像的text內容": "OCR recognition content displays the text content of this image",
    "若啟用時，調閱影像時需要輸入 PIN CODE(系統會寄送至Email信箱)後才能perform影像檢視。": "If enabled, viewing images requires entering a PIN CODE (system will send it to the Email mailbox) before video viewing can be performed.",
    "可依據不同分類設定關鍵字、與Departmentperform檢核。": "Keywords can be set according to different categories and checked with Department.",
    "若設定為Y，表示風險分數 = 關鍵字出現次數 N * 分數": "If set to Y, Risk Score = Keyword Occurrence Count N * Score",
    "cell phone門號": "Cell phone number",
    "直接performEdit": "Perform edit directly",
    "事件紀錄清單可Click": "Event record list can Click",
    "可以多筆選取後performBatch結案作業": "Can perform batch closing operation after selecting multiple items",
    "右上方 Job ID [1] 連結，可以快速連結到列印文件詳細頁perform調閱": "Top right Job ID [1] link can quickly link to the detailed page to perform review",
    "Auditor可perform審核並輸入Remark意見後perform結案": "Auditor can perform audit and enter Remark comments to close the case",
    "Audit Manager可依據需求設定白名單，白名單的Account將不performFour-factor backup operation": "Audit Manager can set whitelist based on requirements; whitelist Accounts will not perform Four-factor backup operation",
    "賦予一個Account具備白名單": "Assign an Account to the whitelist",
    "User角色異動資料": "User Role Change Data",
    "[額度角色維護]": "[Quota Role Maintenance]",
    "新增、Edit、刪除User資料": "Add, Edit, Delete User Data",
    "當Account因登入錯誤次數過多導致被鎖定，可以於User詳細頁手動perform解除鎖定狀態。": "When an Account is locked due to too many login failures, it can be manually unlocked on the User details page.",
    "設定匯入來源、排程作業": "Set import source and schedule tasks",
    "可以從這裡EnterEdit群組內的UserAccount (Click\"Edit\"Icon)": "You can enter/edit User Accounts in the group from here (Click 'Edit' Icon)",
    
    # Generic Tokens (Bottom Priority)
    "裝置": "Device",
    "依續": "Sequential",
    "需求": "Requirements",
    "確認": "Confirm",
    "界面": "Interface",
    "版型": "Template",
    "變化": "Variation",
    "大小": "Size",
    "內容": "Content",
    "賦予": "Assign",
    "\\[Edit\\]": "[Edit]",
    "與": " and ",
    "有": " contains ",
    "圖": "Diagram",
    "指定": "Specify",
    "門號": "Number",
    "結案": "Close Case",
    "意見": "Comments",
    "部門": "Department",
    "檢核": "Verify",
    "檔案": "File",
    "影像": "Image",

    # Phase 3 Final Polish
    "列印伺服器": "Print Server",
    "裝置管理維護": "Device Management Maintenance",
    "依續perform安裝": "Sequentially perform installation",
    "無Printer安裝": "Installation without Printer",
    "software需求": "Software Requirements",
    "出現安裝": "When installation appears",
    "開啟 Print Management software界面": "Open Print Management software Interface",
    "浮水印版型design": "Watermark Template Design",
    "AuditorAccount維護": "Auditor Account Maintenance",
    "AuditorAccount": "Auditor Account",
    "賦予一個Account具備Auditor角色": "Assign an Auditor role to an Account",
    "Notification Level Setting與Audit Ruledesig": "Notification Level Setting and Audit Rule Design",
    "Audit Ruledesig": "Audit Rule Design",
    "點擊[Edit Icon] 即可EnterEdit修改": "Click [Edit Icon] to Enter Edit Mode",
    "design圖": "Design Diagram",
    "OCR辨識Content": "OCR Recognition Content",
    "textContent": "text content",
    "ImageSecurity": "Image Security",
    "DepartmentperformVerify": "Verify with Department",
    "RemarkComments": "Remark Comments",
    "performBatchClose Case": "perform Batch Close Case",
    "performFour-factor": "perform Four-factor",
    "DeviceManagement Maintenance": "Device Management Maintenance",
    "裝置Management Maintenance": "Device Management Maintenance",
    "Sequentialperform": "Sequentially perform",
    "Audit Ruledesign": "Audit Rule Design", 
    "EnterEdit": "Enter Edit",
    "ImageSecurity": "Image Security",
    "Image檔": "Image File",
    "Image檢視": "Image View",
    "BatchClose Case": "Batch Close Case",
    "Four-factor backup": "Four-factor backup",
    "performFour-factor backup operation": "perform Four-factor backup operation",
    "RequirePerform": "Require Perform",
    "ManualPerform": "Manual Perform",
    "Departmentperform": "Department perform",

    # Phase 4 - Nuclear Cleanup (Mapping Artifacts to Final English)
    "Sequentialperform安裝": "Sequentially perform installation",
    "裝置Management Maintenance": "Device Management Maintenance",
    "DeviceManagement Maintenance": "Device Management Maintenance",
    "perform無Printer安裝": "perform No Printer Installation",
    "無Printer安裝": "No Printer Installation",
    "When installation appears": "When installation appears",
    "When installation of ... appears Erlang OTP... ClickNext/安裝": "When installation of Erlang OTP appears... Click Next/Install",
    "When installation of ... appears Rabbit MQ Server... ClickNext/安裝": "When installation of Rabbit MQ Server appears... Click Next/Install",
    "Print Management softwareInterface": "Print Management software Interface",
    "[Add]：建立一個新列印權限角色": "[Add]: Create a new print permission role",
    "[Add]：建立一個新列印成本角色": "[Add]: Create a new print cost role",
    "Edit列印成本角色Content": "Edit Print Cost Role Content",
    "\\[Edit\\]：浮水印Templatedesign": "[Edit]: Watermark Template Design",
    "可在design區中對Watermark Object直接以滑鼠拖曳、選轉、縮放。": "You can drag, rotate, and scale the Watermark Object directly with the mouse in the design area.",
    "font的Variation": "font variations",
    "一般 (進階設定)": "General (Advanced Settings)",
    "系統內的進階設定可以透過此頁面perform調整，惟設定Content請諮詢原廠人員，以避免造成系統不穩定之情形。": "Advanced system settings can be adjusted through this page; however, please consult the original manufacturer for content settings to avoid system instability.",
    "# 列印伺服器": "# Print Server",
    "[Add]：建立一個新的額度角色": "[Add]: Create a new quota role",
    "新增後，EnterEdit詳細資料": "After adding, Enter Edit details",
    "列印文件：列印文件的Image檔案處理方式": "Print Document: Image file processing method for print documents",
    "調閱文件ImageSecurity模式": "View Document Image Security Mode",
    "Quota Role Maintenance]。 (Re-login required)": "Quota Role Maintenance]. (Re-login required)",
    "至少1個number：密碼至少包含1個number。": "At least 1 number: Password must contain at least 1 number.",
    "針對各項Batch程式的啟用OR排程，可以透過此頁面perform調整。": "For the activation OR scheduling of various Batch programs, adjustments can be performed through this page.",
    "資安列印系統的伺服器設定": "Security Print System Server Settings",
    "系統支援多台伺服器 PSS Server": "System supports multiple servers PSS Server",
    "每台 PSS Server提供以下功能": "Each PSS Server provides the following functions",
    "Printer Server - 控制多台印表機": "Printer Server - Controls multiple printers",
    "控制印表機 Printer Queue": "Controls Printer Queue",
    "收取列印、影印、掃描、傳真的影像檔案": "Receives print, copy, scan, and fax image files",
    "影像檔案 OCR辨識、比對\"資安關鍵詞\"，產生風險指數": "Image file OCR recognition, matching 'security keywords', generating risk index",
    "列印伺服器設定 -- 內容": "Print Server Settings -- Content",
    "列出未成功perform OCR 的文件紀錄": "Lists document records that failed to perform OCR",
    "AuditorAccount維護": "Auditor Account Maintenance",
    "[Add]：Assign一個Account具備Auditor角色": "[Add]: Assign an Auditor role to an Account",
    "Notification Level Setting：修改。點擊[Edit Icon] 即可EnterEdit修改": "Notification Level Setting: Modify. Click [Edit Icon] to Enter Edit Mode for modification",
    "Notification Level Setting：刪除。點擊[Delete Icon] 即可刪除。": "Notification Level Setting: Delete. Click [Delete Icon] to delete.",
    "Audit Ruledesign：可perform新增、修改、刪除。": "Audit Rule Design: Can perform add, modify, delete.",
    "(文件Content  contains  \"designDiagram\" OR \"Circuit\")": "(Document content contains 'Design Diagram' OR 'Circuit')",
    "Remark：SpecifyRemark的text": "Remark: Specify Remark text",
    "OCR辨識Content顯示此Image的textContent，if keywords match, they will be highlighted": "OCR recognition content displays the text content of this image; if keywords match, they will be highlighted",
    "若啟用時，調閱Image時需要輸入 PIN CODE(系統會寄送至Email信箱)後才能performImage檢視。": "If enabled, viewing images requires entering a PIN CODE (system will send it to the Email mailbox) before video viewing can be performed.",
    "Keyword Category Setting：可依據不同分類設定關鍵字、 and DepartmentperformVerify。": "Keyword Category Setting: Keywords can be set according to different categories and checked with Department.",
    "累計: 若設定為Y，表示風險分數 = 關鍵字出現次數 N \\* 分數": "Cumulative: If set to Y, Risk Score = Keyword Occurrence Count N * Score",
    "修改關鍵字：選擇要修改的關鍵字，點擊 [Edit Icon]** **直接performEdit。": "Modify Keyword: Select keyword to modify, click [Edit Icon]** **to perform Edit directly.",
    "事件紀錄清單可Click": "Event record list can Click",
    "View event detailed data.": "to view event detailed data.",
    "View print document detailed data.": "to view print document detailed data.",
    "可以多筆選取後performBatchClose Case作業。": "Can perform Batch Close Case operation after selecting multiple items.",
    "右上方 Job ID \\[1\\] 連結，可以快速連結到列印文件詳細頁perform調閱。": "Top right Job ID [1] link can quickly link to the print document detail page to perform review.",
    "事件狀態預設為 [New]，Auditor可perform審核並輸入RemarkComments後performClose Case。": "Event status defaults to [New], Auditor can perform audit and enter Remark Comments to Close Case.",
    "Audit Manager可依據Requirements設定白名單，白名單的Account將不performFour-factor backup operation。": "Audit Manager can set whitelist based on requirements; whitelist Accounts will not perform Four-factor backup operation.",
    "[Add]：Assign一個Account具備白名單": "[Add]: Assign an Account to the whitelist",
    "User角色異動": "User Role Change",
    "[Add]：User角色異動資料": "[Add]: User Role Change Data",
    "User群組觀念說明": "User Group Concept Description",
    "UserAccount維護": "User Account Maintenance",
    "新增、Edit、刪除User資料": "Add, Edit, Delete User Data",
    "當Account因登入錯誤次數過多導致被鎖定，可以於User詳細頁手動perform解除鎖定狀態。": "When an Account is locked due to too many login failures, it can be manually unlocked on the User details page.",
    "User資料匯入": "User Data Import",
    "員工Data Maintenance": "Employee Data Maintenance",
    "User群組異動": "User Group Change",
    "[Add]：User群組異動資料": "[Add]: User Group Change Data",
    "可以從這裡EnterEdit群組內的UserAccount (Click\"Edit\"Icon)": "You can Enter/Edit User Accounts in the group from here (Click \"Edit\" Icon)",
    "新增、Edit、刪除Department資料": "Add, Edit, Delete Department Data",
    "選擇": "Select",

    # Last ditch specific tokens
    "DeviceManagement": "Device Management",
    "AuditorAccount": "Auditor Account",
    "UserAccount": "User Account",
    "ImageSecurity": "Image Security",
    "Image檔": "Image File",
    "Image檢視": "Image View",
    "textContent": "text content",
    "designDiagram": "Design Diagram",
    "design ": "Design ",
    "EnterEdit": "Enter Edit",
    "Recall": "Review",
    "SpecifyRemark": "Specify Remark",
    "RemarkComments": "Remark Comments",
    "performBatchClose": "perform Batch Close",
    "performClose": "perform Close",
    "Four-factor": "Four-factor",
    "performFour-factor": "perform Four-factor",
    "DepartmentperformVerify": "verify with Department",
    "Wait": "Wait",
    "BatchClose": "Batch Close",
    "Close Case": "Close Case", 
    "performBatch": "perform Batch",
    "Image檔案": "Image File",

    # Phase 5 - Source Text Mapping
    "依續perform安裝": "Sequentially perform installation",
    "perform無Printer安裝": "perform No Printer Installation",
    "出現安裝": "When installation appears", # Removed colon to be safe
    "Print Management software界面": "Print Management software Interface",
    "[Add]：建立一個新列印權限角色": "[Add]: Create a new print permission role",
    "[Add]：建立一個新列印成本角色": "[Add]: Create a new print cost role",
    "Edit列印成本角色內容": "Edit Print Cost Role Content",
    "[Edit]：浮水印版型design": "[Edit]: Watermark Template Design",
    "可在design區中對Watermark Object直接以滑鼠拖曳、選轉、縮放。": "You can drag, rotate, and scale the Watermark Object directly with the mouse in the design area.",
    "font的Variation": "font variations",
    "一般 (進階設定)": "General (Advanced Settings)",
    "# 裝置管理維護": "# Device Management Maintenance", 
    "裝置管理維護": "Device Management Maintenance",
    "# 列印伺服器": "# Print Server",
    "列印伺服器": "Print Server",
    "建立一個新的額度角色": "Create a new quota role",
    "新增後，EnterEdit詳細資料": "After adding, Enter Edit details",
    "新增後，進入編輯詳細資料": "After adding, Enter Edit details",
    "列印文件：列印文件的影像檔案處理方式": "Print Document: Image file processing method for print documents",
    "調閱文件影像安全模式": "View Document Image Security Mode",
    "至少1個number：密碼至少包含1個number。": "At least 1 number: Password must contain at least 1 number.",
    "針對各項Batch程式的啟用OR排程，可以透過此頁面perform調整。": "For the activation OR scheduling of various Batch programs, adjustments can be performed through this page.",
    "資安列印系統的伺服器設定": "Security Print System Server Settings",
    "系統支援多台伺服器 PSS Server": "System supports multiple servers PSS Server",
    "每台 PSS Server提供以下功能": "Each PSS Server provides the following functions",
    "Printer Server - 控制多台印表機": "Printer Server - Controls multiple printers",
    "控制印表機 Printer Queue": "Controls Printer Queue",
    "收取列印、影印、掃描、傳真的影像檔案": "Receives print, copy, scan, and fax image files",
    "影像檔案 OCR辨識、比對\"資安關鍵詞\"，產生風險指數": "Image file OCR recognition, matching 'security keywords', generating risk index",
    "列印伺服器設定 -- 內容": "Print Server Settings -- Content",
    "列出未成功perform OCR 的文件紀錄": "Lists document records that failed to perform OCR",
    "稽核員帳號維護": "Auditor Account Maintenance",
    "AuditorAccount維護": "Auditor Account Maintenance",
    "賦予一個Account具備Auditor角色": "Assign an Auditor role to an Account",
    "Notification Level Setting與Audit Ruledesig": "Notification Level Setting and Audit Rule Design",
    "通報等級設定與稽核規則design": "Notification Level Setting and Audit Rule Design",
    "修改。點擊[Edit Icon] 即可EnterEdit修改": "Modify. Click [Edit Icon] to Enter Edit Mode for modification",
    "刪除。點擊[Delete Icon] 即可刪除。": "Delete. Click [Delete Icon] to delete.",
    "可perform新增、修改、刪除。": "Can perform add, modify, delete.",
    "(文件內容 有 \"design圖\" OR \"Circuit\")": "(Document content contains 'Design Diagram' OR 'Circuit')",
    "Remark：指定Remark的text": "Remark: Specify Remark text",
    "OCR辨識內容顯示此影像的text內容": "OCR recognition content displays the text content of this image",
    "若啟用時，調閱影像時需要輸入 PIN CODE(系統會寄送至Email信箱)後才能perform影像檢視。": "If enabled, viewing images requires entering a PIN CODE (system will send it to the Email mailbox) before video viewing can be performed.",
    "Keyword Category Setting：可依據不同分類設定關鍵字、與Departmentperform檢核。": "Keyword Category Setting: Keywords can be set according to different categories and checked with Department.",
    "累計: 若設定為Y，表示風險分數 = 關鍵字出現次數 N * 分數": "Cumulative: If set to Y, Risk Score = Keyword Occurrence Count N * Score",
    "修改關鍵字：選擇要修改的關鍵字，點擊 [Edit Icon]": "Modify Keyword: Select keyword to modify, click [Edit Icon]",
    "直接performEdit。": "to perform Edit directly.",
    "事件紀錄清單可Click": "Event record list can Click",
    "View event detailed data.": "to view event detailed data.",
    "可以多筆選取後performBatch結案作業。": "Can perform Batch Close Case operation after selecting multiple items.",
    "右上方 Job ID [1] 連結，可以快速連結到列印文件詳細頁perform調閱。": "Top right Job ID [1] link can quickly link to the print document detail page to perform review.",
    "事件狀態預設為 [New]，Auditor可perform審核並輸入Remark意見後perform結案。": "Event status defaults to [New], Auditor can perform audit and enter Remark Comments to Close Case.",
    "Audit Manager可依據需求設定白名單，白名單的Account將不performFour-factor backup operation。": "Audit Manager can set whitelist based on requirements; whitelist Accounts will not perform Four-factor backup operation.",
    "賦予一個Account具備白名單": "Assign an Account to the whitelist",
    "User角色異動": "User Role Change",
    "User群組觀念說明": "User Group Concept Description",
    "UserAccount維護": "User Account Maintenance",
    "新增、Edit、刪除User資料": "Add, Edit, Delete User Data",
    "當Account因登入錯誤次數過多導致被鎖定，可以於User詳細頁手動perform解除鎖定狀態。": "When an Account is locked due to too many login failures, it can be manually unlocked on the User details page.",
    "員工Data Maintenance": "Employee Data Maintenance",
    "User群組異動": "User Group Change",
    "可以從這裡EnterEdit群組內的UserAccount": "You can Enter/Edit User Accounts in the group from here",
    "新增、Edit、刪除Department資料": "Add, Edit, Delete Department Data",
    "選擇": "Select",
    "與": " and ",
    "有": " contains ",
    "User資料匯入": "User Data Import", 
    "員工資料維護": "Employee Data Maintenance",
    "使用者資料匯入": "User Data Import", 
    



    
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
