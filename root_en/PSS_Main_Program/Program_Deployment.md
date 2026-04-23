# Program Deployment
## PSS Powermoat Program Deployment Instructions

### 1. IIS \inetpub\wwwroot Deployment Instructions
1.1 WebUI (`\inetpub\wwwroot\WebUI`)
1.2 WebAIPMVC (`\inetpub\wwwroot\WebAIPMVC`)
1.3 WebMonitor (`\inetpub\wwwroot\WebMonitor`)
1.4 WebOxpdMVC (`\inetpub\wwwroot\WebOxpdMVC`)

### 2. Powermoat System Service Deployment Instructions \Program Files\MobileIntelligence
2.1 PSSBatchJobServer (`\Program Files\MobileIntelligence\PSSBatchJobServer`)
2.2 PSSBatchJobServerCore (`\Program Files\MobileIntelligence\PSSBatchJobServerCore`)
2.3 PSSMonitor (`\Program Files\MobileIntelligence\PSSMonitor`)
2.4 PSSOCRProcessSvc (`\Program Files\MobileIntelligence\PSSOCRProcessSvc`)
2.5 PSSOCRService (`\Program Files\MobileIntelligence\PSSOCRService`)

### 3. Powermoat OCR Deployment Instructions \inetpub\ocr
3.1 OCR (`\inetpub\ocr`)

---

## PSS Powermoat Program Deployment Instructions

### 1. IIS \inetpub\wwwroot Deployment Instructions

#### 1.1 WebUI (`\inetpub\wwwroot\WebUI`)
- **Configuration Summary:** `appsettings.json`
- **Database Settings:** `ConnectionStrings` -> `MSSQLConnection` (Default is localhost)
- **Powermoat AD Login Domain:** `AdDomain`

#### 1.2 WebAIPMVC (`\inetpub\wwwroot\WebAIPMVC`)
- **Configuration Summary:** `appsettings.json`
- **Database Settings:** `ConnectionStrings` -> `MSSQLConnection` (Default is localhost)

#### 1.3 WebMonitor (`\inetpub\wwwroot\WebMonitor`)
- **Database Settings:** `ConnectionStrings` -> `MSSQLConnection` (Default is localhost)

#### 1.4 WebOxpdMVC (`\inetpub\wwwroot\WebOxpdMVC`)
- **Configuration Summary:** `appsettings.json`
- **Database Settings:** `ConnectionStrings` -> `MSSQLConnection` (Default is localhost)

### 2. Powermoat System Service Deployment Instructions \Program Files\MobileIntelligence

#### 2.1 PSSBatchJobServer (`\Program Files\MobileIntelligence\PSSBatchJobServer`)
- **Configuration Summary:** `appsettings.json`
- **Database Settings:** `ConnectionStrings` -> `MSSQLConnection` (Default is localhost)

#### 2.2 PSSBatchJobServerCore (`\Program Files\MobileIntelligence\PSSBatchJobServerCore`)
- **Configuration Summary:** `appsettings.json`
- **Database Settings:** `ConnectionStrings` -> `MSSQLConnection` (Default is localhost)

#### 2.3 PSSMonitor (`\Program Files\MobileIntelligence\PSSMonitor`)
- **Configuration Summary:** `appsettings.json`
- **Database Settings:** `ConnectionStrings` -> `MSSQLConnection` (Default is localhost)

#### 2.4 PSSOCRProcessSvc (`\Program Files\MobileIntelligence\PSSOCRProcessSvc`)
- **Configuration Summary:** `appsettings.json`
- **Log Path:** `LogFolder`
- **OCR Service Program Path:** `OcrPath`
- **OCR Service Program File Path:** `WorkDirectory`
- **OCR Service Error Log:** `ErrorDirectory`

#### 2.5 PSSOCRService (`\Program Files\MobileIntelligence\PSSOCRService`)
- **Database Settings:** `ConnectionStrings` -> `MSSQLConnection` (Default is localhost)

### 3. Powermoat OCR Deployment Instructions \inetpub\ocr

#### 3.1 OCR (`\inetpub\ocr`)
- **Configuration Summary:** `appsettings.json`
- **OCR Service Program Path:** `OCRSetting` -> `ocrPath`
- **OCR Service Work Path:** `OCRSetting` -> `workDirectory`
- **OCR Service Temp Path:** `OCRSetting` -> `workingDirectory`

  #@img_A0006/A0006_0010.png
  
- Click the update function, and click OK to execute
  
  #@img_A0006/A0006_0011.png

- Once the execution is finished, the update is complete

  #@img_A0006/A0006_0012.png

- Start the IIS and PSS services

  #@img_A0006/A0006_0013.png

  #@img_A0006/A0006_0014.png

- Start the IIS and PSS services

### 1.5 Program Rollback Method

#### 1.5.1 IIS WEB Program Rollback

- Go to the directory `C:\inetpub\wwwroot`, unzip `PSSWeb`, and overwrite the files in `C:\inetpub\wwwroot`

#### 1.5.2 Powermoat Service Program Rollback

- Reinstall the older version of the service programs such as (`PSSWEB`, `PSSBatchJob`, `PSSBatchJobCore`, `PSSOCRService`, `PSSMonitor`, `PSSSiteBatchJob`)

#### 1.5.3 Database Rollback
  
- Restore the backed-up `PSSDB`