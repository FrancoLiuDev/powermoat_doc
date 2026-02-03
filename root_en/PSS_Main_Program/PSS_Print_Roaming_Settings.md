# PSS Powermoat Print Roaming Settings

## Project Overview

PSS Print Server (PSS Server) basic settings. Print roaming settings are mainly divided into two parts:

- Virtual printer queue installation (Roaming_LPR and Roaming virtual printers installation)

- Roaming print dispatch to physical printers (N units)

## 1. Pre-configuration Environment Preparation

### 1.1 Hardware Requirements

- Physical printers require each printer's IP address and printer password configuration

### 1.2 Operational Requirements

- N/A

## 2. Configuration Setup

### 2.1 Virtual Printer Printer_Roaming_LPR Installation (User Print Queue)

- Open Print Management software interface

  [![image](http://#@ip/html/doc/images/A0003/0001.png)](http://#@ip/html/doc/images/A0003/0001.png)

- Open Print Server -> ports section, use Add Port

  [![image](http://#@ip/html/doc/images/A0003/0002.png)](http://#@ip/html/doc/images/A0003/0002.png)

- Continue selecting Add Port -> Local Port -> Port Name (nil) -> Close
  
  #@img_A0003/0004.png
  
  Users should see a new Port (nil), if not displayed please repeat the operation

- Open Print Server -> Printers section, perform Add Printer operation
  
  #@img_A0003/0005.png

- Select "Add a new printer using an existing port" -> nil (Local port)
  
  #@img_A0003/0006.png

- Select "Use an existing printer driver on the computer"

  #@img_A0003/0007.png

- Enter settings
  
  Printer Name (Printer_Roaming_LPR)

  Share this printer (Yes)
  
  #@img_A0003/0008.png

  #@img_A0003/0009.png
  
  #@img_A0003/0010.png

  #@img_A0003/0011.png

- Open Print Server -> ports section, use Add Port
  
  [![image](http://#@ip/html/doc/images/A0003/0002.png)](http://#@ip/html/doc/images/A0003/0002.png)

- Select to create Standard TCP/IP Port (New port)
  
  #@img_A0003/0012.png

- Open Print Server -> ports section, use Add Port
  
  #@img_A0003/0013.png

- Enter IP and Port Name
  
  IP: Local machine IP
  Port Name: Previously created virtual printer name (Printer_Roaming_LPR)

### 2.2 Virtual Printer Printer_Roaming Installation (User Print Queue)
  
### 2.3 Physical Printers (Roaming Print Printers)

- Open Print Management software interface
