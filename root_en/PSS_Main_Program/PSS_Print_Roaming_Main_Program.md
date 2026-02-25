# PSS Powermoat Roaming Print Main Program

## Project Overview

Install roaming print main program, including backend, database, and frontend programs.

## 1. Environment Preparation Before Installation

### 1.1 Hardware Requirements

### 1.2 softwareRequirements

- Need to install Windows Server 2022 or higher version
- Need to install database (Microsoft SQL Server 2022)

### 1.3 Installation Files

- PSS Powermoat ISO (PSS_v20250902.iso)

### 1.4 Installation Steps

- Log in to Windows Server as administrator
- Execute via PowerShell (Run As Administrator)

  - Execute PowerShell command, open installation option window, taking (D:) as an example

    ```console
    cd D:
    .\pss_system_install.ps1
    ```

  - Select SQL Express ,and select all PSS services
  
    (PSSWEB,PSSBatchJob,PSSBatchJobCore,PSSOCRService,PSSMonitor,PSSSiteBatchJob)
  
    Click Confirm (Execution takes about 20 minutes)

    #@img_A0001/0001.png

  - When SQL unzip path appears, just click [Confirm]

  - When SQL Server installation options appear

    #### Click New SQL Server

    #@img_A0001/0003.png

    #@img_A0001/0004.png

    #### Do not select [ ]SQL Server Replication , [ ]SQL Machine Learning

    #@img_A0001/0005.png

    #### SQL Server installation completed, click [Close]

    #@img_A0001/0006.png

    #### Click top right to close SQL Server installation options

    #@img_A0001/0003.png

  - When Microsoft SQL Studio installation options appear
  
    #### Click Install Microsoft SQL Studio

    #@img_A0001/0007.png

    #### Microsoft SQL Studio installation completed, click [Close]

    #@img_A0001/0008.png

    #### When installation appears Erlang OTP... ClickNext/安裝

    #@img_A0001/0009.png

    #### Erlang installation completed, click [Close]

    #@img_A0001/0010.png

    #### When installation appears Rabbit MQ Server... ClickNext/安裝

    #@img_A0001/0009.png

    #@img_A0001/0012.png

    #### Rabbit MQ Server installation completed, click [Close]

    #@img_A0001/0009.png

    #### Restart computer
