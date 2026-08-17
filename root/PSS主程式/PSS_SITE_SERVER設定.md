# PSSBatchJobSiteServer（Site Server 批次服務）設定說明

適用對象：Site Server（分點印表機伺服器）上的 `PSSBatchJobSiteServer` Windows 服務。

- 安裝路徑：`C:\Program Files\MobileIntelligence\PSSBatchJobSiteServer`
- 服務註冊：`PSSBatchJobSiteServer.exe install`（由 `pss_system_install.ps1` / `pss_system_install_w11.ps1` 的 `ENABLE_PSS_SITE_BATCH=Y` 流程自動執行）
- 排程機制：服務啟動後以主機名稱（hostname）查詢 `printer_server` 取得 `printer_server_id`，再由 `DynamicSchedule`（每分鐘第 50 秒）依 DB 排程設定動態掛載/卸載各 Agent Job
- 日誌：`C:\pss_log\sitebatchjob.log`（NLog，保留 60 天）

> 重要前提：Site Server 的 Windows 主機名稱必須與中央 DB `printer_server.printer_server_hostname` 一致，否則服務啟動時 `GetPrinterServerQuery` 會失敗，所有排程不會啟動。

---

## 1. 服務主程式 appsettings.json（遠端 / 本地 DB 設定）

檔案：`C:\Program Files\MobileIntelligence\PSSBatchJobSiteServer\appsettings.json`

```jsonc
{
  "ConnectionStrings": {
    "Default": "mssql",
    // 遠端（總部 Primary）DB
    "MSSQLConnection": "Data Source=primaryServer;Initial Catalog=pssdb;TrustServerCertificate=True;Persist Security Info=True;User ID=pssuser;Password=P@ssw0rdpssuser",
    // Site Server 本地 DB（SQL Express）
    "SiteMSSQLConnection": "Data Source=.\\SQLEXPRESS;Initial Catalog=pssdb;TrustServerCertificate=True;Persist Security Info=True;User ID=pssuser;Password=P@ssw0rdpssuser"
  },
  "NLogRootFolder": "C:\\pss_log\\sitebatchjob",
  "NLogMaxArchiveFiles": 14
}
```

### 1.1 遠端 DB 設定重點

| 項目                | 說明                                                                                                  |
| ------------------- | ----------------------------------------------------------------------------------------------------- |
| `MSSQLConnection` | 指向總部 Primary MSSQL（`Data Source` 改為總部 DB 主機/IP），資料庫固定 `pssdb`，帳號 `pssuser` |
| Change Tracking     | **遠端 pssdb 必須啟用**，否則 data_sync（Dotmim.Sync ChangeTracking Provider）無法運作：        |

```sql
ALTER DATABASE pssdb SET CHANGE_TRACKING = ON
(CHANGE_RETENTION = 2 DAYS, AUTO_CLEANUP = ON);
```

若有 Secondary（備援）DB，備援庫也需同樣啟用。

### 1.2 本地 DB 設定重點

| 項目                    | 說明                                                                        |
| ----------------------- | --------------------------------------------------------------------------- |
| `SiteMSSQLConnection` | 固定指向本機`.\SQLEXPRESS` 的 `pssdb`                                   |
| 建庫方式                | 由`utilities\rebuild_db` 工具執行 DDL/Trigger/備份腳本建立（見第 3.3 節） |
| 資料來源                | 本地`pssdb` 內容由 `utilities\data_sync` 從遠端下載同步（見第 3.2 節）  |

---

## 2. 動態排程 Job 與 utilities 的關係

`DynamicSchedule` 依 DB 排程設定掛載下列 Agent，各 Agent 透過 `PSSUtilityService` 中的固定路徑呼叫 utilities 執行檔：

| Agent Job                                               | 呼叫的執行檔                                        | 用途                                      |
| ------------------------------------------------------- | --------------------------------------------------- | ----------------------------------------- |
| `SyncSiteData2Agent` / `SiteSyncAgent`              | `utilities\data_sync\PSSDataSyncUtility.exe`      | 遠端 → 本地 資料下載同步                 |
| `SyncSiteDataUpload2Agent`                            | `utilities\data_sync\PSSDataSyncUtility.exe`      | 本地 → 遠端 資料上傳（統計/紀錄）        |
| `CheckConnectionAgent` / `SiteCheckConnectionAgent` | `utilities\conn_check\PSSCheckConnection.exe`     | 遠端 DB 連線健檢與 Primary/Secondary 切換 |
| （手動觸發：前端「重建資料庫」）                        | `utilities\rebuild_db\PSSSiteServerDBRebuild.exe` | 重建本地 pssdb                            |

路徑常數（`PSSUtilityService.cs`）：

