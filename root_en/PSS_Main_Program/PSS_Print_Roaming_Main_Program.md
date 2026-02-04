# PSS Powermoat Print Roaming Main Program

## Project Overview

Install the Print Roaming main program, including the backend, database, and frontend programs.

## I. Pre-installation Environment Preparation

### 1.1 Hardware Requirements

### 1.2 Software Requirements

- Windows Server 2022 or higher is required
- Database installation is required (Microsoft SQL Server 2022)

### 1.3 Installation Files

- PSS Powermoat ISO (PSS_v20250902.iso)

### 1.4 Installation Steps

- Log in to Windows Server as an administrator (administrator)
- Run PowerShell (Run As Administrator)

  - Execute PowerShell commands to open the installation option window, taking (D:) as an example

    ```console
    cd D:
    .\pss_system_install.ps1
    ```

  - Select to install SQL Express, and select all PSS services
  
    (PSSWEB, PSSBatchJob, PSSBatchJobCore, PSSOCRService, PSSMonitor, PSSSiteBatchJob)
  
    Click Confirm (Execution takes about 20 minutes)

    [![image](http://#@ip/html/doc/images/A0001/0001.png)](http://#@ip/html/doc/images/A0001/0001.png)

  - When the SQL extraction path appears, just click [Confirm]
  
    [![image](http://#@ip/html/doc/images/A0001/0002.png)](http://#@ip/html/doc/images/A0001/0002.png)

  - When the SQL Server installation options appear

    #### Click New SQL Server

    [![image](http://#@ip/html/doc/images/A0001/0003.png)](http://#@ip/html/doc/images/A0001/0003.png)

    [![image](http://#@ip/html/doc/images/A0001/0004.png)](http://#@ip/html/doc/images/A0001/0003.png)

    #### Do NOT select [ ]SQL Server Replication, [ ]SQL Machine Learning

    [![image](http://#@ip/html/doc/images/A0001/0005.png)](http://#@ip/html/doc/images/A0001/0005.png)

    #### SQL Server installation completed, click [Close]

    [![image](http://#@ip/html/doc/images/A0001/0006.png)](http://#@ip/html/doc/images/A0001/0006.png)

    #### Click on the top right to close SQL Server installation options

    [![image](http://#@ip/html/doc/images/A0001/0003.png)](http://#@ip/html/doc/images/A0001/0003.png)

  - When the Microsoft SQL Studio installation options appear
  
    #### Click to install Microsoft SQL Studio

    [![image](http://#@ip/html/doc/images/A0001/0007.png)](http://#@ip/html/doc/images/A0001/0007.png)

    #### Microsoft SQL Studio installation completed, click [Close]

    [![image](http://#@ip/html/doc/images/A0001/0008.png)](http://#@ip/html/doc/images/A0001/0008.png)

    #### "Install Erlang OTP..." appears, click Next/Install

    [![image](http://#@ip/html/doc/images/A0001/0009.png)](http://#@ip/html/doc/images/A0001/0009.png)

    #### Erlang installation completed, click [Close]

    [![image](http://#@ip/html/doc/images/A0001/0010.png)](http://#@ip/html/doc/images/A0001/0010.png)

    #### "Install Rabbit MQ Server..." appears, click Next/Install

    [![image](http://#@ip/html/doc/images/A0001/0009.png)](http://#@ip/html/doc/images/A0001/0011.png)

    [![image](http://#@ip/html/doc/images/A0001/0009.png)](http://#@ip/html/doc/images/A0001/0012.png)

    #### Rabbit MQ Server installation completed, click [Close]

    [![image](http://#@ip/html/doc/images/A0001/0009.png)](http://#@ip/html/doc/images/A0001/0013.png)

    #### Restart the computer
