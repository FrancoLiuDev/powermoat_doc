# PSS Powermoat Version Update Guide

## I. Preparation Before Update

### 1.1 Backup PSSDB (Using SQL EXPRESS as an example)

- Open SQL SERVER STUDIO
  
- Open Databases -> PSSDB
  
  #@img_A0006/A0006_0001.png

- Operate on PSSDB -> Tasks -> Back Up, and record the backup path

  #@img_A0006/A0006_0002.png

  #@img_A0006/A0006_0003.png

### 1.2 Pause Services

- Open the Windows Services management interface
  
  #@img_A0006/A0006_0004.png

- Stop the following Services:

   (PSSWEB, PSSBatchJob, PSSBatchJobCore, PSSOCRService, PSSMonitor, PSSSiteBatchJob)

- Open the IIS management interface

  #@img_A0006/A0006_0005.png

- Select the server and click Stop

  #@img_A0006/A0006_0006.png

### 1.3 Update the Database

- Open the installation ISO
- Open the directory \tools\Database\Upgrade
  
  #@img_A0006/A0006_0007.png

- Find the SQL files that need to be updated (execute them according to the version number and date)
  
  #@img_A0006/A0006_0008.png

  #@img_A0006/A0006_0009.png

- Database update is complete

### 1.4 Update the Main Program

- Open the installation ISO directory
- Open PowerShell as Administrator
- Execute pss_system_update.ps1

  #@img_A0006/A0006_0010.png
  
- Select the update function, and click OK to execute
  
  #@img_A0006/A0006_0011.png

- Once the execution is finished, the update is complete

  #@img_A0006/A0006_0012.png

- Start the IIS and PSS services

  #@img_A0006/A0006_0013.png

  #@img_A0006/A0006_0014.png

- Start the IIS and PSS services

### 1.5 Program Rollback Method

#### 1.5.1 IIS WEB Program Rollback

- Go to the directory C:\inetpub\wwwroot, unzip PSSWeb, and overwrite the files in C:\inetpub\wwwroot

#### 1.5.2 Powermoat Service Program Rollback

- Reinstall the older version of the service programs such as (PSSWEB, PSSBatchJob, PSSBatchJobCore, PSSOCRService, PSSMonitor, PSSSiteBatchJob)

#### 1.5.3 Database Rollback
  
- Restore the backed-up PSSDB