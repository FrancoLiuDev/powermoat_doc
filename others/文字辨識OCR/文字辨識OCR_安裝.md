# PSS 文字辨識OCR 安裝

## 專案概述

文字辨識OCR主程式，Powermoat 設定

## 一、安裝前環境準備

### 1.1 硬體需求

### 1.2 軟體需求

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

    #@img_A0001/0001.png

  - 當出現安裝SQL解壓路徑時,只需點擊[確認]
  
  #@img_A0001/0002.png

  - 當出現安裝SQL Server 安裝選項時

    #### 點擊 New SQL Server

    #@img_A0001/0003.png

    #@img_A0001/0003.png

    #### 不選取 [ ]SQL Server Replication , [ ]SQL Machine Learning

    #@img_A0001/0005.png

    #### SQL Server 安裝完成,點擊[關閉]

    #@img_A0001/0006.png

    #### 點擊右上方關閉SQL Server 安裝選項

    #@img_A0001/0003.png

  - 當出現安裝 Microsoft SQL Studio 安裝選項時
  
    #### 點擊安裝 Microsoft SQL Studio

    #@img_A0001/0007.png

    #### Microsoft SQL Studio 安裝完成,點擊[關閉]

    #@img_A0001/0008.png

    #### 出現安裝 Erlang OTP... 點選Next/安裝

    #@img_A0001/0009.png

    #### Erlang 安裝完成,點擊[關閉/Close]

    #@img_A0001/0010.png

    #### 出現安裝 Rabbit MQ Server... 點選Next/安裝

    #@img_A0001/0011.png

    #@img_A0001/0012.png

    #### Rabbit MQ Server 安裝完成,點擊[關閉/Close]

    #@img_A0001/0013.png


    #### 重新啟動電腦
