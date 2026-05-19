CREATE DATABASE IF NOT EXISTS prtcnt;
USE prtcnt;

-- 0. 客戶基本檔 (customers)
CREATE TABLE customers (
    customer_code VARCHAR(20) PRIMARY KEY COMMENT '客戶編碼 (唯一值)',
    customer_name VARCHAR(100) COMMENT '客戶/公司名稱',
    tax_id VARCHAR(8) COMMENT '統一編號',
    contact_person VARCHAR(50) COMMENT '聯絡人姓名',
    contact_phone VARCHAR(50) COMMENT '聯絡電話',
    address VARCHAR(200) COMMENT '總公司/帳單地址'
);

-- 1. 門市基本檔 (stores)
CREATE TABLE stores (
    store_code VARCHAR(20) PRIMARY KEY COMMENT '門市編碼 (唯一值)',
    customer_code VARCHAR(20) COMMENT '客戶編碼',
    operation_unit VARCHAR(50) COMMENT '營運別',
    department VARCHAR(50) COMMENT '隸屬部別',
    store_name VARCHAR(100) COMMENT '門市名稱',
    FOREIGN KEY (customer_code) REFERENCES customers(customer_code)
);

-- 2. 設備基本檔 (devices)
CREATE TABLE devices (
    device_code VARCHAR(50) PRIMARY KEY COMMENT '設備編碼 (唯一值)',
    store_code VARCHAR(20) COMMENT '部署的門市編碼',
    machine_model VARCHAR(50) COMMENT '機器型號',
    serial_number VARCHAR(100) COMMENT '機器原廠序號',
    install_date DATE COMMENT '安裝日期',
    status VARCHAR(20) COMMENT '設備狀態',
    FOREIGN KEY (store_code) REFERENCES stores(store_code)
);

-- 3. 每月抄表紀錄檔 (monthly_print_records) 
-- 移除列印覆蓋率、碳粉殘留啪數，僅記錄抄表當下機器面板上的真實總印量
CREATE TABLE monthly_print_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '系統流水號',
    period_ym VARCHAR(6) COMMENT '計費期數 (如 202510)',
    device_code VARCHAR(50) COMMENT '設備編碼',
    bw_total_pages INT COMMENT '抄表當下黑白總印量',
    color_total_pages INT COMMENT '抄表當下彩色總印量',
    remarks TEXT COMMENT '備註說明',
    FOREIGN KEY (device_code) REFERENCES devices(device_code)
);

-- 4. 檢視表 (View)：每月印量動態計算
-- 利用 LAG() 尋找上一期總印量並相減，自動算出當月實際用量
CREATE VIEW vw_monthly_usage AS
SELECT 
    current_mpr.period_ym,
    s.store_name,
    d.device_code,
    d.machine_model,
    current_mpr.bw_total_pages AS current_bw_total,  -- 抄表當下黑白總印量
    
    -- 本期總印量 - 上期總印量 = 當月黑白用量
    (current_mpr.bw_total_pages - COALESCE(LAG(current_mpr.bw_total_pages) OVER (
        PARTITION BY current_mpr.device_code 
        ORDER BY current_mpr.period_ym
    ), current_mpr.bw_total_pages)) AS bw_printed_pages, 
    
    -- 本期總印量 - 上期總印量 = 當月彩色用量
    (current_mpr.color_total_pages - COALESCE(LAG(current_mpr.color_total_pages) OVER (
        PARTITION BY current_mpr.device_code 
        ORDER BY current_mpr.period_ym
    ), current_mpr.color_total_pages)) AS color_printed_pages 

FROM monthly_print_records current_mpr
JOIN devices d ON current_mpr.device_code = d.device_code
JOIN stores s ON d.store_code = s.store_code;