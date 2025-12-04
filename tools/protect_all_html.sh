#!/bin/bash

# 批次保護 HTML 文件

INPUT_DIR=${1:-"./docs"}
OUTPUT_DIR=${2:-"./protected_html"}

echo "📦 批次保護 HTML 文件"
echo "===================="
echo ""
echo "📂 輸入目錄: $INPUT_DIR"
echo "📤 輸出目錄: $OUTPUT_DIR"
echo ""

# 創建輸出目錄
mkdir -p "$OUTPUT_DIR"

count=0
for html_file in "$INPUT_DIR"/*.html; do
    if [ -f "$html_file" ]; then
        filename=$(basename "$html_file")
        output_file="$OUTPUT_DIR/$filename"
        
        echo "🔒 處理: $filename"
        python3 tools/pack_html.py "$html_file" "$output_file" --minify
        
        if [ $? -eq 0 ]; then
            ((count++))
        fi
        echo ""
    fi
done

echo "================================"
echo "✨ 完成！共處理 $count 個文件"
echo "📂 保護後的文件: $OUTPUT_DIR"
echo "================================"