```
C:\Program Files\MobileIntelligence\PSSBatchJobSiteServer\utilities\data_sync\PSSDataSyncUtility.exe
C:\Program Files\MobileIntelligence\PSSBatchJobSiteServer\utilities\conn_check\PSSCheckConnection.exe
C:\Program Files\MobileIntelligence\PSSBatchJobSiteServer\utilities\rebuild_db\PSSSiteServerDBRebuild.exe
```

---

## 3. utilities 目錄設定說明

### 3.1 conn_check（PSSCheckConnection）

檔案：`utilities\conn_check\appsettings.json`

```jsonc
{
  "LogFolder": "C:\\pss_log\\check_connection",
  "ConnectionStrings": {
    "Current": "Primary",   // 目前使用中的 DB（由程式自動改寫，勿手動亂改）
    "Primary": "Data Source=primary_db_server;Initial Catalog=pssdb;...User ID=pssuser;Password=...",
    "Secondary": "Data Source=.\\SQLEXPRESS;Initial Catalog=pssdb;...User ID=pssuser;Password=..."
  },
  "SMTP": {
    "EncryptType": "NONE",       // NONE / SSL / STARTTLS
    "Host": "192.168.50.201",
    "Port": 25,
    "Username": "noreply@mypss.com.tw",
    "Password": "P@ssw0rd",
    "From": "noreply@mypss.com.tw",
    "To": "admin@mypss.com.tw"   // 切換通知收件者
  }
}
```

設定重點：

- `Primary`：總部（遠端）DB 連線字串。
- `Secondary`：備援 DB，通常即 Site Server 本地 `.\SQLEXPRESS`。
- `Current`：目前生效的連線（`Primary` / `Secondary`），程式切換後會自動回寫此檔。

切換邏輯（每次執行時檢測 Primary / Secondary 連線）：

| Current   | Primary 可連 | Secondary 可連 | 結果                                  |
| --------- | ------------ | -------------- | ------------------------------------- |
| Primary   | O            | O/X            | 不變                                  |
| Primary   | X            | O              | **切到 Secondary** + Email 通知 |
| Primary   | X            | X              | 不變（維持 Primary）                  |
| Secondary | O            | -              | **切回 Primary** + Email 通知   |
| Secondary | X            | O/X            | 不變                                  |

切換時會同步改寫下列 IIS 站台的 `ConnectionStrings:MSSQLConnection`：

```
C:\inetpub\wwwroot\WebMonitor\appsettings.json
C:\inetpub\wwwroot\WebOxpdMVC\appsettings.json
C:\inetpub\wwwroot\WebAIPMVC\appsettings.json
C:\inetpub\wwwroot\WebUI\appsettings.json
```

> 另外 `WebAIPMVC` / `WebOxpdMVC` 的 `DBConnInfoPath` 設定會反向指到本檔（`...\utilities\conn_check\appsettings.json`）以查詢目前 DB 狀態（前端「目前 DB 狀態」功能即讀此檔的 `Current`）。

日誌：`C:\pss_log\check_connection`。

### 3.2 data_sync（PSSDataSyncUtility）

檔案：`utilities\data_sync\appsettings.json`

```jsonc
{
  "LogFolder": "C:\\pss_log\\site_sync",
  "ConnectionStrings": {
    "Default": "mssql",
    "RemoteConnection": "Data Source=remoteServer;Initial Catalog=pssdb;...",  // 遠端（總部）DB
    "LocalConnection":  "Data Source=localServer;Initial Catalog=pssdb;..."    // 本地 DB（.\SQLEXPRESS）
  },
  "SyncTables": [
    { "Name": "auth_user", "SyncDirection": "Download" },
    { "Name": "device",    "SyncDirection": "Download" }
    // ... 見下方完整清單
  ]
}
```

設定重點：

- `RemoteConnection`：改為總部 DB 主機；**遠端 pssdb 必須已啟用 CHANGE_TRACKING**（見 1.1）。
- `LocalConnection`：改為本機 `.\SQLEXPRESS`。
- `SyncTables`：要同步的資料表與方向（`Download` = 遠端→本地；`Upload` = 本地→遠端）。

預設 Download 資料表：`auth_role_user`、`auth_user`、`auth_user_whitelist`、`code_cost_role`、`code_lookup`、`code_paper`、`code_paper_category`、`code_paper_category_assoc`、`code_print_role`、`code_quota_role`、`code_watermark`、`department`、`device`、`license`、`printer`、`printer_group`、`printer_group_assoc`、`printer_server`、`printer_server_cluster`、`quota_department_balance`、`quota_device_balance`、`quota_user_balance`、`usergroup`、`user_usergroup_assoc`。

命令列參數（由 Agent 自動帶入，也可手動執行測試）：

