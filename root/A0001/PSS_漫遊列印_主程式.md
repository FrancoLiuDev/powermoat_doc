# PSS Powermoat 漫遊列印 主程式

## 專案概述

安裝漫遊列印主程式，包含後台,資料庫,前端程式。

## 一、安裝前環境準備

### 1.1 硬體需求

### 1.2 軟體需求

- 需安裝Windows Server 2022 或以上版本
- 需安裝資料庫 (Microsoft SQL Server 2022)

### 1.3 安裝檔

- PSS Powermoat ISO (PSS_v20250902.iso)

### 1.4 安裝步驟

- 以管理者(administrator)登錄 Windows Server
- PowerShell 執行 (Run As Administrator)

  - 執行PowerShell指令,開啟安裝選項視窗, 以 (D:) 為例

    ```console
    cd D:
    .\pss_system_install.ps1
    ```

  - 選取安裝 SQL Express ,及全選PSS 服務
  
    (PSSWEB,PSSBatchJob,PSSBatchJobCore,PSSOCRService,PSSMonitor,PSSSiteBatchJob)
  
    點擊確認 (執行完成需約20分鐘)

    [![image](http://218.35.171.90/html/doc/images/A0001/0001.png)](http://218.35.171.90/html/doc/images/A0001/0001.png)

  - 當出現安裝SQL解壓路徑時,只需點擊[確認]
  
    [![image](http://218.35.171.90/html/doc/images/A0001/0002.png)](http://218.35.171.90/html/doc/images/A0001/0002.png)

  - 當出現安裝SQL Server 安裝選項時

    #### 點擊 New SQL Server

    [![image](http://218.35.171.90/html/doc/images/A0001/0003.png)](http://218.35.171.90/html/doc/images/A0001/0003.png)

    [![image](http://218.35.171.90/html/doc/images/A0001/0004.png)](http://218.35.171.90/html/doc/images/A0001/0003.png)

    #### 不選取 [ ]SQL Server Replication , [ ]SQL Machine Learning

    [![image](http://218.35.171.90/html/doc/images/A0001/0005.png)](http://218.35.171.90/html/doc/images/A0001/0005.png)

    #### SQL Server 安裝完成,點擊[關閉]

    [![image](http://218.35.171.90/html/doc/images/A0001/0006.png)](http://218.35.171.90/html/doc/images/A0001/0006.png)

    #### 點擊右上方關閉SQL Server 安裝選項

    [![image](http://218.35.171.90/html/doc/images/A0001/0003.png)](http://218.35.171.90/html/doc/images/A0001/0003.png)

  - 當出現安裝 Microsoft SQL Studio 安裝選項時
  
    #### 點擊安裝 Microsoft SQL Studio

    [![image](http://218.35.171.90/html/doc/images/A0001/0007.png)](http://218.35.171.90/html/doc/images/A0001/0007.png)

    #### Microsoft SQL Studio 安裝完成,點擊[關閉]

    [![image](http://218.35.171.90/html/doc/images/A0001/0008.png)](http://218.35.171.90/html/doc/images/A0001/0008.png)

    [![image](http://218.35.171.90/html/doc/images/A0001/0009.png)](http://218.35.171.90/html/doc/images/A0001/0009.png)

    [![image](http://218.35.171.90/html/doc/images/A0001/0010.png)](http://218.35.171.90/html/doc/images/A0001/0010.png)
