# PSS Powermoat 列印漫游設定

## 專案概述

PSS列印伺服器(PSS Server) 基本設定,列印漫游設定主要分為兩部份

- 虛擬印表機 Queue 安裝 (Roamig LPR,Roamig 兩台虛擬印表機安裝 )

- 漫游的列印派送至實體印表機 (N 台)

## 1、設定前環境準備

### 1.1 硬體需求

- 實體印表機需要各列表機 IP,以及設定印表機密碼

### 1.2 作業需求

- N/A

## 2、設定前環境準備

### 2.1 虛擬印表機 Printer_Roaming_LPR 安裝 (使用者列印佇列)

- 開啟 Print Management 軟體界面

  [![image](http://#@ip/html/doc/images/A0003/0001.png)](http://#@ip/html/doc/images/A0003/0001.png)

- 開啟 Print Server -> ports 項目,使用 Add Port

  [![image](http://#@ip/html/doc/images/A0003/0002.png)](http://#@ip/html/doc/images/A0003/0002.png)

- 接續選擇 Add Port -> Local Port -> Port Name (nil) -> Close
  
  #@img_A0003/0004.png
  
  使用者應該見到一個新的 Port (nil),如果沒有顯示請重新操作一次

- 打開 Print Server -> Printers項目,操作 Add Printer
  
  #@img_A0003/0005.png

- 選擇 Add a new printer using an existing port -> nil (Local port)
  
  #@img_A0003/0006.png

- 選擇 "Use an existing printer driver on the computer"

  #@img_A0003/0007.png

- 輸入設定
  
  Printer Name (Printer_Roaming_LPR)

  Share this printer (Yes)
  
  #@img_A0003/0008.png

  #@img_A0003/0009.png
  
  #@img_A0003/0010.png

  #@img_A0003/0011.png

- 開啟 Print Server -> ports 項目,使用 Add Port
  
  [![image](http://#@ip/html/doc/images/A0003/0002.png)](http://#@ip/html/doc/images/A0003/0002.png)

- 選摜建立 Standard TCP/IP Port (New port)
  
  #@img_A0003/0012.png

- 開啟 Print Server -> ports 項目,使用 Add Port
  
  #@img_A0003/0013.png

- 輸入 IP 以及 Port Name
  
  IP: 本機 IP
  Port Name: 己建立的虛擬印表機名稱  (Printer_Roaming_LPR)
  



### 2.2 虛擬印表機 Printer_Roaming 安裝 (使用者列印佇列)
  
### 2.3 實體印表機 (漫游列印印表機)

- 開啟 Print Management 軟體界面
-
