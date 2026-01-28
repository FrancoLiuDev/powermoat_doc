# PSS Powermoat 列印漫游設定

## 專案概述

PSS列印伺服器(PSS Server) 基本設定,列印漫游設定主要分為兩部份

### 使用者進行列印工作
  
  在漫游的列印工作中,使用者列印的對象是虛擬印表機.

### PSS 漫游列印派送工作
  
  漫游的列印派送至實體印表機

## 1、設定前環境準備

### 1.1 硬體需求

- 實體印表機需要各列表機 IP,以及設定印表機密碼

### 1.2 作業需求

- N/A

## 2、設定前環境準備

### 2.1 使用者列印佇列設定

- 開啟 Print Management 軟體界面

  [![image](http://#@ip/html/doc/images/A0003/0001.png)](http://#@ip/html/doc/images/A0003/0001.png)

- 開啟 Print Server -> ports 項目,使用 Add Port

  [![image](http://#@ip/html/doc/images/A0003/0002.png)](http://#@ip/html/doc/images/A0003/0002.png)

- 接續選擇 Add Port -> Local Port -> Port Name (nil) -> Close
  
  0004圖
  
  使用者應該見到一個新的 Port (nil),如果沒有顯示請重新操作一次

- 打開 Print Server -> Printers項目,操作 Add Printer
  
  0005圖

- 選擇 Add a new printer using an existing port -> nil (Local port)
  0006圖

- 選擇 Install a new drivr

  0007圖
