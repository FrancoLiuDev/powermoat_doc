CREATE DATABASE IF NOT EXISTS prtcnt_ocr;
USE prtcnt_ocr;

CREATE TABLE monthly_print_records_ocr (
    record_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '系統流水號',
    -- period_ym VARCHAR(6) COMMENT '計費期數 (如 202510)',
    
    -- === 來源與時間追蹤 (新增) ===
    file_name VARCHAR(255) COMMENT '來源檔案名稱 (如: 202510_店名_抄表單.PDF)',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '建立時間/辨識時間',
    
    -- 保留辨識到的設備編碼，不設定 FOREIGN KEY (外鍵) 限制
    -- device_code VARCHAR(50) COMMENT '設備編碼 (OCR辨識結果)', 
    
    -- 設備特徵，可用於比對或反查真實設備
    machine_model VARCHAR(50) COMMENT '設備型號',
    serial_number VARCHAR(100) COMMENT '設備序號',
    
    -- === a4 黑白印量辨識結果 ===
    bw_total_a4_pages INT COMMENT '抄表當下黑白總印量 (主來源/最終決定值)',
    bw_total_a4_pages_detail VARCHAR(255) COMMENT '黑白總印量明細 (第二輸入來源/原始辨識字串)',
    
    -- === a4 彩色印量辨識結果 ===
    color_total_a4_pages INT COMMENT '抄表當下彩色總印量 (主來源/最終決定值)',
    color_total_a4_pages_detail VARCHAR(255) COMMENT '彩色總印量明細 (第二輸入來源/原始辨識字串)',

     -- === a3 黑白印量辨識結果 ===
    bw_total_a3_pages INT COMMENT '抄表當下黑白總印量 (主來源/最終決定值)',
    bw_total_a3_pages_detail VARCHAR(255) COMMENT '黑白總印量明細 (第二輸入來源/原始辨識字串)',
    
    -- === a3 彩色印量辨識結果 ===
    color_total_a3_pages INT COMMENT '抄表當下彩色總印量 (主來源/最終決定值)',
    color_total_a3_pages_detail VARCHAR(255) COMMENT '彩色總印量明細 (第二輸入來源/原始辨識字串)',
    
    flag_ocr_check VARCHAR(20) COMMENT '標記狀態',
    remarks TEXT COMMENT '備註說明'
);