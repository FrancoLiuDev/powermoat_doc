# PSS Powermoat Print Roaming Main Program

## Project Overview

Install the print roaming main program, including backend, database, and frontend components.

## 1. Pre-installation Environment Preparation

### 1.1 Hardware Requirements

### 1.2 Software Requirements

- Requires Windows Server 2022 or higher
- Requires database installation (Microsoft SQL Server 2022)

### 1.3 Installation Files

- PSS Powermoat ISO (PSS_v20250902.iso)

### 1.4 Installation Steps

- Login to Windows Server as administrator
- Run PowerShell (Run As Administrator)

  - Execute PowerShell command to open the installation options window, using (D:) as an example

    ```console
    cd D:
    .\pss_system_install.ps1
    ```

  - Select install SQL Express and select all PSS services
  
    (PSSWEB, PSSBatchJob, PSSBatchJobCore, PSSOCRService, PSSMonitor, PSSSiteBatchJob)
  
    Click Confirm (installation takes approximately 20 minutes)

    [![image](http://#@ip/html/doc/images/A0001/0001.png)](http://#@ip/html/doc/images/A0001/0001.png)

  - When the SQL extraction path appears, just click [Confirm]
  
    [![image](http://#@ip/html/doc/images/A0001/0002.png)](http://#@ip/html/doc/images/A0001/0002.png)

  - When the SQL Server installation options appear

    #### Click New SQL Server

    [![image](http://#@ip/html/doc/images/A0001/0003.png)](http://#@ip/html/doc/images/A0001/0003.png)

    [![image](http://#@ip/html/doc/images/A0001/0004.png)](http://#@ip/html/doc/images/A0001/0003.png)

    #### Do not select [ ] SQL Server Replication , [ ] SQL Machine Learning

    [![image](http://#@ip/html/doc/images/A0001/0005.png)](http://#@ip/html/doc/images/A0001/0005.png)

    #### SQL Server installation complete, click [Close]

    [![image](http://#@ip/html/doc/images/A0001/0006.png)](http://#@ip/html/doc/images/A0001/0006.png)

    #### Click the upper right to close SQL Server installation options

    [![image](http://#@ip/html/doc/images/A0001/0003.png)](http://#@ip/html/doc/images/A0001/0003.png)

  - When Microsoft SQL Studio installation options appear
  
    #### Click to install Microsoft SQL Studio

    [![image](http://#@ip/html/doc/images/A0001/0007.png)](http://#@ip/html/doc/images/A0001/0007.png)

    #### Microsoft SQL Studio installation complete, click [Close]

    [![image](http://#@ip/html/doc/images/A0001/0008.png)](http://#@ip/html/doc/images/A0001/0008.png)

    #### Erlang OTP installation appears... Click Next/Install

    [![image](http://#@ip/html/doc/images/A0001/0009.png)](http://#@ip/html/doc/images/A0001/0009.png)

    #### Erlang installation complete, click [Close]

    [![image](http://#@ip/html/doc/images/A0001/0010.png)](http://#@ip/html/doc/images/A0001/0010.png)

    #### Rabbit MQ Server installation appears... Click Next/Install

    [![image](http://#@ip/html/doc/images/A0001/0009.png)](http://#@ip/html/doc/images/A0001/0011.png)

    [![image](http://#@ip/html/doc/images/A0001/0009.png)](http://#@ip/html/doc/images/A0001/0012.png)

    #### Rabbit MQ Server installation complete, click [Close]

    [![image](http://#@ip/html/doc/images/A0001/0009.png)](http://#@ip/html/doc/images/A0001/0013.png)

    #### Restart the computer