```
PSSDataSyncUtility.exe <runType> <scopeName>
  runType : sync           增量同步（平常排程用）
            schema_update  資料表結構變更後重掛同步範圍
            reinitial      完整重新初始化同步
  scopeName : 同步範圍名稱，固定使用該站的 printer_server_id
```

日誌：`C:\pss_log\site_sync`。

### 3.3 rebuild_db（PSSSiteServerDBRebuild）

檔案：`utilities\rebuild_db\appsettings.json`

```jsonc
{
  "SqlServer": {
    "Instance": ".\\SQLEXPRESS",
    "User": "",        // 空白 → 預設 sa
    "Password": ""     // 空白 → 預設 P@ssw0rdpssdba
  },
  "SqlScripts": {
    "PSSMssqlDdlDir": "",      // 空白 → 預設 <安裝目錄>\rebuild_db\scripts
    "PSSMssqlTriggerDir": ""   // 空白 → 同 DDL 目錄
  },
  "MyLogging": {
    "LogDirectory": "C:\\pss_log\\dbrebuild",
    "LogFile": "dbrebuild.log",
    "LogLevel": "Debug"
  }
}
```

設定重點：

- 透過 `sqlcmd` 依序執行（任一腳本失敗即中止）：
  1. `pss_backup_pssdb.sql` — 先備份現有本地 pssdb
  2. `pss_mssql_ddl.sql` — 重建資料表結構
  3. `pss_mssql_trigger.sql` — 重建 Trigger
- 三支 SQL 由安裝程式（`pss_system_install*.ps1`）從安裝來源 `MsSQL` 目錄複製到 `utilities\rebuild_db\scripts`；升級 DB 結構時記得同步更新這裡的腳本。
- 主機需已安裝 `sqlcmd`（SQL Server Command Line Utilities），否則直接返回失敗。
- 重建完成後，需以 `data_sync` 執行 `reinitial` 重新灌入資料。

日誌：`C:\pss_log\dbrebuild\dbrebuild.log`。

---

## 4. 安裝/設定檢查清單

1. [ ] 主機名稱 = `printer_server.printer_server_hostname`
2. [ ] 本地已安裝 SQL Express（`.\SQLEXPRESS`）與 `sqlcmd`
3. [ ] 遠端 pssdb 已啟用 `CHANGE_TRACKING`
4. [ ] 服務 `appsettings.json`：`MSSQLConnection`（遠端）/ `SiteMSSQLConnection`（本地）
5. [ ] `utilities\conn_check\appsettings.json`：Primary / Secondary / SMTP
6. [ ] `utilities\data_sync\appsettings.json`：RemoteConnection / LocalConnection / SyncTables
7. [ ] `utilities\rebuild_db\appsettings.json` 與 `scripts\` 下三支 SQL 是否存在且版本與主 DB 一致：
   - [ ] `scripts\pss_backup_pssdb.sql`
   - [ ] `scripts\pss_mssql_ddl.sql`
   - [ ] `scripts\pss_mssql_trigger.sql`

   > **版本確認方式**：對照主 DB 目前使用的 DDL / Trigger 版本（可由主 DB 的安裝來源 `MsSQL` 目錄或版本紀錄確認），確保 Site Server 的三支腳本內容與主 DB 完全一致。若主 DB 曾升版，Site Server 的 `scripts\` 目錄也必須同步更新，否則重建資料庫後結構會與主 DB 不符，導致資料同步失敗。

8. [ ] `C:\pss_log\` 各子目錄可寫入
9. [ ] 服務已註冊並啟動（`PSSBatchJobSiteServer.exe install` → 服務 `PSSBatchJobSiteServer`）

## 5. 設定完成後的功能驗證（前端頁面測試）

完成上述所有設定後，**必須透過管理後台前端頁面逐項測試以下功能**，確認全數通過後才視為設定完成：

| # | 測試項目 | 前端操作位置 | 驗證方式 |
|---|---------|------------|--------|
| 1 | **資料重置（重建資料庫）** | 管理後台 → Site Server 管理 → 重建資料庫 | 操作完成後無錯誤訊息；確認本地 `pssdb` 結構完整（DDL + Trigger 均已執行），並查看 `C:\pss_log\dbrebuild\dbrebuild.log` 無 ERROR |
| 2 | **資料上傳** | 管理後台 → Site Server 管理 → 資料上傳 | 操作完成後無錯誤訊息；確認本地列印統計/工作記錄已上傳至主 DB，並查看 `C:\pss_log\site_sync\` 最新 LOG 無 ERROR |
| 3 | **資料同步** | 管理後台 → Site Server 管理 → 資料同步 | 操作完成後無錯誤訊息；確認主 DB 的使用者、設備、授權等資料已同步至本地，並查看 `C:\pss_log\site_sync\` 最新 LOG 無 ERROR |

> 三項功能全數測試通過，Site Server 設定才算完成。
