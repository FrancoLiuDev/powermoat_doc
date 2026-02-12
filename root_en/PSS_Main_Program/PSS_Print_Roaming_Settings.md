# PSS Powermoat Print Roaming Settings

## Project Overview

PSS Print Server (PSS Server) basic settings, print roaming settings are mainly divided into two parts

- Virtual Printer Queue Installation (Installation of two virtual printers: Roaming LPR, Roaming)

- Roaming print dispatched to physical printers (N units)

## 1. Environment Preparation Before Setup

### 1.1 Hardware Requirements

- Physical printers require IP for each printer and a set printer password

### 1.2 Operational Requirements

- Please install Windows Server LPR/LPD service on Printer Server, refer to instructions [Windows Server LPR Installation]

## 2. Environment Preparation Before Setup

### 2.1 Virtual Printer Printer_Roaming_LPR Installation (User Print Queue)

- 開啟 Print Management softwareInterface

  #@img_A0003/0001.png

- Open Print Server -> ports item, use Add Port

  #@img_A0003/0002.png

- Continue to select Add Port -> Local Port -> Port Name (nil) -> Close
  
  #@img_A0003/0004.png
  
  Users should see a new Port (nil); if not displayed, please operate again

- Open Print Server -> Printers item, operate Add Printer
  
  #@img_A0003/0005.png

- Select Add a new printer using an existing port -> nil (Local port)
  
  #@img_A0003/0006.png

- Select "Use an existing printer driver on the computer"

  #@img_A0003/0007.png

- Input settings
  
  Printer Name (Printer_Roaming_LPR)

  Share this printer (Yes)
  
  #@img_A0003/0008.png

  #@img_A0003/0009.png
  
  #@img_A0003/0010.png

  #@img_A0003/0011.png

- Open Print Server -> ports item, use Add Port

  #@img_A0003/0002.png

- Select Create LPR Port (New LPR Port)
  
  #@img_A0003/0012.png
  
- Input IP and Printer Name  
  
  IP: Local IP
  Printer Name: Name of the created virtual printer  (Printer_Roaming_LPR)
  
  #@img_A0003/0013.png

- After operation, check if a new Port is added

  #@img_A0003/0014.png

### 2.2 Virtual Printer Printer_Roaming Installation (User Print Queue)

- Open Print Server -> Printers item, operate Add Printer

  #@img_A0003/0005.png

- Select Add a new printer using an existing port -> xxx.xxx.xxx.xxx:Printer_Roaming_LPR

  #@img_A0003/0015.png

- Select Printer Driver

  #@img_A0003/0016.png

- Input virtual printer name ex.Printer_Roaming (This printer name is the target for user roaming print)

### 2.3 Physical Printer (Roaming Print Printer)

- 開啟 Print Management softwareInterface
-
